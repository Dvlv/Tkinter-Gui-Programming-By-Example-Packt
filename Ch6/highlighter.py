import tkinter as tk

import yaml


class Highlighter:
    def __init__(self, text_widget, syntax_file):
        self.text_widget = text_widget
        self.syntax_file = syntax_file
        self.categories = None
        self.numbers_colour = "blue"

        self.parse_syntax_file()

        self.text_widget.bind('<KeyRelease>', self.on_key_release)

    def on_key_release(self, event=None):
        self.highlight()

    def parse_syntax_file(self):
        with open(self.syntax_file, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                return

        self.categories = config['categories']
        self.numbers_colour = config['numbers']['colour']

        self.configure_tags()

    def configure_tags(self):
        for category in self.categories.keys():
            colour = self.categories[category]['colour']
            self.text_widget.tag_configure(category, foreground=colour)

        self.text_widget.tag_configure("number", foreground=self.numbers_colour)

    def highlight(self, event=None):
        start = 1.0
        length = tk.IntVar()
        for category in self.categories:
            matches = self.categories[category]['matches']
            for keyword in matches:
                keyword = keyword +  '[^A-Za-z]'
                idx = self.text_widget.search(keyword, start, stopindex=tk.END, count=length, regexp=1)
                while idx:
                    end = f"{idx}+{length.get() - 1}c"
                    self.text_widget.tag_add(category, idx, end)

                    start = end
                    idx = self.text_widget.search(keyword, start, stopindex=tk.END, regexp=1)

        start = 1.0
        idx = self.text_widget.search(r"(\d)+[.]?(\d)*", start, stopindex=tk.END, regexp=1, count=length)
        while idx:
            end = f"{idx}+{length.get()}c"
            self.text_widget.tag_add("number", idx, end)

            start = end
            idx = self.text_widget.search(r"(\d)+[.]?(\d)*", start, stopindex=tk.END, regexp=1, count=length)


if __name__ == '__main__':
    w = tk.Tk()
    h = Highlighter(tk.Text(w), 'languages/python.yaml')
    w.mainloop()



