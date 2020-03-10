import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DBMS
con = psycopg2.connect("dbname = voordeelshop user=postgres password=''")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB Cursor
cursor = con.cursor()


def delete_records():
    commands = (
        """DELETE FROM product""",
        """DELETE FROM category""",
        """DELETE FROM brand""",
        """DELETE FROM session_""",
        """DELETE FROM profile"""
        )

    try:
        for command in commands:
            cursor.execute(command)

        cursor.close()
        con.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            print("All records deleted")
            con.close()


delete_records()