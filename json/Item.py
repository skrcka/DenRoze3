#import pyodbc
import os
from datetime import datetime
#from xml.etree import ElementTree
import json
from pprint import pprint as print

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


class Item:
    def __init__(self, id, name, code, price, dph, count, mincount, weight, is_age_restricted):
        self.id = id
        self.name = name
        self.code = code
        self.price = price
        self.dph = dph
        self.count = count
        self.mincount = mincount
        self.weight = weight
        self.is_age_restricted = is_age_restricted

class BillItem:
    def __init__(self, item, count):
        self.item = item
        self.count = count

class Order:
    def __init__(self, user):
        self.user = user
        self.items = []
        self.total = 0
        self.total_weight = 0
        self.date = datetime.now()
    def add_item(self, item, count):
        self.total += item.price * count
        self.total_weight += item.weight * count
        self.items.append(BillItem(item, count))
    def remove_item(self, id):
        self.total -= self.items[id].item.price * self.items[id].count
        self.total_weight -= self.items[id].item.weight * self.items[id].count
        del self.items[id]

class Bill:
    def __init__(self, id):
        self.id = id
        self.items = []
        self.total = 0
        self.date = datetime.now()
    def add_item(self, item, count):
        self.items.append(BillItem(item, count))
        self.total += item.price * count
    def remove_item(self, id):
        self.total -= self.items[id].item.price * self.items[id].count
        del self.items[id]
    def transform(self):
        bill_dict = {
            'id': self.id,
            'items': [],
            'total': self.total,
            'date': self.date,
        }
        for billitem in self.items:
            item_dict = {
                "id": billitem.item.id,
                "name": billitem.item.name,
                "code": billitem.item.code,
                "price": billitem.item.price,
                "dph": billitem.item.dph,
                "count": billitem.item.count,
                "mincount": billitem.item.mincount,
                "weight": billitem.item.weight,
                "is_age_restricted": billitem.item.is_age_restricted,
            }
            billitem_dict = {
                "item": item_dict,
                "count": billitem.count
            }
            bill_dict['items'].append(billitem_dict)
        return bill_dict

class Bills:
    def __init__(self):
        self.bills = []
    def new(self, id):
        bill = Bill(id)
        self.bills.append(bill)
        return bill
    def add(self, bill):
        self.bills.append(bill)
    def remove(self, id):
        del self.bills[id]
    def __setitem__(self, number, data):
        self.bills[number] = data
    def __getitem__(self, number):
        return self.bills[number]

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

class User:
    def __init__(self, id, name, password, is_employee, is_admin):
        self.id = id
        self.name = name
        self.password = password
        self.is_employee = is_employee
        self.is_admin = is_admin

class Users:
    def __init__(self):
        self.users = []
    def load(self,id,name,password, is_employee, is_admin):
        self.users.append(User(id, name, password, is_employee, is_admin))
    def add(self, user):
        self.users.append(user)
    def remove(self, id):
        del self.users[id]
    def __setitem__(self, number, data):
        self.users[number] = data
    def __getitem__(self, number):
        return self.users[number]

class Stock:
    def __init__(self):
        self.stock = []  
    def load(self,id,name,code,price, dph, count, mincount, weight, is_age_resctricted):
        self.stock.append(Item(id, name, code, price, dph, count, mincount, weight, is_age_resctricted))
    def add(self, item):
        self.stock.append(item)
    def remove(self, id):
        del self.stock[id]
    def __setitem__(self, number, data):
        self.stock[number] = data
    def __getitem__(self, number):
        return self.stock[number]
    def transform(self):
        return self.__dict__

# db = Database()
stock = Stock()

bills = Bills()
#print(bill.items[0].item.weight)
#bill.remove_item(0)
#stock.add(Item(0, "vejce", "vesnica", 10, 21, 100, 10, 50, False))
#stock.add(Item(1, "piko", "dubina", 200, 0, 69, 10, 1, False))
#print(bill.items[0].item.weight)
#print(bill.date)
# db.get_stock(stock)
#json = Json()
#json.load_stock(stock)
#print(stock[0].name)
#json.load(1,"skero", "dubina2", 200, 0, 100, 20, 1, False)
#json.write_stock(stock)
db = Local_db()
#db.write_stock(stock)
db.load_stock(stock)
#bills[0].add_item(stock[0],5)
#bills[0].add_item(stock[1],3)
#db.write_bills(bills)
#print(stock[1].name)
db.load_bills(bills)
print(bills[0].total)
