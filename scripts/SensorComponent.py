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
        self.ui_component = None

    def start(self, args):
        self.scene = logic.getCurrentScene()
        self.maze_obj = self.scene.objects.get("Maze")
        if self.maze_obj:
            self.maze_builder = self.maze_obj.components.get("MazeBuilder")
        
        # Encontrar o componente de UI
        for obj in self.scene.objects:
            for component in obj.components:
                if component.__class__.__name__ == 'Interface':
                    self.ui_component = component
                    break
            if self.ui_component:
                break

    def update(self):
        # Se o jogo estiver pausado, não processar a lógica de sensor
        if self.ui_component and self.ui_component.is_game_paused():
            return
        
        if self.exit_pos is None and self.maze_builder:
            self.update_exit_position()

        player = self.scene.objects.get("Player")
        if player and self.exit_pos:
            distance = self.object.getDistanceTo(player)

            if distance < 1.0 and not self.activated:
                print("[SensorExit] Level completo! Mostrando menu...")
                self.activated = True
                
                # Mostrar o menu de level completo
                if self.ui_component:
                    self.ui_component.show_level_complete_menu()

            elif distance >= 1.0:
                self.activated = False
    
    def generate_next_level(self):
        """Gera o próximo nível (chamado pelo botão do menu)"""
        print("[SensorExit] Gerando próximo nível...")
        self.maze_builder.reGenerate()
        
        self.update_exit_position()
        
        # Mover o jogador para o novo ponto de início
        player = self.scene.objects.get("Player")
        start_local = self.maze_builder.get_start_position()
        if start_local and player:
            start_world = self.maze_obj.worldPosition + start_local
            player.worldPosition = start_world + Vector((0, 0, 0))
            print("[SensorExit] Player movido para o novo ponto de início:", start_world)
        
        self.activated = False

    def update_exit_position(self):
        local_pos = self.maze_builder.get_exit_position()
        if local_pos:
            maze_world_pos = self.maze_obj.worldPosition
            self.exit_pos = maze_world_pos + local_pos
            self.object.worldPosition = self.exit_pos + Vector((0, 1.5, 1))
            print("[SensorExit] Cubo de saída movido para:", self.exit_pos)
