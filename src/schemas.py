from datetime import datetime
from pydantic import BaseModel, validator


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: str
    additional_data: str = None

    @validator("birthday")
    def validate_birthday(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
        return value


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    class Config:
        orm_mode = True
