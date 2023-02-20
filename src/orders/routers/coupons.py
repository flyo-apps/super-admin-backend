from fastapi import APIRouter, HTTPException, Security
from auth.authentication_user import get_current_active_user
from ..crud.coupons import CouponsCollection
from ..models.coupons import (
    CouponCreateModel,
    CouponUpdateModel
)

router = APIRouter()

@router.post(
    "/v1/create_coupon",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])]
)
async def create_coupon(
    coupon_details: CouponCreateModel
):
    try:
        coupons_collection = CouponsCollection()

        return await coupons_collection.create_coupon(coupon_details=coupon_details)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_coupon",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_coupon(
    coupon_update_details: CouponUpdateModel,
):
    try:
        coupons_collection = CouponsCollection()
        return await coupons_collection.update_coupon(coupon_update_details=coupon_update_details)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/delete_coupon",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_coupon(
    coupon_id: str
):
    try:
        coupons_collection = CouponsCollection()

        return await coupons_collection.delete_coupon(
            coupon_id=coupon_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_coupon_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_coupon_by_code(
    coupon_code: str
):
    try:
        coupons_collection = CouponsCollection()

        coupon = await coupons_collection.coupon_by_code(
            coupon_code=coupon_code
        )

        return { "internal_response_code": 0, "data": coupon } if coupon else { "internal_response_code": 1, "message": f"""Coupon with code: {coupon_code} not found""" }

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
