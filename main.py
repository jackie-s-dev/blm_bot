import tkinter as tk
import pyperclip
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

        how_to_use = tk.Label(help_window, text="How to use")
        how_to_use.pack()
        how_to_use_text = ("This application was designed to increase YouTube exposure "
        + "for the Black Lives Matter movement.\n"
        + "In order to use this application to its greatest potential, please "
        + "follow the instructions below: \n"
        + "1: Input your Google username and password into the specified fields.*\n\n"
        + "2: Input tags to increase exposure \n"
        + "   - Press 'Add tags to search!' and then type a tag into the field.\n"
        + "     Once you have types a tag into the field, press 'Submit new tag'.\n"
        + "     You can enter several tags by repeating this process.\n\n"
        + "3: Add comments to tagged videos \n"
        + "   - Press 'Add comment' and enter your comment into the field in the pop-up. \n"
        + "   - Press 'Submit new comment' and ensure that the new comment is appended to \n"
        + "     the main window. \n"
        + "     You can enter several comments by repeating this process \n\n"
        + "4: Start the bot \n"
        + "   - In order to start the bot, simply press 'Click to run'.")
        how_to_use_section = tk.Text(help_window, state='normal', height=5)
        how_to_use_section.pack()
        how_to_use_section.insert(tk.INSERT, how_to_use_text)
        how_to_use_section.configure(state='disabled')

        help = tk.Label(help_window, text="Other help")
        help.pack()
        help_text = ("This application was written within a day by a horrible amateur, and "
        + "thus is riddled with mistakes and bugs. If you have any problems with this "
        + "application, please feel free to contact me through my github: \n"
        + "https://github.com/jackie-s-dev/blm_bot \n\n"
        + "In order to aid in the debug process, please send the 'logs.txt' file "
        + "associated with your session. Please note that the 'logs.txt.' file is "
        + "overwritten each time a new session has begun.\n\n"
        + "You can copy and paste the 'logs.txt' file by pressing the button below.")
        help_text_section = tk.Text(help_window, state='normal', height=5)
        help_text_section.pack()
        help_text_section.insert(tk.INSERT, help_text)
        help_text_section.configure(state='disabled')

        copy_log = tk.Button(help_window, command=self.copy_logs)
        copy_log['text'] = "Copy logs to clipboard."
        copy_log.pack()

    def copy_logs(self):
        """
        Responsible for copying the contents of the logs.txt file
        into the users clipboard.
        """
        log_file = open("logs.txt", "r")
        copy_text = ""
        for line in log_file:
            copy_text = copy_text + line

        pyperclip.copy(copy_text)

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

    def add_tags(self):
        """
        Creates windows for adding tags.
        """
        self.tag_window = tk.Toplevel(self)
        self.tag_window.wm_title("Add tags.")
        self.tag_text = tk.Text(self.tag_window, height=2, width=25)
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
        self.comment_text = tk.Text(self.comment_window, height=3, width=25)
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
    try:
        root.iconphoto(True, tk.PhotoImage(file='./imgs/fist.png'))
    except:
        print("Could not load photo.")
    app = Application(master=root)
    app.mainloop()
