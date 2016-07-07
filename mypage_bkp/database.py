""" module for creating and operating the database """

import sqlite3

def login_table(table_name, name = None, age = None):
    """ creates the tables for different users """
    
    conn = sqlite3.connect("names.db")
    c = conn.cursor()
    try:
        c.execute("CREATE TABLE IF NOT EXISTS table_"+ table_name +"(NAME TEXT, AGE REAL)")
    except sqlite3.OperationalError:
        return "Fail"
    if((name is not None) & (age is not None)):
        c.execute("SELECT NAME,AGE FROM table_"+table_name)
        c.execute("INSERT INTO table_" + table_name + "(NAME, AGE) VALUES (?, ?)", (name, age))
        conn.commit()
    
    conn.close()

def register_table( name, password):
    """ creates the table with user credentials """
 
    conn = sqlite3.connect("names.db")
    c = conn.cursor()
    try:
        c.execute("CREATE TABLE IF NOT EXISTS table_register(name TEXT, password TEXT)")
    except sqlite3.OperationalError:
        pass

    c.execute("SELECT name, password FROM table_register")
    c.execute("INSERT INTO table_register(name, password) VALUES (?, ?)", (name, password))
    conn.commit()
    conn.close()

def read_db(table_name):
    """ prints the database """

    conn = sqlite3.connect("names.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM table_"+table_name)
        db = c.fetchall()
        conn.close()
        return db
    except sqlite3.OperationalError:
        return 0

