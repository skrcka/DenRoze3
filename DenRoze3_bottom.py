import json
import os
from datetime import datetime
#import pyodbc
#from xml.etree import ElementTree

class Local_db:
    def __init__(self):
        self.path_to_stock = os.path.abspath(os.path.join('data', 'stock.json'))
        self.path_to_bills = os.path.abspath(os.path.join('data', "bills-{}.json".format(datetime.today().date())))
        self.path_to_changes = os.path.abspath(os.path.join('data', 'changes.json'))
        self.path_to_users = os.path.abspath(os.path.join('data', 'users.json'))
    def load_stock(self, stock):
        with open(self.path_to_stock, "r") as file:
            data = json.load(file)
        for item in data:
            stock.load(item["id"], item["name"], item["code"], item["price"], item["dph"], item["count"], item["mincount"], item["weight"], item["is_age_restricted"])
    def load_users(self, users):
        with open(self.path_to_users, "r") as file:
            data = json.load(file)
        for user in data:
            users.load(user["id"], user["name"], user["password"], user["is_employee"], user["is_admin"])
    def load_bills(self, bills):
        with open(self.path_to_bills, "r") as file:
            data = json.load(file)
        for bill in data:
            b = Bill(bill["id"])
            b.date = datetime.strptime(bill["date"], "%Y-%m-%d %H:%M:%S.%f")
            for billitem in bill["items"]:
                b.add_item(Item(billitem["item"]["id"], billitem["item"]["name"], billitem["item"]["code"],billitem["item"]["price"], billitem["item"]["dph"], billitem["item"]["count"], billitem["item"]["mincount"], billitem["item"]["weight"], billitem["item"]["is_age_restricted"]), billitem["count"])
            b.total = bill["total"]
            b.payment_method = bill["payment_method"]
            bills.add(b)
    def write_bills(self, bills):
        with open(self.path_to_bills, "w+") as file:
            bill_list = []
            for bill in bills:
                bill_list.append(bill.transform())
            json.dump(bill_list,file, indent=2, default=str)
    def write_stock(self, stock) : 
        with open(self.path_to_stock, "w+") as file:
            items = []
            for item in stock:
                items.append(item.__dict__)
            json.dump(items,file, indent=2)

#class Database:
#    def __init__(self):
#        server = 'dbsys.cs.vsb.cz\STUDENT' 
#        database = 'krc0071' 
#        username = 'krc0071' 
#        password = 'ZBH4QBnO33' 
#        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
#    def get_stock(stock):
#        cursor.execute('select * stock')
#        for row in cursor.fetchall():
#            id,name,code,price,count = row
#            stock.load(id,name,code,price,count)