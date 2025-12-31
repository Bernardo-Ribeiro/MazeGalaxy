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
    # Convert XML attributes to widget constructor arguments
    kwargs = {k: try_parse_widget_arg(k, v) for k, v in elem.attrib.items()}
    # Ensure 'parent' is the first argument
    widget = widget_class(parent, **kwargs)
    # Recursively create children, if any
    for child in elem:
        create_widget_from_elem(child, widget)
    return widget

def try_parse_widget_arg(key, value):
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