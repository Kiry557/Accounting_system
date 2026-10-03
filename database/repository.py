from database import get_connection, release_connection


def insert_item(name, category, unit, critical_balance):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO item(name, category, unit, critical_balance) VALUES (%s,%s,%s,%s)', (name, category, unit, critical_balance))
        id_item = cur.lastrowid # Get id insert item
        cur.execute('INSERT INTO stock(id_item,quantity) VALUES (%s, %s)', (id_item, critical_balance))
        conn.commit()
    except Exception as e:  # noqa: BLE001
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
    except Exception as e:  # noqa: BLE001
        print(f'Ошибка при удалении товара: {e}')
    finally:
        release_connection(conn)


def select_item(form, data):
    conn=get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM item WHERE {form}= %s', (data))
        rows = cur.fetchall()
        return rows
    except Exception as e:  # noqa: BLE001
        print(f'Ошибка поиске товара: {e}')
    finally:
        release_connection(conn)
