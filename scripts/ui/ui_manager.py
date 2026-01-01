"""
Gerenciador Central de UI
Coordena todos os elementos da interface do usuário
"""

import os
import sys
from Range import logic

# Adicionar o diretório pai (scripts) ao path
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import bgui
from collections import OrderedDict
from .hud import HUD
from .level_complete_menu import LevelCompleteMenu
from .pause_menu import PauseMenu


class UIManager:
    """Gerenciador central de toda a interface do usuário (não é um componente)"""
    
    def __init__(self):
        
        self.logic = logic

        # Inicializar atributos
        self.game_paused = False
        self.scene = None
        self.gui_system = None
        self.hud = None
        self.level_complete_menu = None
        self.pause_menu = None
        self.maze_builder = None
    
    def start(self, args):
        """
        Inicialização do gerenciador de UI
        
        Args:
            args: Argumentos do componente
        """
        # Estado do jogo
        self.game_paused = False
        self.scene = self.logic.getCurrentScene()
        
        # Sistema BGUI
        self.gui_system = bgui.BGUISystem()
        
        # Inicializar módulos de UI
        self.hud = HUD(self.gui_system)
        self.level_complete_menu = LevelCompleteMenu(self.gui_system)
        self.pause_menu = PauseMenu(self.gui_system)
        
        # Configurar callbacks dos menus
        self.level_complete_menu.on_next_callback = self._on_next_level
        self.level_complete_menu.on_quit_callback = self._on_quit
        
        self.pause_menu.on_resume_callback = self._on_resume
        self.pause_menu.on_restart_callback = self._on_restart
        self.pause_menu.on_quit_callback = self._on_quit
        
        # Carregar interface do XML
        self._load_ui()
        
        # Encontrar componentes do jogo
        self._find_game_components()
    
    def _load_ui(self):
        """Carrega a interface a partir do arquivo XML"""
        script_dir = os.path.dirname(__file__)
        xml_path = os.path.join(script_dir, '..', 'interface.xml')
        
        try:
            widgets = bgui.load_ui_from_xml(xml_path, self.gui_system.main_frame)
            
            # Passar widgets para cada módulo
            self.hud.load(widgets)
            self.level_complete_menu.load(widgets)
            self.pause_menu.load(widgets)
            
        except Exception as e:
            print(f"[UIManager] ERRO ao carregar interface: {e}")
            import traceback
            traceback.print_exc()
    
    def _find_game_components(self):
        """Encontra e conecta componentes do jogo"""
        self.maze_builder = None
        
        for obj in self.scene.objects:
            for component in obj.components:
                # Encontrar MazeBuilder
                if component.__class__.__name__ == 'MazeBuilder':
                    self.maze_builder = component
                    self.hud.set_maze_builder(component)
                    break
            if self.maze_builder:
                break
    
    # ========================================
    # Métodos Públicos - Menu Level Complete
    # ========================================
    
    def show_level_complete_menu(self):
        """Mostra o menu de level completo e pausa o jogo"""
        self.level_complete_menu.show()
        self.game_paused = True
    
    def hide_level_complete_menu(self):
        """Esconde o menu de level completo e despausa o jogo"""
        self.level_complete_menu.hide()
        self.game_paused = False
    
    # ========================================
    # Métodos Públicos - Menu de Pausa
    # ========================================
    
    def toggle_pause_menu(self):
        """Alterna o menu de pausa e o estado do jogo"""
        if self.pause_menu.is_visible():
            self.hide_pause_menu()
        else:
            self.show_pause_menu()
    
    def show_pause_menu(self):
        """Mostra o menu de pausa e pausa o jogo"""
        self.pause_menu.show()
        self.game_paused = True
    
    def hide_pause_menu(self):
        """Esconde o menu de pausa e despausa o jogo"""
        self.pause_menu.hide()
        self.game_paused = False
    
    # ========================================
    # Callbacks Internos
    # ========================================
    
    def _on_next_level(self):
        """Callback quando o jogador clica em 'Next Level'"""
        self.hide_level_complete_menu()
        
        # Encontrar e notificar o sensor de saída para gerar o próximo nível
        for obj in self.scene.objects:
            for component in obj.components:
                if component.__class__.__name__ == 'SensorExit':
                    component.generate_next_level()
                    return
    
    def _on_quit(self):
        """Callback quando o jogador clica em 'Quit'"""
        self.logic.endGame()
    
    def _on_resume(self):
        """Callback quando o jogador clica em 'Resume' no menu de pausa"""
        self.hide_pause_menu()
    
    def _on_restart(self):
        """Callback quando o jogador clica em 'Restart' no menu de pausa"""
        self.hide_pause_menu()
        
        # Regenerar o nível atual sem mudar o número do nível
        if self.maze_builder:
            # Regenerar o labirinto mantendo o mesmo nível
            self.maze_builder.regenerate_current_level()
        
        # Reposicionar o sensor de saída para a nova posição
        for obj in self.scene.objects:
            for component in obj.components:
                if component.__class__.__name__ == 'SensorExit':
                    # Resetar posição de saída para forçar reposicionamento
                    component.exit_pos = None
                    component.activated = False
                    break
        
        # Reposicionar o jogador no ponto de início
        for obj in self.scene.objects:
            for component in obj.components:
                if component.__class__.__name__ == 'Player':
                    # Resetar posição inicial para forçar reposicionamento
                    component.start_pos = None
                    break
    
    # ========================================
    # Controle de Estado
    # ========================================
    
    def is_game_paused(self):
        """Retorna se o jogo está pausado"""
        return self.game_paused
    
    # ========================================
    # Update Loop
    # ========================================
    
    def update(self):
        """Atualização a cada frame"""
        # Atualizar módulos de UI
        self.hud.update()
        self.level_complete_menu.update()
        self.pause_menu.update()
        
        # Rodar sistema BGUI
        self.gui_system.run()
