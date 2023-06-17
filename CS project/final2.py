from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import ImageTk,Image
import mysql.connector as con   


root=Tk()
app_width = 600
app_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2 ) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
#root.configure(bg='#F9F6EE')


frame_main = Frame(root,bg='#F9F6EE',width=app_width,height=app_height)
frame_main.place(x=0,y=0)



my_img=Image.open("hello2.jpeg")
my_img=my_img.resize((400,400), Image.ANTIALIAS)
my_img1 = ImageTk.PhotoImage(my_img)
my_label = Label(frame_main,image=my_img1,bg="red")
my_label.place(x= 100,y=50)



def nextpage():
    for widgets in frame_main.winfo_children():
        widgets.destroy()
    def connect():
        db = con.connect(
        database='project',

        host="localhost",
        user="root",
        password="Utkarsh123#"
        )
        return db

    
    def login(username, password):
        db=connect()
        cur=db.cursor()
        sql='select passkey from employees where employee_id = %s'
        cur.execute(sql,(username,))
        myresult=cur.fetchone()
        for i in myresult:
            if i==password:
                return myresult

    def manager(username):
        db=connect()
        cur=db.cursor()
        sql='select * from branch where branch_key=%i'%username
        cur.execute(sql)
        myresult=cur.fetchone()
        return myresult

    def login_page():
        for widgets in frame_main.winfo_children():
            widgets.destroy()
        my_img2=Image.open("login1.jpg")
        my_img2=my_img2.resize((200,100), Image.ANTIALIAS)
        my_img3 = ImageTk.PhotoImage(my_img2)
        my_label = Label(frame_main,image=my_img3,bg="#F9F6EE")
        my_label.place(x= 200,y=50)

        label_us=Label(frame_main,text='Username',font=("Times New Roman",20),fg="black")
        label_us.config(bg='#F9F6EE')
        label_us.place(x=150,y=160)
        entry_us=Entry(frame_main,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
        entry_us.place(x=280,y=160)

        label_pass=Label(frame_main,text='Password',font=("Times New Roman",20),fg="black")
        label_pass.config(bg='#F9F6EE')
        label_pass.place(x=150,y=200)
        entry_pass=Entry(frame_main,show="*",highlightcolor="black",highlightbackground = "black",highlightthickness=1)
        entry_pass.place(x=280,y=200)

        def loginnow():
            if entry_us.get().strip()=="" or entry_pass.get().strip()=="":
                messagebox.showwarning("showwarning", "All Fields are Important")
            else:
                try:
                    username=int(entry_us.get())
                except ValueError:
                    username=entry_us.get()
                password=entry_pass.get()
                if login(username, password)==None:
                    label_pass=Label(frame_main,text='*Incorrect Username or Password*',font=("Times New Roman",20),fg="red")
                    label_pass.config(bg='#F9F6EE')
                    label_pass.place(x=150,y=260)
                    entry_pass.delete(0,END)
                else:
                    def sidebar_buttons():
                        global items
                        global plus
                        global minus
                        global items_b
                        global add_b
                        global minus_b
                        global logout_b
                        
                        items = ImageTk.PhotoImage(Image.open('items.png').resize((40,40),Image.ANTIALIAS))
                        plus = ImageTk.PhotoImage(Image.open('plus.png').resize((40,40),Image.ANTIALIAS))
                        minus = ImageTk.PhotoImage(Image.open('minus.png').resize((40,40),Image.ANTIALIAS))
                        items_b = Button(frame_sidebar,image=items,command=display,bg='pink')
                        add_b = Button(frame_sidebar,image=plus,command=add_inventory,bg='pink')
                        minus_b = Button(frame_sidebar,image=minus,command=delete_inventory,bg='pink')
                        logout_b=Button(frame_sidebar,text="Exit",command=login_page,bg='pink')

                    def GetValue(event):
                        e1.delete(0, END)
                        e2.delete(0, END)
                        e3.delete(0, END)
                        row_id = Display_table.selection()[0]
                        select = Display_table.set(row_id)
                        e1.insert(0,select['name'])
                        e2.insert(0,select['salary'])
                        e3.insert(0,select['passkey'])

                    def GetValue2(event):
                        e5.delete(0, END)
                        e6.delete(0, END)
                        row_id = Display_table2.selection()[0]
                        select = Display_table2.set(row_id)
                        e5.insert(0,select['product_name'])
                        e6.insert(0,select['quantity'])

                    def GetValue3(event):
                        e8.delete(0, END)
                        e9.delete(0, END)
                        row_id = Display_table3.selection()[0]
                        select = Display_table3.set(row_id)
                        e8.insert(0,select['product_name'])
                        e9.insert(0,select['quantity'])
                        
                    def employee_box():
                        global Display_table
                        db=connect()
                        cur=db.cursor()
                        col_names = ('employee_id','name','salary','passkey')
                        col_text=['password','salary','name','employee_id']
                        Display_table = ttk.Treeview(frame_user, columns=col_names, show='headings')
                         
                        for column1 in col_names:
                            Display_table.column(column1,anchor=CENTER, stretch=NO, width=120)
                            Display_table.heading(column1, text=col_text.pop())
                            Display_table.place(x=10,y=300)
                                
                                
                        cur.execute("SELECT * FROM employees")
                        records = cur.fetchall()
                            
                        for i, (employee_id,name,salary,passkey) in enumerate(records):
                            Display_table.insert("", "end", values=(employee_id,name,salary,passkey))
                        
                        Display_table.bind('<Double-Button-1>',GetValue)
                        db.close()

                    def del_employees():
                        db=connect()
                        cur=db.cursor()

                        def find_emp(pname):
                            db=connect()
                            cur=db.cursor()
                            val=(pname,)
                            sql='select * from employees where name=%s'
                            cur.execute(sql,val)
                            myresult=cur.fetchone()
                            return myresult[0]

                        if e1.get().strip()=="" or e2.get().strip()=="" or e3.get().strip()=="":
                            messagebox.showwarning("showwarning", "All Fields are Important")
                        else:
                            pname = e1.get()
                            psalary = e2.get()
                            ppasskey = e3.get()
                            val=(pname,psalary,ppasskey)
                            if manager(find_emp(pname))==None:
                                val=(pname,psalary,ppasskey)
                                sql='delete from employees where name=%s and salary=%s and passkey=%s'
                                cur.execute(sql,val)
                                db.commit()
                                # messagebox.showinfo("Informantion", "Record Deleted Successfully...")
                            else:
                                r=manager(find_emp(pname))
                                print(r)
                                val=(int(r[2]),)
                                sql='delete from branch where manager_id=%i'%val
                                
                                cur.execute(sql)
                                db.commit()
                                sql='delete from employees where employee_id=%i'%val
                                cur.execute(sql)
                                db.commit()
                                # messagebox.showinfo("Informantion", "Record Deleted Successfully...")
    
                        messagebox.showinfo("Informantion", "Record Deleted Successfully...")   
                        employee_box()
                        e1.delete(0,END)
                        e2.delete(0,END)
                        e3.delete(0,END)
                        e1.focus_set()

                    def input_employees():
                        db=connect()
                        cur=db.cursor()
                        if e1.get().strip()=="" or e2.get().strip()=="" or e3.get().strip()=="":
                            messagebox.showwarning("showwarning", "All Fields are Important")
                        else:
                            pname = e1.get()
                            psalary= e2.get()
                            ppasskey = e3.get()

                            sql = "INSERT INTO employees(name,salary,passkey) VALUES (%s,%s, %s)"
                    
                            val = (pname,psalary,ppasskey)
                            cur.execute(sql, val)
                            db.commit()
                            messagebox.showinfo("Informantion", "Record Inserted Successfully...")
                        employee_box()
                        e1.delete(0,END)
                        e2.delete(0,END)
                        e3.delete(0,END)
                        e1.focus_set()

                    def item_update():
                        if e1.get().strip()=="" or e2.get().strip()=="" or e3.get().strip()=="":
                                    messagebox.showwarning("showwarning", "All Fields are Important")
                        else:
                            pname = e1.get()
                            psalary = e2.get()
                            ppasskey = e3.get()
                            val=(ppasskey,psalary,pname)
                            db=connect()
                            cur=db.cursor()
                            sql = "Update employees set passkey= %s,salary= %s where name= %s"
                            
                            cur.execute(sql, val)
                            db.commit()
                            messagebox.showinfo("information", "Record Updatd successfully...")
                        e1.delete(0, END)
                        e2.delete(0, END)
                        e3.delete(0, END)
                        e1.focus_set()
                        employee_box()

                    def display():
                            for widgets in frame_user.winfo_children():
                                widgets.destroy()
                            frame_user.update()
                            global e1
                            global e2
                            global e3
                            db=connect()
                            cur=db.cursor()

                            h1=Label(frame_user, text="EMPLOYEE", fg="pink", font=("Times New Roman", 24))
                            h1.config(bg='#F9F6EE')
                            h1.place(relx=0.5,y=20,anchor=CENTER)
                            sub1=Label(frame_user, text="Employee Name",font=("Times New Roman", 14))
                            sub1.config(bg='#F9F6EE')
                            sub1.place(x=70, y=80)
                            sub2=Label(frame_user, text="Salary",font=("Times New Roman", 14))
                            sub2.config(bg='#F9F6EE')
                            sub2.place(x=70, y=110)
                            sub3=Label(frame_user, text="Password",font=("Times New Roman", 14))
                            sub3.config(bg='#F9F6EE')
                            sub3.place(x=70, y=140)
                             
                            e1 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                            e1.place(x=200, y=80)
                             
                            e2 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                            e2.place(x=200, y=110)
                             
                            e3 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                            e3.place(x=200, y=140)
                             
                             
                            add_button=Button(frame_user, text="Add",command=input_employees,height=3, width= 13)
                            add_button.place(x=70, y=200)
                            update_button=Button(frame_user, text="Update",command=item_update,height=3, width= 13)
                            update_button.place(x=200, y=200)
                            delete_button=Button(frame_user, text="Delete",command=del_employees,height=3, width= 13)
                            delete_button.place(x=330, y=200)
                            db.close()
                            employee_box()
                
                    def add_TO_items():
                        global item_add
                        db=connect()
                        cur=db.cursor()
                        sql = "INSERT INTO items(product_name,price) VALUES (%s, %s)"
                        product_name,product_price=item_add,int(e10.get())
                        val = (product_name,product_price)
                        cur.execute(sql, val)
                        sql="insert into inventory(product_name,quantity) value (%s,%s)"
                        val=(product_name,0)
                        cur.execute(sql,val)
                        db.commit()
                        e10.delete(0,END)
                        for widgets in frame_user.winfo_children():
                            widgets.destroy()
                        frame_user.update()
                        add_inventory()


                    
                    def add_TO_inventory():
                        def find_inventory(product):
                            db=connect()
                            cur=db.cursor()
                            sql='select * from inventory where product_name=%s'

                            cur.execute(sql,(product,))
                            myresult=cur.fetchone()
                            return myresult


                        def update_quan(inventory_alter,quan_added):
                            db=connect()
                            cur=db.cursor()
                            product_no=inventory_alter[0]
                            inventory_quan=inventory_alter[2]+quan_added
                            val=(inventory_quan,product_no)
                            sql='''update inventory
                            set quantity=%s
                            where product_no=%i
                            '''%val
                            cur.execute(sql)
                            db.commit()
                            inventory_box()

                        if e5.get().strip()=="" or e6.get().strip()=="":
                            messagebox.showwarning("showwarning", "All Fields are Important")
                            e5.delete(0, END)
                            e6.delete(0, END)
                            e5.focus_set()
                            inventory_box()
                        else:
                            global item_add
                            global item_quantityA
                            item_add=e5.get()
                            item_quantityA=int(e6.get())
                            inventory_alter=find_inventory(item_add)
                            e5.delete(0, END)
                            e6.delete(0, END)
                            e5.focus_set()
                            inventory_box()
                        
                            if inventory_alter==None:
                                response=messagebox.askyesno("Information", "Do you wish to enter a new record?")
                                if response==1:
                                    for widgets in frame_user.winfo_children():
                                        widgets.destroy()
                                    frame_user.update()
                                    global e10
                                    db=connect()
                                    cur=db.cursor()
                                    h3=Label(frame_user, text="ADD NEW ITEM", fg="pink", font=("Times New Roman", 24))
                                    h3.config(bg='#F9F6EE')
                                    h3.place(relx=0.5,y=20,anchor=CENTER)
                                    
                                    sub10=Label(frame_user, text="Price",font=("Times New Roman", 14))
                                    sub10.config(bg='#F9F6EE')
                                    sub10.place(x=70, y=110)

                                    e10 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                                    e10.place(x=200, y=110)
                                        
                                    Button(frame_user, text="Add",command=add_TO_items,height=3, width= 13).place(x=150, y=200)
                                    db.close()
                                    inventory_box()
                            
                            else:
                                 update_quan(inventory_alter,item_quantityA)



                    def inventory_box():
                            db=connect()
                            cur=db.cursor()
                            global Display_table2
                            col_names = ('product_no', 'product_name', 'quantity')
                            col_text=["Quantity","Product Name","Product Number"]
                            Display_table2 = ttk.Treeview(frame_user, columns=col_names, show='headings')
                         
                            for column1 in col_names:
                                Display_table2.column(column1,anchor=CENTER, stretch=NO, width=100)
                                Display_table2.heading(column1, text=col_text.pop())
                                Display_table2.place(x=70,y=300)
                                
                                
                            cur.execute("SELECT * FROM inventory")
                            records = cur.fetchall()
                            
                            for i, (product_no,product_name,quantity) in enumerate(records):
                                Display_table2.insert("", "end", values=(product_no,product_name,quantity))
                            db.close()
                            Display_table2.bind('<Double-Button-1>',GetValue2)

                    def inventory_box2():
                        db=connect()
                        cur=db.cursor()
                        global Display_table3
                        col_names = ('product_no', 'product_name', 'quantity')
                        col_text=["Quantity","Product Name","Product Number"]
                        Display_table3 = ttk.Treeview(frame_user, columns=col_names, show='headings')
                        
                        for column1 in col_names:
                            Display_table3.column(column1,anchor=CENTER, stretch=NO, width=100)
                            Display_table3.heading(column1, text=col_text.pop())
                            Display_table3.place(x=70,y=300)
                            
                            
                        cur.execute("SELECT * FROM inventory")
                        records = cur.fetchall()
                        
                        for i, (product_no,product_name,quantity) in enumerate(records):
                            Display_table3.insert("", "end", values=(product_no,product_name,quantity))
                        db.close()
                        Display_table3.bind('<Double-Button-1>',GetValue3)

                    def add_inventory():
                            for widgets in frame_user.winfo_children():
                                widgets.destroy()
                            frame_user.update()

                        
                            global e5
                            global e6
                            db=connect()
                            cur=db.cursor()

                            h2=Label(frame_user, text="ADD TO INVENTORY", fg="pink", font=("Times New Roman", 24))
                            h2.config(bg='#F9F6EE')
                            h2.place(relx=0.5,y=20,anchor=CENTER)
                            
                            sub5=Label(frame_user, text="Product Name",font=("Times New Roman", 14))
                            sub5.config(bg='#F9F6EE')
                            sub5.place(x=70, y=110)
                            sub6=Label(frame_user, text="Quantity",font=("Times New Roman", 14))
                            sub6.config(bg='#F9F6EE')
                            sub6.place(x=70, y=140)
                             
                            
                             
                            e5 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                            e5.place(x=200, y=110)
                             
                            e6 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                            e6.place(x=200, y=140)
                             
                             
                            Button(frame_user, text="Add",command=add_TO_inventory,height=3, width= 13).place(x=150, y=200)
                            db.close()
                            inventory_box()

                    def remove_FROM_inventory():
                        def find_inventory(product):
                            # product=input('enter')
                            db=connect()
                            cur=db.cursor()
                            sql='select * from inventory where product_name=%s'

                            cur.execute(sql,(product,))
                            myresult=cur.fetchone()
                            return myresult
                        
                        def update_quan(inventory_alter,quan_added):
                            db=connect()
                            cur=db.cursor()
                            product_no=inventory_alter[0]
                            inventory_quan=inventory_alter[2]+quan_added
                            if inventory_quan<0:
                                messagebox.showwarning("showwarning", "Insufficient Quantity in Inventory")
                            else:
                                val=(inventory_quan,product_no)
                                sql='''update inventory
                                set quantity=%s
                                where product_no=%i
                                '''%val
                                
                                cur.execute(sql)
                                db.commit()
                            inventory_box2()
                    

                        def salary(username,product_name,item_quantityS):
                            db=connect()
                            cur=db.cursor()
                            sql='select * from items where product_name=%s'
                            cur.execute(sql,(product_name,))
                            item_details=cur.fetchone()
                            item_price=item_details[2]*abs(item_quantityS)
                            employee_commission=(15/100)*item_price

                            sql='select * from employees where employee_id=%i'%username
                            cur.execute(sql)
                            employee_details=cur.fetchone()
                            employee_salary=employee_details[2]+employee_commission

                            val=(employee_salary,username)
                            sql='''update employees
                            set salary=%i
                            where employee_id=%i
                            '''%val
                            cur.execute(sql)
                            db.commit()

                        if e8.get().strip()=="" or e9.get().strip()=="":
                            messagebox.showwarning("showwarning", "All Fields are Important")
                            e8.delete(0, END)
                            e9.delete(0, END)
                            e8.focus_set()
                            inventory_box2()
                        else:
                            item_subtract=e8.get()
                            item_quantityS=-(int(e9.get()))
                            inventory_alter=find_inventory(item_subtract)
                            update_quan(inventory_alter,item_quantityS)
                            salary(username,item_subtract,item_quantityS)
                            e8.delete(0, END)
                            e9.delete(0, END)
                            e8.focus_set()
                            inventory_box2()

                    def delete_inventory():
                            for widgets in frame_user.winfo_children():
                                widgets.destroy()
                            frame_user.update()


                            global e8
                            global e9
                            db=connect()
                            cur=db.cursor()

                            h3=Label(frame_user, text="REMOVE FROM INVENTORY", fg="pink", font=("Times New Roman", 24))
                            h3.config(bg='#F9F6EE')
                            h3.place(relx=0.5,y=20,anchor=CENTER)

                            sub8=Label(frame_user, text="Product Name",font=("Times New Roman", 14))
                            sub8.config(bg='#F9F6EE')
                            sub8.place(x=70, y=110)
                            sub9=Label(frame_user, text="Quantity",font=("Times New Roman", 14))
                            sub9.config(bg='#F9F6EE')
                            sub9.place(x=70, y=140)

                            e8 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                            e8.place(x=200, y=110)
                             
                            e9 = Entry(frame_user,highlightcolor="black",highlightbackground = "black",highlightthickness=1)
                            e9.place(x=200, y=140)
                             
                             
                            Button(frame_user, text="Delete",command=remove_FROM_inventory,height=3, width= 13).place(x=150, y=200)
                            db.close()
                            inventory_box2()

                            
                    if manager(username)==None:
                        for widgets in frame_main.winfo_children():
                            widgets.destroy()

                        frame_user = Frame(frame_main,bg='#F9F6EE',width=app_width-60,height=app_height)
                        frame_user.place(x=60,y=0)
                        frame_user.grid_propagate(False)

                        add_inventory()

                        frame_sidebar = Frame(frame_main,bg='pink',width=60,height=app_height)
                        frame_sidebar.place(x=0,y=0)
                        frame_sidebar.grid_propagate(False)

                        sidebar_buttons()



                        add_b.grid(row=0,column=0,padx=10,pady=10)
                        minus_b.grid(row=1,column=0,pady=10)
                        logout_b.grid(row=2,column=0,pady=400)
                        

                        
                    else:
                        for widgets in frame_main.winfo_children():
                            widgets.destroy()

                        frame_user = Frame(frame_main,bg='#F9F6EE',width=app_width-60,height=app_height)
                        frame_user.place(x=60,y=0)
                        frame_user.grid_propagate(False)

                        display()

                        frame_sidebar = Frame(frame_main,bg='pink',width=60,height=app_height)
                        frame_sidebar.place(x=0,y=0)
                        frame_sidebar.grid_propagate(False)

                        sidebar_buttons()

                        items_b.grid(row=0,column=0,pady=10,padx=10)
                        add_b.grid(row=1,column=0,pady=10)
                        minus_b.grid(row=2,column=0,pady=10)
                        logout_b.grid(row=3,column=0,pady=350)
                        

        Button(frame_main, text="Login Now", command=loginnow,background="pink").place(x=250,y=240)
        root.resizable(False, False)
        root.mainloop()


    login_page()


Button(frame_main, text="Continue", command=nextpage,background="pink",width=10,height=1,font=("Times New Roman",20)).place(x=250,y=500)

root.update_idletasks()
root.resizable(False, False)
frame_main.grid_propagate(False)
root.mainloop()
