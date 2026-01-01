"""
HUD (Heads-Up Display) - Elementos de interface sempre visíveis
Gerencia: Level, Score, Tempo, etc.
"""

class HUD:
    """Gerencia elementos do HUD do jogo"""
    
    def __init__(self, gui_system):
        self.gui_system = gui_system
        self.widgets = {}
        self.maze_builder = None
    
    def load(self, xml_widgets):
        """
        Carrega widgets do HUD a partir do XML
        
        Args:
            xml_widgets: Dicionário de widgets carregados do XML
        """
        self.widgets['level'] = xml_widgets.get('Level')
        
        if not self.widgets['level']:
            print("[HUD] ERRO: Widget 'Level' não encontrado no XML")
    
    def update(self):
        """Atualiza informações do HUD a cada frame"""
        if self.maze_builder and self.widgets.get('level'):
            current_level = self.maze_builder.get_level()
            self.widgets['level'].text = f"Level: {current_level}"
    
    def set_maze_builder(self, builder):
        """
        Define o componente MazeBuilder para obter informações do nível
        
        Args:
            builder: Instância do componente MazeBuilder
        """
        self.maze_builder = builder
    
    def show(self):
        """Mostra o HUD"""
        for widget in self.widgets.values():
            if widget:
                widget.visible = True
    
    def hide(self):
        """Esconde o HUD"""
        for widget in self.widgets.values():
            if widget:
                widget.visible = False
