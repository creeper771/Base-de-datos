from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from container import Container
from PIL import Image, ImageTk
from utils.paths import get_resource_path
from database.user_dao import UserDAO

class Login(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador= controlador
        self.user_dao = UserDAO()
        self.widgets()

    def validacion_datos(self, user, password):
        return len(user) > 0 and len(password) > 0
    
    def login(self):
        user = self.username.get()
        password= self.password.get()

        if self.validacion_datos(user, password):
            try:
                usuario_activo = self.user_dao.verify_user(user, password)
                if usuario_activo:
                    self.controlador.usuario_activo_id = usuario_activo['id']
                    self.controlador.usuario_activo_nombre = usuario_activo['username']
                    self.control1() #Hacer la consulta
                else:
                    self.username.delete(0, "end") #Limpia el campo de usario y contraseña
                    self.password.delete(0, "end")
                    messagebox.showerror(title= "Error", message= "Usuario y/o contraseña incorrecta")#mensaje de error si no coinciden con la base de datos
            except Exception as e:
                messagebox.showerror(title="Error", message= f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showerror(title="Error", message= "Llene todas las casillas")

    def control1(self):
        self.controlador.show_frame(Container)

    def control2(self):
        self.controlador.show_frame(Registro)
            
    def widgets(self):
        fondo= tk.Frame(self, bg="#C6D9E3")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        ruta= get_resource_path(r"Imagenes/fondo_login.jpg")
        self.bg_image= Image.open(ruta)
        self.bg_image= self.bg_image.resize((1100,700))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label= ttk.Label(fondo, image=self.bg_image)
        self.bg_label.place(x=0, y=0, width=1100, height=650)


        frame1=tk.Frame(self, bg="#FFFFFF", highlightbackground= "black", highlightthickness=2)
        frame1.place(x=350, y=40, width=400, height=560)

        ruta= get_resource_path(r"Imagenes/controlfix.png")
        self.logo_image= Image.open(ruta)
        self.logo_image= self.logo_image.resize((200,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label= ttk.Label(frame1, image=self.logo_image, background="#FFFFFF")
        self.logo_label.place(x=100, y=20)

    
        user= ttk.Label(frame1, text="Nombre de usuario", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.username=ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)


        pasword= ttk.Label(frame1, text="Contraseña", font="arial 16 bold", background="#FFFFFF")
        pasword.place(x=100,y=340)
        self.password= ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.password.place(x=80, y=380, width=240, height=40)

        #botones de iniciar sesion y registrar
        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/iniciar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn1= tk.Button(frame1, text="Iniciar sesion", font="arial 16 bold", command= self.login)
        btn1.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn1.image= imagen_tk
        btn1.place(x=80, y=440, width=240, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/registrar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn2= tk.Button(frame1, text="Registrar", font="arial 16 bold", command= self.control2)
        btn2.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn2.image= imagen_tk
        btn2.place(x=80, y=500, width=240, height=40)

class Registro(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador= controlador
        self.user_dao = UserDAO()
        self.widgets()

    def validacion_datos(self, user, password):
        return len(user) > 0 and len(password) > 0 #validar que no esten vacios eso campos

    def registro(self):
        user= self.username.get()
        password= self.password.get()
        key= self.key.get()

        if self.validacion_datos(user, password):
            if len(password) < 5:
                messagebox.showinfo(title= "Error", message="Contraseña demasiada corta")
                self.username.delete(0, 'end')
                self.password.delete(0, 'end')
            else:
            
                if key=="1234":
                    try:
                        self.user_dao.register_user(user, password)
                        self.control1()
                    except Exception as e:
                        messagebox.showerror(title="Error", message=f"Error al registrar: {e}")
                else:
                    messagebox.showerror(title="Registro", message="Error al ingresar el codigo de registro")
        else:
            messagebox.showerror(title="Error", message="Llene sus datos")

    def control1(self):
        self.controlador.show_frame(Container) #si se crea el usuario se pasa a aca

    def control2(self):
        self.controlador.show_frame(Login)#regresa al login

    
    def widgets(self):
        fondo= tk.Frame(self, bg="#C6D9E3")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        ruta= get_resource_path(r"Imagenes/fondo_login.jpg")
        self.bg_image= Image.open(ruta)
        self.bg_image= self.bg_image.resize((1100,650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label= ttk.Label(fondo, image=self.bg_image)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        ruta= get_resource_path(r"Imagenes/controlfix.png")
        self.logo_image= Image.open(ruta)
        self.logo_image= self.logo_image.resize((200,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)

        frame1=tk.Frame(self, bg="#FFFFFF", highlightbackground= "black", highlightthickness=2)
        frame1.place(x=350, y=10, width=400, height=630)

        self.logo_label= ttk.Label(frame1, image=self.logo_image, background="#FFFFFF")
        self.logo_label.place(x=100, y=20)


        user= ttk.Label(frame1, text="Nombre de usuario", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.username=ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)


        pasword= ttk.Label(frame1, text="Contraseña", font="arial 16 bold", background="#FFFFFF")
        pasword.place(x=100,y=340)
        self.password= ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.password.place(x=80, y=380, width=240, height=40)

        key = ttk.Label(frame1, text="Codigo de registro", font="arial 16 bold", background="#FFFFFF")
        key.place(x=100, y=430)
        self.key=ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.key.place(x=80,y=470, width=240, height=40)
        
        #botones de iniciar sesion y registrar
        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/registrar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn3= tk.Button(frame1, text="Registrar", font="arial 16 bold", command=self.registro)
        btn3.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn3.image= imagen_tk
        btn3.place(x=80, y=520, width=240, height=40)

        #Poner iconos a los botones
        ruta= get_resource_path(r"Iconos/regresar.png")
        imagen_pil= Image.open(ruta)
        imagen_resize= imagen_pil.resize((30, 30))
        imagen_tk= ImageTk.PhotoImage(imagen_resize)
        btn4= tk.Button(frame1, text="Regresar", font="arial 16 bold",command=self.control2)
        btn4.config(image= imagen_tk, compound= LEFT, padx= 5)
        btn4.image= imagen_tk
        btn4.place(x=80, y=570, width=240, height=40)