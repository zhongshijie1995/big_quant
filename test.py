import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def buy_sell_power(
        new_buy: int = 1,
        change_buy: int = 1,
        close_sell: int = 1,
        close_buy: int = 1,
        change_sell: int = 1,
        new_sell: int = 1
):
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    fig, ax = plt.subplots()
    labels = ['新多', '多换', '空平', '多平', '空换', '新空']
    colors = ['#FF0000', '#FF6666', '#FF6600', '#66FFFF', '#66FF99', '#66FF00']
    wedges, texts, autotexts = ax.pie(
        [new_buy, change_buy, close_sell, close_buy, change_sell, new_sell],
        labels=labels,
        startangle=90,
        autopct='%.2f%%',
        wedgeprops={'width': 0.3},
        labeldistance=1.15,
        colors=colors
    )
    plt.setp(texts, size=12)
    plt.setp(autotexts, size=12)
    return fig


root = tk.Tk()
root.title("Tkinter with Matplotlib")
fig = buy_sell_power()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
root.mainloop()
