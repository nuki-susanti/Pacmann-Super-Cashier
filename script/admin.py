from db import initial_db, populate_db, query_items, query_item_kerabat, update_nama_item, update_harga_item
from table import pretty_table, typer_style

class Adminonly:
    def query_item_kerabat_helper(self, nama_item):
        fetched = query_item_kerabat(nama_item)

        no = 0
        data = []
        for item in fetched: 
            no += 1                  
            data.append((no, ) + item)

        return pretty_table(data=data, headers='y')


    def reset_db(self):     
        '''Me-reset database and populate with initial data'''

        user_answer = input('Anda yakin untuk menghapus semua menghapus data di database? (y/n): ').strip().lower()

        if user_answer == 'y':
            initial_db()
            typer_style('Database reset successful.')
            populate_db()
        else:
            typer_style('Database reset aborted.', 'RED')


    def update_item_name(self):
        '''Meng-update nama item yang ada di database - hanya untuk admin'''

        while True:
            try:
                typer_style('Item apa yang ingin anda update?')
                nama_item = input('Atau ketik "X" kembali ke menu utama: ').strip().lower()

                if nama_item == 'x':
                    break

                items_fetched = query_items(nama_item)

                if items_fetched:
                    nama_item_baru = str(input('Masukkan nama item yang baru: ').strip()).lower()
                    
                    # Memasukkan nama yang telah di-update ke dalam database
                    update_nama_item(nama_item_baru, items_fetched[0][0])

                    typer_style(f'Berhasil mengupdate {nama_item} menjadi {nama_item_baru}.')
                    
                    fetched = query_items(nama_item_baru)
                    data = [(1, ) + fetched[0]]
                    pretty_table(data=data, headers='y')
 
                else:
                    typer_style(f'Maaf, "{nama_item}" tidak ada di database. Silahkan memilih item yang tersedia.', 'RED')
                    self.query_item_kerabat_helper(nama_item)

            except ValueError as err:
                    typer_style(f'{err}', 'RED')

    
    def update_price_name(self):
        '''Meng-update harga item yang ada di database - hanya untuk admin'''

        while True:
            try:
                typer_style('Harga item apa yang ingin anda update?')
                nama_item = input('Atau ketik "X" kembali ke menu utama: ').strip().lower()

                if nama_item == 'x':
                    break

                items_fetched = query_items(nama_item)

                if items_fetched:
                    harga_item_baru = int(input('Masukkan harga item yang baru: ').strip())

                    # Memasukkan harga yang telah di-update ke dalam database
                    update_harga_item(harga_item_baru, items_fetched[0][0])

                    typer_style(f'Berhasil mengupdate harga {nama_item} menjadi {harga_item_baru}.')
                    data = [(1, ) + (items_fetched[0][0], ) + (harga_item_baru, )]
                    pretty_table(data=data, headers='y')
                else:
                    typer_style(f'Maaf, "{nama_item}" tidak ada di database. Silahkan memilih item yang tersedia.', 'RED')
                    self.query_item_kerabat_helper(nama_item)

            except ValueError as err:
                    typer_style(f'{err}', 'RED')
    
