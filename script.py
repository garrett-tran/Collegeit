from flask import *
from database import init_db, db_session
from models import *
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('collegeit.db')
cursor = conn.cursor()

#college = College(name = "UMICH", class_size = 8000, average_sat = 1430)
query = "DELETE FROM posts WHERE username = 'RHEA';"

cursor.execute(query)

conn.commit()
conn.close()
