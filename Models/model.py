from typing import Optional, Set
from pydantic import BaseModel


class User_Model(BaseModel):
    username: str
    email: str
    mobileno: int
    password: str
    status: bool


class Login(BaseModel):
    username: str
    password: str


class Logout(BaseModel):
    token: str


class DeleteUser(BaseModel):
    username: str


class File_Upload(BaseModel):
    guid = str
    filename = str
    path = str
