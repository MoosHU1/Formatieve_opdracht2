import pymongo
import psycopg2  # Module om met PostgreSQL te communiceren


def get_data_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["huwebshop"]

    colom_product = database["products"]
    colom_profile = database["profiles"]
    colom_session = database["sessions"]

    products = colom_product.find().limit(1)
    profiles = colom_profile.find().limit(1)
    sessions = colom_session.find().limit(1)

    for i in products:
        insert_products_into_postgres("product", (i["_id"], i["gender"], i["name"], i["price"]["selling_price"]))

    for i in profiles:
        insert_products_into_postgres("product", i[""])

    for i in profiles:
        insert_products_into_postgres("session", i[""])

def insert_products_into_postgres(table, values):
    try:
        connection = psycopg2.connect("dbname = voordeelshop user=postgres password=''")
        cursor = connection.cursor()

        if table == "product":
            cursor.execute("""INSERT INTO product VALUES(%s,%s,%s,%s)""",values)

        if table == "profile":
            cursor.execute("""INSERT INTO profile VALUES(%s)""", values)

        if table == "session":
            cursor.execute("""INSERT INTO profile VALUES(%s,&s)""", values)


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into table", error)

get_data_mongo()