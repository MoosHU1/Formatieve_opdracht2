import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_tables():
    commands = (
        '''
        CREATE TABLE brand
        (Brand varchar,
            PRIMARY KEY(Brand)
        )
        ''',
        '''
        CREATE TABLE category
        (
            Category varchar,
            PRIMARY KEY(Category)
        )
        ''',
        '''
        CREATE TABLE Product
        (
          ProductID varchar,
          Category varchar,
          Brand varchar,
          GenderID  varchar,
          ProductName  varchar,
          Price numeric,
          PRIMARY KEY (ProductID),
          FOREIGN KEY (Category) REFERENCES category(Category),
          FOREIGN KEY (Brand) REFERENCES brand(Brand)
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
            
            
if __name__ == "__main__":   
    # Connect to PostgreSQL DBMS
    con = psycopg2.connect("dbname = voordeelshop user=postgres password=''")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Obtain a DB Cursor
    cursor = con.cursor()
    create_tables()
