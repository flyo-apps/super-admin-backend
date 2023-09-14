import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from orders.routers import (
    coupons
)

from items.routers import (
    shipping_data,
    products,
    product_variants,
    product_reviews,
    blogs,
    categories,
    homepage,
    brands,
    brands_collection,
    usecases,
    stories,
    multi_stories,
    quick_filters,
    quick_banners,
    product_collection,
    rate_breakup,
    blog_for_listing_page
)

from influencer.routers import (
    store
)

from db.mongo.mongo_adaptor import (
    close_mongo_connection,
    connect_to_mongo
)

from auth.router import (
    auth
)

from extras.routers import (
    asset_metadata
)

from master.routers import (
    healthcheck
)

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

def config_logging(level=logging.INFO):
    # When run by 'uvicorn ...', a root handler is already
    # configured and the basicConfig below does nothing.
    # To get the desired formatting:
    logging.getLogger().handlers.clear()

    # 'uvicorn --log-config' is broken so we configure in the app.
    #   https://github.com/encode/uvicorn/issues/511
    logging.basicConfig(
        # match gunicorn format
        format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S %z]",
        level=level,
    )

    # When run by 'gunicorn -k uvicorn.workers.UvicornWorker ...',
    # These loggers are already configured and propogating.
    # So we have double logging with a root logger.
    # (And setting propagate = False hurts the other usage.)
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = True
    logging.getLogger("uvicorn.error").propagate = True


config_logging()

origins = [
    "http://localhost:*",
    "http://localhost:3000",
    "https://dev.mable.jewelry",
    "https://www.mabel.jewelry",
    "https://mabel.jewelry",
    "https://www.googletagmanager.com",
    "https://super-ecom-app.vercel.app",
    "http://192.168.12.111:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "DELETE", "PUT"],
    allow_headers=[
        "x-requested-with",
        "Content-Type",
        "origin",
        "authorization",
        "accept",
        "client-security-token",
    ],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# AUTH ROUTERS
app.include_router(auth.router, tags=["Auth"])

# ITEMS ROUTERS
app.include_router(blog_for_listing_page.router, tags=["Blog for Listing Page"])
app.include_router(shipping_data.router, tags=["Shipping Data"])
app.include_router(products.router, tags=["Products"])
app.include_router(rate_breakup.router, tags=["Rate Breakup"]),
app.include_router(product_variants.router, tags=["Product Variants"])
app.include_router(product_reviews.router, tags=["Product Reviews"])
app.include_router(blogs.router, tags=["Blogs"])
app.include_router(categories.router, tags=["Categories"])
app.include_router(brands.router, tags=["Brands"])
app.include_router(brands_collection.router, tags=["Brands Collection"])
app.include_router(homepage.router, tags=["Homepage"])
app.include_router(usecases.router, tags=["Usecases"])
app.include_router(stories.router, tags=["Stories"])
app.include_router(multi_stories.router, tags=["Multi Stories"])
app.include_router(quick_filters.router, tags=["Quick Filters"])
app.include_router(quick_banners.router, tags=["Quick Banners"])
app.include_router(product_collection.router, tags=["Product Collection"])

# Coupons ROUTERS
app.include_router(coupons.router, tags=["Coupons"])

# Influencer ROUTERS
app.include_router(store.router, tags=["Influencer Store"])

# ASSET METADATA ROUTES
app.include_router(asset_metadata.router, tags=["Asset Metadata"])

# MASTER ROUTERS
app.include_router(healthcheck.router, tags=["Health Check"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
