from cassandra.cluster import Cluster
from datetime import datetime
# f = open("processed_files/sample/query.txt", "r")
# lines = f.readlines()
# f.close()
# i = 0
# while i < len(lines):
#     line = lines[i].strip()
#     args = line.split(",")
#     command = args[0]
#     if command == 'N':
#         print(line)
#         print(lines[i+1: i+int(args[-1])+1])
#         # print(i+1, i+int(args[-1]))
#         i += int(args[-1]) + 1
#         continue
#     elif command == 'I':
#         i += 1
#         print(line)
#     elif command == 'D':
#         i += 1
#         print(line)
#     else:
#         print('else')
#         i += 1

cluster = Cluster(['192.168.51.10'], 9043)
session = cluster.connect()

# Create the keyspace.
# session.execute('CREATE KEYSPACE IF NOT EXISTS dateval;')
# print("Created keyspace ybdemo")
#
# # Create the keyspace.
# session.execute('CREATE KEYSPACE IF NOT EXISTS ybdemo;')
# print("Created keyspace ybdemo")

# Create the table.
session.execute(
  """
  CREATE TABLE IF NOT EXISTS ybdemo.employee1 (OL_W_ID int,
                                              OL_D_ID int,
                                              OL_O_ID int,
                                              OL_NUMBER int,
                                              OL_I_ID int,
                                              OL_DELIVERY_D timestamp,
                                              OL_AMOUNT decimal,
                                              OL_SUPPLY_W_ID int,
                                              OL_QUANTITY decimal,
                                              OL_DIST_INFO text,
                                              PRIMARY KEY ((OL_W_ID, OL_D_ID), OL_O_ID, OL_NUMBER));
  """)
print("Created table employee1")
name = "'S_DIST_1'"
print(name)
s = """INSERT INTO ybdemo.employee1 (ol_w_id,ol_d_id,ol_o_id,ol_number,ol_i_id,ol_delivery_d,ol_amount,
ol_supply_w_id,ol_quantity,ol_dist_info) VALUES ({}, {}, {},{},{},{},{},{},{},{});
  """.format(1,1,3019,0,1,'null',295.8,1,4,name)
print(s)
# Insert a row.
session.execute(s)
print("Inserted")

# Query the row.
row = session.execute('SELECT * FROM ybdemo.employee1 WHERE OL_O_ID = 3019;').one()
print(row)

# Close the connection.
cluster.shutdown()