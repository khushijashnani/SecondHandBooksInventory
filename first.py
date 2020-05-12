from tkinter import *
import mysql.connector as mysql
import tkinter.messagebox as MessageBox

class App(Tk):
	def __init__(self,*args,**kwargs):
		Tk.__init__(self,*args,**kwargs)
		self.configure(bg='black')
		self.geometry("1100x800")
		self.container = Frame(self)
		self.container.pack(side='top',fill='both',expand=False)
		#self.container.grid_rowconfigure(0,weight=1)
		#self.container.grid_columnconfigure(0,weight=1)
		self.con = mysql.connect(host='localhost',user='root',password='Khushi',database='python_tkinter')
		self.cursor = self.con.cursor()
		self.id = 0
		self.frames = {}
		self.show_frame(main_screen)
	
	def show_frame(self,context):
		if context in (main_screen,register,login,homepage,buybooks,sellbooks):
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

	def display(self,ID):
		sql="select bid, name, branch, semester, cost from books where id <> %s and status = %s "
		self.cursor.execute(sql,(ID,'A'))
		data = self.cursor.fetchall()
		return data

	def userBooks(self,userno):
		sql="select bid,name,branch,semester,cost,status from books where id=%s"
		self.cursor.execute(sql,(userno,))
		data =self.cursor.fetchall()
		return data


	def buy(self,row,ID):
		MsgBox = MessageBox.askquestion ('Confirmation','Are you sure you want to buy this book')
		if MsgBox == 'yes':
			print('great')
			print(row)
			print(type(row))
			i=row.split()
			print(i)
			print(i[4])
			bid=int(i[4])
			print(type(ID))
			print(ID)
			print(bid)
			sql="update books set status=%s,buyerid=%s where bid=%s"
			self.cursor.execute(sql,('S',ID,bid))
			self.cursor.execute("commit")
			self.show_frame(displaybooks)
		else:
			print('nt so great')

	def avail(self,ID):
		sql="select bid, name, branch, semester, cost from books where buyerid= %s"
		self.cursor.execute(sql,(ID,))
		data = self.cursor.fetchall()
		return data

	def sell(self,name,branch,semester,cost,ID):
		if (name=='' or branch=='' or semester=='' or cost==''):
			MessageBox.showinfo('Registration Status','All fields are required')
		else:
			sql = 'insert into books(name,branch,semester,cost,status,id) values(%s,%s,%s,%s,%s,%s)'
			self.cursor.execute(sql,(name,branch,semester,cost,'A',ID))
			self.cursor.execute("commit")
			MessageBox.showinfo('book Status','Book added to the list!')

	def name(self):
		sql="select username from users where id= %s"
		self.cursor.execute(sql,(self.id,))
		data = self.cursor.fetchall()
		return data

class sellbooks(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.configure(bg='black')
		controller.title('Sell your book')
		self.grid_columnconfigure(0, weight=0, pad="80")
		self.grid_columnconfigure(0, weight=0)
		self.grid_rowconfigure(0,weight=0, pad="80")
		self.grid_rowconfigure(5,weight=0, pad="80")

		Button(self,text = 'Back', bg='light blue', width='20', font=('Helvetica',12), command = lambda:controller.show_frame(homepage)).grid(row=0,column=0)
		name=StringVar()
		branch=StringVar()
		semester=StringVar()
		cost=StringVar()

		Label(self,text ='', height='2', fg='white', width=30, bg='black',font=('Helvetica',15)).grid(row=1,column=0, sticky='e')
		Label(self,text="Name", height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=1,column=3, sticky='e')
		nm=Entry(self,textvariable=name)
		nm.grid(row=1,column=4, padx=10)
		
		Label(self,text="Branch", height='2',fg='white', bg='black',font=('Helvetica',15)).grid(row=2,column=3, sticky='e')
		br=Entry(self,textvariable=branch)
		br.grid(row=2,column=4, padx=10)
		
		Label(self,text="Semester", height='2',fg='white', bg='black',font=('Helvetica',15)).grid(row=3,column=3, sticky='e')
		sem=Entry(self,textvariable=semester)
		sem.grid(row=3,column=4, padx=10)
		
		Label(self,text="Cost", height='2',fg='white', bg='black',font=('Helvetica',15)).grid(row=4,column=3, sticky='e')
		ct=Entry(self,textvariable=cost)
		ct.grid(row=4,column=4, padx=10)
		Button(self,text='Sell', bg='light blue', width='20', font=('Helvetica',12), command=lambda:controller.sell(name.get(),branch.get(),semester.get(),cost.get(),controller.id)).grid(row = 5, column=3, columnspan=2)


class buybooks(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.configure(bg='black')
		controller.title('Inventory')
		self.grid_columnconfigure(0, weight=0, pad="80")
		self.grid_columnconfigure(0, weight=0)
		self.grid_rowconfigure(0,weight=0, pad="80")
		self.grid_rowconfigure(2,weight=0, pad="80")
		data=controller.display(controller.id)
		availablebooks = Listbox(self, fg='white', bg='black', width='80', selectbackground='dark blue')
		
		if data!=[]:
			longest_1 = 20
			longest_2 = 20
			longest_3 = 20
			longest_4 = 20
			longest_5 = 20
			availablebooks.insert(END,'{0:^{longest_1}} {1:^{longest_2}} {2:^{longest_3}} {3:^{longest_4}} {4:^{longest_5}} '.format('Name'.center(20," "),'Branch'.center(20," "),'Semester'.center(20," "),'Cost'.center(20," "),'Bid'.center(20," "),longest_1=longest_1,longest_2=longest_2,longest_3=longest_3,longest_4=longest_4, longest_5=longest_5))  
			print(data)
			for row in data:
				line = '{0:^{longest_1}} {1:^{longest_2}} {2:^{longest_3}} {3:^{longest_4}} {4:^{longest_5}}'.format(row[1].center(20," "),row[2].center(20," "),str(row[3]).center(20," "),str(row[4]).center(20," "),str(row[0]).center(20," "),longest_1=longest_1,longest_2=longest_2,longest_3=longest_3,longest_4=longest_4,longest_5=longest_5)    
				print(line)
				availablebooks.insert(END,line)

		availablebooks.grid(row=2, column=2)
		print(availablebooks.get(ACTIVE))
		Button(self,text = 'Back', bg='light blue', width='20', font=('Helvetica',12), command = lambda:controller.show_frame(homepage)).grid(row=0,column=0)
		
		Label(self,text ='Please select the book you want to buy from the following books', height='2',fg='white', bg='black',font=('Helvetica',15)).grid(row=1, column=1, sticky='e', columnspan="2")

		#Label(self,text ='', height='2', fg='white', width=30, bg='black',font=('Helvetica',15)).grid(row=1,column=0, sticky='e')
		Button(self,text ='Buy', bg='light blue', width='20', font=('Helvetica',12), command=lambda:controller.buy(availablebooks.get(ACTIVE),controller.id)).grid(row=3, column=1, columnspan="2")


class homepage(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.configure(bg='black')
		self.grid_rowconfigure(2,weight=0, pad="80")
		print(controller.id)
		#use this controller.id(current user's id) for queries
		name = 'Welcome, ' + controller.name()[0][0]
		controller.title(name)
		booksSold = Listbox(self, fg='white', bg='black', width='50', selectbackground='dark blue')
		booksAvail = Listbox(self, fg='white', bg='black', width='50', selectbackground='dark blue')
		Label(self,text ='Your books on sale', height='4',width='50',fg='white', bg='black',font=('Helvetica',15)).grid(row=0,column=0)
		Label(self,text ='Books you bought', height='4',width='50',fg='white', bg='black',font=('Helvetica',15)).grid(row=0,column=1)
		data=controller.avail(controller.id)
		bSold = controller.userBooks(controller.id)
		print(bSold)
		#bSold is users books for sale 
		if bSold!=[]:
			longest_1 = 10#max( len(x[1]) for x in bSold )
			longest_2 = 10
			print(longest_1)
			longest_3 = 10
			longest_4 = 10
			longest_5 = 10
			booksSold.insert(END,'{0:^{longest_1}} {1:^{longest_2}} {2:^{longest_3}} {3:^{longest_4}} {4:^{longest_5}} '.format('Name'.center(10," "),'Branch'.center(10," "),'Semester'.center(10," "),'Cost'.center(10," "),'Bid'.center(10," "),longest_1=longest_1,longest_2=longest_2,longest_3=longest_3,longest_4=longest_4,longest_5=longest_5))  
			print(data)	    	
			for row in bSold:
				line = '{0:^{longest_1}} {1:^{longest_2}} {2:^{longest_3}} {3:^{longest_4}} {4:^{longest_5}}'.format(row[1].center(10," "),row[2].center(10," "),str(row[3]).center(10," "),str(row[4]),str(row[0]).center(10," "),longest_1=longest_1,longest_2=longest_2,longest_3=longest_3,longest_4=longest_4,longest_5=longest_5)    
				booksSold.insert(END,line)

		if data!=[]:
			longest_1 = max( len(x[1]) for x in data )
			longest_2 = 7
			print(longest_1)
			#longest_1=max(longest_1,7)+2
			longest_3 = 11
			longest_4 = 5
			longest_5 = 6
			booksAvail.insert(END,'{0:^{longest_1}} {1:^{longest_2}} {2:^{longest_3}} {3:^{longest_4}} {4:^{longest_5}} '.format('Name'.center(10," "),'Branch'.center(10," "),'Semester'.center(10," "),'Cost'.center(10," "),'Bid'.center(10," "),longest_1=longest_1,longest_2=longest_2,longest_3=longest_3,longest_4=longest_4, longest_5=longest_5))              
			print(data)
			for row in data:
				line = '{0:^{longest_1}} {1:^{longest_2}} {2:^{longest_3}} {3:^{longest_4}} {4:^{longest_5}}'.format(row[1].center(10," "),row[2].center(10," "),str(row[3]).center(10," "),str(row[4]).center(10," "),str(row[0]).center(10," "),longest_1=longest_1,longest_2=longest_2,longest_3=longest_3,longest_4=longest_4,longest_5=longest_5)    
				booksAvail.insert(END,line)
		booksSold.grid(row=1,column=0)
		booksAvail.grid(row=1,column=1)
		Button(self, text= 'Want to Buy ?', bg='light blue', width='20', font=('Helvetica',12),command=lambda : controller.show_frame(buybooks)).grid(row=2,column=0)
		Button(self, text= 'Want to Sell ?', bg='light blue', width='20', font=('Helvetica',12),command=lambda : controller.show_frame(sellbooks)).grid(row=2,column=1)
		Button(self, text= 'Log Out', bg='light blue', width='20', font=('Helvetica',12),command=lambda : controller.show_frame(main_screen)).grid(columnspan=3)
		

class register(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.configure(bg='black')
		controller.title('Happy Buying')
		self.grid_columnconfigure(0, weight=0, pad="80")
		self.grid_columnconfigure(0, weight=0)
		self.grid_rowconfigure(0,weight=0, pad="80")
		self.grid_rowconfigure(8,weight=0, pad="80")
		Button(self,text = 'Back', bg='light blue', width='20', font=('Helvetica',12), command = lambda:controller.switch(self)).grid(row=0,column=0)
		username = StringVar()
		password = StringVar()
		email = StringVar()
		phone = StringVar()
		branch = StringVar()
		sem = StringVar()
		Label(self,text ='Please enter the details below : ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=1, column=1, columnspan="2")

		Label(self,text ='Email: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=2,column=1, sticky='e')
		em = Entry(self, textvariable = email)
		em.grid(row=2,column=2)
		
		Label(self,text ='', height='2', fg='white', width=30, bg='black',font=('Helvetica',15)).grid(row=3,column=0, sticky='e')
		Label(self,text ='Username: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=3,column=1, sticky='e')
		user = Entry(self, textvariable = username)
		user.grid(row=3,column=2)
		
		Label(self,text ='Password: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=4,column=1, sticky='e')
		paswd = Entry(self, textvariable = password)
		paswd.grid(row=4,column=2)
		
		Label(self,text ='Phone No: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=5,column=1, sticky='e')
		ph = Entry(self, textvariable = phone)
		ph.grid(row=5,column=2)
		
		Label(self,text ='Branch: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=6,column=1, sticky='e')
		br = Entry(self, textvariable = branch)
		br.grid(row=6,column=2)
		
		Label(self,text ='Semester: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=7,column=1, sticky='e')
		se = Entry(self, textvariable = sem)
		se.grid(row=7,column=2)
		#user = {'email': email.get(),'username':username.get(),'password':password.get(),'phone':phone.get(),'branch':branch.get(),'sem':sem.get()}
		Button(self,text='Register', bg='light blue', width='20', font=('Helvetica',12), command=lambda:controller.regis(email.get(),username.get(),password.get(),phone.get(),branch.get(),sem.get())).grid(row = 8, column=1, columnspan="2")
		
 
class login(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.configure(bg='black')
		controller.title('Happy Buying')
		self.grid_columnconfigure(0, weight=0, pad="80")
		self.grid_columnconfigure(1, weight=0)
		self.grid_rowconfigure(1,weight=0, pad="100")
		self.grid_rowconfigure(5,weight=0, pad="100")
		Button(self,text = 'Back', bg='light blue', width='20', font=('Helvetica',12), command = lambda:controller.switch(self)).grid(row=1,column=0)
		username = StringVar()
		password = StringVar()
		Label(self,text ='Please enter the details below : ', height='2',fg='white', bg='black',font=('Helvetica',15)).grid(row=2, column=1, sticky='e', columnspan="2")
		Label(self,text ='', height='2', fg='white', width=30, bg='black',font=('Helvetica',15)).grid(row=3,column=0, sticky='e')
		Label(self,text ='Username: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=3,column=1, sticky='e')
		Entry(self, textvariable = username).grid(row=3,column=2)
		Label(self,text ='Password: ', height='2', fg='white', bg='black',font=('Helvetica',15)).grid(row=4,column=1, sticky='e')
		Entry(self, textvariable = password).grid(row=4,column=2)
		Button(self,text='Log In', bg='light blue', width='20', font=('Helvetica',12), command=lambda:controller.check_user(username.get(),password.get())).grid(row = 5, column=1, columnspan="2")


class main_screen(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self, parent)
		self.configure(bg='black')
		controller.title('Happy Buying')
		self.grid_rowconfigure(0,weight=1)
		self.grid_rowconfigure(1,weight=1)
		self.grid_rowconfigure(2,weight=1, pad="50")
		self.grid_rowconfigure(3,weight=1)
		#self.grid_rowconfigure(4,weight=1, pad="50")
		#self.grid_rowconfigure(5,weight=1)
		self.grid_columnconfigure(0,weight=1)
		Label(self,text = 'WELCOME!',height='8',width='100',fg='white', bg='black',font=('Helvetica',15)).grid(row=0)        
		Button(self,text = 'Login', bg='light blue', width='20', font=('Helvetica',12), command=lambda : controller.show_frame(login)).grid(row=1)
		Button(self,text = 'Register', bg='light blue', width='20', font=('Helvetica',12), command=lambda : controller.show_frame(register)).grid(row=2)
		Label(self,text = 'Happy Buying!',height='4',width='100',fg='white', bg='black',font=('Helvetica',15)).grid(row=3)
if __name__ == "__main__":
	app = App()

	app.mainloop()
  
