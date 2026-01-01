"""
Gerenciador de UI do Menu Principal
Gerencia a interface do menu inicial
Last updated: 2026-01-01 v2
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
from .main_menu import MainMenu


class MenuUIManager:
    """Gerenciador de UI do menu principal"""

    def __init__(self):
        self.logic = logic
        self.scene = None
        self.gui_system = None
        self.main_menu = None
    
    def start(self, args):
        """
        Inicialização do gerenciador de UI do menu
        
        Args:
            args: Argumentos do componente
        """
        self.scene = self.logic.getCurrentScene()
        
        # Sistema BGUI
        self.gui_system = bgui.BGUISystem()
        
        # Inicializar menu principal
        self.main_menu = MainMenu(self.gui_system)
        
        # Configurar callbacks
        self.main_menu.on_start_callback = self._on_start_game
        self.main_menu.on_options_callback = self._on_options
        self.main_menu.on_quit_callback = self._on_quit
        
        # Carregar interface do XML
        self._load_ui()
    
    def _load_ui(self):
        """Carrega a interface a partir do arquivo XML"""
        script_dir = os.path.dirname(__file__)
        xml_path = os.path.join(script_dir, '..', 'menu_interface.xml')
        
        try:
            widgets = bgui.load_ui_from_xml(xml_path, self.gui_system.main_frame)
            self.main_menu.load(widgets)
            
        except Exception as e:
            print(f"[MenuUIManager] ERRO ao carregar interface: {e}")
            import traceback
            traceback.print_exc()
    
    # ========================================
    # Callbacks
    # ========================================
    
    def _on_start_game(self):
        """Callback quando o jogador clica em 'Start Game'"""
        print("[MenuUIManager] Iniciando jogo...")
        
        # Salvar configurações globais se necessário
        self.logic.globalDict["starting_level"] = 1
        self.logic.globalDict["player_name"] = "Player"
        
        # Trocar para a cena do jogo com transição
        self._transition_to_game()
    
    def _transition_to_game(self):
        """Faz transição suave para a cena do jogo"""
        # TODO: Adicionar fade out aqui no futuro
        
        # Carregar cena do jogo
        self.scene.replace("GameScene")  # Nome da cena do jogo
    
    def _on_options(self):
        """Callback quando o jogador clica em 'Options'"""
        print("[MenuUIManager] Menu de opções (não implementado ainda)")
        # TODO: Implementar menu de opções
    
    def _on_quit(self):
        """Callback quando o jogador clica em 'Quit'"""
        print("[MenuUIManager] Encerrando jogo...")
        self.logic.endGame()
    
    # ========================================
    # Update Loop
    # ========================================
    
    def update(self):
        """Atualização a cada frame"""
        self.main_menu.update()
        self.gui_system.run()
