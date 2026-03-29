from tkinter import*
#from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

# ------------------ Supplier Class ----------------------
class supplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg = "white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ Variables --------------
        self.var_searchby = StringVar()
        self.var_search_text_area = StringVar()
        self.var_supplier_invoice = StringVar()
        self.var_supplier_name = StringVar()
        self.var_supplier_contact = StringVar()
        
        
        #---------- Search Frame -------------
        search_title = Label(
            self.root,
            text="Invoice No.",
            bg="white",
            font=("goudy old style",15)
        ).place(x=700,y=80)

        search_text = Entry(
            self.root,
            textvariable=self.var_search_text_area,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=850,y=80,width=160)

        btn_search_supplier = Button(
            self.root,
            command=self.search,
            text="Search",
            font=("goudy old style",15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=980,y=79,width=100,height=28)

        #-------------- Layout ---------------
        title = Label(
            self.root,
            text="Supplier Details",
            font=("goudy old style",20,"bold"),
            bg="#0f4d7d",
            fg="white"
        ).place(x=50,y=10,width=1000,height=40)

        #-------------- Content ---------------
        supplier_invoice = Label(
            self.root,
            text="Invoice No.",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=80)

        invoice_text_area = Entry(
            self.root,
            textvariable=self.var_supplier_invoice,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=180,y=80,width=180)

        supplier_name = Label(
            self.root,
            text="Name",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=120)

        name_text_area = Entry(
            self.root,
            textvariable=self.var_supplier_name,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=180,y=120,width=180)

        supplier_contact = Label(
            self.root,
            text="Contact",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=160)

        contact_text_area = Entry(
            self.root,
            textvariable=self.var_supplier_contact,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=180,y=160,width=180)

        supplier_description = Label(
            self.root,
            text="Description",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=200)

        self.description_text_area = Text(
            self.root,
            font=("goudy old style",15),
            bg="lightyellow"
        )
        self.description_text_area.place(x=180,y=200,width=470,height=120)
        
        #-------------- Buttons -----------------
        btn_add_supplier = Button(
            self.root,
            text="Save",
            command=self.add,
            font=("goudy old style",15),
            bg="#2196f3",
            fg="white",
            cursor="hand2"
        ).place(x=180,y=370,width=110,height=35)

        btn_update_supplier = Button(
            self.root,
            text="Update",
            command=self.update,
            font=("goudy old style",15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=300,y=370,width=110,height=35)

        btn_delete_supplier = Button(
            self.root,
            text="Delete",
            command=self.delete,
            font=("goudy old style",15),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        ).place(x=420,y=370,width=110,height=35)

        btn_clear_supplier = Button(
            self.root,
            text="Clear",
            command=self.clear,
            font=("goudy old style",15),
            bg="#607d8b",
            fg="white",
            cursor="hand2"
        ).place(x=540,y=370,width=110,height=35)

        #------------ Supplier Information -------------
        sup_frame = Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=700,y=120,width=380,height=350)

        scrolly = Scrollbar(sup_frame,orient=VERTICAL)
        scrollx = Scrollbar(sup_frame,orient=HORIZONTAL)\
        
        self.SupplierTable = ttk.Treeview(
            sup_frame,
            columns=("invoice","name","contact","desc"),
            yscrollcommand=scrolly.set,xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice",text="Invoice")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")
        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=100)
        
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()


# ------------------ Functions----------------------

    # Database connection
    def connect(self, query, params = (), fetch = False):
        con = sqlite3.connect(database = r'ims.db')
        cur = con.cursor()
        try:
            cur.execute(query, params)
            con.commit()
            if fetch:
                return cur.fetchall()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to : {str(e)}", parent = self.root)
        finally:
            con.close()

            
    # Adding a new supplier
    def add(self):
        if self.var_supplier_invoice.get() == "":
            messagebox.showerror("Error", "Invoice must be required", parent = self.root)
            return

        result = self.connect(
            "Select * from supplier where invoice=?",
            (self.var_supplier_invoice.get(),),
            fetch = True
        )

        if result:
            messagebox.showerror("Error", "Invoice no. is already assigned", parent = self.root)
        else:
            self.connect(
                "insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",
                (
                    self.var_supplier_invoice.get(),
                    self.var_supplier_name.get(),
                    self.var_supplier_contact.get(),
                    self.description_text_area.get('1.0', END),
                )
            )
            messagebox.showinfo("Success", "Supplier Added Successfully", parent = self.root)
            self.clear()

    # Displaying all suppliers
    def show(self):
        rows = self.connect("select * from supplier", fetch = True) or []
        self.SupplierTable.delete(*self.SupplierTable.get_children())
        for row in rows:
            self.SupplierTable.insert('', END, values=row)

    # Displaying selected supplier in the input fields
    def get_data(self, event):
        selected = self.SupplierTable.focus()
        row = self.SupplierTable.item(selected)["values"]
        if row:
            self.var_supplier_invoice.set(row[0])
            self.var_supplier_name.set(row[1])
            self.var_supplier_contact.set(row[2])
            self.description_text_area.delete('1.0', END)
            self.description_text_area.insert(END, row[3])

    # Updating a supplier
    def update(self):
        if self.var_supplier_invoice.get() == "":
            messagebox.showerror("Error", "Invoice must be required", parent = self.root)
            return

        result = self.connect(
            "Select * from supplier where invoice=?",
            (self.var_supplier_invoice.get(),),
            fetch = True
        )

        if not result:
            messagebox.showerror("Error", "Invalid Invoice No.", parent = self.root)
        else:
            self.connect(
                "update supplier set name=?,contact=?,desc=? where invoice=?",
                (
                    self.var_supplier_name.get(),
                    self.var_supplier_contact.get(),
                    self.description_text_area.get('1.0', END),
                    self.var_supplier_invoice.get(),
                )
            )
            messagebox.showinfo("Success", "Supplier Updated Successfully", parent = self.root)
            self.show()

    # Deleting a supplier
    def delete(self):
        if self.var_supplier_invoice.get() == "":
            messagebox.showerror("Error","Invoice No. must be required",parent = self.root)
            return

        result = self.connect(
            "SELECT * FROM supplier WHERE invoice=?",
            (self.var_supplier_invoice.get(),),
            fetch=True
        )

        if not result:
            messagebox.showerror("Error","Invalid Invoice No.",parent = self.root)
        
        else:
            op = messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
            if op:
                self.connect(
                    "DELETE FROM supplier WHERE invoice=?",
                    (self.var_supplier_invoice.get(),)
                )
                messagebox.showinfo("Deleted","Supplier Deleted Successfully",parent = self.root)
                self.clear()
                self.show()

    # Clearing the input fields
    def clear(self):
        self.var_supplier_invoice.set("")
        self.var_supplier_name.set("")
        self.var_supplier_contact.set("")
        self.description_text_area.delete('1.0',END)
        self.var_search_text_area.set("")
        self.show()

    # Searching a supplier
    def search(self):
        if self.var_search_text_area.get() == "":
            messagebox.showerror("Error","Invoice No. should be required",parent = self.root)
            return
       
        result = self.connect(
            "SELECT * FROM supplier WHERE invoice=?",
            (self.var_search_text_area.get(),),
            fetch = True
        )
       
        if result:
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in result:
                self.SupplierTable.insert('',END,values = row)
        else:
            messagebox.showerror("Error","No record found!!!",parent = self.root)


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()