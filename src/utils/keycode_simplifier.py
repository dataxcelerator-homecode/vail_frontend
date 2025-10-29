"""
Keycode simplification and color mapping utilities.
"""

from typing import Tuple


def simplify_keycode(keycode: str) -> str:
    """
    Simplify QMK keycode for display purposes.
    
    Args:
        keycode: Full QMK keycode string
        
    Returns:
        Simplified keycode for display
    """
    # Handle special cases
    if keycode == -1 or keycode == "-1":
        return ""
    
    keycode = str(keycode)
    
    # Remove KC_ prefix for cleaner display
    if keycode.startswith("KC_"):
        keycode = keycode[3:]
    
    # Simplify common modifiers
    replacements = {
        "LSFT": "⇧",
        "LCTL": "⌃",
        "LALT": "⌥",
        "LGUI": "⌘",
        "RSHIFT": "R⇧",
        "RCTRL": "R⌃",
        "TRNS": "▽",  # Transparent key
        "NO": "✗",
    }
    
    for old, new in replacements.items():
        keycode = keycode.replace(old, new)
    
    return keycode


def get_key_color(keycode: str) -> Tuple[str, str]:
    """
    Determine key color based on keycode type.
    
    Args:
        keycode: Simplified keycode
        
    Returns:
        Tuple of (face_color, edge_color)
    """
    if keycode == "▽":  # Transparent
        return '#f0f0f0', '#cccccc'
    elif keycode.startswith("MO(") or keycode.startswith("LT"):
        return '#ffcccc', '#cc0000'  # Layer keys
    elif keycode.startswith("DF("):
        return '#ccccff', '#0000cc'  # Default layer change
    elif any(mod in keycode for mod in ["⇧", "⌃", "⌥", "⌘"]):
        return '#ffffcc', '#cccc00'  # Modifier combos
    else:
        return '#e0e0e0', '#666666'  # Regular keys

