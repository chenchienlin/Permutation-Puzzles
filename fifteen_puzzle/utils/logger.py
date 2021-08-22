# https://gist.github.com/joshbode/58fac7ababc700f51e2a9ecdebe563ad
import sys
import logging
from typing import Optional, Dict

from colorama import Fore, Back, Style


class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""
    
    def __init__(self, *args, colors: Optional[Dict[str, str]]=None, **kwargs) -> None:
        """Initialize the formatter with specified format strings."""
        
        super().__init__(*args, **kwargs)
        
        self.colors = colors if colors else {}
    
    def format(self, record) -> str:
        """Format the specified record as text."""
        
        record.color = self.colors.get(record.levelname, '')
        record.reset = Style.RESET_ALL
        
        return super().format(record)

formatter = ColoredFormatter(
    '{asctime} | {threadName} |{color} {levelname:8} {reset}| {name} | {message}',
    style='{', datefmt='%Y-%m-%d %H:%M:%S',
    colors={
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
    }
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.handlers[:] = []
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def set_log_level(logger, mode):
    if mode == 'debug':
        logger.setLevel(logging.DEBUG)
    elif mode == 'info':
        logger.setLevel(logging.INFO)
    elif mode == 'warning':
        logger.setLevel(logging.WARNING)
    elif mode == 'critical':
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.ERROR)