from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_DIR, exist_ok=True)

# ------------------ Dashboard Class ----------------------
class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg = "white")

        self.icon_title = PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
        
        #------------- Layout --------------
        title = Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        ).place(x=0, y=0, relwidth=1, height=70)

        btn_logout = Button(
            self.root, text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow", cursor="hand2"
        ).place(x=1150, y=10, height=50, width=150)

        self.label_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=("times new roman", 15),
            bg="#4d636d", fg="white"
        )
        self.label_clock.place(x=0, y=70, relwidth=1, height=30)

        self.MenuLogo = Image.open(os.path.join(IMAGE_DIR, "menu_im.png"))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo.resize((200, 200)))

        self.LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.LeftMenu.place(x=0, y=102, width=200, height=565)

        menulogo_label = Label(
            self.LeftMenu, 
            image=self.MenuLogo
        ).pack(side=TOP, fill=X)

        menu_label = Label(
            self.LeftMenu, 
            text="Menu",
            font=("times new roman", 20),
            bg="#009688"
        ).pack(side=TOP, fill=X)
        self.icon_side = PhotoImage(file=os.path.join(IMAGE_DIR, "side.png"))

        #----------------- Buttons ---------------------
        menu_items = [
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Products", self.product),
            ("Sales", self.sales),
            ("Exit", self.root.destroy)
        ]

        for text, cmd in menu_items:
            Button(
                self.LeftMenu, text=text, command=cmd,
                image=self.icon_side, compound=LEFT,
                padx=5, anchor="w",
                font=("times new roman", 20, "bold"),
                bg="white", bd=3, cursor="hand2"
            ).pack(side=TOP, fill=X)

        # ----------- Content ----------------
        self.dashboard_boxes = {}
        box_info = [
            ("Employee", "#33bbf9", 300, 120),
            ("Supplier", "#ff5722", 650, 120),
            ("Category", "#009688", 1000, 120),
            ("Product", "#607d8b", 300, 300),
            ("Sales", "#ffc107", 650, 300)
        ]
        for name, color, x, y in box_info:
            lbl = Label(
                self.root, text=f"Total {name}\n{{ 0 }}",
                bd=5, relief=RIDGE, bg=color, fg="white",
                font=("goudy old style", 20, "bold")
            )
            lbl.place(x=x, y=y, height=150, width=300)
            self.dashboard_boxes[name.lower()] = lbl

        # ------------ Footer -----------------
        footer_label = Label(
            self.root,
            text="IMS-Inventory Management System",
            font=("times new roman", 12),
            bg="#4d636d", fg="white"
        ).pack(side=BOTTOM, fill=X)

        self.update_content()

    # -------------- Modules ----------------
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

# ------------------ Functions----------------------

    # Function to display count of records in dashboard boxes
    def get_count(self, cursor, table):
        cursor.execute(f"SELECT * FROM {table}")
        return len(cursor.fetchall())

    # Function to update dashboard content
    def update_content(self):
        con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()

        try:
            self.dashboard_boxes["product"].config(
                text = f"Total Product\n[ {self.get_count(cur, 'product')} ]"
            )
            self.dashboard_boxes["category"].config(
                text = f"Total Category\n[ {self.get_count(cur, 'category')} ]"
            )
            self.dashboard_boxes["employee"].config(
                text = f"Total Employee\n[ {self.get_count(cur, 'employee')} ]"
            )
            self.dashboard_boxes["supplier"].config(
                text = f"Total Supplier\n[ {self.get_count(cur, 'supplier')} ]"
            )

            self.dashboard_boxes["sales"].config(
                text = f"Total Sales\n[ {len(os.listdir(BILL_DIR))} ]"
            )

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.label_clock.config(
                text = f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )

            self.label_clock.after(200, self.update_content)

        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent = self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
