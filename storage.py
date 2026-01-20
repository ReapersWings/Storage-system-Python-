import tkinter;
import sqlite3;
from tkinter import ttk

class connect_database():
    def __init__(self):
        self.alert = alert()
        
        self.dbconn = sqlite3.connect("my_database.db")
        self.conn = self.dbconn.cursor()
        self.conn.execute("""CREATE TABLE IF NOT EXISTS storage_category(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category VARCHAR(255) NOT NULL
            )""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS storage_product(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            type_quantity TEXT NOT NULL,
            product_quantity REAL NOT NULL,
            FOREIGN KEY (category_id) REFERENCES storage_category(category_id)
            )""")
        self.dbconn.commit()
        
    
    ## query product
    
    def search_product(self,search):
        try:
            query = """SELECT 
                        `storage_product`.`product_id`,
                        `storage_product`.`product_name`,
                        `storage_product`.`type_quantity`,
                        `storage_product`.`product_quantity`,
                        `storage_category`.`category` 
                        FROM `storage_product`INNER JOIN `storage_category` ON `storage_product`.`category_id` =`storage_category`.`category_id`"""
            lenresult = len(search)
            count = 1
            
            if lenresult > 0:
                query+=' WHERE '
                
            if "name" in search:
                query+=f"`storage_product`.`product_name` LIKE '{search['name']}'"
                if count < lenresult:
                    query+=' AND '
                count+=1
            
            if "type_quantity" in search:
                query+=f"`storage_product`.`type_quantity`='{search['type_quantity']}'"
                if count < lenresult:
                    query+=' AND '
                count+=1
            
            if "category" in search:
                query+=f"`storage_product`.`category_id`={search['category']}"
                count+=1
            
            self.conn.execute(query)
            return self.conn.fetchall()
        except:
            self.alert.error("Find product Failed!")
        
    def insert_product(self,newdata):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_name`='{newdata[0].upper()}'")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"INSERT INTO `storage_product`(`product_name`,`category_id`,`type_quantity`,`product_quantity`) VALUES ('{newdata[0].upper()}',{newdata[1]},'{newdata[2]}',{newdata[3]})")
                self.dbconn.commit()
                self.alert.successfull("This product add successfull!")
            else:
                self.alert.error("This product already added!")
        except:
            self.alert.error("Add product Failed!")
            self.dbconn.rollback()
        
    def update_product(self,newdata,target_id):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_name`='{newdata}' AND `product_id`!={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1:
                self.conn.execute(f"UPDATE `storage_product` SET `product_name`='{newdata[0].upper()}',`category_id`={newdata[1]},`type_quantity`='{newdata[2]}',`product_quantity`={newdata[3]} WHERE `product_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This product edit successfull!")
            else:
                self.alert.error("This product already edited!") 
        except:
            self.alert.error("Edit product Failed!")
            self.dbconn.rollback()
        
    def delete_product(self,target_id):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_id`={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"DELETE FROM `storage_product` WHERE `product_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This product delete successfull!")
            else:
                self.alert.error("This product already deleted!")
        except:
            self.alert.error("Delete product Failed!")
            self.dbconn.rollback()
            
        
            
    ## query category
    
    def search_category(self,search):
        try:
            query = """SELECT 
                        `category_id`,`category` 
                        FROM `storage_category`"""
            lenresult = len(search)
            count = 1
            
            if lenresult > 0:
                query+=' WHERE '
                
            if "name" in search:
                query+=f"`category` LIKE '{search['name']}'"
            
            self.conn.execute(query)
            return self.conn.fetchall()
        except:
            self.alert.error("Find category Failed!")
    
    def insert_category(self,newdata):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category`='{newdata}'")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"INSERT INTO `storage_category`(`category`) VALUES ('{newdata}')")
                self.dbconn.commit()
                self.alert.successfull("This category add successfull!")
            else:
                self.alert.error("This category already added!")
        except:
            self.alert.error("Add category Failed!")
            self.dbconn.rollback()
        
    def update_category(self,newdata,target_id):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category`='{newdata}' AND `category_id`!={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1:
                self.conn.execute(f"UPDATE `storage_category` SET `category`='{newdata}' WHERE `category_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This category Edit successfull!")
            else:
                 self.alert.error("This category already edited!")
        except:
            self.alert.error("Edit category Failed!")
            self.dbconn.rollback()
        
    def delete_category(self,target_id):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category_id`={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"DELETE FROM `storage_category` WHERE `category_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This category delete successfull!")
            else:
                self.alert.error("This category already deleted!")
        except:
            self.alert.error("Delete category Failed!")
            self.dbconn.rollback()
        
    
class alert:
    def __init__(self):
        self.window = tkinter.Tk()
        
    def error(self,alert):
        self.window.title("Error")
        label = tkinter.Label(self.window,label=alert)
        label.pack()
        button = tkinter.Button(self.window,text="Ok",command=self.window.destroy)
        button.pack()
        self.window.mainloop()
        
    def successfull(self,alert):
        self.window.title("Success")
        label = tkinter.Label(self.window,label=alert)
        label.pack()
        button = tkinter.Button(self.window,text="Ok",command=self.window.destroy)
        button.pack()
        self.window.mainloop()
    
        
class storage:
    def __init__(self):
        self.inputvalue={}
        self.dbconn=connect_database()
        
    def main_window(self):
        self.storage = tkinter.Tk()
        self.table = ttk.Treeview(self.storage)
        self.table['columns']=("Id","product","category","type_quantity","product_quantity")
        self.table.heading("#0",text="No.")
        self.table.heading("Id",text="ID")
        self.table.heading("product",text="Product")
        self.table.heading("category",text="Category")
        self.table.heading("type_quantity",text="Type Quantity")
        self.table.heading("product_quantity",text="Quantity")
        alldata=self.dbconn.search_product(self.inputvalue)
        print(self.dbconn.search_product(self.inputvalue))
        if len(alldata) >0: 
            count=1
            for data in alldata:
                self.table.insert("","end",text=f"count" ,values=(data[0],data[1],data[4],data[2],data[3]))
                count+=1
        self.table.pack(fill="both",side="left")
        
        div=tkinter.Frame(
            self.storage,
            bd=3,
            relief="solid",
            padx=12,
            pady=12
        )
        div.pack(fill="both",side="right")
        
        div_search = tkinter.LabelFrame(
            div,
            bd=3,
            relief="solid",
            text="Search Product :",
            padx=10,
            pady=10
        )
        div_search.pack(fill="both",side="top")
        
        ## Product search
        self.product_name_var = tkinter.StringVar()
        tkinter.Label(div_search,text="Product Name:").pack()
        product_name_search = tkinter.Entry(div_search , textvariable=self.product_name_var)
        product_name_search.pack()
        
        ##Category search
        option_category ={}
        all_category = self.dbconn.search_category([])
        for category in all_category:
            option_category[category[1]]=category[0]
        
        print(option_category)
        tkinter.Label(div_search,text="Category:").pack()
        self.product_category_var = tkinter.StringVar()
        category_select = ttk.Combobox(div_search,
                     textvariable=self.product_category_var,
                     values=list(option_category.keys())
                     )
        category_select.pack()
        
        ##Type Quantity Search
        option_type_quantity={}
        
        print(option_type_quantity)
        tkinter.Label(div_search,text="Type Quantity:").pack()
        self.product_type_quantity_var = tkinter.StringVar()
        type_quantity_select = ttk.Combobox(div_search,
                     textvariable=self.product_type_quantity_var,
                     values=option_type_quantity
                     )
        type_quantity_select.pack()


        button = tkinter.Button( div_search,text="Search", command=self.button_search_product )
        button.pack()
        
        self.storage.mainloop()
        
    def button_search_product(self):
        self.inputvalue["name"]=self.product_name_var.get()
        self.inputvalue["type_quantity"]=self.product_type_quantity_var.get()
        self.inputvalue["category"]=self.product_category_var.get()
        self.dbconn.search_product(self.inputvalue)
        

    
    
window = storage()
window.main_window()