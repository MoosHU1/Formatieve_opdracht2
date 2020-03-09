import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DBMS
con = psycopg2.connect("dbname = voordeelshop user=postgres password=''")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB Cursor
cursor = con.cursor()

def create_tables():
    commands = (
        '''
        CREATE TABLE Product
        (
          ProductID varchar,
          GenderID  varchar,
          ProductName  varchar,
          Price numeric,
          PRIMARY KEY (ProductID)	
        )
        ''',
        '''
        CREATE TABLE Profile
        (
          BrowserID varchar,
          PRIMARY KEY (BrowserID)
        )
        ''',
        '''
        CREATE TABLE Session_
        (
          SessionID varchar,
          BrowserID varchar,
          PRIMARY KEY (SessionID),
          FOREIGN KEY (BrowserID) references Profile(BrowserID)
        )
        ''')

    try:
        for command in commands:
            cursor.execute(command)

        cursor.close()
        con.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
create_tables()