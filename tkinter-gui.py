import tkinter as tk
from tkinter import messagebox
from utils import index
import db

def submit():
    try:
        username = username_entry.get()
        microscope_size = float(microscope_entry.get())
        magnification = float(magnification_entry.get())
        actual_size = index.calculate_actual_size(microscope_size, magnification)
        db.save_to_db(username, microscope_size, actual_size)
        messagebox.showinfo("Result", f"Actual size: {actual_size:.4f} mm")
    except ValueError:
        messagebox.showerror("Error", "Invalid input")

app = tk.Tk()
app.title("Microscope Size Calculator")

tk.Label(app, text="Username").pack()
username_entry = tk.Entry(app)
username_entry.pack()

tk.Label(app, text="Microscope Size (mm)").pack()
microscope_entry = tk.Entry(app)
microscope_entry.pack()

tk.Label(app, text="Magnification").pack()
magnification_entry = tk.Entry(app)
magnification_entry.pack()

tk.Button(app, text="Calculate", command=submit).pack()

app.mainloop()