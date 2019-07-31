import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


LARGE_FONT = ('Verdana',12)

DF_FIELDS = ['PRODUCTLINE', 'MONTHNO', 'SALES', 'STATUS', 'QUANTITYORDERED']
DF_FIELDS_INDEX = ['PRODUCTLINE']
DF_FIELDS_COL = ['MONTHNO']
DF_FIELDS_VAL = ['SALES']

dataparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M')
df = pd.read_csv(r'C:\Users\User\Desktop\W DataVis\data.csv', encoding="ISO-8859-1", parse_dates=['ORDERDATE'],
                 date_parser=dataparse)

df['MONTHNO'] = [datetime.strftime(x, '%m') for x in df['ORDERDATE']]
df['MONTHNM'] = [datetime.strftime(x, '%b') for x in df['ORDERDATE']]

pref_panel = df[DF_FIELDS]

pivot = pref_panel.pivot_table(index=DF_FIELDS_INDEX, columns=DF_FIELDS_COL, values=DF_FIELDS_VAL, aggfunc='sum')

class HeatmapApp (tk.Tk): #Create Frame

    def __init__(self, *args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)


        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame): #Main Page + Buttons

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text='Vehicle Sales Plot', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text='Box Plot', activeforeground = "blue",activebackground = "pink",pady=10, command=lambda: controller.show_frame(PageOne))
        button1.pack(padx = 1, pady=20, side=tk.TOP)

        button2 = tk.Button(self, text='Heat Map', command=lambda: controller.show_frame(PageTwo))
        button2.pack(padx = 1, pady=20, side=tk.TOP)

        button3 = tk.Button(self, text='Scatter Plot', command=lambda: controller.show_frame(PageThree))
        button3.pack(padx = 1, pady=20, side=tk.TOP)

        button4 = tk.Button(self, text='Violin Swarm Plot', command=lambda: controller.show_frame(PageFour))
        button4.pack(padx = 1, pady=20, side=tk.TOP)


class PageOne(tk.Frame): #Boxplot

    def create_plot():

        f, ax = plt.subplots(figsize=(9, 6))
        sns.boxplot(data=pref_panel)

        return f


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Box Plot', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

        fig = PageOne.create_plot()

        canvas = FigureCanvasTkAgg(fig, self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely = 0.2, relwidth=0.75, relheight=0.75, anchor = 'n')


class PageTwo(tk.Frame): #Heatmap

    def create_plot():

        f, ax = plt.subplots(figsize=(9, 6))
        sns.heatmap(pivot, annot=False, fmt='.0f', linewidths=0, square=True, xticklabels=True, cmap='rocket_r')

        return f

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Heat Map', font=LARGE_FONT)
        label.pack(pady=5, padx=5)

        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

        fig = PageTwo.create_plot()

        canvas = FigureCanvasTkAgg(fig, self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely = 0.1, relwidth=1, relheight=0.75, anchor = 'n')



class PageThree(tk.Frame): #Scatter Plot

    def create_plot():

        f, ax = plt.subplots(figsize=(9, 6))
        sns.scatterplot(x="QUANTITYORDERED", y="SALES",
                        palette="ch:r=-.2,d=.3_r",
                        sizes=(1, 8), linewidth=0, data=pref_panel)

        return f

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Scatter Plot', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

        fig = PageThree.create_plot()

        canvas = FigureCanvasTkAgg(fig, self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely = 0.2, relwidth=0.75, relheight=0.75, anchor = 'n')


class PageFour(tk.Frame): #Violin-Swarm Plot

    def create_plot():

        f, ax = plt.subplots(figsize=(9, 6))
        sns.violinplot(x='PRODUCTLINE', y='SALES', data=pref_panel, inner=None)

        sns.swarmplot(x='PRODUCTLINE', y='SALES', data=pref_panel, hue='MONTHNO')

        plt.legend(bbox_to_anchor=(1, 1), loc=2)

        return f

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Violin Swarm Plot', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

        fig = PageFour.create_plot()

        canvas = FigureCanvasTkAgg(fig, self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely = 0.2, relwidth=0.75, relheight=0.75, anchor = 'n')


def main():

    root = HeatmapApp()
    root.geometry("1200x600")
    root.mainloop()


if __name__ == '__main__':
    main()