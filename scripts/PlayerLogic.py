from Range import *
from collections import OrderedDict
from mathutils import Vector

class Player(types.KX_PythonComponent):
    args = OrderedDict({})
    def awake(self, args):
        self.start_pos = None
        self.ui_component = None
        
    def start(self, args):
        self.maze_obj = logic.getCurrentScene().objects.get("Maze")
        if self.maze_obj:
            self.maze_builder = self.maze_obj.components.get("MazeBuilder")
        
        # Encontrar componente de UI
        for obj in logic.getCurrentScene().objects:
            for comp in obj.components:
                if comp.__class__.__name__ == 'Interface':
                    self.ui_component = comp
                    break
            if self.ui_component:
                break
                
    def update(self):
        if self.start_pos is None and self.maze_builder:
            local_pos = self.maze_builder.get_start_position()
            if local_pos:
                maze_world_pos = self.maze_obj.worldPosition
                self.start_pos = maze_world_pos + local_pos

                print("[SensorComp] Posição de saída (world):", self.start_pos)

                self.object.worldPosition = self.start_pos + Vector((0,0,1))
        
        # Verificar tecla ESC
        if logic.keyboard.inputs[events.ESCKEY].activated:
            if self.ui_component:
                self.ui_component.toggle_pause_menu()
