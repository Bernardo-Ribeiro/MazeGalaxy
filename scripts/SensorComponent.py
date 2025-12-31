from Range import *
from collections import OrderedDict
from mathutils import Vector

class SensorExit(types.KX_PythonComponent):
    args = OrderedDict({})

    def awake(self, args):
        self.maze_obj = None
        self.maze_builder = None
        self.exit_pos = None
        self.activated = False

    def start(self, args):
        self.scene = logic.getCurrentScene()
        self.maze_obj = self.scene.objects.get("Maze")
        if self.maze_obj:
            self.maze_builder = self.maze_obj.components.get("MazeBuilder")

    def update(self):
        if self.exit_pos is None and self.maze_builder:
            self.update_exit_position()

        player = self.scene.objects.get("Player")
        if player and self.exit_pos:
            distance = self.object.getDistanceTo(player)

            if distance < 1.0 and not self.activated:
                print("[SensorExit] Novo labirinto gerado")
                self.maze_builder.reGenerate()
                self.activated = True

                self.update_exit_position()

                start_local = self.maze_builder.get_start_position()
                if start_local:
                    start_world = self.maze_obj.worldPosition + start_local
                    player.worldPosition = start_world + Vector((0, 0, 0))
                    print("[SensorExit] Player movido para o novo ponto de início:", start_world)

            elif distance >= 1.0:
                self.activated = False

    def update_exit_position(self):
        local_pos = self.maze_builder.get_exit_position()
        if local_pos:
            maze_world_pos = self.maze_obj.worldPosition
            self.exit_pos = maze_world_pos + local_pos
            self.object.worldPosition = self.exit_pos + Vector((0, 1.5, 1))
            print("[SensorExit] Cubo de saída movido para:", self.exit_pos)
