from psycopg2.pool import ThreadedConnectionPool


def get_pool():
    return ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        dsn = 'dbname= accounting_system, user=postgre'
    )


def get_connection():
    return get_pool().getconn()


def release_connection(conn):
    return get_pool().putconn()
