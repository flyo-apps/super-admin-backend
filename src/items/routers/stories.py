from fastapi import APIRouter, Depends, HTTPException, Security
from db.aurora import auroradb
from sqlalchemy.orm import Session
from auth.authentication_user import get_current_active_user
from items.crud.stories import StoriesCollection
from items.models.stories import StoryCreateBaseModel, StoryUpdateBaseModel

from typing import List

router = APIRouter()

@router.post(
    "/v1/stories/add_story",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_story(
    story: StoryCreateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        story_collection = StoriesCollection()
        return await story_collection.create_story(story_details=story,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.delete(
    "/v1/stories/delete_story_by_code",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_story_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        story_collection = StoriesCollection()
        return await story_collection.delete_story_by_code(story_code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/stories/get_story_by_code",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_story_by_code(
    code: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        story_collection = StoriesCollection()
        return await story_collection.get_story_by_code(story_code=code, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put(
    "/v1/stories/update_story",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_story(
    story_details: StoryUpdateBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        story_collection = StoriesCollection()
        return await story_collection.update_story(story_update_details=story_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post(
    "/v1/stories/upsert_stories",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def upsert_stories(
    story_details: List[StoryCreateBaseModel],
    db: Session = Depends(auroradb.get_db)
):
    try:
        story_collection = StoriesCollection()
        return await story_collection.upsert_multiple_stories(story_details=story_details, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
