import psycopg2 as ps2
from pydantic import BaseModel
from datetime import datetime

class Employee(BaseModel):
   id: int
   full_name: str
   position: str
   department: str
   email: str
   phone: str

   class Config:
      from_attributes = True

class Client(BaseModel):
   id: int
   company_name: str
   inn: str
   address: str
   client_type: str
   status: str
   responsible_manager_id: int

   class Config:
      from_attributes = True

class EmployeeCreate(BaseModel):
  full_name: str
  position: str
  department: str
  email: str
  phone: str

class ClientCreate(BaseModel):
   company_name: str
   inn: str
   address: str
   client_type: str
   status: str
   responsible_manager_id: int

class Offer(BaseModel):
   id: int
   client_id: int
   created_at: datetime
   valid_until: datetime
   total_amount: int
   status: str
   created_by: int

class OfferCreate(BaseModel):
   client_id: int
   valid_until: datetime
   total_amount: int
   status: str
   created_by: int