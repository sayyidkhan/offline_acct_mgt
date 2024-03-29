# OAM - Offline Account Management
<h3>prerequisite</h3>

- MongoDB needs to be installed on your local machine. The version does not matter.

<h3>Manage your account related information online through storing your personal login details offline</h3>
<p>An easy way to manage your storage of your personal accounts on the desktop while able to generate OTP for accounts which require a generated code for it.</p>
<img width="750" alt="app overview" src="https://user-images.githubusercontent.com/22993048/112654421-56556480-8e8a-11eb-8975-ae82386c118b.png">
<br>
<p float='left'>
  <img src="https://user-images.githubusercontent.com/22993048/112653085-0d50e080-8e89-11eb-88b3-4a67407579b6.png" width=200 height=200 />
  <img src="https://user-images.githubusercontent.com/22993048/112653914-d5966880-8e89-11eb-9cd0-41172ed691bf.png" width=500 height=200 />
</p>
<h4>Built with python tkinter(GUI + programming logic's) + pymongo (No-SQL Database)</h4>

## Libraries used:

- tkinter (For building the GUI)
- pyotp (For the generating of OTP)
- pymongo (For the persistence of personal information on the user's harddisk)

## how to run
1. install python first (tkinter will be pre-installed with python)
2. run the commands below in the command line if the libraries are not installed yet
```
pip install pymongo
pip install pyotp
```
3. use your terminal to navigate to the directory folder './offline_acct_mgt' on your computer
4. run these commands below in the terminal
```
python3 mainapp.py
```
5. the app should startup successfully
6. (optional) for dev enthusiast, download mongoDB compass to view the database
<img width="607" alt="Screenshot 2021-03-27 at 8 10 01 PM" src="https://user-images.githubusercontent.com/22993048/112720312-78a5bb80-8f38-11eb-8a27-32eb4d4a72d8.png">
<b>click on the 'Fill in connection fields individually'</b>
<img width="605" alt="Screenshot 2021-03-27 at 8 10 09 PM" src="https://user-images.githubusercontent.com/22993048/112720340-a559d300-8f38-11eb-9ad1-72fc7113eaf6.png">
<b>Ensure all the information is correct before clicking connect!</b>
you should be able to view the database. basic knowledge in mongodb is required to nagivate the database.

## How to use:

### Main Use (Store credentials offline and generate OTP)
<img src='https://user-images.githubusercontent.com/22993048/112718765-06c97400-8f30-11eb-834a-87034623c7eb.gif'>
</p>
<p>User click on the 'Run' Button to generate the OTP on the computer</p>
<h3> User can add new account and username via filling up the info and clicking add button</h3>
<img width='650' src='https://user-images.githubusercontent.com/22993048/112722639-af360300-8f45-11eb-92dc-f4c42f3ac3f5.gif'>
<h3> User can delete existing accounts and username which is no longer in use</h3>
<img width='650' src='https://user-images.githubusercontent.com/22993048/112722888-d5a86e00-8f46-11eb-8a8c-51e7583f896e.gif'>
<h3> User can make edits to existing account with the feature to manage password visibility</h3>
<img width='650' src='https://user-images.githubusercontent.com/22993048/112722943-2b7d1600-8f47-11eb-8e50-48f95fc75e0d.gif'>

