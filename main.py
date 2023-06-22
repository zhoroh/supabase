
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Depends
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from auth_service import AuthService
from customer_service import CustomerService
from types_ import SignUpDto,InsertDto,UpdateDto
load_dotenv()
security = HTTPBearer()
log_format = "%(asctime)s::%(levelname)s::%(name)s::"\
             "%(filename)s::%(lineno)d::%(message)s"
logging.basicConfig(level='DEBUG', format=log_format)
logging.info("successfully imported needed libraries")

prefix = ""
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

tags_metadata = [
    {
        "name":"auth-service",
        "description": "Auth service for users",
    },
    {
        "name":'Customer Service',
        "description": "Customer Service for Users"
    }
]

app = FastAPI(
    docs_url=prefix + "/dev/documentation",
    openapi_url=prefix + "/openapi.json",
    title="Services for a user",
    description="Auth service and Customer Service API Documentation",
    openapi_tags=tags_metadata
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



logging.info("FASTAPI app initialized successfully")

authService = AuthService(url,key)
customerService = CustomerService(authService.supabase)

@app.get(f'{prefix}/')
def root():
     return "Hello World"

@app.post(prefix +"/auth-service/signup", tags=["auth-service"])
def signUp(payload:SignUpDto):
    return authService.signUp(payload.email, payload.password)

@app.post(prefix +"/auth-service/signin", tags=["auth-service"])
def signIn(payload:SignUpDto):
    return authService.signIn(email=payload.email, password=payload.password)
    

@app.post(prefix +"/auth-service/logout", tags=["auth-service"])
def logOut():
    return authService.logOut()

@app.post(prefix +"/customer-service/create-record", tags=["customer-service"])
def addRecord(payload:InsertDto,authorization:str = Depends(security)):
    return customerService.create(payload,authorization.credentials)

@app.post(prefix +"/customer-service/update-record", tags=["customer-service"])
def updateRecord(payload:UpdateDto,authorization:str = Depends(security)):
    return customerService.update(payload,authorization.credentials)

