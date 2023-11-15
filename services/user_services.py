from typing import Optional
from uuid import UUID
from schemas.user_schema import UserAuth
from models.user_model import UserModel
from bin.utils.utils import verify_password


class UserServices:
    @staticmethod
    def authenticate(db, email: str, password: str):
        user = db.execute("SELECT * FROM users WHERE email=:email", {"email":email}).fetchone()
        
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.password):
            return None
        
        return user

    async def verify_login(params):
        session = params.session

        user = session.execute("SELECT * FROM users where id=:user_id", {"id":params.user_id}).fetchone()
        
        if user:
            session.execute("UPDATE users SET otp_for=:otp_for, otp_times=:otp_times, ip_address=:ip_address, user_agent=:user_agen", {
                "otp_for":None,
                "otp_times":0,
                "ip_address":params.ip_address,
                "user_agent":params.user_agent
            })

        session.execute("UPDATE otp_generators SET is_verified=:is_verified", {"is_verified":1})
        """
            paused work will asign to another project
            task is just verify login 
        """
