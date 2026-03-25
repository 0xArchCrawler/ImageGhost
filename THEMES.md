# imageghost themes

## gui themes (10 total)

### 1. arch dark (default)
- clean minimal arch linux dark theme
- blue (#1793d1) accents on black
- perfect for daily use
- monospace fonts

### 2. blackarch
- classic green-on-black terminal
- based on blackarch linux
- hacker aesthetic
- bold green text

### 3. dracula
- popular dracula color scheme
- purple/pink modern theme
- easy on the eyes
- rounded corners

### 4. gruvbox dark
- warm retro color scheme
- brown/orange tones
- comfortable for long sessions

### 5. green hacker
- ultra bright green (#00ff41)
- matrix-style terminal
- bold fonts
- maximum visibility

### 6. blue soc team
- professional blue theme
- security operations center style
- gradient progress bars
- clean modern design

### 7. red team ops
- aggressive red theme
- red team operations style
- high contrast
- intimidating look

### 8. purple team
- purple team theme
- combines red + blue
- gradient effects
- modern ui

### 9. nord
- popular nord color scheme
- blue/white arctic theme
- clean professional
- easy to read

### 10. custom arch
- customizable arch theme
- user can modify colors
- saved in config

## cli theme

### arch linux style (default)
- clean output
- colored status messages
- progress bars
- minimal design

colors:
- [*] info: blue
- [+] success: green
- [-] error: red
- [!] warning: yellow

## changing themes

### gui
1. open settings tab
2. select theme from dropdown
3. theme applies instantly

### cli
cli uses arch linux theme by default (not changeable to keep it clean)

## theme colors

each theme has:
- background (bg)
- alternate background (bg_alt)
- foreground text (fg)
- dimmed text (fg_dim)
- accent color (accent)
- success color (success)
- warning color (warning)
- error color (error)
- border color (border)

## creating custom themes

edit `/home/stuxnet/MyTools/ImageGhost/gui/themes.py`

add new theme to THEMES dict:
```python
'my_theme': {
    'name': 'My Theme',
    'colors': {
        'bg': '#000000',
        'fg': '#ffffff',
        ...
    },
    'stylesheet': '''...'''
}
```
