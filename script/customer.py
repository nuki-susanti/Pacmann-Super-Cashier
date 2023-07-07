import string
import random

from db import add_customers, show_customers
from table import pretty_table, typer_style


class Customer:
    def __init__(self):
        self.cust_id = 'guest'

    def new_customer(self):
        '''Mendaftarkan / menambah  customer baru'''
        try:
            first_name = input('Masukkan nama depan anda: ').lower()
            last_name = input('Masukkan nama belakang anda: ').lower()

            digits = string.digits
            result_digits = ''.join(random.choice(digits) for i in range(2))

            self.cust_id = first_name[0] + first_name[len(first_name)-1] + last_name[0] + last_name[len(last_name)-1] + result_digits

            customer_details = (first_name, last_name, self.cust_id)
            add_customers(customer_details)

            typer_style(f'{first_name.title()} {last_name.title()}, Selamat datang di layanan kami, Self-Cashier!')
            typer_style(f'Customer ID anda adalah {self.cust_id}')

            return self.cust_id
        except:
            typer_style('Ooops.. anda sudah terdaftar sebagai customer kami.')


    def old_customer(self):
        '''Men-query customer_id dari database untuk customer lama / existing customer'''
        try:
            self.cust_id = input('Masukkan customer ID anda: ').lower()
            customer_details = show_customers(self.cust_id)

            if customer_details:
                print(
                    f'Selamat datang kembali di layanan Self-Cashier, {customer_details[0][0].title()} {customer_details[0][1].title()}!')
                return self.cust_id
        except:
            typer_style('Ooops.. anda belum terdaftar sebagai customer kami.')

        
    def add_customer(self):
        '''Menyimpan customer baru dalam database'''
        while True:
            try:
                typer_style('Apakah anda customer baru?')
                user_answer = input('Ketik "Y" untuk mendaftar sebagai customer baru Self-Cashier! atau "N" untuk customer terdaftar: ').strip().lower()

                if user_answer == 'y':
                    self.new_customer()
                    break
                elif user_answer == 'n':
                    self.old_customer()
                    break
                else:
                    print('Maaf anda belum terdaftar di sistem kami. Silahkan mendaftar terlebih dahulu.')
            except ValueError as err:
                typer_style(f'{err}', RED)
