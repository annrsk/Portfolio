from models import Client, Employee, EmployeeCreate, ClientCreate, Offer, OfferCreate
from fastapi import HTTPException

#employees crud func
def get_employees_db(conn):
    with conn.cursor() as cur:
       cur.execute('''select * 
                   from  "savushkin_CRM".employees''')
       rows = cur.fetchall()
       if not rows:
         raise HTTPException(status_code=404, detail='Employees not found')
       column_name = [desc[0] for desc in cur.description]
       employees = []
       for row in rows:
          employee_dict = dict(zip(column_name, row))
          employee = Employee(**employee_dict)
          employees.append(employee)
    print('GET EMPLOYEES OK')
    return employees


def get_employee_id_db(conn, empl_id):
   with conn.cursor() as cur:
      cur.execute('''select * 
                  from "savushkin_CRM".employees 
                  where id = %s''',
                  (empl_id,))
      employee = cur.fetchone()
      if not employee:
         raise HTTPException(status_code=404, detail='Did not find that employee')
      print('GET EMPLOYEE USING ID OK')
      return employee


def create_employee_db(conn, data: EmployeeCreate):
   with conn.cursor() as cur:
      cur.execute('''insert into "savushkin_CRM".employees(full_name, position, department, email, phone)
                  values (%s, %s, %s, %s, %s)
                  returning id, full_name, position, department, email, phone''',
                  (data.full_name, data.position, data.department, data.email, data.phone))
      row = cur.fetchone()
      if not row:
         raise HTTPException(status_code=500, detail='Failed to create employee')
      column_name = [desc[0] for desc in cur.description]
      employee_dict = dict(zip(column_name, row))
      print('CREATE EMPLOUEE OK')
      return Employee(**employee_dict)


def update_employee_bd(conn, empl_id: int, data: EmployeeCreate):
   with conn.cursor() as cur:
      cur.execute('''update "savushkin_CRM".employees 
                  set full_name=%s, position=%s, department=%s, email=%s, phone=%s 
                  where id = %s
                  returning *''',
                   (data.full_name, data.position, data.department, data.email, data.phone, empl_id))
      row = cur.fetchone()
      if not row:
         raise HTTPException(status_code=500, detail='Failed to update employee')
      column_name = [desc[0] for desc in cur.description]
      employee_dict = dict(zip(column_name, row))
      print('EPDATE EMPLOYEE OK')
      return Employee(**employee_dict)


def delete_employee_bd(conn, empl_id: int):
   with conn.cursor() as cur:
      cur.execute('''select * 
                  from "savushkin_CRM".employees 
                  where id = %s''',
                  (empl_id,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Did not find that employee')
      else:
         cur.execute('''delete from "savushkin_CRM".employees 
                  where id = %s''',
                  (empl_id,))
      print('EMPLOYEE DELET OK')
      return {f'deleted employee with id = {empl_id}'}


#clients crud func
def get_clients_db(conn):
   with conn.cursor() as cur:
      cur.execute('''select * from "savushkin_CRM".clients''')
      rows = cur.fetchall()
      if not rows:
         raise HTTPException(status_code=404, detail='Clients not found')
      column_name = [disc[0] for disc in cur.description]
      clients = []
      for row in rows:
         client_dict = dict(zip(column_name, row))
         client = Client(**client_dict)
         clients.append(client)
      print('GET CLIENTS OK')
      return clients


def get_client_id_db(conn, cl_id):
   with conn.cursor() as cur:
      cur.execute('''select * 
                  from "savushkin_CRM".clients
                  where id = %s''',
                  (cl_id,))
      client = cur.fetchone()
      if not client:
         raise HTTPException( status_code=404, detail = 'Did not find that client')
      print('GET CLIENT OK')
      return client


def create_client_db(conn, data: ClientCreate):
   with conn.cursor() as cur:
      cur.execute('''select id 
                  from "savushkin_CRM".employees 
                  where id = %s''', 
                  (data.responsible_manager_id,))
      manager_exists = cur.fetchone()
      if not manager_exists:
         raise HTTPException(status_code=404, detail='Введенный ответсвенные менеджер не найден в базе данных')
      cur.execute('''insert into "savushkin_CRM".clients(company_name, inn, address, client_type, status, responsible_manager_id)
                  values(%s, %s, %s, %s, %s, %s) 
                  returning id, company_name, inn, address, client_type, status, responsible_manager_id''', 
                  (data.company_name, data.inn, data.address, data.client_type, data.status, data.responsible_manager_id))
      row = cur.fetchone()
      if not row:
         raise HTTPException(status_code=500, detail='Failed to create client')
      column_name = [desc[0] for desc in cur.description]
      client_dict = dict(zip(column_name, row))
      print('CREATE CLIENT OK')
      return Client(**client_dict)


def update_client_db(conn, cl_id: int, data: ClientCreate):
   with conn.cursor() as cur:
      cur.execute('''select id 
                  from "savushkin_CRM".clients
                  where id =%s''',
                  (cl_id,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Did not finf that client')
      cur.execute('''select id 
                  from "savushkin_CRM".employees 
                  where id = %s''', 
                  (data.responsible_manager_id,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Введенный ответсвенные менеджер не найден в базе данных')
      cur.execute('''update "savushkin_CRM".clients
                  set company_name=%s, inn=%s, address=%s, client_type=%s, status=%s, responsible_manager_id=%s
                  where id=%s''',
                  (data.company_name, data.inn, data.address, data.client_type, data.status, data.responsible_manager_id, cl_id))
      upd_client = cur.fetchone()
      if not upd_client:
         raise HTTPException(status_code=500, detail='Failed to update client')
      column_names = [desc[0] for desc in cur.description]
      client_dict = dict(zip(column_names, upd_client))
      updated_client = Client(**client_dict)
      return updated_client

def delete_client_db(conn, cl_id:int):
   with conn.cursor() as cur:
      cur.execute('''select id 
                  from "savushkin_CRM".clients
                  where id =%s''',
                  (cl_id,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Did not find that client')
      cur.execute('''delete from "savushkin_CRM".clients
                  where id =%s''',
                  (cl_id,))
      print('DELETE CLIENT OK')
      return{f'Deleted client with id = {cl_id}'}



#offers crud func
def get_offers_db(conn):
   with conn.cursor() as cur:
      cur.execute('''select *
                  from "savushkin_CRM".commercial_offers''')
      rows = cur.fetchall()
      if not rows:
         raise HTTPException(status_code=404, detail='Offers are not found')
      columns_names = [desc[0] for desc in cur.description]
      offers = []
      for row in rows:
         offer_dict = dict(zip(columns_names, row))
         offer = Offer(**offer_dict)
         offers.append(offer)
      print('GET OFFERS OK')
      return offers

def get_offer_id_db(conn, off_id: int):
   with conn.cursor() as cur:
      cur.execute('''select * 
                  from "savushkin_CRM".commercial_offers
                  where id=%s''',
                  (off_id,))
      row = cur.fetchone()
      if not row:
         raise HTTPException(status_code=404, detail='Did not find that offer')
      column_names = [desc[0] for desc in cur.description]
      off_dict = dict(zip(column_names, row))
      offer = Offer(**off_dict)
      return offer


def create_offer_db(conn, data: OfferCreate):
   with conn.cursor() as cur:
      cur.execute('''select id
                  from "savushkin_CRM".clients
                  where id = %s''',
                  (data.client_id,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Did not find that client')
      cur.execute('''select id
                  from "savushkin_CRM".employees
                  where id=%s''',
                  (data.created_by,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Did not find that employee')
      cur.execute('''insert into "savushkin_CRM".commercial_offers(client_id, valid_until, total_amount, status, created_by)
                  values (%s, %s, %s, %s, %s)
                  returning id, client_id, created_at, valid_until, total_amount, status, created_by''',
                  (data.client_id, data.valid_until, data.total_amount, data.status, data.created_by))
      row = cur.fetchone()
      if not row:
         raise HTTPException(status_code=500, detail='Failed create offer')
      column_names = [desc[0] for desc in cur.description]
      offer_dict = dict(zip(column_names, row))
      print('CREATED OFFER OK')
      offer = Offer(**offer_dict)
      return offer


def update_offer_db(conn, off_id:int, data: OfferCreate):
   with conn.cursor() as cur:
      cur.execute('''select id 
                  from "savushkin_CRM".commercial_offers
                  where id=%s''', 
                  (off_id,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Did not find that offer')
      cur.execute('''update "savushkin_CRM".commercial_offers
                  set client_id=%s, valid_until=%s, total_amount=%s, status=%s, created_by=%s
                  where id=%s
                  returning *''',
                  (data.client_id, data.valid_until, data.total_amount, data.status, data.created_by, off_id))
      row = cur.fetchone()
      if not row:
         raise HTTPException(status_code=500, detail='Failed to update offet')
      column_names = [desc[0] for desc in cur.description]
      offer_dict = dict(zip(column_names, row))
      print('CREATED UPDATED OK')
      offer = Offer(**offer_dict)
      return offer


def delete_offer_db(conn, off_id: int):
   with conn.cursor() as cur:
      cur.execute('''select id 
                  from "savushkin_CRM".commercial_offers
                  where id =%s''',
                  (off_id,))
      if not cur.fetchone():
         raise HTTPException(status_code=404, detail='Did not find that offer')
      cur.execute('''delete from "savushkin_CRM".commercial_offers
                  where id =%s''',
                  (off_id,))
      print('DELETE OFFER OK')
      return{f'Deleted client with id = {off_id}'}