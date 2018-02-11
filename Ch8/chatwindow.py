import tkinter as tk
import tkinter.ttk as ttk


class ChatWindow(tk.Toplevel):
    def __init__(self, master, friend_name, friend_avatar, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.title(friend_name)
        self.geometry('540x640')
        self.minsize(540,640)


        self.right_frame = tk.Frame(self)
        self.left_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self.left_frame)

        self.messages_area = tk.Text(self.left_frame, bg="white", fg="black", wrap=tk.WORD, width=30)
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient='vertical', command=self.messages_area.yview)
        self.messages_area.configure(yscrollcommand=self.scrollbar.set)

        self.text_area = tk.Text(self.bottom_frame, bg="white", fg="black", height=3, width=30)
        self.send_button = ttk.Button(self.bottom_frame, text="Send", command=self.send_message, style="send.TButton")

        self.profile_picture = tk.PhotoImage(file="images/avatar.png")
        self.friend_profile_picture = tk.PhotoImage(file=friend_avatar)

        self.profile_picture_area = tk.Label(self.right_frame, image=self.profile_picture, relief=tk.RIDGE)
        self.friend_profile_picture_area = tk.Label(self.right_frame, image=self.friend_profile_picture, relief=tk.RIDGE)

        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.left_frame.pack_propagate(0)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.messages_area.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.messages_area.configure(state='disabled')

        self.right_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.profile_picture_area.pack(side=tk.BOTTOM)
        self.friend_profile_picture_area.pack(side=tk.TOP)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.pack(side=tk.LEFT, fill=tk.X, expand=1, pady=5)
        self.send_button.pack(side=tk.RIGHT, pady=5)

        self.configure_styles()
        self.bind_events()

    def bind_events(self):
        self.left_frame.bind('<Configure>', self.on_window_resized)

        self.bind("<Return>", self.send_message)
        self.text_area.bind("<Return>", self.send_message)

    def on_window_resized(self, event):

        if not self.left_frame.cget('width') == event.width - 2000:
            self.left_frame.configure(width=event.width - 2000)
        return "break"

    def send_message(self, event=None):
        message = self.text_area.get(1.0, tk.END)

        if message:
            message = "Me: " + message
            self.messages_area.configure(state='normal')
            self.messages_area.insert(tk.END, message)
            self.messages_area.configure(state='disabled')

            self.text_area.delete(1.0, tk.END)

        return "break"

    def receive_message(self, message):
        label = ttk.Label(self.left_frame, text=message, anchor=tk.W, style="friend.TLabel")
        label.pack(fill=tk.X)

    def configure_styles(self):
        style = ttk.Style()
        style.configure("me.TLabel", background='#efefef', foreground="black", padding=15)
        style.configure("friend.TLabel", background='#ff6600', foreground="black", padding=15)
        style.configure("send.TButton", background='#dddddd', foreground="black", padding=16)

    # def chat_width(self, event):
    #     canvas_width = event.width
    #     self.messages_area.itemconfig(self.canvas_frame, width=canvas_width)
    #
    # def on_frame_resized(self, event=None):
    #     self.messages_area.configure(scrollregion=self.messages_area.bbox("all"))


if __name__ == '__main__':
    w = tk.Tk()
    c = ChatWindow(w, 'b', 'images/avatar.png')
    c.protocol("WM_DELETE_WINDOW", w.destroy)
    w.mainloop()
