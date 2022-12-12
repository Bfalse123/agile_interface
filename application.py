#libs for GUI
import tkinter as tk
from tkinterdnd2 import TkinterDnD

class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Zakupki")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
        self.geometry("1200x800")
       #self.search_page = SearchPage(parent=self.main_frame)

#probably add SearchPage hera