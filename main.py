import pandas as pd
import matplotlib; matplotlib.use('TkAgg'); import matplotlib.pyplot as plt; from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk); from matplotlib.figure import Figure
import tkinter as tk; from tkinter import filedialog; from tkinter import *
from sklearn import datasets, linear_model; from sklearn.linear_model import LinearRegression; from sklearn.metrics import mean_squared_error, r2_score
class EasyGraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EasyGraph")
        screen_width = self.winfo_screenwidth(); screen_height = self.winfo_screenheight()
        ww=1100; wh=680
        x = int((screen_width/2) - (ww/2)); y = int((screen_height/2.15) - (wh/2))
        self.geometry(f"{ww}x{wh}+{x}+{y}")
        container = tk.Frame(self)
        container.pack()
        self.canvas = None
        self.line_plot_canvas = None
        self.lin_reg_canvas = None
        self.data = None
        self.line_plot_window = None
        self.lin_reg_window = None

        self.button2 = tk.Button(container, text="Load data", width=11, command=self.load_csv)
        self.button2.pack(side="left", padx=10, pady=10)

        self.button_plot = tk.Button(container, text="Line plot", width=11, command=self.plot_graph)
        self.button_plot.pack(side="left", padx=10, pady=10)

        self.button_linreg = tk.Button(container, text="Linear Regression", width=11, command=self.create_linear_reg)
        self.button_linreg.pack(side="left", padx=10, pady=10)
        
        self.button_del_graph = tk.Button(container, text="Delete graph", width=11, command=self.delete_graph)
        self.button_del_graph.pack(side="left", padx=10, pady=10)

        self.stats_button = tk.Button(container, text="Statistics", width=11, command=self.show_stats)
        self.stats_button.pack(side="left", padx=10,pady=10)

        self.button1 = tk.Button(container, text='Close', width=11, command=self.destroy)
        self.button1.pack(side="right", padx=10, pady=10)
    
    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("XLSX files", "*.xlsx")])
        if file_path:
            self.data = pd.read_excel(file_path)
    
    def plot_graph(self):
        if self.data is not None:
            num_columns = len(self.data.columns)
            if num_columns != 2:
                tk.messagebox.showerror("Error", "The loaded Excel file must have 2 columns.")
                return

            figure = Figure(figsize=(9, 6), dpi=100)
            self.line_plot_window = Toplevel(self)
            self.line_plot_window.title("Line Plot")
            self.line_plot_canvas = FigureCanvasTkAgg(figure, self.line_plot_window)
            self.line_plot_canvas.draw()
            self.line_plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            NavigationToolbar2Tk(self.line_plot_canvas, self.line_plot_window)
            axes = figure.add_subplot()

            for i in range(num_columns):
                axes.plot(self.data.iloc[:, i], label=self.data.columns[i])
            axes.legend()
    
    def create_linear_reg(self):
        if self.data is not None:
            num_columns = len(self.data.columns)
            if num_columns != 2:
                    tk.messagebox.showerror("Error", "The loaded Excel file must have 2 columns.")
                    return

            A = self.data.iloc[:, 0].values.reshape(-1, 1)
            B = self.data.iloc[:, 1].values

            if len(A) < 21:
                tk.messagebox.showerror("Error", "Not enough data points. A minimum of 21 data points is required.")
                return

            A_train = A[:-20]
            B_train = B[:-20]

            A_test = A[-20:]
            B_test = B[-20:]

            lin_reg = linear_model.LinearRegression()
            lin_reg.fit(A_train, B_train)
            pred = lin_reg.predict(A_test)

            figure = Figure(figsize=(9, 6), dpi=100)
            self.lin_reg_window = Toplevel(self)
            self.lin_reg_window.title("Linear Regression")
            self.lin_reg_canvas = FigureCanvasTkAgg(figure, self.lin_reg_window)
            self.lin_reg_canvas.draw()
            self.lin_reg_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            NavigationToolbar2Tk(self.lin_reg_canvas, self.lin_reg_window)
            axes = figure.add_subplot()
            axes.scatter(A_test, B_test)
            axes.plot(A_test, pred)
            axes.legend()
        else:
            tk.messagebox.showerror("Error", "No data has been loaded.")
    
    def delete_graph(self):
        if self.line_plot_window is not None:
            self.line_plot_window.destroy()
            self.line_plot_window = None
        elif self.lin_reg_window is not None:
            self.lin_reg_window.destroy()
            self.lin_reg_window = None
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


if __name__ == "__main__":
    app = EasyGraphApp()
    app.mainloop()