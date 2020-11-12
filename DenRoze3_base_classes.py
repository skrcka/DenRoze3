import os
from datetime import datetime
from pprint import pprint as print


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

class User:
    def __init__(self, id, name, password, is_employee, is_admin):
        self.id = id
        self.name = name
        self.password = password
        self.is_employee = is_employee
        self.is_admin = is_admin
