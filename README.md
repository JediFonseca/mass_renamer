# 🗂️ Mass Renamer 2.0

Download for Linux and Windows: [**Releases**](https://github.com/JediFonseca/mass_renamer/releases)

## In English (Portuguese below):

**Mass Renamer** is a desktop application developed in Python with a `Qt6` interface, which allows you to rename multiple files quickly, safely, and in an organized manner. It supports undoing the most recent renaming, adding extensions to filenames and a multilingual interface (🇧🇷 Portuguese and 🇺🇸 English).

<img width="913" height="696" alt="Captura de tela de 2025-09-08 09-50-32" src="https://github.com/user-attachments/assets/c9221352-ea9b-4d86-9c81-974139e60b60" />

<img width="911" height="695" alt="Captura de tela de 2025-09-08 09-50-46" src="https://github.com/user-attachments/assets/33f385fb-ecc0-4f7e-99e2-60440298a278" />

---

### 🎯 Purpose

This software was created for **recreational and experimental purposes**. It is being made available as **free** and **open-source**. If it helps you in any way, make good use of it. Feel free to contribute, adapt, or share! I am not a developer, I don't work in the field, and I don't have in-depth knowledge of any programming language. The development of this software was done **for fun and as a hobby** with the assistance of the AI (Vibe Coding).

---

### 🚀 How to use

1. Run the ".appimage", ".exe" or the Python script (`mass_renamer.py`).
2. Select the folder where the files to be renamed are located.
3. Click "Load names" to load the names of all files in the selected folder or enter the original names manually in the "Original names" field.
4. Enter the new names in the "New names" field.
5. Click on "Rename files".

NOTE: The file whose original name is on line "1" of the "Original names" field will be renamed to the name that is on line "1" of the "New names" field, and so on.

---

### 🛠️ Features

- 📁 Selection of the folder with the files to be renamed;
- ✍️ Fields for original names and new names (with line numbering);
- 🔁 Button to undo the most recent renaming;
- 🧼 Automatic removal of invalid characters for filenames;
- 🌙 Toggle between light and dark mode (the option is saved for future sessions);
- 🌐 Support for two languages: Portuguese and English (the option is saved for future sessions);
- 🔤 Quick addition of popular extensions to filenames (.jpg, .pdf, .mp3, etc.);
- 🧠 Responsive and intuitive interface with `Qt6`.

---

### 📦 Requirements (to run from source code)

If you prefer to run the project directly from the Python code, without using the `.exe` or the `.appimage` executable, you will need:

On Linux Mint 22.2:

"apt install" packages: python3 python3-pip python3-tk build-essential python3.12-venv patchelf ccache
"pip install" packages: PyQt6 pyinstaller nuitka

On Windows (using the 1.0 version source code):

- Python 3.13 or higher
- Libraries:
  - `customtkinter`
  - `tkinter` 
  - `json`, `os`, `sys`

---

### 📄 License

Distributed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). You can use, modify, and redistribute this software freely, as long as you maintain the attribution and license notices.

---

### 👤 Author

**Jedielson da Fonseca**

📧 [jdfn7@proton.me](mailto:jdfn7@proton.me)

# 🗂️ Mass Renamer 1.0

Download para Linux e Windows: [**Releases**](https://github.com/JediFonseca/mass_renamer/releases)

## Em Português:

**Mass Renamer** é um aplicativo desktop desenvolvido em Python com interface `Qt6`, que permite renomear múltiplos arquivos de forma rápida, segura e organizada. Suporta desfazer a renomeação mais recente, adicionar extensões aos nomes de arquivo e interface multilíngue (🇧🇷 português e 🇺🇸 inglês).

---

### 🎯 Propósito

Este software foi criado para **fins recreativos e experimentais**. Está disponível como **gratuito** e **open-source**. Se isso ajudar de alguma forma, faça bom uso. Sinta-se à vontade para contribuir, adaptar ou compartilhar! Não sou desenvolvedor, não trabalho na área e não tenho conhecimento aprofundado em nenhuma linguagem de programação. O desenvolvimento deste software foi feito **por diversão e como hobby** com assistência de IA (Vibe Coding).

---

### 🚀 Como usar

1. Execute o ".appimage", ".exe" ou o script Python (`mass_renamer.py`).  
2. Selecione a pasta onde estão os arquivos a serem renomeados.  
3. Clique em "Carregar nomes" para carregar os nomes de todos os arquivos na pasta selecionada ou insira os nomes originais manualmente no campo "Nomes originais".  
4. Digite os novos nomes no campo "Novos nomes".  
5. Clique em "Renomear arquivos".  

NOTA: O arquivo cujo nome original está na linha "1" do campo "Nomes originais" será renomeado para o nome que está na linha "1" do campo "Novos nomes", e assim por diante.

---

### 🛠️ Funcionalidades

- 📁 Seleção da pasta com os arquivos a serem renomeados  
- ✍️ Campos para nomes originais e novos nomes (com numeração de linhas)  
- 🔁 Botão para desfazer a renomeação mais recente  
- 🧼 Remoção automática de caracteres inválidos para nomes de arquivo  
- 🌙 Alternância entre modo claro e escuro (a opção é salva para sessões futuras)  
- 🌐 Suporte para dois idiomas: português e inglês (a opção é salva para sessões futuras)  
- 🔤 Adição rápida de extensões populares a nomes de arquivo (.jpg, .pdf, .mp3, etc.)  
- 🧠 Interface responsiva e intuitiva com `Qt6`.

---

### 📦 Requisitos (para executar a partir do código-fonte)

Se preferir executar o projeto diretamente do código Python, sem usar o executável `.exe` ou `.appimage`, você precisará:

No Linux Mint 22.2:

Pacotes "apt install": python3 python3-pip python3-tk build-essential python3.12-venv patchelf ccache  
Pacotes "pip install": PyQt6 pyinstaller nuitka

Em Windows (usando o código-fonte da versão 1.0):

- Python 3.13 ou superior  
- Bibliotecas:  
  - `customtkinter`  
  - `tkinter`  
  - `json`, `os`, `sys`

---

### 📄 Licença

Distribuído sob a [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). Você pode usar, modificar e redistribuir este software livremente, desde que mantenha os avisos de atribuição e licença.

---

### 👤 Autor

**Jedielson da Fonseca**

📧 [jdfn7@proton.me](mailto:jdfn7@proton.me)
