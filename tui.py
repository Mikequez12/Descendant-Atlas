import os
import sys
import re

from colorist import Effect, Color


if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty

from utils import unicode_supported

_default_pointer = '❯' if unicode_supported else '>'


def _read_key():
    if os.name == "nt":
        while True:
            c = msvcrt.getch()

            if c in (b"\x00", b"\xe0"):
                k = msvcrt.getch()
                return {
                    b"H": "UP",
                    b"P": "DOWN",
                    b"K": "LEFT",
                    b"M": "RIGHT",
                }.get(k)

            if c == b"\r":
                return "ENTER"

            if c == b" ":
                return "SPACE"

            if c == b"\x1b":
                return "ESC"

    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            c = sys.stdin.read(1)

            if c == "\x1b":
                seq = sys.stdin.read(2)
                return {
                    "[A": "UP",
                    "[B": "DOWN",
                    "[C": "RIGHT",
                    "[D": "LEFT",
                }.get(seq, "ESC")

            if c == "\r":
                return "ENTER"

            if c == " ":
                return "SPACE"

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def cls(n):
    print(f"\x1b[{n}F", end="")

def choose(
    options,
    *,
    title='',
    pointer=f"{_default_pointer} {Effect.REVERSE}",
    header=None,
    clear=True,
    wrap=True,
    pad='  ',
    return_index=False,
    on_select_pointer=f" {_default_pointer}{Effect.REVERSE}"
):
    if len(options) == 0:return None

    values = None
    if isinstance(options,dict):
        values = list(options.values())
        options = list(options.keys())

    add = 1 + bool(title is not None) + bool(header)

    index = 0

    ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

    def ansi_truncate(text, width):
        out = []
        visible = 0
        i = 0

        while i < len(text):
            m = ANSI_RE.match(text, i)

            if m:
                out.append(m.group())
                i = m.end()
                continue

            if visible >= width:
                break

            out.append(text[i])
            visible += 1
            i += 1

        if i < len(text):
            out.append("…")

        out.append(Effect.OFF)
        return "".join(out)

    print('\n' * ((add - 1) + len(options)))
    def render(index,last):
        cols,rows = os.get_terminal_size()
        
        if clear:
            cls(len(options) + add)
            
        if title is not None:
            print(f'╭╴{title}')

        if header:
            t = f'│{pad}{Effect.UNDERLINE+Effect.BOLD}{header}{Effect.OFF}'
            if (len(ANSI_RE.sub("", t)) > cols):
                t = ansi_truncate(t, cols - 1)
            print(t)
        for i, option in enumerate(options):
            if i == index:
                italic = "\x1b[3m" if last else ""
                t = f'│{(on_select_pointer if last else pointer)+italic} {option} {Effect.OFF}'
            else:
                t = f'│{Effect.DIM if i%2==1 else ""}{pad} {option} {Effect.OFF}'

            if (len(ANSI_RE.sub("", t)) > cols):
                t = ansi_truncate(t, cols - 1)
            print(t)
        print('╰╴')

    while True:
        render(index,False)
        
        key = _read_key()

        if key == "UP":
            if wrap:
                index = (index - 1) % len(options)
            elif index:
                return -1

        elif key == "DOWN":
            if wrap:
                index = (index + 1) % len(options)
            elif index < len(options) - 1:
                return 1
        elif key in ("ENTER", "SPACE"):
            render(index,True)
            if return_index:
                return index
            if values:
                return values[index]
            return options[index]

        elif key == "ESC":
            print('\n'*(len(options) + add))
            raise KeyboardInterrupt
        



def choose_select(
    options : dict,
    *,
    title=None,
    pointer=f"{_default_pointer} {Effect.REVERSE}",
    header=None,
    clear=True,
    wrap=True,
    pad='  ',
    return_index=False,
    render_index=None,
    return_metadata=None,
    on_select_pointer=f" {_default_pointer}{Effect.REVERSE}"
):
    if len(options) == 0:return {}

    add = 2 + bool(header)

    index = 0
    index_values = {k:0 for k in options }

    ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

    def ansi_truncate(text, width):
        out = []
        visible = 0
        i = 0

        while i < len(text):
            m = ANSI_RE.match(text, i)

            if m:
                out.append(m.group())
                i = m.end()
                continue

            if visible >= width:
                break

            out.append(text[i])
            visible += 1
            i += 1

        if i < len(text):
            out.append("…")

        out.append(Effect.OFF)
        return "".join(out)

    print('\n' * ((add - 1) + len(options)))
    def render(index,last):
        cols,rows = os.get_terminal_size()

        spacing_ = max([len(_) for _ in options]) + 2
        
        if clear:
            cls(len(options) + add)
            
        if title:
            print(f'╭╴{title}')

        if header:
            t = f'│{pad}{Effect.UNDERLINE+Effect.BOLD}{header}{Effect.OFF}'
            if (len(ANSI_RE.sub("", t)) > cols):
                t = ansi_truncate(t, cols - 1)
            print(t)
        for i, (option, value) in enumerate(options.items()):
            if render_index:value = value[render_index]
            value = value[index_values[option]] 
            spacing = spacing_ - len(ANSI_RE.sub("", option))
            if i == index:
                italic = "\x1b[3m" if last else ""
                t = f'│{(on_select_pointer if last else pointer)+italic} {option} {" "*spacing} ❮ {value} ❯ {Effect.OFF} '
            else:
                t = f'│{Effect.DIM if i%2==1 else ""}{pad} {option} {" "*spacing} ❮ {value} ❯ {Effect.OFF} '

            if (len(ANSI_RE.sub("", t)) > cols):
                t = ansi_truncate(t, cols - 1)
            print(t)
        print('╰╴')

    while True:
        render(index,False)
        
        key = _read_key()

        if key == "UP":
            if wrap:
                index = (index - 1) % len(options)
            elif index:
                return -1

        elif key == "DOWN":
            if wrap:
                index = (index + 1) % len(options)
            elif index < len(options) - 1:
                return 1
        elif key == "RIGHT":
            index_values[list(options.keys())[index]] += 1
            index_values[list(options.keys())[index]] %= len(list(options.values())[index])
            render(index,False)
        elif key == "LEFT":
            index_values[list(options.keys())[index]] -= 1
            if index_values[list(options.keys())[index]] == -1:
                index_values[list(options.keys())[index]] = len(list(options.values())[index]) - 1
            render(index,False)
        elif key in ("ENTER", "SPACE"):
            render(index,True)
            if return_metadata is not None:index_values = {k:[v,options[k][return_metadata]] for i,(k,v) in enumerate(index_values.items())}
            if return_index:
                return index_values
            return {k:options[k][v] for k,v in index_values.items()}

        elif key == "ESC":
            print('\n'*(len(options) + add))
            raise KeyboardInterrupt
        


_last_progress_len = 0

def progress(value, total=100, *, width=None, prefix="", suffix="", end_cmd='\n'):
    """
    value: progreso actual
    total: progreso máximo
    width: ancho de la barra (automático si es None)
    """

    global _last_progress_len

    cols = os.get_terminal_size().columns

    ratio = 0 if total == 0 else max(0, min(1, value / total))
    percent = ratio * 100

    if width is None:
        reserved = len(prefix) + len(suffix) + len(" (100.00%) ") + 4
        width = max(10, cols - reserved)

    filled = round(width * ratio)

    bar = "█" * filled + "░" * (width - filled)

    text = f"{prefix}[{bar}] ({percent:6.2f}%) {suffix}{(end_cmd*2) if percent == 100 else ''}"

    padding = max(0, _last_progress_len - len(text))
    print("\r" + text + " " * padding, end="", flush=True)

    _last_progress_len = len(text)

def custom_input(title,prefix=f'{_default_pointer} ',accept=lambda _:True,error_msg='Invalid value',error_format=Color.RED,_as_error=False):
    cols,rows = os.get_terminal_size()

    italic = "\x1b[3m"

    print(f'╭╴{title+(f' {error_format}{italic+error_msg+Effect.OFF}' if _as_error else '')}')
    print('')
    print('╰╴')

    cls(2)

    t = input(f'│ {prefix}')

    if accept(t):
        cls(1)
        print(f'│ {prefix}{Effect.REVERSE+italic}{t}{Effect.OFF}')
        print()
        return t
    else:
        cls(1)
        print(f'| {prefix}'+' '*(cols-len(prefix)-2))
        cls(2)
        return custom_input(title,prefix,accept,error_msg,error_format,_as_error=True)