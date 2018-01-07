import tkinter as tk
import tkinter.ttk as ttk


class FindWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs  )

        self.geometry('400x150')

        self.text_to_find = tk.StringVar()

        self.entry = ttk.Entry(self, textvar=self.text_to_find)

        self.find_button = ttk.Button(self, text="Find", command=self.on_find)
        self.cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)

        self.entry.grid(row=0, column=0, sticky='nswe')
        self.find_button.grid(row=2, column=1)
        self.cancel_button.grid(row=3, column=1)

    def on_find(self):
        self.master.find(self.text_to_find.get())


if __name__ == '__main__':
    mw = tk.Tk()
    fw = FindWindow(mw)
    mw.mainloop()
