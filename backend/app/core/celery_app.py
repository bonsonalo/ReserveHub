from typing import List
from celery import Celery
from fastapi_mail import MessageSchema
from pydantic import EmailStr

from backend.app.service.email_service import send_welcome_email
from backend.app.service.email_service import mail
from asgiref.sync import async_to_sync

celery_app= Celery(
    "reservehub-worker",
    broker_url= "redis://localhost:6379/0",
    result_backend= "redis://localhost:6379/1" 
)

celery_app.conf.task_routes= { 
    "app.tasks.*": {"queue": "default"}
}



@celery_app.task()
def send_welcome_email_task(recipient_email: list[EmailStr]):

    async_to_sync(send_welcome_email)(recipient_email)