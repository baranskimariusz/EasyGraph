import pandas as pd
import matplotlib; matplotlib.use('TkAgg'); import matplotlib.pyplot as plt; from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk); from matplotlib.figure import Figure
import tkinter as tk; from tkinter import filedialog; from tkinter import *
import sklearn as sk
class EasyGraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EasyGraph")
        screen_width = self.winfo_screenwidth(); screen_height = self.winfo_screenheight()
        ww=950; wh=570
        x = int((screen_width/2) - (ww/2)); y = int((screen_height/2.15) - (wh/2))
        self.geometry(f"{ww}x{wh}+{x}+{y}")
        container = tk.Frame(self)
        container.pack()

        self.button2 = tk.Button(container, text="Load data", width=13, command=self.load_csv)
        self.button2.pack(side="left", padx=10, pady=10)
        
        self.plot_options = ["Line Plot", "Scatter Plot", "Bar Plot"]
        self.selected_option = tk.StringVar()

        self.plot_button = tk.Menubutton(container, text="Plot", width=13)
        self.plot_button.pack(side="left", padx=10, pady=10)

        self.plot_menu = tk.Menu(self.plot_button, tearoff=False)
        self.plot_menu.add_command(label="Line plot", command=self.plot_graph)
        self.plot_menu.add_command(label="Scatter plot", command=self.plot_graph_scatter)
        self.plot_menu.add_command(label="Bar plot", command=self.plot_graph_bar)
        self.plot_menu.add_command(label="Delete graph", command=self.delete_graph)
        self.plot_button.configure(menu=self.plot_menu)

        self.button1 = tk.Button(container, text='Add data', width=13, command=self.add_data)
        self.button1.pack(side="left", padx=10, pady=10)

        self.data = None
        self.stats_button = tk.Button(container, text="Statistics", width=13, command=self.show_stats)
        self.stats_button.pack(side="left", padx=10,pady=10)

        self.button1 = tk.Button(container, text='Close', width=13, command=self.destroy)
        self.button1.pack(side="right", padx=10, pady=10)
    
    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
        if file_path:
            self.data = pd.read_excel(file_path)
    
    def plot_graph(self):
        if self.data is not None:
            num_columns = len(self.data.columns)
            if num_columns < 2:
                tk.messagebox.showerror("Error", "The loaded Excel file must have at least 2 columns.")
                return

            xlabel = tk.simpledialog.askstring("X Label", "Enter the x label:", parent=self)
            ylabel = tk.simpledialog.askstring("Y Label", "Enter the y label:", parent=self)

            figure = Figure(figsize=(5, 5), dpi=100)
            self.canvas = FigureCanvasTkAgg(figure, self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            NavigationToolbar2Tk(self.canvas, self)
            axes = figure.add_subplot()

            for i in range(num_columns):
                axes.plot(self.data.iloc[:, i], label=self.data.columns[i])
            axes.set_xlabel(xlabel)
            axes.set_ylabel(ylabel)
            axes.legend()
        else:
            tk.messagebox.showerror("Error", "No data has been loaded.")

    def plot_graph_scatter(self):
        if self.data is not None:
            if len(self.data.columns) < 2:
                tk.messagebox.showerror("Error", "The loaded Excel file must have at least 2 columns.")
                return

            figure = Figure(figsize=(5, 5), dpi=100)
            self.canvas = FigureCanvasTkAgg(figure, self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            NavigationToolbar2Tk(self.canvas, self)
            axes = figure.add_subplot()
            x_values = range(0, len(self.data))
            axes.scatter(x_values, self.data.iloc[:, 0], label=self.data.columns[0])
            axes.scatter(x_values, self.data.iloc[:, 1], label=self.data.columns[1])
            axes.legend()
            axes.set_xlabel("Observations")
            axes.set_ylabel(self.data.columns[1])
            axes.set_xlim([0, len(self.data)])
        else:
            tk.messagebox.showerror("Error", "No data has been loaded.")

    def plot_graph_bar(self):
        if self.data is not None:
            if len(self.data.columns) < 2:
                tk.messagebox.showerror("Error", "The loaded Excel file must have at least 2 columns.")
                return
    
            figure = Figure(figsize=(5, 5), dpi=100)
            self.canvas = FigureCanvasTkAgg(figure, self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            NavigationToolbar2Tk(self.canvas, self)
            axes = figure.add_subplot()
            x_values = range(len(self.data))
            y_values1 = self.data.iloc[:, 0]
            y_values2 = self.data.iloc[:, 1]
            axes.bar(x_values, y_values1, label=self.data.columns[0])
            axes.bar(x_values, y_values2, label=self.data.columns[1])
            axes.set_xlabel("Observation")
            axes.set_ylabel("Value")
            axes.set_title("Bar Graph")
            axes.legend()
        else:
            tk.messagebox.showerror("Error", "No data has been loaded.")
    
    def delete_graph(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        else:
            tk.messagebox.showinfo("Information", "No graph is currently displayed.")

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

    def add_data(self):
        if self.data is not None:
            variable_name = tk.simpledialog.askstring("Name", "Enter name of the new variable: ", parent=self)
            for i in range(len(self.data)):
                new_data = tk.simpledialog.askstring("Input", f"Enter data for row {i+1}: ", parent=self)
                self.data.loc[i, variable_name] = new_data
            #self.data.update(new_data, overwrite=True, errors='ignore')
        else:
            tk.messagebox.showerror("Error", "No data has been loaded.")

if __name__ == "__main__":
    app = EasyGraphApp()
    app.mainloop()