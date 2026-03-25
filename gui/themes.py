# gui themes for imageghost
# arch linux inspired dark themes

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

THEMES = {
    'arch_dark': {
        'name': 'Arch Dark',
        'colors': {
            'bg': '#0d0d0d',
            'bg_alt': '#1a1a1a',
            'fg': '#ffffff',
            'fg_dim': '#808080',
            'accent': '#1793d1',
            'success': '#00ff00',
            'warning': '#ffaa00',
            'error': '#ff0000',
            'border': '#333333',
        },
        'stylesheet': '''
            QWidget {
                background-color: #0d0d0d;
                color: #ffffff;
                font-family: "Hack", "Fira Code", "DejaVu Sans Mono", monospace;
                font-size: 10pt;
            }
            QMainWindow {
                background-color: #0d0d0d;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #333333;
                padding: 8px 16px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #1793d1;
                border: 1px solid #1793d1;
            }
            QPushButton:pressed {
                background-color: #135d87;
            }
            QLineEdit, QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #333333;
                padding: 4px;
                border-radius: 2px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #1793d1;
            }
            QListWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 2px;
            }
            QListWidget::item:selected {
                background-color: #1793d1;
            }
            QProgressBar {
                background-color: #1a1a1a;
                border: 1px solid #333333;
                border-radius: 2px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #1793d1;
            }
            QGroupBox {
                border: 1px solid #333333;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #1793d1;
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                background-color: #0d0d0d;
            }
            QTabBar::tab {
                background-color: #1a1a1a;
                color: #808080;
                padding: 8px 16px;
                border: 1px solid #333333;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0d0d0d;
                color: #1793d1;
                border-bottom: 2px solid #1793d1;
            }
            QComboBox {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #333333;
                padding: 4px;
                border-radius: 2px;
            }
            QComboBox:hover {
                border: 1px solid #1793d1;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #ffffff;
            }
            QCheckBox {
                color: #ffffff;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #333333;
                border-radius: 2px;
                background-color: #1a1a1a;
            }
            QCheckBox::indicator:checked {
                background-color: #1793d1;
                border: 1px solid #1793d1;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QStatusBar {
                background-color: #1a1a1a;
                color: #808080;
                border-top: 1px solid #333333;
            }
        '''
    },

    'blackarch': {
        'name': 'BlackArch',
        'colors': {
            'bg': '#000000',
            'bg_alt': '#0a0a0a',
            'fg': '#00ff00',
            'fg_dim': '#008800',
            'accent': '#ff0000',
            'success': '#00ff00',
            'warning': '#ffaa00',
            'error': '#ff0000',
            'border': '#00ff00',
        },
        'stylesheet': '''
            QWidget {
                background-color: #000000;
                color: #00ff00;
                font-family: "Terminus", "Hack", monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #0a0a0a;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 8px 16px;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
            }
            QLineEdit, QTextEdit {
                background-color: #0a0a0a;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 4px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #00ff00;
            }
            QListWidget {
                background-color: #0a0a0a;
                color: #00ff00;
                border: 1px solid #00ff00;
            }
            QListWidget::item:selected {
                background-color: #00ff00;
                color: #000000;
            }
            QProgressBar {
                background-color: #0a0a0a;
                border: 1px solid #00ff00;
                text-align: center;
                color: #00ff00;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
            }
            QGroupBox {
                border: 1px solid #00ff00;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #ff0000;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 1px solid #00ff00;
            }
            QTabBar::tab {
                background-color: #0a0a0a;
                color: #008800;
                padding: 8px 16px;
                border: 1px solid #00ff00;
            }
            QTabBar::tab:selected {
                background-color: #000000;
                color: #00ff00;
                border-bottom: 2px solid #ff0000;
            }
            QCheckBox {
                color: #00ff00;
            }
            QCheckBox::indicator {
                border: 1px solid #00ff00;
                background-color: #0a0a0a;
            }
            QCheckBox::indicator:checked {
                background-color: #00ff00;
            }
            QStatusBar {
                background-color: #0a0a0a;
                color: #00ff00;
                border-top: 1px solid #00ff00;
            }
        '''
    },

    'dracula': {
        'name': 'Dracula',
        'colors': {
            'bg': '#282a36',
            'bg_alt': '#44475a',
            'fg': '#f8f8f2',
            'fg_dim': '#6272a4',
            'accent': '#bd93f9',
            'success': '#50fa7b',
            'warning': '#ffb86c',
            'error': '#ff5555',
            'border': '#6272a4',
        },
        'stylesheet': '''
            QWidget {
                background-color: #282a36;
                color: #f8f8f2;
                font-family: "Fira Code", "Hack", monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #44475a;
                color: #f8f8f2;
                border: 1px solid #6272a4;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #bd93f9;
                border: 1px solid #bd93f9;
            }
            QLineEdit, QTextEdit {
                background-color: #44475a;
                color: #f8f8f2;
                border: 1px solid #6272a4;
                padding: 4px;
                border-radius: 2px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #bd93f9;
            }
            QListWidget {
                background-color: #44475a;
                color: #f8f8f2;
                border: 1px solid #6272a4;
            }
            QListWidget::item:selected {
                background-color: #bd93f9;
                color: #282a36;
            }
            QProgressBar {
                background-color: #44475a;
                border: 1px solid #6272a4;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #50fa7b;
                border-radius: 4px;
            }
            QGroupBox {
                border: 1px solid #6272a4;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #bd93f9;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 1px solid #6272a4;
            }
            QTabBar::tab {
                background-color: #44475a;
                color: #6272a4;
                padding: 8px 16px;
                border: 1px solid #6272a4;
            }
            QTabBar::tab:selected {
                background-color: #282a36;
                color: #bd93f9;
                border-bottom: 2px solid #bd93f9;
            }
            QCheckBox::indicator {
                border: 1px solid #6272a4;
                background-color: #44475a;
            }
            QCheckBox::indicator:checked {
                background-color: #bd93f9;
            }
            QStatusBar {
                background-color: #44475a;
                color: #6272a4;
                border-top: 1px solid #6272a4;
            }
        '''
    },

    'gruvbox': {
        'name': 'Gruvbox Dark',
        'colors': {
            'bg': '#282828',
            'bg_alt': '#3c3836',
            'fg': '#ebdbb2',
            'fg_dim': '#928374',
            'accent': '#fabd2f',
            'success': '#b8bb26',
            'warning': '#fe8019',
            'error': '#fb4934',
            'border': '#504945',
        },
        'stylesheet': '''
            QWidget {
                background-color: #282828;
                color: #ebdbb2;
                font-family: "Iosevka", "Hack", monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #3c3836;
                color: #ebdbb2;
                border: 1px solid #504945;
                padding: 8px 16px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #fabd2f;
                color: #282828;
                border: 1px solid #fabd2f;
            }
            QLineEdit, QTextEdit {
                background-color: #3c3836;
                color: #ebdbb2;
                border: 1px solid #504945;
                padding: 4px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #fabd2f;
            }
            QListWidget {
                background-color: #3c3836;
                color: #ebdbb2;
                border: 1px solid #504945;
            }
            QListWidget::item:selected {
                background-color: #fabd2f;
                color: #282828;
            }
            QProgressBar {
                background-color: #3c3836;
                border: 1px solid #504945;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #b8bb26;
            }
            QGroupBox {
                border: 1px solid #504945;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #fabd2f;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 1px solid #504945;
            }
            QTabBar::tab {
                background-color: #3c3836;
                color: #928374;
                padding: 8px 16px;
                border: 1px solid #504945;
            }
            QTabBar::tab:selected {
                background-color: #282828;
                color: #fabd2f;
                border-bottom: 2px solid #fabd2f;
            }
            QCheckBox::indicator {
                border: 1px solid #504945;
                background-color: #3c3836;
            }
            QCheckBox::indicator:checked {
                background-color: #fabd2f;
            }
            QStatusBar {
                background-color: #3c3836;
                color: #928374;
                border-top: 1px solid #504945;
            }
        '''
    },

    'green_hacker': {
        'name': 'Green Hacker',
        'colors': {
            'bg': '#0a0e0a',
            'bg_alt': '#0f140f',
            'fg': '#33ff33',
            'fg_dim': '#1a9919',
            'accent': '#00ff41',
            'success': '#39ff14',
            'warning': '#ffff00',
            'error': '#ff1744',
            'border': '#00ff41',
        },
        'stylesheet': '''
            QWidget {
                background-color: #0a0e0a;
                color: #33ff33;
                font-family: "Terminus", "Courier New", monospace;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton {
                background-color: #0f140f;
                color: #00ff41;
                border: 2px solid #00ff41;
                padding: 8px 16px;
                border-radius: 0px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff41;
                color: #0a0e0a;
                border: 2px solid #39ff14;
            }
            QPushButton:pressed {
                background-color: #39ff14;
                color: #0a0e0a;
            }
            QLineEdit, QTextEdit {
                background-color: #0f140f;
                color: #33ff33;
                border: 2px solid #00ff41;
                padding: 4px;
                selection-background-color: #00ff41;
                selection-color: #0a0e0a;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #39ff14;
                background-color: #0a0e0a;
            }
            QListWidget {
                background-color: #0f140f;
                color: #33ff33;
                border: 2px solid #00ff41;
            }
            QListWidget::item:selected {
                background-color: #00ff41;
                color: #0a0e0a;
            }
            QProgressBar {
                background-color: #0f140f;
                border: 2px solid #00ff41;
                text-align: center;
                color: #33ff33;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #00ff41;
            }
            QGroupBox {
                border: 2px solid #00ff41;
                margin-top: 8px;
                padding-top: 12px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #39ff14;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 2px solid #00ff41;
            }
            QTabBar::tab {
                background-color: #0f140f;
                color: #1a9919;
                padding: 8px 16px;
                border: 2px solid #00ff41;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #0a0e0a;
                color: #39ff14;
                border-bottom: 3px solid #00ff41;
            }
            QCheckBox {
                color: #33ff33;
                font-weight: bold;
            }
            QCheckBox::indicator {
                border: 2px solid #00ff41;
                background-color: #0f140f;
            }
            QCheckBox::indicator:checked {
                background-color: #00ff41;
            }
            QStatusBar {
                background-color: #0f140f;
                color: #33ff33;
                border-top: 2px solid #00ff41;
                font-weight: bold;
            }
            QComboBox {
                background-color: #0f140f;
                color: #33ff33;
                border: 2px solid #00ff41;
            }
        '''
    },

    'blue_soc': {
        'name': 'Blue SOC Team',
        'colors': {
            'bg': '#0c1021',
            'bg_alt': '#151b2d',
            'fg': '#87ceeb',
            'fg_dim': '#4682b4',
            'accent': '#00bfff',
            'success': '#00ff7f',
            'warning': '#ffa500',
            'error': '#ff4444',
            'border': '#1e90ff',
        },
        'stylesheet': '''
            QWidget {
                background-color: #0c1021;
                color: #87ceeb;
                font-family: "Roboto Mono", "Consolas", monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #151b2d;
                color: #87ceeb;
                border: 2px solid #1e90ff;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1e90ff;
                color: #ffffff;
                border: 2px solid #00bfff;
            }
            QPushButton:pressed {
                background-color: #00bfff;
            }
            QLineEdit, QTextEdit {
                background-color: #151b2d;
                color: #87ceeb;
                border: 2px solid #1e90ff;
                padding: 4px;
                border-radius: 2px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #00bfff;
                background-color: #0c1021;
            }
            QListWidget {
                background-color: #151b2d;
                color: #87ceeb;
                border: 2px solid #1e90ff;
                border-radius: 2px;
            }
            QListWidget::item:selected {
                background-color: #1e90ff;
                color: #ffffff;
            }
            QProgressBar {
                background-color: #151b2d;
                border: 2px solid #1e90ff;
                border-radius: 4px;
                text-align: center;
                color: #87ceeb;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e90ff, stop:1 #00bfff);
                border-radius: 2px;
            }
            QGroupBox {
                border: 2px solid #1e90ff;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #00bfff;
                font-weight: bold;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 2px solid #1e90ff;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #151b2d;
                color: #4682b4;
                padding: 8px 16px;
                border: 2px solid #1e90ff;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0c1021;
                color: #00bfff;
                border-bottom: 3px solid #00bfff;
                font-weight: bold;
            }
            QCheckBox {
                color: #87ceeb;
            }
            QCheckBox::indicator {
                border: 2px solid #1e90ff;
                background-color: #151b2d;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #1e90ff;
            }
            QStatusBar {
                background-color: #151b2d;
                color: #87ceeb;
                border-top: 2px solid #1e90ff;
            }
        '''
    },

    'red_team': {
        'name': 'Red Team Ops',
        'colors': {
            'bg': '#1a0000',
            'bg_alt': '#2d0000',
            'fg': '#ff6b6b',
            'fg_dim': '#cc0000',
            'accent': '#ff0000',
            'success': '#00ff00',
            'warning': '#ffaa00',
            'error': '#ffffff',
            'border': '#ff0000',
        },
        'stylesheet': '''
            QWidget {
                background-color: #1a0000;
                color: #ff6b6b;
                font-family: "Hack", "Monaco", monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #2d0000;
                color: #ff6b6b;
                border: 2px solid #ff0000;
                padding: 8px 16px;
                border-radius: 2px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff0000;
                color: #ffffff;
                border: 2px solid #ff4444;
            }
            QPushButton:pressed {
                background-color: #cc0000;
            }
            QLineEdit, QTextEdit {
                background-color: #2d0000;
                color: #ff6b6b;
                border: 2px solid #ff0000;
                padding: 4px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #ff4444;
                background-color: #1a0000;
            }
            QListWidget {
                background-color: #2d0000;
                color: #ff6b6b;
                border: 2px solid #ff0000;
            }
            QListWidget::item:selected {
                background-color: #ff0000;
                color: #ffffff;
            }
            QProgressBar {
                background-color: #2d0000;
                border: 2px solid #ff0000;
                text-align: center;
                color: #ff6b6b;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
            }
            QGroupBox {
                border: 2px solid #ff0000;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #ff4444;
                font-weight: bold;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 2px solid #ff0000;
            }
            QTabBar::tab {
                background-color: #2d0000;
                color: #cc0000;
                padding: 8px 16px;
                border: 2px solid #ff0000;
            }
            QTabBar::tab:selected {
                background-color: #1a0000;
                color: #ff4444;
                border-bottom: 3px solid #ff0000;
                font-weight: bold;
            }
            QCheckBox {
                color: #ff6b6b;
            }
            QCheckBox::indicator {
                border: 2px solid #ff0000;
                background-color: #2d0000;
            }
            QCheckBox::indicator:checked {
                background-color: #ff0000;
            }
            QStatusBar {
                background-color: #2d0000;
                color: #ff6b6b;
                border-top: 2px solid #ff0000;
            }
        '''
    },

    'purple_team': {
        'name': 'Purple Team',
        'colors': {
            'bg': '#1a0a1f',
            'bg_alt': '#2d1533',
            'fg': '#c792ea',
            'fg_dim': '#9c5cb8',
            'accent': '#bb86fc',
            'success': '#00ff7f',
            'warning': '#ffca28',
            'error': '#ff6b6b',
            'border': '#bb86fc',
        },
        'stylesheet': '''
            QWidget {
                background-color: #1a0a1f;
                color: #c792ea;
                font-family: "Fira Code", "Source Code Pro", monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #2d1533;
                color: #c792ea;
                border: 2px solid #bb86fc;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #bb86fc;
                color: #1a0a1f;
            }
            QLineEdit, QTextEdit {
                background-color: #2d1533;
                color: #c792ea;
                border: 2px solid #bb86fc;
                padding: 4px;
                border-radius: 2px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #d4aafc;
            }
            QListWidget {
                background-color: #2d1533;
                color: #c792ea;
                border: 2px solid #bb86fc;
            }
            QListWidget::item:selected {
                background-color: #bb86fc;
                color: #1a0a1f;
            }
            QProgressBar {
                background-color: #2d1533;
                border: 2px solid #bb86fc;
                border-radius: 4px;
                text-align: center;
                color: #c792ea;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #bb86fc, stop:0.5 #d4aafc, stop:1 #bb86fc);
                border-radius: 2px;
            }
            QGroupBox {
                border: 2px solid #bb86fc;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #d4aafc;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 2px solid #bb86fc;
            }
            QTabBar::tab {
                background-color: #2d1533;
                color: #9c5cb8;
                padding: 8px 16px;
                border: 2px solid #bb86fc;
            }
            QTabBar::tab:selected {
                background-color: #1a0a1f;
                color: #d4aafc;
                border-bottom: 3px solid #bb86fc;
            }
            QCheckBox::indicator {
                border: 2px solid #bb86fc;
                background-color: #2d1533;
            }
            QCheckBox::indicator:checked {
                background-color: #bb86fc;
            }
            QStatusBar {
                background-color: #2d1533;
                color: #c792ea;
                border-top: 2px solid #bb86fc;
            }
        '''
    },

    'nord': {
        'name': 'Nord',
        'colors': {
            'bg': '#2e3440',
            'bg_alt': '#3b4252',
            'fg': '#eceff4',
            'fg_dim': '#d8dee9',
            'accent': '#88c0d0',
            'success': '#a3be8c',
            'warning': '#ebcb8b',
            'error': '#bf616a',
            'border': '#4c566a',
        },
        'stylesheet': '''
            QWidget {
                background-color: #2e3440;
                color: #eceff4;
                font-family: "JetBrains Mono", "Menlo", monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #3b4252;
                color: #eceff4;
                border: 1px solid #4c566a;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #88c0d0;
                color: #2e3440;
                border: 1px solid #88c0d0;
            }
            QLineEdit, QTextEdit {
                background-color: #3b4252;
                color: #eceff4;
                border: 1px solid #4c566a;
                padding: 4px;
                border-radius: 2px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #88c0d0;
            }
            QListWidget {
                background-color: #3b4252;
                color: #eceff4;
                border: 1px solid #4c566a;
            }
            QListWidget::item:selected {
                background-color: #88c0d0;
                color: #2e3440;
            }
            QProgressBar {
                background-color: #3b4252;
                border: 1px solid #4c566a;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #88c0d0;
                border-radius: 2px;
            }
            QGroupBox {
                border: 1px solid #4c566a;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #88c0d0;
                left: 8px;
                padding: 0 4px;
            }
            QTabWidget::pane {
                border: 1px solid #4c566a;
            }
            QTabBar::tab {
                background-color: #3b4252;
                color: #d8dee9;
                padding: 8px 16px;
                border: 1px solid #4c566a;
            }
            QTabBar::tab:selected {
                background-color: #2e3440;
                color: #88c0d0;
                border-bottom: 2px solid #88c0d0;
            }
            QCheckBox::indicator {
                border: 1px solid #4c566a;
                background-color: #3b4252;
            }
            QCheckBox::indicator:checked {
                background-color: #88c0d0;
            }
            QStatusBar {
                background-color: #3b4252;
                color: #d8dee9;
                border-top: 1px solid #4c566a;
            }
        '''
    }
}

def get_theme(theme_name):
    """get theme by name"""
    return THEMES.get(theme_name, THEMES['arch_dark'])

def get_theme_names():
    """get list of available theme names"""
    return [t['name'] for t in THEMES.values()]

def apply_theme(widget, theme_name):
    """apply theme to widget"""
    theme = get_theme(theme_name)
    widget.setStyleSheet(theme['stylesheet'])

def get_theme(theme_name):
    """get theme by name"""
    return THEMES.get(theme_name, THEMES['arch_dark'])

def get_theme_names():
    """get list of available theme names"""
    return [t['name'] for t in THEMES.values()]

def apply_theme(widget, theme_name):
    """apply theme to widget"""
    theme = get_theme(theme_name)
    widget.setStyleSheet(theme['stylesheet'])
