from PyQt5 import QtWidgets, uic
import sys
from DenRoze3_middle import Reader_Writer, Stock, Bills, Users, Orders, sqlite_mode,Reader_Writer_json
from DenRoze3_base_classes import Item, BillItem, Bill, DateCreator


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        # Program stuff
        self.stock = Stock()
        self.bills = Bills()
        self.orders = Orders()
        self.users = Users()

        if sqlite_mode:
            Reader_Writer.init()
            Reader_Writer.load_all(self.stock, self.bills, self.orders, self.users)
        else:
            Reader_Writer_json.init()
            Reader_Writer_json.load_all(self.stock, self.bills, self.orders, self.users)

        self.b = None
        self.o = None
        self.u = None
        self.i = None
        # UIC loads
        uic.loadUi('gui.ui', self)
        uic.loadUi('login_widget.ui', self.login_widget)
        uic.loadUi('stock_widget.ui', self.stock_widget)
        uic.loadUi('bills_widget.ui', self.bills_widget)
        uic.loadUi('orders_widget.ui', self.orders_widget)
        # Fill lists
        self.get_stock_list()
        self.get_orders_list()
        self.get_bills_list()
        # List select binding
        self.stock_widget.stock_list.currentItemChanged.connect(self.stock_select)

        self.bills_widget.stock_list.currentItemChanged.connect(self.bill_stock_select)
        self.bills_widget.bills_list.currentItemChanged.connect(self.bill_select)
        self.bills_widget.bill_items_list.currentItemChanged.connect(self.bill_item_select)

        self.orders_widget.stock_list.currentItemChanged.connect(self.order_stock_select)
        self.orders_widget.orders_list.currentItemChanged.connect(self.order_select)
        self.orders_widget.order_items_list.currentItemChanged.connect(self.order_item_select)
        # Initial hide
        self.stock_widget.hide()
        self.bills_widget.hide()
        self.orders_widget.hide()
        self.menu_widget.hide()
        self.stock_button.setEnabled(False)
        self.bills_button.setEnabled(False)
        self.orders_button.setEnabled(False)
        # Menu buttons
        self.stock_button.clicked.connect(self.stock_menu)
        self.bills_button.clicked.connect(self.bill_menu)
        self.orders_button.clicked.connect(self.order_menu)
        self.write_button.clicked.connect(self.write)
        # Widget buttons
        self.login_widget.login_button.clicked.connect(self.login)

        self.stock_widget.stock_delete_button.clicked.connect(self.stock_delete)
        self.stock_widget.stock_add_button.clicked.connect(self.stock_new)
        self.stock_widget.stock_item_save_button.clicked.connect(self.stock_edit)

        self.bills_widget.bills_add_button.clicked.connect(self.bill_new)
        self.bills_widget.bills_delete_button.clicked.connect(self.bill_delete)
        self.bills_widget.bill_add_item_button.clicked.connect(self.bill_add_item)
        self.bills_widget.bill_remove_item_button.clicked.connect(self.bill_remove_item)
        self.bills_widget.bill_print_button.clicked.connect(self.bill_print)

        self.orders_widget.orders_add_button.clicked.connect(self.order_new)
        self.orders_widget.orders_delete_button.clicked.connect(self.order_delete)
        self.orders_widget.order_add_item_button.clicked.connect(self.order_add_item)
        self.orders_widget.order_remove_item_button.clicked.connect(self.order_remove_item)
        self.orders_widget.order_print_button.clicked.connect(self.order_print)
        # Show GUI
        self.show()
    def write(self):
        if sqlite_mode:
            Reader_Writer.write_changes(self.stock, self.bills, self.orders)
        else:
            Reader_Writer_json.write_changes(self.stock, self.bills, self.orders)
        self.close()
    def bill_print(self):
        self.b.print()
    def order_print(self):
        self.o.print()
    def bill_add_item(self):
        self.b.add_item(self.i, int(self.bills_widget.bill_item_count.text()))
        if sqlite_mode:
            Reader_Writer.write_bill(self.b)
        self.get_bill_items_list()
    def order_add_item(self):
        self.o.add_item(self.i, int(self.orders_widget.order_item_count.text()))
        if sqlite_mode:
            Reader_Writer.write_order(self.o)
        self.get_order_items_list()
    def bill_remove_item(self):
        if self.b is not None:
            biID = self.b.remove_item_by_position(self.bills_widget.bill_items_list.currentRow())
            if sqlite_mode:
                Reader_Writer.delete_billitem_by_id(biID)
            self.get_bill_items_list()
    def order_remove_item(self):
        if self.o is not None:
            biID = self.o.remove_item_by_position(self.orders_widget.bill_items_list.currentRow())
            if sqlite_mode:
                Reader_Writer.delete_orderitem_by_id(biID)
            self.get_order_items_list()
    def bill_new(self):
        self.b = self.bills.new()
        self.get_bills_list()
    def order_new(self):
        self.o = self.orders.new(self.u)
        self.get_orders_list()
    def bill_delete(self):
        if self.b is not None:
            self.bills.delete(self.b.id)
            self.get_bills_list()
            self.b = None
    def order_delete(self):
        if self.o is not None:
            self.orders.delete(self.o.id)
            self.get_orders_list()
            self.o = None
    def bill_item_select(self):
        self.bills_widget.bill_remove_item_button.setEnabled(True)
    def order_item_select(self):
        self.orders_widget.order_remove_item_button.setEnabled(True)
    def bill_stock_select(self):
        self.bills_widget.bill_add_item_button.setEnabled(True)
        self.i = self.stock[self.bills_widget.stock_list.currentRow()]
    def order_stock_select(self):
        self.orders_widget.order_add_item_button.setEnabled(True)
        self.i = self.stock[self.orders_widget.stock_list.currentRow()]
    def bill_select(self):
        self.bills_widget.bills_delete_button.setEnabled(True)
        self.bills_widget.stock_list.setEnabled(True)
        self.bills_widget.bill_print_button.setEnabled(True)
        if len(self.bills.bills) == 0:
            return
        self.b = self.bills[self.bills_widget.bills_list.currentRow()]
        self.get_bill_items_list()
    def order_select(self):
        self.orders_widget.orders_delete_button.setEnabled(True)
        self.orders_widget.stock_list.setEnabled(True)
        self.orders_widget.order_print_button.setEnabled(True)
        if len(self.orders.orders) == 0:
            return
        self.o = self.orders[self.orders_widget.orders_list.currentRow()]
        self.get_order_items_list()
    def stock_edit(self):
        self.i.name = self.stock_widget.stock_item_name_edit.text()
        self.i.code = self.stock_widget.stock_item_code_edit.text()
        self.i.price = float(self.stock_widget.stock_item_price_edit.text())
        self.i.dph = int(self.stock_widget.stock_item_dph_edit.text())
        self.i.count = int(self.stock_widget.stock_item_count_edit.text())
        self.i.mincount = int(self.stock_widget.stock_item_mincount_edit.text())
        self.i.weight = float(self.stock_widget.stock_item_weight_edit.text())
        self.i.is_age_restricted = self.stock_widget.stock_item_is_age_restricted_edit.text()
        self.get_stock_list()
        if sqlite_mode:
            Reader_Writer.write_item(self.i)
    def stock_new(self):
        self.stock.new("NEW ITEM", "", 0, 0, 0, 0, 0, False)
        self.get_stock_list()
    def closeEvent(self, event):
        if sqlite_mode:
            Reader_Writer.write_all_and_clear(self.stock, self.bills, self.orders, self.users)
            Reader_Writer.close_connection()
        else:
            Reader_Writer_json.write_all_and_clear(self.stock, self.bills, self.orders, self.users)
    def get_stock_list(self):
        self.stock_widget.stock_list.clear()
        self.bills_widget.stock_list.clear()
        self.orders_widget.stock_list.clear()
        for item in self.stock:
            self.stock_widget.stock_list.addItem(item.name)
            self.bills_widget.stock_list.addItem(item.name)
            self.orders_widget.stock_list.addItem(item.name)
    def get_orders_list(self):
        self.orders_widget.orders_list.clear()
        for order in self.orders:
            self.orders_widget.orders_list.addItem(str(order.id))
    def get_order_items_list(self):
        self.orders_widget.order_items_list.clear()
        for item in self.o.items:
            self.orders_widget.order_items_list.addItem('[{}] {} * {}'.format(str(item.id), str(item.item.name), str(item.count)))
    def get_bills_list(self):
        self.bills_widget.bills_list.clear()
        for bill in self.bills:
            self.bills_widget.bills_list.addItem(str(bill.id))
    def get_bill_items_list(self):
        self.bills_widget.bill_items_list.clear()
        for item in self.b.items:
            self.bills_widget.bill_items_list.addItem('[{}] {} * {}'.format(str(item.id), str(item.item.name), str(item.count)))
    def stock_delete(self):
        if self.i is not None:
            self.stock.delete(self.i.id)
            self.get_stock_list()
            self.i = None
    def stock_select(self):
        if len(self.stock.stock) == 0:
            return
        self.stock_widget.stock_delete_button.setEnabled(True)
        self.stock_widget.stock_item_save_button.setEnabled(True)
        self.i = self.stock[self.stock_widget.stock_list.currentRow()]
        self.stock_widget.stock_item_id_edit.setText(str(self.i.id))
        self.stock_widget.stock_item_name_edit.setText(self.i.name)
        self.stock_widget.stock_item_code_edit.setText(self.i.code)
        self.stock_widget.stock_item_price_edit.setText(str(self.i.price))
        if self.i.dph is not None:
            self.stock_widget.stock_item_dph_edit.setText(str(self.i.dph))
        else:
            self.stock_widget.stock_item_dph_edit.setText("")
        if self.i.count is not None:
            self.stock_widget.stock_item_count_edit.setText(str(self.i.count))
        else:
            self.stock_widget.stock_item_count_edit.setText("")
        if self.i.mincount is not None:
            self.stock_widget.stock_item_mincount_edit.setText(str(self.i.mincount))
        else:
            self.stock_widget.stock_item_mincount_edit.setText("")
        if self.i.weight is not None:
            self.stock_widget.stock_item_weight_edit.setText(str(self.i.weight))
        else:
            self.stock_widget.stock_item_weight_edit.setText("")
        if self.i.is_age_restricted is not None:
            self.stock_widget.stock_item_is_age_restricted_edit.setText(str(self.i.is_age_restricted))
        else:
            self.stock_widget.stock_item_is_age_restricted_edit.setText("")
    def login(self):
        self.u = self.users.auth(self.login_widget.username_edit.text(), self.login_widget.password_edit.text())
        if self.u is not None:
            self.login_widget.hide()
            self.menu_widget.show()
            self.stock_button.setEnabled(True)
            self.bills_button.setEnabled(True)
            self.orders_button.setEnabled(True)
            self.update()
    def stock_menu(self):
        self.bills_widget.hide()
        self.orders_widget.hide()
        self.login_widget.hide()
        self.stock_widget.show()
    def bill_menu(self):
        self.stock_widget.hide()
        self.orders_widget.hide()
        self.login_widget.hide()
        self.bills_widget.show()
    def order_menu(self):
        self.stock_widget.hide()
        self.bills_widget.hide()
        self.login_widget.hide()
        self.orders_widget.show()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()