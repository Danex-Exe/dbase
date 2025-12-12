__all__ = ['Logger']

from ._imports import *

class Logger:
    def __init__(self, title: str = 'DBASE', /, log_file: str = None, log_format: str = None, time_format: str = "%Y-%m-%d %H:%M:%S"):
        self.title = title
        self.log_file = log_file
        self.time_format = time_format
        
        time_color = color.rgb_bgcolor(124, 9, 153)
        level_color = color.rgb_bgcolor(81, 9, 153)
        title_color = color.rgb_bgcolor(127, 89, 11)
        message_color = ""
        reset = color.reset
        
        default_format = f"[{time_color}{{time}}{reset}] [{level_color}{{level}}{reset}] [{title_color}{{title}}{reset}] {message_color}{{message}}{reset}"
        
        self.format = log_format or default_format
        self.log_dir = "logs"

        if log_file and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log(self, message: str, level: str = "INFO"):
        log_entry = self.format.format(
            time=time.strftime(self.time_format),
            level=level,
            title=self.title,
            message=message
        )

        print(log_entry)

        if self.log_file:
            with open(os.path.join(self.log_dir, self.log_file), "a", encoding='utf-8') as f:
                f.write(log_entry + "\n")

    def info(self, message: str):
        self.log(message, "INFO")

    def warning(self, message: str):
        self.log(message, "WARNING")

    def error(self, message: str):
        self.log(message, "ERROR")