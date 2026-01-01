"""
Menu Principal
Tela inicial do jogo
"""

class MainMenu:
    """Menu principal do jogo"""
    
    def __init__(self, gui_system):
        self.gui_system = gui_system
        self.menu_frame = None
        self.start_button = None
        self.options_button = None
        self.quit_button = None
        
        # Callbacks externos
        self.on_start_callback = None
        self.on_options_callback = None
        self.on_quit_callback = None
        
        # Controle de cliques
        self.button_click_pending = None
        self.start_was_active = False
        self.options_was_active = False
        self.quit_was_active = False
    
    def load(self, xml_widgets):
        """
        Carrega o menu a partir dos widgets do XML
        
        Args:
            xml_widgets: Dicionário de widgets carregados do XML
        """
        self.menu_frame = xml_widgets.get('MainMenu')
        
        if not self.menu_frame:
            print("[MainMenu] ERRO: Frame do menu não encontrado no XML")
            return
        
        # Configurar aparência do menu
        self.menu_frame.visible = True
        self.menu_frame.colors = [
            [0.0, 0.0, 0.0, 0.0],  # Transparente (fundo será a cena 3D)
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ]
        
        # Buscar botões
        self.start_button = self.menu_frame.children.get('StartButton')
        self.options_button = self.menu_frame.children.get('OptionsButton')
        self.quit_button = self.menu_frame.children.get('QuitButton')
        
        if self.start_button and self.quit_button:
            # Habilitar eventos nos botões
            self.start_button.frozen = False
            self.quit_button.frozen = False
            
            # Configurar callbacks
            self.start_button.on_active = self._on_start_active
            self.quit_button.on_active = self._on_quit_active
            
            # Options é opcional
            if self.options_button:
                self.options_button.frozen = False
                self.options_button.on_active = self._on_options_active
        else:
            print("[MainMenu] ERRO: Botões essenciais não encontrados no menu")
    
    def _on_start_active(self, widget):
        """Callback interno quando o botão Start é pressionado"""
        if not self.start_was_active:
            self.start_was_active = True
            self.button_click_pending = 'start'
    
    def _on_options_active(self, widget):
        """Callback interno quando o botão Options é pressionado"""
        if not self.options_was_active:
            self.options_was_active = True
            self.button_click_pending = 'options'
    
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
            
            if self.start_button:
                self.start_button.frozen = False
            if self.options_button:
                self.options_button.frozen = False
            if self.quit_button:
                self.quit_button.frozen = False
    
    def hide(self):
        """Esconde o menu da tela"""
        if self.menu_frame:
            self.menu_frame.visible = False
    
    def update(self):
        """Processa cliques pendentes a cada frame"""
        if self.button_click_pending:
            if self.button_click_pending == 'start':
                if self.on_start_callback:
                    self.on_start_callback()
                self.start_was_active = False
                
            elif self.button_click_pending == 'options':
                if self.on_options_callback:
                    self.on_options_callback()
                self.options_was_active = False
                
            elif self.button_click_pending == 'quit':
                if self.on_quit_callback:
                    self.on_quit_callback()
                self.quit_was_active = False
            
            self.button_click_pending = None
    
    def is_visible(self):
        """Retorna se o menu está visível"""
        return self.menu_frame and self.menu_frame.visible
