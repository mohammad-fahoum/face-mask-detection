import psycopg2
class ManageDB:
    def add_table(self, tname, **columns):
        """CREATE NEW TABLE : THE PARAMETERS(tname, **columns) TAKE A STRING TYPE AND DICTIONARY"""
        columns = ", ".join([f"{name} {ctype}" for name, ctype in columns.items()])
        self.cursor.execute(f"CREATE TABLE {tname}({columns});")

    def join_tables(self, columns = "*", condition = "", **tbnames):
        """JOIN TABLES BASED ON SPECIFIED KEYS : THE PARAMETERS(columns = "*", condition = "", **tbnames) TAKE A STRING TYPE AND DICTIONARY"""
        tables = list(tbnames.keys())
        join_statement = " ".join([f"JOIN {tables[i+1]} ON {tables[i]}.{tbnames[tables[i]]} = {tables[i+1]}.{tbnames[tables[i+1]]}" for i in range(len(tables[1:]))])
        self.cursor.execute(f"SELECT {columns} FROM {tables[0]} {join_statement} {condition};")
        return self.cursor.fetchall()

    def update_table(self, tbname, condition = None, **items):
        """UPDATE SINGLE OR MULTIPLE RECORD BASED ON SPECIFIED CONDITION STATEMENT : THE PARAMETERS(tbname, condition = None, **items) TAKE A STRING TYPE AND DICTIONARY"""        
        column_values = ",".join([f"{key} = {value}" for key, value in items.items()])
        self.cursor.execute(f"UPDATE {tbname} SET {column_values} WHERE {condition};")

    def update_full_table(self, tbname, **items):
        """UPDATE THE WHOLE COLUMNS IN THE TABLE: THE PARAMETERS(tbname, **items) TAKE A STRING TYPE AND DICTIONARY"""        
        column_values = ",".join([f"{key} = {value}" for key, value in items.items()])
        self.cursor.execute(f"UPDATE {tbname} SET {column_values};")

    def remove_table(self, tname):
        """DROP THE TABLE FROM THE DATABASE: THE PARAMETERS(tbname) TAKE A STRING TYPE"""        
        try:
            self.cursor.execute(f"DROP TABLE {tname};")
        except:
            self.cursor.execute(f"DROP TABLE {tname} CASCADE;")

    def clear_table(self, tname):
        """EMPTY THE TABLE: THE PARAMETERS(tbname) TAKE A STRING TYPE"""
        self.cursor.execute(f"DELETE FROM {tname};")

    def call_table(self, tbname):
        """CALL THE TABLE: THE PARAMETERS(tbname) TAKE A STRING TYPE"""        
        self.cursor.execute(f"SELECT * FROM {tbname};")
        return self.cursor.fetchall()

    def add_column(self, tbname, **column):
        """ADD OR REPLACE A COLUMN IN THE TABLE: THE PARAMETERS(tbname, **column) TAKE A STRING TYPE AND DICTIONARY ({COLNAME:VALUE} OR COLNAME = 'VALUE')"""
        columns = " ".join(column.items()[0][0], column.items()[0][1])
        self.cursor.execute(f"ALTER TABLE {tbname} ADD {columns};")

    def remove_column(self, tbname, colname):
        """DROP A COLUMN FROM THE TABLE: THE PARAMETERS(tbname) TAKE A STRING TYPE"""
        self.cursor.execute(f"ALTER TABLE {tbname} DROP COLUMN {colname};")

    def add_record(self, tbname, **kwargs):
        """ADD A NEW RECORDS TO THE TABLE: THE PARAMETERS(tbname, **kwargs) TAKE A STRING TYPE AND DICTIONARY (COLNAME:VALUE OR COLNAME = 'VALUE')"""
        columns = ", ".join(tuple(kwargs.keys()))
        values = ", ".join(tuple(kwargs.values()))
        self.cursor.execute(f"INSERT INTO {tbname}({columns}) VALUES({values});")

    def remove_record(self, tbname, condition):
        """DELETE A RECORDS FROM THE TABLE BASAED ON SPECIFIED CONDITION STATEMENT: THE PARAMETERS(tbname, condition) TAKE A STRING TYPE"""
        self.cursor.execute(f"DELETE FROM {tbname} WHERE {condition};")
        # try:
        #     self.cursor.execute(f"DELETE FROM {tbname} WHERE {condition};")
        # except:
        #     self.cursor.execute(f"DELETE CASCADE FROM {tbname} WHERE {condition};")

    def call_record(self, tbname, columns = "*",condition = ''):
        """RETRIEVE DATA FROM THE TABLE BASAED ON SPECIFIED CONDITION STATEMENT: THE PARAMETERS(tbname, columns = "*",condition = '') TAKE A STRING TYPE"""
        self.cursor.execute(f"SELECT {columns} FROM {tbname} {condition};")
        return self.cursor.fetchall()


class SimpleDB(ManageDB):
    def __init__(self, dbname):
        """CREATE A NEW CONNETION TO THE SQLITE3 DATABASE SYSTEM"""
        self.database = dbname.lower()
        import sqlite3 
        self.conn = sqlite3.connect(self.database, check_same_thread = False)
        self.cursor = self.conn.cursor()
        self.conn.commit()

class Pgadmin(ManageDB):
    def __init__(self, database = 'postgres', user = 'postgres', password = 'postgres', host = '127.0.0.1', port = '5432'):
        """CREATE A NEW CONNETION TO THE POSTGRES DATABASE SYSTEM"""
        self.database = database.lower()
        self.user = user
        self.password = password
        self.host = host
        self.port = port 

        self.conn = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port)
        self.cursor = self.conn.cursor()

        if self.database in self.list_databases():
            self.conn = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = self.database)
            self.cursor = self.conn.cursor()
        else:
            self.conn.set_isolation_level(0)
            self.conn.cursor().execute(f'CREATE DATABASE {database};')
            self.conn = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = self.database)
            self.cursor = self.conn.cursor()

        self.conn.autocommit = True
        self.conn.commit()

    def connect_to_database(self, dbname):
       """CREATE A NEW CONNETION TO THE POSTGRES DATABASE SYSTEM"""
       self.conn = psycopg2.connect(user = self, password = self.password, host = self.host, port = self.port, database = dbname.lower())

    def close_database(self):
        """CLOSE THE CONNETION TO THE POSTGRES DATABASE SYSTEM"""
        self.conn.close()

    def create_database(self, dbname):
        """CREATE A NEW DATABASE IN THE POSTGRES SERVER"""
        self.cursor.execute(f"CREATE DATABASE {dbname};")

    def drop_database(self, dbname):
        """DROP A DATABASE FROM THE POSTGRES SERVER"""
        self.cursor.execute(f"DROP DATABASE {dbname};")
    
    def list_databases(self):
        """LIST THE DATABASES NAMES THAT EXIST IN THE POSTGRES SERVER"""
        self.cursor.execute("SELECT datname FROM pg_database;")
        return [dbname[0] for dbname in self.cursor.fetchall()]


