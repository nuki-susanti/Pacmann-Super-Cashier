DROP DATABASE IF EXISTS railway;
CREATE DATABASE railway;
USE railway;


CREATE TABLE customers(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    cust_id VARCHAR(8) NOT NULL UNIQUE
);

CREATE TABLE items(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    nama_item VARCHAR(255) NOT NULL UNIQUE,
    harga_per_item INTEGER NOT NULL
);

CREATE TABLE transactions(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    transaction_date DATE NOT NULL,
    transaction_id VARCHAR(8) NOT NULL,
    nama_item VARCHAR(255) NOT NULL UNIQUE,
    jumlah_item INTEGER NOT NULL,
    total_belanja INTEGER NOT NULL,
    cust_id VARCHAR(8) NOT NULL,
    FOREIGN KEY (nama_item) REFERENCES items(nama_item),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);