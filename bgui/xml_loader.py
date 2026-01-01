import xml.etree.ElementTree as ET
import os
from .label import Label
from .widget import Widget
from .slider import Slider
from .frame_button import FrameButton
from .progress_bar import ProgressBar
from .frame import Frame
from .image import Image
from .image_button import ImageButton
from .list_box import ListBox
from .text_block import TextBlock
from .text_input import TextInput
from .video import Video
from .theme import Theme

# Import BGUI constants for options parsing
from .widget import (
    BGUI_DEFAULT,
    BGUI_CENTERX,
    BGUI_CENTERY,
    BGUI_NO_NORMALIZE,
    BGUI_NO_THEME,
    BGUI_NO_FOCUS,
    BGUI_CACHE,
    BGUI_CENTERED
)

# Mapping of flag names to their numeric values
BGUI_FLAG_MAP = {
    'BGUI_DEFAULT': BGUI_DEFAULT,
    'BGUI_CENTERX': BGUI_CENTERX,
    'BGUI_CENTERY': BGUI_CENTERY,
    'BGUI_NO_NORMALIZE': BGUI_NO_NORMALIZE,
    'BGUI_NO_THEME': BGUI_NO_THEME,
    'BGUI_NO_FOCUS': BGUI_NO_FOCUS,
    'BGUI_CACHE': BGUI_CACHE,
    'BGUI_CENTERED': BGUI_CENTERED,
}

# Mapping XML tag names to BGUI widget classes
WIDGET_MAP = {
    'Label': Label,
    'Slider': Slider,
    'Button': FrameButton,
    'ProgressBar': ProgressBar,
    'Frame': Frame,
    'Image': Image,
    'ImageButton': ImageButton,
    'ListBox': ListBox,
    'TextBlock': TextBlock,
    'TextInput': TextInput,
    'Video': Video,
}

def load_ui_from_xml(xml_path, parent, theme=None):
    """
    Carrega uma interface de usuário a partir de um arquivo XML.
    
    :param xml_path: Path to the XML file
    :param parent: Parent widget (usually a System)
    :param theme: Theme or object name. If None, uses the default theme.
    """
    if theme is not None:
        system = parent.system if hasattr(parent, 'system') else parent
        if isinstance(theme, str):
            try:
                from Range import logic
                theme_path = logic.expandPath(f"//bgui/themes/{theme}")
                if not os.path.exists(theme_path):
                    print(f"BGUI WARNING: Theme '{theme}' not found. Using existing theme.")
                else:
                    system.theme = Theme(theme_path)
            except ImportError:
                theme_path = f"themes/{theme}"
                if os.path.exists(theme_path):
                    system.theme = Theme(theme_path)
                else:
                    print(f"BGUI WARNING: Theme '{theme}' not found. Using existing theme.")
        else:
            system.theme = theme
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    widgets = []
    for elem in root:
        widget = create_widget_from_elem(elem, parent)
        if widget:
            widgets.append(widget)
    return {w.name: w for w in widgets if hasattr(w, "name")}

def create_widget_from_elem(elem, parent):
    widget_type = elem.tag
    widget_class = WIDGET_MAP.get(widget_type)
    if not widget_class:
        print(f"Unknown widget type: {widget_type}")
        return None
    
    # Parse all attributes
    parsed_attrs = {k: try_parse_widget_arg(k, v) for k, v in elem.attrib.items()}
    
    # Widget-specific constructor parameter rules
    # Label: no 'size', accepts 'color' in constructor
    # Frame: accepts 'size', no 'color' (use 'colors' property after creation)
    # Button: accepts 'size' and 'text'
    
    if widget_type == 'Label':
        # Label doesn't accept 'size' in constructor
        constructor_kwargs = {k: v for k, v in parsed_attrs.items() if k != 'size'}
        post_props = {}
        # For Label, 'color' goes in constructor, not post-creation
    elif widget_type == 'Frame':
        # Frame accepts most params but 'color' should be 'colors' property
        post_props = {}
        if 'color' in parsed_attrs:
            # Convert single color to 4-corner colors
            color = parsed_attrs.pop('color')
            post_props['colors'] = [color, color, color, color]
        constructor_kwargs = parsed_attrs
    else:
        # For other widgets, use default behavior
        post_creation_props = {'colors', 'border_color', 'text_color', 
                               'fill_color', 'fill_colors', 'highlight_color', 'selection_color',
                               'base_color', 'hover_color', 'click_color'}
        constructor_kwargs = {k: v for k, v in parsed_attrs.items() if k not in post_creation_props}
        post_props = {k: v for k, v in parsed_attrs.items() if k in post_creation_props}
    
    # Create the widget with constructor arguments only
    widget = widget_class(parent, **constructor_kwargs)
    
    # Set post-creation properties
    for k, v in post_props.items():
        if hasattr(widget, k):
            setattr(widget, k, v)
        else:
            print(f"BGUI WARNING: Widget {widget_type} does not have property '{k}'")
    
    # Recursively create children, if any
    for child in elem:
        create_widget_from_elem(child, widget)
    
    return widget

def try_parse_widget_arg(key, value):
    """
    Parse widget arguments from XML attributes.
    
    Special handling for 'options' attribute:
    - Supports named flags (e.g., "BGUI_CENTERX|BGUI_NO_THEME")
    - Supports numeric values (e.g., "9" for BGUI_CENTERX | BGUI_NO_THEME)
    - Multiple flags can be combined with | (pipe) character
    """
    # Special handling for 'options' attribute - support named flags
    if key == "options":
        # Check if value contains named flags (contains letters)
        if any(c.isalpha() for c in value):
            # Parse named flags
            flags = [flag.strip() for flag in value.split("|")]
            result = 0
            for flag in flags:
                if flag in BGUI_FLAG_MAP:
                    result |= BGUI_FLAG_MAP[flag]
                else:
                    print(f"BGUI WARNING: Unknown flag '{flag}'. Available flags: {', '.join(BGUI_FLAG_MAP.keys())}")
            return result
        # Otherwise try to parse as int (numeric value)
        try:
            return int(value)
        except ValueError:
            print(f"BGUI WARNING: Invalid options value '{value}'. Using BGUI_DEFAULT (0).")
            return BGUI_DEFAULT
    
    # Convert comma-separated strings to lists of floats for certain attributes
    if key in ("pos", "size", "base_color", "color", "outline_color", "fill_color", "fill_colors", 
               "border_color", "text_color", "highlight_color", "selection_color"):
        return [float(x) for x in value.split(",")]
    
    # Try to convert to int or float, otherwise keep as string
    for fn in (int, float):
        try:
            return fn(value)
        except ValueError:
            continue
    return value 