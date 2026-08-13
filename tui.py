import os
import sys
import re
import json

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty

from utils import unicode_supported, ansi_supported

_default_pointer = '❯'
_default_pointer_rev = '❮'

with open('config.json','r',encoding='utf-8') as file:
    CONFIG = json.load(file)

if (not ansi_supported) or CONFIG.get('.ansi-ldm',False):
    from utils import Color, Effect, Console
else:
    from colorist import Effect, Color
    Effect.italic = "\x1b[3m"

if (not unicode_supported) or CONFIG.get('.unicode-ldm',False):
    if not CONFIG.get('.unicode-ldm',False):
        print('ERROR: This terminal doesn\'t support UNICODE codes. Atlas has a simple system that tries to get rid of UNICODE by default.')
        if input('Do you wanna enable it [Y/N]? ').upper() not in ['YES','Y','1','ACCEPT','OK']:
            print('Aborting...')
            exit(0)
    import sys

    class ASCIIStdout:
        REPLACE = {
            "❯": ">",
            "❮": "<",
            "╭": "+",
            "╰": "+",
            "╮": "+",
            "╯": "+",
            "│": "|",
            "─": "-",
            "█": "#",
            "░": ".",
            "…": "...",
        }

        def __init__(self, real):
            self.real = real

        def write(self, text):
            for old, new in self.REPLACE.items():
                text = text.replace(old, new)
            return self.real.write(text)

        def flush(self):
            return self.real.flush()

        def __getattr__(self, name):
            return getattr(self.real, name)

    sys.stdout = ASCIIStdout(sys.stdout)









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
            
            if c == b".":
                return "."

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
            
            if c == ".":
                return "."

            if c == "\r":
                return "ENTER"

            if c == " ":
                return "SPACE"

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def cls(n=None,w=None,k=None,r=lambda t:print(t,end='')):
    if not ((not ansi_supported) or CONFIG.get('.ansi-ldm',False)):
        t = ''
        if n is not None:t += f"\x1b[{n}F"
        if w is not None:t += f"\x1b[{w}G"
        if k is not None:t += '\x1b[J'
        return r(t)
    else:
        if r != cls.__defaults__[3]:
            return ' '*5
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')
        return ''

def choose(
    options,
    *,
    title='',
    pointer=f"{_default_pointer} {Effect.REVERSE}",
    header=None,
    footer='',
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
                italic = Effect.italic if last else ""
                t = f'│{(on_select_pointer if last else pointer)+italic} {option} {Effect.OFF}'
            else:
                t = f'│{pad} {option} {Effect.OFF}'

            if (len(ANSI_RE.sub("", t)) > cols):
                t = ansi_truncate(t, cols - 1)
            print(t)
        print(f'╰╴{footer}')

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
    on_select_pointer=f" {_default_pointer}{Effect.REVERSE}",
    ch_pointer=_default_pointer,
    rev_ch_pointer=_default_pointer_rev
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
                italic = Effect.italic if last else ""
                t = f'│{(on_select_pointer if last else pointer)+italic} {option} {" "*spacing} {rev_ch_pointer} {value} {ch_pointer} {Effect.OFF}{cls(None,None,0,r=lambda o:o)}'
            else:
                t = f'│{pad} {option} {" "*spacing} {rev_ch_pointer} {value} {ch_pointer} {Effect.OFF}{cls(None,None,0,r=lambda o:o)}'

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

    italic = Effect.italic

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
    

def ask_config(
    default_config={
        'minecraft-launcher-directory':str,
        'minecraft-version':str,
        '.config-version':str,
        '.ansi-ldm':bool,
        '.unicode-ldm':bool
    },config_values:dict=None,
    title='Config',
    pointer=f"{_default_pointer} {Effect.REVERSE}",
    on_select_pointer=f" {_default_pointer}{Effect.REVERSE}",
    clear=True,
    wrap=True,
    pad='  ',
    ch_pointer=_default_pointer,
    rev_ch_pointer=_default_pointer_rev
):
    index = 0

    ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

    config = {k:v for k,v in default_config.items()}

    if config_values:
        for k,v in config_values.items():
            c = default_config.get(k, object)
            if not isinstance(v,c):
                print(f'Invalid type {k}: got {v} expected {c}.')
                config[k] = c
            else:
                config[k] = v

    add = len([k for k in config if not k[0] == '.']) + 2

    spacing_ = max([len(_) for _ in config]) + 2

    print('\n'*(add - 1))

    DEBUG = False

    def handle_input(key,index,default_config):
        """
        config_values[list(config.keys())[index]] += 1
        config_values[list(config.keys())[index]] %= len(list(config.values())[index])
        """
        n = len(vis_config)-index+1
        _ = list(config.keys())[index]
        match default_config[_]:
            case t if t is str:
                if key == 'LEFT':return
                if clear:cls(n,spacing_+len(ANSI_RE.sub("",pointer))+7)
                if config[_] is None:config[_] = 'unset'
                i = len(config[_])
                print('\x1b[0K',end=Effect.REVERSE+' '*i)
                if clear:cls(None,spacing_ + 9)
                new_value = input()
                if clear:cls(index+1,spacing_ + len(new_value) + 9,k=True)
                if new_value == '' and _ not in default_config.keys():
                    del config[_]
                    vis_config.pop(0)
                    index -= 1
                    if index < 0:
                        index = len(vis_config) - 1
                else:
                    config[_] = new_value
                print(Effect.OFF+'\n'*len(vis_config))
                # m = index + 4 - len(config)
            case t if t is bool:
                config[_] = not config[_]

    def render(index,last,DEBUG,avoid_cls=False):
        italic = Effect.italic

        add = len([k for k in config if DEBUG or k[0] != '.']) + 2

        if not avoid_cls and clear:cls(add)
        print(f'╭╴{title}')
        for i,(k,v) in enumerate(config.items()):
            if k[0] == '.' and not DEBUG:continue
            if v is None: v = f'{Effect.DIM+italic}unset{Effect.DIM}'
            if type(v) == bool:
                v = 'Yes' if v else 'No'
                if i == index:
                    v = f'{rev_ch_pointer} {v} {ch_pointer}'
            spacing = spacing_ - len(ANSI_RE.sub("", k))
            print(f'│{(pointer if not last else on_select_pointer) if i == index else pad} {italic if last and i == index else ""}{Effect.DIM if k[0] == "." else ""}{k} {" " * spacing} {v} {Effect.OFF+cls(k=0,r=lambda _:_)}')
        print('╰╴')

    while True:
        render(index,False,DEBUG)
        
        key = _read_key()

        vis_config = [k for k in config if DEBUG or k[0] != '.']

        if key == "UP":
            if wrap:
                index = (index - 1) % len(vis_config)
            elif index:
                return -1

        elif key == "DOWN":
            if wrap:
                index = (index + 1) % len(vis_config)
            elif index < len(vis_config) - 1:
                return 1
        elif key == "RIGHT":
            handle_input('RIGHT',index,default_config)
        elif key == "LEFT":
            handle_input('LEFT',index,default_config)
        elif key == ".":
            add = len([k for k in config if DEBUG and k[0] == '.']) + 4
            if clear:cls(add,k=True)
            DEBUG = not(DEBUG)
            render(index,False,DEBUG,avoid_cls=True)
        elif key in ("ENTER", "SPACE"):
            render(index,True,DEBUG)
            config = {k:None if isinstance(v,type) else v for k,v in config.items()}
        
            return config

        elif key == "ESC":
            raise KeyboardInterrupt