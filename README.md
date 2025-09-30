# 🗂️ Mass Renamer 2.3

**Mass Renamer** is a Linux application developed in Python with a `Qt6` interface, which allows you to rename multiple files quickly, safely, and in an organized manner. It supports undoing the most recent renaming even if the app was closed or crashed, adding extensions to filenames, protection from accidental file or folder overscription and a multilingual interface (🇧🇷 Portuguese and 🇺🇸 English).

[**Download the AppImage**](https://github.com/JediFonseca/mass_renamer/releases)

**Version 2.3 tested on:**  
✅ Fedora 42 (GNOME);  
✅ openSUSE Leap 15.6 (KDE Plasma);  
✅ openSUSE Tumbleweed (GNOME);  
✅ Pop!_OS 22.04;  
✅ Linux Mint 22.2 (Cinnamon);  
✅ Ubuntu 24.04;  
✅ Ubuntu 22.04;  
✅ Manjaro (XFCE);  
✅ Lubuntu 24.04;  
✅ Lubuntu 25.04;  
✅ Ubuntu Budgie 24.04;  
✅ Zorin OS 17.3;  
✅ Debian 13 (MATE);  
✅ Debian 12 (GNOME).  

**IMPORTANT:** This software was created for **recreational and experimental purposes**. It is being made available as **free** and **open-source**. If it helps you in any way, make good use of it. Feel free to contribute, adapt, or share! I am not a developer, I don't work in the field, and I don't have in-depth knowledge of any programming language. The development of this software was done **for fun and as a hobby** with the **assistance of AI** (**Vibe Coding**).

<img width="911" height="695" alt="img01" src="https://github.com/user-attachments/assets/64c958b6-09a1-44d0-b306-3e0bbe5f054d" />

<img width="904" height="685" alt="img02" src="https://github.com/user-attachments/assets/bacf2549-6c36-4aac-b68e-b34951666ca6" />

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
5. Click on "Rename".

NOTE: The file whose original name is on line "1" of the "Original names" field will be renamed to the name that is on line "1" of the "New names" field, and so on.

---

### 🛠️ Features

- 📁 Selection of the folder with the files to be renamed;
- ✍️ Fields for original names and new names (with line numbering);
- 📝 Persistent history files for renaming and undoing;
- 🛡️ Protection from accidental file or folder overscription;
- 🔁 Button to undo the most recent renaming;
- 🧼 Automatic removal of invalid characters for filenames, with the option to disable/enable it based on different operating systems;
- 🌙 Toggle between 10 different themes, including popular ones like Adwaita and Breeze (Both on their light and dark variants). The theme is saved for future sessions.;
- 🌐 Support for two languages: Portuguese and English (the option is saved for future sessions);
- 🔤 Quick addition of ANY extensions to filenames;
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




























