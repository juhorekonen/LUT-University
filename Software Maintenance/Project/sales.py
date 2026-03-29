from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
# import sqlite3
import os

# ------------------ Path Setup ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BILL_DIR = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_DIR, exist_ok=True)


# ------------------ Sales Class ----------------------
class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg = "white")
        self.root.resizable(False, False)
        self.root.focus_force()

        #--------------- Variables ---------------------
        self.bill_list = []
        self.var_invoice = StringVar()

        # --------------- Layout ---------------------
        title = Label(
            self.root,
            text="View Customer Bills",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=20)

        invoice_label = Label(
            self.root, 
            text="Invoice No.", 
            font=("times new roman", 15), 
            bg="white"
        ).place(x=50, y=100)

        invoice_text_area = Entry(
            self.root, 
            textvariable=self.var_invoice, 
            font=("times new roman", 15), 
            bg="lightyellow"
        ).place(x=160, y=100, width=180, height=28)

        btn_search_sales = Button(
            self.root, text="Search", command=self.search,
            font=("times new roman", 15, "bold"),
            bg="#2196f3", fg="white", cursor="hand2"
        ).place(x=360, y=100, width=120, height=28)

        btn_clear_sales = Button(
            self.root, text="Clear", command=self.clear,
            font=("times new roman", 15, "bold"),
            bg="lightgray", cursor="hand2"
        ).place(x=490, y=100, width=120, height=28)

        # ----------------- Bill list -------------------
        sales_frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_frame, orient=VERTICAL)
        self.Sales_List = Listbox(
            sales_frame, font=("goudy old style", 15),
            bg="white", yscrollcommand=scrolly.set
        )
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # --------------- Bill Information ----------------------
        bill_frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_frame.place(x=280, y=140, width=410, height=330)

        bill_area_title = Label(
            bill_frame, text="Customer Bill Area",
            font=("goudy old style", 20), bg="orange"
        ).pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_frame, orient=VERTICAL)
        self.bill_area = Text(bill_frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # ------------- Image -----------------
        self.bill_photo = Image.open("images/cat2.jpg").resize((450,300))
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        label_image = Label(
            self.root, 
            image=self.bill_photo, 
            bd=0
        ).place(x=700, y=110)

        self.show()


 # ------------------ Functions----------------------

    # Function to read file 
    def read_file(self, file_path):
        self.bill_area.delete('1.0', END)
        with open(file_path, 'r') as fp:
            self.bill_area.insert(END, fp.read())

    # Function to display all bills in the listbox
    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0, END)

        for i in os.listdir(BILL_DIR):
            if i.split('.')[-1] == 'txt':
                self.Sales_List.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    # Function to get bill information
    def get_data(self, event):
        index_ = self.Sales_List.curselection()
        if not index_:
            return

        file_name = self.Sales_List.get(index_)
        file_path = os.path.join(BILL_DIR, file_name)
        self.read_file(file_path)

    # Function to search bills
    def search(self):
        invoice = self.var_invoice.get()
        if invoice == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent = self.root)
        elif invoice in self.bill_list:
            file_path = os.path.join(BILL_DIR, f"{self.var_invoice.get()}.txt")
            self.read_file(file_path)
        else:
            messagebox.showerror("Error", "Invalid Invoice No.", parent = self.root)

    # Function to clear the bill area
    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
