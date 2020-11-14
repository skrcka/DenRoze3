import os
from datetime import datetime
from pprint import pprint


class IDcreator:
    def __init__(self):
        self.id = 0
    def getid(self):
        self.id += 1
        return self.id
    def setmaxid(self, var):
        maxid = 0
        for v in var:
            if v.id > maxid:
                maxid = v.id
        self.id = maxid

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
    def __init__(self, id):
        self.id = id
        self.user = None
        self.items = []
        self.total = 0
        self.total_weight = 0
        self.date = datetime.now()
        self.payment_method = ""
        self.shipping_method = ""
        self.address = ""
    def add_item(self, item, count):
        self.total += item.price * count
        self.total_weight += item.weight * count
        self.items.append(BillItem(item, count))
    def remove_item(self, id):
        self.total -= self.items[id].item.price * self.items[id].count
        self.total_weight -= self.items[id].item.weight * self.items[id].count
        del self.items[id]
    def print(self):
        print("****************************************************")
        print("Objednavka: [%d] Datum a cas: %s" % (self.id, self.date))
        print("Zbozi: [id] nazev dph mnozstvi cena cena_celkem")
        for i in self.items:
            print('\t[%d] %s %d %d %.2f %.2f' % (i.item.id, i.item.name, i.item.dph, i.count, i.item.price, i.item.price * i.count))
        print("Celkova cena: %.2f" % self.total)
        print("Celkova vaha: %.2f" % self.total_weight)
        print("Shipping method: %s" % self.shipping_method)
        print("Address: %s" % self.address)
        print("****************************************************")
    def transform(self):
        order_dict = {
            'id': self.id,
            'user': self.user,
            'items': [],
            'total': self.total,
            'total_weight': self.total_weight,
            'date': self.date,
            'payment_method': self.payment_method,
            'shipping_method': self.shipping_method,
            'address': self.address
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
            order_dict['items'].append(billitem_dict)
        return order_dict

class Bill:
    def __init__(self, id):
        self.id = id
        self.items = []
        self.total = 0
        self.date = datetime.now()
        self.payment_method = ""
        self.eet = ""
        self.is_sale = True
    def add_item(self, item, count):
        self.items.append(BillItem(item, count))
        self.total += item.price * count
    def load_item(self, id, name, code, price, dph, count, mincount, weight, is_age_resctricted, sale_count):
        self.items.append(BillItem(Item(id, name, code, price, dph, count, mincount, weight, is_age_resctricted), sale_count))
        self.total += price * sale_count
    def remove_item(self, id):
        self.total -= self.items[id].item.price * self.items[id].count
        del self.items[id]
    def transform(self):
        bill_dict = {
            'id': self.id,
            'items': [],
            'total': self.total,
            'date': self.date,
            'payment_method': self.payment_method
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
    def print(self):
        print("****************************************************")
        print("Uctenka: [%d] Datum a cas: %s" % (self.id, self.date))
        print("Zbozi: [id] nazev dph mnozstvi cena cena_celkem")
        for i in self.items:
            print('\t[%d] %s %d %d %.2f %.2f' % (i.item.id, i.item.name, i.item.dph, i.count, i.item.price, i.item.price * i.count))
        print("Celkova cena: %.2f" % self.total)
        print("EET kod: %s" % self.eet)
        print("****************************************************")

class User:
    def __init__(self, id, name, real_name, password, phone, email, is_employee, is_manager):
        self.id = id
        self.name = name
        self.real_name = real_name
        self.password = password
        self.phone = phone
        self.email = email
        self.is_employee = is_employee
        self.is_manager = is_manager
