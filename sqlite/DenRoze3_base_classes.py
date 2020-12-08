import os
from datetime import datetime
from pprint import pprint


class DateCreator:
    def getdate(self, day, month, year):
        newdate = datetime(year, month, day)
        return newdate

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
    def print(self):
        print("[{}]{}, {}, {}({}), {}, {}, {}, {}".format(self.id, self.name, self.code, self.price, self.dph, self.count, self.mincount, self.weight, self.is_age_restricted))

class BillItem:
    def __init__(self, id, item, count):
        self.id = id
        self.item = item
        self.count = count

class Order:
    def __init__(self, id, user):
        self.id = id
        self.user = user
        self.items = []
        self.total = 0
        self.total_weight = 0
        self.date = datetime.now()
        self.payment_method = ""
        self.shipping_method = ""
        self.address = ""
        self.status = ""
    def count_totals(self):
        self.total = 0
        self.total_weight = 0
        for item in self.items:
            self.total += float(item.item.price) * int(item.count)
            self.total_weight += float(item.item.weight) * int(item.count)
    def load_item(self, idbi, idi, name, code, price, dph, count, mincount, weight, is_age_restricted, sale_count):
        self.items.append(BillItem(int(idbi), Item(int(idi), name, code, float(price), int(dph), int(count), int(mincount), float(weight), bool(is_age_restricted)), sale_count))
        self.total += float(price) * int(sale_count)
        self.total_weight += float(weight) * int(sale_count)
    def load_item_db(self, id, item, count):
        self.items.append(BillItem(id, item, count))
    def add_item(self, item, count):
        self.total += item.price * count
        self.total_weight += item.weight * count
        self.items.append(BillItem(0, item, count))
    def find_item(self, search_term):
        for i in self.items:
            if(i.item.id == search_term or i.item.name == search_term or i.item.code == search_term):
                return i
        print("Item not found")
        return None
    def change_item(self, search_term, count):
        i = self.find_item(search_term)
        i.count = count
    def remove_item(self, search_term):
        i = self.find_item(search_term)
        if i is not None:
            index = self.items.index(i)
            id = i.id
            self.total -= i.item.price * i.count
            self.total_weight -= i.item.weight * i.count
            del self.items[index]
            return id
    def remove_item_by_position(self, pos):
        i = self.items[pos]
        id = i.id
        self.total -= i.item.price * i.count
        del self.items[pos]
        return id
    def print(self):
        print("****************************************************")
        print("Objednavka: [%d] Datum a cas: %s" % (self.id, self.date))
        print("Status %s" % self.status)
        print("Zbozi: [id] nazev dph mnozstvi cena cena_celkem")
        for i in self.items:
            print('\t[%d] %s %d %d %.2f %.2f' % (i.id, i.item.name, i.item.dph, i.count, i.item.price, i.item.price * i.count))
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
            'address': self.address,
            'status': self.status
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
                "id": billitem.id,
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
    def change_type(self):
        self.is_sale = not self.is_sale
    def count_totals(self):
        self.total = 0
        for item in self.items:
            self.total += float(item.item.price) * int(item.count)
    def add_item(self, item, count):
        self.items.append(BillItem(0, item, int(count)))
        self.total += item.price * int(count)
    def load_item(self, idbi, idi, name, code, price, dph, count, mincount, weight, is_age_restricted, sale_count):
        self.items.append(BillItem(int(idbi), Item(int(idi), name, code, float(price), int(dph), int(count), int(mincount), float(weight), bool(is_age_restricted)), sale_count))
        self.total += float(price) * int(sale_count)
    def load_item_db(self, id, item, count):
        self.items.append(BillItem(id, item, count))
    def change_item(self, search_term, count):
        i = self.find_item(search_term)
        i.count = count
    def find_item(self, search_term):
        for i in self.items:
            if(i.id == search_term):
                return i
            if(i.item.id == search_term or i.item.name == search_term or i.item.code == search_term):
                return i
        print("Item not found")
        return None
    def remove_item(self, search_term):
        i = self.find_item(search_term)
        if i is not None:
            index = self.items.index(i)
            id = i.id
            self.total -= i.item.price * i.count
            del self.items[index]
            return id
    def remove_item_by_position(self, pos):
        i = self.items[pos]
        id = i.id
        self.total -= i.item.price * i.count
        del self.items[pos]
        return id
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
                "id": billitem.id,
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
            print('\t[%d] %s %d %d %.2f %.2f' % (i.id, i.item.name, i.item.dph, i.count, i.item.price, i.item.price * i.count))
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
