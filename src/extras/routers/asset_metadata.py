from fastapi import APIRouter, HTTPException, Security, Depends, UploadFile, Response
from auth.authentication_user import get_current_active_user
from typing import List
from extras.crud.asset_metadata import AssetMetaDataCollection
from extras.models.asset_metadata import CreateAssetMetaDataBaseModel
from db.aurora import auroradb
from sqlalchemy.orm import Session


router = APIRouter()

@router.post(
    "/v1/create_asset_metadata",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_asset_metadata(
    create_asset_metadata_base: CreateAssetMetaDataBaseModel,
    db: Session = Depends(auroradb.get_db)
):
    try:
        asset_metadata_collection = AssetMetaDataCollection()
        return await asset_metadata_collection.create_asset_metadata(db=db, create_asset_metadata_base=create_asset_metadata_base)
    except Exception:
        raise HTTPException(status_code=500, detail="something went wrong")
        

@router.get(
    "/v1/get_asset_metadata",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_asset_metadata(
    name: str,
    db: Session = Depends(auroradb.get_db)
):
    try:
        asset_metadata_collection = AssetMetaDataCollection()
        return await asset_metadata_collection.get_asset_metadata(db=db, name=name)
    except Exception:
        raise HTTPException(status_code=500, detail="something went wrong")

@router.post(
    "/v1/get_multiple_asset_metadata",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_multiple_asset_metadata(
    names: List[str],
    db: Session = Depends(auroradb.get_db)
):
    try:
        asset_metadata_collection = AssetMetaDataCollection()
        return await asset_metadata_collection.get_multiple_asset_metadata(db=db, names=names)
    except Exception:
        raise HTTPException(status_code=500, detail="something went wrong")

@router.post(
    "/v1/create_asset_metadata_from_blob",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_asset_metadata(
	image_name: str,
	image_type: str,
	image_dimension: str,
	image_blob_file: UploadFile,
    db: Session = Depends(auroradb.get_db)
):
    try:
        asset_metadata_collection = AssetMetaDataCollection()
        return await asset_metadata_collection.create_asset_metadata_from_blob(image_name, image_type, image_dimension, image_blob_file, db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="something went wrong")

