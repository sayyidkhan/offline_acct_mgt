''' start of import '''
from tkinter import *
from tkinter import ttk

from . import frontend_logic as fel
''' end of import '''

class MainWindow:

	def __init__(self,dbOperations):
		self.dbOperations = dbOperations

	def _getDb(self):
		return self.dbOperations

	@staticmethod
	def togglePasswordUI(textBoxObj,state):
		print(state)
		if(state['currentState']):
			state['currentState'] = False
			textBoxObj['password'].config(show='')
			textBoxObj['googleAuthKey'].config(show='')
		else:
			state['currentState'] = True
			textBoxObj['password'].config(show='*')
			textBoxObj['googleAuthKey'].config(show='*')

	def renderUI(self):
		root = Tk()
		content = ttk.Frame(root, padding=(12,12,12,12))
		showPassword = {'currentState' : True}

		## top label
		topButtonFrame = Frame(content, highlightbackground="black", highlightthickness=1)
		dashboardLabel = ttk.Label(topButtonFrame, text="Dashboard")
		''' add '''
		add = ttk.Button(topButtonFrame, text="Add", command=lambda:tableGUI.addRecord())
		run = ttk.Button(topButtonFrame, text="Run",command=lambda:tableGUI.generateOTP())
		otpLbl = ttk.Label(topButtonFrame, text="OTP: " )
		otpEntry = ttk.Entry(topButtonFrame)

		#label and textfield section frame
		userDetailFrame = ttk.Frame(content, borderwidth=3, relief="ridge")
		''' run order '''
		runorderLbl = ttk.Label(userDetailFrame, text="Run Order")
		fel.CreateToolTip(runorderLbl,text="Decides which account will run first\n"+"in the automation program")
		runorderEntry = ttk.Entry(userDetailFrame)
		callback = root.register(fel.only_numeric_input) # registers a Tcl to Python callback
		runorderEntry.configure(validate="key", validatecommand=(callback, "%P"))  # enables validation

		''' account type '''
		accTypeLbl = ttk.Label(userDetailFrame, text="Account Type")
		fel.CreateToolTip(accTypeLbl,text="what is this account for?")
		accTypeEntry = ttk.Entry(userDetailFrame)

		''' name '''
		nameLbl = ttk.Label(userDetailFrame, text="Username")
		fel.CreateToolTip(nameLbl,text="Username of your account")
		nameEntry = ttk.Entry(userDetailFrame)

		''' password '''
		passwordLbl = ttk.Label(userDetailFrame, text="Password")
		fel.CreateToolTip(passwordLbl,text="Password of your account")
		passwordEntry = ttk.Entry(userDetailFrame,show='*')

		''' google Authenticator '''
		goggleAuthLbl = ttk.Label(userDetailFrame, text="Google Auth Key")
		fel.CreateToolTip(goggleAuthLbl,text="Google Authenticator secret key of your account")
		goggleAuthEntry = ttk.Entry(userDetailFrame,show='*')

		''' consolidate into dictonary for easy access '''
		textBoxObj = {
			'runOrder' : runorderEntry,
			'acctType' : accTypeEntry,
			'myUsername' : nameEntry,
			'password' : passwordEntry,
			'googleAuthKey' : goggleAuthEntry,
		}

		#list frame
		listLbl = ttk.Label(content, text="List Of Accounts")
		listFrame = ttk.Frame(content, borderwidth=3, relief="ridge")
		''' table GUI '''
		tableGUI = fel.TableBox(frame=listFrame,textBoxObj=textBoxObj,dbOperations=self.dbOperations,otpEntry=otpEntry)
		tableGUI.updateTable()

		## information panel
		informationFrame = Frame(content, highlightbackground="black", highlightthickness=1)
		infoLabel = ttk.Label(informationFrame, text="Info: ")
		descriptionValue = StringVar()
		descriptionLabelObj = fel.InfoBox(informationFrame)
		descriptionLabel = descriptionLabelObj.getDescriptionBox()

		## bottom label
		bottomButtonFrame = Frame(content, highlightbackground="black", highlightthickness=1)
		actionLabel = ttk.Label(bottomButtonFrame, text="Actions")
		clear = ttk.Button(bottomButtonFrame,text="Clear",command=lambda:tableGUI.clearcurrSelection())
		delete = ttk.Button(bottomButtonFrame, text="Delete Selected Row",state='disabled', command=lambda:tableGUI.deleteCurrRow())
		save = ttk.Button(bottomButtonFrame, text="Save", state='disabled', command=lambda:tableGUI.updateRecord())
		refresh = ttk.Button(bottomButtonFrame, text="Refresh List", command=lambda:tableGUI.refreshTable())
		hideInfo = ttk.Button(bottomButtonFrame, text="Show Info", command=lambda:MainWindow.togglePasswordUI(textBoxObj,showPassword))

		''' add btns & information object into dict '''
		textBoxObj['btnDelete'] = delete
		textBoxObj['btnSave'] = save
		textBoxObj['descriptionLabel'] = descriptionLabelObj


		#### arrangement all the contents ####

		## main panel
		content.grid(row=0, column=0, sticky=(N, S, E, W))

		## top buttons panel   row0
		topButtonFrame.grid(row=0,column=0,columnspan=10,sticky=(N,S,E,W))
		dashboardLabel.grid(row=0,column=0)
		add.grid(row=0,column=1,sticky=(E))
		run.grid(row=0,column=2,sticky=(E))
		otpLbl.grid(row=0,column=3,padx=10,pady=10,sticky=(E))
		otpEntry.grid(row=0,column=4,sticky=(E))


		##mid section - list view   row1
		listLbl.grid(row=1, column=0, sticky=(N, S))
		listFrame.grid(row=2, column=0, rowspan=2, sticky=(N, S, E, W))


		##mid section - user details   row2
		userDetailFrame.grid(row=2, column=5, columnspan=5, rowspan=2, sticky=(N, S, E, W))
		runorderLbl.grid(row=0,column=1)
		runorderEntry.grid(row=0, column=2, columnspan=2, sticky=(E))
		accTypeLbl.grid(row=1,column=1)
		accTypeEntry.grid(row=1,column=2, sticky=(E))
		nameLbl.grid(row=2,column=1)
		nameEntry.grid(row=2, column=2, columnspan=2, sticky=(E))
		passwordLbl.grid(row=3,column=1)
		passwordEntry.grid(row=3, column=2, columnspan=2, sticky=(E))
		goggleAuthLbl.grid(row=4,column=1)
		goggleAuthEntry.grid(row=4, column=2, columnspan=2, sticky=(E))

		## info panel   row4
		informationFrame.grid(row=4,column=0,columnspan=10,sticky=(N,S,E,W))		
		infoLabel.grid(row=0, column=0,pady=10, sticky=(W))
		descriptionLabel.grid(row=0, column=1,padx=10,pady=10,sticky=(N,S,E,W))

		## bottom buttons panel   row5
		bottomButtonFrame.grid(row=5,column=0,columnspan=10,sticky=(N,S,E,W))
		actionLabel.grid(row=0, column=0, sticky=(W))
		clear.grid(row=0,column=1)
		delete.grid(row=0,column=2)
		save.grid(row=0,column=3)
		refresh.grid(row=0,column=4)
		hideInfo.grid(row=0,column=5)

		## config

		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		content.columnconfigure(0, weight=1)
		content.columnconfigure(1, weight=0)
		informationFrame.columnconfigure(1,weight=1)
		# content.columnconfigure(2, weight=3)
		# content.columnconfigure(3, weight=1)
		# content.columnconfigure(4, weight=1)
		# content.rowconfigure(1, weight=1)


		root.geometry("850x450")
		root.wm_title("OAM - Offline Account Manager")
		root.resizable(0, 0) #Don't allow resizing in the x or y direction
		root.mainloop()


