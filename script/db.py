from dotenv import load_dotenv
from os import environ as env
from mysql.connector import connect, Error, IntegrityError, DatabaseError
import dataseed

from table import typer_style

load_dotenv()

def create_server_connection():
    '''Membuat koneksi dengan MySQl server'''

    connection = None
    try:
        connection = connect(
            user=env.get('USERNAME'),
            password=env.get('PASSW'),
            host=env.get('HOST'),
            port=env.get('PORT'),
            database=env.get('DB'),
        )
    except Error as err:
        typer_style(f'{err}', 'RED')

    return connection


def query(connection, query, data=None, many=False, fetch=None):
    '''Insert, update, delete database'''

    cur = connection.cursor()
    try:
        if many:
            cur.executemany(query, data)
        else:
            cur.execute(query, data)

        if fetch:
            return cur.fetchall()
        else:
            connection.commit()

    except (IntegrityError, DatabaseError, Error) as err:
        typer_style(f'Failed. You have an error message: {err}', 'RED')
    finally:
        cur.close()


def populate_db():
    '''Menginisialisasi database dengan data default dari file ddl.sql'''

    sql_customers = 'INSERT INTO customers(first_name, last_name, cust_id) VALUES(%s, %s, %s);'
    sql_items = 'INSERT INTO items(nama_item, harga_per_item) VALUES(%s, %s);'

    try:
        with create_server_connection() as con:
            query(con, sql_customers, dataseed.seed_customers, many=True)
            query(con, sql_items, dataseed.seed_items, many=True)
            typer_style('Database is successfully initilized.')
    except Error as err:
        typer_style(
            f'Sorry, something happened. Failed to load the database. {err}', 'RED')


def initial_db():
    '''Menampilkan (print) SQL script yang menginisialisasi database dengan default data'''
    try:
        with create_server_connection() as con:
            with con.cursor() as cur:
                with open('ddl.sql', 'r') as file:
                    for statement in cur.execute(file.read(), multi=True):
                        print(f"Executed: {statement.statement}")
    except Error as err:
        typer_style(f'Error: {err}', 'RED')


def show_all_items():
    '''Menampilkan semua item yang bisa dibeli'''
    try:
        with create_server_connection() as con:
            sql_script = 'SELECT * FROM items;'
            return query(con, sql_script, fetch=True)
    except Error as err:
        typer_style(f'Sorry, nothing found. {err}', 'RED')


def add_customers(customers_details):
    '''Menambahkan customer baru'''
    try:
        with create_server_connection() as con:
            sql_script = 'INSERT INTO customers(first_name, last_name, cust_id) VALUES(%s, %s, %s);'
            query(con, sql_script, customers_details)
    except Error as err:
        typer_style(f'Error: {err}', 'RED')


def show_customers(cust_id):
    '''Men-display customer berdasarkan customer ID'''
    try:
        with create_server_connection() as con:
            data = (cust_id, )
            sql_script = 'SELECT first_name, last_name FROM customers WHERE cust_id LIKE %s'

            return query(con, sql_script, data=data, fetch=True)
    except Error as err:
        typer_style(f'Error: {err}', 'RED')


def query_items(nama_item):
    '''Men-query items dari database'''
    try:
        with create_server_connection() as con:
            data = (nama_item, )
            sql_script = 'SELECT nama_item, harga_per_item FROM items WHERE nama_item LIKE %s'

            return query(con, sql_script, data=data, fetch=True)
    except Error as err:
        typer_style(f'Error: {err}', 'RED')


def query_item_kerabat(nama_item):
    '''Menammpilkan item yang masih berhubungan deng nama item yang dicari ketika ada kasus typo dari user'''
    try:
        with create_server_connection() as con:
            item = ('%' + nama_item + '%',)
            sql_script = 'SELECT nama_item, harga_per_item FROM items WHERE nama_item LIKE %s'

            return query(con, sql_script, data=item, fetch=True)
    except Error:
        print(f'Maaf, {nama_item} tidak ditemukan. Silahkan coba lagi.')


def update_nama_item(nama_item_baru, nama_item_lama):
    '''Meng-update nama item di database - hanya admin'''
    try:
        with create_server_connection() as con:
            sql_script = 'UPDATE items SET nama_item = %s WHERE nama_item = %s;'
            data = (nama_item_baru, nama_item_lama)

            return query(con, sql_script, data=data)
    except Error as err:
        typer_style(f'Error: {err}', 'RED')


def update_harga_item(harga_item_baru, nama_item):
    '''Meng-update harga item di database - hanya admin'''
    try:
        with create_server_connection() as con:
            sql_script = 'UPDATE items SET harga_per_item = %s WHERE nama_item = %s;'
            data = (harga_item_baru, nama_item)

            return query(con, sql_script, data=data)
    except Error as err:
        typer_style(f'Error: {err}', 'RED')


def add_transaction_to_db(transaction_details):
    try:
        with create_server_connection() as con:
            sql_script = 'INSERT INTO transactions(transaction_date, transaction_id, nama_item, jumlah_item, total_belanja, cust_id) VALUES(%s, %s, %s, %s, %s, %s);'
            query(con, sql_script, transaction_details)

            print(
                f'Transaction id: {transaction_details[1]} dari customer {transaction_details[5]} berhasil ditambahkan dalam database.')
    except Error as err:
        typer_style(f'Error: {err}', 'RED')
