from datetime import datetime
from DenRoze3_base_classes import Item, BillItem, Order, Bill, User, IDcreator
from DenRoze3_bottom import Local_db, Sqlite_db
from pprint import pprint as pprint
from DenRoze3_top_cli import json_mode

class DB_Reader_Writer:
    def __init__(self):
        self.sqlite_db = Sqlite_db()
    def load_all(self, stock, bills, orders, users):
        pass
    def write_all_and_clear(self, stock, bills, orders, users):
        self.write_stock(stock)
        self.write_bills(bills)
        self.write_users(users)
        self.write_orders(orders)
    def write_user(self, user):
        self.sqlite_db.create_connection()
        if(user.id == 0):
            user.id = self.sqlite_db.insert_user(user)
        self.sqlite_db.close_connection()
    def write_users(self, users):
        for user in users:
            self.write_user(user)
    def write_stock(self, stock):
        for item in stock:
            self.write_item(item)
    def write_item(self, item):
        self.sqlite_db.create_connection()
        if(item.id == 0):
            item.id = self.sqlite_db.insert_item(item)
        self.sqlite_db.close_connection()
    def write_order_item(self, billitem, id):
        self.sqlite_db.create_connection()
        if(billitem.id == 0):
            billitem.id = self.sqlite_db.insert_orderitem(billitem, id)
        self.sqlite_db.close_connection()
    def write_order(self, order):
        self.sqlite_db.create_connection()
        if(order.id == 0):
            if(order.user.id == None):
                order.id = self.sqlite_db.insert_order(order, 0)
            else:
                order.id = self.sqlite_db.insert_order(order, order.user.id)
        self.sqlite_db.close_connection()
        for billitem in order.items:
            self.write_order_item(billitem, order.id)
    def write_orders(self, orders):
        for order in orders:
            self.write_order(order)
    def write_bill_item(self, billitem, id):
        self.sqlite_db.create_connection()
        if(billitem.id == 0):
            billitem.id = self.sqlite_db.insert_billitem(billitem, id)
        self.sqlite_db.close_connection()
    def write_bill(self, bill):
        self.sqlite_db.create_connection()
        if(bill.id == 0):
            bill.id = self.sqlite_db.insert_bill(bill)
        self.sqlite_db.close_connection()
        for billitem in bill.items:
            self.write_bill_item(billitem, bill.id)
    def write_bills(self, bills):
        for bill in bills:
            self.write_bill(bill)
    def create_empty_database(self):
        self.sqlite_db.create_connection()
        self.sqlite_db.close_connection()
    def create_database(self):
        self.sqlite_db.create_connection()
        User_script = """CREATE TABLE IF NOT EXISTS Users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    real_name text NOT NULL,
                                    password text NOT NULL,
                                    phone text NOT NULL,
                                    email text NOT NULL,
                                    is_employee integer,
                                    is_manager integer
                                );"""
        self.sqlite_db.create_table(User_script)
        Stock_script = """CREATE TABLE IF NOT EXISTS Stock (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    code text NOT NULL,
                                    price real NOT NULL,
                                    dph integer,
                                    count integer,
                                    mincount integer,
                                    weight,
                                    is_age_restricted integer
                                );"""
        self.sqlite_db.create_table(Stock_script)
        Bill_script = """CREATE TABLE IF NOT EXISTS Bills (
                                    id integer PRIMARY KEY,
                                    total real,
                                    date text NOT NULL,
                                    payment_method text NOT NULL,
                                    eet text NOT NULL,
                                    is_sale integer
                                );"""
        self.sqlite_db.create_table(Bill_script)
        Order_script = """CREATE TABLE IF NOT EXISTS Orders (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
                                    total real,
                                    total_weight real,
                                    date text NOT NULL,
                                    payment_method text,
                                    shipping_method text,
                                    address text,
                                    status text,
                                    FOREIGN KEY (user_id) REFERENCES Users (id)
                                );"""
        self.sqlite_db.create_table(Order_script)
        BillItem_script = """CREATE TABLE IF NOT EXISTS BillItems (
                                    id integer PRIMARY KEY,
                                    count integer NOT NULL,
                                    item_id integer NOT NULL,
                                    bill_id integer NOT NULL,
                                    FOREIGN KEY (item_id) REFERENCES Stock (id)
                                    FOREIGN KEY (bill_id) REFERENCES Bills (id)
                                );"""
        self.sqlite_db.create_table(BillItem_script)
        OrderItem_script = """CREATE TABLE IF NOT EXISTS OrderItems (
                                    id integer PRIMARY KEY,
                                    count integer NOT NULL,
                                    item_id integer NOT NULL,
                                    order_id integer NOT NULL,
                                    FOREIGN KEY (item_id) REFERENCES Stock (id)
                                    FOREIGN KEY (order_id) REFERENCES Orders (id)
                                );"""
        self.sqlite_db.create_table(OrderItem_script)
        self.sqlite_db.close_connection()


class Reader_Writer:
    def __init__(self):
        self.local_db = Local_db()
    def load_orders(self, orders):
        self.local_db.load_orders(orders)
    def write_orders(self, orders):
        self.local_db.write_orders(orders)
    def load_users(self, users):
        self.local_db.load_users(users)
    def write_users(self, users):
        self.local_db.write_users(users)
    def load_bills(self, bills):
        self.local_db.load_bills(bills)
    def write_bills(self, bills):
        self.local_db.write_bills(bills)
    def load_stock(self, stock):
        self.local_db.load_stock(stock)
    def write_stock(self, stock):
        self.local_db.write_stock(stock)
    def write_all_and_clear(self, stock, bills, orders, users):
        self.local_db.write_bills(bills)
        self.local_db.write_stock(stock)
        self.local_db.write_orders(orders)
        self.local_db.write_users(users)
        stock.clear()
        bills.clear()
        orders.clear()
        users.clear()
    def load_all(self, stock, bills, orders, users):
        self.local_db.load_stock(stock)
        self.local_db.load_bills(bills)
        self.local_db.load_orders(orders)
        self.local_db.load_users(users)
        for bill in bills:
            for item in bill.items:
                item.item = stock.find_item(item.item.id)
            bill.count_totals()
        for order in orders:
            for item in order.items:
                item = stock.find_item(item.id)
            order.count_totals()
    def timeshift(self, newdate, stock, bills, orders, users):
        self.write_all_and_clear(stock, bills, orders, users)
        self.local_db.timeshift(newdate)
        self.load_all(stock, bills, orders, users)

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
    def delete(self, search_term):
        o = self.find_order(search_term)
        if(o == None):
            return
        del o
    def find_order(self, search_term):
        for o in self.orders:
            if(o.id == search_term):
                return o
        print("Order not found")
        return None
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
    def delete(self, search_term):
        b = self.find_bill(search_term)
        if(b == None):
            return
        del b
    def find_bill(self, search_term):
        for b in self.bills:
            if(b.id == search_term):
                return b
        print("Bill not found")
        return None
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
    def new(self, name, real_name, password, phone, email, is_employee, is_manager):
        self.users.append(User(self.idcreator.getid(), name, real_name, password, phone, email, is_employee, is_manager))
    def load(self, id, name, real_name, password, phone, email, is_employee, is_manager):
        self.users.append(User(int(id), name, real_name, password, phone, email, bool(is_employee), bool(is_manager)))
    def add(self, user):
        self.users.append(user)
    def auth(self, username, password):
        for user in self.users:
            if(username == user.name):
                if(password == user.password):
                    return user
        return None
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
        self.stock.append(Item(int(id), name, code, float(price), int(dph), int(count), int(mincount), float(weight), bool(is_age_restricted)))
    def add(self, item):
        self.stock.append(item)
    def new(self, name, code, price, dph, count, mincount, weight, is_age_restricted):
        self.stock.append(Item(self.idcreator.getid(), name, code, price, dph, count, mincount, weight, is_age_restricted))
    def delete(self, search_term):
        i = self.find_item(search_term)
        if(i == None):
            return
        del i
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