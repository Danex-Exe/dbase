from __future__ import annotations

__all__ = ['Colors', 'color']

class Colors:
    def __init__(self, esc_type: str = '\033'):
        self.esc_type = esc_type
        
        self.black = f'{self.esc_type}[30m'
        self.red = f'{self.esc_type}[31m'
        self.green = f'{self.esc_type}[32m'
        self.yellow = f'{self.esc_type}[33m'
        self.blue = f'{self.esc_type}[34m'
        self.magenta = f'{self.esc_type}[35m'
        self.cyan = f'{self.esc_type}[36m'
        self.white = f'{self.esc_type}[37m'
        
        self.bright_black = f'{self.esc_type}[90m'
        self.bright_red = f'{self.esc_type}[91m'
        self.bright_green = f'{self.esc_type}[92m'
        self.bright_yellow = f'{self.esc_type}[93m'
        self.bright_blue = f'{self.esc_type}[94m'
        self.bright_magenta = f'{self.esc_type}[95m'
        self.bright_cyan = f'{self.esc_type}[96m'
        self.bright_white = f'{self.esc_type}[97m'
        
        self.bg_black = f'{self.esc_type}[40m'
        self.bg_red = f'{self.esc_type}[41m'
        self.bg_green = f'{self.esc_type}[42m'
        self.bg_yellow = f'{self.esc_type}[43m'
        self.bg_blue = f'{self.esc_type}[44m'
        self.bg_magenta = f'{self.esc_type}[45m'
        self.bg_cyan = f'{self.esc_type}[46m'
        self.bg_white = f'{self.esc_type}[47m'
        
        self.bg_bright_black = f'{self.esc_type}[100m'
        self.bg_bright_red = f'{self.esc_type}[101m'
        self.bg_bright_green = f'{self.esc_type}[102m'
        self.bg_bright_yellow = f'{self.esc_type}[103m'
        self.bg_bright_blue = f'{self.esc_type}[104m'
        self.bg_bright_magenta = f'{self.esc_type}[105m'
        self.bg_bright_cyan = f'{self.esc_type}[106m'
        self.bg_bright_white = f'{self.esc_type}[107m'
        
        self.reset = f'{self.esc_type}[0m'
        self.bold = f'{self.esc_type}[1m'
        self.dim = f'{self.esc_type}[2m'
        self.italic = f'{self.esc_type}[3m'
        self.underline = f'{self.esc_type}[4m'
        self.blink = f'{self.esc_type}[5m'
        self.inverse = f'{self.esc_type}[7m'
        self.hidden = f'{self.esc_type}[8m'
        self.strikethrough = f'{self.esc_type}[9m'
        
        self.reset_bold = f'{self.esc_type}[21m'
        self.reset_dim = f'{self.esc_type}[22m'
        self.reset_italic = f'{self.esc_type}[23m'
        self.reset_underline = f'{self.esc_type}[24m'
        self.reset_blink = f'{self.esc_type}[25m'
        self.reset_inverse = f'{self.esc_type}[27m'
        self.reset_hidden = f'{self.esc_type}[28m'
        self.reset_strikethrough = f'{self.esc_type}[29m'
    

    def color_256(self, code: str | int) -> str:
        return f'{self.esc_type}[38;5;{code}m'
    
    def bg_color_256(self, code: str | int) -> str:
        return f'{self.esc_type}[48;5;{code}m'
    
    
    def rgb_color(self, r: str | int, g: str | int, b: str | int) -> str:
        return f'{self.esc_type}[38;2;{r};{g};{b}m'
    
    def rgb_bgcolor(self, r: str | int, g: str | int, b: str | int) -> str:
        return f'{self.esc_type}[48;2;{r};{g};{b}m'
    

    def cursor_up(self, n: str | int = 1) -> str:
        return f'{self.esc_type}[{n}A'
    
    def cursor_down(self, n: str | int = 1) -> str:
        return f'{self.esc_type}[{n}B'
    
    def cursor_forward(self, n: str | int = 1) -> str:
        return f'{self.esc_type}[{n}C'
    
    def cursor_back(self, n: str | int = 1) -> str:
        return f'{self.esc_type}[{n}D'
    
    def cursor_position(self, row: str | int, col: str | int) -> str:
        return f'{self.esc_type}[{row};{col}H'
    
    def cursor_save(self) -> str:
        return f'{self.esc_type}[s'
    
    def cursor_restore(self) -> str:
        return f'{self.esc_type}[u'
    
    def cursor_hide(self) -> str:
        return f'{self.esc_type}[?25l'
    
    def cursor_show(self) -> str:
        return f'{self.esc_type}[?25h'
    

    def clear_screen(self) -> str:
        return f'{self.esc_type}[2J'
    
    def clear_line(self) -> str:
        return f'{self.esc_type}[2K'
    
    def clear_line_end(self) -> str:
        return f'{self.esc_type}[0K'
    
    def clear_line_start(self) -> str:
        return f'{self.esc_type}[1K'
    
    def color_message(self, message: str, color: str) -> str:
        return f'{color}{message}{self.reset}'
    

    def styled_message(self, message: str, *styles: str) -> str:
        style_str = ''.join(styles)
        return f'{style_str}{message}{self.reset}'
    

    def gradient_text(self, text: str, start_rgb: tuple | list, end_rgb: tuple | list ) -> str:
        result = []
        length = len(text)
        for i, char in enumerate(text):
            ratio = i / max(length - 1, 1)
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            result.append(f'{self.rgb_color(r, g, b)}{char}')
        return ''.join(result) + self.reset

color = Colors()