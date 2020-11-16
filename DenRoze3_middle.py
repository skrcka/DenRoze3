from datetime import datetime
from DenRoze3_base_classes import Item, BillItem, Order, Bill, User, IDcreator
from DenRoze3_bottom import Local_db
from pprint import pprint as pprint


class Reader_Writer:
    def __init__(self):
        self.local_db = Local_db()
    def load_orders_local(self, orders):
        self.local_db.load_orders(orders)
    def write_orders_local(self, orders):
        self.local_db.write_orders(orders)
    def load_users_local(self, users):
        self.local_db.load_users(users)
    def write_users_local(self, users):
        self.local_db.write_users(users)
    def load_bills_local(self, bills):
        self.local_db.load_bills(bills)
    def write_bills_local(self, bills):
        self.local_db.write_bills(bills)
    def load_stock_local(self, stock):
        self.local_db.load_stock(stock)
    def write_stock_local(self, stock):
        self.local_db.write_stock(stock)
    def write_local_and_clear(self, stock, bills, orders, users):
        self.local_db.write_bills(bills)
        self.local_db.write_stock(stock)
        self.local_db.write_orders(orders)
        self.local_db.write_users(users)
        stock.clear()
        bills.clear()
        orders.clear()
        users.clear()
    def load_all_local(self, stock, bills, orders, users):
        self.local_db.load_stock(stock)
        self.local_db.load_bills(bills)
        self.local_db.load_orders(orders)
        self.local_db.load_users(users)
    def timeshift(self, newdate, stock, bills, orders, users):
        self.write_local_and_clear(stock, bills, orders, users)
        self.local_db.timeshift(newdate)
        self.load_all_local(stock, bills, orders, users)

class Orders:
    def __init__(self):
        self.orders = []
        self.idcreator = IDcreator()
    def new(self):
        order = Order(self.idcreator.getid())
        self.orders.append(order)
        return order
    def add(self, order):
        self.orders.append(order)
    def remove(self, id):
        del self.orders[id]
    def __setitem__(self, number, data):
        self.orders[number] = data
    def __getitem__(self, number):
        return self.orders[number]
    def clear(self):
        self.orders.clear()
    def print(self):
        for o in self.orders:
            o.print()

class Bills:
    def __init__(self):
        self.bills = []
        self.idcreator = IDcreator()
    def new(self):
        bill = Bill(self.idcreator.getid())
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
    def print(self):
        for b in self.bills:
            b.print()

class Users:
    def __init__(self):
        self.users = []
        self.idcreator = IDcreator()
    def load(self, name, real_name, password, phone, email, is_employee, is_manager):
        self.users.append(User(self.idcreator.getid(), name, real_name, password, phone, email, is_employee, is_manager))
    def add(self, user):
        self.users.append(user)
    def remove(self, id):
        del self.users[id]
    def __setitem__(self, number, data):
        self.users[number] = data
    def __getitem__(self, number):
        return self.users[number]
    def clear(self):
        self.users.clear()

class Stock:
    def __init__(self):
        self.stock = []  
        self.idcreator = IDcreator()
    def load(self, id, name, code, price, dph, count, mincount, weight, is_age_restricted):
        self.stock.append(Item(id, name, code, price, dph, count, mincount, weight, is_age_restricted))
    def add(self, item):
        self.stock.append(item)
    def new(self, name, code, price, dph, count, mincount, weight, is_age_restricted):
        self.stock.append(Item(self.idcreator.getid(), name, code, price, dph, count, mincount, weight, is_age_restricted))
    def delete(self, search_term):
        id = self.find_item(search_term)
        del self.stock[id]
    def __setitem__(self, number, data):
        self.stock[number] = data
    def __getitem__(self, number):
        return self.stock[number]
    def transform(self):
        return self.__dict__
    def find_item(self, search_term):
        for i in self.stock:
            if(i.id == search_term or i.name == search_term or i.code == search_term):
                return i
        print("Item not found")
        return None
    def clear(self):
        self.stock.clear()
    def print_under_minimum(self):
        for i in self.stock:
            if(i.count <= i.mincount):
                print("[{}] {} {}".format(i.id, i.name, i.count))
    def print(self):
        print("[id]nazev, kod, cena(dph), pocet, minpocet, vaha, vekomez")
        for i in self.stock:
            i.print()