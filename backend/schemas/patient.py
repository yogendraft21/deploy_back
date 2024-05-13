from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    email: str
    mobile: str
    address:str

    class Config():
        orm_mode = True
