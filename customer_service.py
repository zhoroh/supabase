import logging
import jwt
from fastapi import HTTPException,status
from supabase import Client
from types_ import InsertDto, UpdateDto
from dotenv import load_dotenv
import postgrest.exceptions
import ast
load_dotenv()

log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(level='DEBUG', format=log_format)


class CustomerService:
    def __init__(self,supabase):
        self.supabase :Client = supabase
    def create(self,payload:InsertDto,access_token:str):
        try:
            self.supabase.postgrest.auth(access_token)
            user = jwt.decode(access_token,algorithms=["HS256"],options={"verify_signature": False})
            user_uid = user['sub']
            payload = payload.dict()
            payload['user_id'] = user_uid
            print(payload)
            data,count = self.supabase.table('customers').insert(payload).execute()
           
            return data[1]
        except postgrest.exceptions.APIError as e:
            e = e.args[0]
            e = ast.literal_eval(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e['message'].replace('\"', ''))
    
    def update(self,payload:UpdateDto,access_token:str):
        try:
            self.supabase.postgrest.auth(access_token)
            user = jwt.decode(access_token,algorithms=["HS256"],options={"verify_signature": False})
            user_uid = user['sub']
            data,count = self.supabase.table('customers').update(payload.dict()).eq('user_id',user_uid).execute()
            return data[1]
        except postgrest.exceptions.APIError as e:
            e = e.args[0]
            e = ast.literal_eval(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e['message'].replace('\"', ''))
    
