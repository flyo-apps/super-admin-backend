from fastapi import HTTPException
from db.mongo.collections import RANDOM_COUPONS
from db.mongo.mongo_base import MongoBase
from ..models.coupons import CouponsModelOut

class RandomCouponsCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(RANDOM_COUPONS)

    async def get_random_coupon_by_code(
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