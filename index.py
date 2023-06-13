from inspect import Parameter
from tkinter import ttk
from tkinter import *
import sqlite3

class Product():
    
    db_name = 'database.db'
    
    def __init__(self, window) -> None:
        self.window = window
        self.window.title("Product Application")
        
        # Crear Contenedor(Frame)
        frame = LabelFrame(self.window, text="Registra un nuevo producto")
        frame.grid(row=0,column=0, columnspan=3, pady=20)
        
        #Entrada de nombre
        Label(frame, text="Nombre: ").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)
        
        #Entrada input
        Label(frame, text="Precio").grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2,column=1)
        
        #Boton agregar producto
        ttk.Button(frame, text="Guardar Producto", command=self.add_product).grid(row=3, columnspan=2,sticky=W+E)
        #Mensaje de salida
        self.message = Label(text="", fg="red")
        self.message.grid(row=3, column= 0, columnspan=2,sticky = W+E)        
        
        #Tabla
        self.tree = ttk.Treeview(height=20, columns= 2)
        self.tree.grid(row=4,column=0, columnspan=2)
        self.tree.heading("#0", text="Nombre", anchor=CENTER)
        self.tree.heading("#1", text="Precio", anchor=CENTER)
        
        #Botones
        ttk.Button(text = "Eliminar", command=self.delete_product).grid(row=5, column = 0, sticky= W+E)
        ttk.Button(text = "Editar", command = self.edit_product).grid(row=5, column = 1, sticky= W+E)

        
        #Llenando las filas
        self.get_products()

    
    def run_query(self, query, parameters =()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_products(self):
        #Limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Cpnsultando datos
        query = "SELECT * From product ORDER BY name DESC"
        db_rows = self.run_query(query)
        #Rellenando los datos
        for row in db_rows:
            self.tree.insert("",0,text=row[1], values=row[2])
    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
    
    
    def add_product(self):
        if self.validation():
            query = "INSERT INTO product VALUES(NULL,?,?)"
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message["text"] = f"Producto {self.name.get()} agregado satisfactoriamente"
            self.name.delete(0,END)
            self.price.delete(0,END)
        else:
            self.message["text"] = "El nombre y el precio es requerido"
        self.get_products()
        
        
    def delete_product(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona una opcion"
            return
        self.message["text"] = ""
        name = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM product WHERE name = ?"
        self.run_query(query, (name,))
        self.message["text"] = f"Producto {name} ha sido eliminado de forma exitosa"
        self.get_products()
        
    def edit_product(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona una opcion"
            return
        name = self.tree.item(self.tree.selection())["text"]
        old_price = self.tree.item(self.tree.selection())["values"][0]
        
        self.edit_wind = Toplevel()
        self.edit_wind.resizable(False,False)
        self.edit_wind.title("Editar Producto")
        
        #Nombre anterior
        Label(self.edit_wind, text="Nombre Anterior: ").grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind,value=name),state= "readonly").grid(row=0,column=2)
        #nuevo nombre
        Label(self.edit_wind, text="Nuevo Nombre: ").grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)
        
        #old_price
        Label(self.edit_wind, text= "Precio Anterior").grid(row=2, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value = old_price),state="readonly").grid(row=2,column = 2)
        #new_price
        Label(self.edit_wind, text = "Nuevo Precio").grid(row=3, column= 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)
        
        #boton
        Button(self.edit_wind, text= "Actualizar", command= lambda: self.edit_records(new_name.get(),name, new_price.get(),old_price)).grid(row=4,column=2,sticky=W)
    
    def edit_records(self, new_name, name, new_price, old_price):
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ? "
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message["text"] = f"Producto {name} actualizado correctamente"
        self.get_products()



if __name__ == "__main__":
    window = Tk()
    window.resizable(False,False)

    application = Product(window)
    
    
    
    window.mainloop()