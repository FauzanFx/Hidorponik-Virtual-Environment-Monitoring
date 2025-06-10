# main.py

import tkinter as tk
from model import Model
from view import View
from controller import Controller
from environment import HydroponicEnvironment

class App:
    def __init__(self, root):
        """Inisialisasi aplikasi MVC."""
        # Buat instance dari setiap komponen
        self.environment = HydroponicEnvironment()
        self.model = Model()
        
        # Controller membutuhkan referensi ke model dan environment
        self.controller = Controller(self.model, None, self.environment)
        
        # View membutuhkan referensi ke root window dan controller
        self.view = View(root, self.controller)
        
        # Sekarang view sudah dibuat, berikan referensinya ke controller
        self.controller.view = self.view
        
        # Atur layout view
        self.view.pack(fill=tk.BOTH, expand=True)
        
        # Mulai loop pembaruan data
        self.controller.update_loop()

if __name__ == "__main__":
    # Buat variable root untuk Tkinter
    root = tk.Tk()
    app = App(root)
    root.mainloop()