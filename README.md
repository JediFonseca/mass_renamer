# 🗂️ Mass Renamer 2.1

This software was created for **recreational and experimental purposes**. It is being made available as **free** and **open-source**. If it helps you in any way, make good use of it. Feel free to contribute, adapt, or share! I am not a developer, I don't work in the field, and I don't have in-depth knowledge of any programming language. The development of this software was done **for fun and as a hobby** with the **assistance of AI** (**Vibe Coding**).

Download: [**Releases**](https://github.com/JediFonseca/mass_renamer/releases)

**Mass Renamer** is a Linux application developed in Python with a `Qt6` interface, which allows you to rename multiple files quickly, safely, and in an organized manner. It supports undoing the most recent renaming, adding extensions to filenames and a multilingual interface (🇧🇷 Portuguese and 🇺🇸 English).

<img width="910" height="692" alt="Captura de tela de 2025-09-10 17-01-50" src="https://github.com/user-attachments/assets/a90e3627-3cd6-45b7-b678-f88ee62c9f01" />

<img width="909" height="691" alt="Captura de tela de 2025-09-10 17-02-05" src="https://github.com/user-attachments/assets/8fdb072c-fb45-42e1-824f-f75bc556a485" />

---

### 🚀 Installation and usage

Mass Renamer is made available in AppImage, which can run, theoretically, on any Linux distro.
On Ubuntu you may need to install the `libfuse2t64` package:
```
sudo apt install libfuse2t64
```
1. Run the ".appimage".
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

If you prefer to run the project directly from the Python code, without using the `.appimage` executable, you will need:

On Linux Mint 22.2:

"apt install" packages: python3 python3-pip python3-tk build-essential python3.12-venv patchelf ccache

"pip install" packages: PyQt6 pyinstaller nuitka

### 📄 License

Distributed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). You can use, modify, and redistribute this software freely, as long as you maintain the attribution and license notices.

---

### 👤 Author

**Jedielson da Fonseca**

📧 [jdfn7@proton.me](mailto:jdfn7@proton.me)

