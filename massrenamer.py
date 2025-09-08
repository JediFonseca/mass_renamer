# Copyright 2025 Jedielson da Fonseca
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Author: Jedielson da Fonseca jdfn7@proton.me

import os
import json
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QPlainTextEdit, QFileDialog, QMessageBox, QFrame,
    QTextEdit, QHBoxLayout, QMenu, QStyledItemDelegate
)
from PyQt6.QtGui import QIcon, QFont, QPainter, QColor, QTextFormat, QCursor, QAction
from PyQt6.QtCore import Qt, QRect, QSize, QEvent

# forbidden characters on Windows
ILLEGAL_CHARS = set('<>:"/\\|?*')

# most popular extensions
POPULAR_EXTS = [
    ".txt", ".jpg", ".png", ".webp", ".pdf", ".docx",
    ".xlsx", ".mp3", ".mp4", ".avi", ".mkv", ".zip", ".py"
]

# --- Stylesheets for Dark and Light Themes ---
DARK_STYLESHEET = """
    QWidget {
        background-color: #282828;
        color: #e8e8e8;
        font-family: 'Segoe UI';
        font-size: 10pt;
    }
    QMainWindow {
        background-color: #282828;
    }
    QPlainTextEdit, QLineEdit {
        background-color: #3c3c3c;
        border: 1px solid #555;
        border-radius: 5px;
        padding: 5px;
        font-family: 'Consolas';
        font-size: 11pt;
    }

    /* --- CONTROLES PARA BOTÕES (Selecionar, Carregar, Renomear, Desfazer) --- */
    QPushButton {
        padding: 8px 16px;
        font-size: 10pt;
        background-color: #3e82d8;
        color: white;
        border: none;
        border-radius: 5px;
    }

    /* --- CONTROLES PARA SELETORES (Idioma, Tema, Extensões) --- */
    QComboBox, QPushButton#ExtButton {
        padding: 6px 16px;
        font-size: 10pt;
        background-color: #3c3c3c;
        color: white;
        border: 1px solid #555;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color: #4a90e2;
    }
    QPushButton:disabled {
        background-color: #555;
        color: #999;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox QAbstractItemView {
        background-color: #3c3c3c;
        border: 1px solid #555;
        selection-background-color: #3e82d8;
    }
    QComboBox QAbstractItemView::item:hover, QMenu::item:selected {
        background-color: #4a90e2;
        color: #ffffff;
    }
    QLabel#HelpLabel {
        color: #3e82d8;
        font-weight: bold;
    }
"""

LIGHT_STYLESHEET = """
    QWidget {
        background-color: #e8e8e8;
        color: #282828;
        font-family: 'Segoe UI';
        font-size: 10pt;
    }
    QMainWindow {
        background-color: #e8e8e8;
    }
    QPlainTextEdit, QLineEdit {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px;
        font-family: 'Consolas';
        font-size: 11pt;
    }

    /* --- CONTROLES PARA BOTÕES (Selecionar, Carregar, Renomear, Desfazer) --- */
    QPushButton {
        padding: 8px 16px;
        font-size: 10pt;
        background-color: #3e82d8;
        color: white;
        border: none;
        border-radius: 5px;
    }
    
    /* --- CONTROLES PARA SELETORES (Idioma, Tema, Extensões) --- */
    QComboBox, QPushButton#ExtButton {
        padding: 6px 16px;
        font-size: 10pt;
        background-color: #ffffff;
        color: #282828;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color: #4a90e2;
    }
    QPushButton:disabled {
        background-color: #ccc;
        color: #777;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        border: 1px solid #ccc;
        selection-background-color: #3e82d8;
    }
    QComboBox QAbstractItemView::item:hover, QMenu::item:selected {
        background-color: #4a90e2;
        color: #ffffff;
    }
    QLabel#HelpLabel {
        color: #3e82d8;
        font-weight: bold;
    }
"""

# rename history (for undo)
rename_history = []

# --- Translation dictionaries ---
LANG_TEXTS = {
    "en": {
        "title": "Mass Renamer 2.0", "help": "Help", "dark_mode": "Dark Mode", "dark": "Dark",
        "light": "Light", "file_location": "📂 File location:", "select_folder": "Select folder",
        "load_original": "Load names", "add_extension": "Add extension:",
        "orig_names": "Original names (one per line):", "new_names": "New names (one per line):",
        "log": "Log", "rename": "Rename files", "undo": "Undo", "error": "Error",
        "map_error": "Mapping Error", "invalid_chars": "Invalid characters",
        "invalid_chars_msg": "There are forbidden characters in the new names.\nDo you want to remove them?",
        "not_found": "Not found:", "error_renaming": "Error renaming", "done": "🏁 Done.",
        "undo_confirm": "Confirm undo all renames?", "undo_done": "🏁 Undo completed.",
        "undoing": "⏮︎ Undoing...", "error_undoing": "Error undoing",
        "cannot_list": "Could not list files:", "select_valid_folder": "Select a valid folder.",
        "map_error_msg": "{0} original names vs {1} new names",
        "help_text": (
            "<p>1. Select the folder where the files to be renamed are located.<br>"
            "2. Enter the original names of all files in the field \"Original names\".<br>"
            "3. Enter the new names in the field \"New names\".<br>"
            "4. Click on \"Rename files\".</p>"
            "<p><b>NOTE:</b> The file whose original name is on line \"1\" of the field \"Original names\" "
            "will be renamed to the name that is on line \"1\" of the field \"New names\" and so on.</p>"
            "<hr>"
            "<p>License: <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\">Apache License 2.0</a><br>"
            "Author: <a href=\"https://www.instagram.com/jedifonseca/\">2025 Jedielson da Fonseca</a><br>"
            "<a href=\"https://github.com/JediFonseca/mass_renamer\">Github</a></p>"
        )
    },
    "pt": {
        "title": "Mass Renamer 2.0", "help": "Ajuda", "dark_mode": "Modo Escuro", "dark": "Escuro",
        "light": "Claro", "file_location": "📂 Localização dos arquivos:",
        "select_folder": "Selecionar pasta", "load_original": "Carregar nomes",
        "add_extension": "Adicionar extensão:", "orig_names": "Nomes originais (um por linha):",
        "new_names": "Novos nomes (um por linha):", "log": "Log", "rename": "Renomear Arquivos",
        "undo": "Desfazer", "error": "Erro", "map_error": "Erro de Mapeamento",
        "invalid_chars": "Caracteres inválidos",
        "invalid_chars_msg": "Há caracteres não permitidos nos novos nomes.\nDeseja removê-los?",
        "not_found": "Não encontrado:", "error_renaming": "Erro renomeando", "done": "🏁 Concluído.",
        "undo_confirm": "Confirmar desfazer todas renomeações?", "undo_done": "🏁 Desfazer concluído.",
        "undoing": "⏮︎ Desfazendo...", "error_undoing": "Erro desfazendo",
        "cannot_list": "Não foi possível listar arquivos:", "select_valid_folder": "Selecione uma pasta válida.",
        "map_error_msg": "{0} nomes originais vs {1} nomes novos",
        "help_text": (
            "<p>1. Selecione a pasta onde os arquivos a serem renomeados estão localizados.<br>"
            "2. Indique os nomes originais de todos os arquivos no campo \"Nomes originais\".<br>"
            "3. Indique os novos nomes no campo \"Novos nomes\".<br>"
            "4. Clique em \"Renomear arquivos\".</p>"
            "<p><b>OBS.:</b> O arquivo cujo nome original estiver na linha \"1\" do campo \"Nomes originais\" "
            "será renomeado para o nome que está na linha \"1\" do campo \"Novos nomes\" e assim sucessivamente.</p>"
            "<hr>"
            "<p>Licença: <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\">Apache License 2.0</a><br>"
            "Autor: <a href=\"https://www.instagram.com/jedifonseca/\">2025 Jedielson da Fonseca</a><br>"
            "<a href=\"https://github.com/JediFonseca/mass_renamer\">Github</a></p>"
        )
    }
}

CONFIG_PATH = "config.json"

# ATUALIZAÇÃO: Função de path robusta para dev, compilado e AppImage
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev, PyInstaller/Nuitka, and AppImage. """
    # Check for AppImage environment variable
    appdir = os.environ.get('APPDIR')
    if appdir:
        base_path = appdir
    else:
        # Check for PyInstaller/Nuitka temporary folder
        try:
            base_path = sys._MEIPASS
        except Exception:
            # Fallback to script's current directory for development
            base_path = os.path.abspath(".")
            
    return os.path.join(base_path, relative_path)

# --- Custom Widget: QPlainTextEdit with Line Numbers ---
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count //= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        
        is_dark = QApplication.instance().styleSheet() == DARK_STYLESHEET
        bg_color = QColor("#282828") if is_dark else QColor("#e8e8e8")
        num_color = QColor("#9E9E9E") if is_dark else QColor("#757575")

        painter.fillRect(event.rect(), bg_color)
        
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(num_color)
                painter.drawText(0, int(top), self.lineNumberArea.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

class CenteredItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        super().paint(painter, option, index)

# --- Main Application Window ---
class MassRenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.current_lang = self.config["language"]
        self.current_theme = self.config["theme"]
        
        self.init_ui()

        initial_lang_text = "Português" if self.current_lang == "pt" else "English"
        self.set_language(initial_lang_text)
        
        self.change_theme(self.tr(self.current_theme), startup=True)

    def load_config(self):
        default = {"language": "en", "theme": "dark"}
        if not os.path.exists(CONFIG_PATH):
            return default
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**default, **data}
        except Exception:
            return default

    def save_config(self, language=None, theme=None):
        if language is not None:
            self.config["language"] = language
        if theme is not None:
            self.config["theme"] = theme
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.config, f)
        except Exception:
            pass

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonRelease:
            if obj is self.lang_menu.lineEdit():
                self.lang_menu.showPopup()
                return True
            if obj is self.theme_menu.lineEdit():
                self.theme_menu.showPopup()
                return True
        return super().eventFilter(obj, event)

    def init_ui(self):
        self.setWindowIcon(QIcon(resource_path('appicon.svg')))
        self.setGeometry(100, 100, 900, 650)
        self.setMinimumSize(900, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QGridLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # --- Top controls ---
        self.label_location = QLabel()
        main_layout.addWidget(self.label_location, 0, 0, 1, 1)

        top_right_layout = QHBoxLayout()
        self.lang_menu = QComboBox()
        self.lang_menu.addItems(["English", "Português"])
        self.lang_menu.currentTextChanged.connect(self.change_lang)
        
        self.theme_menu = QComboBox()
        self.theme_menu.currentTextChanged.connect(self.change_theme)
        
        self.lang_menu.setLineEdit(QLineEdit())
        self.lang_menu.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lang_menu.lineEdit().setReadOnly(True)
        self.lang_menu.lineEdit().installEventFilter(self)

        self.theme_menu.setLineEdit(QLineEdit())
        self.theme_menu.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.theme_menu.lineEdit().setReadOnly(True)
        self.theme_menu.lineEdit().installEventFilter(self)

        self.centered_delegate = CenteredItemDelegate(self)
        self.lang_menu.view().setItemDelegate(self.centered_delegate)
        self.theme_menu.view().setItemDelegate(self.centered_delegate)

        top_right_layout.addWidget(self.lang_menu)
        top_right_layout.addWidget(self.theme_menu)
        main_layout.addLayout(top_right_layout, 0, 1, 1, 3, Qt.AlignmentFlag.AlignRight)

        self.entry_local = QLineEdit()
        main_layout.addWidget(self.entry_local, 1, 0, 1, 3)

        self.select_button = QPushButton()
        self.select_button.clicked.connect(self.selecionar_pasta)
        main_layout.addWidget(self.select_button, 1, 3)

        # --- Original names ---
        self.label_orig = QLabel()
        main_layout.addWidget(self.label_orig, 2, 0, 1, 4)
        
        self.text_orig = CodeEditor()
        main_layout.addWidget(self.text_orig, 3, 0, 1, 4)
        main_layout.setRowStretch(3, 1)

        ext_frame_o = QWidget()
        ext_layout_o = QHBoxLayout(ext_frame_o)
        ext_layout_o.setContentsMargins(0, 0, 0, 0)
        self.ext_label_o = QLabel()
        self.ext_button_o = QPushButton("▼")
        self.ext_button_o.setObjectName("ExtButton")
        self.ext_button_o.clicked.connect(lambda: self.show_extension_menu(self.ext_button_o, self.text_orig))
        ext_layout_o.addWidget(self.ext_label_o)
        ext_layout_o.addWidget(self.ext_button_o)
        ext_layout_o.addStretch(1)
        main_layout.addWidget(ext_frame_o, 4, 0, 1, 2)
        
        self.load_button = QPushButton()
        self.load_button.clicked.connect(self.carregar_nomes_originais)
        self.load_button.setEnabled(False)
        main_layout.addWidget(self.load_button, 4, 2, 1, 2, Qt.AlignmentFlag.AlignRight)

        # --- New names ---
        self.label_new = QLabel()
        main_layout.addWidget(self.label_new, 5, 0, 1, 4)

        self.text_new = CodeEditor()
        main_layout.addWidget(self.text_new, 6, 0, 1, 4)
        main_layout.setRowStretch(6, 1)

        ext_frame_n = QWidget()
        ext_layout_n = QHBoxLayout(ext_frame_n)
        ext_layout_n.setContentsMargins(0, 0, 0, 0)
        self.ext_label_n = QLabel()
        self.ext_button_n = QPushButton("▼")
        self.ext_button_n.setObjectName("ExtButton")
        self.ext_button_n.clicked.connect(lambda: self.show_extension_menu(self.ext_button_n, self.text_new))
        ext_layout_n.addWidget(self.ext_label_n)
        ext_layout_n.addWidget(self.ext_button_n)
        ext_layout_n.addStretch(1)
        main_layout.addWidget(ext_frame_n, 7, 0, 1, 2)
        
        # --- Log ---
        self.label_log = QLabel()
        main_layout.addWidget(self.label_log, 8, 0, 1, 4)

        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text, 9, 0, 1, 4)
        main_layout.setRowStretch(9, 1)

        # --- Bottom buttons ---
        buttons_frame = QWidget()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0,10,0,0)
        
        self.help_label = QLabel()
        self.help_label.setObjectName("HelpLabel")
        self.help_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.help_label.mousePressEvent = self.show_help
        
        self.rename_button = QPushButton()
        self.rename_button.clicked.connect(self.renomear)
        
        self.undo_button = QPushButton()
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self.desfazer)
        
        buttons_layout.addWidget(self.help_label, 0, Qt.AlignmentFlag.AlignLeft)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.rename_button)
        buttons_layout.addWidget(self.undo_button)

        main_layout.addWidget(buttons_frame, 10, 0, 1, 4)
        
        button_width = 150
        widgets_to_fix_width = [
            self.select_button, self.rename_button, self.undo_button,
            self.lang_menu, self.theme_menu, self.load_button
        ]
        for widget in widgets_to_fix_width:
            widget.setFixedWidth(button_width)
        
        self.ext_button_o.setFixedWidth(75)
        self.ext_button_n.setFixedWidth(75)

    def tr(self, key):
        """Translate text using the current language dictionary."""
        return LANG_TEXTS[self.current_lang].get(key, key)
    
    def show_extension_menu(self, button, text_widget):
        menu = QMenu(self)
        for ext in POPULAR_EXTS:
            action = menu.addAction(ext)
            action.triggered.connect(lambda checked, extension=ext: self.add_extension_to_widget(text_widget, extension))
        
        button_pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(button_pos)
        
    def set_language(self, lang_text):
        lang_code = "pt" if lang_text == "Português" else "en"
        self.current_lang = lang_code
        self.save_config(language=lang_code)

        self.setWindowTitle(self.tr("title"))
        self.help_label.setText(self.tr("help"))
        self.label_location.setText(self.tr("file_location"))
        self.select_button.setText(self.tr("select_folder"))
        self.load_button.setText(self.tr("load_original"))
        self.label_orig.setText(self.tr("orig_names"))
        self.label_new.setText(self.tr("new_names"))
        self.label_log.setText(self.tr("log"))
        self.rename_button.setText(self.tr("rename"))
        self.undo_button.setText(self.tr("undo"))
        self.ext_label_o.setText(self.tr("add_extension"))
        self.ext_label_n.setText(self.tr("add_extension"))

        current_idx = 1 if lang_code == 'pt' else 0
        self.lang_menu.blockSignals(True)
        self.lang_menu.setCurrentIndex(current_idx)
        self.lang_menu.blockSignals(False)

        current_theme_text = self.theme_menu.currentText()
        self.theme_menu.blockSignals(True)
        self.theme_menu.clear()
        self.theme_menu.addItems([self.tr("light"), self.tr("dark")])
        if current_theme_text in [LANG_TEXTS["en"]["dark"], LANG_TEXTS["pt"]["dark"]]:
             self.theme_menu.setCurrentText(self.tr("dark"))
        else:
             self.theme_menu.setCurrentText(self.tr("light"))
        self.theme_menu.blockSignals(False)

    def change_lang(self, lang_text):
        self.set_language(lang_text)
        
    def change_theme(self, choice, startup=False):
        mode = "dark" if choice == self.tr("dark") else "light"
        self.current_theme = mode
        stylesheet = DARK_STYLESHEET if mode == "dark" else LIGHT_STYLESHEET
        QApplication.instance().setStyleSheet(stylesheet)
        
        if not startup:
            self.save_config(theme=mode)
        
        self.theme_menu.blockSignals(True)
        self.theme_menu.setCurrentText(self.tr(mode))
        self.theme_menu.blockSignals(False)

    def show_help(self, event):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("help"))
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(self.tr("help_text"))
        msg_box.exec()

    def selecionar_pasta(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("select_folder"))
        if folder:
            self.entry_local.setText(folder)
            self.load_button.setEnabled(True)

    def add_extension_to_widget(self, text_widget, ext):
        current_text = text_widget.toPlainText()
        lines = [l.rstrip() for l in current_text.splitlines()]
        new_lines = []
        for l in lines:
            if not l:
                new_lines.append("")
                continue
            new_lines.append(l + ext)
        text_widget.setPlainText("\n".join(new_lines))

    def renomear(self):
        global rename_history
        rename_history.clear()

        folder = self.entry_local.text().strip()
        origs = [l.strip() for l in self.text_orig.toPlainText().splitlines() if l.strip()]
        news = [l.strip() for l in self.text_new.toPlainText().splitlines() if l.strip()]

        if not folder or not os.path.isdir(folder):
            QMessageBox.critical(self, self.tr("error"), self.tr("select_valid_folder"))
            return

        if len(origs) != len(news):
            QMessageBox.critical(
                self, self.tr("map_error"),
                self.tr("map_error_msg").format(len(origs), len(news))
            )
            return

        if any(ch in ILLEGAL_CHARS for name in news for ch in name):
            resp = QMessageBox.question(
                self, self.tr("invalid_chars"), self.tr("invalid_chars_msg"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if resp == QMessageBox.StandardButton.Yes:
                cleaned = [''.join(c for c in n if c not in ILLEGAL_CHARS) for n in news]
                self.text_new.setPlainText("\n".join(cleaned))
                news = cleaned
            else:
                return

        self.log_text.clear()
        for o, n in zip(origs, news):
            src = os.path.join(folder, o)
            dst = os.path.join(folder, n)
            if not os.path.exists(src):
                self.log_text.appendPlainText(f"❌ {self.tr('not_found')} {o}")
                continue
            try:
                os.rename(src, dst)
                rename_history.append((dst, src))
                self.log_text.appendPlainText(f"✅ {o} → {n}")
            except Exception as e:
                self.log_text.appendPlainText(f"⚠️ {self.tr('error_renaming')} {o}: {e}")

        if rename_history:
            self.undo_button.setEnabled(True)
        self.log_text.appendPlainText(f"\n{self.tr('done')}")

    def desfazer(self):
        global rename_history
        if not rename_history:
            return
        if QMessageBox.question(
            self, self.tr("undo"), self.tr("undo_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.No:
            return

        self.log_text.appendPlainText(f"\n{self.tr('undoing')}\n")
        for dst, src in reversed(rename_history):
            try:
                os.rename(dst, src)
                self.log_text.appendPlainText(f"↩️ {os.path.basename(dst)} → {os.path.basename(src)}")
            except Exception as e:
                self.log_text.appendPlainText(f"⚠️ {self.tr('error_undoing')} {dst}: {e}")

        self.log_text.appendPlainText(f"\n{self.tr('undo_done')}")
        rename_history.clear()
        self.undo_button.setEnabled(False)

    def carregar_nomes_originais(self):
        folder = self.entry_local.text().strip()
        if not folder or not os.path.isdir(folder):
            QMessageBox.critical(self, self.tr("error"), self.tr("select_valid_folder"))
            return
        try:
            items = os.listdir(folder)
            files = sorted(f for f in items if os.path.isfile(os.path.join(folder, f)))
        except Exception as e:
            QMessageBox.critical(self, self.tr("error"), f"{self.tr('cannot_list')}\n{e}")
            return

        self.text_orig.setPlainText("\n".join(files))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MassRenamerApp()
    window.show()
    sys.exit(app.exec())
