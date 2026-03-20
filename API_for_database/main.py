import psycopg2 as ps2
from fastapi import FastAPI
from crud_func import *
from models import Employee, Client, EmployeeCreate, ClientCreate, Offer, OfferCreate
from typing import List
from database import*

app = FastAPI(title='Савушкин CRM')


@app.get('/')
def root():
  return {'Hello hello. This is Savuskhin CRM API.\nEndpoints: /employees, /clients /offers.\nYou can check API in /docs'}

#EMPLOYEES API
@app.get('/employees/', response_model=List[Employee])
def get_employees():
  conn = create_conn()
  employees = get_employees_db(conn)
  close_conn(conn)
  return employees


@app.get('/employees/{employee_id}')
def get_employee_id(employee_id: int):
  conn = create_conn()
  employee = get_employee_id_db(conn, employee_id)
  close_conn(conn)
  return employee


@app.post('/employees/', response_model=Employee)
def create_employee(empl: EmployeeCreate):
  conn = create_conn()
  try:
      new_employee = create_employee_db(conn, empl)
      conn.commit()
      close_conn(conn)
      return new_employee
  except Exception as e:
    conn.rollback()  
    close_conn(conn)
    return {f'error creating empoyee: {str(e)}'}


@app.put('/employees/{employee_id}')
def update_employee(empl_id: int, empl: EmployeeCreate):
  conn = create_conn()
  try:
    updated_employee = update_employee_bd(conn, empl_id, empl)
    conn.commit()
    close_conn(conn)
    return updated_employee
  except Exception as e:
    conn.rollback()  
    close_conn(conn)
    return {f'error updating employee: {str(e)}'}


@app.delete('/employees/{employee_id}')
def delete_employee(empl_id: int):
  conn = create_conn()
  try:
    deleted_empl = delete_employee_bd(conn, empl_id)
    conn.commit()
    close_conn(conn)
    return deleted_empl
  except Exception as e:
    conn.rollback()  
    close_conn(conn)
    return {f'error deleting employee: {str(e)}'}

#CLIENTS API
@app.get('/clients/', response_model=List[Client])
def get_clients():
  conn = create_conn()
  clients = get_clients_db(conn)
  close_conn(conn)
  return clients

@app.get('/clients/{client_id}')
def get_client_id(client_id: int):
  conn = create_conn()
  client = get_client_id_db(conn, client_id)
  close_conn(conn)
  return client


@app.post('/clients/', response_model=Client)
def create_client(cl: ClientCreate):
  conn = create_conn()
  try:
    new_client = create_client_db(conn, cl)
    conn.commit()
    close_conn(conn)
    return new_client
  except Exception as e:
    conn.rollback()  
    close_conn(conn)
    return {f'error creating client: {str(e)}'}


@app.put('/clients/{client_id}', response_model=Client)
def update_client(cl_id:int, cl: ClientCreate):
  conn = create_conn()
  try:
    updated_client = update_client_db(conn, cl_id, cl)
    conn.commit()
    close_conn(conn)
    print('UPDATE CLIENT OK')
    return updated_client
  except Exception as e:
    conn.rollback()  
    close_conn(conn)
    return {f'error updating client: {str(e)}'}    


@app.delete('/clients/{client_id}')
def delete_client(cl_id:int):
  conn = create_conn()
  try:
    deleted_cl = delete_client_db(conn, cl_id)
    conn.commit()
    return deleted_cl
  except Exception as e:
    return {f'error deleting client: {str(e)}'}


#OFFERS API
@app.get('/offers/', response_model=List[Offer])
def get_offer():
  conn = create_conn()
  try:
    offers = get_offers_db(conn)
    close_conn(conn)
    return offers
  except Exception as e:
    conn.rollback()  
    close_conn(conn)
    return {f'error getting offers: {str(e)}'}


@app.get('/offers/{offer_id}')
def get_offer(off_id: int):
  conn = create_conn()
  try:
    offer = get_offer_id_db(conn, off_id)
    close_conn(conn)
    return offer
  except Exception as e:
    conn.rollback()  
    close_conn(conn)
    return {f'error getting offers: {str(e)}'}


@app.post('/offers/', response_model=Offer)
def create_offer(off: OfferCreate):
  conn = create_conn()
  try:
    new_offer = create_offer_db(conn, off)
    conn.commit()
    close_conn(conn)
    return new_offer
  except Exception as e:
    conn.rollback()
    close_conn(conn)
    return {f'error creating offer: {str(e)}'}


@app.put('/offers/{offer_id}', response_model=Offer)
def update_offer(off_id: int, off: OfferCreate):
  conn = create_conn()
  try:
    updated_offer = update_offer_db(conn, off_id, off)
    conn.commit()
    close_conn(conn)
    return updated_offer
  except Exception as e:
    conn.rollback()
    close_conn(conn)
    return {f'error updat offer: {str(e)}'}


@app.delete('/offers/{offer_id}')
def delete_offer(off_id: int):
  conn = create_conn()
  try:
    deleted_offer = delete_offer_db(conn, off_id)
    conn.commit()
    return deleted_offer
  except Exception as e:
    conn.rollback()
    close_conn(conn)
    return {f'error deleting offer: {str(e)}'}