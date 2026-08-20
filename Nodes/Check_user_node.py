from Nodes.state import state_schema
from config.system_info import DB_PATH
from Database.db_connection import db_connection


cursor, conn = db_connection(DB_PATH)

def check_user(state : state_schema):

    row = cursor.execute("SELECT name FROM users WHERE cust_id=?",(state['user_id'],)).fetchone()
    name = row[0] if row else None
    li = cursor.execute("SELECT cust_id FROM users").fetchall()

    if row:

        if state['name'] == name:

            state['evaluator'] = 'correct'
        else:
            state['evaluator'] = 'in-correct'

    else:

        state['evaluator'] = 'in-correct'

    return state