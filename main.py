from application import Application
from search import Search
from data import Data

if __name__ == "__main__":
	app = Application() #Object of GUI
	data_main_frame_widget = Data(app.main_frame) #Object of widget for demonstating scv data
	search_main_frame_widget = Search(app.main_frame, data_main_frame_widget) #Object of widgets for navigating through scv data
	
	app.mainloop() #Infinite event loop with response to users actions