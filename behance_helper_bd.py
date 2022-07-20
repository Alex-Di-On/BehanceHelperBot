from mysql.connector import connect, Error

try:
    with connect(host='31.31.196.38', user='u1726449_alex', password='vY9aQ3gX3x', db='BehanceHelper') as connection:
        print(connection)
except Error as error:
    print(error)


