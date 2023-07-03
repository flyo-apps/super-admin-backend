from fastapi import HTTPException
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session
from influencer.schemas.store import InfluencerStoreSchema

class InfluencerStoreCollection:
    def __init__(self) -> None:
        self.influencer_store_model = CRUDBase(InfluencerStoreSchema)
  
    async def get_store(
        self,
        store_code: str,
        db: Session,
    ) -> any:
        try:
            store = self.influencer_store_model.get_one(db=db, code=store_code)
            return store
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong") 
