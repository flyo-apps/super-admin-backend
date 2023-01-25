from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from db.mongo.collections import COUPONS
from db.mongo.mongo_base import MongoBase
from master.models.master import BaseIsCreated
from ..models.coupons import (
    CouponsModelOut,
    CouponCreateModel,
    CouponUpdateModel
)

class CouponsCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(COUPONS)


    async def create_coupon(
        self,
        coupon_details: CouponCreateModel
    ) -> any:
        try:
            existing_coupon = await self.get_coupon_by_code(coupon_code=coupon_details.coupon_code)

            if existing_coupon is not None:
                return { "internal_response_code": 1, "message": "Coupon code already present" }

            details = CouponCreateModel(
                **coupon_details.dict()
            )
            details.updated_at = datetime.now()

            details.created_on = datetime.now()

            insert_id = await self.collection.insert_one(
                details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated
            )

            return { "internal_response_code": 0, "data": {"coupon_id": str(insert_id)}, "message": "Coupon created" } if insert_id else { "internal_response_code": 1, "message": "Coupon not created" }

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_coupon(
        self,
        coupon_update_details: CouponUpdateModel
    ) -> any:
        try:
            coupon = await self.get_coupon_by_code(coupon_code=coupon_update_details.coupon_code)

            if coupon == None:
                return {"internal_response_code": 1, "coupon_code": coupon_update_details.coupon_code, "message": "Coupon not found"}

            coupon_update = CouponUpdateModel(**coupon_update_details.dict(exclude_unset=True))
            coupon_update.is_updated = True
            coupon_update.updated_at = datetime.now()
            coupon_update_dict = coupon_update.dict(exclude_unset=True)

            finder = { "coupon_code": coupon_update_details.coupon_code }
            updater = { "$set": coupon_update_dict }
            updated_coupon = await self.collection.find_one_and_modify(find=finder, update=updater)

            return { "internal_response_code": 0, "data": {"coupon_code": coupon_update_details.coupon_code}, "message": "Coupon updated" } if updated_coupon else { "internal_response_code": 1, "coupon_code": coupon_update_details.coupon_code, "message": "Coupon not updated" }

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_coupon_by_code(
        self,
        coupon_code: str
    ) -> any:
        try:
            finder = {
                "$or":[
                    {"coupon_code": coupon_code},
                    {"coupon_code": coupon_code.upper()},
                    {"coupon_code": coupon_code.lower()}
                ],
                "is_deleted": False
            }

            coupon = await self.collection.find_one(
                finder=finder,
                return_doc_id=True,
                extended_class_model=CouponsModelOut
            )

            if coupon is None:
                random_coupons_collection = RandomCouponsCollection()
                coupon = await random_coupons_collection.get_random_coupon_by_code(coupon_code=coupon_code)

            return coupon if coupon else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def coupon_by_code(
        self,
        coupon_code: str
    ) -> any:
        try:
            finder = {
                "$or":[
                    {"coupon_code": coupon_code},
                    {"coupon_code": coupon_code.upper()},
                    {"coupon_code": coupon_code.lower()}
                ],
                "is_deleted": False
            }

            coupon = await self.collection.find_one(
                finder=finder,
                return_doc_id=True,
                extended_class_model=CouponsModelOut
            )

            return coupon if coupon else None

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_coupon(
        self,
        coupon_id: str
    ) -> any:
        try:
            finder = {"_id": ObjectId(coupon_id)}
            updater = {"$set": {"is_deleted": True, "deleted_on": datetime.now()}}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CouponsModelOut,
                insert_if_not_found=False,
                return_updated_document=True
            )

            return result
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")