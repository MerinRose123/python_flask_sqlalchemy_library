import sqlite3

conn = sqlite3.connect('book_database.db')  # formerly typo as 'book_database.db'
print("Opened database successfully")

# conn.execute('CREATE TABLE book1 (book_name TEXT )')
conn.execute('CREATE TABLE book (book_id INTEGER PRIMARY KEY,book_name TEXT NOT NULL,author TEXT NOT NULL,publisher '
             'text NOT NULL,page_no text NOT NULL);')
print("Table created successfully")
conn.close()