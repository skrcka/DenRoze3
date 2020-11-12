from datetime import datetime
from DenRoze3_base_classes import Item, BillItem, Order, Bill, User
from DenRoze3_bottom import Local_db


class Reader_Writer:
    def __init__(self):
        local_db = Local_db()
    def load_users_local(self, users):
        this.local_db.load_users(users)
    def load_bills_local(self, bills):
        this.local_db.load_bills(bills)
    def write_bills_local(self, bills):
        this.local_db.write_bills(bills)
    def load_stock_local(self, stock):
        this.local_db.load_stock(stock)
    def write_stock_local(self, stock):
        this.local_db.write_bills(bills)
    def write_local_and_clear(self, stock, bills):
        this.local_db.write_bills(bills)
        this.local_db.write_stock(stock)
        stock.clear()
        bills.clear()

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
    def clear(self):
        self.bills.clear()

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
    def find(self, item):
        for i in self.stock:
            if(i.id == item.id):
                return i
        return None
    def clear(self):
        self.stock.clear()