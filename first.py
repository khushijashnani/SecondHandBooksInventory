from tkinter import *
import mysql.connector as mysql
import tkinter.messagebox as MessageBox

class App(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        self.container = Frame(self)
        self.container.pack(side='top',fill='both',expand=False)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        self.con = mysql.connect(host='localhost',user='root',password='Khushi',database='python_tkinter')
        self.cursor = self.con.cursor()
        self.id = 0
        self.frames = {}
        self.show_frame(main_screen)
    
    def show_frame(self,context):
        if context in (main_screen,register,login,homepage):
            frame = context(self.container,self)
            self.frames[context]= frame 
            frame.grid(row=0,column=0,sticky='nsew')
        frame.tkraise()

    def switch(self,context):
        frame = context
        if isinstance(frame,register):
            frame = self.frames[main_screen]
        if isinstance(frame,login):
            frame = self.frames[main_screen]
        frame.tkraise()

    def regis(self,email,username,password,phone,branch,sem):
        print(email)
        print("12345")
        if (username=='' or password=='' or phone=='' or email=='' or branch=='' or sem==''):
            MessageBox.showinfo('Registration Status','All fields are required')
        else :
            rc = self.register_user(email,username,password,phone,branch,sem)
            print(rc)
            if rc == True:
                sql = 'select id from users where email = %s'
                print(sql)
                self.cursor.execute(sql,(email,))
                self.id = self.cursor.fetchall()[0][0]
                print(self.id)
                self.show_frame(homepage)

    def register_user(self,email,username,password,phone,branch,sem):
        sql = 'insert into users(email,username,password,phone,branch,sem) values(%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql,(email,username,password,phone,branch,sem))
        self.cursor.execute("commit")
        MessageBox.showinfo('Registration Status','User registered !')
        return True

    def check_user(self,username,password):
        sql = 'select id from users where username = %s and password = %s'
        print(sql)
        self.cursor.execute(sql,(username,password))
        result= self.cursor.fetchall()
        if result != []:
            print(result)
            self.id = result[0][0]
            self.show_frame(homepage)
        else:
            MessageBox.showinfo('Login Status','Incorrect credentials')
        

class homepage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        print(controller.id)
        #use this controller.id(current user's id) for queries
        booksSold = Listbox(self)
        booksAvail = Listbox(self)
        Label(self,text ='List of your books',font=('Helvetica',13)).grid(row=0,column=0)
        Label(self,text ='List of the books available in the inventory',font=('Helvetica',13)).grid(row=0,column=1)
        booksSold.grid(row=1,column=0)
        booksAvail.grid(row=1,column=1)
        Button(self, text= 'Want to Buy ?',height='2',width='40',command=lambda : controller.show_frame()).grid(row=2,column=0)
        Button(self, text= 'Want to Sell ?',height='2',width='40',command=lambda : controller.show_frame()).grid(row=2,column=1)
        Button(self, text= 'Log Out',height='2',width='20',command=lambda : controller.show_frame(main_screen)).grid(row=3,column=1,sticky='E')
        

class register(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        Button(self,text = 'Back',command = lambda:controller.switch(self)).grid(row=0,column=0)
        username = StringVar()
        password = StringVar()
        email = StringVar()
        phone = StringVar()
        branch = StringVar()
        sem = StringVar()
        Label(self,text ='Please enter the details below : ',font=('Helvetica',13)).grid(row=1)
        Label(self,text ='Email: ',font=('Helvetica',13)).grid(row=2,column=0)
        em = Entry(self, textvariable = email)
        em.grid(row=2,column=1)
        Label(self,text ='Username: ',font=('Helvetica',13)).grid(row=3,column=0)
        user = Entry(self, textvariable = username)
        user.grid(row=3,column=1)
        Label(self,text ='Password: ',font=('Helvetica',13)).grid(row=4,column=0)
        paswd = Entry(self, textvariable = password)
        paswd.grid(row=4,column=1)
        Label(self,text ='Phone No: ',font=('Helvetica',13)).grid(row=5,column=0)
        ph = Entry(self, textvariable = phone)
        ph.grid(row=5,column=1)
        Label(self,text ='Branch: ',font=('Helvetica',13)).grid(row=6,column=0)
        br = Entry(self, textvariable = branch)
        br.grid(row=6,column=1)
        Label(self,text ='Semester: ',font=('Helvetica',13)).grid(row=7,column=0)
        se = Entry(self, textvariable = sem)
        se.grid(row=7,column=1)
        #user = {'email': email.get(),'username':username.get(),'password':password.get(),'phone':phone.get(),'branch':branch.get(),'sem':sem.get()}
        Button(self,text='Register',height='2',width='40',command=lambda:controller.regis(email.get(),username.get(),password.get(),phone.get(),branch.get(),sem.get())).grid(row = 8)
        

class login(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        Button(self,text = 'Back',command = lambda:controller.switch(self)).grid(row=0,column=0)
        username = StringVar()
        password = StringVar()
        Label(self,text ='Please enter the details below : ',font=('Helvetica',13)).grid(row=1)
        Label(self,text ='Username: ',font=('Helvetica',13)).grid(row=2,column=0)
        Entry(self, textvariable = username).grid(row=2,column=1)
        Label(self,text ='Password: ',font=('Helvetica',13)).grid(row=3,column=0)
        Entry(self, textvariable = password).grid(row=3,column=1)
        Button(self,text='Log In',height='2',width='40',command=lambda:controller.check_user(username.get(),password.get())).grid(row = 4)

class main_screen(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        Label(self,text = 'Admin?',height='2',width='300',fg='white', bg='black',font=('Helvetica',13)).pack()
        Label(self,text='').pack()
        Button(self,text= 'Admin',height='2',width='30').pack()
        Label(self,text='').pack()
        Label(self,text = 'User?',height='2',width='300',fg='white', bg='black',font=('Helvetica',13)).pack()
        Label(self,text='').pack()
        Button(self,text = 'Login',height='2',width='25',command=lambda : controller.show_frame(login)).pack()
        Label(self,text='').pack()
        Button(self,text = 'Register',height='2',width='25',command=lambda : controller.show_frame(register)).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()