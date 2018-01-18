import tkinter as tk
import tkinter.ttk as ttk

from tkinter import filedialog

from textarea import TextArea
from linenumbers import LineNumbers
from highlighter import Highlighter
from findwindow import FindWindow


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.text_area = TextArea(self, bg="white", fg="black", undo=True)

        self.scrollbar = ttk.Scrollbar(orient="vertical", command=self.scroll_text)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.line_numbers = LineNumbers(self, self.text_area, bg="grey", fg="white", width=1)
        self.highlighter = Highlighter(self.text_area, 'languages/python.yaml')

        self.menu = tk.Menu(self, bg="lightgrey", fg="black")
        sub_menu_items = ["file", "edit", "tools", "help"]
        self.generate_sub_menus(sub_menu_items)
        self.configure(menu=self.menu)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.bind_events()

        self.open_file = ''

    def bind_events(self):
        self.text_area.bind("<MouseWheel>", self.scroll_text)
        self.text_area.bind("<Button-4>", self.scroll_text)
        self.text_area.bind("<Button-5>", self.scroll_text)

        self.bind('<Control-f>', self.show_find_window)

        self.line_numbers.bind("<MouseWheel>", lambda e: "break")
        self.line_numbers.bind("<Button-4>", lambda e: "break")
        self.line_numbers.bind("<Button-5>", lambda e: "break")

    def scroll_text(self, *args):
        try:
            self.text_area.yview_moveto(args[1])
            self.line_numbers.yview_moveto(args[1])
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
            self.line_numbers.yview_scroll(int(move), "units")

    def show_find_window(self, event=None):
        FindWindow(self.text_area)

    def file_new(self):
        """
        Ctrl+N
        """
        pass

    def file_open(self):
        """
        Ctrl+O
        """
        file_to_open = filedialog.askopenfilename()
        if file_to_open:
            self.open_file = file_to_open

            self.text_area.display_file_contents(file_to_open)
            self.highlighter.force_highlight()

    def file_save(self):
        """
        Ctrl+S
        """
        pass

    def edit_cut(self):
        """
        Ctrl+X
        """
        self.text_area.event_generate("<Control-x>")

    def edit_paste(self):
        """
        Ctrl+V
        """
        self.text_area.event_generate("<Control-v>")

    def edit_copy(self):
        """
        Ctrl+C
        """
        self.text_area.event_generate("<Control-c>")

    def edit_select_all(self):
        """
        Ctrl+A
        """
        self.text_area.event_generate("<Control-a>")

    def edit_find_and_replace(self):
        """
        Ctrl+F
        """
        self.show_find_window()

    def help_about(self):
        """
        Ctrl+H
        """
        self.show_about_page()

    def tools_change_syntax_highlighting(self):
        """
        Ctrl+M
        """
        self.load_syntax_highlighting_file()

    def tools_change_colour_scheme(self):
        """
        Ctrl+G
        """
        self.change_colour_scheme()

    def generate_sub_menus(self, sub_menu_items):
        window_methods = [method_name for method_name in dir(self)
                          if callable(getattr(self, method_name))]
        tkinter_methods = [method_name for method_name in dir(tk.Tk)
                           if callable(getattr(tk.Tk, method_name))]

        my_methods = [method for method in set(window_methods) - set(tkinter_methods)]

        for item in sub_menu_items:
            sub_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
            matching_methods = []
            for method in my_methods:
                if method.startswith(item):
                    matching_methods.append(method)

            for match in matching_methods:
                actual_method = getattr(self, match)
                method_shortcut = actual_method.__doc__.strip()
                friendly_name = ' '.join(match.split('_')[1:])
                sub_menu.add_command(label=friendly_name.title(), command=actual_method, accelerator=method_shortcut)

            self.menu.add_cascade(label=item.title(), menu=sub_menu)

    def show_about_page(self):
        pass

    def load_syntax_highlighting_file(self):
        pass

    def change_colour_scheme(self):
        pass


if __name__ == '__main__':
    mw = MainWindow()
    mw.mainloop()

