"""
ANSI color codes for TreeCatt output
"""

import sys


def _supports_color() -> bool:
    """Check if the terminal supports color"""
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True


USE_COLOR = _supports_color()


def c(code: str, text: str) -> str:
    """Wrap text in an ANSI color code if colors are supported"""
    if not USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


# Shortcuts
def dim(text: str) -> str:
    return c("2", text)

def bold(text: str) -> str:
    return c("1", text)

def blue(text: str) -> str:
    return c("34", text)

def cyan(text: str) -> str:
    return c("36", text)

def green(text: str) -> str:
    return c("32", text)

def yellow(text: str) -> str:
    return c("33", text)

def magenta(text: str) -> str:
    return c("35", text)

def red(text: str) -> str:
    return c("31", text)

def white(text: str) -> str:
    return c("37", text)

def bright_blue(text: str) -> str:
    return c("94", text)

def bright_cyan(text: str) -> str:
    return c("96", text)

def bright_green(text: str) -> str:
    return c("92", text)

def bright_yellow(text: str) -> str:
    return c("93", text)

def bright_white(text: str) -> str:
    return c("97", text)