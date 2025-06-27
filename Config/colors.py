PRIMARY_BLUE = "#2563eb"      # Modern blue
PRIMARY_DARK = "#1e40af"      # Darker blue for hover states
PRIMARY_LIGHT = "#3b82f6"     # Lighter blue for accents

SECONDARY_GREEN = "#059669"   # Success green
SECONDARY_RED = "#dc2626"     # Error/danger red
SECONDARY_YELLOW = "#d97706"  # Warning orange-yellow
SECONDARY_PURPLE = "#7c3aed"  # Info purple

WHITE = "#ffffff"
LIGHT_GRAY = "#f8fafc"       # Very light background
GRAY_100 = "#f1f5f9"         # Light background
GRAY_200 = "#e2e8f0"         # Border color
GRAY_300 = "#cbd5e1"         # Disabled elements
GRAY_400 = "#94a3b8"         # Placeholder text
GRAY_500 = "#64748b"         # Secondary text
GRAY_600 = "#475569"         # Primary text
GRAY_700 = "#334155"         # Dark text
GRAY_800 = "#1e293b"     
ONXY = "#383D3B"    # Very dark text
BLACK = "#000000"

MILITARY_GREEN = "#4a5d23"    # Military olive green
MILITARY_GRAY = "#5a6c57"     # Military gray-green
NAVY_BLUE = "#1e3a8a"         # Navy blue
KHAKI = "#c8b99c"             # Khaki tan

SUCCESS = SECONDARY_GREEN
ERROR = SECONDARY_RED
WARNING = SECONDARY_YELLOW
INFO = SECONDARY_PURPLE

BUTTON_PRIMARY = PRIMARY_BLUE
BUTTON_PRIMARY_HOVER = PRIMARY_DARK
BUTTON_SECONDARY = GRAY_500
BUTTON_SECONDARY_HOVER = GRAY_600
BUTTON_SUCCESS = SUCCESS
BUTTON_DANGER = ERROR

BG_PRIMARY = WHITE
BG_SECONDARY = LIGHT_GRAY
BG_DARK = GRAY_800
BG_CARD = WHITE
BG_HOVER = GRAY_100

TEXT_PRIMARY = GRAY_800
TEXT_SECONDARY = GRAY_600
TEXT_MUTED = GRAY_400
TEXT_WHITE = WHITE
TEXT_SUCCESS = SUCCESS
TEXT_ERROR = ERROR
TEXT_WARNING = WARNING

BORDER_LIGHT = GRAY_200
BORDER_MEDIUM = GRAY_300
BORDER_DARK = GRAY_400

# Dark theme colors
DARK_BG_PRIMARY = "#1a1a1a"      # Dark primary background
DARK_BG_SECONDARY = "#2d2d2d"    # Dark secondary background
DARK_BG_CARD = "#363636"         # Dark card background
DARK_TEXT_PRIMARY = "#ffffff"    # Dark theme primary text
DARK_TEXT_SECONDARY = "#d1d5db"  # Dark theme secondary text
DARK_TEXT_MUTED = "#9ca3af"      # Dark theme muted text
DARK_GRAY_100 = "#404040"        # Dark gray for inputs
DARK_GRAY_200 = "#525252"        # Dark gray for borders
DARK_GRAY_300 = "#666666"        # Dark gray for disabled
DARK_ONXY = "#e5e5e5"           # Light text for dark backgrounds

COLORS = {
    'primary': PRIMARY_BLUE,
    'primary_dark': PRIMARY_DARK,
    'primary_light': PRIMARY_LIGHT,
    'secondary_green': SECONDARY_GREEN,
    'secondary_red': SECONDARY_RED,
    'secondary_yellow': SECONDARY_YELLOW,
    'secondary_purple': SECONDARY_PURPLE,
    'white': WHITE,
    'black': BLACK,
    'success': SUCCESS,
    'error': ERROR,
    'warning': WARNING,
    'info': INFO,
}

BUTTON_COLORS = {
    'primary': BUTTON_PRIMARY,
    'primary_hover': BUTTON_PRIMARY_HOVER,
    'secondary': BUTTON_SECONDARY,
    'secondary_hover': BUTTON_SECONDARY_HOVER,
    'success': BUTTON_SUCCESS,
    'danger': BUTTON_DANGER,
}

TEXT_COLORS = {
    'primary': TEXT_PRIMARY,
    'secondary': TEXT_SECONDARY,
    'muted': TEXT_MUTED,
    'white': TEXT_WHITE,
    'success': TEXT_SUCCESS,
    'error': TEXT_ERROR,
    'warning': TEXT_WARNING,
}

BACKGROUND_COLORS = {
    'primary': BG_PRIMARY,
    'secondary': BG_SECONDARY,
    'dark': BG_DARK,
    'card': BG_CARD,
    'hover': BG_HOVER,
}

def get_color(color_name, fallback=WHITE):
    
    return COLORS.get(color_name.lower(), fallback)

def get_theme_colors(theme='light'):
    """Get colors based on the current theme"""
    if theme == 'dark':
        return {
            'BG_PRIMARY': DARK_BG_PRIMARY,
            'BG_SECONDARY': DARK_BG_SECONDARY,
            'BG_CARD': DARK_BG_CARD,
            'WHITE': DARK_BG_CARD,
            'GRAY_100': DARK_GRAY_100,
            'GRAY_200': DARK_GRAY_200,
            'GRAY_300': DARK_GRAY_300,
            'GRAY_500': GRAY_500,
            'GRAY_600': GRAY_600,
            'GRAY_700': DARK_TEXT_SECONDARY,
            'ONXY': DARK_ONXY,
            'TEXT_PRIMARY': DARK_TEXT_PRIMARY,
            'TEXT_SECONDARY': DARK_TEXT_SECONDARY,
            'TEXT_MUTED': DARK_TEXT_MUTED,
            'PRIMARY_BLUE': PRIMARY_BLUE,
            'SUCCESS': SUCCESS,
            'ERROR': ERROR,
            'WARNING': WARNING,
        }
    else:  # light theme
        return {
            'BG_PRIMARY': BG_PRIMARY,
            'BG_SECONDARY': BG_SECONDARY,
            'BG_CARD': BG_CARD,
            'WHITE': WHITE,
            'GRAY_100': GRAY_100,
            'GRAY_200': GRAY_200,
            'GRAY_300': GRAY_300,
            'GRAY_500': GRAY_500,
            'GRAY_600': GRAY_600,
            'GRAY_700': GRAY_700,
            'ONXY': ONXY,
            'TEXT_PRIMARY': TEXT_PRIMARY,
            'TEXT_SECONDARY': TEXT_SECONDARY,
            'TEXT_MUTED': TEXT_MUTED,
            'PRIMARY_BLUE': PRIMARY_BLUE,
            'SUCCESS': SUCCESS,
            'ERROR': ERROR,
            'WARNING': WARNING,
        }

THEME = {
    'name': 'Professional Military',
    'primary': PRIMARY_BLUE,
    'secondary': MILITARY_GREEN,
    'background': WHITE,
    'text': TEXT_PRIMARY,
    'accent': SECONDARY_GREEN,
}