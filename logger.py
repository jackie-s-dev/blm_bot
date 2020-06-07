import datetime

class Logger():
    def __init__(self, settings):
        """
        Beginning a new log file and appending the current settings to it.
        """
        self.log_file = open("logs.txt", "w")
        for key in settings:
            values = settings[key]
            for value in values:
                self.log_file.write("[ " + key + value + " ]\n")

        self.log_file.write("[ Session Date: " + str(datetime.datetime.now()) + " ]\n")

    def log(self, msg, failure=False):
        """
        Logging new message.
        """
        if failure == False:
            self.log_file.write("[GOOD] " + msg + "\n")
        else:
            self.log_file.write("[WARNING] " + msg + "\n")

    def stop_close(self):
        """
        Closing the log file.
        """
        self.log_file.write("[CLOSING FILE]\n")
        self.log_file.close()
