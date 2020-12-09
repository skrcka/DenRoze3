import json
import os
from datetime import datetime
from DenRoze3_base_classes import Item, BillItem, Order, Bill, User
import sqlite3
from sqlite3 import Error


class Sqlite_db:
    def __init__(self):
        self.path_to_sqlite = os.path.abspath(os.path.join('data', 'database.sqlite'))
        self.conn = None
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.path_to_sqlite)
        except Error as e:
            print(e)
    def close_connection(self):
        self.conn.close()
        self.conn = None

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_item(self, item):
        self.create_connection()
        sql = 'INSERT INTO Stock(name,code,price,dph,count,mincount,weight,is_age_restricted) VALUES(?,?,?,?,?,?,?,?)'
        cur = self.conn.cursor()
        is_age_restricted = 0
        if item.is_age_restricted == True:
            is_age_restricted = 1
        cur.execute(sql, (str(item.name), str(item.code), str(item.price), str(item.dph), str(item.count), str(item.mincount), str(item.weight), str(is_age_restricted)))
        self.conn.commit()
    
        return cur.lastrowid
        self.close_connection()

    def update_item(self, item):
        sql = 'UPDATE Stock SET name = ?, code = ?, price = ?, dph = ?, count = ?, mincount = ?, weight = ?, is_age_restricted = ? WHERE id = ?'
        cur = self.conn.cursor()
        is_age_restricted = 0
        if item.is_age_restricted == True:
            is_age_restricted = 1
        cur.execute(sql, (str(item.name), str(item.code), str(item.price), str(item.dph), str(item.count), str(item.mincount), str(item.weight), str(is_age_restricted), str(item.id)))
        self.conn.commit()

    def delete_item(self, id):
        sql = 'DELETE FROM Stock WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    def load_stock(self, stock):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Stock")

        rows = cur.fetchall()

        for row in rows:
            stock.load(int(row[0]), row[1], row[2], float(row[3]), int(row[4]), int(row[5]), int(row[6]), float(row[7]), bool(row[8]))

    def load_item(self, item, search_term):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Stock WHERE code=?")

        rows = cur.fetchall()
        item.id = int(row[0])
        item.name = row[1]
        item.code = row[2]
        item.price = float(row[3])
        item.dph = int(row[4])
        item.count = int(row[5])
        item.mincount = int(row[6])
        item.weight = float(row[7])
        item.is_age_restricted = False
        if row[8] == '1':
            item.is_age_restricted = True

    def insert_bill(self, bill):
        sql = 'INSERT INTO Bills(total,date,payment_method,eet,is_sale) VALUES(?,?,?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, (str(bill.total), str(bill.date), str(bill.payment_method), str(bill.eet), str(bill.is_sale)))
        self.conn.commit()
        bill_id = cur.lastrowid

        return bill_id

    def update_bill(self, bill):
        sql = 'UPDATE Bills SET total = ?, date = ?, payment_method = ?, eet = ?, is_sale = ? WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, (str(bill.total), str(bill.date), str(bill.payment_method), str(bill.eet), str(bill.is_sale), str(bill.id)))
        self.conn.commit()

    def load_bills(self, bills, stock):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Bills WHERE date(date) = date('now')")

        rows = cur.fetchall()

        for row in rows:
            bill = bills.load(int(row[0]), float(row[1]), row[2], row[3], row[4], bool(row[5]))
            self.load_billitems(bill, stock)

    def load_billitems(self, bill, stock):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM BillItems WHERE bill_id={}".format(str(bill.id)))

        rows = cur.fetchall()
        for row in rows:
            item = stock.find_item(int(row[2]))
            bill.load_item_db(int(row[0]), item, int(row[1]))

    def delete_bill(self, id):
        sql = 'DELETE FROM Bills WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    def insert_order(self, order, uid):
        sql = 'INSERT INTO Orders(user_id,total,total_weight,date,payment_method,shipping_method,address,status) VALUES(?,?,?,?,?,?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, (str(uid), str(order.total), str(order.total_weight), str(order.date), str(order.payment_method),str(order.shipping_method),str(order.address),str(order.status)))
        self.conn.commit()
        order_id = cur.lastrowid

        return order_id
    
    def update_order(self, order, uid):
        sql = 'UPDATE Orders SET user_id = ?, total = ?, total_weight = ?, date = ?, payment_method = ?, shipping_method = ?, address = ?, status = ? WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, (str(uid), str(order.total), str(order.total_weight), str(order.date), str(order.payment_method),str(order.shipping_method),str(order.address),str(order.status), str(order.id)))
        self.conn.commit()

    def load_orders(self, orders, stock, users):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Orders WHERE date(date) = date('now')")

        rows = cur.fetchall()

        for row in rows:
            user = users.find_user(int(row[1]))
            order = orders.load(int(row[0]), user, float(row[2]), float(row[3]), row[4], row[5], row[6], row[7], row[8])
            self.load_orderitems(order, stock)

    def load_orderitems(self, order, stock):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM OrderItems WHERE order_id={}".format(str(order.id)))

        rows = cur.fetchall()
        for row in rows:
            item = stock.find_item(int(row[2]))
            order.load_item_db(int(row[0]), item, int(row[1]))

    def delete_order(self, id):
        sql = 'DELETE FROM Orders WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()
    
    def insert_orderitem(self, billitem, id):
        sql = 'INSERT INTO OrderItems(count,item_id,order_id) VALUES(?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, (str(billitem.count), str(billitem.item.id), str(id)))
        self.conn.commit()
        orderitem_id = cur.lastrowid

        return orderitem_id

    def update_orderitem(self, billitem, id):
        sql = 'UPDATE OrderItems SET count = ?, item_id = ?, order_id = ? WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, (str(billitem.count), str(billitem.item.id), str(id), str(billitem.id)))
        self.conn.commit()

    def delete_orderitem(self, id):
        sql = 'DELETE FROM OrderItems WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    def insert_billitem(self, billitem, id):
        sql = 'INSERT INTO BillItems(count,item_id,bill_id) VALUES(?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, (str(billitem.count), str(billitem.item.id), str(id)))
        self.conn.commit()
        billitem_id = cur.lastrowid

        return billitem_id

    def update_billitem(self, billitem, id):
        sql = 'UPDATE BillItems SET count = ?, item_id = ?, bill_id = ? WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, (str(billitem.count), str(billitem.item.id), str(id), str(billitem.id)))
        self.conn.commit()

    def delete_billitem(self, id):
        sql = 'DELETE FROM BillItems WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    def insert_user(self, user):
        sql = 'INSERT INTO Users(name,real_name,password,phone,email,is_employee,is_manager) VALUES(?,?,?,?,?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, (str(user.name), str(user.real_name), str(user.password), str(user.phone), str(user.email), str(user.is_employee), str(user.is_manager)))
        self.conn.commit()
        billitem_id = cur.lastrowid

        return billitem_id

    def update_user(self, user):
        sql = 'UPDATE Users SET name = ?, real_name = ?, password = ?, phone = ?, email = ?, is_employee = ?, is_manager = ? WHERE id = ?'
        cur = self.conn.cursor()
        cur.execute(sql, (str(user.name), str(user.real_name), str(user.password), str(user.phone), str(user.email), str(user.is_employee), str(user.is_manager), str(user.id)))
        self.conn.commit()
    
    def delete_user(self, id):
        sql = 'DELETE FROM Users WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    def load_users(self, users):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Users")

        rows = cur.fetchall()

        for row in rows:
            users.load(int(row[0]), row[1], row[2], row[3], row[4], row[5], bool(row[6]), bool(row[7]))
