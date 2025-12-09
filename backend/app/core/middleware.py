from collections import defaultdict
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict

async def register_middleware(app: FastAPI):
    

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time= time.time()

        response = await call_next(request)
        processing_time= time.time() - start_time

        message= f"{request.client.host} : {request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}"

        print(message)
        return response

    app.add_middleware(
            CORSMiddleware,
            allow_origins= ["*"],
            allow_methods= ["*"],
            allow_headers= ["*"],
            allow_credentials= True
    ) 

    app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts= []  # your domain
    )
                       
                       
    
class AdvancedMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float]= defaultdict(float)
    async def log_message(self, message: str):
        print(message)
    async def dispatch(self, request: Request, call_next):
        client_ip= request.client.host
        current_time= time.time()

        if current_time- self.rate_limit_records[client_ip] < 1: # 1 request per second limit
            return Response(content="rate limit exceeded", status_code=429)
        
        self.rate_limit_records[client_ip]= current_time

        path= request.url.path
        await self.log_message(f"request to {path}")

        #process sthe request

        start_time= time.time()
        response= await call_next(request)
        process_time= time.time() - start_time


        #add custom header without modifying he original headers object

        custom_headers= {"X-Process-Time": str(process_time)}
        for header, value in custom_headers.items():
            response.headers.append(header, value)


        #asynchronous logging for processing time

        await self.log_message(f"response for {path} took {process_time} seconds")

        return response
    
    

        






