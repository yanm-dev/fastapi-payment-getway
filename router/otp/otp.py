import datetime, time, uuid
import pyotp
from fastapi import APIRouter, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from schemas.user_schema import UserAuth, UserOut
from fastapi import Depends
from schemas.user_schema import GeneratePost, VerifyPost
from models.otp_model import OTPModel
from bin.deps.deps import get_current_user
from bin.database.database import Database
from bin.settings.settings import Settings as settings
from bin.utils.utils import verify_password
from schemas.response import ResponseData



otp_router = APIRouter()

db = Database()
engine = db.get_db_connection()
session = db.get_db_session(engine)

@otp_router.post('/otp/generate', summary="generate otp")
async def generate(
    req:Request, 
    res:Response, 
    body: GeneratePost
):
    #check session

    #validation
    user = None
    field = ""

    if not body.password or body.password is None or body.password == "":
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request", None)

    elif body.email != None or body.email=="":
        print("email execute")
        field = 'email'
        body.phone = None
        user = session.execute("SELECT * FROM users WHERE email=:email",{"email":body.email}).fetchone()

        if not user or body.email != user.email or verify_password(body.password, user.password) == False:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            return ResponseData(status.HTTP_401_UNAUTHORIZED, False, "The password you entered is incorrect.", None)


    elif body.phone != None or body.phone == "":
        field = "phone_number"
        body.email = None
        user = session.execute("SELECT u.id, u.password, p.contact, p.user_id FROM users as u LEFT JOIN profiles as p ON u.id=p.user_id WHERE p.contact=:contact",{"contact":body.phone}).fetchone()
        
        if not user or body.phone != user.contact or verify_password(body.password, user.password) == False:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            return ResponseData(status.HTTP_401_UNAUTHORIZED, False, "The password you entered is incorrect.", None)
    else:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request", None)


    if user == None:
        res.status_code = status.HTTP_200_OK
        return ResponseData(status.HTTP_200_OK, True, None, f"If that {field} is in our database, we will send you an OTP.")

    ip_address = req.client.host
    if ip_address == '127.0.0.1':
        ip_address == '180.241.243.239'

    otp = None

    if body.email != None:
        otp = session.execute("SELECT * FROM otp_generators WHERE user_id=:user_id AND is_verified=:is_verified AND ip_address=:ip_address AND otp_for=:otp_for AND email=:email",{
            "user_id":user.id,
            "is_verified":0,
            "ip_address":ip_address,
            "otp_for":user.otp_for,
            "email":user.email
        }).fetchone()
    elif body.phone != None:
        otp = session.execute("SELECT * FROM otp_generators WHERE user_id=:user_id AND is_verified=:is_verified AND ip_address=:ip_address AND otp_for=:otp_for AND email=:email",{
            "user_id":user.id,
            "is_verified":0,
            "ip_address":ip_address,
            "otp_for":user.otp_for,
            "email":user.email
        }).fetchone()

    else:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request", None)

    otp_expired_time = time.time()+300
    try:
        if otp:
            del_otp = session.execute("DELETE from otp_generators WHERE id =:id", {"id":otp.id})
            print(del_otp)

        otp_code = pyotp.TOTP('base32secret3232').now()        
        model = OTPModel(
            id= uuid.uuid1(),
            user_id=user.id,
            email=body.email,
            phone_number=None,
            code= otp_code,
            is_verified=False,
            otp_for=user.otp_for,
            ip_address=ip_address,
            expired_at=otp_expired_time
        )
        session.add(model)
        session.flush()
        session.refresh(model, attribute_names=["id","expired_at","email","phone_number","otp_for"])
        session.commit()
        session.close()
        

        if field == "email":
            print("send otp via email action")
        elif field == "phone_number":
            print("send otp via phone action")
        else:
            pass

        res.status_code = status.HTTP_200_OK
        return ResponseData(status.HTTP_200_OK, True, None, {
            "otp_id":model.id,
            "expired_at":model.expired_at,
            "redirect":f"https://app.kasandra.bio/admin/users/otp?otp_id={model.id}&otp_for={model.otp_for}&email={model.email}&=phone_number={model.phone_number}&expired_at={model.expired_at}"
        })
    except Exception as ex:
        print(ex)
        res.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return ResponseData(status.HTTP_500_INTERNAL_SERVER_ERROR, False, ex, None)

@otp_router.post('/otp/verify', summary="verify otp", response_model=UserOut)
async def verify(
    req:Request, 
    res:Response, 
    body: VerifyPost
):
    otp = None
    if body.email != None or body.email != "":
        email = body.email
        phone = None
        otp = session.execute("SELECT * FROM otp_generators WHERE id=:otp_id OR code=:code AND email=:email", {"otp_id":body.otp_id, "code":body.code, "email":body.email}).fetchone()

    elif body.phone_number != None or body.phone_number != "":
        phone = body.phone_number
        email = None
        otp = session.execute("SELECT * FROM otp_generators WHERE id=:otp_id OR code=:code AND phone_number=:phone_number", {"otp_id":body.otp_id, "code":body.code, "phone_number":body.phone_number}).fetchone()
    else:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseData(status.HTTP_400_BAD_REQUEST, False, "Bad Request", None)

    if not otp or otp == None:
        user = session.execute("SELECT u.id, u.otp_times, p.contact, p.user_id FROM users as u LEFT JOIN profiles as p ON u.id=p.user_id WHERE p.contact=:contact OR u.email=:email" ,{"contact":body.phone, "email":body.email}).fetchone()
        if user:
            otp_times = user.otp_times + 1
            session.execute("UPDATE user SET otp_times=:otp_times WHERE id=:id", {"id":user.id, "otp_times":otp_times})
            session.close()
        res.status_code = status.HTTP_403
        return ResponseData(status.HTTP_403, False, "OTP is invalid.", None)

    if otp.is_verified == 1 or otp.expired_time <= time.time():
        res.status_code = status.HTTP_403_FORBIDDEN
        return ResponseData(status.HTTP_403_FORBIDDEN, False, "OTP has expired.", None)

    if otp.otp_for == "login":
        pass

    res.status_code = status.HTTP_404_NOT_FOUND
    return ResponseData(status.HTTP_404, False, "OTP is invalid.", None)





@otp_router.get('/otp', summary="get otp", response_model=UserOut)
async def index(data: UserAuth):
    pass
