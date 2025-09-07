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
import sys  # Added to handle resource paths
import customtkinter as ctk
from tkinter import filedialog, messagebox
from customtkinter import CTkFont
from PIL import Image, ImageTk

# forbidden characters on Windows
ILLEGAL_CHARS = set('<>:"/\\|?*')

# most popular extensions
POPULAR_EXTS = [
    ".txt", ".jpg", ".png", ".webp", ".pdf", ".docx",
    ".xlsx", ".mp3", ".mp4", ".avi", ".mkv", ".zip", ".py"
]

# background colors for dark and light
BG_COLOR_DARK  = "#282828"
BG_COLOR_LIGHT = "#e8e8e8"

# rename history (for undo)
rename_history = []

# ----------------- Translation dictionaries -----------------
LANG_TEXTS = {
    "en": {
        "help": "Help",
        "dark_mode": "Dark Mode",
        "dark": "Dark",
        "light": "Light",
        "file_location": "📂 File location:",
        "select_folder": "Select folder",
        "load_original": "Load original names",
        "add_extension": "Add extension:",
        "orig_names": "Original names (one per line):",
        "new_names": "New names (one per line):",
        "log": "Log",
        "rename": "Rename files",
        "undo": "Undo",
        "error": "Error",
        "map_error": "Mapping Error",
        "invalid_chars": "Invalid characters",
        "invalid_chars_msg": "There are forbidden characters in the new names.\nDo you want to remove them?",
        "not_found": "Not found:",
        "error_renaming": "Error renaming",
        "done": "Done.",
        "undo_confirm": "Confirm undo all renames?",
        "undo_done": "Undo completed.",
        "undoing": "Undoing...",
        "error_undoing": "Error undoing",
        "cannot_list": "Could not list files:",
        "help_text": (
            "1. Select the folder where the files to be renamed are located.\n"
            "2. Enter the original names of all files in the field \"Original names\".\n"
            "3. Enter the new names in the field \"New names\".\n"
            "4. Click on \"Rename files\".\n\n"
            "NOTE: The file whose original name is on line \"1\" of the field \"Original names\" "
            "will be renamed to the name that is on line \"1\" of the field \"New names\" and so on.\n\n"
            "License: Apache License 2.0\n"
            "License Link: http://www.apache.org/licenses/LICENSE-2.0\n"
            "Author: 2025 Jedielson da Fonseca\n"
            "Contact: jdfn7@proton.me"
        )
    },
    "pt": {
        "help": "Ajuda",
        "dark_mode": "Modo Escuro",
        "dark": "Escuro",
        "light": "Claro",
        "file_location": "📂 Localização dos arquivos:",
        "select_folder": "Selecionar pasta",
        "load_original": "Carregar nomes originais",
        "add_extension": "Adicionar extensão:",
        "orig_names": "Nomes originais (um por linha):",
        "new_names": "Novos nomes (um por linha):",
        "log": "Log",
        "rename": "Renomear Arquivos",
        "undo": "Desfazer",
        "error": "Erro",
        "map_error": "Erro de Mapeamento",
        "invalid_chars": "Caracteres inválidos",
        "invalid_chars_msg": "Há caracteres não permitidos nos novos nomes.\nDeseja removê-los?",
        "not_found": "Não encontrado:",
        "error_renaming": "Erro renomeando",
        "done": "🏁 Concluído.",
        "undo_confirm": "Confirmar desfazer todas renomeações?",
        "undo_done": "🏁 Desfazer concluído.",
        "undoing": "⏮︎Desfazendo...",
        "error_undoing": "Erro desfazendo",
        "cannot_list": "Não foi possível listar arquivos:",
        "help_text": (
            "1. Selecione a pasta onde os arquivos a serem renomeados estão localizados.\n"
            "2. Indique os nomes originais de todos os arquivos no campo \"Nomes originais\".\n"
            "3. Indique os novos nomes no campo \"Novos nomes\".\n"
            "4. Clique em \"Renomear arquivos\".\n\n"
            "OBS.: O arquivo cujo nome original estiver na linha \"1\" do campo \"Nomes originais\" "
            "será renomeado para o nome que está na linha \"1\" do campo \"Novos nomes\" e assim sucessivamente.\n\n"
            "Licença: Apache License 2.0\n"
            "Link da licença: http://www.apache.org/licenses/LICENSE-2.0\n"
            "Autor: 2025 Jedielson da Fonseca\n"
            "Contato: jdfn7@proton.me"
        )
    }
}

CONFIG_PATH = "config.json"

def load_config():
    """Load configuration from disk or return defaults."""
    default = {"language": "en", "theme": "dark"}
    if not os.path.exists(CONFIG_PATH):
        return default
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {**default, **data}
    except Exception:
        return default

def save_config(language=None, theme=None):
    """Merge and save configuration to disk."""
    data = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    if language is not None:
        data["language"] = language
    if theme is not None:
        data["theme"] = theme
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

# Load settings
config = load_config()
current_lang = config["language"]
current_theme = config["theme"]
HELP_TEXT = LANG_TEXTS[current_lang]["help_text"]

# --- NEW: Function to find the icon path ---
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----------------- Utility functions -----------------
def update_line_numbers(text_widget, ln_widget):
    total = int(text_widget.index("end-1c").split(".")[0])
    ln_widget.configure(state="normal")
    ln_widget.delete("1.0", "end")
    for i in range(1, total + 1):
        ln_widget.insert("end", f"{i}\n")
    ln_widget.configure(state="disabled")
    first, _ = text_widget.yview()
    ln_widget.yview_moveto(first)

def setup_line_number_sync(text_widget, ln_widget):
    # keep line numbers aligned on scroll
    def on_text_scroll(top, bottom):
        ln_widget.yview_moveto(top)
    text_widget.configure(yscrollcommand=on_text_scroll)

    # update numbers when text changes
    def on_modified(event=None):
        update_line_numbers(text_widget, ln_widget)
        try:
            text_widget.edit_modified(False)
        except Exception:
            pass
    text_widget.bind("<<Modified>>", on_modified)

    # scroll text when line-widget scrolls
    def on_ln_mousewheel(event):
        delta = -int(event.delta / 120) if event.delta else 0
        if delta:
            text_widget.yview_scroll(delta, "units")
            top, _ = text_widget.yview()
            ln_widget.yview_moveto(top)
        return "break"
    ln_widget.bind("<MouseWheel>", on_ln_mousewheel)

    update_line_numbers(text_widget, ln_widget)

def add_extension_to_widget(text_widget, ln_widget, ext):
    if not ext:
        return
    lines = [l.rstrip() for l in text_widget.get("1.0", "end").splitlines()]
    text_widget.delete("1.0", "end")
    for l in lines:
        if not l:
            continue
        text_widget.insert("end", (l if l.endswith(ext) else l + ext) + "\n")
    update_line_numbers(text_widget, ln_widget)

def setup_line_highlighting(text_widget, ln_widget):
    """Configure current line highlighting in the line-number widget."""
    ln_widget.tag_config("highlight", background="#1f6aa5")
    def update_highlight(event=None):
        ln_widget.configure(state="normal")
        ln_widget.tag_remove("highlight", "1.0", "end")
        try:
            line_num = text_widget.index(ctk.INSERT).split('.')[0]
        except Exception:
            ln_widget.configure(state="disabled")
            return
        start = f"{line_num}.0"
        end = f"{line_num}.end"
        ln_widget.tag_add("highlight", start, end)
        ln_widget.configure(state="disabled")
    text_widget.bind("<ButtonRelease-1>", update_highlight)
    text_widget.bind("<KeyRelease>", update_highlight)

# ----------------- Main actions -----------------
def renomear():
    global rename_history
    rename_history.clear()

    folder = entry_local.get().strip()
    origs = [l.strip() for l in text_orig.get("1.0", "end").splitlines() if l.strip()]
    news  = [l.strip() for l in text_new.get("1.0", "end").splitlines() if l.strip()]

    if not folder or not os.path.isdir(folder):
        messagebox.showerror(LANG_TEXTS[current_lang]["error"], "Select a valid folder.")
        return

    if len(origs) != len(news):
        messagebox.showerror(
            LANG_TEXTS[current_lang]["map_error"],
            f"{len(origs)} orig vs {len(news)} new names"
        )
        return

    if any(ch in ILLEGAL_CHARS for name in news for ch in name):
        resp = messagebox.askyesno(
            LANG_TEXTS[current_lang]["invalid_chars"],
            LANG_TEXTS[current_lang]["invalid_chars_msg"]
        )
        if resp:
            cleaned = [''.join(c for c in n if c not in ILLEGAL_CHARS) for n in news]
            text_new.delete("1.0", "end")
            for ln in cleaned:
                text_new.insert("end", ln + "\n")
            update_line_numbers(text_new, ln_new)
            news = cleaned
        else:
            return

    log_text.delete("1.0", "end")
    for o, n in zip(origs, news):
        src = os.path.join(folder, o)
        dst = os.path.join(folder, n)
        if not os.path.exists(src):
            log_text.insert("end", f"❌ {LANG_TEXTS[current_lang]['not_found']} {o}\n")
            continue
        try:
            os.rename(src, dst)
            rename_history.append((dst, src))
            log_text.insert("end", f"✅ {o} → {n}\n")
        except Exception as e:
            log_text.insert("end", f"⚠️ {LANG_TEXTS[current_lang]['error_renaming']} {o}: {e}\n")

    if rename_history:
        undo_button.configure(state="normal")
    log_text.insert("end", f"\n{LANG_TEXTS[current_lang]['done']}")

def desfazer():
    global rename_history
    if not rename_history:
        return
    if not messagebox.askyesno(LANG_TEXTS[current_lang]["undo"], LANG_TEXTS[current_lang]["undo_confirm"]):
        return

    log_text.insert("end", f"\n{LANG_TEXTS[current_lang]['undoing']}\n")
    for dst, src in reversed(rename_history):
        try:
            os.rename(dst, src)
            log_text.insert("end", f"↩️ {os.path.basename(dst)} → {os.path.basename(src)}\n")
        except Exception as e:
            log_text.insert("end", f"⚠️ {LANG_TEXTS[current_lang]['error_undoing']} {dst}: {e}\n")

    log_text.insert("end", f"\n{LANG_TEXTS[current_lang]['undo_done']}")
    rename_history.clear()
    undo_button.configure(state="disabled")

def carregar_nomes_originais():
    folder = entry_local.get().strip()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror(LANG_TEXTS[current_lang]["error"], "Select a valid folder.")
        return
    try:
        items = os.listdir(folder)
        files = sorted(f for f in items if os.path.isfile(os.path.join(folder, f)))
    except Exception as e:
        messagebox.showerror(LANG_TEXTS[current_lang]["error"], f"{LANG_TEXTS[current_lang]['cannot_list']}\n{e}")
        return

    text_orig.delete("1.0", "end")
    for name in files:
        text_orig.insert("end", name + "\n")  
    update_line_numbers(text_orig, ln_orig)

# ----------------- GUI construction -----------------
ctk.set_appearance_mode(current_theme)
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Mass Renamer 1.0")

# NOVO BLOCO com Pillow para alta qualidade
try:
    # Caminho para o ícone de alta resolução
    icon_path = resource_path('appicon.png')

    # 1. Abre a imagem original com Pillow
    high_res_image = Image.open(icon_path)

    # 2. Redimensiona a imagem para um tamanho ideal com um filtro de alta qualidade
    #    Image.Resampling.LANCZOS é o melhor para reduzir imagens
    resized_image = high_res_image.resize((48, 48), Image.Resampling.LANCZOS)

    # 3. Converte a imagem do Pillow para um formato que o Tkinter entende
    icon_image = ImageTk.PhotoImage(resized_image)

    # 4. Define o ícone da janela
    app.wm_iconphoto(False, icon_image)

except Exception as e:
    print(f"Error loading icon: {e}")

bg = BG_COLOR_DARK if current_theme == "dark" else BG_COLOR_LIGHT
app.geometry("900x650")
app.minsize(900, 650)
app.configure(fg_color=bg)

container = ctk.CTkFrame(app, fg_color=bg, corner_radius=0, border_width=0)
container.pack(fill="both", expand=True, padx=15, pady=15)

content = ctk.CTkFrame(container, fg_color="transparent", corner_radius=0, border_width=0)
content.pack(fill="both", expand=True)

for c in range(4):
    content.grid_columnconfigure(c, weight=0)
content.grid_columnconfigure(0, weight=1)
content.grid_columnconfigure(2, weight=1)
content.grid_columnconfigure(3, weight=0)
content.grid_rowconfigure(4, weight=1)
content.grid_rowconfigure(7, weight=1)
content.grid_rowconfigure(10, weight=1)

def change_theme(choice):
    mode = "dark" if choice == LANG_TEXTS[current_lang]["dark"] else "light"
    ctk.set_appearance_mode(mode)
    new_bg = BG_COLOR_DARK if mode == "dark" else BG_COLOR_LIGHT
    app.configure(fg_color=new_bg)
    container.configure(fg_color=new_bg)
    save_config(theme=mode)

theme_menu = ctk.CTkOptionMenu(
    content,
    values=[LANG_TEXTS[current_lang]["light"], LANG_TEXTS[current_lang]["dark"]],
    command=change_theme,
    width=141
)
theme_menu.grid(row=0, column=3, sticky="ne", padx=0, pady=5)
initial_theme_label = LANG_TEXTS[current_lang]["dark"] if current_theme == "dark" else LANG_TEXTS[current_lang]["light"]
theme_menu.set(initial_theme_label)

def change_lang(choice):
    new_lang = "en" if choice == "English" else "pt"
    set_language(new_lang)
    save_config(language=new_lang)

lang_menu = ctk.CTkOptionMenu(
    content,
    values=["English", "Português"],
    command=change_lang,
    width=141
)
lang_menu.grid(row=0, column=2, sticky="ne", padx=(0,5), pady=5)
lang_menu.set("English" if current_lang == "en" else "Português")

label_location = ctk.CTkLabel(content, text=LANG_TEXTS[current_lang]["file_location"])
label_location.grid(row=0, column=0, columnspan=2, sticky="w", pady=(5,0))

entry_local = ctk.CTkEntry(content)
entry_local.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(2,10))

def selecionar_pasta():
    folder = filedialog.askdirectory()
    if folder:
        entry_local.delete(0, "end")
        entry_local.insert(0, folder)
        load_button.configure(state="normal")

select_button = ctk.CTkButton(content, text=LANG_TEXTS[current_lang]["select_folder"], command=selecionar_pasta)
select_button.grid(row=1, column=3, sticky="e", padx=(2,0), pady=(2,10))

fg_color = entry_local.cget("fg_color")
bw = entry_local.cget("border_width")
bc = entry_local.cget("border_color")
textbox_font = CTkFont(family="Consolas", size=13)

label_orig = ctk.CTkLabel(content, text=LANG_TEXTS[current_lang]["orig_names"])
label_orig.grid(row=3, column=0, columnspan=4, sticky="w")
frame_orig = ctk.CTkFrame(content, fg_color="transparent")
frame_orig.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=(2,5))
frame_orig.grid_columnconfigure(1, weight=1)
frame_orig.grid_rowconfigure(0, weight=1)

ln_orig = ctk.CTkTextbox(frame_orig, width=80, state="disabled",
                         fg_color=fg_color, border_width=bw, border_color=bc,
                         font=textbox_font)
ln_orig.grid(row=0, column=0, sticky="ns")

text_orig = ctk.CTkTextbox(frame_orig, fg_color=fg_color,
                           border_width=bw, border_color=bc,
                           font=textbox_font)
text_orig.grid(row=0, column=1, sticky="nsew")

setup_line_number_sync(text_orig, ln_orig)
setup_line_highlighting(text_orig, ln_orig)

ext_frame_o = ctk.CTkFrame(content, fg_color="transparent")
ext_frame_o.grid(row=5, column=0, columnspan=2, sticky="w", pady=(0,10))
ext_label_o = ctk.CTkLabel(ext_frame_o, text=LANG_TEXTS[current_lang]["add_extension"])
ext_label_o.pack(side="left", padx=(0,5))
ctk.CTkOptionMenu(ext_frame_o, values=POPULAR_EXTS, width=120, corner_radius=6,
    command=lambda e: add_extension_to_widget(text_orig, ln_orig, e)).pack(side="left")

load_button = ctk.CTkButton(content, text=LANG_TEXTS[current_lang]["load_original"],
                            command=carregar_nomes_originais, state="disabled")
load_button.grid(row=5, column=2, columnspan=2, sticky="e", padx=(0,5), pady=(0,10))

label_new = ctk.CTkLabel(content, text=LANG_TEXTS[current_lang]["new_names"])
label_new.grid(row=6, column=0, columnspan=4, sticky="w")
frame_new = ctk.CTkFrame(content, fg_color="transparent")
frame_new.grid(row=7, column=0, columnspan=4, sticky="nsew", pady=(2,5))
frame_new.grid_columnconfigure(1, weight=1)
frame_new.grid_rowconfigure(0, weight=1)

ln_new = ctk.CTkTextbox(frame_new, width=80, state="disabled",
                       fg_color=fg_color, border_width=bw, border_color=bc,
                       font=textbox_font)
ln_new.grid(row=0, column=0, sticky="ns")

text_new = ctk.CTkTextbox(frame_new, fg_color=fg_color,
                         border_width=bw, border_color=bc,
                         font=textbox_font)
text_new.grid(row=0, column=1, sticky="nsew")

setup_line_number_sync(text_new, ln_new)
setup_line_highlighting(text_new, ln_new)

ext_frame_n = ctk.CTkFrame(content, fg_color="transparent")
ext_frame_n.grid(row=8, column=0, columnspan=2, sticky="w", pady=(0,10))
ext_label_n = ctk.CTkLabel(ext_frame_n, text=LANG_TEXTS[current_lang]["add_extension"])
ext_label_n.pack(side="left", padx=(0,5))
ctk.CTkOptionMenu(ext_frame_n, values=POPULAR_EXTS, width=120, corner_radius=6,
    command=lambda e: add_extension_to_widget(text_new, ln_new, e)).pack(side="left")

label_log = ctk.CTkLabel(content, text=LANG_TEXTS[current_lang]["log"])
label_log.grid(row=9, column=0, columnspan=4, sticky="w")
frame_log = ctk.CTkFrame(content, fg_color="transparent")
frame_log.grid(row=10, column=0, columnspan=4, sticky="nsew", pady=(2,10))
frame_log.grid_columnconfigure(0, weight=1)
frame_log.grid_rowconfigure(0, weight=1)

log_text = ctk.CTkTextbox(frame_log, fg_color=fg_color,
                          border_width=bw, border_color=bc,
                          font=textbox_font)
log_text.grid(row=0, column=0, sticky="nsew")

buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
buttons_frame.grid(row=11, column=0, columnspan=4, pady=(10,5), sticky="ew")
buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(3, weight=1)

help_label = ctk.CTkLabel(
    buttons_frame,
    text=LANG_TEXTS[current_lang]["help"],
    text_color=ctk.CTkButton(buttons_frame, text="").cget("fg_color"),
    cursor="hand2",
    font=CTkFont(weight="bold")
)
help_label.grid(row=0, column=0, sticky="w")
help_label.bind("<Button-1>", lambda e: messagebox.showinfo(LANG_TEXTS[current_lang]["help"], HELP_TEXT))

rename_button = ctk.CTkButton(
    buttons_frame,
    text=LANG_TEXTS[current_lang]["rename"],
    command=renomear
)
rename_button.grid(row=0, column=1, padx=(13,7))

undo_button = ctk.CTkButton(
    buttons_frame,
    text=LANG_TEXTS[current_lang]["undo"],
    state="disabled",
    command=desfazer
)
undo_button.grid(row=0, column=2, padx=(0,50))

def set_language(lang):
    global current_lang, HELP_TEXT
    current_lang = lang
    HELP_TEXT = LANG_TEXTS[current_lang]["help_text"]
    save_config(language=lang)
    texts = LANG_TEXTS[lang]
    # update static texts
    help_label.configure(text=texts["help"])
    label_location.configure(text=texts["file_location"])
    select_button.configure(text=texts["select_folder"])
    load_button.configure(text=texts["load_original"])
    label_orig.configure(text=texts["orig_names"])
    label_new.configure(text=texts["new_names"])
    label_log.configure(text=texts["log"])
    rename_button.configure(text=texts["rename"])
    undo_button.configure(text=texts["undo"])
    ext_label_o.configure(text=texts["add_extension"])
    ext_label_n.configure(text=texts["add_extension"])
    # update menus
    lang_menu.set("English" if current_lang == "en" else "Português")
    theme_menu.configure(values=[texts["light"], texts["dark"]])
    theme_menu.set(texts[current_theme])

# initialize language and theme
set_language(current_lang)

app.mainloop()
