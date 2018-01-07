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
        self.text_area.bind("<MouseWheel>", self.scroll_text)
        self.text_area.bind("<Button-4>", self.scroll_text)
        self.text_area.bind("<Button-5>", self.scroll_text)

    def scroll_text(self, *args):
        try:
            self.text_area.yview_moveto(args[1])
        except IndexError:
            event = args[0]
            if event.delta:
                move = -1 * (event.delta / 120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1

            self.text_area.yview_scroll(int(move), "units")


if __name__ == '__main__':
    mw = MainWindow()
    mw.mainloop()

