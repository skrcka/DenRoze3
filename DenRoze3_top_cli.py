from pprint import pprint as print
from DenRoze3_middle import Reader_Writer
from DenRoze3_middle import Stock
from DenRoze3_middle import Bills
from DenRoze3_middle import Users

rw = Reader_Writer()
stock = Stock()
bills = Bills()
#rw.load_stock(stock)
#rw.load_bills(bills)
stock.load(0, "vejce", "vesnica", 10, 21, 100, 10, 50, False)
stock.load(1, "piko", "dubina", 200, 0, 69, 10, 1, False)
print(stock[0].weight)
#bill.remove_item(0)
#print(bill.items[0].item.weight)
#print(bill.date)
# db.get_stock(stock)
#json = Json()
#json.load_stock(stock)
#print(stock[0].name)
#json.load(1,"skero", "dubina2", 200, 0, 100, 20, 1, False)
#json.write_stock(stock)
#db.write_stock(stock)
#db.load_stock(stock)
#bills[0].add_item(stock[0],5)
#bills[0].add_item(stock[1],3)
#db.write_bills(bills)
#print(stock[1].name)
#db.load_bills(bills)
#db.write(stock, bills)
#db.write_stock(stock)
#print(bills[0].total)