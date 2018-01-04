import tkinter as tk
import tkinter.ttk as ttk

from textarea import TextArea


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.text_area = TextArea(self, bg="white", fg="black", undo=True)

        self.scrollbar = ttk.Scrollbar(orient="vertical", command=self.scroll_text)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.bind_events()

    def bind_events(self):
        self.bind('')

    def scroll_text(self, command, value):
        self.text_area.yview_moveto(value)


if __name__ == '__main__':
    mw = MainWindow()
    mw.mainloop()

