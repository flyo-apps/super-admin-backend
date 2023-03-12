from datetime import date, datetime
from fastapi import HTTPException
from typing import List

from extras.schemas.asset_metadata import AssetMetadataSchema
from extras.models.asset_metadata import (
    CreateAssetMetaDataBaseModel,
    CreateAssetMetaDataModel
)
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session
from sqlalchemy import exc


class AssetMetaDataCollection:
    def __init__(self):
        self.model = CRUDBase(AssetMetadataSchema)
    
    async def create_asset_metadata(
        self,
        create_asset_metadata_base: CreateAssetMetaDataBaseModel,
        db: Session
    ) -> any:
        try:
            create_asset_metadata = CreateAssetMetaDataModel(**create_asset_metadata_base.dict(), created_at=datetime.now())
            asset_metadata = self.model.create(db=db, obj_in=create_asset_metadata)
            
            return {"internal_response_code": 0, "message": "success", "data": None} if asset_metadata else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception as e:
            if type(e) == exc.IntegrityError:                
                try: 
                    db.rollback()
                    where_clause = f"""name='{create_asset_metadata.name}'"""
                    update_values = {
                        "link": create_asset_metadata.link,
                        "type": create_asset_metadata.type,
                        "dimension": create_asset_metadata.dimension,
                        "is_updated": True,
                        "updated_at": datetime.now()
                    }
                    asset_metadata = self.model.filter_update(db=db, where_clause=where_clause, update_values=update_values)
                    return {"internal_response_code": 0, "message": "success", "data": None} 
                except Exception as e:
                    raise HTTPException(status_code=500, detail="Something went wrong")

            raise HTTPException(status_code=500, detail="Something went wrong")


    async def get_asset_metadata(
        self,
        name: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""name='{name}'"""
            asset_metadata = self.model.get_one(db=db, where_clause=where_clause)
            
            return {"internal_response_code": 0, "message": "success", "data": asset_metadata} if asset_metadata else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    
    async def get_multiple_asset_metadata(
        self,
        names: List[str],
        db: Session
    ) -> any:
        try:
            if len(names) > 30:
                {"internal_response_code": 1, "message": "Names list can not have more than 30 values", "data": None}
            name_values = ["'" + name + "'" for name in names]
            array_val = ','.join(name_values)
            where_clause = f"""name IN ({array_val})"""

            asset_metadata = self.model.get_all(db=db, where_clause=where_clause)
            
            return {"internal_response_code": 0, "message": "success", "data": asset_metadata} if asset_metadata else {"internal_response_code": 1, "message": "failed", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")


    