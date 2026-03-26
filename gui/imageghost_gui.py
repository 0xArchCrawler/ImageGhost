#!/usr/bin/env python3
# imageghost gui
# arch linux inspired interface

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QFileDialog, QProgressBar, QCheckBox, QComboBox,
                             QLineEdit, QTabWidget, QGroupBox, QMessageBox,
                             QListWidget, QInputDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scrubber import ImageScrubber
from core.crypto import ImageCrypto
from core.secure_delete import SecureDelete
from gui.themes import THEMES, apply_theme, get_theme_names


class WorkerThread(QThread):
    """background processing thread"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)

    def __init__(self, operation, params):
        super().__init__()
        self.operation = operation
        self.params = params

    def run(self):
        try:
            if self.operation == 'scrub':
                self._scrub()
            elif self.operation == 'encrypt':
                self._encrypt()
            elif self.operation == 'pipeline':
                self._pipeline()
        except Exception as e:
            self.finished.emit({'success': False, 'error': str(e)})

    def _scrub(self):
        scrubber = ImageScrubber(verbose=False)
        files = self.params['files']
        output_dir = self.params['output_dir']
        total = len(files)

        for idx, file_path in enumerate(files, 1):
            filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, filename)

            self.progress.emit(int((idx / total) * 100), f"scrubbing {filename}...")
            scrubber.scrub_image(file_path, output_path)

        stats = scrubber.get_stats()
        self.finished.emit({'success': True, 'stats': stats})

    def _encrypt(self):
        crypto = ImageCrypto(verbose=False)
        files = self.params['files']
        output_dir = self.params['output_dir']
        password = self.params['password']
        total = len(files)

        for idx, file_path in enumerate(files, 1):
            filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, filename + '.encrypted')

            self.progress.emit(int((idx / total) * 100), f"encrypting {filename}...")
            crypto.encrypt_file(file_path, output_path, password)

        self.finished.emit({'success': True})

    def _pipeline(self):
        # full pipeline implementation
        pass


class ImageGhostGUI(QMainWindow):
    """main gui window"""

    def __init__(self):
        super().__init__()
        self.current_theme = 'arch_dark'
        self.files = []
        self.setup_window()
        self.setup_ui()
        apply_theme(self, self.current_theme)

    def setup_window(self):
        self.setWindowTitle("imageghost v3.0")
        self.setGeometry(100, 100, 1100, 750)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # header
        header = self.create_header()
        layout.addWidget(header)

        # tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_scrub_tab(), "scrub")
        tabs.addTab(self.create_encrypt_tab(), "encrypt")
        tabs.addTab(self.create_pipeline_tab(), "pipeline")
        tabs.addTab(self.create_settings_tab(), "settings")
        layout.addWidget(tabs)

        self.statusBar().showMessage("ready")

    def create_header(self):
        """create header widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("IMAGEGHOST")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("monospace", 20, QFont.Bold))
        layout.addWidget(title)

        subtitle = QLabel("metadata scrubber + encryption")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("monospace", 10))
        layout.addWidget(subtitle)

        return widget

    def create_scrub_tab(self):
        """create scrubbing tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # file selection
        file_group = QGroupBox("images")
        file_layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("add images")
        btn_add.clicked.connect(self.add_images)
        btn_clear = QPushButton("clear")
        btn_clear.clicked.connect(self.clear_images)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_clear)
        file_layout.addLayout(btn_layout)

        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list)

        self.file_count_label = QLabel("files: 0")
        file_layout.addWidget(self.file_count_label)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # options
        opt_group = QGroupBox("options")
        opt_layout = QVBoxLayout()

        self.check_encrypt = QCheckBox("encrypt after scrubbing")
        opt_layout.addWidget(self.check_encrypt)

        self.check_shred = QCheckBox("securely delete originals")
        opt_layout.addWidget(self.check_shred)

        shred_layout = QHBoxLayout()
        shred_layout.addWidget(QLabel("shred method:"))
        self.combo_shred = QComboBox()
        self.combo_shred.addItems(['dod 5220.22-m', 'gutmann 35-pass', 'random 7-pass', 'quick 3-pass'])
        shred_layout.addWidget(self.combo_shred)
        shred_layout.addStretch()
        opt_layout.addLayout(shred_layout)

        opt_group.setLayout(opt_layout)
        layout.addWidget(opt_group)

        # progress
        self.progress_scrub = QProgressBar()
        layout.addWidget(self.progress_scrub)

        self.status_scrub = QLabel("ready")
        layout.addWidget(self.status_scrub)

        # execute
        btn_exec = QPushButton("START SCRUBBING")
        btn_exec.clicked.connect(self.execute_scrub)
        layout.addWidget(btn_exec)

        return widget

    def create_encrypt_tab(self):
        """create encryption tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info = QLabel("aes-256-gcm encryption with argon2id key derivation")
        layout.addWidget(info)

        # file selection
        file_group = QGroupBox("files")
        file_layout = QVBoxLayout()

        btn_select = QPushButton("select files")
        btn_select.clicked.connect(self.select_encrypt_files)
        file_layout.addWidget(btn_select)

        self.encrypt_file_list = QListWidget()
        file_layout.addWidget(self.encrypt_file_list)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # password
        pwd_group = QGroupBox("password")
        pwd_layout = QVBoxLayout()

        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("enter password (12+ chars)")
        pwd_layout.addWidget(self.pwd_input)

        self.pwd_confirm = QLineEdit()
        self.pwd_confirm.setEchoMode(QLineEdit.Password)
        self.pwd_confirm.setPlaceholderText("confirm password")
        pwd_layout.addWidget(self.pwd_confirm)

        btn_gen = QPushButton("generate secure password")
        btn_gen.clicked.connect(self.generate_password)
        pwd_layout.addWidget(btn_gen)

        pwd_group.setLayout(pwd_layout)
        layout.addWidget(pwd_group)

        # progress
        self.progress_encrypt = QProgressBar()
        layout.addWidget(self.progress_encrypt)

        # execute
        btn_encrypt = QPushButton("ENCRYPT FILES")
        btn_encrypt.clicked.connect(self.execute_encrypt)
        layout.addWidget(btn_encrypt)

        layout.addStretch()

        return widget

    def create_pipeline_tab(self):
        """create pipeline tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info = QLabel("full pipeline: scrub → encrypt → shred")
        layout.addWidget(info)

        warning = QLabel("⚠ warning: original files will be permanently deleted")
        layout.addWidget(warning)

        # directory
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("directory:"))
        self.dir_input = QLineEdit()
        dir_layout.addWidget(self.dir_input)
        btn_browse = QPushButton("browse")
        btn_browse.clicked.connect(self.browse_dir)
        dir_layout.addWidget(btn_browse)
        layout.addLayout(dir_layout)

        # password
        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(QLabel("password:"))
        self.pipeline_pwd = QLineEdit()
        self.pipeline_pwd.setEchoMode(QLineEdit.Password)
        pwd_layout.addWidget(self.pipeline_pwd)
        layout.addLayout(pwd_layout)

        # options
        self.check_pipeline_shred = QCheckBox("shred originals (irreversible)")
        layout.addWidget(self.check_pipeline_shred)

        # progress
        self.progress_pipeline = QProgressBar()
        layout.addWidget(self.progress_pipeline)

        self.status_pipeline = QLabel("")
        layout.addWidget(self.status_pipeline)

        # execute
        btn_pipeline = QPushButton("RUN PIPELINE")
        btn_pipeline.clicked.connect(self.execute_pipeline)
        layout.addWidget(btn_pipeline)

        layout.addStretch()

        return widget

    def create_settings_tab(self):
        """create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # theme selection
        theme_group = QGroupBox("theme")
        theme_layout = QVBoxLayout()

        theme_layout.addWidget(QLabel("select theme:"))

        self.combo_theme = QComboBox()
        theme_names = [THEMES[k]['name'] for k in THEMES.keys()]
        self.combo_theme.addItems(theme_names)
        self.combo_theme.setCurrentText(THEMES[self.current_theme]['name'])
        self.combo_theme.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(self.combo_theme)

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # about
        about_group = QGroupBox("about")
        about_layout = QVBoxLayout()

        about_text = QLabel("""
imageghost v3.0

multi-image fingerprint scrubber for pentesters and red-teamers

features:
• complete metadata removal (exif, gps, xmp, iptc, thumbnails)
• steganography trace removal
• aes-256-gcm encryption with argon2id
• dod 5220.22-m secure deletion
• batch processing (60-100+ images)
• support for 50+ image formats

for authorized security testing only
        """)
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)

        about_group.setLayout(about_layout)
        layout.addWidget(about_group)

        layout.addStretch()

        return widget

    def add_images(self):
        """add images to list"""
        from core.formats import FORMATS

        extensions = ' '.join([f'*{ext}' for ext in FORMATS.keys()])
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "select images",
            "",
            f"images ({extensions})"
        )

        for file in files:
            if file not in self.files:
                self.files.append(file)
                self.file_list.addItem(os.path.basename(file))

        self.file_count_label.setText(f"files: {len(self.files)}")

    def clear_images(self):
        """clear image list"""
        self.files = []
        self.file_list.clear()
        self.file_count_label.setText("files: 0")

    def select_encrypt_files(self):
        """select files for encryption"""
        files, _ = QFileDialog.getOpenFileNames(self, "select files")
        self.encrypt_file_list.clear()
        self.encrypt_files = files
        for file in files:
            self.encrypt_file_list.addItem(os.path.basename(file))

    def browse_dir(self):
        """browse for directory"""
        directory = QFileDialog.getExistingDirectory(self, "select directory")
        if directory:
            self.dir_input.setText(directory)

    def generate_password(self):
        """generate secure password"""
        crypto = ImageCrypto(verbose=False)
        password = crypto.generate_secure_password(32)

        msg = QMessageBox()
        msg.setWindowTitle("generated password")
        msg.setText("secure password generated")
        msg.setInformativeText(f"password: {password}\n\nsave this securely!")
        msg.exec_()

        self.pwd_input.setText(password)
        self.pwd_confirm.setText(password)

    def change_theme(self, theme_name):
        """change gui theme"""
        # find theme key by name
        theme_key = None
        for key, val in THEMES.items():
            if val['name'] == theme_name:
                theme_key = key
                break

        if theme_key:
            self.current_theme = theme_key
            apply_theme(self, theme_key)

    def execute_scrub(self):
        """execute scrubbing"""
        if not self.files:
            QMessageBox.warning(self, "no files", "add images first")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "select output directory")
        if not output_dir:
            return

        params = {
            'files': self.files,
            'output_dir': output_dir
        }

        self.worker = WorkerThread('scrub', params)
        self.worker.progress.connect(self.update_scrub_progress)
        self.worker.finished.connect(self.scrub_finished)
        self.worker.start()

        self.status_scrub.setText("processing...")

    def update_scrub_progress(self, value, message):
        """update progress"""
        self.progress_scrub.setValue(value)
        self.status_scrub.setText(message)

    def scrub_finished(self, result):
        """handle completion"""
        if result.get('success'):
            stats = result.get('stats', {})
            msg = f"scrubbing complete\n\n"
            msg += f"processed: {stats.get('processed', 0)}\n"
            msg += f"failed: {stats.get('failed', 0)}\n"
            msg += f"metadata removed: {stats.get('bytes_removed', 0):,} bytes"

            QMessageBox.information(self, "success", msg)
            self.status_scrub.setText("complete")
            self.progress_scrub.setValue(100)
        else:
            QMessageBox.critical(self, "error", f"failed: {result.get('error')}")
            self.status_scrub.setText("failed")

    def execute_encrypt(self):
        """execute encryption"""
        if not hasattr(self, 'encrypt_files') or not self.encrypt_files:
            QMessageBox.warning(self, "no files", "select files first")
            return

        pwd1 = self.pwd_input.text()
        pwd2 = self.pwd_confirm.text()

        if not pwd1:
            QMessageBox.warning(self, "no password", "enter a password")
            return

        if pwd1 != pwd2:
            QMessageBox.warning(self, "mismatch", "passwords don't match")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "output directory")
        if not output_dir:
            return

        params = {
            'files': self.encrypt_files,
            'output_dir': output_dir,
            'password': pwd1
        }

        self.worker = WorkerThread('encrypt', params)
        self.worker.progress.connect(self.update_encrypt_progress)
        self.worker.finished.connect(self.encrypt_finished)
        self.worker.start()

    def update_encrypt_progress(self, value, message):
        """update encryption progress"""
        self.progress_encrypt.setValue(value)
        self.statusBar().showMessage(message)

    def encrypt_finished(self, result):
        """handle encryption completion"""
        if result.get('success'):
            QMessageBox.information(self, "success", "encryption complete")
            self.progress_encrypt.setValue(100)
        else:
            QMessageBox.critical(self, "error", f"failed: {result.get('error')}")

    def execute_pipeline(self):
        """execute full pipeline"""
        if not self.dir_input.text():
            QMessageBox.warning(self, "no directory", "select a directory")
            return

        if not self.pipeline_pwd.text():
            QMessageBox.warning(self, "no password", "enter a password")
            return

        if self.check_pipeline_shred.isChecked():
            reply = QMessageBox.question(
                self,
                "confirm",
                "this will permanently delete original files\n\nare you sure?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply != QMessageBox.Yes:
                return

        QMessageBox.information(self, "pipeline", "pipeline would run here")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = ImageGhostGUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
