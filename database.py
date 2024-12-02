from sql_connection import get_sql_connection
from datetime import datetime

connection = get_sql_connection()

def tounix(date):
    date_string = date
    date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M')
    unix_timestamp = int(date_obj.timestamp())
    return unix_timestamp

def insert_user(connection,user_id,role,password):
    query = "INSERT INTO users (user_id,role,password) VALUES ('{}','{}','{}');".format (user_id,role,password)
    print(query)
    cur = connection.cursor()
    cur.execute(query)
    connection.commit()

def insert_request(connection,exam_id,release_date,user_id):
    query = "INSERT INTO requests (exam_id,release_date,user_id) VALUES ('{}','{}','{}');".format (exam_id,release_date,user_id)
    print(query)
    cur = connection.cursor()
    cur.execute(query)
    connection.commit()
    
def fetch_request(connection,user_id):
    query = "SELECT exam_id FROM requests WHERE user_id = '{}';".format (user_id)
    print(query)
    cur = connection.cursor()
    cur.execute(query)
    response = []
    for user_id in cur:
        response.append(user_id[0])
    return response

def is_valid(connection,user_id,role,password):
    query = "SELECT user_id FROM users WHERE user_id = '{}' AND role = '{}' AND password = '{}';".format (user_id,role,password)
    cur = connection.cursor()
    cur.execute(query)
    response = cur.fetchone()
    if response == None:
        a = False
    else:
        a = True
    return a

def delete_request(connection,exam_id,user_id):
    query = "DELETE FROM requests WHERE exam_id = '{}' and user_id = '{}';".format (exam_id,user_id)
    cur = connection.cursor()
    cur.execute(query)
    connection.commit()
    print("deleted")
    
def get_time(connection,exam_id):
    query = "SELECT release_date FROM requests WHERE exam_id = '{}';".format (exam_id)
    cur = connection.cursor()
    cur.execute(query)
    response = cur.fetchone()
    return int(response[0])
    
a=get_time(connection,'22234')
print(a)
# a=fetch_request(connection,1)
# print(a)
# delete_request(connection,'12','t1')
# id= 2
# role = 'teacher'
# password = 123
# insert_user(connection,id,role,password)

# insert_request(connection,password,1)