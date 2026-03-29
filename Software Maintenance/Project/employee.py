from dataclasses import fields
from tkinter import*
#from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3

# ------------------ Employee Class ----------------------
class employeeClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg = "white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ Variables --------------
        variables = [
            "searchby", "searchtxt", "emp_id", "gender", "contact",
            "name", "dob", "doj", "email", "pass", "utype", "salary"
        ]

        for variable in variables:
            setattr(self, f"var_{variable}", StringVar())

        #---------- Search Frame -------------
        search_frame = LabelFrame(
            self.root,
            text="Search Employee",
            font=("goudy old style",12,"bold"),
            bd=2,relief=RIDGE,bg="white"
        )
        search_frame.place(x=250,y=20,width=600,height=70)

        #------------ Options ----------------
        cmb_search_employee = ttk.Combobox(
            search_frame,
            textvariable=self.var_searchby,
            values=("Select","Email","Name","Contact"),
            state='readonly',
            justify=CENTER,
            font=("goudy old style",15)
        )
        cmb_search_employee.place(x=10,y=10,width=180)
        cmb_search_employee.current(0)

        search_text_area = Entry(
            search_frame,
            textvariable=self.var_searchtxt,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=200,y=10)

        btn_search_employee = Button(
            search_frame,
            command=self.search,
            text="Search",
            font=("goudy old style",15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=410,y=9,width=150,height=30)

        #-------------- Layout ---------------
        title = Label(
            self.root,
            text="Employee Details",
            font=("goudy old style",15),
            bg="#0f4d7d",
            fg="white"
        ).place(x=50,y=100,width=1000)

        #---------- Row 1 ----------------
        employee_id_label = Label(
            self.root,
            text="Emp ID",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=150)

        employee_id_text_area = Entry(
            self.root,
            textvariable=self.var_emp_id,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=150,y=150,width=180)

        gender_label = Label(
            self.root,
            text="Gender",
            font=("goudy old style",15),
            bg="white"
        ).place(x=350,y=150)

        cmb_gender = ttk.Combobox(
            self.root,
            textvariable=self.var_gender,
            values=("Select","Male","Female","Other"),
            state='readonly',
            justify=CENTER,
            font=("goudy old style",15)
        )
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)

        contact_label = Label(
            self.root,
            text="Contact",
            font=("goudy old style",15),
            bg="white"
        ).place(x=750,y=150)

        contact_text_area = Entry(
            self.root,
            textvariable=self.var_contact,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=850,y=150,width=180)

        #---------- Row 2 ----------------
        employee_name_label = Label(
            self.root,
            text="Name",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=190)

        employee_name_text_area = Entry(
            self.root,
            textvariable=self.var_name,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=150,y=190,width=180)

        dob_label = Label(
            self.root,
            text="D.O.B.",
            font=("goudy old style",15),
            bg="white"
        ).place(x=350,y=190)

        dob_text_area = Entry(
            self.root,
            textvariable=self.var_dob,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=500,y=190,width=180)

        doj_label = Label(
            self.root,
            text="D.O.J.",
            font=("goudy old style",15),
            bg="white"
        ).place(x=750,y=190)

        doj_text_area = Entry(
            self.root,
            textvariable=self.var_doj,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=850,y=190,width=180)

        #---------- Row 3 ----------------
        email_label = Label(
            self.root,
            text="Email",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=230)

        email_text_area = Entry(
            self.root,
            textvariable=self.var_email,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=150,y=230,width=180)

        password_label = Label(
            self.root,
            text="Password",
            font=("goudy old style",15),
            bg="white"
        ).place(x=350,y=230)

        pasword_text_area = Entry(
            self.root,
            textvariable=self.var_pass,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=500,y=230,width=180)

        user_type_label = Label(
            self.root,
            text="User Type",
            font=("goudy old style",15),
            bg="white"
        ).place(x=750,y=230)

        cmb_user_type = ttk.Combobox(
            self.root,
            textvariable=self.var_utype,
            values=("Admin","Employee"),
            state='readonly',
            justify=CENTER,
            font=("goudy old style",15)
        )
        cmb_user_type.place(x=850,y=230,width=180)
        cmb_user_type.current(0)
        
        #---------- Row 4 ----------------
        address_label = Label(
            self.root,
            text="Address",
            font=("goudy old style",15),
            bg="white"
        ).place(x=50,y=270)

        self.txt_address = Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60)

        salary_label = Label(
            self.root,
            text="Salary",
            font=("goudy old style",15),
            bg="white"
        ).place(x=500,y=270)

        salary_text_area = Entry(
            self.root,
            textvariable=self.var_salary,
            font=("goudy old style",15),
            bg="lightyellow"
        ).place(x=600,y=270,width=180)
        
        #-------------- Buttons -----------------
        btn_add_employee = Button(
            self.root,
            text="Save",
            command=self.add,
            font=("goudy old style",15),
            bg="#2196f3",
            fg="white",
            cursor="hand2"
        ).place(x=500,y=305,width=110,height=28)

        btn_update_employee = Button(
            self.root,
            text="Update",
            command=self.update,
            font=("goudy old style",15),
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        ).place(x=620,y=305,width=110,height=28)

        btn_delete_employee = Button(
            self.root,
            text="Delete",
            command=self.delete,
            font=("goudy old style",15),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        ).place(x=740,y=305,width=110,height=28)

        btn_clear_employee = Button(
            self.root,
            text="Clear",
            command=self.clear,
            font=("goudy old style",15),
            bg="#607d8b",
            fg="white",
            cursor="hand2"
        ).place(x=860,y=305,width=110,height=28)

        #------------ Employee Information -------------
        emp_frame = Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly = Scrollbar(emp_frame,orient=VERTICAL)
        scrollx = Scrollbar(emp_frame,orient=HORIZONTAL)\
        
        self.EmployeeTable = ttk.Treeview(
            emp_frame,
            columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        #------------ Employee Table -------------
        table_columns = [
            ("eid", "EMP ID", 90),
            ("name", "Name", 100),
            ("email", "Email", 100),
            ("gender", "Gender", 100),
            ("contact", "Contact", 100),
            ("dob", "D.O.B", 100),
            ("doj", "D.O.J", 100),
            ("pass", "Password", 100),
            ("utype", "User Type", 100),
            ("address", "Address", 100),
            ("salary", "Salary", 100),
        ]

        self.EmployeeTable["columns"] = [col[0] for col in table_columns]
        self.EmployeeTable["show"] = "headings"

        for col_id, text, width in table_columns:
            self.EmployeeTable.heading(col_id, text=text)
            self.EmployeeTable.column(col_id, width=width)
        
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

 # ------------------ Functions----------------------
    
    # Function to connect to the database
    def connect(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        return con, cur
    
    # Function to add an employee
    def add(self):
        con, cur = self.connect()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error","Employee ID must be required",parent = self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","This Employee ID is already assigned",parent = self.root)
                else:
                    cur.execute("insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent = self.root)
                    self.clear()
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Function to display all employees in the table
    def show(self):
        con, cur = self.connect()
        try:
            cur.execute("select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values = row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Function to get employee information
    def get_data(self,event):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']

        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])
    
    # Function to update employee information
    def update(self):
        con, cur = self.connect()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error","Employee ID must be required",parent = self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Employee ID",parent = self.root)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Function to delete an employee
    def delete(self):
        con, cur = self.connect()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error","Employee ID must be required",parent = self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Employee ID",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?",parent = self.root)
                    if op == True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent = self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()

    # Function to clear the input fields
    def clear(self):
        defaults = {
            "gender": "Select",
            "utype": "Admin",
            "searchby": "Select",
        }

        for variable in [
            "searchby", "searchtxt", "emp_id", "gender", "contact",
            "name", "dob", "doj", "email", "pass", "utype", "salary"
        ]:
            value = defaults.get(variable, "")
            getattr(self, f"var_{variable}").set(value)

        self.txt_address.delete('1.0', END)
        self.show()

    # Function to search employees
    def search(self):
        con, cur = self.connect()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error","Select Search By option",parent = self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Search input should be required",parent = self.root)
            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()