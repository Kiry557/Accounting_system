import pandas as pd
from psycopg import errors

from database import get_connection
from database.connection import release_connection

# test code for internet

def forming_report(query, name_fileReport, sheet_nameReport):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.rollback()
        data = cur.fetchall()
        columns=[desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)

        output_file = f'report/{name_fileReport}.xlsx'
        save_report(df, output_file, sheet_nameReport)

        return "Отчет сформирован"
    except errors.QueryCanceled as e:
        return ("Ошибка", e)
    finally:
        release_connection(conn)

def save_report(df, output_file, sheet_nameReport):
    try:
        df.to_excel(output_file, index=False, sheet_name=f'{sheet_nameReport}')
    except PermissionError as e:
        return ('Ошибка при сохранении файла',e)
