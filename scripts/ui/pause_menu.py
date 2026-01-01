"""
Menu de Pausa
Aparece quando o jogador pausa o jogo (ESC)
"""

class PauseMenu:
    """Menu que aparece quando o jogador pausa o jogo"""
    
    def __init__(self, gui_system):
        self.gui_system = gui_system
        self.menu_frame = None
        self.resume_button = None
        self.restart_button = None
        self.quit_button = None
        
        # Callbacks externos
        self.on_resume_callback = None
        self.on_restart_callback = None
        self.on_quit_callback = None
        
        # Controle de cliques
        self.button_click_pending = None
        self.resume_was_active = False
        self.restart_was_active = False
        self.quit_was_active = False
    
    def load(self, xml_widgets):
        """
        Carrega o menu a partir dos widgets do XML
        
        Args:
            xml_widgets: Dicionário de widgets carregados do XML
        """
        self.menu_frame = xml_widgets.get('PauseMenu')
        
        if not self.menu_frame:
            print("[PauseMenu] ERRO: Frame do menu não encontrado no XML")
            return
        
        # Configurar aparência do menu
        self.menu_frame.visible = False
        self.menu_frame.colors = [
            [0.05, 0.05, 0.05, 0.90],
            [0.05, 0.05, 0.05, 0.90],
            [0.05, 0.05, 0.05, 0.90],
            [0.05, 0.05, 0.05, 0.90]
        ]
        
        # Buscar botões
        self.resume_button = self.menu_frame.children.get('ResumeButton')
        self.restart_button = self.menu_frame.children.get('RestartButton')
        self.quit_button = self.menu_frame.children.get('QuitButton')
        
        if self.resume_button and self.quit_button:
            # Habilitar eventos nos botões
            self.resume_button.frozen = False
            self.quit_button.frozen = False
            
            # Configurar callbacks
            self.resume_button.on_active = self._on_resume_active
            self.quit_button.on_active = self._on_quit_active
            
            # Restart é opcional
            if self.restart_button:
                self.restart_button.frozen = False
                self.restart_button.on_active = self._on_restart_active
        else:
            print("[PauseMenu] ERRO: Botões essenciais não encontrados no menu")
    
    def _on_resume_active(self, widget):
        """Callback interno quando o botão Resume é pressionado"""
        if not self.resume_was_active:
            self.resume_was_active = True
            self.button_click_pending = 'resume'
    
    def _on_restart_active(self, widget):
        """Callback interno quando o botão Restart é pressionado"""
        if not self.restart_was_active:
            self.restart_was_active = True
            self.button_click_pending = 'restart'
    
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
            
            if self.resume_button:
                self.resume_button.frozen = False
            if self.restart_button:
                self.restart_button.frozen = False
            if self.quit_button:
                self.quit_button.frozen = False
    
    def hide(self):
        """Esconde o menu da tela"""
        if self.menu_frame:
            self.menu_frame.visible = False
    
    def update(self):
        """Processa cliques pendentes a cada frame"""
        if self.button_click_pending:
            if self.button_click_pending == 'resume':
                if self.on_resume_callback:
                    self.on_resume_callback()
                self.resume_was_active = False
                
            elif self.button_click_pending == 'restart':
                if self.on_restart_callback:
                    self.on_restart_callback()
                self.restart_was_active = False
                
            elif self.button_click_pending == 'quit':
                if self.on_quit_callback:
                    self.on_quit_callback()
                self.quit_was_active = False
            
            self.button_click_pending = None
    
    def is_visible(self):
        """Retorna se o menu está visível"""
        return self.menu_frame and self.menu_frame.visible
    
    def toggle(self):
        """Alterna entre mostrar e esconder o menu"""
        if self.is_visible():
            self.hide()
        else:
            self.show()
