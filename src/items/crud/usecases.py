from datetime import datetime
from fastapi import HTTPException
import os
from ..utils.constants import USECASE_COL_RETURN
from ..models.usecases import (
    UsecaseUpdateBaseModel,
    UsecaseCreateBaseModel,
    UsecaseCreateModel,
    UsecaseDeleteModel,
    UsecaseUpdateModel
)
from ..schemas.usecases import (
    UsecasesSchema
)

from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session

class UsecaseCollection:
    def __init__(self):
        self.model = CRUDBase(UsecasesSchema)

    async def create_usecase(
        self,
        usecase_details: UsecaseCreateBaseModel,
        db: Session
    ) -> any:
        try:
            existing_usecase = self.model.get_one(db=db, code=usecase_details.code)
            if existing_usecase is not None:
                return

            usecase_create = UsecaseCreateModel(**usecase_details.dict())
            created_usecase = self.model.create(db=db, obj_in=usecase_create)

            return created_usecase if created_usecase else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    async def update_usecase(
        self,
        usecase_update_details: UsecaseUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            usecase = self.model.get_one(db=db, code=usecase_update_details.code)
            if usecase == None:
                return {"internal_response_code": 1, "code": usecase_update_details.code, "message": "Usecase not found"}

            usecase_update = UsecaseUpdateModel(**usecase_update_details.dict(exclude_unset=True))
            usecase_update.is_updated = True
            usecase_update.updated_at = datetime.now()
            updated_usecase = self.model.update(db=db, db_obj=usecase,obj_in=usecase_update)
            return {"internal_response_code": 0, "code": updated_usecase.code, "message": "Usecase updated"} if updated_usecase else {"internal_response_code": 1, "code": updated_usecase.code, "message": "Usecase not updated"}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_usecase(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            usecase_delete = UsecaseDeleteModel(code=code)
            usecase_delete_dict = usecase_delete.dict()
            usecase = self.model.get_one(db=db, code=code)
            if usecase == None:
                {"internal_response_code": 1, "code": code, "message": "Usecase not found"}
            deleted_usecase = self.model.update(db=db, db_obj=usecase,obj_in=usecase_delete_dict)

            return {"internal_response_code": 0, "code": code, "message": "Usecase deleted"} if deleted_usecase else {"internal_response_code": 1, "code": code, "message": "Usecase not deleted"} 
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def get_usecase(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            usecase = self.model.get_one(db=db, code=code, column_load=USECASE_COL_RETURN)

            return usecase if usecase else None
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

            