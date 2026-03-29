from tkinter import*
# from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

# ------------------ Product Class ----------------------
class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg = "white")
        self.root.resizable(False,False)
        self.root.focus_force()
        
        #----------- Variables -------------
        self.var_category = StringVar()
        self.category_list = []
        self.supplier_list = []
        self.fetch_category_supplier()

        self.var_product_id = StringVar()
        self.var_supplier = StringVar()
        self.var_product_name = StringVar()
        self.var_product_price = StringVar()
        self.var_product_quantity = StringVar()
        self.var_product_status = StringVar()
        self.var_searchby = StringVar()
        self.var_search_text_area = StringVar()

        product_Frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #------------ Layout --------------
        title = Label(
            product_Frame,
            text="Manage Product Details",
            font=("goudy old style",18),
            bg="#0f4d7d",
            fg="white"
        ).pack(side=TOP,fill=X)

        category_label = Label(
            product_Frame,
            text="Category",
            font=("goudy old style",18),
            bg="white"
        ).place(x=30,y=60)

        supplier_label = Label(
            product_Frame,
            text="Supplier",
            font=("goudy old style",18),
            bg="white"
        ).place(x=30,y=110)

        product_name_label = Label(
            product_Frame,
            text="Name",
            font=("goudy old style",18),
            bg="white"
        ).place(x=30,y=160)

        name_text_area = Entry(
            product_Frame,
            textvariable=self.var_product_name,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=150,y=160,width=200)

        product_price_label = Label(
            product_Frame,
            text="Price",
            font=("goudy old style",18),
            bg="white"
        ).place(x=30,y=210)

        price_text_area = Entry(
            product_Frame,
            textvariable=self.var_product_price,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=150,y=210,width=200)

        product_quantity_label = Label(
            product_Frame,
            text="Quantity",
            font=("goudy old style",18),
            bg="white"
        ).place(x=30,y=260)

        quantity_text_area = Entry(
            product_Frame,
            textvariable=self.var_product_quantity,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=150,y=260,width=200)

        product_status_label = Label(
            product_Frame,
            text="Status",
            font=("goudy old style",18),
            bg="white"
        ).place(x=30,y=310)

        cmb_category = ttk.Combobox(
            product_Frame,
            textvariable=self.var_category,
            values=self.category_list,
            state='readonly',
            justify=CENTER,
            font=("goudy old style",15)
        )
        cmb_category.place(x=150,y=60,width=200)
        cmb_category.current(0)

        cmb_supplier = ttk.Combobox(
            product_Frame,
            textvariable=self.var_supplier,
            values=self.supplier_list,
            state='readonly',
            justify=CENTER,
            font=("goudy old style",15)
        )
        cmb_supplier.place(x=150,y=110,width=200)
        cmb_supplier.current(0)

        cmb_status = ttk.Combobox(
            product_Frame,
            textvariable=self.var_product_status,
            values=("Active","Inactive"),
            state='readonly',
            justify=CENTER,
            font=("goudy old style",15)
        )
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        #-------------- Buttons -----------------
        btn_add_product = Button(
            product_Frame,
            text="Save",
            command=self.add,
            font=("goudy old style",15),
            bg="#2196f3",
            fg="white",
            cursor="hand2"
        ).place(x=10,y=400,width=100,height=40)

        btn_update_product = Button(
            product_Frame,
            text="Update",
            command=self.update,
            font=("goudy old style",15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=120,y=400,width=100,height=40)

        btn_delete_product = Button(
            product_Frame,
            text="Delete",
            command=self.delete,
            font=("goudy old style",15),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        ).place(x=230,y=400,width=100,height=40)

        btn_clear_product = Button(
            product_Frame,
            text="Clear",
            command=self.clear,
            font=("goudy old style",15),
            bg="#607d8b",
            fg="white",
            cursor="hand2"
        ).place(x=340,y=400,width=100,height=40)

        #---------- Search Frame -------------
        search_frame = LabelFrame(
            self.root,
            text="Search Product",
            font=("goudy old style",12,"bold"),
            bd=2,
            relief=RIDGE,
            bg="white"
        )
        search_frame.place(x=480,y=10,width=600,height=80)

        #------------ Options ----------------
        cmb_search = ttk.Combobox(
            search_frame,
            textvariable=self.var_searchby,
            values=("Select","Category","Supplier","Name"),
            state='readonly',
            justify=CENTER,
            font=("goudy old style",15)
        )
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        search_text = Entry(
            search_frame,
            textvariable=self.var_search_text_area,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=200,y=10)

        btn_search_product = Button(
            search_frame,
            text="Search",
            command=self.search,
            font=("goudy old style",15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=410,y=9,width=150,height=30)

        #------------ Product Information -------------
        product_frame = Frame(self.root,bd=3,relief=RIDGE)
        product_frame.place(x=480,y=100,width=600,height=390)

        scrolly = Scrollbar(product_frame,orient=VERTICAL)
        scrollx = Scrollbar(product_frame,orient=HORIZONTAL)\
        
        self.ProductTable = ttk.Treeview(
            product_frame,
            columns=("pid","Category","Supplier","name","price","qty","status"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        table_columns = [
            ("pid", "P ID", 90),
            ("Category", "Category", 100),
            ("Supplier", "Supplier", 100),
            ("name", "Name", 100),
            ("price", "Price", 100),
            ("qty", "Quantity", 100),
            ("status", "Status", 100)
        ]

        self.ProductTable["columns"] = [col[0] for col in table_columns]
        self.ProductTable["show"] = "headings"

        for col_id, text, width in table_columns:
            self.ProductTable.heading(col_id, text=text)
            self.ProductTable.column(col_id, width=width)
        
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.tag_configure('low_quantity', background='#fff3cd')
        self.ProductTable.tag_configure('high_quantity', background='#d4edda')
        self.ProductTable.tag_configure('inactive_status', background='#f8d7da')
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        self.fetch_category_supplier()


# ------------------ Functions----------------------

    # Function to connect to the database
    def connect(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        return con, cur
    
    # Function for fetching categories and their suppliers
    def fetch_category_supplier(self):
        self.category_list.append("Empty")
        self.supplier_list.append("Empty")
        
        con, cur = self.connect()

        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.category_list[:]
                self.category_list.append("Select")
                for i in cat:
                    self.category_list.append(i[0])
            cur.execute("select name from supplier")
            sup = cur.fetchall()

            if len(sup)>0:
                del self.supplier_list[:]
                self.supplier_list.append("Select")
                for i in sup:
                    self.supplier_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Adding a new product
    def add(self):
        con, cur = self.connect()
        try:
            if self.var_category.get() == "Select" or self.var_category.get() == "Empty" or self.var_supplier == "Select" or self.var_supplier == "Empty":
                messagebox.showerror("Error","All fields are required",parent = self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_product_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","Product already present",parent = self.root)
                else:
                    cur.execute("insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                        self.var_category.get(),
                        self.var_supplier.get(),
                        self.var_product_name.get(),
                        self.var_product_price.get(),
                        self.var_product_quantity.get(),
                        self.var_product_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully",parent = self.root)
                    self.clear()
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Displaying products
    def show(self):
        con, cur = self.connect()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                quantity = int(row[5])
                status = row[6]

                # First check activity status, then check quantity to determine the appropriate tag
                if status == "Inactive":
                    self.ProductTable.insert('', END, values=row, tags=('inactive_status',))
                elif quantity <= 3:
                    self.ProductTable.insert('', END, values = row, tags = ('low_quantity',))
                else:
                    self.ProductTable.insert('', END, values = row, tags=('high_quantity',))

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Displaying selected product details in the input fields
    def get_data(self,event):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_product_id.set(row[0])
        self.var_category.set(row[1])
        self.var_supplier.set(row[2])
        self.var_product_name.set(row[3])
        self.var_product_price.set(row[4])
        self.var_product_quantity.set(row[5])
        self.var_product_status.set(row[6])

    # Updating a product
    def update(self):
        con, cur = self.connect()
        try:
            if self.var_product_id.get() == "":
                messagebox.showerror("Error","Please select product from list",parent = self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_product_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Product",parent = self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                        self.var_category.get(),
                        self.var_supplier.get(),
                        self.var_product_name.get(),
                        self.var_product_price.get(),
                        self.var_product_quantity.get(),
                        self.var_product_status.get(),
                        self.var_product_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully",parent = self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Deleting a product
    def delete(self):
        con, cur = self.connect()
        try:
            if self.var_product_id.get() == "":
                messagebox.showerror("Error","Select Product from the list",parent = self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_product_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Product",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?",parent = self.root)
                    if op == True:
                        cur.execute("delete from product where pid=?",(self.var_product_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent = self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Clearing the input fields
    def clear(self):
        self.var_category.set("Select")
        self.var_supplier.set("Select")
        self.var_product_name.set("")
        self.var_product_price.set("")
        self.var_product_quantity.set("")
        self.var_product_status.set("Active")
        self.var_product_id.set("")
        self.var_searchby.set("Select")
        self.var_search_text_area.set("")

        self.show()

    # Searching a product
    def search(self):
        con, cur = self.connect()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error","Select Search By option",parent = self.root)
            elif self.var_search_text_area.get() == "":
                messagebox.showerror("Error","Search input should be required",parent = self.root)
            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_search_text_area.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values = row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent = self.root)
    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()