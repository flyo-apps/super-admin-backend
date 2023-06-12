from datetime import datetime
from pydantic import BaseModel


class CreateAssetMetaDataBaseModel(BaseModel):
    name: str
    link: str
    type : str
    dimension: str

class CreateAssetMetaDataModel(CreateAssetMetaDataBaseModel):
    created_at: datetime = datetime.now()

class CreateAssetMetaDataFromBlobModel(BaseModel):
    name: str
    type: str
    dimension: str
    link: str = ""
    blob_filedata: bytes
    created_at: datetime = datetime.now()