# Sistema de Interface do Usuário - MazeGalaxy

## 📁 Estrutura Modular

```
scripts/
├── ui/
│   ├── __init__.py              # Exportações do módulo
│   ├── ui_manager.py            # Gerenciador central (GameScene)
│   ├── menu_ui_manager.py       # Gerenciador do menu (MenuScene)
│   ├── hud.py                   # HUD (Level, Score, etc)
│   ├── level_complete_menu.py   # Menu de conclusão de nível
│   ├── pause_menu.py            # Menu de pausa
│   └── main_menu.py             # Menu principal
├── Ui.py                        # Wrapper de compatibilidade (GameScene)
├── MenuController.py            # Controlador do menu (MenuScene)
├── interface.xml                # Interface do jogo
└── menu_interface.xml           # Interface do menu
```

## 🎯 Componentes

### UIManager (`ui_manager.py`)
**Responsabilidade:** Coordenador central de toda a interface
- Inicializa todos os módulos de UI
- Carrega XML e distribui widgets
- Gerencia estado de pausa do jogo
- Conecta callbacks e componentes do jogo

**Uso:**
```python
# O componente Interface (Ui.py) usa automaticamente
# Você também pode usar diretamente:
from ui.ui_manager import UIManager

ui = UIManager()
ui.show_level_complete_menu()
ui.is_game_paused()
```

### HUD (`hud.py`)
**Responsabilidade:** Elementos sempre visíveis na tela
- Exibe informações em tempo real (Level, Score, Tempo)
- Atualiza automaticamente a cada frame
- Pode ser expandido para incluir vida, energia, etc.

**Métodos:**
- `load(xml_widgets)` - Carrega widgets do XML
- `update()` - Atualiza informações
- `set_maze_builder(builder)` - Conecta ao gerador de labirintos
- `show()` / `hide()` - Controla visibilidade

### LevelCompleteMenu (`level_complete_menu.py`)
**Responsabilidade:** Menu de conclusão de nível
- Aparece quando o jogador completa um level
- Botões: "Next Level" e "Quit"
- Pausa o jogo enquanto visível
- Processa cliques e notifica callbacks

**Callbacks:**
- `on_next_callback` - Chamado ao clicar em "Next Level"
- `on_quit_callback` - Chamado ao clicar em "Quit"

### PauseMenu (`pause_menu.py`)
**Responsabilidade:** Menu de pausa durante o jogo
- Aparece quando o jogador pressiona ESC (ou outro input configurado)
- Botões: "Resume", "Restart" e "Quit"
- Pausa o jogo enquanto visível
- Permite retomar, reiniciar ou sair do jogo

**Callbacks:**
- `on_resume_callback` - Chamado ao clicar em "Resume"
- `on_restart_callback` - Chamado ao clicar em "Restart"
- `on_quit_callback` - Chamado ao clicar em "Quit"

**Métodos extras:**
- `toggle()` - Alterna entre mostrar/esconder o menu

### MainMenu (`main_menu.py`)
**Responsabilidade:** Menu principal do jogo (MenuScene)
- Tela inicial quando o jogo inicia
- Botões: "Start Game", "Options" e "Quit"
- Interface para navegar entre menu e jogo
- Gerencia transição entre cenas

**Callbacks:**
- `on_start_callback` - Chamado ao clicar em "Start Game"
- `on_options_callback` - Chamado ao clicar em "Options"
- `on_quit_callback` - Chamado ao clicar em "Quit"

### MenuUIManager (`menu_ui_manager.py`)
**Responsabilidade:** Gerenciador da UI do menu principal
- Coordena o MainMenu
- Gerencia transições entre cenas
- Salva configurações em `logic.globalDict`
- Controla fluxo: Menu → Jogo

## 🔌 Interface de Compatibilidade

O arquivo `Ui.py` mantém compatibilidade com componentes existentes:

```python
class Interface(types.KX_PythonComponent):
    # Redireciona para UIManager internamente
    # Não quebrará código existente!
```

## 💡 Exemplo de Uso: Tecla ESC para Pausar

Para adicionar a funcionalidade de pausar com ESC, adicione no seu componente de controle do jogador:

```python
from Range import logic

class PlayerController(types.KX_PythonComponent):
    def update(self):
        # Encontrar componente de UI
        if not hasattr(self, 'ui_component'):
            for obj in logic.getCurrentScene().objects:
                for comp in obj.components:
                    if comp.__class__.__name__ == 'Interface':
                        self.ui_component = comp
                        break
        
        # Verificar se ESC foi pressionado
        if logic.keyboard.inputs[events.ESCKEY].activated:
            if self.ui_component:
                self.ui_component.toggle_pause_menu()
```

## 📝 Como Adicionar Novos Menus

### 1. Criar arquivo do menu
```python
# scripts/ui/pause_menu.py

class PauseMenu:
    def __init__(self, gui_system):
        self.gui_system = gui_system
        self.menu_frame = None
        
    def load(self, xml_widgets):
        self.menu_frame = xml_widgets.get('PauseMenu')
        # ... configurar botões
    
    def show(self):
        self.menu_frame.visible = True
    
    def hide(self):
        self.menu_frame.visible = False
    
    def update(self):
        # Processar eventos
        pass
```

### 2. Adicionar ao UIManager
```python
# Em ui_manager.py

from .pause_menu import PauseMenu

class UIManager:
    def start(self, args):
        # ...
        self.pause_menu = PauseMenu(self.gui_system)
        
    def _load_ui(self):
        # ...
        self.pause_menu.load(widgets)
        
    def update(self):
        # ...
        self.pause_menu.update()
```

### 3. Adicionar ao XML
```xml
<!-- interface.xml -->
<Frame name="PauseMenu" pos="0.3,0.2" size="0.4,0.6">
    <Label name="PauseTitle" text="PAUSED" .../>
    <Button name="ResumeButton" text="Resume" .../>
    <Button name="QuitButton" text="Quit" .../>
</Frame>
```

## 🚀 Benefícios da Nova Estrutura

✅ **Organização:** Cada arquivo tem uma responsabilidade clara
✅ **Manutenção:** Fácil encontrar e corrigir bugs
✅ **Expansão:** Adicionar novos menus sem bagunçar código existente
✅ **Reutilização:** Componentes podem ser usados em outros projetos
✅ **Testes:** Cada módulo pode ser testado independentemente
✅ **Colaboração:** Múltiplas pessoas podem trabalhar em paralelo

## 📚 Documentação Adicional

- **[BGUI Options Reference](../../BGUI_OPTIONS_REFERENCE.md)** - Guia completo sobre flags de alinhamento e opções do BGUI
- **[Menu Setup Guide](../../MENU_SETUP.md)** - Guia de configuração do menu principal no Blender/UPBGE

## 📚 Próximos Passos

Você pode facilmente adicionar:
- 🎮 **Menu Principal** - Tela inicial do jogo ✅ **IMPLEMENTADO**
- 💀 **Game Over Menu** - Quando o jogador perde
- ⚙️ **Menu de Configurações** - Opções de som, gráficos, etc.
- 📊 **Tela de Estatísticas** - Pontuação, tempo, recordes
- 🏆 **Tela de Conquistas** - Sistema de achievements

## 🔍 Debugging

Cada módulo possui prints informativos (apenas para erros críticos):
- `[UIManager]` - Erros de carregamento
- `[HUD]` - Erros de widgets não encontrados
- `[LevelCompleteMenu]` - Erros de botões não encontrados
- `[PauseMenu]` - Erros de configuração

Para adicionar mais debug, simplesmente adicione prints nos métodos relevantes.

## 📄 Licença

Parte do projeto MazeGalaxy
