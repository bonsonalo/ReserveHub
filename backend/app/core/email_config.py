from fastapi_mail import ConnectionConfig
import os
from dotenv import load_dotenv
load_dotenv() 



MAIL_PASS = os.getenv("MAIL_PASS")
MAIL_USERNAME= os.getenv("MAIL_USERNAME")

conf= ConnectionConfig(
    MAIL_USERNAME= MAIL_USERNAME,
    MAIL_PASSWORD= MAIL_PASS,
    MAIL_FROM= "bonson2468@gmail.com",
    MAIL_PORT= "2525",
    MAIL_SERVER= "sandbox.smtp.mailtrap.io",
    MAIL_FROM_NAME= "my_app",
    MAIL_STARTTLS= True,
    MAIL_SSL_TLS= False,
    USE_CREDENTIALS= True,
    VALIDATE_CERTS= True
    )