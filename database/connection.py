import atexit

from psycopg_pool import ConnectionPool

# import streamlit as st

# @st.cache_resource
def _init_pool():
    pool = ConnectionPool(
        min_size=1,
        max_size=10,
        conninfo='dbname=accounting_system user=postgres host=127.0.0.1 port=5432',
        open=True
    )
    atexit.register(pool.close)
    return pool

_pool= _init_pool()

def get_connection():
    return _pool.getconn()


def release_connection(conn):
    return _pool.putconn(conn)
