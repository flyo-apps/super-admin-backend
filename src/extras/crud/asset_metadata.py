from datetime import date, datetime
from fastapi import HTTPException, UploadFile
from typing import List
import base64
from extras.schemas.asset_metadata import AssetMetadataSchema
from extras.models.asset_metadata import (
    CreateAssetMetaDataBaseModel,
    CreateAssetMetaDataModel,
    CreateAssetMetaDataFromBlobModel
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

    async def create_asset_metadata_from_blob(
        self,
        image_name: str,
        image_type: str,
        image_dimension: str,
        image_blob_file: UploadFile,
        db: Session
    ) -> any:
        try:
            blob_data = await image_blob_file.read()
            if len(blob_data) == 0:
                return {"internal_response_code": 1, "message": "failed: recieved empty file", "data": None}

            # Check if the blob file size exceeds 200KB
            if len(blob_data) > 500 * 1024:
                return {"internal_response_code": 1, "message": "failed: recieved file > 200kb", "data": None}

            # Check if the blob file size is less than 20KB
            if len(blob_data) < 20 * 1024:
                return {"internal_response_code": 1, "message": "failed: recieved file < 20kb", "data": None}

            encoded_blob_data = base64.b64decode(blob_data.encode())
            create_asset_metadata = CreateAssetMetaDataFromBlobModel(name=image_name, type=image_type, dimension=image_dimension, blob_filedata=encoded_blob_data, created_at=datetime.now())
            asset_metadata = self.model.create(db=db, obj_in=create_asset_metadata.dict())

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
                        "blob_filedata": encoded_blob_data,
                        "is_updated": True,
                        "updated_at": datetime.now()
                    }
                    asset_metadata = self.model.filter_update(db=db, where_clause=where_clause, update_values=update_values)
                    return {"internal_response_code": 0, "message": "success", "data": None}
                except Exception as e:
                    raise HTTPException(status_code=500, detail="Something went wrong")

            print(e)
            raise HTTPException(status_code=500, detail="Something went wrong")

    