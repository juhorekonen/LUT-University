from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

# ------------------ Category Class ----------------------
class categoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg = "white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #--------------- Variables ------------------
        self.var_category_id = StringVar()
        self.var_category_name = StringVar()

        #--------------- Layout ---------------------
        title = Label(
            self.root,
            text="Manage Product Category",
            font=("goudy old style",30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        ).pack(side=TOP,fill=X,padx=10,pady=20)
        
        description = Label(
            self.root,
            text="Enter Category Name",
            font=("goudy old style",30),
            bg="white"
        ).place(x=50,y=100)

        text_area = Entry(
            self.root,
            textvariable=self.var_category_name,
            bg="lightyellow",
            font=("goudy old style",18)
        ).place(x=50,y=170,width=300)

        btn_add_category = Button(
            self.root,
            text="ADD",
            command=self.add,
            font=("goudy old style",15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=360,y=170,width=150,height=30)

        btn_delete_category = Button(
            self.root,
            text="Delete",
            command=self.delete,
            font=("goudy old style",15),
            bg="red",
            fg="white",
            cursor="hand2"
        ).place(x=520,y=170,width=150,height=30)

        #------------ Category Information -----------
        information_frame = Frame(self.root,bd=3,relief=RIDGE)
        information_frame.place(x=700,y=100,width=380,height=100)

        scrolly = Scrollbar(information_frame,orient=VERTICAL)
        scrollx = Scrollbar(information_frame,orient=HORIZONTAL)\
        
        self.CategoryTable = ttk.Treeview(
            information_frame,
            columns=("cid","name"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid",text="C ID")
        self.CategoryTable.heading("name",text="Name")
        self.CategoryTable["show"]="headings"

        self.CategoryTable.column("cid",width=90)
        self.CategoryTable.column("name",width=100)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

        #----------------- Images ---------------------
        self.first_image = Image.open("images/cat.jpg").resize((500,250))
        self.first_image = ImageTk.PhotoImage(self.first_image)

        self.label_first_image = Label(
            self.root,
            image=self.first_image,
            bd=2,
            relief=RAISED
        ).place(x=50,y=220)

        self.second_image = Image.open("images/category.jpg").resize((500,250))
        self.second_image = ImageTk.PhotoImage(self.second_image)

        self.label_second_image = Label(
            self.root,
            image=self.second_image,
            bd=2,
            relief=RAISED
        ).place(x=580,y=220)

    
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

    # Adding a category
    def add(self):
        if self.var_category_name.get() == "":
            messagebox.showerror("Error","Category Name must be required",parent = self.root)
            return
        
        result = self.connect(
            "SELECT * FROM category WHERE name=?", 
            (self.var_category_name.get(),), 
            fetch = True
        )

        if result:
            messagebox.showerror("Error","Category already present",parent = self.root)
        else: 
            self.connect(
                "INSERT INTO category(name) VALUES (?)", 
                (self.var_category_name.get(),)
            )
            messagebox.showinfo("Success","Category added successfully",parent = self.root)
            self.clear()
            self.show()
    
    # Displaying categories in the table
    def show(self):
        rows = self.connect("SELECT * FROM category", fetch = True) or []
        self.CategoryTable.delete(*self.CategoryTable.get_children())
        for row in rows:
            self.CategoryTable.insert("", END, values = row)

    # Clearing the input fields
    def clear(self):
        self.var_category_name.set("")
        self.var_category_id.set("")
        self.show()

    # Displaying selected category in the input fields
    def get_data(self, event):
        selected = self.CategoryTable.focus()
        values = self.CategoryTable.item(selected)["values"]
        if values:
            self.var_category_id.set(values[0])
            self.var_category_name.set(values[1])

    # Deleting a category
    def delete(self):
        if self.var_category_id.get() == "":
            messagebox.showerror("Error", "Category name must be required", parent = self.root)
            return
        
        result = self.connect(
            "SELECT * FROM category WHERE cid=?",
            (self.var_category_id.get(),),
            fetch = True
        )

        if not result:
            messagebox.showerror("Error", "Invalid Category Name", parent = self.root)
            return

        confirm = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
        if confirm:
            self.connect(
                "DELETE FROM category WHERE cid=?",
                (self.var_category_id.get(),)
            )
            messagebox.showinfo("Success", "Category Deleted Successfully", parent = self.root)
            self.clear()


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
