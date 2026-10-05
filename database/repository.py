from psycopg import sql

from database import get_connection, release_connection


def insert_item(name, category, unit, critical_balance):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO item(name, category, unit, critical_balance) VALUES (%s,%s,%s,%s) RETURNING ID;', (name, category, unit, critical_balance))
        rez = cur.fetchone()  # Get id insert item
        id_item = rez[0]
        # Добавление колличества item в таблицу с остатками
        cur.execute('INSERT INTO stock(id_item,quantity) VALUES (%s, %s)', (id_item, critical_balance))
        conn.commit()
        return "Успешное добавление карточки товара"
    except Exception as e:  # noqa: BLE001
        # ВАЖНО: Если что-то пошло не так (например, дубликат или ошибка типа),
        # обязательно откатываем транзакцию перед тем, как вернуть коннект в пул
        conn.rollback()

        print(f'Ошибка при добавлении товара: {e}')
    finally:
        release_connection(conn)


def delete_item(id):
    conn=get_connection()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM item WHERE id=%s', (id))
        cur.execute('DELETE FROM stock WHERE id_item=%s', (id))
        conn.commit()
        return "Успешное удаление карточки товара"
    except Exception as e:  # noqa: BLE001
        print(f'Ошибка при удалении товара: {e}')
    finally:
        release_connection(conn)


def select_item(form, data):
    conn=get_connection()
    try:
        cur = conn.cursor()
        column_name = form
        query = sql.SQL('SELECT * FROM item WHERE {column}= %s').format(
            column = sql.Identifier(column_name))
        cur.execute(query, (data,))
        rows = cur.fetchall()
        conn.rollback()
        return rows
    except Exception as e:  # noqa: BLE001
        print(f'Ошибка поиске товара: {e}')
    finally:
        release_connection(conn)
