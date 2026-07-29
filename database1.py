import sqlite3


# make the conncection
connection = sqlite3.connect("sqlite.db")

cursor=connection.cursor()

#=====================================================================
#==================== TABLE CREATION =================================
#=====================================================================


# # 1. Create a table
# cursor.execute("""
#                CREATE TABLE IF NOT EXISTS shipment(
#                    id INTEGER,
#                    content TEXT,
#                    weight REAL,
#                    status TEXT
#                    )""")

# # 2. Add shipment data
# cursor.execute("""
#     INSERT INTO shipment (id, content, weight, status)
#     VALUES
#         (234234, 'Palm Trees', 8.4, 'placed'),
#         (234234, 'mango Trees', 8.5, 'in_transit'),
#         (234235, 'Mangoes', 12.5, 'in_transit'),
#         (234236, 'Laptops', 3.2, 'delivered'),
#         (234237, 'Mobile Phones', 1.8, 'placed'),
#         (234238, 'Books', 15.6, 'cancelled'),
#         (234239, 'Furniture', 45.0, 'in_transit'),
#         (234240, 'Clothes', 6.3, 'delivered'),
#         (234241, 'Medicines', 2.1, 'placed'),
#         (234242, 'Electronics', 9.8, 'in_transit'),
#         (234243, 'Shoes', 4.7, 'delivered')
# """)

# # Read shipment data by id
# cursor.execute("""
#     SELECT * FROM shipment
               
# """)

# # to fetch selected data 
# result=cursor.fetchall()
# print(result)

# # to fetch some  rows only
# result=cursor.fetchmany(3)
# print(result)


# # to fetch one rows only
# result=cursor.fetchone()
# print(result)

# # to read data with filter
# cursor.execute("""
#     SELECT * 
#     FROM shipment
#     WHERE id=234237
# """)

# # to fetch the rows
# result=cursor.fetchall()
# print(result)


# Delete all shipment 

# cursor.execute("""
#     DELETE FROM shipment

# """)

# # Drop the table
# cursor.execute("""
#     DROP TABLE shipment
# """)


#=====================================================================
#======================== PRIMARY KEY ================================
#=====================================================================

# without primary key same data is duplicated at multiple place

# # 1. Create a table
# cursor.execute("""
#                CREATE TABLE IF NOT EXISTS shipment(
#                    id INTEGER PRIMARY KEY,
#                    content TEXT,
#                    weight REAL,
#                    status TEXT
#                    )""")


# 2. Add shipment data with duplicate data like id=234234
# cursor.execute("""
#     INSERT INTO shipment (id, content, weight, status)
#     VALUES
#         (234234, 'Palm Trees', 8.4, 'placed'),
#         (234234, 'mango Trees', 8.5, 'in_transit'),
#         (234235, 'Mangoes', 12.5, 'in_transit'),
#         (234236, 'Laptops', 3.2, 'delivered')
# """)

# error = sqlite3.IntegrityError: UNIQUE constraint failed: shipment.id

# # 2. Add shipment data with duplicate data like id=234234
# cursor.execute("""
#     INSERT INTO shipment (id, content, weight, status)
#     VALUES
#         (234234, 'Palm Trees', 8.4, 'placed'),
#         (234235, 'mango Trees', 8.5, 'in_transit'),
#         (234236, 'Mangoes', 12.5, 'in_transit'),
#         (234237, 'Laptops', 3.2, 'delivered')
# """)


# # Read shipment data by id
# cursor.execute("""
#     SELECT * FROM shipment
               
# """)

# # to fetch selected data 
# result=cursor.fetchall()
# print(result)


#=====================================================================
#==================== TO UPDATE ROW ==================================
#=====================================================================

# cursor.execute("""
#     UPDATE shipment 
#     SET status='order_completed'
#     WHERE id=234234   
# """)


#=====================================================================
#==============SQL QUERY PARAMETERS ==================================
#=====================================================================

# # update values 
# id=234234
# status='in_transit'

# cursor.execute("""
#     UPDATE shipment SET status=?
#     WHERE id=?
# """,(status,id))

# Another methdo

# id=234235
# status="delivery_completed"

# cursor.execute("""
#     UPDATE shipment SET status=:status
#     WHERE id=:id
# """,
#     {"status":status,"id":id}
# )














# to push the changes 
connection.commit()


# close the connection
connection.close()