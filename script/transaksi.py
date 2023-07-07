import random
from datetime import date
import string

from customer import Customer
from admin import Adminonly
from db import show_all_items, query_items, query_item_kerabat, add_transaction_to_db
from helper import tuple_to_list, list_to_tuple
from table import pretty_table, typer_style

class Cashier(Customer):
    def __init__(self):
        self.transaction_date = date.today()
        self.cust_id = 'guest'
        self.transaction_id = self.transaction()
        self.keranjang_belanja_total = []
        self.total_belanja = 0

    def transaction(self):
        '''Menghasilkan output 8 karakter transaction_id'''

        letters = string.ascii_lowercase
        digits = string.digits
        result_letters = ''.join(random.choice(letters) for i in range(4))
        result_digits = ''.join(random.choice(digits) for i in range(4))
        self.transaction_id = result_letters + result_digits

        return self.transaction_id

    def display_all_items(self):
        pretty_table(data=show_all_items(), headers='y')


    def total_harga_belanja(self):
        '''Menghitung total belanja dari item dalam keranjang'''

        self.total_belanja = 0
        for item in self.keranjang_belanja_total:
            self.total_belanja += item[4]

        return self.total_belanja


    def check_keranjang(self):
        '''Check order dalam keranjang belanja'''

        self.total_belanja = self.total_harga_belanja()
        if self.total_belanja > 200000:
            self.total_price()
        else:
            data = self.keranjang_belanja_total + [('Total belanja tanpa diskon', '-', '-', '-', self.total_belanja)]
            pretty_table(data=data)


    def check_order(self):
        self.check_keranjang()

        while True:
            user_input = input('Apakah pemesanan sudah benar? Ketik "Y" untuk membayar belanja anda atau ketik sembarang karakter untuk mengubah pesanan: ').strip().lower()

            if user_input == 'y' and len(self.keranjang_belanja_total) != 0:
                typer_style(f'Total belanja anda adalah Rp {self.total_belanja}')

                # Menyimpan transaksi ke dalam database
                for item in self.keranjang_belanja_total:
                    transaction_details = tuple([self.transaction_date, self.transaction_id, item[1], item[3], self.total_belanja, self.cust_id])
                    add_transaction_to_db(transaction_details)

                typer_style('Terimakasih telah memilih layanan Self-Cashier. Sampai jumpa!')
            if len(self.keranjang_belanja_total) == 0:
                typer_style('Maaf anda keranjang belanja anda masih kosong.', 'RED')
                break
            else:
                break
        

    def total_price(self):
        '''Menghitung harga diskon berdasarkan total belanja; 5%, 8% atau 10%'''

        try:
            disc = '0'
            harga_diskon = 0

            typer_style('Menampilkan semua item dalam keranjang...')

            # Menghitung total belanja
            self.total_harga_belanja()

            if 200000 < self.total_belanja <= 300000:
                harga_diskon = int(self.total_belanja * 0.95)
                disc = '5%'

            elif 300000 < self.total_belanja <= 500000:
                harga_diskon = int(self.total_belanja * 0.92)
                disc = '8%'
            elif self.total_belanja > 500000:
                harga_diskon = int(self.total_belanja * 0.9)
                disc = '10%'

            data = self.keranjang_belanja_total + [('Total belanja tanpa diskon', '-', '-', '-', self.total_belanja)] + [
                (f'Total belanja diskon {disc}', '-', '-', '-', harga_diskon)]

            pretty_table(data=data)

            # Meng-overwrite total belanja dengan harga yang telah didiskon
            self.total_belanja = harga_diskon

        except ValueError as err:
            typer_style(f'{err}', 'RED')


    def add_item(self):
        '''Menambah item ke dalam keranjang belanja'''

        while True:
            try:
                nama_item, jumlah_item = list(input('Masukkan nama item, jumlah item tersedia yang ingin dibeli: ').split(',', 2))
                nama_item, jumlah_item = [item.strip().lower() for item in [nama_item, jumlah_item]]

                jumlah_item = int(jumlah_item)

                # Men-query nama item dari database
                items_fetched = query_items(nama_item)

                if items_fetched:
                    harga_bayar = jumlah_item * items_fetched[0][1]
                    updated_item = tuple(
                        (len(self.keranjang_belanja_total)+1, ) + items_fetched[0]) + (jumlah_item, harga_bayar)

                    # Check item yang sama dan menambahkan jumlah item
                    item_sama = False
                    for index, item in enumerate(self.keranjang_belanja_total):
                        if item[1] == nama_item:
                            item_sama = True
                            jumlah_item += item[3]
                            updated_item = (item[0], items_fetched[0][0], items_fetched[0]
                                            [1], jumlah_item, jumlah_item * items_fetched[0][1])
                            self.keranjang_belanja_total[index] = updated_item

                    self.keranjang_belanja_total.append(updated_item)

                    if item_sama:
                        del self.keranjang_belanja_total[-1]

                    self.total_belanja = self.total_harga_belanja()

                    typer_style(f'{nama_item.capitalize()} berhasil dimasukkan dalam keranjang.')

                    if self.total_belanja > 200000:
                        self.total_price()
                    else:
                        data = self.keranjang_belanja_total + [('Total belanja tanpa diskon', '-', '-', '-', self.total_belanja)]
                        pretty_table(data=data)

                else:
                    typer_style(f'Maaf, "{nama_item}" tidak ada di toko kami. Silahkan memilih item yang tersedia.', 'RED')
                    fetched = query_item_kerabat(nama_item)

                    no = 0
                    data = []
                    for item in fetched: 
                        no += 1                  
                        data.append((no, ) + item)

                    pretty_table(data=data, headers='y')

                continue_or_not = input(
                    'Apakah anda ingin menambahkan item lagi? Ketik "Y" untuk menambah item atau ketik sembarang karakter untuk meyelesaikan transaksi: ').strip().lower()

                if continue_or_not == 'y':
                    return self.add_item()                
                else:
                    self.total_price()
                    typer_style('Terimakasih telah memilih layanan Self-Cashier! Silahkan membayar belanja anda.')
                    break
                
            except ValueError as err:
                typer_style(f'{err}', 'RED')


    def update_jumlah_item(self):
        '''Meng-update jumlah item dalam keranjang'''

        while True:
            try:
                self.check_keranjang()

                typer_style('Jumlah item apa yang ingin anda update?')
                nama_item = input('Atau ketik "X" kembali ke menu utama: ').strip().lower()

                if nama_item == 'x':
                    break

                jumlah_item_baru = int(input('Berapa jumlah item yang anda inginkan?: '))

                # Check item yang sama dan meng-update jumlah
                # Mengubah tuple ke list untuk memudahkan operasi
                self.keranjang_belanja_total = tuple_to_list(self.keranjang_belanja_total)
                item_sama = False

                for item in self.keranjang_belanja_total:
                    if nama_item in item:
                        item_sama = True
                        typer_style(f'Berhasil mengubah jumlah {nama_item} dari {item[3]} menjadi {jumlah_item_baru}.')
                        item[3] = jumlah_item_baru
                        item[4] = item[2] * item[3]
                        break
    
                if item_sama == False:  
                    typer_style(f'Maaf, {nama_item} tidak ada di daftar belanja anda. Silahkan memilih item yang tersedia.', 'RED')
            
                # Mengubah list kembali ke tuple untuk disimpan, memudahankan untuk menyimpan dalam database
                self.keranjang_belanja_total = list_to_tuple(self.keranjang_belanja_total)

            except ValueError as err:
                typer_style(f'{err}', 'RED')


    def delete_item(self):
        '''Meng-hapus item dari daftar belanja'''

        while True:
            try:
                self.check_keranjang()

                typer_style('Item apa yang ingin anda hapus?')
                nama_item = input('Atau ketik "X" untuk kembali ke menu utama: ').strip().lower()

                if nama_item == 'x':
                    typer_style('Process menghapus item dari daftar belanja dibatalkan.')
                    break

                # Mengubah tuple ke list untuk memudahkan operasi
                self.keranjang_belanja_total = tuple_to_list(self.keranjang_belanja_total)

                # Check item yang sama dan mengahapus item
                any_deleted_item = False
                for index, item in enumerate(self.keranjang_belanja_total):
                    if nama_item == item[1]:
                        any_deleted_item = True
                        self.keranjang_belanja_total.pop(index)
                        typer_style(f'Berhasil menghapus {nama_item} dari daftar belanja.')
                    
                if any_deleted_item:
                    for index, item in enumerate(self.keranjang_belanja_total):
                        item[0] = index + 1
                else:
                    typer_style(f'Maaf, {nama_item} tidak ada dalam daftar belanja anda. Silahkan masukkan item yang tersedia dari daftar belanja anda.', 'RED')


                # Mengubah list kembali ke tuple untuk disimpan, memudahankan untuk menyimpan dalam database
                self.keranjang_belanja_total = list_to_tuple(self.keranjang_belanja_total)

            except ValueError as err:
                typer_style(f'{err}', 'RED')


    def reset_transaction(self):
        '''Meng-reset daftar belanja'''

        while True:
            try:
                self.check_keranjang()

                yes_or_no = input(
                    'Apakah anda ingin menghapus semua item dari daftar belanja? Ketik "Y" untuk menghapus semua item and "N" untuk membatalkan: ').strip().lower()

                if yes_or_no == 'y':
                    self.keranjang_belanja_total = []
                    typer_style(
                        f'Berhasil menghapus semua item dari daftar belanja.')               
                elif yes_or_no == 'n':
                    typer_style(
                        f'Process menghapus item dari daftar belanja dibatalkan.', 'RED')
                    break
                else:
                    typer_style(
                        f'Maaf "{yes_or_no}" tidak valid. Ketik "Y" untuk menghapus semua item and "N" untuk membatalkan.', 'RED')
            except ValueError as err:
                typer_style(f'{err}', 'RED')
