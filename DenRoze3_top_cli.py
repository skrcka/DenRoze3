from pprint import pprint
from DenRoze3_middle import Reader_Writer, Stock, Bills, Users, Orders, sqlite_mode, Reader_Writer_json
from DenRoze3_base_classes import Item, BillItem, Bill, DateCreator
    
stock = Stock()
bills = Bills()
orders = Orders()
users = Users()

if sqlite_mode:
    Reader_Writer.init()
    Reader_Writer.load_all(stock, bills, orders, users)
else:
    Reader_Writer_json.init()
    Reader_Writer_json.load_all(stock, bills, orders, users)

app_on = True
b = None
o = None
u = None
i = None

while(app_on):
    commands = []
    user_input = input()
    commands = user_input.split(' ')
    try:
        if(u == None):
            if(commands[0] == "login"):
                u = users.auth(commands[1], commands[2])
                continue
            elif(commands[0] == "quit"):
                app_on = False
                break
            else:
                print("Please login first: login [username] [password]")
                continue
        if(commands[0] == "quit"):
            app_on = False
            break
        elif(commands[0] == "logout"):
            u = None
        elif(commands[0] == "stock"):
            if(commands[1] == "new"):
                i = stock.new(commands[2], commands[3], float(commands[4]), int(commands[5]), int(commands[6]), int(commands[7]), float(commands[8]), bool(commands[9]))
            elif(commands[1] == "print"):
                stock.print()
            elif(commands[1] == "edit"):
                i = stock.find_item(commands[2])
                if i == None:
                    print("Wrong input!")
                    continue
                if(commands[3] == "name"):
                    i.name = commands[4]
                elif(commands[3] == "code"):
                    i.code = commands[4]
                elif(commands[3] == "price"):
                    i.price = commands[4]
                elif(commands[3] == "dph"):
                    i.dph = commands[4]
                elif(commands[3] == "count"):
                    i.count = commands[4]
                elif(commands[3] == "mincount"):
                    i.mincount = commands[4]
                elif(commands[3] == "weight"):
                    i.weight = commands[4]
                elif(commands[3] == "is_age_restricted"):
                    i.is_age_restricted = commands[4]
            elif(commands[1] == "add"):
                i = stock.find_item(commands[2])
                if i == None:
                    print("Wrong input!")
                    continue
                i.count += commands[3]
            elif(commands[1] == "remove"):
                i = stock.find_item(commands[2])
                if i == None:
                    print("Wrong input!")
                    continue
                i.count -= commands[3]
            elif(commands[1] == "delete"):
                stock.delete(commands[2])
            else:
                print("Wrong input!")
                continue
        elif(commands[0] == "bill"):
            if(commands[1] == "new"):
                b = bills.new()
            elif(commands[1] == "select"):
                b = bills.find_bill(commands[2])
            elif(commands[1] == "delete"):
                bills.delete(commands[2])
            elif(commands[1] == "add"):
                if(b == None):
                    print("Wrong bill selected")
                    continue
                b.add_item(stock.find_item(commands[2]), int(commands[3]))
            elif(commands[1] == "remove"):
                if(b == None):
                    print("Wrong bill selected")
                    continue
                biID = b.remove_item(commands[2])
                if sqlite_mode:
                    Reader_Writer.delete_billitem_by_id(biID)
            elif(commands[1] == "print"):
                if(b == None):
                    print("Wrong bill selected")
                    continue
                b.print()
            elif(commands[1] == "printall"):
                bills.print()
            else:
                print("Wrong input!")
                continue
        elif(commands[0] == "write"):
            if sqlite_mode:
                Reader_Writer.write_changes(stock, bills, orders)
            else:
                Reader_Writer_json.write_changes(stock, bills, orders)
            app_on = False
            break
        elif(commands[0] == "order"):
            if(commands[1] == "new"):
                o = orders.new(u)
            elif(commands[1] == "select"):
                o = orders.find_order(commands[2])
            elif(commands[1] == "delete"):
                orders.delete(int(commands[2]) - 1)
            elif(commands[1] == "add"):
                if(o == None):
                    print("Wrong order selected")
                    continue
                o.add_item(stock.find_item(commands[2]), int(commands[3]))
                if sqlite_mode:
                    Reader_Writer.write_order(o)
            elif(commands[1] == "remove"):
                if(o == None):
                    print("Wrong order selected")
                    continue
                biID = o.remove_item(commands[2])
                if sqlite_mode:
                    Reader_Writer.delete_orderitem_by_id(biID)
            elif(commands[1] == "change"):
                if(o == None):
                    print("Wrong order selected")
                    continue
                o.change_item(int(commands[2]) - 1, int(commands[3]))
            elif(commands[1] == "print"):
                if(o == None):
                    print("Wrong bill selected")
                    continue
                o.print()
            elif(commands[1] == "printall"):
                orders.print()
            else:
                print("Wrong input!")
                continue
        elif(commands[0] == "help"):
            print("Use with: [stock/bill/order/quit/write]")
            print("stock help: ")
            print("\t new - Creates new item and adds it to stock")
            print("\t print - Prints stock")
            print("\t edit [item] [attribute] [newvalue] - Edits item in stock")
            print("\t add [item] [count] - Adds count to item in stock")
            print("\t remove [item] [count] - Removes count from item in stock")
            print("\t delete [item] - Removes item from stock")
            print("bill help: ")
            print("\t new - Creates new bill and selects it")
            print("\t select - Selects bill")
            print("\t delete [id] - Deletes bill")
            print("\t remove [item] - Removes item from selected bill")
            print("\t print - Prints selected bill")
            print("\t printall - Prints all bills")
            print("order help: ")
            print("\t new - Creates new order and selects it")
            print("\t select - Selects order")
            print("\t delete [id] - Deletes order")
            print("\t remove [item] - Removes item from selected order")
            print("\t print - Prints selected order")
            print("\t printall - Prints all orders")
            print("quit - Exits and saves")
            print("write - Substracts all sales from stock, writes and exits")
        else:
            print("Wrong input!")
            continue
    except Exception as e:
        print(e) 
    if i is not None:
        if sqlite_mode:
            Reader_Writer.write_item(i)
    if b is not None:
        if sqlite_mode:
            Reader_Writer.write_bill(b)
    if o is not None:
        if sqlite_mode:
            Reader_Writer.write_order(o)
if sqlite_mode:
    Reader_Writer.write_all_and_clear(stock, bills, orders, users)
    Reader_Writer.close_connection()
else:
    Reader_Writer_json.write_all_and_clear(stock, bills, orders, users)