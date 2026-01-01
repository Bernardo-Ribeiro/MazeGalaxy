# 🎨 BGUI Named Flags - Quick Reference

## Overview

O BGUI agora suporta **flags nomeadas** no XML! Você pode usar nomes legíveis ao invés de números mágicos.

## Sintaxe

```xml
<!-- Ao invés de: -->
<Label text="Hello" options="9"/>

<!-- Use: -->
<Label text="Hello" options="BGUI_CENTERX|BGUI_NO_THEME"/>
```

## Color Properties in XML

You can now set color properties directly in XML attributes. Colors are specified as comma-separated RGBA values (0-1 range):

```xml
<!-- Frame with custom colors -->
<Frame name="overlay" size="1,1" pos="0,0" 
       color="0,0,0,0.5"/>

<!-- Label with custom text color -->
<Label name="title" text="Game Paused" 
       pos="0.5,0.5" 
       options="BGUI_CENTERED"
       text_color="1,1,0,1"/>
```

### Supported Color Properties

- `color` - Main color (for Frames, buttons, etc.)
- `colors` - Multiple corner colors for gradients
- `text_color` - Text color (for labels, buttons)
- `border_color` - Border color
- `outline_color` - Outline color
- `fill_color` - Fill color
- `highlight_color` - Highlight color
- `selection_color` - Selection color
- `base_color` - Base color
- `hover_color` - Hover state color
- `click_color` - Click state color

**Note:** These properties are set *after* widget creation, so they won't cause constructor errors.

## Flags Disponíveis

| Nome da Flag | Valor | Descrição |
|-------------|-------|-----------|
| `BGUI_DEFAULT` | 0 | Nenhuma flag especial |
| `BGUI_CENTERX` | 1 | Centraliza horizontalmente na posição |
| `BGUI_CENTERY` | 2 | Centraliza verticalmente na posição |
| `BGUI_CENTERED` | 3 | Centraliza X e Y (equivale a CENTERX\|CENTERY) |
| `BGUI_NO_NORMALIZE` | 4 | Usa pixels absolutos ao invés de coordenadas 0-1 |
| `BGUI_NO_THEME` | 8 | Desabilita aplicação de tema (para cores customizadas) |
| `BGUI_NO_FOCUS` | 16 | Widget não pode receber foco do teclado |
| `BGUI_CACHE` | 32 | Habilita cache de renderização (otimização) |

## Combinando Flags

Use o caractere `|` (pipe) para combinar múltiplas flags:

```xml
<!-- Centralizado em ambas direções + sem tema -->
<Label text="Title" pos="0.5,0.5" 
       options="BGUI_CENTERX|BGUI_CENTERY|BGUI_NO_THEME"/>

<!-- Ou use a flag combinada BGUI_CENTERED -->
<Label text="Title" pos="0.5,0.5" 
       options="BGUI_CENTERED|BGUI_NO_THEME"/>
```

## Exemplos Práticos

### Label Centralizado
```xml
<!-- Centraliza o texto na posição especificada -->
<Label name="title" text="MAZE GALAXY" 
       pos="0.5,0.8" 
       options="BGUI_CENTERX"
       pt_size="48" color="1,1,1,1"/>
```

### Button (texto já centralizado)
```xml
<!-- Buttons já centralizam o texto automaticamente -->
<Button name="start" text="Start Game" 
        pos="0.35,0.65" size="0.3,0.08"
        pt_size="32"/>
```

### Frame Customizado (sem tema)
```xml
<!-- Frame com cor customizada -->
<Frame name="menu" pos="0.3,0.2" size="0.4,0.6"
       options="BGUI_NO_THEME"
       color="0.2,0.2,0.2,0.9"
       border="2"/>
```

### Múltiplas Flags
```xml
<!-- Frame centralizado, sem tema, e sem foco -->
<Frame name="dialog" pos="0.5,0.5" size="0.6,0.4"
       options="BGUI_CENTERED|BGUI_NO_THEME|BGUI_NO_FOCUS"
       color="0.1,0.1,0.1,0.95">
    <Label text="Game Paused" 
           pos="0.5,0.8" size="0.8,0.15"
           options="BGUI_CENTERED"
           pt_size="36" color="1,1,1,1"/>
</Frame>
```

### Posicionamento Absoluto (pixels)
```xml
<!-- Usa pixels ao invés de valores 0-1 -->
<Label text="Fixed Position" 
       pos="100,50" 
       options="BGUI_NO_NORMALIZE"
       pt_size="20"/>
```

## Conversão Rápida

| Valor Numérico | Flag Nomeada | Uso Comum |
|----------------|--------------|-----------|
| `0` | `BGUI_DEFAULT` | Padrão, sem flags |
| `1` | `BGUI_CENTERX` | Centraliza horizontalmente |
| `2` | `BGUI_CENTERY` | Centraliza verticalmente |
| `3` | `BGUI_CENTERED` | Centraliza ambas direções |
| `4` | `BGUI_NO_NORMALIZE` | Posicionamento em pixels |
| `8` | `BGUI_NO_THEME` | Cores customizadas |
| `9` | `BGUI_CENTERX\|BGUI_NO_THEME` | Centro X + customizado |
| `11` | `BGUI_CENTERED\|BGUI_NO_THEME` | Centro + customizado |
| `16` | `BGUI_NO_FOCUS` | Widget não recebe foco |
| `32` | `BGUI_CACHE` | Otimização de renderização |

## Validação de Erros

Se você usar uma flag inválida, o BGUI mostrará um aviso:

```python
BGUI WARNING: Unknown flag 'BGUI_CENTER'. Available flags: BGUI_DEFAULT, BGUI_CENTERX, ...
```

Flags válidas:
- ✅ `BGUI_CENTERX`
- ✅ `BGUI_CENTERED`
- ❌ `BGUI_CENTER` (não existe!)
- ❌ `CENTER_X` (nome incorreto)

## Compatibilidade

✅ **Valores numéricos ainda funcionam:**
```xml
<!-- Ambos são equivalentes -->
<Label text="Old Way" options="3"/>
<Label text="New Way" options="BGUI_CENTERED"/>
```

## Widgets e Options

### Label
- `BGUI_CENTERX` / `BGUI_CENTERY` - Centraliza o texto na posição
- `BGUI_NO_NORMALIZE` - Usa pixels absolutos
- `BGUI_NO_THEME` - Ignora cores do tema

### Button (FrameButton)
- ⚠️ O **texto do botão é sempre centralizado** automaticamente
- Use `options` apenas para: `BGUI_NO_NORMALIZE`, `BGUI_NO_THEME`, `BGUI_NO_FOCUS`
- Não use `BGUI_CENTERX` no Button (não faz nada para o texto)

### Frame
- `BGUI_CENTERX` / `BGUI_CENTERY` - Centraliza o frame na posição
- `BGUI_NO_THEME` - Permite cores customizadas
- `BGUI_NO_FOCUS` - Frame não responde a foco

## Implementação

A conversão de nomes para valores é feita automaticamente pelo `xml_loader.py`:

```python
# bgui/xml_loader.py - função try_parse_widget_arg()
if key == "options":
    if any(c.isalpha() for c in value):
        # Parse named flags
        flags = [flag.strip() for flag in value.split("|")]
        result = 0
        for flag in flags:
            if flag in BGUI_FLAG_MAP:
                result |= BGUI_FLAG_MAP[flag]
        return result
```

## Arquivo de Exemplo

Ver: `scripts/test_named_flags.xml` e `scripts/menu_interface_named_flags.xml`

## Recursos

- 📘 `BGUI_OPTIONS_REFERENCE.md` - Documentação completa
- 📄 `bgui/widget.py` - Definições das flags (linhas 36-44)
- 📄 `bgui/xml_loader.py` - Implementação do parser
- 📄 `scripts/test_named_flags.xml` - Exemplos práticos

---

**Última atualização:** $(Get-Date)
