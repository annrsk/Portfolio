import psycopg2 as ps2
import os

def create_conn():
  conn = ps2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'))
  return conn

def close_conn(conn):
  conn.close()