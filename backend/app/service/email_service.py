from fastapi_mail import FastMail, MessageSchema, MessageType
from backend.app.core.email_config import conf
from pydantic import EmailStr


mail = FastMail(conf)


async def send_welcome_email(recipient_email: list[EmailStr]):

    html= """ 
    <h1> welcome</h1>
    <p>your accounthas been created successfully</p>
    """

    message= MessageSchema(
        subject= "Welcome to our platform",
        recipients= [recipient_email],
        body= html,
        subtype= "html"
    )

    await mail.send_message(message)