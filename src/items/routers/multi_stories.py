from fastapi import APIRouter, Depends, HTTPException, Security
from db.aurora import auroradb
from sqlalchemy.orm import Session
from auth.authentication_user import get_current_active_user
from items.crud.multi_stories import MultiStoriesCollection
from items.models.multi_stories import MultiStoryCreateBaseModel, MultiStoryUpdateBaseModel

from typing import List

router = APIRouter()

@router.post(
    "/v1/multi_stories/add_story",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_story(
    story: MultiStoryCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        multi_story_collection = MultiStoriesCollection()
        return await multi_story_collection.create_story(story_details=story,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.delete(
    "/v1/multi_stories/delete_story_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_story_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        multi_story_collection = MultiStoriesCollection()
        return await multi_story_collection.delete_story_by_code(story_code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/multi_stories/get_story_by_code",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_story_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        multi_story_collection = MultiStoriesCollection()
        return await multi_story_collection.get_story_by_code(story_code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put(
    "/v1/multi_stories/update_story",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_story(
    story_details: MultiStoryUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        multi_story_collection = MultiStoriesCollection()
        return await multi_story_collection.update_story(story_update_details=story_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/multi_stories/upsert_stories",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def upsert_stories(
    story_details: List[MultiStoryCreateBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        multi_story_collection = MultiStoriesCollection()
        return await multi_story_collection.upsert_multiple_stories(story_details=story_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
