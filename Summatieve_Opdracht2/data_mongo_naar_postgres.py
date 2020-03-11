"""
Bron 1: https://stackoverflow.com/questions/13793399/passing-table-name-as-a-parameter-in-psycopg2
Bron 2: https://www.postgresqltutorial.com/postgresql-python/insert/
"""

import pymongo
import psycopg2  # Module om met PostgreSQL te communiceren


def get_data_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["huwebshop"]

    colom_product = database["products"]
    colom_profile = database["profiles"]
    colom_session = database["sessions"]

    products = colom_product.find().limit(100)
    profiles = colom_profile.find().limit(100)
    sessions = colom_session.find().limit(100)

    categories = set()
    brands = set()

    for i in products:
        if i["category"] is not None and i["category"] not in categories:
            categories.add(i["category"])
            insert_products_into_postgres("category", (i["category"],))

        if i["brand"] is not None and i["brand"] not in brands:
            brands.add(i["brand"])
            insert_products_into_postgres("brand", (i["brand"],))

        insert_products_into_postgres("product", (i["_id"], i["category"], i["brand"], i["gender"], i["name"], i["price"]["selling_price"]))

    for i in profiles:
        try:  # Try except statement wegens profielen zonder browserid
            for j in range(len(i["buids"])):
                insert_products_into_postgres("profile", (i["buids"][j],))
        except:
            continue

    for i in sessions:
        insert_products_into_postgres("session", (i["_id"], i["buid"][0]))


def insert_products_into_postgres(table, values):
    try:
        connection = psycopg2.connect("dbname = voordeelshop user=postgres password=''")
        cursor = connection.cursor()

        #   Table kan geen variabele zijn, daarom 3 if statements. Zie bron 1.
        if table == "category":
            cursor.execute("""INSERT INTO category VALUES(%s)""",values)

        if table == "brand":
            cursor.execute("""INSERT INTO brand VALUES(%s)""",values)

        if table == "product":
            cursor.execute("""INSERT INTO product VALUES(%s,%s,%s,%s,%s,%s)""",values)

        if table == "profile":
            cursor.execute("""INSERT INTO profile VALUES(%s)""", values)

        if table == "session":
            cursor.execute("""INSERT INTO session_ VALUES(%s,%s)""", values)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)


get_data_mongo()
