import pymongo
import psycopg2  # Module om met PostgreSQL te communiceren


def get_data_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["huwebshop"]

    colom_product = database["products"]
    colom_profile = database["profiles"]
    colom_session = database["sessions"]

    products = colom_product.find().limit(10)
    profiles = colom_profile.find().limit(1000)
    sessions = colom_session.find().limit(1000)

    for i in products:
        insert_products_into_postgres("product", (i["_id"], i["gender"], i["name"], i["price"]["selling_price"]))

    loop =0
    for i in profiles:
        loop+=1
        if loop%10 == 0:
            print(loop,"Profiles inserted into database")
        try:
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

        #   Table kan geen variabele zijn, daarom 3 if statements
        if table == "product":
            cursor.execute("""INSERT INTO product VALUES(%s,%s,%s,%s)""",values)

        if table == "profile":
            cursor.execute("""INSERT INTO profile VALUES(%s)""", values)

        if table == "session":
            cursor.execute("""INSERT INTO session_ VALUES(%s,%s)""", values)


        connection.commit()
        count = cursor.rowcount
        #print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into table", error)

get_data_mongo()