from typing import List
from pydantic import BaseModel, NameEmail




class EmailSchema(BaseModel):
    email: List[NameEmail]