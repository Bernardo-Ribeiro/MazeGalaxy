"""
Interface - Compatibilidade com o sistema antigo
Este arquivo mantém a classe Interface por compatibilidade,
mas agora usa o UIManager modular internamente.
"""

import os
import sys
from Range import *
import bgui
from collections import OrderedDict

# Adicionar o diretório scripts ao path se necessário
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from ui.ui_manager import UIManager as NewUIManager


class Interface(types.KX_PythonComponent):
    """
    Classe de compatibilidade que redireciona para o novo UIManager
    Mantido para não quebrar componentes existentes no projeto
    """
    
    args = OrderedDict({})
    
    def start(self, args):
        """Inicializa usando o novo sistema modular"""
        # Inicializar _ui_manager como None primeiro
        self._ui_manager = None
        
        try:
            # Criar instância do novo UIManager
            self._ui_manager = NewUIManager()
            self._ui_manager.start(args)
        except Exception as e:
            print(f"[Interface] Erro ao inicializar UIManager: {e}")
            import traceback
            traceback.print_exc()
            # Garantir que _ui_manager existe mesmo com erro
            self._ui_manager = None
    
    def show_level_complete_menu(self):
        """Mostra o menu de level completo"""
        if hasattr(self, '_ui_manager') and self._ui_manager:
            return self._ui_manager.show_level_complete_menu()
    
    def hide_level_complete_menu(self):
        """Esconde o menu de level completo"""
        if hasattr(self, '_ui_manager') and self._ui_manager:
            return self._ui_manager.hide_level_complete_menu()
    
    def toggle_pause_menu(self):
        """Alterna o menu de pausa"""
        if hasattr(self, '_ui_manager') and self._ui_manager:
            return self._ui_manager.toggle_pause_menu()
    
    def show_pause_menu(self):
        """Mostra o menu de pausa"""
        if hasattr(self, '_ui_manager') and self._ui_manager:
            return self._ui_manager.show_pause_menu()
    
    def hide_pause_menu(self):
        """Esconde o menu de pausa"""
        if hasattr(self, '_ui_manager') and self._ui_manager:
            return self._ui_manager.hide_pause_menu()
    
    def is_game_paused(self):
        """Retorna se o jogo está pausado"""
        if hasattr(self, '_ui_manager') and self._ui_manager:
            return self._ui_manager.is_game_paused()
        return False
    
    def update(self):
        """Atualização a cada frame"""
        if hasattr(self, '_ui_manager') and self._ui_manager:
            self._ui_manager.update()


