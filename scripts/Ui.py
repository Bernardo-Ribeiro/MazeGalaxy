import os
from Range import *
import bgui
from collections import OrderedDict

class Interface(types.KX_PythonComponent):
    args = OrderedDict({
    })
    
    def start(self, args):
        self.scene = logic.getCurrentScene()
        
        self.gui_system = bgui.BGUISystem()
        
        script_dir = os.path.dirname(__file__)
        xml_path = os.path.join(script_dir, 'interface.xml')
        
        self.widgets = bgui.load_ui_from_xml(xml_path, self.gui_system.main_frame)
        
        self.level_widget = self.widgets['Level']
        
        self.maze_builder = None
        for obj in self.scene.objects:
            for component in obj.components:
                if component.__class__.__name__ == 'MazeBuilder':
                    self.maze_builder = component
                    break
            if self.maze_builder:
                break

    def update(self):
        if self.maze_builder:
            current_level = self.maze_builder.get_level()
            self.level_widget.text = f"Level: {current_level}"
        
        self.gui_system.run()

