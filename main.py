from application import Application
from search import Search
from data import Data

if __name__ == "__main__":
	app = Application() #object of GUI
	data_main_frame_widget = Data(app.main_frame) #object of widget for demonstating scv data
	search_main_frame_widget = Search(app.main_frame, data_main_frame_widget) #object of widgets for navigating through scv data
	
	app.mainloop() #infinite event loop with response to users actions