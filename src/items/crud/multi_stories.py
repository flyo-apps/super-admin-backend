from datetime import datetime
from fastapi import HTTPException
from ..models.multi_stories import (
    MultiStoryCreateBaseModel,
    MultiStoryCreateModel,
    MultiStoryUpdateBaseModel,
    MultiStoryUpdateModel,
    MultiStoryDeleteModel
)
from ..schemas.multi_stories import (
    MultiStoriesSchema
)
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session
from typing import List

class MultiStoriesCollection:
    def __init__(self):
        self.model = CRUDBase(MultiStoriesSchema)

    async def create_story(
        self,
        story_details: MultiStoryCreateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{story_details.code}'"""
            existing_story = self.model.get_one(db=db, where_clause=where_clause)
            if existing_story is not None:
                return {"internal_response_code": 1, "message": f"""story with code {story_details.code} exists"""}

            story_create = MultiStoryCreateModel(**story_details.dict())
            created_story = self.model.create(db=db, obj_in=story_create)

            return {"internal_response_code": 0, "message": f"""created story {story_details.code}"""} if created_story else {"internal_response_code": 1, "message": f"""failed to create story {story_details.code}"""}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_story(
        self,
        story_update_details: MultiStoryUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{story_update_details.code}'"""
            existing_story = self.model.get_one(db=db, where_clause=where_clause)
            if existing_story is None:
                return {"internal_response_code": 1, "message": f"""story {story_update_details.code} not found"""}

            story_update = MultiStoryUpdateModel(**story_update_details.dict(exclude_unset=True))
            story_update.is_updated = True
            story_update.updated_at = datetime.now()
            updated_story = self.model.update(db=db, db_obj=existing_story, obj_in=story_update)
            
            return {"internal_response_code": 0, "message": f"""story {story_update_details.code} updated"""} if updated_story else {"internal_response_code": 1, "message": f"""failed to update story {story_update_details.code}"""}
            
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_story_by_code(
        self,
        story_code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(code='{story_code}' AND is_deleted=false)"""
            existing_story = self.model.get_one(db=db, where_clause=where_clause)

            return existing_story if existing_story else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def upsert_multiple_stories(
        self,
        story_details: List[MultiStoryCreateBaseModel],
        db: Session
    ) -> any:
        try:
            codes = ','.join(["'" + data.code + "'" for data in story_details])
            existing_codes = []
            where_clause = f"""code IN ({codes})"""
            existing_stories = self.model.get_all(db=db, where_clause=where_clause,skip=0,limit=len(story_details))
            if existing_stories:
                existing_codes = [data.code for data in existing_stories]

            stories_create = []
            stories_update = []
            for story in story_details:
                if story.code not in existing_codes:
                    story_create = MultiStoryCreateModel(**story.dict())
                    stories_create.append(story_create.dict())
                else:
                    story_update = MultiStoryUpdateModel(**story.dict())
                    story_update.is_updated = True
                    story_update.updated_at = datetime.now()
                    stories_update.append(story_update.dict())

            res = self.model.bulk_upsert(db=db, update_vals=stories_update, insert_vals=stories_create)
            return {"internal_response_code": 0, "message": f"""story created for {len(stories_create)} codes and updated for {len(stories_update)} codes"""} if res is None else {"internal_response_code": 1, "message": f"""upsert operation failed"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_story_by_code(
        self,
        story_code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{story_code}' AND is_deleted=false"""
            existing_story = self.model.get_one(db=db, where_clause=where_clause)
            if existing_story is None:
                return {"internal_response_code": 1, "message": f"""story {story_code} not found"""}

            story_delete_dict = MultiStoryDeleteModel(code=story_code).dict()
            deleted_story = self.model.update(db=db, db_obj=existing_story, obj_in=story_delete_dict)

            return {"internal_response_code": 0, "message": f"""story {story_code} deleted"""} if deleted_story else {"internal_response_code": 1, "message": f"""failed to delete story {story_code}"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")
