from typing import Union
from fastapi import APIRouter, HTTPException, status, Request, Response
from sqlalchemy.sql import text, bindparam
from fastapi_pagination import Page, paginate, add_pagination, Params
from schemas.user_schema import UserAuth, UserOut
from fastapi import Depends
from schemas.invoices_schema import AddInvoice
from models.invoices_model import InvoicesModel
from models.user_model import UserModel as User
from bin.deps.deps import get_current_user
from bin.database.database import Database
from models.product_model import ProductModel, CategoryModel, FileModel
from schemas.response import ResponseData, ResponseDataWithPagination
from bin.settings.settings import settings
from bin.utils.utils import validate_key
import datetime



invoice_router = APIRouter()

add_pagination(invoice_router)

db = Database()
engine = db.get_db_connection()
session = db.get_db_session(engine)


@invoice_router.get('/invoices', summary="get list invoice")
async def invoices(
        req: Request, 
        res:Response,
        orderBy: Union[str, None] = "DESC",
        params:Params = Depends(),   
        current_user: User = Depends(get_current_user)
    ):
    keys = await validate_key(session, req.headers.get("x-client-id"), req.headers.get("x-client-secret"))
    if not keys:
        return ResponseData(400, False, "Bad Request, keys invalid", None)

    try:
        sql = f"SELECT inv.id as invoices_id, inv.client_id, inv.invoice_number, inv.sequence_number, inv.recurring, inv.date, inv.due_date, inv.status_id,\
          inv.recurring_cycle_id, inv.sub_total, inv.discount_type, inv.discount, inv.total, inv.received_amount, inv.due_amount, inv.notes, inv.terms,\
          inv.created_by, inv.deleted_at, inv.created_at, inv.updated_at, s.id as s_id, s.name status_name, s.class, c.id as c_id, rc.id as rc_id,\
          rc.name, u.id as userID, u.first_name, u.last_name FROM invoices as inv LEFT JOIN statuses as s ON s.id=inv.status_id LEFT JOIN  clients as c\
          ON c.id=inv.client_id LEFT JOIN users as u ON u.id=inv.client_id LEFT JOIN recurring_cycles as rc\
          ON rc.id=inv.recurring_cycle_id ORDER BY inv.id {orderBy}"

        data = session.execute(sql).fetchall()
        temp = paginate(data, params)

        return ResponseDataWithPagination(200, True, None, params, temp)

    except Exception as ex:
        print(ex)
        res.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return ResponseData(status.HTTP_500_INTERNAL_SERVER_ERROR, False, ex, None)


@invoice_router.get('/invoice-details/{id}', summary="get details invoice by id")
async def invoices(
    id: int,
    req: Request, 
    res:Response, 
    current_user: User = Depends(get_current_user) 
    ):
    # if current_user["statusCode"] > 200:
    #     return current_user
    print(current_user.id)
    keys = await validate_key(session, req.headers.get("x-client-id"), req.headers.get("x-client-secret"))
    if not keys:
        return ResponseData(400, False, "Bad Request, keys invalid", None)
    
    try:
        sql1 = f"SELECT i.client_id as ali_id, inv.id as invoices_id, inv.client_id, inv.invoice_number, inv.sequence_number, inv.recurring, inv.date, inv.due_date, inv.status_id,\
          inv.recurring_cycle_id, inv.sub_total, inv.discount_type, inv.discount, inv.total, inv.received_amount, inv.due_amount, inv.notes, inv.terms,\
          inv.created_by, inv.deleted_at, inv.created_at, inv.updated_at, u.id as id_user, u.first_name, u.last_name, u.email, u.last_login_at,\
          u.created_by as cb_user, u.status_id u_status_id, u.invitation_token, u.created_at as ca_user, u.updated_at as ua_user, u.deleted_at as da_user,\
          p.id as p_id, p.user_id as p_user_id, p.gender, p.date_of_birth, p.address, p.contact, p.vat_number, p.created_at as p_ca, p.updated_at as p_ua,\
          id.id as id_id, id.invoice_id, id.product_id, id.quantity, id.price, id.tax_id, id.created_at as id_ca, id.updated_at as id_ua\
          FROM invoices as inv LEFT JOIN users as u ON inv.created_by=u.id LEFT JOIN profiles as p ON p.user_id=u.id LEFT JOIN invoices as i ON i.client_id=u.id\
          LEFT JOIN invoice_details as id ON id.invoice_id=inv.id WHERE inv.id =:id";
        data = session.execute(sql1,{"id":id}).fetchone()
        if data is None:
            res.status_code=status.HTTP_400_BAD_REQUEST
            return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request No data Reference", None)


        sql2 = f"SELECT inv.client_id, c.user_id, u.*, p.* FROM invoices as inv  LEFT JOIN clients as c ON c.user_id=inv.client_id LEFT JOIN users as u ON u.id=c.user_id\
               LEFT JOIN profiles as p ON p.user_id=u.id WHERE inv.client_id = :client_id"
        data2 = session.execute(sql2, {"client_id":data.client_id}).fetchone()
        if data2 is None:
            res.status_code=status.HTTP_400_BAD_REQUEST
            return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request No data Reference", None)

        response = {
            "id":data.invoices_id,
            "client_id":data.client_id,
            "invoice_number":data.invoice_number,
            "recurring":data.recurring,
            "date":data.date,
            "due_date":data.due_date,
            "status_id":data.status_id,
            "recurring_cycle_id":data.recurring_cycle_id,
            "sub_total":data.sub_total,
            "discount_type":data.discount_type,
            "discount":data.discount,
            "total":data.total,
            "received_amount":data.received_amount,
            "due_amount":data.due_amount,
            "notes":data.notes,
            "terms":data.terms,
            "deleted_at":data.deleted_at,
            "created_at":data.created_at,
            "updated_at":data.updated_at,
            "created_by":{
                "id":data.id_user,
                "first_name":data.first_name,
                "last_name":data.last_name,
                "email":data.email,
                "last_login_at":data.last_login_at,
                "created_by":data.cb_user,
                "status_id":data.u_status_id,
                "invitation_token":data.invitation_token,
                "created_at":data.ca_user,
                "updated_at":data.ua_user,
                "deleted_at":data.da_user,
                "phone":None,
                "full_name":f"{data.first_name } {data.last_name}",
                "profile":{
                    "id":data.p_id,
                    "user_id":data.p_user_id,
                    "gender":data.gender,
                    "date_of_birth":data.date_of_birth,
                    "address":data.address,
                    "contact":data.contact,
                    "vat_number":data.vat_number,
                    "created_at":data.p_ca,
                    "updated_at":data.p_ua,
                }
            },
            "client":{
                "id":data2.client_id,
                "first_name":data2.first_name,
                "last_name":data2.last_name,
                "email":data2.email,
                "last_login_at":data2.last_login_at,
                "created_by":data2.created_by,
                "status_id":data2.status_id,
                "invitation_token":data2.invitation_token,
                "created_at":data2.created_at,
                "updated_at":data2.updated_at,
                "deleted_at":data2.deleted_at,
                "phone":None,
                "full_name":f"{data2.first_name} {data2.last_name}",
                "profile":{
                    "id":data2.id,
                    "user_id":data2.user_id,
                    "date_of_birth":data2.date_of_birth,
                    "address":data2.address,
                    "contact":data2.contact,
                    "data":data2.vat_number,
                    "created_at":data2.created_at,
                    "updated_at":data2.updated_at
                }
            },
            "invoice_details":[
                {
                    "id":data.id_id,
                    "invoice_id":data.invoice_id,
                    "product_id":data.product_id,
                    "quantity":data.quantity,
                    "price":data.price,
                    "tax_id":data.tax_id,
                    "created_at":data.id_ca,
                    "updated_at":data.id_ua,
                    "tax":None,
                    "product":None
                }
            ]
        }
        return ResponseData(200, True, None, response)

    except Exception as ex:
       print(ex)
       res.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
       return ResponseData(status.HTTP_500_INTERNAL_SERVER_ERROR, False, ex, None)

@invoice_router.post('/create-invoice', summary="create invoice")
async def invoices(
    body:AddInvoice,
    req:Request,
    res:Response,
    current_user: User = Depends(get_current_user) 
    ):
    print(f"this is current user: {current_user}")
    keys = await validate_key(session, req.headers.get("x-client-id"), req.headers.get("x-client-secret"))
    if not keys:
        return ResponseData(400, False, "Bad Request, keys invalid", None)

    try:
        sql_insert_invoices = "INSERT INTO invoices (client_id, date, discount, discount_type, due_amount, due_date, invoice_number, notes,\
                received_amount, recurring, status_id, sub_total, terms, total) VALUES(:client_id, :date, :discount, :discount_type,\
                :due_amount, :due_date, :invoice_number, :notes, :received_amount, :recurring, :status_id, :sub_total, :terms, :total)"
        invoices_values = {
            "client_id":body.client_id, 
            "date":body.date, 
            "discount":body.discount,
            "discount_type":body.discount_type, 
            "due_amount":body.due_amount,
            "due_date":body.due_date, 
            "invoice_number":body.invoice_number,
            "notes":body.notes,
            "received_amount":body.received_amount,
            "recurring":body.recurring,
            "status_id":body.status_id,
            "sub_total":body.sub_total,
            "terms":body.terms, "total":body.total,
            "created_at":datetime.datetime.now(),
            "updated_at":datetime.datetime.now()
        }   

        sql_insert_product = "INSERT INTO proudct (product_id, name, quantity, price, tax_id) VALUES(:product_id, :name, :quantity, :price, :tax_id)"
        product_values = {
            "product_id":body.products[0].product_id,
            "name":body.products[0].name,
            "quantity":body.products[0].quantity,
            "price":body.products[0].price,
            "tax_id":body.products[0].tax_id,
            "created_at":datetime.datetime.now(),
            "updated_at":datetime.datetime.now()
        }
        invoices = session.execute(sql_insert_invoices, invoices_values)
        product = session.execute(sql_insert_product, product_values)

    except Exception as ex:
        print(ex)
        res.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return ResponseData(status.HTTP_500_INTERNAL_SERVER_ERROR, False, ex, None)

@invoice_router.delete('/invoices/{id}', summary="delete invoice by id", response_model=UserOut)
async def invoices(data: UserAuth):
    pass


@invoice_router.post('/invoices/send/{id}', summary="send invoice", response_model=UserOut)
async def invoices(data: UserAuth):
    pass


@invoice_router.put('/invoices/{id}', summary="edit invoice", response_model=UserOut)
async def invoices(data: UserAuth):
    pass