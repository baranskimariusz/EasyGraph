import pandas as pd
import tkinter as tk

class EasyGraph():
    main=tk.Tk()
    main.title('EasyGraph')
    button1 = tk.Button(main, text='Close', width=25, command=main.destroy)
    button1.pack()
    main.mainloop()

EasyGraph()