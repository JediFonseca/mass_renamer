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
from collections import Counter
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit,
    QPushButton, QPlainTextEdit, QFileDialog, QMessageBox,
    QHBoxLayout, QMenu, QWidgetAction, QDialog, QVBoxLayout,
    QTabWidget, QCheckBox, QDialogButtonBox
)
from PyQt6.QtGui import QIcon, QPainter, QCursor, QFont
from PyQt6.QtCore import Qt, QRect, QSize, QSettings

# --- Character sets for different OS ---
# Based on common restrictions. Note that filesystems (like FAT32) can add more.
ILLEGAL_CHARS_LINUX = set('/')
ILLEGAL_CHARS_WINDOWS = set('/\\:*?"<>|')
ILLEGAL_CHARS_MACOS = set('/:')
ILLEGAL_CHARS_IOS = set('/:') # Similar to macOS
# Android often uses Windows-like filesystems (FAT32, exFAT) for external storage (SD cards),
# so it's safest to block the same characters as Windows for broad compatibility.
ILLEGAL_CHARS_ANDROID = set('/\\:*?"<>|')

# --- Stylesheets ---

# Helper function to create menu item styles
def create_menu_item_style(text_color, hover_bg_color, hover_text_color):
    return f"""
        QLabel#menuItemLabel {{
            color: {text_color};
            background-color: transparent;
            padding: 3px 20px;
        }}
        QLabel#menuItemLabel:hover {{
            color: {hover_text_color};
            background-color: {hover_bg_color};
        }}
    """

DARK_STYLESHEET = """
    QDialog, QWidget {
        /* Default background color and text color for windows and widgets */
        background-color: #282828; color: #e8e8e8; font-family: 'Segoe UI'; font-size: 10pt;
    }

    QMainWindow, QTabWidget::pane { 
        /* Background color for the main window and tab pane */
        background-color: #282828; 
    }

    QPlainTextEdit, QLineEdit {
        /* Background color and border color for text boxes */
        background-color: #3c3c3c; border: 1px solid #555; border-radius: 5px;
        padding: 5px; font-family: 'Consolas'; font-size: 11pt;
    }

    QPushButton {
        /* Background color and text color for main buttons */
        padding: 7px 16px; font-size: 10pt; background-color: #3e82d8;
        color: white; border: none; border-radius: 5px;
    }

    QPushButton#settingsBtn {
        /* Background color, text, and border for secondary buttons */
        padding: 6px 16px; font-size: 10pt; background-color: #3c3c3c;
        color: white; border: 1px solid #555; border-radius: 5px;
    }

    QMenu {
        /* Background color and border color for dropdown menus */
        background-color: #3c3c3c; border: 1px solid #555;
    }

    QPushButton:hover { 
        /* Background color for buttons on hover */
        background-color: #4a90e2; 
    }

    QPushButton:disabled { 
        /* Background color and text color for disabled buttons */
        background-color: #555; color: #999; 
    }

    QMenu#extensionsMenu::item:selected { 
        /* Background color and text color for selected menu items */
        background-color: #4a90e2; color: #ffffff; 
    }

    QLabel#settingsLabel { 
        /* Text color for the "Settings" link */
        color: #3e82d8; font-weight: bold; 
    }
    QLabel#progressLabel { 
        /* Style for the progress percentage label in the log area */
        background-color: transparent; padding: 0 24px 5px 0; 
    }

    QTabBar::tab { 
        /* Background color and border for tabs */
        background: #282828; padding: 8px 15px; border: 1px solid #555; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }

    QTabBar::tab:selected { 
        /* Background color for the selected tab */
        background: #3c3c3c; 
    }

    QTabBar::tab:!selected { 
        /* Background color and text for non-selected tabs */
        background: #282828; color: #999; 
    }

    QTabWidget::pane { 
        /* Border color for the tab pane */
        border: 1px solid #555; border-radius: 5px; 
    }

    QCheckBox::indicator { 
        /* Border color and background for the checkbox (unchecked) */
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #555; background-color: #3c3c3c; 
    }

    QCheckBox::indicator:checked { 
        /* Background color for the checkbox (checked) */
        background-color: #3e82d8; 
    }
    
    CodeEditor > QWidget {
        /* Background color and text for the line number area */
        background-color: #282828;
        color: #e8e8e8;
    }
""" + create_menu_item_style(
    text_color="#e8e8e8",             # Menu item text color
    hover_bg_color="#4a90e2",        # Menu item background color on hover
    hover_text_color="#ffffff"       # Menu item text color on hover
)

LIGHT_STYLESHEET = """
    QDialog, QWidget {
        /* Default background color and text color for windows and widgets */
        background-color: #e8e8e8; color: #282828; font-family: 'Segoe UI'; font-size: 10pt;
    }

    QMainWindow, QTabWidget::pane { 
        /* Background color for the main window and tab pane */
        background-color: #e8e8e8; 
    }

    QPlainTextEdit, QLineEdit {
        /* Background color and border color for text boxes */
        background-color: #ffffff; border: 1px solid #ccc; border-radius: 5px;
        padding: 5px; font-family: 'Consolas'; font-size: 11pt;
    }

    QPushButton {
        /* Background color and text color for main buttons */
        padding: 7px 16px; font-size: 10pt; background-color: #3e82d8;
        color: white; border: none; border-radius: 5px;
    }

    QPushButton#settingsBtn {
        /* Background color, text, and border for secondary buttons */
        padding: 6px 16px; font-size: 10pt; background-color: #ffffff;
        color: #282828; border: 1px solid #ccc; border-radius: 5px;
    }

    QMenu {
        /* Background color and border color for dropdown menus */
        background-color: #ffffff; border: 1px solid #ccc;
    }

    QPushButton:hover { 
        /* Background color for buttons on hover */
        background-color: #4a90e2; 
    }

    QPushButton:disabled { 
        /* Background color and text color for disabled buttons */
        background-color: #ccc; color: #777; 
    }

    QMenu#extensionsMenu::item:selected { 
        /* Background color and text color for selected menu items */
        background-color: #4a90e2; color: #ffffff; 
    }

    QLabel#settingsLabel { 
        /* Text color for the "Settings" link */
        color: #3e82d8; font-weight: bold; 
    }
    
    QLabel#progressLabel { 
        /* Style for the progress percentage label in the log area */
        background-color: transparent; padding: 0 24px 5px 0; 
    }

    QTabBar::tab { 
        /* Background color and border for tabs */
        background: #e8e8e8; padding: 8px 15px; border: 1px solid #ccc; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }

    QTabBar::tab:selected { 
        /* Background color for the selected tab */
        background: #ffffff; 
    }

    QTabBar::tab:!selected { 
        /* Background color and text for non-selected tabs */
        background: #e8e8e8; color: #777; 
    }

    QTabWidget::pane { 
        /* Border color for the tab pane */
        border: 1px solid #ccc; border-radius: 5px; 
    }

    QCheckBox::indicator { 
        /* Border color and background for the checkbox (unchecked) */
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #ccc; background-color: #ffffff; 
    }

    QCheckBox::indicator:checked { 
        /* Background color for the checkbox (checked) */
        background-color: #3e82d8; 
    }
    
    CodeEditor > QWidget {
        /* Background color and text for the line number area */
        background-color: #e8e8e8;
        color: #282828;
    }
""" + create_menu_item_style(
    text_color="#282828",             # Menu item text color
    hover_bg_color="#4a90e2",        # Menu item background color on hover
    hover_text_color="#ffffff"       # Menu item text color on hover
)

MINT_Y_DARK_AQUA_STYLESHEET = """
    QDialog, QWidget { 
        /* Default background color and text color */
        background-color: #222226; color: #E4E4E4; font-family: 'Segoe UI'; font-size: 10pt; 
    }

    QMainWindow { 
        /* Background color of the main window */
        background-color: #222226; 
    }

    QPlainTextEdit, QLineEdit { 
        /* Background color and border for text boxes */
        background-color: #2E2E33; border: 1px solid #45454C; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }

    QPushButton { 
        /* Background color and text for main buttons */
        padding: 7px 16px; font-size: 10pt; background-color: #1F9EDE; color: white; border: none; border-radius: 5px; 
    }

    QPushButton#settingsBtn { 
        /* Background color, text, and border for secondary buttons */
        padding: 6px 16px; font-size: 10pt; background-color: #2E2E33; color: #E4E4E4; border: 1px solid #45454C; border-radius: 5px; 
    }

    QMenu { 
        /* Background color and border for dropdown menus */
        background-color: #2E2E33; border: 1px solid #45454C; 
    }

    QPushButton:hover { 
        /* Background color for buttons on hover */
        background-color: #57B7E7; 
    }

    QPushButton:disabled { 
        /* Background color and text for disabled buttons */
        background-color: #2E2E33; color: #8A8A8A; 
    }

    QMenu#extensionsMenu::item:selected { 
        /* Background color and text for selected menu items */
        background-color: #1F9EDE; color: #E4E4E4; 
    }

    QLabel#settingsLabel { 
        /* Text color for the "Settings" link */
        color: #1F9EDE; font-weight: bold; 
    }
    
    QLabel#progressLabel { 
        /* Style for the progress percentage label in the log area */
        background-color: transparent; padding: 0 24px 5px 0; 
    }

    QTabBar::tab { 
        /* Background color and border for tabs */
        background: #222226; padding: 8px 15px; border: 1px solid #45454C; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }

    QTabBar::tab:selected { 
        /* Background color for the selected tab */
        background: #2E2E33; 
    }

    QTabBar::tab:!selected { 
        /* Background color and text for non-selected tabs */
        background: #222226; color: #8A8A8A; 
    }

    QTabWidget::pane { 
        /* Border color for the tab pane */
        border: 1px solid #45454C; border-radius: 5px; 
    }

    QCheckBox::indicator { 
        /* Border color and background for the checkbox (unchecked) */
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #45454C; background-color: #2E2E33; 
    }

    QCheckBox::indicator:checked { 
        /* Background color for the checkbox (checked) */
        background-color: #1F9EDE; 
    }

    CodeEditor > QWidget { 
        /* Background color and text for the line number area */
        background-color: #222226; color: #E4E4E4; 
    }
""" + create_menu_item_style(
    text_color="#FFFFFF",             # Menu item text color
    hover_bg_color="#1F9EDE",        # Menu item background color on hover
    hover_text_color="#FFFFFF"       # Menu item text color on hover
)

MINT_Y_AQUA_STYLESHEET = """
    QDialog, QWidget { 
        /* Default background color and text color */
        background-color: #EBEBED; color: #202020; font-family: 'Segoe UI'; font-size: 10pt; 
    }

    QMainWindow { 
        /* Background color of the main window */
        background-color: #EBEBED; 
    }

    QPlainTextEdit, QLineEdit { 
        /* Background color and border for text boxes */
        background-color: #FFFFFF; border: 1px solid #C0C0C6; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }

    QPushButton { 
        /* Background color and text for main buttons */
        padding: 7px 16px; font-size: 10pt; background-color: #1F9EDE; color: white; border: none; border-radius: 5px; 
    }

    QPushButton#settingsBtn { 
        /* Background color, text, and border for secondary buttons */
        padding: 6px 16px; font-size: 10pt; background-color: #FFFFFF; color: #202020; border: 1px solid #C0C0C6; border-radius: 5px; 
    }

    QMenu { 
        /* Background color and border for dropdown menus */
        background-color: #FFFFFF; border: 1px solid #C0C0C6; 
    }

    QPushButton:hover { 
        /* Background color for buttons on hover */
        background-color: #57B7E7; 
    }

    QPushButton:disabled { 
        /* Background color and text for disabled buttons */
        background-color: #FFFFFF; color: #8A8A8A; 
    }

    QMenu#extensionsMenu::item:selected { 
        /* Background color and text for selected menu items */
        background-color: #1F9EDE; color: #FFFFFF; 
    }

    QLabel#settingsLabel { 
        /* Text color for the "Settings" link */
        color: #1F9EDE; font-weight: bold; 
    }
    
    QLabel#progressLabel { 
        /* Style for the progress percentage label in the log area */
        background-color: transparent; padding: 0 24px 5px 0; 
    }

    QTabBar::tab { 
        /* Background color and border for tabs */
        background: #EBEBED; padding: 8px 15px; border: 1px solid #C0C0C6; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }

    QTabBar::tab:selected { 
        /* Background color for the selected tab */
        background: #FFFFFF; 
    }

    QTabBar::tab:!selected { 
        /* Background color and text for non-selected tabs */
        background: #EBEBED; color: #8A8A8A; 
    }

    QTabWidget::pane { 
        /* Border color for the tab pane */
        border: 1px solid #C0C0C6; border-radius: 5px; 
    }

    QCheckBox::indicator { 
        /* Border color and background for the checkbox (unchecked) */
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #C0C0C6; background-color: #FFFFFF; 
    }

    QCheckBox::indicator:checked { 
        /* Background color for the checkbox (checked) */
        background-color: #1F9EDE; 
    }

    CodeEditor > QWidget { 
        /* Background color and text for the line number area */
        background-color: #EBEBED; color: #202020; 
    }
""" + create_menu_item_style(
    text_color="#000000",             # Menu item text color
    hover_bg_color="#1F9EDE",        # Menu item background color on hover
    hover_text_color="#FFFFFF"       # Menu item text color on hover
)

UBUNTU_STYLESHEET = """
    QDialog, QWidget { 
        /* Default background color and text color */
        background-color: #FFFFFF; color: #000000; font-family: 'Segoe UI'; font-size: 10pt; 
    }

    QMainWindow { 
        /* Background color of the main window */
        background-color: #FFFFFF; 
    }

    QPlainTextEdit, QLineEdit { 
        /* Background color and border for text boxes */
        background-color: #ECECEC; border: 1px solid #B2B2B2; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }

    QPushButton { 
        /* Background color and text for main buttons */
        padding: 7px 16px; font-size: 10pt; background-color: #D34615; color: white; border: none; border-radius: 5px; 
    }

    QPushButton#settingsBtn { 
        /* Background color, text, and border for secondary buttons */
        padding: 6px 16px; font-size: 10pt; background-color: #ECECEC; color: #000000; border: 1px solid #B2B2B2; border-radius: 5px; 
    }

    QMenu { 
        /* Background color and border for dropdown menus */
        background-color: #ECECEC; border: 1px solid #B2B2B2; 
    }

    QPushButton:hover { 
        /* Background color for buttons on hover */
        background-color: #E95420; 
    }

    QPushButton:disabled { 
        /* Background color and text for disabled buttons */
        background-color: #E3E3E3; color: #919191; 
    }

    QMenu#extensionsMenu::item:selected { 
        /* Background color and text for selected menu items */
        background-color: #D34615; color: #FFFFFF; 
    }

    QLabel#settingsLabel { 
        /* Text color for the "Settings" link */
        color: #D34615; font-weight: bold; 
    }
    
    QLabel#progressLabel { 
        /* Style for the progress percentage label in the log area */
        background-color: transparent; padding: 0 24px 5px 0; 
    }

    QTabBar::tab { 
        /* Background color and border for tabs */
        background: #FFFFFF; padding: 8px 15px; border: 1px solid #B2B2B2; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }

    QTabBar::tab:selected { 
        /* Background color for the selected tab */
        background: #ECECEC; 
    }

    QTabBar::tab:!selected { 
        /* Background color and text for non-selected tabs */
        background: #FFFFFF; color: #919191; 
    }

    QTabWidget::pane { 
        /* Border color for the tab pane */
        border: 1px solid #B2B2B2; border-radius: 5px; 
    }

    QCheckBox::indicator { 
        /* Border color and background for the checkbox (unchecked) */
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #B2B2B2; background-color: #ECECEC; 
    }

    QCheckBox::indicator:checked { 
        /* Background color for the checkbox (checked) */
        background-color: #D34615; 
    }

    CodeEditor > QWidget { 
        /* Background color and text for the line number area */
        background-color: #FFFFFF; color: #000000; 
    }
""" + create_menu_item_style(
    text_color="#000000",             # Menu item text color
    hover_bg_color="#D34615",        # Menu item background color on hover
    hover_text_color="#FFFFFF"       # Menu item text color on hover
)

UBUNTU_DARK_STYLESHEET = """
    QDialog, QWidget { 
        /* Default background color and text color */
        background-color: #303030; color: #FFFFFF; font-family: 'Segoe UI'; font-size: 10pt; 
    }

    QMainWindow { 
        /* Background color of the main window */
        background-color: #303030; 
    }

    QPlainTextEdit, QLineEdit { 
        /* Background color and border for text boxes */
        background-color: #3D3D3D; border: 1px solid #454545; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }

    QPushButton { 
        /* Background color and text for main buttons */
        padding: 7px 16px; font-size: 10pt; background-color: #E95420; color: white; border: none; border-radius: 5px; 
    }

    QPushButton#settingsBtn { 
        /* Background color, text, and border for secondary buttons */
        padding: 6px 16px; font-size: 10pt; background-color: #3D3D3D; color: #FFFFFF; border: 1px solid #303030; border-radius: 5px; 
    }

    QMenu { 
        /* Background color and border for dropdown menus */
        background-color: #3D3D3D; border: 1px solid #303030; 
    }

    QPushButton:hover { 
        /* Background color for buttons on hover */
        background-color: #D34615; 
    }

    QPushButton:disabled { 
        /* Background color and text for disabled buttons */
        background-color: #3D3D3D; color: #8A8A8A; 
    }

    QMenu#extensionsMenu::item:selected { 
        /* Background color and text for selected menu items */
        background-color: #E95420; color: #FFFFFF; 
    }

    QLabel#settingsLabel { 
        /* Text color for the "Settings" link */
        color: #E95420; font-weight: bold; 
    }
    
    QLabel#progressLabel { 
        /* Style for the progress percentage label in the log area */
        background-color: transparent; padding: 0 24px 5px 0; 
    }

    QTabBar::tab { 
        /* Background color and border for tabs */
        background: #303030; padding: 8px 15px; border: 1px solid #454545; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }

    QTabBar::tab:selected { 
        /* Background color for the selected tab */
        background: #3D3D3D; 
    }

    QTabBar::tab:!selected { 
        /* Background color and text for non-selected tabs */
        background: #303030; color: #8A8A8A; 
    }

    QTabWidget::pane { 
        /* Border color for the tab pane */
        border: 1px solid #454545; border-radius: 5px; 
    }

    QCheckBox::indicator { 
        /* Border color and background for the checkbox (unchecked) */
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #454545; background-color: #3D3D3D; 
    }

    QCheckBox::indicator:checked { 
        /* Background color for the checkbox (checked) */
        background-color: #E95420; 
    }

    CodeEditor > QWidget { 
        /* Background color and text for the line number area */
        background-color: #303030; color: #FFFFFF; 
    }
""" + create_menu_item_style(
    text_color="#FFFFFF",             # Menu item text color
    hover_bg_color="#E95420",        # Menu item background color on hover
    hover_text_color="#FFFFFF"       # Menu item text color on hover
)

ADWAITA_STYLESHEET = """
    QDialog, QWidget { 
        background-color: #fafafa; color: #202020; font-family: 'Segoe UI'; font-size: 10pt; 
    }
    QMainWindow { 
        background-color: #fafafa; 
    }
    QPlainTextEdit, QLineEdit { 
        background-color: #FFFFFF; border: 1px solid #C0C0C6; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }
    QPushButton { 
        padding: 7px 16px; font-size: 10pt; background-color: #3584e4; color: white; border: none; border-radius: 5px; 
    }
    QPushButton#settingsBtn { 
        padding: 6px 16px; font-size: 10pt; background-color: #e3e3e3; color: #202020; border: 1px solid #C0C0C6; border-radius: 5px; 
    }
    QMenu { 
        background-color: #FFFFFF; border: 1px solid #C0C0C6; 
    }
    QPushButton:hover { 
        background-color: #4a90e2; 
    }
    QPushButton:disabled { 
        background-color: #e3e3e3; color: #8A8A8A; 
    }
    QMenu#extensionsMenu::item:selected { 
        background-color: #3584e4; color: #FFFFFF; 
    }
    QLabel#settingsLabel { 
        color: #3584e4; font-weight: bold; 
    }
    QLabel#progressLabel { 
        background-color: transparent; padding: 0 24px 5px 0; 
    }
    QTabBar::tab { 
        background: #fafafa; padding: 8px 15px; border: 1px solid #C0C0C6; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }
    QTabBar::tab:selected { 
        background: #FFFFFF; 
    }
    QTabBar::tab:!selected { 
        background: #fafafa; color: #8A8A8A; 
    }
    QTabWidget::pane { 
        border: 1px solid #C0C0C6; border-radius: 5px; 
    }
    QCheckBox::indicator { 
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #C0C0C6; background-color: #FFFFFF; 
    }
    QCheckBox::indicator:checked { 
        background-color: #3584e4; 
    }
    CodeEditor > QWidget { 
        background-color: #fafafa; color: #202020; 
    }
""" + create_menu_item_style(
    text_color="#000000",
    hover_bg_color="#3584e4",
    hover_text_color="#FFFFFF"
)

ADWAITA_DARK_STYLESHEET = """
    QDialog, QWidget { 
        background-color: #242424; color: #eeeeee; font-family: 'Segoe UI'; font-size: 10pt; 
    }
    QMainWindow { 
        background-color: #242424; 
    }
    QPlainTextEdit, QLineEdit { 
        background-color: #1e1e1e; border: 1px solid #404040; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }
    QPushButton { 
        padding: 7px 16px; font-size: 10pt; background-color: #3584e4; color: white; border: none; border-radius: 5px; 
    }
    QPushButton#settingsBtn { 
        padding: 6px 16px; font-size: 10pt; background-color: #3c3c3c; color: #eeeeee; border: 1px solid #404040; border-radius: 5px; 
    }
    QMenu { 
        background-color: #1e1e1e; border: 1px solid #404040; 
    }
    QPushButton:hover { 
        background-color: #4a90e2; 
    }
    QPushButton:disabled { 
        background-color: #3c3c3c; color: #8A8A8A; 
    }
    QMenu#extensionsMenu::item:selected { 
        background-color: #3584e4; color: #eeeeee; 
    }
    QLabel#settingsLabel { 
        color: #3584e4; font-weight: bold; 
    }
    QLabel#progressLabel { 
        background-color: transparent; padding: 0 24px 5px 0; 
    }
    QTabBar::tab { 
        background: #242424; padding: 8px 15px; border: 1px solid #404040; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }
    QTabBar::tab:selected { 
        background: #1e1e1e; 
    }
    QTabBar::tab:!selected { 
        background: #242424; color: #8A8A8A; 
    }
    QTabWidget::pane { 
        border: 1px solid #404040; border-radius: 5px; 
    }
    QCheckBox::indicator { 
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #404040; background-color: #1e1e1e; 
    }
    QCheckBox::indicator:checked { 
        background-color: #3584e4; 
    }
    CodeEditor > QWidget { 
        background-color: #242424; color: #eeeeee; 
    }
""" + create_menu_item_style(
    text_color="#FFFFFF",
    hover_bg_color="#3584e4",
    hover_text_color="#FFFFFF"
)

BREEZE_STYLESHEET = """
    QDialog, QWidget { 
        background-color: #eff0f1; color: #232629; font-family: 'Segoe UI'; font-size: 10pt; 
    }
    QMainWindow { 
        background-color: #eff0f1; 
    }
    QPlainTextEdit, QLineEdit { 
        background-color: #fcfcfc; border: 1px solid #c8c8c8; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }
    QPushButton { 
        padding: 7px 16px; font-size: 10pt; background-color: #3daee9; color: white; border: none; border-radius: 5px; 
    }
    QPushButton#settingsBtn { 
        padding: 6px 16px; font-size: 10pt; background-color: #f6f7f8; color: #232629; border: 1px solid #c8c8c8; border-radius: 5px; 
    }
    QMenu { 
        background-color: #fcfcfc; border: 1px solid #c8c8c8; 
    }
    QPushButton:hover { 
        background-color: #57B7E7; 
    }
    QPushButton:disabled { 
        background-color: #f6f7f8; color: #808080; 
    }
    QMenu#extensionsMenu::item:selected { 
        background-color: #3daee9; color: #FFFFFF; 
    }
    QLabel#settingsLabel { 
        color: #3daee9; font-weight: bold; 
    }
    QLabel#progressLabel { 
        background-color: transparent; padding: 0 24px 5px 0; 
    }
    QTabBar::tab { 
        background: #eff0f1; padding: 8px 15px; border: 1px solid #c8c8c8; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }
    QTabBar::tab:selected { 
        background: #fcfcfc; 
    }
    QTabBar::tab:!selected { 
        background: #eff0f1; color: #808080; 
    }
    QTabWidget::pane { 
        border: 1px solid #c8c8c8; border-radius: 5px; 
    }
    QCheckBox::indicator { 
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #c8c8c8; background-color: #fcfcfc; 
    }
    QCheckBox::indicator:checked { 
        background-color: #3daee9; 
    }
    CodeEditor > QWidget { 
        background-color: #eff0f1; color: #232629; 
    }
""" + create_menu_item_style(
    text_color="#000000",
    hover_bg_color="#3daee9",
    hover_text_color="#FFFFFF"
)

BREEZE_DARK_STYLESHEET = """
    QDialog, QWidget { 
        background-color: #2a2e32; color: #eff0f1; font-family: 'Segoe UI'; font-size: 10pt; 
    }
    QMainWindow { 
        background-color: #2a2e32; 
    }
    QPlainTextEdit, QLineEdit { 
        background-color: #222528; border: 1px solid #404448; border-radius: 5px; padding: 5px; font-family: 'Consolas'; font-size: 11pt; 
    }
    QPushButton { 
        padding: 7px 16px; font-size: 10pt; background-color: #3daee9; color: white; border: none; border-radius: 5px; 
    }
    QPushButton#settingsBtn { 
        padding: 6px 16px; font-size: 10pt; background-color: #31363b; color: #eff0f1; border: 1px solid #404448; border-radius: 5px; 
    }
    QMenu { 
        background-color: #222528; border: 1px solid #404448; 
    }
    QPushButton:hover { 
        background-color: #57B7E7; 
    }
    QPushButton:disabled { 
        background-color: #31363b; color: #808080; 
    }
    QMenu#extensionsMenu::item:selected { 
        background-color: #3daee9; color: #eff0f1; 
    }
    QLabel#settingsLabel { 
        color: #3daee9; font-weight: bold; 
    }
    QLabel#progressLabel { 
        background-color: transparent; padding: 0 24px 5px 0; 
    }
    QTabBar::tab { 
        background: #2a2e32; padding: 8px 15px; border: 1px solid #404448; border-bottom: none; border-top-left-radius: 5px; border-top-right-radius: 5px; 
    }
    QTabBar::tab:selected { 
        background: #222528; 
    }
    QTabBar::tab:!selected { 
        background: #2a2e32; color: #808080; 
    }
    QTabWidget::pane { 
        border: 1px solid #404448; border-radius: 5px; 
    }
    QCheckBox::indicator { 
        width: 15px; height: 15px; border-radius: 4px; border: 1px solid #404448; background-color: #222528; 
    }
    QCheckBox::indicator:checked { 
        background-color: #3daee9; 
    }
    CodeEditor > QWidget { 
        background-color: #2a2e32; color: #eff0f1; 
    }
""" + create_menu_item_style(
    text_color="#FFFFFF",
    hover_bg_color="#3daee9",
    hover_text_color="#FFFFFF"
)


# --- Translation Dictionaries ---
LANG_TEXTS = {
    "en": {
        "title": "Mass Renamer 2.2", "settings": "Settings", "help": "Help", "dark": "Dark", "light": "Light",
        "file_location": "📂 File location:", "select_folder": "Select folder",
        "load_original": "Load names", "add_extension": "Add extension:",
        "orig_names": "Original names (one per line):", "new_names": "New names (one per line):",
        "log": "Log", "rename": "Rename Files", "undo": "Undo", "error": "Error", "yes": "Yes", "no": "No",
        "map_error": "Mapping Error", "invalid_chars": "Invalid Characters",
        "invalid_chars_msg": "The following characters are not allowed: {0}\nDo you want to remove them?",
        "not_found": "Not found or not a file:", "error_renaming": "Error renaming", "done": "🏁 Done.",
        "undo_confirm": "Are you sure you want to undo the last renaming operation?",
        "undo_done": "🏁 Undo completed.",
        "undoing": "⏮︎ Undoing...", "error_undoing": "Error undoing",
        "cannot_list": "Could not list files:", "select_valid_folder": "Select a valid folder.",
        "map_error_msg": "{0} original names vs {1} new names",
        "transfer_extensions": "Transf. Extensions", "remove_extension": "Remove Extensions",
        "conflict_title": "Name Conflict Found",
        "conflict_text": "Found {0} names that already exist in the destination folder or are duplicated in the list.",
        "conflict_info": (
            "• Click on <b>\"Rename\"</b> to add a numeric suffix (e.g., name_(1).txt) to all conflicting names and continue.<br><br>"
            "• Click on <b>\"List Errors\"</b> to cancel the operation and see the lines with problems in the Log area for manual correction.<br><br>"
            "• Click on <b>\"Cancel\"</b> to close this window without doing anything."
        ),
        "conflict_btn_rename": "Rename", "conflict_btn_list": "List Errors", "conflict_btn_cancel": "Cancel",
        "help_text": "<p>1. Select the folder where the files are located.<br>2. Click \"Load names\" or enter the original names manually.<br>3. Enter the new names.<br>4. Click on \"Rename Files\".</p><p><b>NOTE:</b> The file on line \"1\" of original names will be renamed to the name on line \"1\" of new names, and so on.</p><hr><p>Version: 2.2<br>License: <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\">Apache 2.0</a><br>Author: <a href=\"https://www.instagram.com/jedifonseca/\">Jedielson da Fonseca</a><br><a href=\"https://github.com/JediFonseca/mass_renamer\">Github</a></p>",
        "apply": "Apply", "cancel": "Cancel", "invalid_chars_os": "Disallow invalid characters for:",
        "invalid_chars_windows": "Windows", "invalid_chars_macos": "macOS",
        "invalid_chars_ios": "iOS", "invalid_chars_android": "Android",
        "edit_extensions": "Edit popular extensions (separated by comma and space):",
        "theme_mint_dark": "Mint-Y-Dark-Aqua", "theme_mint": "Mint-Y-Aqua", "theme_ubuntu": "Ubuntu", "theme_ubuntu_dark": "Ubuntu Dark",
        "theme_adwaita": "Adwaita", "theme_adwaita_dark": "Adwaita Dark", "theme_breeze": "Breeze", "theme_breeze_dark": "Breeze Dark",
        "how_to_use": "How to use Mass Renamer:", "language_label": "Language:", "theme_label": "Theme:",
        "forbidden_dir_title": "Forbidden Directory",
        "forbidden_dir_msg": "This is the application's configuration directory. Renaming files here is not permitted.",
        "log_saved_rename": "This log has been saved to: {0}\nIt will be overwritten on the next 'Rename' operation.",
        "log_saved_undo": "This log has been saved to: {0}\nIt will be overwritten on the next 'Undo' operation.",
        "undo_failed_title": "Undo Not Possible",
        "undo_failed_msg": "The last rename cannot be undone because the files in the target folder, or their names, have been modified. This is a Mass Renamer safeguard to prevent accidental data overwriting."
    },
    "pt": {
        "title": "Mass Renamer 2.2", "settings": "Ajustes", "help": "Ajuda", "dark": "Escuro", "light": "Claro",
        "file_location": "📂 Localização dos arquivos:", "select_folder": "Selecionar pasta",
        "load_original": "Carregar nomes", "add_extension": "Adicionar extensão:",
        "orig_names": "Nomes originais (um por linha):", "new_names": "Novos nomes (um por linha):",
        "log": "Log", "rename": "Renomear Arquivos", "undo": "Desfazer", "error": "Erro", "yes": "Sim", "no": "Não",
        "map_error": "Erro de Mapeamento", "invalid_chars": "Caracteres Inválidos",
        "invalid_chars_msg": "Os seguintes caracteres não são permitidos: {0}\nDeseja removê-los?",
        "not_found": "Não encontrado ou não é um arquivo:", "error_renaming": "Erro renomeando", "done": "🏁 Concluído.",
        "undo_confirm": "Tem certeza de que deseja desfazer a última operação de renomeação?",
        "undo_done": "🏁 Desfazer concluído.",
        "undoing": "⏮︎ Desfazendo...", "error_undoing": "Erro desfazendo",
        "cannot_list": "Não foi possível listar arquivos:", "select_valid_folder": "Selecione uma pasta válida.",
        "map_error_msg": "{0} nomes originais vs {1} nomes novos",
        "transfer_extensions": "Transf. Extensões", "remove_extension": "Remover Extensões",
        "conflict_title": "Conflito de Nomes Encontrado",
        "conflict_text": "Foram encontrados {0} nomes que já existem na pasta de destino ou estão duplicados na lista.",
        "conflict_info": (
            "• Clique em <b>\"Renomear\"</b> para adicionar um sufixo numérico (ex: nome_(1).txt) a todos os nomes conflitantes e continuar.<br><br>"
            "• Clique em <b>\"Listar Erros\"</b> para cancelar a operação e ver as linhas com problemas na área de Log para correção manual.<br><br>"
            "• Clique em <b>\"Cancelar\"</b> para fechar esta janela sem fazer nada."
        ),
        "conflict_btn_rename": "Renomear", "conflict_btn_list": "Listar Erros", "conflict_btn_cancel": "Cancelar",
        "help_text": "<p>1. Selecione a pasta onde os arquivos estão.<br>2. Clique em \"Carregar nomes\" ou insira os nomes originais manualmente.<br>3. Indique os novos nomes.<br>4. Clique em \"Renomear arquivos\".</p><p><b>OBS.:</b> O arquivo na linha \"1\" dos nomes originais será renomeado para o nome na linha \"1\" dos novos nomes, e assim sucessivamente.</p><hr><p>Versão: 2.2<br>Licença: <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\">Apache 2.0</a><br>Autor: <a href=\"https://www.instagram.com/jedifonseca/\">Jedielson da Fonseca</a><br><a href=\"https://github.com/JediFonseca/mass_renamer\">Github</a></p>",
        "apply": "Aplicar", "cancel": "Cancelar", "invalid_chars_os": "Não permitir caracteres inválidos para:",
        "invalid_chars_windows": "Windows", "invalid_chars_macos": "macOS",
        "invalid_chars_ios": "iOS", "invalid_chars_android": "Android",
        "edit_extensions": "Editar extensões populares (separadas por vírgula e espaço):",
        "theme_mint_dark": "Mint-Y-Dark-Aqua", "theme_mint": "Mint-Y-Aqua", "theme_ubuntu": "Ubuntu", "theme_ubuntu_dark": "Ubuntu Dark",
        "theme_adwaita": "Adwaita", "theme_adwaita_dark": "Adwaita Dark", "theme_breeze": "Breeze", "theme_breeze_dark": "Breeze Dark",
        "how_to_use": "Como usar o Mass Renamer:", "language_label": "Idioma:", "theme_label": "Tema:",
        "forbidden_dir_title": "Diretório Proibido",
        "forbidden_dir_msg": "Este é o diretório de configuração do aplicativo. Não é permitido renomear arquivos aqui.",
        "log_saved_rename": "Este log foi salvo em: {0}\nEle será sobrescrito na próxima operação de 'Renomear'.",
        "log_saved_undo": "Este log foi salvo em: {0}\nEle será sobrescrito na próxima operação de 'Desfazer'.",
        "undo_failed_title": "Não é Possível Desfazer",
        "undo_failed_msg": "A última renomeação não pode ser desfeita porque os arquivos na pasta de destino, ou seus nomes, foram modificados. Esta é uma proteção do Mass Renamer para evitar a sobrescrita acidental de seus dados."
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
        bg_color = self.lineNumberArea.palette().window().color()
        num_color = self.lineNumberArea.palette().windowText().color()
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

# --- Settings Dialog ---
class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setModal(True)
        self.setLayout(QVBoxLayout())

        self.tabs = QTabWidget()
        self.create_settings_tab()
        self.create_help_tab()
        self.layout().addWidget(self.tabs)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Apply | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_changes)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.custom_reject)
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).setFixedWidth(150)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setFixedWidth(150)
        self.layout().addWidget(self.button_box)

        self.resize(600, 450)
        self.setMinimumSize(600, 450)
        
        self.load_initial_state()
        self.load_translations()


    def create_settings_tab(self):
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        layout.setSpacing(15)

        # --- Language and Theme ---
        lang_theme_layout = QHBoxLayout()
        lang_theme_layout.setSpacing(20)

        # Language selection
        lang_v_layout = QVBoxLayout()
        lang_v_layout.setSpacing(5)
        self.lang_title_label = QLabel()
        lang_v_layout.addWidget(self.lang_title_label)
        self.lang_btn = QPushButton()
        self.lang_btn.setObjectName("settingsBtn")
        self.lang_btn.setFixedWidth(150)
        self.lang_btn.clicked.connect(self.show_lang_menu)
        lang_v_layout.addWidget(self.lang_btn)
        lang_theme_layout.addLayout(lang_v_layout)

        # Theme selection
        theme_v_layout = QVBoxLayout()
        theme_v_layout.setSpacing(5)
        self.theme_title_label = QLabel()
        theme_v_layout.addWidget(self.theme_title_label)
        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("settingsBtn")
        self.theme_btn.setFixedWidth(150)
        self.theme_btn.clicked.connect(self.show_theme_menu)
        theme_v_layout.addWidget(self.theme_btn)
        lang_theme_layout.addLayout(theme_v_layout)

        lang_theme_layout.addStretch(1)
        layout.addLayout(lang_theme_layout)

        # --- Invalid Characters ---
        self.char_label = QLabel()
        layout.addWidget(self.char_label)
        
        checkbox_layout = QHBoxLayout()
        self.check_windows = QCheckBox()
        self.check_macos = QCheckBox()
        self.check_ios = QCheckBox()
        self.check_android = QCheckBox()
        checkbox_layout.addWidget(self.check_windows)
        checkbox_layout.addWidget(self.check_macos)
        checkbox_layout.addWidget(self.check_ios)
        checkbox_layout.addWidget(self.check_android)
        checkbox_layout.addStretch(1)
        layout.addLayout(checkbox_layout)

        # --- Extensions Editor ---
        self.ext_label = QLabel()
        layout.addWidget(self.ext_label)
        self.ext_edit = QLineEdit()
        layout.addWidget(self.ext_edit)

        layout.addStretch(1)
        self.tabs.addTab(settings_widget, "")
        
    def create_help_tab(self):
        help_widget = QWidget()
        layout = QVBoxLayout(help_widget)
        
        self.how_to_label = QLabel()
        font = self.how_to_label.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 2)
        self.how_to_label.setFont(font)
        layout.addWidget(self.how_to_label)
        
        self.help_text_label = QLabel()
        self.help_text_label.setTextFormat(Qt.TextFormat.RichText)
        self.help_text_label.setWordWrap(True)
        self.help_text_label.setOpenExternalLinks(True)
        layout.addWidget(self.help_text_label)
        layout.addStretch(1)
        self.tabs.addTab(help_widget, "")

    def load_initial_state(self):
        """Loads settings from parent and stores original/pending states."""
        self.original_lang = self.parent_window.current_lang
        self.original_theme = self.parent_window.current_theme
        self.pending_lang = self.original_lang
        self.pending_theme = self.original_theme

        # Set button texts based on pending state
        self.update_lang_button_text()
        self.update_theme_button_text()
        
        s = self.parent_window.settings
        self.check_windows.setChecked(s.value("disallow_windows_chars", True, type=bool))
        self.check_macos.setChecked(s.value("disallow_macos_chars", True, type=bool))
        self.check_ios.setChecked(s.value("disallow_ios_chars", True, type=bool))
        self.check_android.setChecked(s.value("disallow_android_chars", True, type=bool))

        self.ext_edit.setText(", ".join(self.parent_window.popular_exts))

    def tr_dialog(self, key):
        """Translate using the pending language for the dialog's UI."""
        return LANG_TEXTS[self.pending_lang].get(key, key)

    def load_translations(self):
        self.setWindowTitle(self.tr_dialog("settings"))
        self.tabs.setTabText(0, self.tr_dialog("settings"))
        self.tabs.setTabText(1, self.tr_dialog("help"))
        self.help_text_label.setText(self.tr_dialog("help_text"))
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).setText(self.tr_dialog("apply"))
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(self.tr_dialog("cancel"))
        self.char_label.setText(self.tr_dialog("invalid_chars_os"))
        self.check_windows.setText(self.tr_dialog("invalid_chars_windows"))
        self.check_macos.setText(self.tr_dialog("invalid_chars_macos"))
        self.check_ios.setText(self.tr_dialog("invalid_chars_ios"))
        self.check_android.setText(self.tr_dialog("invalid_chars_android"))
        self.ext_label.setText(self.tr_dialog("edit_extensions"))
        self.how_to_label.setText(self.tr_dialog("how_to_use"))
        self.lang_title_label.setText(self.tr_dialog("language_label"))
        self.theme_title_label.setText(self.tr_dialog("theme_label"))
        
    def apply_changes(self):
        # Apply language and theme
        self.parent_window.set_language(self.pending_lang)
        self.parent_window.change_theme(self.pending_theme) # This is already visually applied
        
        # Save other settings
        s = self.parent_window.settings
        s.setValue("disallow_windows_chars", self.check_windows.isChecked())
        s.setValue("disallow_macos_chars", self.check_macos.isChecked())
        s.setValue("disallow_ios_chars", self.check_ios.isChecked())
        s.setValue("disallow_android_chars", self.check_android.isChecked())
        
        new_exts = [ext.strip() for ext in self.ext_edit.text().split(',') if ext.strip()]
        self.parent_window.popular_exts = new_exts
        s.setValue("popular_exts", ",".join(new_exts))
        
        self.parent_window._save_settings()
        self.accept()

    def custom_reject(self):
        """Revert theme if it was changed, then close."""
        if self.pending_theme != self.original_theme:
            self.parent_window.change_theme(self.original_theme)
        self.reject()

    def select_language(self, lang_code):
        self.pending_lang = lang_code
        self.update_lang_button_text()
        self.load_translations()

    def select_theme(self, theme_key):
        self.pending_theme = theme_key
        self.parent_window.change_theme(theme_key) # Live preview
        self.update_theme_button_text()
        
    def update_lang_button_text(self):
        lang_text = "Português" if self.pending_lang == 'pt' else "English"
        self.lang_btn.setText(lang_text)
        
    def update_theme_button_text(self):
        tr = self.tr_dialog
        theme_map = {
            "dark": tr("dark"), "light": tr("light"),
            "Mint-Y-Dark-Aqua": tr("theme_mint_dark"), "Mint-Y-Aqua": tr("theme_mint"),
            "Ubuntu": tr("theme_ubuntu"), "Ubuntu Dark": tr("theme_ubuntu_dark"),
            "Adwaita": tr("theme_adwaita"), "Adwaita Dark": tr("theme_adwaita_dark"),
            "Breeze": tr("theme_breeze"), "Breeze Dark": tr("theme_breeze_dark")
        }
        self.theme_btn.setText(theme_map.get(self.pending_theme, self.pending_theme))
        
    def show_lang_menu(self):
        menu = QMenu(self)
        menu.setObjectName("settingsMenu")
        menu.setFixedWidth(150)
        en_action = self.parent_window._create_centered_action("English", menu)
        en_action.triggered.connect(lambda: self.select_language("en"))
        menu.addAction(en_action)
        pt_action = self.parent_window._create_centered_action("Português", menu)
        pt_action.triggered.connect(lambda: self.select_language("pt"))
        menu.addAction(pt_action)
        menu.exec(self.lang_btn.mapToGlobal(self.lang_btn.rect().bottomLeft()))

    def show_theme_menu(self):
        menu = QMenu(self)
        menu.setObjectName("settingsMenu")
        menu.setFixedWidth(150)
        tr = self.tr_dialog
        theme_order = [
            ("dark", tr("dark")), ("light", tr("light")),
            ("Mint-Y-Dark-Aqua", tr("theme_mint_dark")), ("Mint-Y-Aqua", tr("theme_mint")),
            ("Ubuntu Dark", tr("theme_ubuntu_dark")), ("Ubuntu", tr("theme_ubuntu")),
            ("Adwaita Dark", tr("theme_adwaita_dark")), ("Adwaita", tr("theme_adwaita")),
            ("Breeze Dark", tr("theme_breeze_dark")), ("Breeze", tr("theme_breeze"))
        ]
        
        for theme_key, display_name in theme_order:
            action = self.parent_window._create_centered_action(display_name, menu)
            action.triggered.connect(lambda checked, t=theme_key: self.select_theme(t))
            menu.addAction(action)
            
        menu.exec(self.theme_btn.mapToGlobal(self.theme_btn.rect().bottomLeft()))


# --- Main Application Window ---
class MassRenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rename_history = []
        self.settings = QSettings("MassRenamer", "MassRenamer")

        self.themes = {
            "dark": DARK_STYLESHEET, "light": LIGHT_STYLESHEET,
            "Mint-Y-Dark-Aqua": MINT_Y_DARK_AQUA_STYLESHEET, "Mint-Y-Aqua": MINT_Y_AQUA_STYLESHEET,
            "Ubuntu": UBUNTU_STYLESHEET, "Ubuntu Dark": UBUNTU_DARK_STYLESHEET,
            "Adwaita": ADWAITA_STYLESHEET, "Adwaita Dark": ADWAITA_DARK_STYLESHEET,
            "Breeze": BREEZE_STYLESHEET, "Breeze Dark": BREEZE_DARK_STYLESHEET
        }

        self._load_settings()
        
        self.config_dir = os.path.expanduser("~/.config/MassRenamer")
        os.makedirs(self.config_dir, exist_ok=True)
        self.history_file_path = os.path.join(self.config_dir, "mass_renamer.history")
        
        self._init_ui()
        self._load_history_on_startup()
        
        self.set_language(self.current_lang)
        self.change_theme(self.current_theme, startup=True)

    def _load_settings(self):
        self.current_lang = self.settings.value("language", "pt")
        self.current_theme = self.settings.value("theme", "dark")
        default_exts = ".jpg, .png, .webp, .txt, .pdf, .docx, .xlsx, .pptx, .ods, .ots, .odt, .ott, .odp, .otp, .mp3, .ogg, .flac, .wav, .mp4, .avi, .mkv, .webm, .zip, .rar, .7z"
        ext_string = self.settings.value("popular_exts", default_exts)
        self.popular_exts = [ext.strip() for ext in ext_string.split(',') if ext.strip()]

    def _save_settings(self):
        self.settings.setValue("language", self.current_lang)
        self.settings.setValue("theme", self.current_theme)

    def _center_window(self):
        screen_geometry = self.screen().availableGeometry()
        center_point = screen_geometry.center()
        self.move(int(center_point.x() - self.width() / 2), int(center_point.y() - self.height() / 2))

    def _init_ui(self):
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
        self.main_layout.addWidget(self.label_location, 0, 0, 1, 4)

        self.entry_local = QLineEdit()
        self.main_layout.addWidget(self.entry_local, 1, 0, 1, 3)

        self.select_button = QPushButton()
        self.select_button.clicked.connect(self.select_folder)
        self.select_button.setFixedWidth(150)
        self.main_layout.addWidget(self.select_button, 1, 3)

    def _create_original_names_panel(self):
        self.label_orig = QLabel()
        self.main_layout.addWidget(self.label_orig, 2, 0, 1, 4)
        
        self.text_orig = CodeEditor(self)
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
        
        self.text_new = CodeEditor(self)
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

        # Create a container widget to hold both the text area and the progress label
        log_container = QWidget()
        log_layout = QGridLayout(log_container)
        log_layout.setContentsMargins(0, 0, 0, 0)

        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text, 0, 0)

        # Create the progress label and add it to the container's layout
        self.progress_label = QLabel("0%", log_container)
        self.progress_label.setObjectName("progressLabel")
        self.progress_label.setFont(self.log_text.font())
        # Align it to the bottom-right corner of the layout cell
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        log_layout.addWidget(self.progress_label, 0, 0)
        self.progress_label.hide()  # Initially hidden

        self.main_layout.addWidget(log_container, 9, 0, 1, 4)
        
    def _create_bottom_bar(self):
        buttons_frame = QWidget()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        
        self.settings_label = QLabel()
        self.settings_label.setObjectName("settingsLabel")
        self.settings_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_label.mousePressEvent = self.open_settings_dialog
        
        self.rename_button = QPushButton()
        self.rename_button.clicked.connect(self.rename)
        
        self.undo_button = QPushButton()
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self.undo)
        
        for btn in [self.rename_button, self.undo_button]:
            btn.setFixedWidth(150)

        buttons_layout.addWidget(self.settings_label, 0, Qt.AlignmentFlag.AlignLeft)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.rename_button)
        buttons_layout.addWidget(self.undo_button)
        self.main_layout.addWidget(buttons_frame, 10, 0, 1, 4)

    def _load_history_on_startup(self):
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

    def rename(self):
        self.rename_history.clear()
        self.progress_label.hide()
        QApplication.processEvents()
        
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
        
        # Check if the selected folder is the configuration directory
        config_path = os.path.normpath(self.config_dir)
        selected_path = os.path.normpath(folder)
        if config_path == selected_path:
            QMessageBox.critical(self, self.tr("forbidden_dir_title"), self.tr("forbidden_dir_msg"))
            return None
            
        origs = [l.strip() for l in self.text_orig.toPlainText().splitlines() if l.strip()]
        news = [l.strip() for l in self.text_new.toPlainText().splitlines() if l.strip()]
        if len(origs) != len(news):
            QMessageBox.critical(self, self.tr("map_error"), self.tr("map_error_msg").format(len(origs), len(news)))
            return None

        # --- Character Validation based on settings ---
        illegal_chars = ILLEGAL_CHARS_LINUX.copy() # Base for all
        if self.settings.value("disallow_windows_chars", True, type=bool):
            illegal_chars.update(ILLEGAL_CHARS_WINDOWS)
        if self.settings.value("disallow_macos_chars", True, type=bool):
            illegal_chars.update(ILLEGAL_CHARS_MACOS)
        if self.settings.value("disallow_ios_chars", True, type=bool):
            illegal_chars.update(ILLEGAL_CHARS_IOS)
        if self.settings.value("disallow_android_chars", True, type=bool):
            illegal_chars.update(ILLEGAL_CHARS_ANDROID)

        found_illegal = {ch for name in news for ch in name if ch in illegal_chars}

        if found_illegal:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(self.tr("invalid_chars"))
            msg_box.setText(self.tr("invalid_chars_msg").format(" ".join(sorted(found_illegal))))
            yes_btn = msg_box.addButton(self.tr("yes"), QMessageBox.ButtonRole.YesRole)
            msg_box.addButton(self.tr("no"), QMessageBox.ButtonRole.NoRole)
            msg_box.exec()
            if msg_box.clickedButton() == yes_btn:
                news = [''.join(c for c in n if c not in illegal_chars) for n in news]
                self.text_new.setPlainText("\n".join(news))
            else:
                return None
        return folder, origs, news

    def _handle_name_conflicts(self, news, folder):
        conflicting_indices = set()
        
        # 1. Check for files that already exist in the folder
        for i, name in enumerate(news):
            if os.path.exists(os.path.join(folder, name)):
                conflicting_indices.add(i)

        # 2. Check for duplicate names within the 'news' list itself
        name_counts = Counter(news)
        for name, count in name_counts.items():
            if count > 1:
                # Find all indices of this duplicated name
                for i, n in enumerate(news):
                    if n == name:
                        conflicting_indices.add(i)

        if not conflicting_indices:
            return news

        conflicts = [{'name': news[i], 'index': i, 'line': i + 1} for i in sorted(list(conflicting_indices))]

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
            self.log_text.setPlainText(f"Operation canceled. The names on the following lines already exist in the selected folder or are duplicated: {line_numbers}.")
            return None
        elif clicked == cancel_btn: return None
        elif clicked == rename_btn:
            temp_news = list(news) # Work on a copy
            for c in conflicts:
                base, ext = os.path.splitext(c['name'])
                count = 1
                while True:
                    new_name = f"{base}_({count}){ext}"
                    # Check against both filesystem and the rest of the list
                    if not os.path.exists(os.path.join(folder, new_name)) and new_name not in temp_news:
                        temp_news[c['index']] = new_name
                        break
                    count += 1
            self.text_new.setPlainText("\n".join(temp_news))
            return temp_news
        return None

    def _execute_rename(self, folder, origs, news):
        self.log_text.clear()
        
        total_files = len(origs)
        if total_files == 0:
            self.log_text.appendPlainText(f"\n{self.tr('done')}")
            return
            
        processed_count = 0
        self.progress_label.setText("0%")
        self.progress_label.show()

        try: os.remove(self.history_file_path)
        except OSError: pass
        
        temp_history = []
        for o, n in zip(origs, news):
            src, dst = os.path.join(folder, o), os.path.join(folder, n)
            if not os.path.isfile(src):
                self.log_text.appendPlainText(f"❌ {self.tr('not_found')} {o}")
            else:
                try:
                    shutil.move(src, dst)
                    temp_history.append((dst, src))
                    with open(self.history_file_path, "w", encoding="utf-8") as f:
                        json.dump(temp_history, f)
                    self.log_text.appendPlainText(f"✅ {o} → {n}")
                except Exception as e:
                    self.log_text.appendPlainText(f"⚠️ {self.tr('error_renaming')} {o}: {e}")
            
            # Update progress
            processed_count += 1
            percentage = int((processed_count / total_files) * 100)
            self.progress_label.setText(f"{percentage}%")
            QApplication.processEvents() # Force UI update to show progress

        self.rename_history.extend(temp_history)
        if self.rename_history: self.undo_button.setEnabled(True)
        self.log_text.appendPlainText(f"\n{self.tr('done')}")

        # Save the log file
        rename_log_path = os.path.join(self.config_dir, "rename.log")
        save_msg = self.tr("log_saved_rename").format(rename_log_path)
        self.log_text.appendPlainText(f"\n---\n{save_msg}")
        try:
            with open(rename_log_path, "w", encoding="utf-8") as f:
                f.write(self.log_text.toPlainText())
        except IOError as e:
            print(f"Could not save rename log: {e}")

    def undo(self):
        self.progress_label.hide()
        if not self.rename_history:
            return
            
        # --- Undo Safety Check ---
        all_files_exist = True
        for new_path, _ in self.rename_history:
            if not os.path.exists(new_path):
                all_files_exist = False
                break

        if not all_files_exist:
            QMessageBox.critical(self, self.tr("undo_failed_title"), self.tr("undo_failed_msg"))
            return
        # --- End of Safety Check ---
        
        reply = QMessageBox.question(self, self.tr("undo"), self.tr("undo_confirm"),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
            
        self.log_text.clear()
        self.log_text.appendPlainText(f"{self.tr('undoing')}\n")
        
        total_files = len(self.rename_history)
        if total_files == 0:
            return
            
        processed_count = 0
        self.progress_label.setText("0%")
        self.progress_label.show()
        
        for dst, src in reversed(self.rename_history):
            try:
                shutil.move(dst, src)
                self.log_text.appendPlainText(f"↩️ {os.path.basename(dst)} → {os.path.basename(src)}")
            except Exception as e:
                self.log_text.appendPlainText(f"⚠️ {self.tr('error_undoing')} {dst}: {e}")
            
            # Update progress
            processed_count += 1
            percentage = int((processed_count / total_files) * 100)
            self.progress_label.setText(f"{percentage}%")
            QApplication.processEvents() # Force UI update
                
        self.log_text.appendPlainText(f"\n{self.tr('undo_done')}")
        self.rename_history.clear()
        self.undo_button.setEnabled(False)
        try:
            os.remove(self.history_file_path)
        except OSError:
            pass

        # Save the log file
        undo_log_path = os.path.join(self.config_dir, "undo.log")
        save_msg = self.tr("log_saved_undo").format(undo_log_path)
        self.log_text.appendPlainText(f"\n---\n{save_msg}")
        try:
            with open(undo_log_path, "w", encoding="utf-8") as f:
                f.write(self.log_text.toPlainText())
        except IOError as e:
            print(f"Could not save undo log: {e}")

    def tr(self, key):
        return LANG_TEXTS[self.current_lang].get(key, key)

    def set_language(self, lang_code):
        self.current_lang = lang_code
        self.setWindowTitle(self.tr("title"))
        self.settings_label.setText(self.tr("settings"))
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

    def change_theme(self, theme_key, startup=False):
        self.current_theme = theme_key
        stylesheet = self.themes.get(theme_key, DARK_STYLESHEET)
        QApplication.instance().setStyleSheet(stylesheet)
        
        # Set progress label color dynamically from the main text color
        palette = self.log_text.palette()
        text_color = palette.text().color()
        self.progress_label.setStyleSheet(f"color: {text_color.name()};")
        
        if not startup: self._save_settings()

    def _create_centered_action(self, text, menu):
        action = QWidgetAction(menu)
        label = QLabel(text)
        label.setObjectName("menuItemLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        action.setDefaultWidget(label)
        return action

    def open_settings_dialog(self, event=None):
        dialog = SettingsDialog(self)
        dialog.exec()

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
        menu.setFixedWidth(75)
        for ext in self.popular_exts:
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
