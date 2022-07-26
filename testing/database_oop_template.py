from mysql.connector import connect, Error


class DataBase:

    connection = None
    cursor = None
    query_create = None

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.connection = connect(host=self.host, user=self.user, password=self.password, database=self.database)
            return self.use_cursor()
        except Error as error:
            print(error)


    def use_cursor(self):
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.query_create = '''
        CREATE TABLE test_data_base(
            id INT AUTO_INCREMENT PRIMARY KEY, 
            client_id VARCHAR(255)
        )
        '''
        try:
            self.cursor.execute(self.query_create)
            self.connection.commit()
        except Error as error:
            print(error)


db = DataBase('31.31.196.38', 'u1726449_alex', 'eY4vT5pM6m', 'u1726449_default')
db.connect()
db.create_table()




# def get_url_history(id):
#     try:
#         with connect(host='31.31.196.38', user='u1726449_alex', password='eY4vT5pM6m') as connection:
#             request_mysql = 'USE u1726449_default'
#             request_select = f"SELECT url_interface, id FROM behance_helper WHERE client_id={id}"
#             with connection.cursor() as cursor:
#                 cursor.execute(request_mysql)
#                 cursor.execute(request_select)
#                 result = cursor.fetchall()
#                 connection.commit()
#                 result_string = ' '.join(list(set([i[0] for i in result])))
#                 if len(result_string) == 0:
#                     return 'is empty.'
#                 return result_string
#     except Error as error:
#         print(error)
#
# print(get_url_history(1172947980))