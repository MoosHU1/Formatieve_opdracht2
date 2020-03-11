"""
Bron 1: https://pynative.com/python-postgresql-insert-update-delete-table-data-to-perform-crud-operations/#Python_PostgreSQL_INSERT_into_database_Table
LET OP
Het wachtwoord van je PostgreSQL moet je zelf invullen, anders werkt het niet
Zoek naar de plekken waar je een wachtwoord in moet vullen met ctrl+f password
"""

import pymongo
import psycopg2  # Module om met PostgreSQL te communiceren
import random


def get_connection():
    connection = psycopg2.connect(dbname='voordeelshop',
                                  user='postgres',
                                  password='',
                                  port=5432)
    return connection


def get_products_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["huwebshop"]
    colom_product = database["products"]
    products = colom_product.find({"gender": "Unisex"}).limit(20)

    for i in products:
        insert_into_postgres((i["_id"], i["gender"], i["name"], i["price"]["selling_price"]))


def insert_into_postgres(values):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO product VALUES(%s,%s,%s,%s)"""
        record_to_insert = values
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)


def get_random_item_postgres():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        postgres_select_query = """SELECT productname, price FROM product"""
        cursor.execute(postgres_select_query)
        product_price_records = cursor.fetchall()


    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    prod_price_dict = {}
    for item in product_price_records:
        prod_price_dict[item[0]] = item[1]

    random_name, random_price = random.choice(list(prod_price_dict.items()))
    diff_dict = {}

    for prod_name, price in prod_price_dict.items():
        diff = abs(random_price - price)
        diff_dict[prod_name] = diff

    max_diff = max(diff_dict.values())
    list_of_prods = []
    for k, v in diff_dict.items():
        if v == max_diff:
            list_of_prods.append(k)

    print('Producten met het grootste verschil: {}'.format(list_of_prods))


def opdracht_2():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        postgreSQL_select_Query = "select Price from Product"

        cursor.execute(postgreSQL_select_Query)
        price_records = cursor.fetchall()

        total = 0
        b = 0
        for row in price_records:
            total += row[0]
            b += 1
        print("Gemiddelde prijs is "+str(total/b))

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)


if __name__ == "__main__":
    a_ = input("Staat de data al in je postgresql?(J/N):")
    a_ = a_.lower()
    if 'n' in a_:
        get_products_mongo()

    opdracht_2()
    get_random_item_postgres()
