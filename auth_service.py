import logging
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi import HTTPException,status
from gotrue.exceptions import APIError
load_dotenv()

log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(level='DEBUG', format=log_format)


class AuthService:
    def __init__(self,url:str,key:str):
        self.url = url
        self.key = key
        self.supabase :Client = create_client(self.url,self.key)

    def signUp(self,email:str, password:str):
        try:
            self.supabase.auth.sign_up(email=email,password=password)
            logging.info("Signed Up Successfully")
            return {"status_code":200, "message":"User account created successfully"}
        except APIError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User's credential already esxists")

    def signIn(self,email:str,password:str):
        session = None
        try:
            session = self.supabase.auth.sign_in(email=email,password=password)
            logging.info("Logged in Successfully")
            self.logOut()
            return {'access_token':session.access_token,"user":session.user}
        except APIError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Login in Failed, make sure you input the correct email and password or Sign up if you haven't")
        
    def logOut(self):
        return self.supabase.auth.sign_out()
    
