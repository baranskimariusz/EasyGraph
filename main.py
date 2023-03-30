import pandas as pd
import matplotlib; matplotlib.use('TkAgg'); import matplotlib.pyplot as plt; from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk); from matplotlib.figure import Figure
import tkinter as tk; from tkinter import filedialog; from tkinter import *
import sklearn as sk
class EasyGraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EasyGraph")
        screen_width = self.winfo_screenwidth(); screen_height = self.winfo_screenheight()
        ww=900; wh=550
        x = int((screen_width/2) - (ww/2)); y = int((screen_height/2.15) - (wh/2))
        self.geometry(f"{ww}x{wh}+{x}+{y}")
        container = tk.Frame(self)
        container.pack()

        self.button1 = tk.Button(container, text='Close', width=18, command=self.destroy)
        self.button1.pack(side="right", padx=10, pady=10)
        self.button2 = tk.Button(container, text="Load data", width=18, command=self.load_csv)
        self.button2.pack(side="left", padx=10, pady=10)
        self.plot_button = tk.Button(container, text="Plot", width=18, command=self.plot_graph)
        self.plot_button.pack(side="left", padx=10,pady=10)
        self.data = None
        self.stats_button = tk.Button(container, text="Show statistics", width=18, command=self.show_stats)
        self.stats_button.pack(side="left", padx=10,pady=10)
    
    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
        if file_path:
            self.data = pd.read_excel(file_path)
    
    def plot_graph(self):
        if self.data is not None:
            if len(self.data.columns) < 2:
                tk.messagebox.showerror("Error", "The loaded Excel file must have at least 2 columns.")
                return

            xlabel = tk.simpledialog.askstring("X Label", "Enter the x label:", parent=self)
            ylabel = tk.simpledialog.askstring("Y Label", "Enter the y label:", parent=self)

            figure = Figure(figsize=(5, 5), dpi=100)
            canvas = FigureCanvasTkAgg(figure, self)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            NavigationToolbar2Tk(canvas, self)
            axes = figure.add_subplot()
            axes.plot(self.data.iloc[:, 0], label=self.data.columns[0])
            axes.plot(self.data.iloc[:, 1], label=self.data.columns[1])
            axes.set_xlabel(xlabel)
            axes.set_ylabel(ylabel)
            axes.legend()
        else:
            tk.messagebox.showerror("Error", "No data has been loaded.")

    def show_stats(self):
        if self.data is not None:
            stats = self.data.describe()
            popup = Toplevel()
            popup.grab_set()
            text = Text(popup, bd=5, height=10, width=50, bg='black')
            text.pack()
            text.insert(tk.END, stats)
        else:
            tk.messagebox.showerror("Error", "No data has been loaded.")

        
if __name__ == "__main__":
    app = EasyGraphApp()
    app.mainloop()