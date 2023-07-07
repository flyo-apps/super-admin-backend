from fastapi import APIRouter, Depends, HTTPException, Security
from db.aurora import auroradb
from sqlalchemy.orm import Session
from auth.authentication_user import get_current_active_user
from influencer.crud.store import InfluencerStoreCollection

router = APIRouter()

@router.get(
    "/v1/influencer/store/get_store_by_name",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_store_by_name(
    influencer_handle: str,
    store_name: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        influencer_store_collection = InfluencerStoreCollection()
        return await influencer_store_collection.get_store_by_name(db=db, influencer_handle=influencer_handle, store_name=store_name)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")