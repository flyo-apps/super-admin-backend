from items.models.blogs import BlogCreateBaseModel, BlogCreateModel,BlogUpdateBaseModel, BlogUpdateModel, BlogDeleteModel
from items.models.blogs import NewBlogCreateBaseModel, NewBlogCreateModel, NewBlogUpdateBaseModel, NewBlogUpdateModel
from ..schemas.blogs import BlogsSchema, NewBlogsSchema
from db.aurora.aurora_base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException
import json
from datetime import datetime
from typing import List

BLOGS_SORTING_METHOD = "blog_rank ASC, rank ASC"
BLOGS_MEDIA_SORTING_METHOD= "rank ASC"

class BlogsCollection:
    def __init__(self):
        self.model = CRUDBase(BlogsSchema)
        self.new_blogs_model = CRUDBase(NewBlogsSchema)
    
    async def create_blog(
        self,
        blog: BlogCreateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{blog.code}'"""
            existing_blog = self.model.get_one(db=db, where_clause=where_clause)
            if existing_blog is not None:
                return {"internal_response_code": 1, "message": f"""blog {blog.code} exists"""}

            blog_create = BlogCreateModel(**blog.dict())
            created_blog = self.model.create(db=db, obj_in=blog_create)

            return {"internal_response_code": 0, "message": f"""blog {blog.code} created"""} if created_blog else {"internal_response_code": 1, "message": f"""failed to create blog {blog.code}"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")
    
    async def delete_blog_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{code}' AND is_deleted=false"""
            existing_blog = self.model.get_one(db=db, where_clause=where_clause)
            if existing_blog is None:
                return {"internal_response_code": 1, "message": f"""blog {code} not found"""}

            blog_delete_dict = BlogDeleteModel(code=code).dict()
            deleted_blog = self.model.update(db=db, db_obj=existing_blog, obj_in=blog_delete_dict)

            return {"internal_response_code": 0, "message": f"""blog {code} deleted"""} if deleted_blog else {"internal_response_code": 1, "message": f"""failed to delete blog {code}"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_blog_by_code(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""(code='{code}' AND is_deleted=false)"""
            existing_blog = self.model.get_one(db=db, where_clause=where_clause)

            return {"internal_response_code": 0, "data": existing_blog} if existing_blog else {"internal_response_code": 1, "message": f"""blog {code} not found"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_blogs_by_blog_code_and_name(
        self,
        blog_name: str,
        blog_code: str,
        page_number: int,
        limit: int,
        db: Session
    ) -> any:
        try:
            where_clause = f"""blog_code='{blog_code}' AND blog_name='{blog_name}' AND is_deleted=false"""
            skip=0
            if page_number >1 :
                skip = (page_number - 1)*limit
            blogs = self.model.get_all(db=db, where_clause=where_clause,skip=skip,limit=limit,sorting_method=BLOGS_MEDIA_SORTING_METHOD)

            return {"internal_response_code": 0, "data": blogs}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_blog(
        self,
        blog: BlogUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{blog.code}' AND is_deleted=false"""
            existing_blog = self.model.get_one(db=db, where_clause=where_clause)
            if existing_blog is None:
                return {"internal_response_code": 1, "message": f"""blog {blog.code} not found"""}

            blog_update = BlogUpdateModel(**blog.dict())
            blog_update.is_updated = True
            blog_update.updated_at = datetime.now()
            updated_blog = self.model.update(db=db, db_obj=existing_blog,obj_in=blog_update)

            return {"internal_response_code": 0, "message": f"""blog {blog.code} updated"""} if updated_blog else {"internal_response_code": 1, "message": f"""failed to update blog {blog.code}"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_blogs(
        self,
        page_number: int,
        limit: int,
        db: Session
    ) -> any:
        try:
            skip = 0
            if page_number > 1:
                skip = (page_number - 1)*limit

            postgreSQL_agg_query = f"""SELECT blog_code, blog_name, blog_rank, blog_summary_image, jsonb_agg(to_jsonb(blogs) - 'blog_code' - 'blog_name' - 'blog_rank' - 'blog_summary_image' ORDER BY rank ASC) as blog_data FROM blogs where is_deleted = false GROUP BY blog_code, blog_name, blog_rank, blog_summary_image ORDER BY blog_rank DESC OFFSET {skip} LIMIT {limit}"""

            blogs = self.model.call_postgres_function(db=db, query=postgreSQL_agg_query)

            return {"internal_response_code": 0, "data": blogs}

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def upsert_multiple_blogs(
        self,
        blog_details: List[BlogCreateBaseModel],
        db: Session
    ) -> any:
        try:
            codes = ','.join(["'" + data.code + "'" for data in blog_details])
            existing_codes = []
            where_clause = f"""code IN ({codes})"""
            existing_blogs = self.model.get_all(db=db, where_clause=where_clause,skip=0,limit=len(blog_details))
            if existing_blogs:
                existing_codes = [data.code for data in existing_blogs]

            blogs_create = []
            blogs_update = []
            for blog in blog_details:
                if blog.code not in existing_codes:
                    blog_create = BlogCreateModel(**blog.dict())
                    blogs_create.append(blog_create.dict())
                else:
                    blog_update = BlogUpdateModel(**blog.dict())
                    blogs_update.append(blog_update.dict())

            res = self.model.bulk_upsert(db=db, update_vals=blogs_update,insert_vals=blogs_create)
            return {"internal_response_code": 0, "message": f"""blog created for {len(blogs_create)} codes and updated for {len(blogs_update)} codes"""} if res is None else {"internal_response_code": 1, "message": f"""upsert operation failed"""}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def create_new_blog(
        self,
        blog: NewBlogCreateBaseModel,
        db: Session
    ) -> any:
        try:
            if blog.screen_filter != None:
                where_clause_dict = json.dumps(blog.screen_filter, separators=(':', ': ')).lower()
                where_clause = f"""screen_filter::text='{where_clause_dict}'::text"""
            else:
                where_clause = f"""code='{blog.code}'"""

            existing_blog = self.new_blogs_model.get_one(db=db, where_clause=where_clause)
            if existing_blog is not None:
                return {"internal_response_code": 1, "message": f"""blog {blog.code} exists or {blog.screen_filter} exits""", "data": None}

            blog_create = NewBlogCreateModel(**blog.dict(exclude_unset=True))
            blog_create.screen_filter = json.loads(json.dumps(blog.screen_filter).lower())
            created_blog = self.new_blogs_model.create(db=db, obj_in=blog_create)

            return {"internal_response_code": 0, "message": f"""blog {blog.code} created""", "data": None} if created_blog else {"internal_response_code": 1, "message": f"""failed to create blog {blog.code}""", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_content_for_product_listing(
        self,
        screen_filter: dict,
        db: Session
    ) -> any:
        try:
            where_clause_dict = json.dumps(screen_filter, separators=(':', ': ')).lower()
            where_clause = f"""screen_filter::text='{where_clause_dict}'::text"""
            blog = self.new_blogs_model.get_one(db=db, where_clause=where_clause)

            return {"internal_response_code": 0, "message": "success", "data": blog} if blog else {"internal_response_code": 1, "message": "failed", "data": None}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def update_new_blog(
        self,
        blog: NewBlogUpdateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{blog.code}' AND is_deleted=false"""
            existing_blog = self.new_blogs_model.get_one(db=db, where_clause=where_clause)
            if existing_blog is None:
                return {"internal_response_code": 1, "message": f"""blog {blog.code} not found or is deleted""", "data": None}

            blog_update = NewBlogUpdateModel(**blog.dict(exclude_unset=True))
            blog_update.is_updated = True
            blog_update.updated_at = datetime.now()
            updated_blog = self.new_blogs_model.update(db=db, db_obj=existing_blog,obj_in=blog_update)

            return {"internal_response_code": 0, "message": f"""blog {blog.code} updated""", "data": None} if updated_blog else {"internal_response_code": 1, "message": f"""failed to update blog {blog.code}""", "data": None}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def delete_new_blog(
        self,
        code: str,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{code}' AND is_deleted=false"""
            existing_blog = self.new_blogs_model.get_one(db=db, where_clause=where_clause)
            if existing_blog is None:
                return {"internal_response_code": 1, "message": f"""blog {code} not found or already deleted"""}

            blog_delete_dict = BlogDeleteModel(code=code).dict()
            deleted_blog = self.new_blogs_model.update(db=db, db_obj=existing_blog, obj_in=blog_delete_dict)

            return {"internal_response_code": 0, "message": f"""blog {code} deleted""", "data": None} if deleted_blog else {"internal_response_code": 1, "message": f"""failed to delete blog {code}""", "data": None}

        except:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_new_blog(
        self,
        code: NewBlogCreateBaseModel,
        db: Session
    ) -> any:
        try:
            where_clause = f"""code='{code}' AND is_deleted=false"""
            blog = self.new_blogs_model.get_one(db=db, where_clause=where_clause)

            return {"internal_response_code": 0, "message": f"""success""", "data": blog} if blog else {"internal_response_code": 1, "message": f"""blog {code} not found""", "data": None}
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def get_new_blogs(
        self,
        db: Session,
        page_number: int
    ) -> any:
        try:
            limit = 30
            skip = 0
            if page_number > 1:
                skip = (page_number - 1)*limit

            query = f"""select * from new_blogs where is_deleted = false ORDER BY rank DESC OFFSET {skip} LIMIT {limit}"""
            blogs = self.new_blogs_model.call_postgres_function(db=db, query=query)

            return {"internal_response_code": 0, "message": "success", "data": blogs} if len(blogs) > 0 else {"internal_response_code": 1, "message": "failed", "data": None}

        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")