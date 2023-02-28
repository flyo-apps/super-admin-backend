
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Security, BackgroundTasks
from auth.authentication_user import get_current_active_user
from master.utils.constants import REQUEST_LIMIT, REQUEST_PAGE_NUMBER
from ..crud.homepage import HomePageCollection
from users.models.users import UserModel
from ..models.homepage import (
    HomePageCreateBaseModel,
    HomePageUpdateBaseModel,
    HomePageFilterDetails
)

from db.aurora import auroradb
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/v1/create_homepage_component",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def create_homepage_component(
    background_tasks: BackgroundTasks,
    homepage_details: HomePageCreateBaseModel,
    db: Session = Depends(auroradb.get_db),
    from_lambda: Optional[bool] = False,
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["admin:write"],
    ),
):
    try:
        homepage_collection = HomePageCollection()

        return await homepage_collection.create_homepage_component(homepage_details=homepage_details, db=db, from_lambda=from_lambda, username=current_user.username, background_tasks=background_tasks)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_homepage",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_homepage(
    homepage_name: Optional[str] = "Primary",
    limit: Optional[int] = REQUEST_LIMIT,
    page: Optional[int] = REQUEST_PAGE_NUMBER,
    db: Session = Depends(auroradb.get_db),
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["guest:read"],
    )
):
    try:
        if page < 1 or limit < 1:
            return None
            
        homepage_collection = HomePageCollection()
        # homepage_title = await homepage_collection.get_homepage_validations(current_user = current_user, default_title=default_title)
        # get type from above and move
        details = await homepage_collection.get_homepage_details(homepage_name=homepage_name, limit=limit, page=page, db=db)

        if len(details) < limit:
            internal_response_code = 1
        else:
            internal_response_code = 0

        return {"internal_response_code": internal_response_code, "homepage_details": details}
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get(
    "/v1/get_homepage_component_by_component_title",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_homepage_component_by_component_title(
    component_title: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        homepage_collection = HomePageCollection()
        return await homepage_collection.get_homepage_component_by_component_title(component_title=component_title,db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get(
    "/v1/get_homepage_component_by_component_title_and_code",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_homepage_component_by_component_title_and_code(
    component_title: str,
    code: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        homepage_collection = HomePageCollection()
        return await homepage_collection.get_homepage_component_by_component_title_and_code(component_title=component_title,db=db,code=code)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
        

@router.get(
    "/v1/get_homepage_component_by_element_type",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def get_homepage_component_by_element_type(
    homepage_name: str,
    component_elements_type: Optional[str] = "Product",
    limit: Optional[int] = REQUEST_LIMIT,
    page: Optional[int] = REQUEST_PAGE_NUMBER,
    db: Session = Depends(auroradb.get_db),
):
    try:
        homepage_collection = HomePageCollection()

        details = await homepage_collection.get_homepage_component_by_element_type(db=db, homepage_name=homepage_name, component_elements_type=component_elements_type, limit=limit, page=page)

        if len(details) < limit:
            internal_response_code = 1
        else:
            internal_response_code = 0

        return {"internal_response_code": internal_response_code, "homepage_details": details}
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/update_homepage",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_homepage(
    background_tasks: BackgroundTasks,
    update_details: HomePageUpdateBaseModel,
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["admin:write"],
    ),
    db: Session = Depends(auroradb.get_db),
    from_lambda: bool = False
):
    try:
        homepage_collection = HomePageCollection()

        return await homepage_collection.update_homepage(db=db, update_details=update_details, background_tasks=background_tasks,current_user=current_user.username,from_lambda=from_lambda)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
    

@router.post(
    "/v1/update_homepage_elements",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def update_homepage_elements(  
    code: str,
    homepage_name: str,
    update_type: str,
    component_title: str,
    component_type: str,
    background_tasks: BackgroundTasks,
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["admin:write"],
    ),
    component_elements_type: Optional[str] = None,
    component_elements: Optional[str] = None,
    component_elements_image: Optional[str] = None,
    component_elements_secondary_text: Optional[str] = None,
    component_elements_position: Optional[int] = None,
    element_background_color: Optional[str] = None,
    filter_details: Optional[HomePageFilterDetails] = None,
    db: Session = Depends(auroradb.get_db),
    from_lambda: Optional[bool] = False
):
    try:
        homepage_collection = HomePageCollection()
        if filter_details != None:
            filter_details = filter_details.dict()
        else:
            filter_details = None

        return await homepage_collection.update_homepage_elements(
            db=db,
            code=code,
            background_tasks=background_tasks,
            homepage_name=homepage_name,
            update_type=update_type,
            component_title=component_title,
            component_type=component_type,
            component_elements_type=component_elements_type,
            component_elements=component_elements,
            component_elements_image=component_elements_image,
            component_elements_secondary_text=component_elements_secondary_text,
            component_elements_position=component_elements_position,
            element_background_color=element_background_color,
            username=current_user.username,
            filter_details=filter_details,
            from_lambda=from_lambda
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")



@router.post(
    "/v1/add_homepage_component_item_list",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_homepage_component_item_list( 
    code: str, 
    homepage_name: str,
    component_title: str,
    add_to_title: str,
    add_to_code: str,
    rank: int,
    db: Session = Depends(auroradb.get_db),
):
    try:
        homepage_collection = HomePageCollection()
        return await homepage_collection.add_homepage_component_item_list(
            db=db,
            code=code,
            add_to_code=add_to_code,
            add_to_title=add_to_title,
            homepage_name=homepage_name,
            component_title=component_title,
            rank=rank
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/remove_homepage_component_item_list",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def remove_homepage_component_item_list(  
    code: str, 
    homepage_name: str,
    component_title: str,
    add_to_title: str,
    add_to_code: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        homepage_collection = HomePageCollection()
        return await homepage_collection.remove_homepage_component_item_list(
            db=db,
            code=code,
            add_to_code=add_to_code,
            add_to_title=add_to_title,
            homepage_name=homepage_name,
            component_title=component_title
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/v1/refresh_homepage_redis",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def refresh_homepage_redis(
    homepage_name: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        homepage_collection = HomePageCollection()
        return await homepage_collection.refresh_homepage_redis(homepage_name=homepage_name, db=db)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.delete(
    "/v1/delete_homepage_component",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def delete_homepage_component(
    homepage_component_code: str,
    homepage_name: str,
    db: Session = Depends(auroradb.get_db),
):
    try:
        homepage_collection = HomePageCollection()
        return await homepage_collection.delete_homepage_component(db=db, homepage_code=homepage_component_code, homepage_name=homepage_name)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
