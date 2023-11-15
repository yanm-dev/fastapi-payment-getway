from fastapi import APIRouter, HTTPException, status, Request, Response
from schemas.user_schema import UserAuth, UserOut
from fastapi import Depends
from services.user_services import UserServices
from models.user_model import UserModel as User
from bin.deps.deps import get_current_user
from bin.database.database import Database
from models.product_model import ProductModel, CategoryModel, FileModel
from schemas.response import ResponseData
from bin.settings.settings import settings
from bin.utils.utils import validate_key



product_router = APIRouter()

db = Database()
engine = db.get_db_connection()
session = db.get_db_session(engine)

@product_router.get('/products', summary="get list product", response_model=UserOut)
async def products(data: UserAuth):
    pass


@product_router.get('/product-detail/{id}', summary="get details product")
async def details_products(
    id: int,
    req: Request,
    res:Response,
    current_user: User = Depends(get_current_user)):
    
    keys = await validate_key(session, req.headers.get("x-client-id"), req.headers.get("x-client-secret"))
    if not keys:
        return ResponseData(400, False, "Bad Request, keys invalid", None)

    try:
        rows = session.execute(
            "SELECT p.id p_id, p.name as p_name, p.code, p.category_id, p.unit_price, p.description, p.created_at as p_created_at, p.updated_at as p_updated_at, \
                c.id as c_id, c.name as c_name, c.created_by, c.created_at as c_created_at, c.updated_at as c_updated_at, f.id as f_id, f.path, f.fileable_type, f.fileable_id, \
                f.type, f.created_at, f.updated_at FROM products p INNER JOIN categories c ON c.id = p.category_id INNER JOIN files f ON f.fileable_id = c.id WHERE p.id = :id", {"id": id}
        ).fetchall()

        if len(rows) == 0 :
            try:
                query = session.execute("SELECT * FROM products WHERE id = :id", {"id":id}).fetchone()
                data = {
                    "id": query.id,
                    "name": query.name,
                    "category_id": query.category_id,
                    "unit_price": query.unit_price,
                    "description": query.description,
                    "created_at": query.created_at,
                    "updated_at": query.updated_at,
                    "category": None,
                    "file": None
                }
                return ResponseData(200, True, None, data)
            except Exception as ex:
                print(ex)
                res.status_code=status.HTTP_400_BAD_REQUEST
                return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request No data Reference", None)


        if not rows or rows is None:
            res.status_code=status.HTTP_400_BAD_REQUEST
            return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request No data Reference", None)
        data = {
            "id": rows[0].p_id,
            "name": rows[0].p_name,
            "category_id": rows[0].category_id,
            "unit_price": rows[0].unit_price,
            "description": rows[0].description,
            "created_at": rows[0].p_created_at,
            "updated_at": rows[0].p_updated_at,
            "category":{
                "id": rows[0].c_id,
                "name": rows[0].c_name,
                "created_by":rows[0].created_by,
                "created_at":rows[0].c_created_at,
                "updated_at":rows[0].c_updated_at
            },
            "file":{
                "id":rows[0].f_id,
                "path":rows[0].path,
                "type":rows[0].type,
                "created_at":rows[0].created_at,
                "updated_at":rows[0].updated_at,
                "full_url":f"{settings.BASE_URL}{rows[0].path}"
            }
        }
        return ResponseData(200, True, None, data)

    except Exception as ex:
       print(ex)
       res.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
       return ResponseData(status.HTTP_500_INTERNAL_SERVER_ERROR, False, ex, None)


@product_router.post('/products/{id}', summary="add product", response_model=UserOut)
async def add_products(data: UserAuth):
    pass

@product_router.put('/products/{id}', summary="update product", response_model=UserOut)
async def update_products(data: UserAuth):
    pass

@product_router.delete('/products/{id}', summary="delete product", response_model=UserOut)
async def delete_products(data: UserAuth):
    pass


