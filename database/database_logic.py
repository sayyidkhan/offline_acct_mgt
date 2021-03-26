import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbList = myclient.list_database_names()

databaseName = 'psAccountManagement'
myDb = None
myCol = None

if databaseName not in dbList:
	print("database does not exist, initalise database...")
	# Important: In MongoDB, a database & collection is not created until it gets content!
	mydb = myclient[databaseName]
	myCol = mydb['accounts']

	initDummyRecord = {
	'runOrder': '1',
	'acctType': 'Not specified',
	'myUsername':'lorem',
	'password': 'password123',
	'googleAuthKey' : 'googleauthkey123',
	}
	myCol.insert_one(initDummyRecord)

else:
	print("database exist, reuse the existing database...")
	mydb = myclient[databaseName]
	myCol = mydb['accounts']

class DbOperations:
	
	@staticmethod
	def getAllRecordsDict():
		allRecords = myCol.find({},{"_id": 0,}).sort('runOrder')
		return allRecords

	@staticmethod
	def getTableRecords():
		allRecords = myCol.find({},{"_id": 0,"runOrder": 1,"acctType": 1,"myUsername" : 1,}).sort('runOrder')
		allRecords = list(allRecords)
		tableRecords = []
		for myDict in allRecords:
			currIteration = []
			currIteration.append(myDict['runOrder'])
			currIteration.append(myDict['acctType'])
			currIteration.append(myDict['myUsername'])
			currIteration.append('')
			tableRecords.append(currIteration)
		return tableRecords

	@staticmethod
	def getOneRecord(myAcctType,myUsername):
		record = myCol.find_one({"myUsername" : myUsername, "acctType" : myAcctType},{"_id": 0})
		if(record == None):
			record = {
			'runOrder' : '',
			'acctType' : '',
			'myUsername' : '',
			'password' : '',
			'googleAuthKey' : '',
			}
			return record
		else:
			return record

	@staticmethod
	def getOneRecordUsingRunOrder(runOrder):
		record = myCol.find_one({"runOrder" : str(runOrder)},{"_id": 0})
		if(record == None):
			record = {
			'runOrder' : '',
			'acctType' : '',
			'myUsername' : '',
			'password' : '',
			'googleAuthKey' : '',
			}
			return record
		else:
			return record

	@staticmethod
	def createOneNewRecord(myDict):
		try:
			myCol.insert_one(myDict)
			print(f'successfully deleted 1 record, record account type: {myQuery["acctType"]}, username: {myQuery["myUsername"]}')
		except:
			print('error inserting new record...')

	@staticmethod
	def updateRunOrder(myAcctType,myUsername,runOrder):
		record = DbOperations.getOneRecord(myAcctType,myUsername)
		myQuery = {"myUsername" : record['myUsername']}
		newValues = {'$set' : {'runOrder' : str(runOrder)} }
		myCol.update_one(myQuery,newValues)

	@staticmethod
	def deleteOneRecord(myAcctType,myUsername):
		try:
			myQuery = {"myUsername" : myUsername, "acctType" : myAcctType}
			myCol.delete_one(myQuery)
			print(f'successfully deleted 1 record, record account type: {myQuery["acctType"]}, username: {myQuery["myUsername"]}')
			return 'OK'
		except:
			print('error inserting new record...')
			return None

	@staticmethod
	def updateOneRecord_new(myDict,currSelectedData):
		acctType = currSelectedData[1]
		myUsername = currSelectedData[2]
		myQuery = {'myUsername' : myUsername, 'acctType' : acctType}
		newValues = {
		'$set' : {
		'runOrder' : myDict['runOrder'],
		'acctType' : myDict['acctType'],
		'myUsername' : myDict['myUsername'],
		'password' : myDict['password'],
		'googleAuthKey' : myDict['googleAuthKey'],
		}}
		myCol.update_one(myQuery,newValues)

	@staticmethod
	def updateOneRecord(myDict,currentSelectedData):

		def checkSwapOrder(myQuery,newValues,successStatement):
			currentSwapOrder = myDict['runOrder']
			originalswapOrder = currentSelectedData[0]
			if(int(currentSwapOrder) == int(originalswapOrder)):
				''' user did not swap the order '''
				myCol.update_one(myQuery,newValues)
				print(successStatement)
			else:
				''' user swap the order '''
				record = DbOperations.getOneRecordUsingRunOrder(currentSwapOrder)
				''' only swap if number exist within range '''
				if(record['myUsername'] != ''):
					''' update the run order of the number which i am going to swap with '''
					DbOperations.updateRunOrder(record['myUsername'],originalswapOrder)
					myCol.update_one(myQuery,newValues)
					print(successStatement)
				else:
					''' user is trying to swap a record out of range '''
					print('user is trying to swap record which is out of range')
					return


		myUsername = myDict['myUsername'].strip()
		if(len(myUsername) != 0):
			record = DbOperations.getOneRecord(myDict['myUsername'])
			if(len(record['myUsername']) != 0):
				''' user is not editing the username '''
				myQuery = {"myUsername" : myDict['myUsername']}
				newValues = {
				'$set' : {
				'runOrder' : myDict['runOrder'],
				'acctType' : myDict['acctType'],
				'myUsername' : myDict['myUsername'],
				'password' : myDict['password'],
				'googleAuthKey' : myDict['googleAuthKey'],
				}}
				successStatement = f'successfully updated 1 record, record username: {myQuery["myUsername"]}'
				checkSwapOrder(myQuery,newValues,successStatement)
				print()
			else:
				''' if the user is editing the username '''
				originalMyUsername = currentSelectedData[1]
				myQuery = {"myUsername" :  originalMyUsername }
				newValues = {
				'$set' : {
				'runOrder' : myDict['runOrder'],
				'acctType' : myDict['acctType'],
				'myUsername' : myDict['myUsername'],
				'password' : myDict['password'],
				'googleAuthKey' : myDict['googleAuthKey'],
				}}
				successStatement = f'successfully updated and edited username of 1 record, new record username: {myDict["myUsername"]}'
				checkSwapOrder(myQuery,newValues,successStatement)






