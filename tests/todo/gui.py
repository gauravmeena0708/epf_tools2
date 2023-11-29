import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Create the main window
window = tk.Tk()
window.title("Excel Summary")

# Create a function to open the file dialog and display the summary
def show_summary():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    print("Selected file:", file_path)
    
    # Load the Excel file into a pandas dataframe
    df = pd.read_excel(file_path)
    
    # Display the summary of the dataframe
    summary_text = df.describe().to_string()
    summary_label.config(text=summary_text)

# Create a button to open the file dialog and show the summary
button = tk.Button(text="Browse", command=show_summary)
button.pack()

# Create a label to display the summary
summary_label = tk.Label(text="")
summary_label.pack()

# Run the main loop
window.mainloop()

"""
import tkinter as tk
from tkinter import filedialog

# Create the main window
window = tk.Tk()
window.title("Excel Browser")

# Create a function to open the file dialog
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    print("Selected file:", file_path)

# Create a button to open the file dialog
button = tk.Button(text="Browse", command=browse_file)
button.pack()

# Run the main loop
window.mainloop()
"""