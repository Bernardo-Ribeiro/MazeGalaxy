from Range import *
from collections import OrderedDict
from mathutils import Vector

class Player(types.KX_PythonComponent):
    args = OrderedDict({})
    def awake(self, args):
        self.start_pos = None
        
    def start(self, args):
        self.maze_obj = logic.getCurrentScene().objects.get("Maze")
        if self.maze_obj:
            self.maze_builder = self.maze_obj.components.get("MazeBuilder")
                
    def update(self):
        if self.start_pos is None and self.maze_builder:
            local_pos = self.maze_builder.get_start_position()
            if local_pos:
                maze_world_pos = self.maze_obj.worldPosition
                self.start_pos = maze_world_pos + local_pos

                print("[SensorComp] Posição de saída (world):", self.start_pos)

                self.object.worldPosition = self.start_pos + Vector((0,0,1))
    