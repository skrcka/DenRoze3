from pprint import pprint as print
from DenRoze3_middle import Reader_Writer, Stock, Bills, Users
from DenRoze3_base_classes import Item, BillItem, Bill

rw = Reader_Writer()
stock = Stock()
bills = Bills()
#rw.load_stock(stock)
#rw.load_bills(bills)
#stock.load(0, "vejce", "vesnica", 10, 21, 100, 10, 50, False)
#stock.load(1, "piko", "dubina", 200, 0, 69, 10, 1, False)
#rw.write_stock_local(stock)
rw.load_stock_local(stock)
#print(stock[0].weight)
#b = bills.new()
#b.add_item(stock[0],3)
#b.add_item(stock[1],1)
#b = bills.new()
#b.add_item(stock[0],30)
#b.add_item(stock[1],10)
#rw.write_bills_local(bills)
rw.load_bills_local(bills)
bills.print()