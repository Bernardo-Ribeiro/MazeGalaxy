import Range
import math
from collections import OrderedDict
from mathutils import Vector

class Character(Range.types.KX_PythonComponent):
    args = OrderedDict()

    def start(self, args):
        self._character = Range.constraints.getCharacter(self.object)
        self.base_speed = 0.2

    def update(self):
        keyboard = Range.logic.keyboard.inputs
        
        # Movimento básico
        y = keyboard[Range.events.WKEY].active - keyboard[Range.events.SKEY].active
        x = keyboard[Range.events.DKEY].active - keyboard[Range.events.AKEY].active
        
        # Vetor de movimento normalizado
        movement_vector = Vector((x, y, 0)).normalized() * self.base_speed
        self._character.walkDirection = self.object.worldOrientation * movement_vector