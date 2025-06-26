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

THEME = {
    'name': 'Professional Military',
    'primary': PRIMARY_BLUE,
    'secondary': MILITARY_GREEN,
    'background': WHITE,
    'text': TEXT_PRIMARY,
    'accent': SECONDARY_GREEN,
}