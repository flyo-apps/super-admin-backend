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
)

from db.mongo.mongo_adaptor import (
    close_mongo_connection,
    connect_to_mongo
)

from auth.router import (
    auth
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
app.include_router(shipping_data.router, tags=["Shipping Data"])
app.include_router(products.router, tags=["Products"])
app.include_router(product_variants.router, tags=["Product Variants"])
app.include_router(product_reviews.router, tags=["Product Reviews"])
app.include_router(blogs.router, tags=["Blogs"])
app.include_router(categories.router, tags=["Categories"])
app.include_router(brands.router, tags=["Brands"])
app.include_router(brands_collection.router, tags=["Brands Collection"])
app.include_router(homepage.router, tags=["Homepage"])

# Coupons ROUTERS
app.include_router(coupons.router, tags=["Coupons"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
