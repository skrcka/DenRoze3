from PyQt5 import QtWidgets, uic
import sys
from DenRoze3_middle import Reader_Writer, Stock, Bills, Users, Orders
from DenRoze3_base_classes import Item, BillItem, Bill, DateCreator


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        # Program stuff
        self.stock = Stock()
        self.bills = Bills()
        self.orders = Orders()
        self.users = Users()

        Reader_Writer.init()
        Reader_Writer.load_all(self.stock, self.bills, self.orders, self.users)

        self.b = None
        self.o = None
        self.u = None
        self.i = None
        # UIC loads
        uic.loadUi('gui.ui', self)
        uic.loadUi('login_widget.ui', self.login_widget)
        uic.loadUi('stock_widget.ui', self.stock_widget)
        # Fill lists
        self.get_stock_list()
        # List select binding
        self.stock_widget.stock_list.currentItemChanged.connect(self.stock_select)
        # Initial hide
        self.stock_widget.hide()
        self.bills_widget.hide()
        self.order_widget.hide()
        # Menu buttons:
        self.stock_button.setEnabled(False)
        self.stock_button.clicked.connect(self.stock_menu)
        self.bills_button.setEnabled(False)
        self.bills_button.clicked.connect(self.bill_menu)
        self.orders_button.setEnabled(False)
        self.orders_button.clicked.connect(self.order_menu)
        # Widget buttons
        self.login_widget.login_button.clicked.connect(self.login)
        self.stock_widget.stock_delete_button.clicked.connect(self.stock_delete)
        self.stock_widget.stock_add_button.clicked.connect(self.stock_new)
        self.stock_widget.stock_item_save_button.clicked.connect(self.stock_edit)
        # Show GUI
        self.show()
    def stock_edit(self):
        self.i.name = self.stock_widget.stock_item_name_edit.text()
        self.i.code = self.stock_widget.stock_item_code_edit.text()
        self.i.price = float(self.stock_widget.stock_item_price_edit.text())
        self.i.dph = int(self.stock_widget.stock_item_dph_edit.text())
        self.i.count = int(self.stock_widget.stock_item_count_edit.text())
        self.i.mincount = int(self.stock_widget.stock_item_mincount_edit.text())
        self.i.weight = float(self.stock_widget.stock_item_weight_edit.text())
        self.i.is_age_restricted = bool(self.stock_widget.stock_item_is_age_restricted_edit.text())
        self.get_stock_list()
        Reader_Writer.write_item(self.i)
    def stock_new(self):
        self.stock.new("NEW ITEM", "", 0, 0, 0, 0, 0, False)
        self.get_stock_list()
    def closeEvent(self, event):
        Reader_Writer.write_all_and_clear(self.stock, self.bills, self.orders, self.users)
        Reader_Writer.close_connection()
    def get_stock_list(self):
        self.stock_widget.stock_list.clear()
        for item in self.stock:
            self.stock_widget.stock_list.addItem(item.name)
    def stock_delete(self):
        self.stock.delete(self.i.id)
        self.get_stock_list()
    def stock_select(self):
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
            self.stock_button.setEnabled(True)
            self.bills_button.setEnabled(True)
            self.orders_button.setEnabled(True)
            self.update()
    def stock_menu(self):
        self.bills_widget.hide()
        self.order_widget.hide()
        self.login_widget.hide()
        self.stock_widget.show()
    def bill_menu(self):
        self.stock_widget.hide()
        self.order_widget.hide()
        self.login_widget.hide()
        self.bills_widget.show()
    def order_menu(self):
        self.stock_widget.hide()
        self.bills_widget.hide()
        self.login_widget.hide()
        self.order_widget.show()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()