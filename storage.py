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
                query+=f"`storage_product`.`product_name` LIKE '{search['name'].upper()}'"
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
            self.alert.error("Search product Failed!")
            return False
        
    def insert_product(self,newdata):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_name`='{newdata[0].upper()}'")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"INSERT INTO `storage_product`(`product_name`,`category_id`,`type_quantity`,`product_quantity`) VALUES ('{newdata[0].upper()}',{newdata[1]},'{newdata[2]}',{newdata[3]})")
                self.dbconn.commit()
                self.alert.successfull("This product add successfull!")
                return True
            else:
                self.alert.error("This product already added!")
                return False
        except:
            self.alert.error("Add product Failed!")
            self.dbconn.rollback()
            return False
        
    def update_product(self,newdata,target_id):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_name`='{newdata}' AND `product_id`!={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1:
                self.conn.execute(f"UPDATE `storage_product` SET `product_name`='{newdata[0].upper()}',`category_id`={newdata[1]},`type_quantity`='{newdata[2]}',`product_quantity`={newdata[3]} WHERE `product_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This product edit successfull!")
                return True
            else:
                self.alert.error("This product already edited!")
                return False
        except:
            self.alert.error("Edit product Failed!")
            self.dbconn.rollback()
            return False
        
    def delete_product(self,target_id):
        try:
            self.conn.execute(f"SELECT `product_id` FROM `storage_product`WHERE `product_id`={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"DELETE FROM `storage_product` WHERE `product_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This product delete successfull!")
                return True
            else:
                self.alert.error("This product already deleted!")
                return False
        except:
            self.alert.error("Delete product Failed!")
            self.dbconn.rollback()
            return False
            
    def list_diff_type_quantity(self):
        try:
            self.conn.execute("SELECT `type_quantity` ,COUNT(`product_id`) FROM `storage_product` GROUP BY `type_quantity`")
            return self.conn.fetchall()
        except:
            self.alert.error("Search product Failed!")
            return False
            
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
            self.alert.error("Search Category Failed!")
            return False
    
    def insert_category(self,newdata):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category`='{newdata}'")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"INSERT INTO `storage_category`(`category`) VALUES ('{newdata}')")
                self.dbconn.commit()
                self.alert.successfull("This category add successfull!")
                return True
            else:
                self.alert.error("This category already added!")
                return False
        except:
            self.alert.error("Add category Failed!")
            self.dbconn.rollback()
            return False
        
    def update_category(self,newdata,target_id):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category`='{newdata}' AND `category_id`!={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1:
                self.conn.execute(f"UPDATE `storage_category` SET `category`='{newdata}' WHERE `category_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This category Edit successfull!")
                return True
            else:
                 self.alert.error("This category already edited!")
                 return False
        except:
            self.alert.error("Edit category Failed!")
            self.dbconn.rollback()
            return False
        
    def delete_category(self,target_id):
        try:
            self.conn.execute(f"SELECT `category_id` FROM `storage_category`WHERE `category_id`={target_id}")
            result=self.conn.fetchall()
            if len(result) < 1 :
                self.conn.execute(f"DELETE FROM `storage_category` WHERE `category_id`={target_id}")
                self.dbconn.commit()
                self.alert.successfull("This category delete successfull!")
                return True
            else:
                self.alert.error("This category already deleted!")
                return False
        except:
            self.alert.error("Delete category Failed!")
            self.dbconn.rollback()
            return False
        
    
class alert:
    def __init__(self):
        if hasattr(self, "window") and self.window.winfo_exists():
            self.window.destroy
        
    def error(self,alert):
        self.window = tkinter.Tk()
        self.window.title("Error")
        label = tkinter.Label(self.window,text=alert)
        label.pack()
        button = tkinter.Button(self.window,text="Ok",command=self.window.destroy)
        button.pack()
        self.window.mainloop()
        
    def successfull(self,alert):
        self.window = tkinter.Tk()
        self.window.title("Success")
        label=tkinter.Label(self.window,text=alert)
        label.pack()
        button = tkinter.Button(self.window,text="Ok",command=self.window.destroy)
        button.pack()
        self.window.mainloop()
        
class storage:
    def __init__(self):
        self.inputvalue={}
        self.dbconn=connect_database()
        self.window_effect = window_effect()
        self.set_condition = condition_set()
        
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
        self.treeview_refresh()
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
        self.option_category ={}
        all_category = self.dbconn.search_category([])
        if self.set_condition.result_query_search(all_category) :
            for category in all_category:
                self.option_category[category[1]]=category[0]
        else:
            self.option_category=[]
            
        print(self.option_category)
        tkinter.Label(div_search,text="Category:").pack()
        self.product_category_var = tkinter.StringVar()
        category_select = ttk.Combobox(div_search,
                    textvariable=self.product_category_var,
                    values=list(self.option_category.keys())
                    )
        category_select.pack()
        
        ##Type Quantity Search
        option_type_quantity=self.dbconn.list_diff_type_quantity()
        if self.set_condition.result_query_search(option_type_quantity) :
            option_type_quantity=self.dbconn.list_diff_type_quantity()
        else:
            option_type_quantity=[]
        print(option_type_quantity)
        tkinter.Label(div_search,text="Type Quantity:").pack()
        self.product_type_quantity_var = tkinter.StringVar()
        type_quantity_select = ttk.Combobox(div_search,
                     textvariable=self.product_type_quantity_var,
                     values=option_type_quantity
                     )
        type_quantity_select.pack()

        button = tkinter.Button( div_search,text="Search", command=self.button_search_product,width=16)
        button.pack()
        
        div_effect = tkinter.LabelFrame(
            div,
            bd=3,
            relief="solid",
            text="Effect Product :",
            padx=10,
            pady=10
        )
        div_effect.pack(fill="both",side="bottom")
        
        button = tkinter.Button( div_effect,text="Add product", command=self.window_effect.window_add_product ,width=16)
        button.pack()
        
        self.storage.mainloop()
        
    def button_search_product(self):
        self.inputvalue["name"]=self.product_name_var.get()
        self.inputvalue["type_quantity"]=self.product_type_quantity_var.get()
        self.inputvalue["category"]=self.option_category[self.product_category_var.get()]
        self.treeview_refresh()
        
    def treeview_refresh(self):
        self.table.delete(*self.table.get_children())
        alldata=self.dbconn.search_product(self.inputvalue)
        if self.set_condition.result_query_search(alldata):
            print(self.dbconn.search_product(self.inputvalue))
            if len(alldata) >0: 
                count=1
                for data in alldata:
                    self.table.insert("","end",text=f"count" ,values=(data[0],data[1],data[4],data[2],data[3]))
                    count+=1
        

class window_effect:
    def __init__(self):
        self.dbconn = connect_database()
        self.inputvalue=[]
        self.condition_set = condition_set()
        
    def window_add_product(self):
        if hasattr(self,"window_add") and self.window_add.winfo_exists:
            self.window_add.destroy()
            del self.window_add
        self.window_add = tkinter.Tk()
        self.window_add.title("Add Product")
        div_effect = tkinter.LabelFrame(
            self.window_add,
            bd=3,
            relief="solid",
            text="Add Product :",
            padx=10,
            pady=10
        )
        div_effect.pack(fill="both",side="top")
        
        self.product_name_var = tkinter.StringVar()
        tkinter.Label(div_effect,text="Product Name:").pack()
        product_name = tkinter.Entry(div_effect , textvariable=self.product_name_var)
        product_name.pack()
        error_product = tkinter.Label(div_effect,fg="red").pack()
        
        self.option_category ={}
        all_category = self.dbconn.search_category([])
        if self.condition_set.result_query_search(all_category):
            for category in all_category:
                self.option_category[category[1]]=category[0]
            
            print(self.option_category)
            tkinter.Label(div_effect,text="Category:").pack()
            self.product_category_var = tkinter.StringVar()
            category_select = ttk.Combobox(div_effect,
                        textvariable=self.product_category_var,
                        values=list(self.option_category.keys()),
                        state="readonly"
                        )
            category_select.pack()
            error_category = tkinter.Label(div_effect,fg="red").pack()
        else:
            self.window_add.destroy()
        
        option_type_quantity=self.dbconn.list_diff_type_quantity()
        if self.condition_set.result_query_search(option_type_quantity) :
            tkinter.Label(div_effect,text="Type Quantity:").pack()
            self.product_type_quantity_var = tkinter.StringVar()
            type_quantity_select = ttk.Combobox(div_effect,
                        textvariable=self.product_type_quantity_var,
                        values=option_type_quantity
                        )
            type_quantity_select.pack()
            error_type_quantity = tkinter.Label(div_effect,fg="red").pack()
        else:
            self.window_add.destroy()
        
        self.quantity_var = tkinter.StringVar()
        tkinter.Label(div_effect,text="Quantity :").pack()
        Quantity = tkinter.Entry(div_effect , textvariable=self.quantity_var)
        Quantity.pack()
        error_quantity = tkinter.Label(div_effect,fg="red").pack()
        
        if hasattr(self,"window_add_error_warning") and len(self.window_add_error_warning) >0 :
            # combobox style
            style = ttk.Style()
            style.configure(
                "Red.TCombobox",
                bordercolor="red",
                lightcolor="red",
                darkcolor="red"
            )
            if "product_name" in self.window_add_error_warning:
                self.product_name_var.set(self.old_value[0])
                product_name['highlightthickness']=2
                #product_name['highlightbackground']="red"
                product_name['highlightcolor']="red"
                error_product['text']=self.window_add_error_warning['product_name']
                
            if "category" in self.window_add_error_warning:
                category_select['style']="Red.TCombobox"
                self.product_category_var.set(self.old_value[1])
                error_category['text']=self.window_add_error_warning['category']
                
            if "type_quantity" in self.window_add_error_warning:
                type_quantity_select['style']="Red.TCombobox"
                self.product_type_quantity_var.set(self.old_value[2])
                error_type_quantity['text']=self.window_add_error_warning['type_quantity']
                
            if "quantity" in self.window_add_error_warning:
                product_name['highlightthickness']=2
                #product_name['highlightbackground']="red"
                product_name['highlightcolor']="red"
                self.quantity_var.set(self.old_value[3])
                error_quantity['text']=self.window_add_error_warning['quantity']
                
            del self.window_add_error_warning
        
        button =tkinter.Button(div_effect, text="Insert", command=self.f_insert_product ,width=16)
        button.pack()
        
        self.window_add.mainloop()
    
    def f_insert_product(self):
        self.window_add_error_warning={}
        error_count = 0
        self.old_value=[]
        
        self.old_value.append(self.product_name_var.get())
        self.old_value.append(self.product_category_var.get())
        self.old_value.append(self.product_type_quantity_var.get())
        self.old_value.append(self.quantity_var.get())
        
        if   self.product_name_var.get() == "":
            self.inputvalue.append(self.product_name_var.get())
        else:
            self.window_add_error_warning['product_name']='please input the product name !'
            error_count+=1
            
        if self.product_category_var.get() != "":
            self.inputvalue.append(self.option_category[self.product_category_var.get()])
        else:
            self.window_add_error_warning['category']='please input the category !'
            error_count+=1
            
        if self.product_type_quantity_var.get() != "":
            self.inputvalue.append(self.product_type_quantity_var.get())
        else:
            self.window_add_error_warning['type_quantity']='please input the type quantity !'
            error_count+=1
            
        if self.quantity_var.get() != "":
            if self.condition_set.in_numeric(self.quantity_var.get()):
                self.inputvalue.append(float(self.quantity_var.get()))
            else:
                self.window_add_error_warning['quantity']='textbox quantity is number !' 
        else:
            self.window_add_error_warning['quantity']='please input the quantity !'
            error_count+=1
        
        if error_count < 0 :
            result = self.dbconn.insert_product(self.inputvalue)
            if result :
                self.window_add.destroy()
            else:
                self.window_add_product()
        elif error_count > 0:
            self.window_add_product()
                
        
class condition_set:
    def in_numeric(string):
        try:
            float(string)
            return True
        except:
            return False
        
    def result_query_search(result):
        if isinstance(result, (list, tuple, set)):
            return True
        else:
            return False
    
window = storage()
window.main_window()