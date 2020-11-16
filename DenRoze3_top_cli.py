from pprint import pprint
from DenRoze3_middle import Reader_Writer, Stock, Bills, Users, Orders
from DenRoze3_base_classes import Item, BillItem, Bill, DateCreator

rw = Reader_Writer()
stock = Stock()
bills = Bills()
orders = Orders()
users = Users()

rw.load_all_local(stock, bills, orders, users)
app_on = True
while(app_on):
    commands = []
    user_input = input()
    commands = user_input.split(' ')
    pprint(commands)
    if(commands[0] == "quit"):
        app_on = False
        break
    elif(commands[0] == "stock"):
        if(commands[1] == "new"):
            print("name, code, price, dph, count, mincount, weight, is_age_restricted")
            name, code, price, dph, count, mincount, weight, is_age_restricted = input().split(" ")
            stock.new(name, code, price, dph, count, mincount, weight, is_age_restricted)
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
        b = None
        if(commands[1] == "new"):
            b = bills.new()
        elif(commands[1] == "select"):
            b = bills[commands[2]]
        elif(commands[1] == "delete"):
            bills.delete(commands[2])
        elif(commands[1] == "add"):
            if(b == None):
                print("Wrong bill selected")
                continue
            b.add_item(stock.find_item(commands[2]), commands[3])
        elif(commands[1] == "remove"):
            if(b == None):
                print("Wrong bill selected")
                continue
            b.remove_item(commands[2])
        else:
            print("Wrong input!")
            continue
    elif(commands[0] == "order"):
        pass
    elif(commands[0] == "help"):
        pass
    else:
        print("Wrong input!")
        continue
rw.write_local_and_clear(stock, bills, orders, users)