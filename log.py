import logging
import os
import time
import sys
from typing import Optional


class Logger(object):
    """
    A simle log class.
    Reference: https://www.cnblogs.com/ltkekeli1229/p/15541941.html

    DEBUG	详细信息，一般只在调试问题时使用。
    INFO	证明事情按预期工作。
    WARNING	某些没有预料到的事件的提示，或者在将来可能会出现的问题提示。例如：磁盘空间不足。但是软件还是会照常运行。
    ERROR	由于更严重的问题，软件已不能执行一些功能了。
    CRITICAL	严重错误，表明软件已不能继续运行了。
    """

    #日志级别关系映射
    level_map = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }
    
    def __init__(self,
                 level: str = "debug",
                 name: Optional[str] = None):
        """
        level: str, 日志级别, 可选值有: ['debug', 'info', 'warning', 'error', crit']
        """

        if level not in self.level_map:
            raise ValueError(f"Invalid log level: {level}. Expected one of: {list(self.level_map.keys())}")
        
        self.level = self.level_map[level]
        self.name = name
        self.logger = logging.getLogger(self.name) if self.name is not None else logging.getLogger()

        # 设置日志的默认级别
        self.logger.setLevel(self.level)

        # 设置日志格式和时间格式
        self.formatter = logging.Formatter(
            fmt='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 设置日志存储目录和文件名
        self.root_dir = os.path.join(os.path.abspath('.'), 'logs')
        self.log_filename = os.path.join(self.root_dir, f"{time.strftime('%Y-%m-%d')}.log")

        # 设置日志文件的handler
        self.logger.addHandler(self.get_file_handler(self.log_filename))
        self.logger.addHandler(self.get_console_handler())


    def get_file_handler(self, filename):
        """
        输出到文件的handler
        """
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        filehandler = logging.FileHandler(filename, encoding="utf-8")
        filehandler.setFormatter(self.formatter)
        return filehandler


    def get_console_handler(self):
        """
        输出到控制台的handler
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler


# Disable OpenAI and httpx logging
# Configure logging level for specific loggers by name
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
# # Disable specific loggers by name
# logging.getLogger("openai").disabled = True
# logging.getLogger("httpx").disabled = True

logger = Logger().logger


""""
How to use:

from log import logger


"""

if __name__ == "__main__":

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')