from tkinter import *
from PIL import ImageTk,Image
import mysql.connector as con   
import tkinter as tk



def connect():
    db = con.connect(
    database='project',

    host="localhost",
    user="root",
    password="Utkarsh123#"
    )
    return db
employees_table='''create table employees (
    employee_id INT primary key auto_increment,
    name varchar(20) not null ,
    branch_key int,
    salary int,
    passkey varchar(9)
    );
    '''
branch_table='''create table branch (
    branch_key int primary key auto_increment,
    name varchar(20) not null,
    manager_id int default null,
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id) 

);
'''
clients_table='''create table clients (
    client_id int primary key auto_increment,
    client_name varchar(20) unique,
    sales int default 0,
    employee_id int,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) 

);
'''

items_table='''create table items (
    product_no int primary key auto_increment,
    product_name varchar(20) unique,
    price int

);'''

inventory_table='''create table inventory (
    product_no int primary key auto_increment,
    product_name varchar(20) unique,
    quantity int,
    FOREIGN KEY (product_no) REFERENCES items(product_no),
    FOREIGN KEY (product_name) REFERENCES items(product_name)

);'''
def create_table(a):
    db=connect()
    cur=db.cursor()
    cur.execute(a)
    db.commit()
    db.close()
list_table=[employees_table,branch_table,clients_table,items_table,inventory_table]

# for table_name in list_table:
#     create_table(table_name)

def input_employees():
    db=connect()
    cur=db.cursor()

    sql = "INSERT INTO employees(name,branch_key,salary,passkey) VALUES (%s, %s,%s, %s)"
    name,branch_key,salary,passkey=input('name of employee'),input('branch key'),input('salary'),input('password')
    val = (name,branch_key,salary,passkey)
    cur.execute(sql, val)
    db.commit()

def input_branch():
    db=connect()
    cur=db.cursor()

    sql = "INSERT INTO branch(name) VALUES (%s)"
    name=input('name of branch')
    val = (name)
    cur.execute(sql, val)
    db.commit()
    
def add_TO_items():
    db=connect()
    cur=db.cursor()
    sql = "INSERT INTO items(product_name,price) VALUES (%s, %s)"
    product_name,product_price=input('name of product'),input('price of product')
    val = (product_name,product_price)
    cur.execute(sql, val)
    sql="insert into inventory(product_name,quantity) value (%s,%s)"
    val=(product_name,0)
    cur.execute(sql,val)
    db.commit()

def input_items():
    db=connect()
    cur=db.cursor()
    sql = "INSERT INTO items(product_name,price) VALUES (%s, %s)"
    product_name,product_price=input('name of product'),input('price of product')
    val = (product_name,product_price)
    cur.execute(sql, val)
    sql="insert into inventory(product_name,quantity) value (%s,%s)"
    val=(product_name,0)
    cur.execute(sql,val)
    db.commit()


def input_clients():
    db=connect()
    cur=db.cursor()
    sql = "INSERT INTO clients(client_id,client_name,employee_id) VALUES (%s, %s,%s)"
    client_id,client_name,employee_id=input('client id'),input('client name'), input('employee id')
    val = (client_id,client_name,employee_id)
    cur.execute(sql, val)
    db.commit()

# for i in range(3):
#     input_clients()

def login(username, password):
    db=connect()
    cur=db.cursor()
    sql='select * from employees where employee_id = %s and passkey=%s'
    cur.execute(sql,[username,password])
    myresult=cur.fetchone()
    return myresult

def manager(username):
    db=connect()
    cur=db.cursor()
    sql='select * from branch where branch_key=%i'%username
    cur.execute(sql)
    myresult=cur.fetchone()
    return myresult

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
    val=(inventory_quan,product_no)
    sql='''update inventory
    set quantity=%s
    where product_no=%i
    '''%val
    
    cur.execute(sql)
    db.commit()

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
    employee_salary=employee_details[3]+employee_commission

    val=(employee_salary,username)
    sql='''update employees
    set salary=%i
    where employee_id=%i
    '''%val

    cur.execute(sql)
    db.commit()

def display(table_name):
    db=connect()
    cur=db.cursor()
    sql='select * from %s'%table_name
    cur.execute(sql)
    myresult=cur.fetchall()
    return myresult

def removeFrom_Table(table_name,id_name,id):
    db=connect()
    cur=db.cursor()
    val=(table_name,id_name, id)
    sql='delete from %s where %s=%i'%val
    
    cur.execute(sql)
    db.commit()
    db.close()


    username=int(input('enter username'))
    password=input('enter password')

    def loginnow():
        if login(username, password)==None:
            print('incorrect password')

        else:
            login_process=login(username, password)
            if manager(username)==None:
                print('employee')
                button_emp=input('enter a or s if you want to add or remove in inventory')
                if button_emp=='a':
                    item_add=input('enter name of item you want to add')
                    item_quantityA=int(input('enter quantity you want to add'))
                    inventory_alter=find_inventory(item_add)

                    update_quan(inventory_alter,item_quantityA)
                
                if button_emp=='s':
                    item_subtract=input('enter name of item you want to subtract')
                    item_quantityS=int(input('enter quantity you want to subtract'))
                    inventory_alter=find_inventory(item_subtract)

                    update_quan(inventory_alter,item_quantityS)

                    salary(username,item_subtract,item_quantityS)


                

            else:
                
                button_man=input('Enter c, e or b if you want to access clients employees or branch respectively')
                if button_man=='c':
                    table_name='clients'
                    print(display(table_name))
                    ask_man=input('Enter a or r if you want to add or remove a client')
                    if ask_man=='a':
                        input_clients()
                    elif ask_man=='r':
                        man_clientID=input('enter client id')
                        removeFrom_Table(man_clientID,table_name='clients',id_name='client_id')
                    else:
                        print('enter correct')
                elif button_man=='e':
                    table_name='employees'
                    print(display(table_name))
                    ask_man=input('Enter a or r if you want to add or remove an employee')
                    if ask_man=='a':
                        input_employees()
                    elif ask_man=='r':
                        man_employeeID=input('enter employee id')
                        removeFrom_Table(man_employeeID,table_name='employees',id_name='employee_id')
                    else:
                        print('enter correct')
                
                elif button_man=='b':
                    table_name='branch'
                    print(display(table_name))
                    ask_man=input('Enter a or r if you want to add or remove an employee')
                    if ask_man=='a':
                        input_branch()
                    elif ask_man=='r':
                        man_branchID=input('enter employee id')
                        removeFrom_Table(man_branchID,table_name='branch',id_name='branch_id')
                    else:
                        print('enter correct')
    

    



