from ._imports import *

class Logger:
    def __init__(
            self,
            title: str = "DBASE",
            log_file: Optional[str] = None,
            log_format: Optional[str] = None,
            time_format: str = "%Y-%m-%d %H:%M:%S"
    ):
        self.title = title
        self.log_file = log_file
        self.time_format = time_format
        self.format = log_format or "[{time}] [{level}] [{title}] {message}"
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
            with open(os.path.join(self.log_dir, self.log_file), "a") as f:
                f.write(log_entry + "\n")

    def info(self, message: str):
        self.log(message, "INFO")

    def warning(self, message: str):
        self.log(message, "WARNING")

    def error(self, message: str):
        self.log(message, "ERROR")