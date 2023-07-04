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

    async def get_store_by_name(
        self,
        store_name: str,
        influencer_handle: str,
        db: Session,
    ) -> any:
        try:
            store = self.influencer_store_model.get_one(db=db, where_clause=f"""lower(influencer_handle)='{influencer_handle.lower()}' and lower(name)='{store_name.lower()}'""")
            return {"internal_response_code": 0, "message": "success", "data": store} if store else {"internal_response_code": 1, "message": 'failed', "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong") 
