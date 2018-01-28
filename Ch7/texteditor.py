import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg

import yaml

from tkinter import filedialog

from textarea import TextArea
from linenumbers import LineNumbers
from highlighter import Highlighter
from findwindow import FindWindow
from colourchooser import ColourChooser


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Python Text Editor v2')
        self.geometry('800x600')

        self.foreground = 'black'
        self.background = 'lightgrey'
        self.text_foreground = 'black'
        self.text_background='white'

        self.load_scheme_file('schemes/default.yaml')
        self.configure_ttk_elements()

        self.text_area = TextArea(self, bg=self.text_background, fg=self.text_foreground, undo=True)

        self.scrollbar = ttk.Scrollbar(orient="vertical", command=self.scroll_text)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.line_numbers = LineNumbers(self, self.text_area, bg="grey", fg="white", width=1)
        self.highlighter = Highlighter(self.text_area, 'languages/python.yaml')

        self.menu = tk.Menu(self, bg=self.background, fg=self.foreground)
        self.all_menus = [self.menu]

        sub_menu_items = ["file", "edit", "tools", "help"]
        self.generate_sub_menus(sub_menu_items)
        self.configure(menu=self.menu)


        self.right_click_menu = tk.Menu(self, bg="lightgrey", fg="black")
        self.right_click_menu.add_command(label='paste')

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.bind_events()

        self.open_file = ''

    def bind_events(self):
        self.text_area.bind("<MouseWheel>", self.scroll_text)
        self.text_area.bind("<Button-4>", self.scroll_text)
        self.text_area.bind("<Button-5>", self.scroll_text)
        self.text_area.bind("<Button-3>", self.show_right_click_menu)

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

    def show_right_click_menu(self, event):
        print('a')
        self.right_click_menu.post(event.x, event.y)  # TODO get these relative

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
            sub_menu = tk.Menu(self.menu, tearoff=0, bg=self.background, fg=self.foreground)
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
            self.all_menus.append(sub_menu)

    def show_about_page(self):
        msg.showinfo("About", "My text editor, version 2, written in Python3.6 using tkinter!")

    def load_syntax_highlighting_file(self):
        syntax_file = filedialog.askopenfilename(filetypes=[("YAML file", ("*.yaml", "*.yml"))])
        if syntax_file:
            self.highlighter.clear_highlight()
            self.highlighter = Highlighter(self.text_area, syntax_file)
            self.highlighter.force_highlight()

    def load_scheme_file(self, scheme):
        with open(scheme, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                return

        self.foreground = config['foreground']
        self.background = config['background']
        self.text_foreground = config['text_foreground']
        self.text_background = config['text_background']

    def change_colour_scheme(self):
        ColourChooser(self)

    def apply_colour_scheme(self, foreground, background, text_foreground, text_background):
        self.text_area.configure(fg=text_foreground, bg=text_background)
        self.background = background
        self.foreground = foreground
        for menu in self.all_menus:
            menu.configure(bg=self.background, fg=self.foreground)
        self.configure_ttk_elements()

    def configure_ttk_elements(self):
        style = ttk.Style()
        style.configure('editor.TLabel', foreground=self.foreground, background=self.background)
        style.configure('editor.TButton', foreground=self.foreground, background=self.background)



if __name__ == '__main__':
    mw = MainWindow()
    mw.mainloop()

