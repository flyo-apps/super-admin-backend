from typing import Optional
from pydantic import BaseModel

class CreateProductVariantBaseModel(BaseModel):
    unique_id : str
    variant_name : str
    variant_type : str
    sku_code : str
    product_name : str
    product_image : str
    rank: Optional[int]

class CreateProductVariantModel(CreateProductVariantBaseModel):
    code : str

class UpdateProductVariantModel(BaseModel):
    unique_id : str
    sku_code : str
    variant_name : Optional[str]
    variant_type : Optional[str]
    product_name : Optional[str]
    product_image : Optional[str]
    rank: Optional[int]


class CreateProductVariantMapModel(BaseModel):
    code : str
    unique_id : str
    sku_code : str