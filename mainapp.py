''' frontend '''
from frontend.frontend_ui import MainWindow

''' database '''
from database.database_logic import DbOperations

database = DbOperations()
frontend = MainWindow(dbOperations= database)

frontend.renderUI()