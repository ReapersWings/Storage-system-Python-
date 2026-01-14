import tkinter;
import sqlite3;
from tkinter import ttk
class connect_database():
    def __init__(self):
        self.dbconn = sqlite3.connect("my_database.db")
        self.conn = self.dbconn.cursor()
        self.conn.execute("""CREATE TABLE IF NOT EXISTS storage_category(
            `category_id` INT PRIMARY KEY AUTO_INCREMENT,
            `category` VARCHAR(255) NOT NULL
            )""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS storage_product(
            `product_id` INT PRIMARY KEY AUTO_INCREMENT,
            `product_name` VARCHAR(255) NOT NULL,
            `category_id` INT(255) NOT NULL,
            `type_quantity` VARCHAR(10) NOT NULL,
            `product_quantity` float NOT NULL,
            FOREGIN KEY (`category_id`) REFERENCES storage_category(`category_id`)
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
                        FROM `product_quantity`INNER JOIN `storage_quantity` ON `storage_product`.`category_id` =`storage_category`.`category_id` WHERE"""
            lenresult = len(search)
            count = 1
            
            if lenresult == 0:
                query+='0'
                
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
                query+=f"`storage_category`.`category`='{search['category']}'"
                count+=1
            
            self.conn.execute(query)
            return self.conn.fetchall()
        except:
            alert.error("Add product Failed!")
        
    def insert_product(self,newdata):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_name`='{newdata[0].upper()}'")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"INSERT INTO `storage_product`(`product_name`,`category_id`,`type_quantity`,`product_quantity`) VALUES ('{newdata[0].upper()}',{newdata[1]},'{newdata[2]}',{newdata[3]})")
                self.dbconn.commit()
                alert.successfull("This product add successfull!")
            else:
                alert.error("This product already added!")
        except:
            alert.error("Add product Failed!")
            self.dbconn.rollback()
        
    def update_product(self,newdata,target_id):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_name`='{newdata}' AND `product_id`!={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1:
                self.conn.execute(f"UPDATE `storage_product` SET `product_name`='{newdata[0].upper()}',`category_id`={newdata[1]},`type_quantity`='{newdata[2]}',`product_quantity`={newdata[3]} WHERE `product_id`={target_id}")
                self.dbconn.commit()
                alert.successfull("This product edit successfull!")
            else:
                alert.error("This product already edited!") 
        except:
            alert.error("Edit product Failed!")
            self.dbconn.rollback()
        
    def delete_product(self,target_id):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_id`={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"DELETE FROM `storage_product` WHERE `product_id`={target_id}")
                self.dbconn.commit()
                alert.successfull("This product delete successfull!")
            else:
                alert.error("This product already deleted!")
        except:
            alert.error("Delete product Failed!")
            self.dbconn.rollback()
            
        
            
    ## query category
    
    def insert_category(self,newdata):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category`='{newdata}'")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"INSERT INTO `storage_category`(`category`) VALUES ('{newdata}')")
                self.dbconn.commit()
                alert.successfull("This category add successfull!")
            else:
                alert.error("This category already added!")
        except:
            alert.error("Add category Failed!")
            self.dbconn.rollback()
        
    def update_category(self,newdata,target_id):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category`='{newdata}' AND `category_id`!={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1:
                self.conn.execute(f"UPDATE `storage_category` SET `category`='{newdata}' WHERE `category_id`={target_id}")
                self.dbconn.commit()
                alert.successfull("This category Edit successfull!")
            else:
                 alert.error("This category already edited!")
        except:
            alert.error("Edit category Failed!")
            self.dbconn.rollback()
        
    def delete_category(self,target_id):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category_id`={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"DELETE FROM `storage_category` WHERE `category_id`={target_id}")
                self.dbconn.commit()
                alert.successfull("This category delete successfull!")
            else:
                alert.error("This category already deleted!")
        except:
            alert.error("Delete category Failed!")
            self.dbconn.rollback()
        
    
class alert:
    def __init__(self):
        self.window = tkinter.Tk()
        
    def error(self,alert):
        self.window.title("Error")
        label = tkinter.Label(self.window,label=alert)
        label.pack()
        button = tkinter.Button(self.window,text="Ok",command=self.window.destroy())
        button.pack()
        self.window.mainloop()
        
    def successfull(self,alert):
        self.window.title("Success")
        label = tkinter.Label(self.window,label=alert)
        label.pack()
        button = tkinter.Button(self.window,text="Ok",command=self.window.destroy())
        button.pack()
        self.window.mainloop()
    
        
class storage:
    def __init__(self):
        self.storage = tkinter.Tk()
        self.table = ttk.Treeview()
        
        self.storage.mainloop()