from transaksi import Cashier
from admin import Adminonly
from table import typer_style

sistem_on = True
tr = Cashier()
admin_only = Adminonly()


while sistem_on:

    user_command = input(
        '''Pilih menu transaksi:
    1. Untuk login/mendaftar sebagai customer baru
    2. Untuk melihat semua item yang kami jual
    3. Untuk menambah item ke dalam keranjang belanja
    4. Untuk mengupdate jumlah item dalam keranjang belanja
    5. Untuk menghapus item dari keranjang belanja
    6. Untuk mereset keranjang belanja
    7. Untuk menampilkan pesanan dalam keranjang belanja dan membayar belanja anda
    8. Untuk keluar dari aplikasi
    00. Untuk me-reset database (admin only - should be hidden/added "admin" verification)
    01. Untuk mengupdate nama item (admin only - should be hidden/added "admin" verification)
    02. Untuk mengupdate harga item (admin only - should be hidden/added "admin" verification)
    Ketik 1-7: '''
    ).strip()

    try:
        if user_command == '1':
            tr.add_customer()
        elif user_command == '2':
            tr.display_all_items()
        elif user_command == '3':
            tr.add_item()
        elif user_command == '4':
            tr.update_jumlah_item()
        elif user_command == '5':
            tr.delete_item()
        elif user_command == '6':
            tr.reset_transaction()
        elif user_command == '7':
            tr.check_order()
        elif user_command == '8':
            sistem_on = False
        elif user_command == '00':
            admin_only.reset_db()
        elif user_command == '01':
            admin_only.update_item_name()
        elif user_command == '02':
            admin_only.update_price_name()
        else:
            typer_style(
                f'Maaf menu "{user_command}" tidak valid. Pilih menu 1-8.')
    except ValueError as err:
        typer_style(f'{err}', RED)
