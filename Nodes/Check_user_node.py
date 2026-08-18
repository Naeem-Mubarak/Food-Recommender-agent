from Nodes.state import state_schema
from config.system_info import DB_PATH
from Database.db_connection import db_connection


cursor, conn = db_connection(DB_PATH)

def check_user(state : state_schema):

    name = cursor.execute("SELECT name FROM WHERE cust_id=?",(state['user_id'],))
    li = cursor.execute("SELECT cust_id FROM users")

    if (state['user_id'],) in li:

        if state['name'] == name:

            state['evaluator'] = 'correct'
    else:

        state['evaluator'] = 'in-correct'