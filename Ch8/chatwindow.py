import tkinter as tk
import tkinter.ttk as ttk


class ChatWindow(tk.Toplevel):
    def __init__(self, master, friend_name, friend_avatar, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.title(friend_name)
        self.geometry('520x640')

        self.messages_area = tk.Canvas(self, bg="white")

        self.left_frame = tk.Frame(self.messages_area)
        self.right_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self.messages_area)

        self.scrollbar = ttk.Scrollbar(self.messages_area, orient='vertical', command=self.messages_area.yview)
        self.messages_area.configure(yscrollcommand=self.scrollbar.set)

        self.text_area = tk.Text(self.bottom_frame, bg="white", fg="black", height=3, width=20)
        self.send_button = ttk.Button(self.bottom_frame, text="Send", command=self.send_message, style="send.TButton")

        self.profile_picture = tk.PhotoImage(file="images/avatar.png")
        self.friend_profile_picture = tk.PhotoImage(friend_avatar)

        self.profile_picture_area = tk.Label(self.right_frame, image=self.profile_picture, relief=tk.RIDGE)
        self.friend_profile_picture_area = tk.Label(self.right_frame, image=self.friend_profile_picture, relief=tk.RIDGE)

        self.messages_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.canvas_frame = self.messages_area.create_window((4, 4), window=self.left_frame, anchor="nw")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.right_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.profile_picture_area.pack(side=tk.BOTTOM)
        self.friend_profile_picture_area.pack(side=tk.TOP)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.pack(side=tk.LEFT, fill=tk.X, expand=1, pady=5)
        self.send_button.pack(side=tk.RIGHT, pady=5)

        self.configure_styles()
        self.bind_events()

    def bind_events(self):
        self.bind('<Configure>', self.on_frame_resized)
        self.messages_area.bind('<Configure>', self.chat_width)

    def send_message(self):
        message = self.text_area.get(1.0, 'end-1c')

        label = ttk.Label(self.left_frame, text=message, anchor=tk.W, style="me.TLabel")
        label.pack(fill=tk.X)

        self.text_area.delete(1.0, tk.END)

    def configure_styles(self):
        style = ttk.Style()
        style.configure("me.TLabel", background='#efefef', foreground="black", padding=15)
        style.configure("send.TButton", background='#ff6600', foreground="black", padding=16)

    def chat_width(self, event):
        canvas_width = event.width
        self.messages_area.itemconfig(self.canvas_frame, width=canvas_width)

    def on_frame_resized(self, event=None):
        self.messages_area.configure(scrollregion=self.messages_area.bbox("all"))


if __name__ == '__main__':
    w = tk.Tk()
    c = ChatWindow(w, 'b', 'images/avatar.png')
    w.mainloop()
