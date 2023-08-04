from typing import List, Optional

from pydantic import BaseModel


class Filter(BaseModel):
    category: Optional[List[str]] = None
    size: Optional[List[str]] = None
    product_type: Optional[List[str]] = None
    occasion: Optional[List[str]] = None
    brand: Optional[List[str]] = None
    collection: Optional[List[str]] = None
    discount: Optional[List[str]] = None
    metal: Optional[List[str]] = None
    material: Optional[List[str]] = None
    colour: Optional[List[str]] = None
    metal_colour: Optional[List[str]] = None
    plating: Optional[List[str]] = None
    warranty: Optional[List[str]] = None
    shipping_time: Optional[List[str]] = None
    purity: Optional[List[str]] = None
    price: Optional[List[int]] = None
    gifting: Optional[List[bool]] = None
    gender: Optional[List[str]] = None
    design_type: Optional[List[str]] = None