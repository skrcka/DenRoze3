import json
import os
from datetime import datetime
from DenRoze3_base_classes import Item, BillItem, Order, Bill, User, IDcreator
#import pyodbc
#from xml.etree import ElementTree

class Local_db:
    def __init__(self):
        self.path_to_stock = os.path.abspath(os.path.join('data', 'stock.json'))
        self.path_to_bills = os.path.abspath(os.path.join('data', "bills-{}.json".format(datetime.today().date())))
        self.path_to_orders = os.path.abspath(os.path.join('data', "orders-{}.json".format(datetime.today().date())))
        self.path_to_changes = os.path.abspath(os.path.join('data', 'changes.json'))
        self.path_to_users = os.path.abspath(os.path.join('data', 'users.json'))

    def load_stock(self, stock):
        with open(self.path_to_stock, "r") as file:
            data = json.load(file)
        for item in data:
            stock.load(item["id"], item["name"], item["code"], item["price"], item["dph"], item["count"], item["mincount"], item["weight"], item["is_age_restricted"])
        stock.idcreator.setmaxid(stock)
    def write_stock(self, stock) : 
        with open(self.path_to_stock, "w+") as file:
            items = []
            for item in stock:
                items.append(item.__dict__)
            json.dump(items, file, indent=2)

    def load_users(self, users):
        with open(self.path_to_users, "r") as file:
            data = json.load(file)
        for user in data:
            users.load(user["id"], user["name"], user["password"], user["is_employee"], user["is_admin"])
    def write_users(self, users):
        with open(self.path_to_users, "w+") as file:
            usrs = []
            for user in users:
                usrs.append(user.__dict__)
            json.dump(usrs, file, indent=2)

    def load_orders(self, orders):
        with open(self.path_to_orders, "r") as file:
            data = json.load(file)
        for order in data:
            o = Order(order["id"])
            o.date = datetime.strptime(order["date"], "%Y-%m-%d %H:%M:%S.%f")
            o.user = order["user"]
            for billitem in order["items"]:
                o.add_item(Item(billitem["item"]["id"], billitem["item"]["name"], billitem["item"]["code"],billitem["item"]["price"], billitem["item"]["dph"], billitem["item"]["count"], billitem["item"]["mincount"], billitem["item"]["weight"], billitem["item"]["is_age_restricted"]), billitem["count"])
            o.total = order["total"]
            o.total_weight = order["total_weight"]
            o.payment_method = order["payment_method"]
            o.shipping_method = order["shipping_method"]
            o.address = order["address"]
            o.status = order["status"]
            orders.add(o)
        bills.idcreator.setmaxid(bills)
    def write_orders(self, orders):
        with open(self.path_to_orders, "w+") as file:
            order_list = []
            for order in orders:
                order_list.append(order.transform())
            json.dump(order_list, file, indent=2, default=str)

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
        bills.idcreator.setmaxid(bills)
    def write_bills(self, bills):
        with open(self.path_to_bills, "w+") as file:
            bill_list = []
            for bill in bills:
                bill_list.append(bill.transform())
            json.dump(bill_list,file, indent=2, default=str)

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