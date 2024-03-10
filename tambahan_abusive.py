import sqlite3

# Membuat koneksi ke database
conn = sqlite3.connect('simple_apiv3/data/abusive.db')

# Menambahkan kata "kntl" ke dalam tabel
word = "kntl"
conn.execute(f"INSERT INTO abusivewords (abusive) VALUES ('{word}')")

# Melakukan commit dan menutup koneksi
conn.commit()
conn.close()