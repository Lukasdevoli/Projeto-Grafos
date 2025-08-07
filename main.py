import customtkinter as ctk
from interface import Interface

if __name__ == "__main__":
    root = ctk.CTk()
    app = Interface(root)
    root.mainloop()
