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
        
    def id_search_product(self , target_id):
        try:
            self.conn.execute(f"""SELECT 
                        `storage_product`.`product_name`,
                        `storage_product`.`type_quantity`,
                        `storage_product`.`product_quantity`,
                        `storage_category`.`category` 
                        FROM `storage_product`INNER JOIN `storage_category` ON `storage_product`.`category_id` =`storage_category`.`category_id` WHERE `storage_product`.`product_id`={target_id}""")
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
        if hasattr(self , "storage") and self.storage.winfo_exists :
            self.storage.destroy()
            self.inputvalue={}
            del self.category_name_var
            
        self.storage = tkinter.Tk()
        
        selection_plece=tkinter.Frame(
            self.storage,
            padx=25,
            pady=12
        )
        selection_plece.pack(fill="both",side="top")
        
        button_category = tkinter.Button(selection_plece,text="Category",command=self.window_category , width=25)
        button_category.pack()
        
        main_plece=tkinter.Frame(
            self.storage,
            padx=25,
            pady=12
        )
        main_plece.pack(fill="both",side="bottom")
        
        self.table_product = ttk.Treeview(main_plece)
        self.table_product['columns']=("Id","product","category","type_quantity","product_quantity")
        self.table_product.heading("#0",text="No.")
        self.table_product.heading("Id",text="ID")
        self.table_product.heading("product",text="Product")
        self.table_product.heading("category",text="Category")
        self.table_product.heading("type_quantity",text="Type Quantity")
        self.table_product.heading("product_quantity",text="Quantity")
        self.product_treeview_refresh()
        self.table_product.pack(fill="both",side="left")
        self.table_product.bind("<<TreeviewSelect>>",self.f_product_selected)
        
        div=tkinter.Frame(
            main_plece,
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
            text="Product :",
            padx=10,
            pady=10
        )
        div_effect.pack(fill="both",side="bottom")
        
        add_product_button = tkinter.Button( div_effect,text="Add Product", command=self.window_effect.window_add_product ,width=16)
        add_product_button.pack()
        
        self.delete_product_button = tkinter.Button( div_effect,text="Delete Product", command=self.f_delete_product , state="disabled" ,width=16)
        self.delete_product_button.pack()
        
        self.update_product_button = tkinter.Button( div_effect,text="Edit Product" , state="disabled" ,width=16)
        self.update_product_button.pack()
        
        self.storage.mainloop()
        
        
    def window_category(self):
        if hasattr(self , "storage") and self.storage.winfo_exists :
            self.storage.destroy()
            self.inputvalue={}
            del self.product_name_var
            self.option_category.clear()
            del self.product_category_var
            del self.product_type_quantity_var
            
        self.storage = tkinter.Tk()
        
        selection_plece=tkinter.Frame(
            self.storage,
            padx=25,
            pady=12
        )
        selection_plece.pack(fill="both",side="top")
        
        button_category = tkinter.Button(selection_plece,text="Storage",command=self.main_window , width=25)
        button_category.pack()
        
        main_plece=tkinter.Frame(
            self.storage,
            padx=25,
            pady=12
        )
        main_plece.pack(fill="both",side="bottom")
        
        self.table_category = ttk.Treeview(main_plece)
        self.table_category['columns']=("Id","category")
        self.table_category.heading("#0",text="No.")
        self.table_category.heading("Id",text="ID")
        self.table_category.heading("category",text="Category")
        self.category_treeview_refresh()
        self.table_category.pack(fill="both",side="left")
        self.table_category.bind("<<TreeviewSelect>>",)
        
        div=tkinter.Frame(
            main_plece,
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
            text="Search Category :",
            padx=10,
            pady=10
        )
        div_search.pack(fill="both",side="top")
        
        self.category_name_var = tkinter.StringVar()
        tkinter.Label(div_search,text="Category Name:").pack()
        category_name_search = tkinter.Entry(div_search , textvariable=self.category_name_var)
        category_name_search.pack()

        button = tkinter.Button( div_search,text="Search", command=self.button_search_category,width=16)
        button.pack()
        
        div_effect = tkinter.LabelFrame(
            div,
            bd=3,
            relief="solid",
            text="Categoey :",
            padx=10,
            pady=10
        )
        div_effect.pack(fill="both",side="bottom")
        
        add_category_button = tkinter.Button( div_effect,text="Add Category", command=self.window_effect.window_add_category ,width=16)
        add_category_button.pack()
        
        self.delete_category_button = tkinter.Button( div_effect,text="Delete Category", command=self.f_delete_category , state="disabled" ,width=16)
        self.delete_category_button.pack()
        
        self.update_category_button = tkinter.Button( div_effect,text="Edit Category" , state="disabled" ,width=16)
        self.update_category_button.pack()
        
        self.storage.mainloop()
        
    def f_delete_category(self):
        selected_item = self.table_category.selection()
        result = self.dbconn.delete_category(selected_item[0])
        if result :
            self.category_treeview_refresh()
        
    def button_search_category(self):
        self.inputvalue["category"]=self.category_name_var.get()
        self.category_treeview_refresh()
    
    def category_treeview_refresh(self):
        self.table_category.delete(*self.table_category.get_children())
        alldata=self.dbconn.search_category(self.inputvalue)
        if self.set_condition.result_query_search(alldata):
            print(self.dbconn.search_category(self.inputvalue))
            if len(alldata) >0: 
                count=1
                for data in alldata:
                    self.table_category.insert("","end",text=f"{count}" ,values=(data[0],data[1]))
                    count+=1
    
    def f_category_selected(self,event):
        selected_item = self.table_product.selection()
        if not selected_item :
            self.delete_category_button["state"]="disabled"
            self.update_category_button["state"]="disabled"
            self.update_category_button["command"]=self.window_effect.window_edit_category(selected_item[0])
        else:
            self.delete_category_button["state"]="normal"
            self.update_category_button["state"]="normal"
            self.update_category_button["command"]=""
        
    def button_search_product(self):
        self.inputvalue["name"]=self.product_name_var.get()
        self.inputvalue["type_quantity"]=self.product_type_quantity_var.get()
        self.inputvalue["category"]=self.option_category[self.product_category_var.get()]
        self.product_treeview_refresh()
        
    def f_product_selected(self,event):
        selected_item = self.table_product.selection()
        if not selected_item :
            self.delete_product_button["state"]="disabled"
            self.update_product_button["state"]="disabled"
            self.update_product_button["command"]=self.window_effect.window_edit_product(selected_item[0])
        else:
            self.delete_product_button["state"]="normal"
            self.update_product_button["state"]="normal"
            self.update_product_button["command"]=""
        
    
    def f_delete_product(self):
        selected_item = self.table_product.selection()
        result = self.dbconn.delete_product(selected_item[0])
        if result :
            self.product_treeview_refresh()
            
        
    def product_treeview_refresh(self):
        self.table_product.delete(*self.table_product.get_children())
        alldata=self.dbconn.search_product(self.inputvalue)
        if self.set_condition.result_query_search(alldata):
            print(self.dbconn.search_product(self.inputvalue))
            if len(alldata) >0: 
                count=1
                for data in alldata:
                    self.table_product.insert("","end",text=f"{count}" ,values=(data[0],data[1],data[4],data[2],data[3]))
                    count+=1
        

class window_effect:
    def __init__(self):
        self.dbconn = connect_database()
        self.inputvalue=[]
        self.condition_set = condition_set()
        
    def window_edit_product(self ,target_id):
        if target_id != 0 and hasattr(self , "window_edit_error_warning")!= True:
            self.update_id = target_id
            result_search_id = self.dbconn.id_search_product(self.update_id)
            if self.condition_set.result_query_search(result_search_id):
                self.update_old_value=[]
                self.update_old_value.append(result_search_id[0])
                self.update_old_value.append(result_search_id[3])
                self.update_old_value.append(result_search_id[1])
                self.update_old_value.append(result_search_id[2])
            else:
                self.window_effect.destroy()
        if hasattr(self,"window_effect") and self.window_effect.winfo_exists:
            self.window_effect.destroy()
            del self.window_effect
        self.window_effect = tkinter.Tk()
        self.window_effect.title("Add Product")
        div_effect = tkinter.LabelFrame(
            self.window_effect,
            bd=3,
            relief="solid",
            text="Edit Product :",
            padx=10,
            pady=10
        )
        div_effect.pack(fill="both",side="top")
        
        self.edit_product_name_var = tkinter.StringVar()
        tkinter.Label(div_effect,text="Product Name:").pack()
        product_name = tkinter.Entry(div_effect , textvariable=self.edit_product_name_var)
        product_name.pack()
        error_product = tkinter.Label(div_effect,fg="red").pack()
        
        self.option_category ={}
        all_category = self.dbconn.search_category([])
        if self.condition_set.result_query_search(all_category):
            for category in all_category:
                self.option_category[category[1]]=category[0]
            
            print(self.option_category)
            tkinter.Label(div_effect,text="Category:").pack()
            self.edit_product_category_var = tkinter.StringVar()
            category_select = ttk.Combobox(div_effect,
                        textvariable=self.edit_product_category_var,
                        values=list(self.option_category.keys()),
                        state="readonly"
                        )
            category_select.pack()
            error_category = tkinter.Label(div_effect,fg="red").pack()
        else:
            self.window_effect.destroy()
        
        option_type_quantity=self.dbconn.list_diff_type_quantity()
        if self.condition_set.result_query_search(option_type_quantity) :
            tkinter.Label(div_effect,text="Type Quantity:").pack()
            self.product_edit_type_quantity_var = tkinter.StringVar()
            type_quantity_select = ttk.Combobox(div_effect,
                        textvariable=self.product_edit_type_quantity_var,
                        values=option_type_quantity
                        )
            type_quantity_select.pack()
            error_type_quantity = tkinter.Label(div_effect,fg="red").pack()
        else:
            self.window_effect.destroy()
        
        self.edit_quantity_var = tkinter.StringVar()
        tkinter.Label(div_effect,text="Quantity :").pack()
        Quantity = tkinter.Entry(div_effect , textvariable=self.edit_quantity_var)
        Quantity.pack()
        error_quantity = tkinter.Label(div_effect,fg="red").pack()
        
        if hasattr(self,"update_old_value"):
            self.edit_product_name_var.set(self.update_old_value[0])
            self.edit_product_category_var.set(self.update_old_value[1])
            self.product_edit_type_quantity_var.set(self.update_old_value[2])
            self.edit_quantity_var.set(self.update_old_value[3])
        
        if hasattr(self,"window_edit_error_warning") and len(self.window_edit_error_warning) >0 :
            # combobox style
            style = ttk.Style()
            style.configure(
                "Red.TCombobox",
                bordercolor="red",
                lightcolor="red",
                darkcolor="red"
            )
            if "product_name" in self.window_edit_error_warning:
                
                product_name['highlightthickness']=2
                #product_name['highlightbackground']="red"
                product_name['highlightcolor']="red"
                error_product['text']=self.window_edit_error_warning['product_name']
                
            if "category" in self.window_edit_error_warning:
                category_select['style']="Red.TCombobox"
                error_category['text']=self.window_edit_error_warning['category']
                
            if "type_quantity" in self.window_edit_error_warning:
                type_quantity_select['style']="Red.TCombobox"
                
                error_type_quantity['text']=self.window_edit_error_warning['type_quantity']
                
            if "quantity" in self.window_edit_error_warning:
                product_name['highlightthickness']=2
                #product_name['highlightbackground']="red"
                product_name['highlightcolor']="red"
                
                error_quantity['text']=self.window_edit_error_warning['quantity']
                
            del self.window_edit_error_warning
        
        button =tkinter.Button(div_effect, text="Edit", command=self.f_insert_product ,width=16)
        button.pack()
        
        self.window_effect.mainloop()
        
    def f_edit_product(self):
        self.window_edit_error_warning={}
        error_count = 0
        self.old_value=[]
        
        self.old_value.append(self.product_name_var.get())
        self.old_value.append(self.product_category_var.get())
        self.old_value.append(self.product_type_quantity_var.get())
        self.old_value.append(self.quantity_var.get())
        
        if   self.product_name_var.get() == "":
            self.inputvalue.append(self.product_name_var.get())
        else:
            self.window_edit_error_warning['product_name']='please input the product name !'
            error_count+=1
            
        if self.product_category_var.get() != "":
            self.inputvalue.append(self.option_category[self.product_category_var.get()])
        else:
            self.window_edit_error_warning['category']='please input the category !'
            error_count+=1
            
        if self.product_type_quantity_var.get() != "":
            self.inputvalue.append(self.product_type_quantity_var.get())
        else:
            self.window_edit_error_warning['type_quantity']='please input the type quantity !'
            error_count+=1
            
        if self.quantity_var.get() != "":
            if self.condition_set.in_numeric(self.quantity_var.get()):
                self.inputvalue.append(float(self.quantity_var.get()))
            else:
                self.window_edit_error_warning['quantity']='textbox quantity is number !' 
        else:
            self.window_edit_error_warning['quantity']='please input the quantity !'
            error_count+=1
        
        if error_count < 0 :
            result = self.dbconn.update_product(self.inputvalue)
            if result :
                self.window_effect.destroy()
            else:
                self.window_edit_product(self.update_id)
        elif error_count > 0:
            self.window_edit_product(self.update_id)
        
    def window_add_product(self):
        if hasattr(self,"window_effect") and self.window_effect.winfo_exists:
            self.window_effect.destroy()
            del self.window_effect
        self.window_effect = tkinter.Tk()
        self.window_effect.title("Edit Product")
        div_effect = tkinter.LabelFrame(
            self.window_effect,
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
            self.window_effect.destroy()
        
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
            self.window_effect.destroy()
        
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
        
        self.window_effect.mainloop()
    
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
                self.window_effect.destroy()
            else:
                self.window_add_product()
        elif error_count > 0:
            self.window_add_product()
            
    def window_add_category(self):
        if hasattr(self,"window_insert_category") and self.window_insert_category.winfo_exists:
            self.window_insert_category.destroy()
            del self.window_insert_category
        self.window_insert_category = tkinter.Tk()
        self.window_insert_category.title("Add Product")
        div_effect = tkinter.LabelFrame(
            self.window_insert_category,
            bd=3,
            relief="solid",
            text="Add Product :",
            padx=10,
            pady=10
        )
        div_effect.pack(fill="both",side="top")
        
        self.category_var = tkinter.StringVar()
        tkinter.Label(div_effect,text="Quantity :").pack()
        category = tkinter.Entry(div_effect , textvariable=self.category_var)
        category.pack()
        error_category = tkinter.Label(div_effect,fg="red").pack()
        
        if hasattr(self,"window_add_category_error_warning") and len(self.window_add_category_error_warning) >0 :
                
            if "category" in self.window_add_category_error_warning:
                category['highlightthickness']=2
                #product_name['highlightbackground']="red"
                category['highlightcolor']="red"
                self.category_var.set(self.window_add_category_old_value[3])
                error_category['text']=self.window_add_category_error_warning['quantity']
                
            del self.window_add_category_error_warning
        
        button =tkinter.Button(div_effect, text="Insert", command=self.f_insert_category ,width=16)
        button.pack()
        
        self.window_insert_category.mainloop()
           
    def f_insert_category(self):
        self.window_add_category_error_warning={}
        error_count = 0
        self.window_add_category_old_value=[]

        self.window_add_category_old_value.append(self.product_category_var.get())
        
        if   self.product_name_var.get() == "":
            self.inputvalue.append(self.product_name_var.get())
        else:
            self.window_add_category_error_warning['product_name']='please input the category !'
            error_count+=1
        
        if error_count < 0 :
            result = self.dbconn.insert_product(self.inputvalue)
            if result :
                self.window_insert_category.destroy()
            else:
                self.window_add_category()
        elif error_count > 0:
            self.window_add_category()
        
class condition_set:
    def in_numeric(string):
        try:
            float(string)
            return True
        except:
            return False
        
    def result_query_search(self, result):
        if isinstance(result, (list, tuple, set)):
            return True
        else:
            return False
    
window = storage()
window.main_window()