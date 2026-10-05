from datetime import date

import psycopg

from database import get_connection, release_connection


# Допилить до нормального вида
def checkCriticalLevelStock():
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute('SELECT name FROM item')
        rows_nameItems = cur.fetchall()

        cur.execute('SELECT critical_balance FROM item')
        rows_valueCriticalLevel = cur.fetchall()
        cur.execute('SELECT quantity FROM stock')
        rows_quantityNow = cur.fetchall()
        conn.rollback()
        error_criticalLevel = []
        for name_item, criticalLevel, quantity in rows_nameItems,rows_valueCriticalLevel, rows_quantityNow:
            if quantity <= criticalLevel:
                error = f'Критический уровень {name_item} пополните запас'
                error_criticalLevel.append(error)

        return error_criticalLevel
    except psycopg.Error as e:
        print('Ошибка запроса к базе', e)
    finally:
        release_connection(conn)


# Проверка возможности списания при совершении операции
def checkPossibilWrite(name_item, quantity_write, type_operation):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT ID FROM item WHERE name=%s', name_item)
        id  = cur.fetchone()
        cur.execute('SELECT quantity FROM stock  WHERE id_item=%s', id)
        stock = cur.fetchone()
        conn.rollback()
        if type_operation == "writeOffQuantity":
            return not stock - quantity_write <= 0
    except psycopg.Error as e:
        print('Ошибка запроса к базе', e)
    finally:
        release_connection(conn)

# получение даных о списании и формирование строки с
def transaction(id_product, type_transaction,quantity, commit):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT unit FROM item WHERE ID=%s", id_product)
        units = cur.fetchone()
        date_today = date.today()  # noqa: DTZ011
        cur.execute('INSERT INTO transactions(id_product, type_transaction, quantity, unit, date_transaction, commit) VALUES (%s,%s,%s,%s,%s,%s)',
            (id_product, type_transaction, quantity, units, date_today, commit))
        conn.commit()
    except psycopg.Error as e:
        print('Ошибка запроса к базе', e)

    finally:
        release_connection(conn)


# Функционал сотрудника
def updateStockQuantity(name_item, new_stock, type_operation, commit):
    conn = get_connection()
    try:
        cur = conn.cursor()
        if checkPossibilWrite(name_item, new_stock, type_operation) == False:
            return "Данная операция невозможна, укажите другое значение"
        else:
            cur.execute('UPDATE stock SET quantity=%s WHERE name_item=%s', (new_stock, name_item))
            conn.commit()
            transaction(name_item,type_operation, new_stock, commit)
            return "Операция успешно выполнена"
    except psycopg.Error as e:
        print('Ошибка запроса к базе', e)

    finally:
        release_connection(conn)
