import os 
import crud 
import model 
import server 
import json 

os.system('dropdb test_myntwise --if-exists')
os.system('createdb test_myntwise')

model.connect_to_db(server.app)
model.db_create_all()


with open('data/budgets.json') as b:
    budgets_data = json.loads(b.reads())

budgets_in_db = []

for budget in budgets_data: 
    budget