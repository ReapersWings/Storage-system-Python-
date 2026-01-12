import tkinter;
import sqlite3;
from tkinter import ttk
class connect_database():
    def __init__(self):
        self.dbconn = sqlite3.connect("my_database.db")
        self.conn = self.dbconn.cursor()
        self.conn.execute("""CREATE TABLE IF NOT EXISTS storage_quantity(
            `quantity_id` INT PRIMARY KEY AUTO_INCREMENT,
            `quantity` VARCHAR(255) NOT NULL
            )""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS storage_product(
            `product_id` INT PRIMARY KEY AUTO_INCREMENT,
            `product_name` VARCHAR(255) NOT NULL,
            `category_id` INT(255) NOT NULL,
            `type_quantity` VARCHAR(10) NOT NULL,
            `product_quantity` float NOT NULL,
            FOREGIN KEY (`type_quantity`) REFERENCES storage_quantity(`quantity_id`)
            )""")
        self.dbconn.commit()
        
    def insert_product(self,newdata):
        try:
            self.conn.execute(f"INSERT INTO `storage_product`(`product_name`,`category_id`,`type_quantity`,`product_quantity`) VALUES ('{newdata[0].upper()}',{newdata[1]},'{newdata[2]}',{newdata[3]})")
            self.dbconn.commit()
        except:
            self.dbconn.rollback()
        
    def update_product(self,newdata,target_id):
        try:
            self.conn.execute(f"UPDATE `storage_product` SET `product_name`='{newdata[0].upper()}',`category_id`={newdata[1]},`type_quantity`='{newdata[2]}',`product_quantity`={newdata[3]} WHERE `product_id`={target_id}")
            self.dbconn.commit()
        except:
            self.dbconn.rollback()
        
    def delete_product(self,target_id):
        try:
            self.conn.execute(f"DELETE FROM `storage_product` WHERE `product_id`={target_id}")
            self.dbconn.commit()
        except:
            self.dbconn.rollback()
            
            
    
    def insert_quantity(self,newdata):
        try:
            self.conn.execute(f"INSERT INTO `storage_quantity`(`quantity`) VALUES ('{newdata}')")
            self.dbconn.commit()
        except:
            self.dbconn.rollback()
        
    def update_quantity(self,newdata,target_id):
        try:
            self.conn.execute(f"UPDATE `storage_quantity` SET `quantity`='{newdata}' WHERE `quantity_id`={target_id}")
            self.dbconn.commit()
        except:
            self.dbconn.rollback()
        
    def delete_quantity(self,target_id):
        try:
            self.conn.execute(f"DELETE FROM `storage_quantity` WHERE `quantity_id`={target_id}")
            self.dbconn.commit()
        except:
            self.dbconn.rollback()
        
    
        
class storage:
    def __init__(self):
        self.storage = tkinter.Tk()
        self.table = ttk.Treeview()
        
        self.storage.mainloop()