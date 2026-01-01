"""
Menu de Level Completo
Aparece quando o jogador completa um nível
"""

class LevelCompleteMenu:
    """Menu que aparece quando o jogador completa um level"""
    
    def __init__(self, gui_system):
        self.gui_system = gui_system
        self.menu_frame = None
        self.next_button = None
        self.quit_button = None
        
        # Callbacks externos
        self.on_next_callback = None
        self.on_quit_callback = None
        
        # Controle de cliques
        self.button_click_pending = None
        self.next_was_active = False
        self.quit_was_active = False
    
    def load(self, xml_widgets):
        """
        Carrega o menu a partir dos widgets do XML
        
        Args:
            xml_widgets: Dicionário de widgets carregados do XML
        """
        self.menu_frame = xml_widgets.get('LevelCompleteMenu')
        
        if not self.menu_frame:
            print("[LevelCompleteMenu] Erro: Frame do menu não encontrado no XML")
            return
        
        # Configurar aparência do menu
        self.menu_frame.visible = False
        self.menu_frame.colors = [
            [0.1, 0.1, 0.1, 0.85],
            [0.1, 0.1, 0.1, 0.85],
            [0.1, 0.1, 0.1, 0.85],
            [0.1, 0.1, 0.1, 0.85]
        ]
        
        # Buscar botões
        self.next_button = self.menu_frame.children.get('NextLevelButton')
        self.quit_button = self.menu_frame.children.get('QuitButton')
        
        if self.next_button and self.quit_button:
            # Habilitar eventos nos botões
            self.next_button.frozen = False
            self.quit_button.frozen = False
            
            # Configurar callbacks
            self.next_button.on_active = self._on_next_active
            self.quit_button.on_active = self._on_quit_active
        else:
            print("[LevelCompleteMenu] ERRO: Botões não encontrados no menu")
    
    def _on_next_active(self, widget):
        """Callback interno quando o botão Next Level é pressionado"""
        if not self.next_was_active:
            self.next_was_active = True
            self.button_click_pending = 'next'
    
    def _on_quit_active(self, widget):
        """Callback interno quando o botão Quit é pressionado"""
        if not self.quit_was_active:
            self.quit_was_active = True
            self.button_click_pending = 'quit'
    
    def show(self):
        """Mostra o menu na tela"""
        if self.menu_frame:
            self.menu_frame.visible = True
            self.menu_frame.frozen = False
            
            if self.next_button:
                self.next_button.frozen = False
            if self.quit_button:
                self.quit_button.frozen = False
    
    def hide(self):
        """Esconde o menu da tela"""
        if self.menu_frame:
            self.menu_frame.visible = False
    
    def update(self):
        """Processa cliques pendentes a cada frame"""
        if self.button_click_pending:
            if self.button_click_pending == 'next':
                if self.on_next_callback:
                    self.on_next_callback()
                self.next_was_active = False
                
            elif self.button_click_pending == 'quit':
                if self.on_quit_callback:
                    self.on_quit_callback()
                self.quit_was_active = False
            
            self.button_click_pending = None
    
    def is_visible(self):
        """Retorna se o menu está visível"""
        return self.menu_frame and self.menu_frame.visible
