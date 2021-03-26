from tkinter import *
from tkinter import messagebox

import tkinter.font as tkFont
import tkinter.ttk as ttk

import pyotp

class WidgetBox:

    ## update data in widget
    def clearFieldData(textBoxObj):
        textBoxObj['runOrder'].delete(0,'end')
        textBoxObj['acctType'].delete(0,'end')
        textBoxObj['myUsername'].delete(0,'end')
        textBoxObj['password'].delete(0,'end')
        textBoxObj['googleAuthKey'].delete(0,'end')

    def updateFieldData(textBoxObj,updateDict):
        ''' function for updating StringVar '''
        def setInputTextStringVar(stringVar,updatedText):
            stringVar.set(updatedText)

        ''' function for updating entry '''
        def setInputTextEntry(entry,updatedText):
            entry.delete(0,"end")
            entry.insert(0,updatedText)

        ''' fields to be updated '''
        setInputTextEntry(textBoxObj['runOrder'],updateDict['runOrder'])
        setInputTextEntry(textBoxObj['acctType'],updateDict['acctType'])
        setInputTextEntry(textBoxObj['myUsername'],updateDict['myUsername'])
        setInputTextEntry(textBoxObj['password'],updateDict['password'])
        setInputTextEntry(textBoxObj['googleAuthKey'],updateDict['googleAuthKey'])

    def getAllFieldData(textBoxObj):
        newValues = {
        'runOrder' : textBoxObj['runOrder'].get(),
        'acctType' : textBoxObj['acctType'].get(),
        'myUsername' : textBoxObj['myUsername'].get(),
        'password' : textBoxObj['password'].get(),
        'googleAuthKey' : textBoxObj['googleAuthKey'].get(),
        }
        return newValues

    def toggleSaveBtn(textBoxObj):
        myValue = textBoxObj['myUsername'].get().strip()
        if(len(myValue) == 0):
            textBoxObj['btnSave']['state'] = 'disabled'
        else:
            textBoxObj['btnSave']['state'] = 'enabled'

    def toggleDeleteBtn(textBoxObj):
        myValue = textBoxObj['myUsername'].get().strip()
        if(len(myValue) == 0):
            textBoxObj['btnDelete']['state'] = 'disabled'
        else:
            textBoxObj['btnDelete']['state'] = 'enabled'



''' start of username table logic '''
class TableBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self,frame,textBoxObj,dbOperations,otpEntry):
        self.tree = None
        self.frame = frame
        self.tableHeader = ['No','Account Type','Username','----',]
        self.tableData = []
        self.otpEntry = otpEntry
        self._setup_widgets()
        self._build_tree()

        ''' db operations '''
        self.dbOperations = dbOperations

        ''' textbox widget '''
        self.textBoxObj = textBoxObj

        '''account data '''
        self.accData = []

    def _setup_widgets(self):
        # select item
        def selectItem(a):
            if(len(self.tableData) == 0):
                ## do not execute code below, if table data is empty
                return

            ''' update accData '''
            curItem = self.tree.focus()
            curItem = self.tree.item(curItem)
            curItem = curItem['values']
            self.accData = curItem
            print("current record selected: ")
            print(curItem)

            ''' update fields '''
            acctType = self.accData[1]
            username = self.accData[2]
            updateDict = self.dbOperations.getOneRecord(acctType,username) #get record from DB
            WidgetBox.updateFieldData(self.textBoxObj,updateDict)

            ''' update btn logic '''
            WidgetBox.toggleSaveBtn(self.textBoxObj)
            WidgetBox.toggleDeleteBtn(self.textBoxObj)

            ''' update info box '''
            self._getInfoBox().setInfoText(f'Account selected: {acctType}, Username Selected: {username}')


        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=self.tableHeader, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.frame)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.frame)
        hsb.grid(column=0, row=1, sticky='ew', in_=self.frame)

        self.tree.bind('<ButtonRelease-1>', selectItem)
        self.tree.bind('<Return>', selectItem)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

    def _delAllRowInTree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def _rebuild_count_order(self):
        if(len(self.tableData) != 0):
            count = 1
            for row in self.tableData:
                ''' db operations, update counter '''
                acctType = row[1] #get acctType
                username = row[2] #get username
                self.dbOperations.updateRunOrder(acctType,username,count) # update run order

                ''' update array '''
                row[0] = count
                count += 1

    def _build_tree(self):
        for col in self.tableHeader:
            self.tree.heading(col, text=col.title(),)
            # adjust the column's width to the header string
            self.tree.column(col,width=tkFont.Font().measure(col.title()))

        ''' custom feature here '''
        self._delAllRowInTree() #always delete record, before rebuilding
        self._rebuild_count_order() #always rebuild run order, before rebuilding

        for item in self.tableData:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.tableHeader[ix],width=None)<col_w:
                    self.tree.column(self.tableHeader[ix], width=col_w)

    def _getInfoBox(self):
        return self.textBoxObj['descriptionLabel']

    ## logic need to fix
    def addRecord(self):
        username = self.textBoxObj['myUsername']
        acctType = self.textBoxObj['acctType']
        ''' only add if account type and username not blank '''
        if( username.get() == '' and acctType.get() == '' ):
            self._getInfoBox().setErrorText('unable to create a new record due to username / account type is blank')
        else:

            checkForRecord = self.dbOperations.getOneRecord(acctType.get(),username.get())
            ''' if exist prevent adding of new record '''
            if(checkForRecord['myUsername'] != ''):
                self._getInfoBox().setErrorText('unable to create a duplicate record of same account type and username')
            else:
                highestRunOrder = self.tableData[-1][0]
                self.tableData.append([str(highestRunOrder + 1),acctType.get(),username.get(),'N/A'])

                ''' insert new record into DB '''
                latestRecord = self.tableData[-1] #get latest record
                try:
                    record = WidgetBox.getAllFieldData(self.textBoxObj)
                    self.dbOperations.createOneNewRecord(record)
                    ''' update info box '''
                    self._getInfoBox().setSuccessText(f'added a new record with username: {username.get()}')
                except:
                    self._getInfoBox().setErrorText('unable to create a new record')


        self._build_tree()
        ''' update btn logic '''
        WidgetBox.toggleSaveBtn(self.textBoxObj)

    def deleteCurrRow(self):
        infoCount = 0
        validateAcctType = ''
        validateUsername = ''

        ''' if record left one, cannot remove '''
        if(len(self.tableData) == 1):
            self._getInfoBox().setWarningText('Cannot remove last record')
            return
        else:
            ''' delete row '''
            for row in self.tableData:
                ''' content to validate against '''
                acctType = self.accData[1]
                username = self.accData[2]

                validateAcctType = row[1]
                validateUsername = row[2]
                if(acctType == validateAcctType and username == validateUsername):
                    self.tableData.remove(row)
                    ''' db operation '''
                    try:
                        self.dbOperations.deleteOneRecord(acctType,username) # delete record
                        infoCount = 1
                    except:
                        self._getInfoBox().setErrorText('unable to delete the record')
                        infoCount = 2

            ''' remove selection '''
            self.clearcurrSelection()
            ''' rebuild ui '''
            self._build_tree()

            ''' info box message '''
            if(infoCount == 1):
                self._getInfoBox().setSuccessText(f'successfully deleted 1 record, record account type: {validateAcctType}, username: {validateUsername}')
            elif(infoCount == 2):
                self._getInfoBox().setErrorText('unable to delete the record')

    def refreshTable(self):
        self.clearcurrSelection()
        self.updateTable()

    def clearcurrSelection(self):
        ''' remove all fields '''
        WidgetBox.clearFieldData(self.textBoxObj)

        ''' remove focus '''
        self.tree.selection_clear()

        ''' purge data '''
        self.accData = []

        '''  btn logic '''
        WidgetBox.toggleSaveBtn(self.textBoxObj)
        WidgetBox.toggleDeleteBtn(self.textBoxObj)

        ''' update info box '''
        self._getInfoBox().clearText()


    def updateTable(self):
        self.tableData = self.dbOperations.getTableRecords() # gets all the records from the database
        self._build_tree()


    def updateRecord(self):
        record = WidgetBox.getAllFieldData(self.textBoxObj)
        selectedAcctType = self.accData[1]
        selectedUsername = self.accData[2]
        if( record['myUsername'] == '' or record['acctType']):
            self._getInfoBox().setErrorText(f'Account type or username is empty')
        ''' if user is not editing username and account type '''
        if( selectedUsername == record['myUsername'] and selectedAcctType == record['acctType'] ):
            self.dbOperations.updateOneRecord_new(record,self.accData) ## update db record
            self._getInfoBox().setSuccessText(f'account updated with no changes to the account: {selectedAcctType}\n username: {selectedUsername} please refresh before proceeding')
        else:
            ''' check if the user is changing to a username that exist '''
            myUsername = record['myUsername']
            acctType = record['acctType']

            for row in self.tableData:
                currAcctType = row[1]
                currUsername = row[2]

                if( currUsername == record['myUsername'] and currAcctType == record['acctType'] ):
                    self._getInfoBox().setErrorText(f'User trying to update to a username/account that exist')
                    return

            self.dbOperations.updateOneRecord_new(record,self.accData)
            self._getInfoBox().setSuccessText(f'account updated with changes to the account/username,\n please refresh before proceeding')

        self.updateTable()

    def generateOTP(self):
        ''' function for updating entry '''
        def setInputTextEntry(entry,updatedText):
            entry.delete(0,"end")
            entry.insert(0,updatedText)

        if(self.textBoxObj['googleAuthKey'].get() == ''):
            self._getInfoBox().setErrorText(f'google auth key is not added for this record')
            return

        secret_key = self.textBoxObj['googleAuthKey'].get()
        otpGenerated = ""
        try:
            totp = pyotp.TOTP(secret_key)
            otpGenerated = totp.now()
            print("Current OTP:", otpGenerated)
            setInputTextEntry(self.otpEntry,otpGenerated)
        except:
            printStr = "OTP not success"
            print(printStr)
            self._getInfoBox().setErrorText(printStr)
        return otpGenerated


''' end of username table logic '''

''' start of infobox logic '''
class InfoBox:

    outcomeSelection = ("SUCCESS", "ERROR", "WARNING")
    colourSelection = ("Red", "Green","lightblue","orange",'grey')

    def __init__(self,frame):
        self.fg = "white"
        self._text = StringVar()
        self._label = Label(frame, textvariable=self._text,fg=self.fg,bg= 'grey',relief=GROOVE,anchor="w",padx=10,pady=10,height=2, justify=LEFT)

        self._text.set("Welcome to Offiline Account Manager. We aim to help to automatically help you manage your accounts.")
        # self._label['textvariable'] = self._text
        #self._textBox['fg'] = 'blue'

    def getDescriptionBox(self):
        return self._label

    def _setText(self,textInput,color):
        self._label.config(bg=color)
        self._text.set(textInput)

    def setInfoText(self,textInput):
        self._setText(textInput,'#54b0c4')

    def setSuccessText(self,textInput):
        self._setText("SUCCESS, " + textInput,'green')

    def setErrorText(self,textInput):
        self._setText("ERROR, " + textInput,'red')

    def setWarningText(self,textInput):
        self._setText("WARNING, " + textInput,'orange')

    def clearText(self):
        self._setText('','grey')

''' end of infobox logic '''

class TerminalBox:

    outcomeSelection = ("SUCCESS", "ERROR", "WARNING")
    colourSelection = ("Red", "Green", "Yellow",'Grey')

    def __init__(self,textBox):
        self._textBox = textBox
        self._textBox.insert(INSERT,"testtesttest")
        #self._textBox['fg'] = 'blue'

    def getTextBox(self):
        return self._textBox

''' start of tooltip-logic '''  
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw,
                      text=self.text,
                      justify=LEFT,
                      background="#ffffe0",
                      relief=SOLID,
                      borderwidth=1,
                      font=("Verdana", "12", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

''' end of tooltip-logic '''

## for only allowing numeric input
def only_numeric_input(P):
    # checks if entry's value is an integer or empty and returns an appropriate boolean
    if P.isdigit() or P == "":  # if a digit was entered or nothing was entered
        return True
    return False

## Adding combobox drop down list
def initComboboxList(comboBox,array):
    comboBox['values'] = array

def save(entry):
    prompt = messagebox.askokcancel(title = "Confirm",
                                    message = "Do you wish to continue")


