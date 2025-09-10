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
import shutil
import tempfile
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QPlainTextEdit, QFileDialog, QMessageBox,
    QHBoxLayout, QMenu, QStyledItemDelegate, QWidgetAction
)
from PyQt6.QtGui import QIcon, QPainter, QColor, QCursor
from PyQt6.QtCore import Qt, QRect, QSize, QEvent, QSettings

# Forbidden characters for filenames (Linux-focused)
ILLEGAL_CHARS = set('/')

# Most popular file extensions for the dropdown menu
POPULAR_EXTS = [
    ".jpg", ".png", ".webp", ".txt", ".pdf", ".docx", ".xlsx", ".pptx", ".ods", ".ots",
    ".odt", ".ott", ".odp", ".otp", ".mp3", ".ogg", ".flac", ".wav", ".mp4", ".avi", ".mkv", ".webm", ".zip", ".rar", ".7z"
]

# --- Stylesheets for Dark and Light Themes ---
DARK_STYLESHEET = """
    QWidget {
        background-color: #282828; color: #e8e8e8; font-family: 'Segoe UI'; font-size: 10pt;
    }
    QMainWindow { background-color: #282828; }
    QPlainTextEdit, QLineEdit {
        background-color: #3c3c3c; border: 1px solid #555; border-radius: 5px;
        padding: 5px; font-family: 'Consolas'; font-size: 11pt;
    }
    QPushButton {
        padding: 7px 16px; font-size: 10pt; background-color: #3e82d8;
        color: white; border: none; border-radius: 5px;
    }
    QPushButton#settingsBtn {
        padding: 6px 16px; font-size: 10pt; background-color: #3c3c3c;
        color: white; border: 1px solid #555; border-radius: 5px;
    }
    QMenu {
        background-color: #3c3c3c; border: 1px solid #555;
    }
    QMenu#extensionsMenu::item {
        padding: 3px 18px;
    }
    QPushButton:hover { background-color: #4a90e2; }
    QPushButton:disabled { background-color: #555; color: #999; }
    QMenu#extensionsMenu::item:selected {
        background-color: #4a90e2; color: #ffffff;
    }
    QLabel#HelpLabel { color: #3e82d8; font-weight: bold; }
"""

LIGHT_STYLESHEET = """
    QWidget {
        background-color: #e8e8e8; color: #282828; font-family: 'Segoe UI'; font-size: 10pt;
    }
    QMainWindow { background-color: #e8e8e8; }
    QPlainTextEdit, QLineEdit {
        background-color: #ffffff; border: 1px solid #ccc; border-radius: 5px;
        padding: 5px; font-family: 'Consolas'; font-size: 11pt;
    }
    QPushButton {
        padding: 7px 16px; font-size: 10pt; background-color: #3e82d8;
        color: white; border: none; border-radius: 5px;
    }
    QPushButton#settingsBtn {
        padding: 6px 16px; font-size: 10pt; background-color: #ffffff;
        color: #282828; border: 1px solid #ccc; border-radius: 5px;
    }
    QMenu {
        background-color: #ffffff; border: 1px solid #ccc;
    }
    QMenu#extensionsMenu::item {
        padding: 4px 20px;
    }
    QPushButton:hover { background-color: #4a90e2; }
    QPushButton:disabled { background-color: #ccc; color: #777; }
    QMenu#extensionsMenu::item:selected {
        background-color: #4a90e2; color: #ffffff;
    }
    QLabel#HelpLabel { color: #3e82d8; font-weight: bold; }
"""

# --- Translation Dictionaries ---
LANG_TEXTS = {
    "en": {
        "title": "Mass Renamer 2.1", "help": "Help", "dark": "Dark", "light": "Light",
        "file_location": "📂 File location:", "select_folder": "Select folder",
        "load_original": "Load names", "add_extension": "Add extension:",
        "orig_names": "Original names (one per line):", "new_names": "New names (one per line):",
        "log": "Log", "rename": "Rename Files", "undo": "Undo", "error": "Error", "yes": "Yes", "no": "No",
        "map_error": "Mapping Error", "invalid_chars": "Invalid Characters",
        "invalid_chars_msg": "The character '/' is not allowed in filenames.\nDo you want to remove it?",
        "not_found": "Not found or not a file:", "error_renaming": "Error renaming", "done": "🏁 Done.",
        "undo_confirm": "Confirm undo all renames?", "undo_done": "🏁 Undo completed.",
        "undoing": "⏮︎ Undoing...", "error_undoing": "Error undoing",
        "cannot_list": "Could not list files:", "select_valid_folder": "Select a valid folder.",
        "map_error_msg": "{0} original names vs {1} new names",
        "transfer_extensions": "Transf. Extensions", "remove_extension": "Remove Extensions",
        "conflict_title": "Name Conflict Found",
        "conflict_text": "Found {0} names that already exist in the destination folder.",
        "conflict_info": (
            "• Click on <b>\"Rename\"</b> to add a numeric suffix (e.g., name_(1).txt) to all conflicting names and continue.<br><br>"
            "• Click on <b>\"List Errors\"</b> to cancel the operation and see the lines with problems in the Log area for manual correction.<br><br>"
            "• Click on <b>\"Cancel\"</b> to close this window without doing anything."
        ),
        "conflict_btn_rename": "Rename", "conflict_btn_list": "List Errors", "conflict_btn_cancel": "Cancel",
        "help_text": "<p>1. Select the folder where the files are located.<br>2. Click \"Load names\" or enter the original names manually.<br>3. Enter the new names.<br>4. Click on \"Rename Files\".</p><p><b>NOTE:</b> The file on line \"1\" of original names will be renamed to the name on line \"1\" of new names, and so on.</p><hr><p>License: <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\">Apache 2.0</a><br>Author: <a href=\"https://www.instagram.com/jedifonseca/\">Jedielson da Fonseca</a><br><a href=\"https://github.com/JediFonseca/mass_renamer\">Github</a></p>"
    },
    "pt": {
        "title": "Mass Renamer 2.1", "help": "Ajuda", "dark": "Escuro", "light": "Claro",
        "file_location": "📂 Localização dos arquivos:", "select_folder": "Selecionar pasta",
        "load_original": "Carregar nomes", "add_extension": "Adicionar extensão:",
        "orig_names": "Nomes originais (um por linha):", "new_names": "Novos nomes (um por linha):",
        "log": "Log", "rename": "Renomear Arquivos", "undo": "Desfazer", "error": "Erro", "yes": "Sim", "no": "Não",
        "map_error": "Erro de Mapeamento", "invalid_chars": "Caracteres Inválidos",
        "invalid_chars_msg": "O caractere '/' não é permitido em nomes de arquivos.\nDeseja removê-lo?",
        "not_found": "Não encontrado ou não é um arquivo:", "error_renaming": "Erro renomeando", "done": "🏁 Concluído.",
        "undo_confirm": "Confirmar desfazer todas renomeações?", "undo_done": "🏁 Desfazer concluído.",
        "undoing": "⏮︎ Desfazendo...", "error_undoing": "Erro desfazendo",
        "cannot_list": "Não foi possível listar arquivos:", "select_valid_folder": "Selecione uma pasta válida.",
        "map_error_msg": "{0} nomes originais vs {1} nomes novos",
        "transfer_extensions": "Transf. Extensões", "remove_extension": "Remover Extensões",
        "conflict_title": "Conflito de Nomes Encontrado",
        "conflict_text": "Foram encontrados {0} nomes que já existem na pasta de destino.",
        "conflict_info": (
            "• Clique em <b>\"Renomear\"</b> para adicionar um sufixo numérico (ex: nome_(1).txt) a todos os nomes conflitantes e continuar.<br><br>"
            "• Clique em <b>\"Listar Erros\"</b> para cancelar a operação e ver as linhas com problemas na área de Log para correção manual.<br><br>"
            "• Clique em <b>\"Cancelar\"</b> para fechar esta janela sem fazer nada."
        ),
        "conflict_btn_rename": "Renomear", "conflict_btn_list": "Listar Erros", "conflict_btn_cancel": "Cancelar",
        "help_text": "<p>1. Selecione a pasta onde os arquivos estão.<br>2. Clique em \"Carregar nomes\" ou insira os nomes originais manualmente.<br>3. Indique os novos nomes.<br>4. Clique em \"Renomear arquivos\".</p><p><b>OBS.:</b> O arquivo na linha \"1\" dos nomes originais será renomeado para o nome na linha \"1\" dos novos nomes, e assim sucessivamente.</p><hr><p>Licença: <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\">Apache 2.0</a><br>Autor: <a href=\"https://www.instagram.com/jedifonseca/\">Jedielson da Fonseca</a><br><a href=\"https://github.com/JediFonseca/mass_renamer\">Github</a></p>"
    }
}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev, PyInstaller, and AppImage. """
    appdir = os.environ.get('APPDIR')
    if appdir:
        base_path = appdir
    else:
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Custom Widgets ---
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

class HoverLabel(QLabel):
    """ A custom QLabel that handles its own hover effects programmatically. """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.is_dark_theme = True
        self.set_default_style()

    def set_theme(self, is_dark):
        self.is_dark_theme = is_dark
        self.set_default_style()

    def set_default_style(self):
        color = "#e8e8e8" if self.is_dark_theme else "#282828"
        self.setStyleSheet(f"background-color: transparent; color: {color}; padding: 3px 20px;")

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #4a90e2; color: #ffffff; padding: 3px 20px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.set_default_style()
        super().leaveEvent(event)

# --- Main Application Window ---
class MassRenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Encapsulated application state
        self.rename_history = []
        self.settings = QSettings("JediFonseca", "MassRenamer")

        self._load_settings()
        self.history_file_path = os.path.join(tempfile.gettempdir(), "mass_renamer.history")
        
        self._init_ui()
        self._load_history_on_startup()
        
        # Apply settings AFTER the UI has been initialized
        self.set_language(self.current_lang)
        self.change_theme(self.current_theme, startup=True)

    # --- Settings Management ---
    def _load_settings(self):
        """ Load language and theme from QSettings, with defaults. """
        self.current_lang = self.settings.value("language", "pt")
        self.current_theme = self.settings.value("theme", "dark")

    def _save_settings(self):
        """ Save current language and theme to QSettings. """
        self.settings.setValue("language", self.current_lang)
        self.settings.setValue("theme", self.current_theme)

    def _center_window(self):
        """ Centers the window on the available screen space. """
        screen_geometry = self.screen().availableGeometry()
        center_point = screen_geometry.center()
        self.move(
            int(center_point.x() - self.width() / 2),
            int(center_point.y() - self.height() / 2)
        )

    # --- UI Initialization ---
    def _init_ui(self):
        """ Initialize the main UI, creating and arranging all widgets. """
        self.setWindowIcon(QIcon(resource_path('appicon.svg')))
        self.resize(900, 650)
        self.setMinimumSize(900, 650)
        self._center_window()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QGridLayout(central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        self._create_top_bar()
        self._create_original_names_panel()
        self._create_new_names_panel()
        self._create_log_panel()
        self._create_bottom_bar()

        self.main_layout.setRowStretch(3, 1)
        self.main_layout.setRowStretch(6, 1)
        self.main_layout.setRowStretch(9, 1)
        
    def _create_top_bar(self):
        self.label_location = QLabel()
        self.main_layout.addWidget(self.label_location, 0, 0, 1, 1)

        settings_layout = QHBoxLayout()
        self.lang_btn = QPushButton()
        self.lang_btn.setObjectName("settingsBtn")
        self.lang_btn.clicked.connect(self.show_lang_menu)
        
        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("settingsBtn")
        self.theme_btn.clicked.connect(self.show_theme_menu)
        
        for btn in [self.lang_btn, self.theme_btn]:
            btn.setFixedWidth(150)
            settings_layout.addWidget(btn)
        
        self.main_layout.addLayout(settings_layout, 0, 1, 1, 3, Qt.AlignmentFlag.AlignRight)

        self.entry_local = QLineEdit()
        self.main_layout.addWidget(self.entry_local, 1, 0, 1, 3)

        self.select_button = QPushButton()
        self.select_button.clicked.connect(self.select_folder)
        self.select_button.setFixedWidth(150)
        self.main_layout.addWidget(self.select_button, 1, 3)

    def _create_original_names_panel(self):
        self.label_orig = QLabel()
        self.main_layout.addWidget(self.label_orig, 2, 0, 1, 4)
        
        self.text_orig = CodeEditor()
        self.main_layout.addWidget(self.text_orig, 3, 0, 1, 4)
        
        ext_frame_o = QWidget()
        ext_layout_o = QHBoxLayout(ext_frame_o)
        ext_layout_o.setContentsMargins(0, 0, 0, 0)
        
        self.ext_label_o = QLabel()
        self.ext_button_o = QPushButton("▼")
        self.ext_button_o.setObjectName("settingsBtn")
        self.ext_button_o.setFixedWidth(75)
        self.ext_button_o.clicked.connect(lambda: self.show_extension_menu(self.ext_button_o, self.text_orig))
        
        self.transfer_ext_button = QPushButton()
        self.transfer_ext_button.clicked.connect(self.transfer_extensions)
        self.transfer_ext_button.setFixedWidth(150)
        
        ext_layout_o.addWidget(self.ext_label_o)
        ext_layout_o.addWidget(self.ext_button_o)
        ext_layout_o.addWidget(self.transfer_ext_button)
        ext_layout_o.addStretch(1)
        self.main_layout.addWidget(ext_frame_o, 4, 0, 1, 2)
        
        self.load_button = QPushButton()
        self.load_button.clicked.connect(self.load_original_names)
        self.load_button.setEnabled(False)
        self.load_button.setFixedWidth(150)
        self.main_layout.addWidget(self.load_button, 4, 2, 1, 2, Qt.AlignmentFlag.AlignRight)

    def _create_new_names_panel(self):
        self.label_new = QLabel()
        self.main_layout.addWidget(self.label_new, 5, 0, 1, 4)
        
        self.text_new = CodeEditor()
        self.main_layout.addWidget(self.text_new, 6, 0, 1, 4)

        ext_frame_n = QWidget()
        ext_layout_n = QHBoxLayout(ext_frame_n)
        ext_layout_n.setContentsMargins(0, 0, 0, 0)
        
        self.ext_label_n = QLabel()
        self.ext_button_n = QPushButton("▼")
        self.ext_button_n.setObjectName("settingsBtn")
        self.ext_button_n.setFixedWidth(75)
        self.ext_button_n.clicked.connect(lambda: self.show_extension_menu(self.ext_button_n, self.text_new))
        
        self.remove_ext_button = QPushButton()
        self.remove_ext_button.clicked.connect(self.remove_extension)
        self.remove_ext_button.setFixedWidth(150)
        
        ext_layout_n.addWidget(self.ext_label_n)
        ext_layout_n.addWidget(self.ext_button_n)
        ext_layout_n.addWidget(self.remove_ext_button)
        ext_layout_n.addStretch(1)
        self.main_layout.addWidget(ext_frame_n, 7, 0, 1, 2)

    def _create_log_panel(self):
        self.label_log = QLabel()
        self.main_layout.addWidget(self.label_log, 8, 0, 1, 4)
        
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        self.main_layout.addWidget(self.log_text, 9, 0, 1, 4)
        
    def _create_bottom_bar(self):
        buttons_frame = QWidget()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        
        self.help_label = QLabel()
        self.help_label.setObjectName("HelpLabel")
        self.help_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.help_label.mousePressEvent = self.show_help
        
        self.rename_button = QPushButton()
        self.rename_button.clicked.connect(self.rename)
        
        self.undo_button = QPushButton()
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self.undo)
        
        for btn in [self.rename_button, self.undo_button]:
            btn.setFixedWidth(150)

        buttons_layout.addWidget(self.help_label, 0, Qt.AlignmentFlag.AlignLeft)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.rename_button)
        buttons_layout.addWidget(self.undo_button)
        self.main_layout.addWidget(buttons_frame, 10, 0, 1, 4)

    # --- History Management ---
    def _load_history_on_startup(self):
        """ Load rename history from the temp file on startup, if it exists. """
        if os.path.exists(self.history_file_path):
            try:
                with open(self.history_file_path, "r", encoding="utf-8") as f:
                    self.rename_history = json.load(f)
                if self.rename_history:
                    self.undo_button.setEnabled(True)
            except (json.JSONDecodeError, IOError):
                self.rename_history = []
                try: os.remove(self.history_file_path)
                except OSError: pass

    # --- Core Logic ---
    def rename(self):
        self.rename_history.clear()
        validated_data = self._get_and_validate_inputs()
        if not validated_data: return
        folder, origs, news = validated_data
        news = self._handle_name_conflicts(news, folder)
        if news is None: return
        self._execute_rename(folder, origs, news)

    def _get_and_validate_inputs(self):
        folder = self.entry_local.text().strip()
        if not folder or not os.path.isdir(folder):
            QMessageBox.critical(self, self.tr("error"), self.tr("select_valid_folder"))
            return None
        origs = [l.strip() for l in self.text_orig.toPlainText().splitlines() if l.strip()]
        news = [l.strip() for l in self.text_new.toPlainText().splitlines() if l.strip()]
        if len(origs) != len(news):
            QMessageBox.critical(self, self.tr("map_error"), self.tr("map_error_msg").format(len(origs), len(news)))
            return None
        if any(ch in ILLEGAL_CHARS for name in news for ch in name):
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(self.tr("invalid_chars"))
            msg_box.setText(self.tr("invalid_chars_msg"))
            yes_btn = msg_box.addButton(self.tr("yes"), QMessageBox.ButtonRole.YesRole)
            msg_box.addButton(self.tr("no"), QMessageBox.ButtonRole.NoRole)
            msg_box.exec()
            if msg_box.clickedButton() == yes_btn:
                news = [''.join(c for c in n if c not in ILLEGAL_CHARS) for n in news]
                self.text_new.setPlainText("\n".join(news))
            else: return None
        return folder, origs, news

    def _handle_name_conflicts(self, news, folder):
        conflicts = [{'name': name, 'index': i, 'line': i + 1} for i, name in enumerate(news) if os.path.exists(os.path.join(folder, name))]
        if not conflicts: return news
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("conflict_title"))
        msg_box.setText(self.tr("conflict_text").format(len(conflicts)))
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setInformativeText(self.tr("conflict_info"))
        rename_btn = msg_box.addButton(self.tr("conflict_btn_rename"), QMessageBox.ButtonRole.YesRole)
        list_btn = msg_box.addButton(self.tr("conflict_btn_list"), QMessageBox.ButtonRole.NoRole)
        cancel_btn = msg_box.addButton(self.tr("conflict_btn_cancel"), QMessageBox.ButtonRole.RejectRole)
        buttons = [rename_btn, list_btn, cancel_btn]
        max_width = max(b.sizeHint().width() for b in buttons)
        for b in buttons: b.setFixedWidth(max_width + 10)
        msg_box.exec()
        clicked = msg_box.clickedButton()
        if clicked == list_btn:
            line_numbers = ", ".join(str(c['line']) for c in conflicts)
            self.log_text.setPlainText(f"Operação cancelada. Os nomes nas linhas a seguir já estão presentes na pasta selecionada: {line_numbers}.")
            return None
        elif clicked == cancel_btn: return None
        elif clicked == rename_btn:
            for c in conflicts:
                base, ext = os.path.splitext(c['name'])
                count = 1
                while True:
                    new_name = f"{base}_({count}){ext}"
                    if not os.path.exists(os.path.join(folder, new_name)):
                        news[c['index']] = new_name
                        break
                    count += 1
            self.text_new.setPlainText("\n".join(news))
            return news
        return None

    def _execute_rename(self, folder, origs, news):
        self.log_text.clear()
        try: os.remove(self.history_file_path)
        except OSError: pass
        temp_history = []
        for o, n in zip(origs, news):
            src, dst = os.path.join(folder, o), os.path.join(folder, n)
            if not os.path.isfile(src):
                self.log_text.appendPlainText(f"❌ {self.tr('not_found')} {o}")
                continue
            try:
                shutil.move(src, dst)
                temp_history.append((dst, src))
                with open(self.history_file_path, "w", encoding="utf-8") as f:
                    json.dump(temp_history, f)
                self.log_text.appendPlainText(f"✅ {o} → {n}")
            except Exception as e:
                self.log_text.appendPlainText(f"⚠️ {self.tr('error_renaming')} {o}: {e}")
        self.rename_history.extend(temp_history)
        if self.rename_history: self.undo_button.setEnabled(True)
        self.log_text.appendPlainText(f"\n{self.tr('done')}")

    def undo(self):
        if not self.rename_history: return
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("undo"))
        msg_box.setText(self.tr("undo_confirm"))
        yes_btn = msg_box.addButton(self.tr("yes"), QMessageBox.ButtonRole.YesRole)
        msg_box.addButton(self.tr("no"), QMessageBox.ButtonRole.NoRole)
        msg_box.exec()
        if msg_box.clickedButton() != yes_btn: return
        self.log_text.appendPlainText(f"\n{self.tr('undoing')}\n")
        for dst, src in reversed(self.rename_history):
            try:
                shutil.move(dst, src)
                self.log_text.appendPlainText(f"↩️ {os.path.basename(dst)} → {os.path.basename(src)}")
            except Exception as e:
                self.log_text.appendPlainText(f"⚠️ {self.tr('error_undoing')} {dst}: {e}")
        self.log_text.appendPlainText(f"\n{self.tr('undo_done')}")
        self.rename_history.clear()
        self.undo_button.setEnabled(False)
        try: os.remove(self.history_file_path)
        except OSError: pass

    # --- UI Callbacks and Event Handlers ---
    def tr(self, key):
        """ Translate a text key using the current language dictionary. """
        return LANG_TEXTS[self.current_lang].get(key, key)

    def set_language(self, lang_code):
        self.current_lang = lang_code
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
        self.transfer_ext_button.setText(self.tr("transfer_extensions"))
        self.remove_ext_button.setText(self.tr("remove_extension"))
        lang_text = "Português" if lang_code == 'pt' else "English"
        self.lang_btn.setText(lang_text)
        self.theme_btn.setText(self.tr(self.current_theme))
        self._save_settings()

    def change_theme(self, theme_key, startup=False):
        self.current_theme = theme_key
        stylesheet = DARK_STYLESHEET if theme_key == "dark" else LIGHT_STYLESHEET
        QApplication.instance().setStyleSheet(stylesheet)
        self.theme_btn.setText(self.tr(self.current_theme))
        if not startup: self._save_settings()

    def _create_centered_action(self, text, menu):
        """Creates a QWidgetAction with a centered, hoverable QLabel."""
        action = QWidgetAction(menu)
        label = HoverLabel(text)
        label.set_theme(self.current_theme == "dark")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        action.setDefaultWidget(label)
        return action

    def show_lang_menu(self):
        menu = QMenu(self)
        menu.setObjectName("settingsMenu")
        menu.setFixedWidth(self.lang_btn.width())
        en_action = self._create_centered_action("English", menu)
        en_action.triggered.connect(lambda: self.set_language("en"))
        menu.addAction(en_action)
        pt_action = self._create_centered_action("Português", menu)
        pt_action.triggered.connect(lambda: self.set_language("pt"))
        menu.addAction(pt_action)
        menu.exec(self.lang_btn.mapToGlobal(self.lang_btn.rect().bottomLeft()))
        
    def show_theme_menu(self):
        menu = QMenu(self)
        menu.setObjectName("settingsMenu")
        menu.setFixedWidth(self.theme_btn.width())
        light_action = self._create_centered_action(self.tr("light"), menu)
        light_action.triggered.connect(lambda: self.change_theme("light"))
        menu.addAction(light_action)
        dark_action = self._create_centered_action(self.tr("dark"), menu)
        dark_action.triggered.connect(lambda: self.change_theme("dark"))
        menu.addAction(dark_action)
        menu.exec(self.theme_btn.mapToGlobal(self.theme_btn.rect().bottomLeft()))

    def show_help(self, event):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("help"))
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(self.tr("help_text"))
        msg_box.exec()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("select_folder"))
        if folder:
            self.entry_local.setText(folder)
            self.load_button.setEnabled(True)

    def load_original_names(self):
        folder = self.entry_local.text().strip()
        if not folder or not os.path.isdir(folder):
            QMessageBox.critical(self, self.tr("error"), self.tr("select_valid_folder"))
            return
        try:
            items = os.listdir(folder)
            files = sorted(f for f in items if os.path.isfile(os.path.join(folder, f)))
        except (OSError, PermissionError) as e:
            QMessageBox.critical(self, self.tr("error"), f"{self.tr('cannot_list')}\\n{e}")
            return
        self.text_orig.setPlainText("\n".join(files))
        
    def show_extension_menu(self, button, text_widget):
        menu = QMenu(self)
        menu.setObjectName("extensionsMenu")
        for ext in POPULAR_EXTS:
            action = menu.addAction(ext)
            action.triggered.connect(lambda checked, extension=ext: self.add_extension_to_widget(text_widget, extension))
        button_pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(button_pos)
        
    def add_extension_to_widget(self, text_widget, ext):
        lines = [l.rstrip() for l in text_widget.toPlainText().splitlines()]
        new_lines = [f"{l}{ext}" if l else "" for l in lines]
        text_widget.setPlainText("\n".join(new_lines))

    def transfer_extensions(self):
        orig_lines = self.text_orig.toPlainText().splitlines()
        new_lines = self.text_new.toPlainText().splitlines()
        num_lines_to_process = min(len(orig_lines), len(new_lines))
        result_lines = list(new_lines)
        for i in range(num_lines_to_process):
            if not result_lines[i].strip(): continue
            _ , orig_ext = os.path.splitext(orig_lines[i])
            if orig_ext:
                new_base, _ = os.path.splitext(result_lines[i])
                result_lines[i] = new_base + orig_ext
        self.text_new.setPlainText("\n".join(result_lines))

    def remove_extension(self):
        lines = self.text_new.toPlainText().splitlines()
        new_lines = [os.path.splitext(line)[0] for line in lines]
        self.text_new.setPlainText("\n".join(new_lines))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MassRenamerApp()
    window.show()
    sys.exit(app.exec())
