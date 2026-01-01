"""
Menu Principal - Componente Python
Gerencia o menu principal do jogo
Updated: 2026-01-01 v2
"""

import os
import sys
from Range import types, logic, events
from collections import OrderedDict

# Adicionar o diretório scripts ao path
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from ui.menu_ui_manager import MenuUIManager


class MenuController(types.KX_PythonComponent):
    """
    Controlador do menu principal
    Gerencia a interface e lógica do menu
    """
    
    args = OrderedDict({})
    
    def start(self, args):
        """Inicializa o sistema de menu"""
        # Inicializar _menu_manager como None primeiro
        self._menu_manager = None
        
        try:
            # Criar instância do MenuUIManager
            self._menu_manager = MenuUIManager()
            self._menu_manager.start(args)
            print("[MenuController] Menu inicializado com sucesso!")
        except Exception as e:
            print(f"[MenuController] ERRO ao inicializar menu: {e}")
            import traceback
            traceback.print_exc()
            self._menu_manager = None
    
    def update(self):
        """Atualização a cada frame"""
        if hasattr(self, '_menu_manager') and self._menu_manager:
            self._menu_manager.update()
