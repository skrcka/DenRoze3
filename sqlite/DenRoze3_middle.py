from datetime import datetime
from DenRoze3_base_classes import Item, BillItem, Order, Bill, User, sqlite_mode, IDcreator
from DenRoze3_bottom import Sqlite_db, Local_db
from pprint import pprint as pprint

class Reader_Writer_json:
    def init():
        Reader_Writer_json.local_db = Local_db()
    def load_orders(orders):
        Reader_Writer_json.local_db.load_orders(orders)
    def write_orders(orders):
        Reader_Writer_json.local_db.write_orders(orders)
    def load_users(users):
        Reader_Writer_json.local_db.load_users(users)
    def write_users(users):
        Reader_Writer_json.local_db.write_users(users)
    def load_bills(bills):
        Reader_Writer_json.local_db.load_bills(bills)
    def write_bills(bills):
        Reader_Writer_json.local_db.write_bills(bills)
    def load_stock(stock):
        Reader_Writer_json.local_db.load_stock(stock)
    def write_stock(stock):
        Reader_Writer_json.local_db.write_stock(stock)
    def write_all_and_clear(stock, bills, orders, users):
        Reader_Writer_json.local_db.write_bills(bills)
        Reader_Writer_json.local_db.write_stock(stock)
        Reader_Writer_json.local_db.write_orders(orders)
        Reader_Writer_json.local_db.write_users(users)
        stock.clear()
        bills.clear()
        orders.clear()
        users.clear()
    def load_all(stock, bills, orders, users):
        Reader_Writer_json.local_db.load_users(users)
        Reader_Writer_json.local_db.load_stock(stock)
        Reader_Writer_json.local_db.load_bills(bills)
        Reader_Writer_json.local_db.load_orders(orders, users)
        for bill in bills:
            for item in bill.items:
                item.item = stock.find_item(item.item.id)
            bill.count_totals()
        for order in orders:
            for item in order.items:
                item = stock.find_item(item.id)
            order.count_totals()

class Reader_Writer:
    def init():
        Reader_Writer.sqlite_db = Sqlite_db()
        Reader_Writer.sqlite_db.create_connection()
    def close_connection():
        Reader_Writer.sqlite_db.close_connection()
    def load_all(stock, bills, orders, users):
        Reader_Writer.load_users(users)
        Reader_Writer.load_stock(stock)
        Reader_Writer.load_bills(bills,stock)
        Reader_Writer.load_orders(orders,stock,users)
    def write_all_and_clear(stock, bills, orders, users):
        Reader_Writer.write_users(users)
        Reader_Writer.write_stock(stock)
        Reader_Writer.write_bills(bills)
        Reader_Writer.write_orders(orders)
    def write_user(user):
        if(user.id == 0):
            user.id = Reader_Writer.sqlite_db.insert_user(user)
        else:
            Reader_Writer.sqlite_db.update_user(user)
    def write_users(users):
        for user in users:
            Reader_Writer.write_user(user)
    def write_stock(stock):
        for item in stock:
            Reader_Writer.write_item(item)
    def delete_user(user):
        Reader_Writer.sqlite_db.delete_user(user.id)
    def load_stock(stock):
        Reader_Writer.sqlite_db.load_stock(stock)
    def load_item(item, code):
        Reader_Writer.sqlite_db.load_item(item, code)
    def write_item(item):
        if(item.id == 0):
            item.id = Reader_Writer.sqlite_db.insert_item(item)
        else:
            Reader_Writer.sqlite_db.update_item(item)
    def delete_item(item):
        Reader_Writer.sqlite_db.delete_item(item.id)
    def write_orderitem(billitem, id):
        if(billitem.id == 0):
            billitem.id = Reader_Writer.sqlite_db.insert_orderitem(billitem, id)
        else:
            Reader_Writer.sqlite_db.update_orderitem(order, id)
    def delete_bill(bill):
        for bi in bill.items:
            Reader_Writer.delete_billitem(bi)
        Reader_Writer.sqlite_db.delete_bill(bill.id)
    def delete_orderitem(billitem):
        Reader_Writer.sqlite_db.delete_orderitem(billitem.id)
    def delete_orderitem_by_id(id):
        Reader_Writer.sqlite_db.delete_orderitem(id)
    def delete_order(order):
        for bi in order.items:
            Reader_Writer.delete_orderitem(bi)
        Reader_Writer.sqlite_db.delete_order(order.id)
    def write_order(order):
        if(order.id == 0):
            if(order.user.id == None):
                order.id = Reader_Writer.sqlite_db.insert_order(order, 0)
            else:
                order.id = Reader_Writer.sqlite_db.insert_order(order, order.user.id)
            for billitem in order.items:
                Reader_Writer.write_orderitem(billitem, order.id)
        else:
            if(order.user.id == None):
                Reader_Writer.sqlite_db.update_order(order, 0)
            else:
                Reader_Writer.sqlite_db.update_order(order, order.user.id)
            for billitem in order.items:
                Reader_Writer.write_orderitem(billitem, order.id)
    def write_orders(orders):
        for order in orders:
            Reader_Writer.write_order(order)
    def write_billitem(billitem, id):
        if(billitem.id == 0):
            billitem.id = Reader_Writer.sqlite_db.insert_billitem(billitem, id)
        else:
            Reader_Writer.sqlite_db.update_billitem(billitem, id)
    def write_bill(bill):
        if(bill.id == 0):
            bill.id = Reader_Writer.sqlite_db.insert_bill(bill)
            for billitem in bill.items:
                Reader_Writer.write_billitem(billitem, bill.id)
        else:
            Reader_Writer.sqlite_db.update_bill(bill)
            for billitem in bill.items:
                Reader_Writer.write_billitem(billitem, bill.id)
    def write_bills(bills):
        for bill in bills:
            Reader_Writer.write_bill(bill)
    def load_bills(bills, stock):
        Reader_Writer.sqlite_db.load_bills(bills, stock)
    def delete_billitem(billitem):
        Reader_Writer.sqlite_db.delete_billitem(billitem.id)
    def delete_billitem_by_id(id):
        Reader_Writer.sqlite_db.delete_billitem(id)
    def load_users(users):
        Reader_Writer.sqlite_db.load_users(users)
    def load_orders(orders, stock, users):
        Reader_Writer.sqlite_db.load_orders(orders, stock, users)
    def create_database():
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
        Reader_Writer.sqlite_db.create_table(User_script)
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
        Reader_Writer.sqlite_db.create_table(Stock_script)
        Bill_script = """CREATE TABLE IF NOT EXISTS Bills (
                                    id integer PRIMARY KEY,
                                    total real,
                                    date text NOT NULL,
                                    payment_method text NOT NULL,
                                    eet text NOT NULL,
                                    is_sale integer
                                );"""
        Reader_Writer.sqlite_db.create_table(Bill_script)
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
        Reader_Writer.sqlite_db.create_table(Order_script)
        BillItem_script = """CREATE TABLE IF NOT EXISTS BillItems (
                                    id integer PRIMARY KEY,
                                    count integer NOT NULL,
                                    item_id integer NOT NULL,
                                    bill_id integer NOT NULL,
                                    FOREIGN KEY (item_id) REFERENCES Stock (id)
                                    FOREIGN KEY (bill_id) REFERENCES Bills (id)
                                );"""
        Reader_Writer.sqlite_db.create_table(BillItem_script)
        OrderItem_script = """CREATE TABLE IF NOT EXISTS OrderItems (
                                    id integer PRIMARY KEY,
                                    count integer NOT NULL,
                                    item_id integer NOT NULL,
                                    order_id integer NOT NULL,
                                    FOREIGN KEY (item_id) REFERENCES Stock (id)
                                    FOREIGN KEY (order_id) REFERENCES Orders (id)
                                );"""
        Reader_Writer.sqlite_db.create_table(OrderItem_script)

class Orders:
    def __init__(self):
        self.orders = []
        if sqlite_mode == False:
            self.idcreator = IDcreator()
    def new(self, user):
        if sqlite_mode:
            order = Order(0, user)
            self.orders.append(order)
            Reader_Writer.write_order(order)
            return order
        else:
            order = Order(self.idcreator.getid(), user)
            self.orders.append(order)
            return order
    def add(self, order):
        self.orders.append(order)
    def load(self, id, user, total, total_weight, date, payment_method, shipping_method, address, status):
        order = Order(id, user)
        order.items = []
        order.total = total
        order.total_weight = total_weight
        order.date = date
        order.payment_method = payment_method
        order.shipping_method = shipping_method
        order.address = address
        order.status = status
        self.orders.append(order)
        return order
    def delete(self, search_term):
        o = self.find_order(search_term)
        if(o == None):
            return
        index = self.orders.index(o)
        if sqlite_mode:
            Reader_Writer.delete_order(o)
        del self.orders[index]
    def find_order(self, search_term):
        for o in self.orders:
            if(o.id == int(search_term)):
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
        if sqlite_mode == False:
            self.idcreator = IDcreator()
    def new(self):
        if sqlite_mode:
            bill = Bill(0)
            self.bills.append(bill)
            Reader_Writer.write_bill(bill)
            return bill
        else:
            bill = Bill(self.idcreator.getid())
            self.bills.append(bill)
            return bill
    def add(self, bill):
        self.bills.append(bill)
    def load(self, id, total, date, payment_method, eet, is_sale):
        bill = Bill(id)
        bill.total = total
        bill.date = date
        bill.payment_method = payment_method
        bill.eet = eet
        bill.is_sale = is_sale
        self.bills.append(bill)
        return bill
    def delete(self, search_term):
        b = self.find_bill(search_term)
        if(b == None):
            return
        index = self.bills.index(b)
        if sqlite_mode:
            Reader_Writer.delete_bill(b)
        del self.bills[index]
    def find_bill(self, search_term):
        for b in self.bills:
            if(b.id == int(search_term)):
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
        if sqlite_mode == False:
            self.idcreator = IDcreator()
    def new(self, name, real_name, password, phone, email, is_employee, is_manager):
        if sqlite_mode:
            self.users.append(User(0, name, real_name, password, phone, email, is_employee, is_manager))
        else:
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
    def find_user(self, search_term):
        for u in self.users:
            if(u.id == search_term or u.name == search_term or u.email == search_term):
                return u
        print("Item not found")
        return None
    def remove(self, search_term):
        u = self.find_user(search_term)
        if u is None:
            return
        index = self.users.index(u)
        del self.users[index]
    def __setitem__(self, number, data):
        self.users[number] = data
    def __getitem__(self, number):
        return self.users[number]
    def clear(self):
        self.users.clear()

class Stock:
    def __init__(self):
        self.stock = []  
        if sqlite_mode == False:
            self.idcreator = IDcreator()
    def load(self, id, name, code, price, dph, count, mincount, weight, is_age_restricted):
        self.stock.append(Item(int(id), name, code, float(price), int(dph), int(count), int(mincount), float(weight), bool(is_age_restricted)))
    def add(self, item):
        self.stock.append(item)
    def new(self, name, code, price, dph, count, mincount, weight, is_age_restricted):
        if sqlite_mode:
            item = Item(0, name, code, price, dph, count, mincount, weight, is_age_restricted)
            self.stock.append(item)
            Reader_Writer.write_item(item)
            return item
        else:
            item = Item(self.idcreator.getid(), name, code, price, dph, count, mincount, weight, is_age_restricted)
            self.stock.append(item)
            return item
    def delete(self, search_term):
        i = self.find_item(search_term)
        if i is None:
            return
        if sqlite_mode:
            Reader_Writer.delete_item(i)
        index = self.stock.index(i)
        del self.stock[index]
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