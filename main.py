import tkinter as tk
from bot import Bot

BLM_VIDEO = 'https://www.youtube.com/watch?v=bCgLa25fDHM'

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.tags = []
        self.comments = []

    def create_widgets(self):
        username_label = tk.Label(self, text="USERNAME: ")
        username_label.pack()
        self.username = tk.Text(self, height=2, width=30)
        self.username.pack()

        password_label = tk.Label(self, text="PASSWORD: ")
        password_label.pack()
        self.password = tk.Text(self, height=2, width=30)
        self.password.pack()

        # tags
        tags_label = tk.Label(self, text="TAGS: ")
        tags_label.pack()
        self.tags_display = tk.Text(self, state='disabled', height=5,width=30)
        self.tags_display.pack()
        self.add_tag_button = tk.Button(self, command=self.add_tags)
        self.add_tag_button['text'] = "Add tags to search!"
        self.add_tag_button.pack()

        # comments
        comments_label = tk.Label(self, text="COMMENTS: ")
        comments_label.pack()
        self.comments_display = tk.Text(self, state='disabled', height=5,width=30)
        self.comments_display.pack()
        self.add_comments_button = tk.Button(self, command=self.add_comment)
        self.add_comments_button['text'] = "Add comment"
        self.add_comments_button.pack()

        self.run_button = tk.Button(self, command=self.start_bot)
        self.run_button["text"] = "Click to run"
        self.run_button.pack()

        self.info_button = tk.Button(self, command=self.display_info)
        self.info_button['text'] = "Help/View Information"
        self.info_button.pack()

    def display_info(self):
        """
        Displays help information.
        """
        help_window = tk.Toplevel(self)
        help_window.wm_title("Help")

    def start_bot(self):
        """
        Begins the bot based on pre-defined rules.
        """
        self.run_button.destroy()
        username = self.username.get("1.0", 'end-1c')
        password = self.password.get("1.0", 'end-1c')
        comments = self.comments
        tags = self.tags

        # initializing bot
        bot = Bot(comments, tags, BLM_VIDEO)
        bot.login(username, password)
        bot.run(500)

        self.bot_button = tk.Button(self, command=self.stop_bot)
        self.bot_button['text'] = "Stop"
        self.bot_button.pack()

    def add_tags(self):
        """
        Creates windows for adding tags.
        """
        self.tag_window = tk.Toplevel(self)
        self.tag_window.wm_title("Add tags.")
        self.tag_text = tk.Text(self.tag_window, height=5, width=10)
        self.tag_text.pack()

        tag_button = tk.Button(self.tag_window, command=self.new_tag)
        tag_button['text'] = "Submit new tag."
        tag_button.pack()

    def new_tag(self):
        """
        Displays new tag, appends to list, and destroys window.
        """
        tag = self.tag_text.get("1.0", 'end-1c')
        self.tags.append(tag)
        self.tags_display.configure(state='normal')
        self.tags_display.insert(tk.INSERT, (tag + "\n"))
        self.tags_display.configure(state='disabled')
        self.tag_window.destroy()

    def add_comment(self):
        """
        Creates a new windows for adding new comments.
        """
        self.comment_window = tk.Toplevel(self)
        self.comment_window.wm_title("Add comments!")
        self.comment_text = tk.Text(self.comment_window, height=5, width=10)
        self.comment_text.pack()

        comment_button = tk.Button(self.comment_window, command=self.new_comment)
        comment_button['text'] = "Submit new comment."
        comment_button.pack()

    def new_comment(self):
        """
        Creates a new window and destroys the old comment.
        """
        comment = self.comment_text.get("1.0", 'end-1c')
        self.comments.append(comment)
        self.comments_display.configure(state='normal')
        self.comments_display.insert(tk.INSERT, (comment + "\n"))
        self.comments_display.configure(state='disabled')
        self.comment_window.destroy()

    def stop_bot(self):
        """
        Stops the bot and destroys all windows.
        """
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("BLACK LIVES MATTER")
    app = Application(master=root)
    app.mainloop()
