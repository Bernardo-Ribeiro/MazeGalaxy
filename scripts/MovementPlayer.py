import Range
import math
from collections import OrderedDict
from mathutils import Vector

class Character(Range.types.KX_PythonComponent):
    args = OrderedDict()

    def start(self, args):
        self._character = Range.constraints.getCharacter(self.object)
        self.base_speed = 0.2
        self.ui_component = None
        
        # Encontrar o componente de UI
        scene = Range.logic.getCurrentScene()
        for obj in scene.objects:
            for component in obj.components:
                if component.__class__.__name__ == 'Interface':
                    self.ui_component = component
                    break
            if self.ui_component:
                break

    def update(self):
        # Se o jogo estiver pausado, não processar movimento
        if self.ui_component and self.ui_component.is_game_paused():
            self._character.walkDirection = Vector((0, 0, 0))
            return
        
        keyboard = Range.logic.keyboard.inputs
        
        # Movimento básico
        y = keyboard[Range.events.WKEY].active - keyboard[Range.events.SKEY].active
        x = keyboard[Range.events.DKEY].active - keyboard[Range.events.AKEY].active
        
        # Vetor de movimento normalizado
        movement_vector = Vector((x, y, 0)).normalized() * self.base_speed
        self._character.walkDirection = self.object.worldOrientation * movement_vector