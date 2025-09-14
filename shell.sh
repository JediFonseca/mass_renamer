#!/bin/bash

# Abre uma nova janela de terminal para executar o script, se ainda não estiver em uma.
if [ -z "$GNOME_TERMINAL_SCREEN" ]; then
    gnome-terminal -- /bin/bash -c "cd '$PWD' && ./'$0' && read -p 'Pressione Enter para fechar...'"
    exit 0
fi

# Limpa a tela para uma melhor visualização.
clear

# Exibe o cabeçalho e a pergunta de confirmação.
echo "---------------------------------------------------------------------"
echo "  Instalação de Pacotes: gnome-software, flatpak e plugins"
echo "---------------------------------------------------------------------"
echo
echo "Este script irá instalar os seguintes pacotes no seu sistema:"
echo "  - gnome-software"
echo "  - flatpak"
echo "  - gnome-software-plugin-flatpak"
echo
read -p "Pressione Enter para continuar ou Ctrl+C para cancelar..."

# Atualiza a lista de pacotes.
echo
echo "--> Atualizando a lista de pacotes (apt update)..."
sudo apt update
echo

# Simulação (Dry Run) da instalação.
echo "--> Iniciando simulação (dry run) para verificar por erros..."
if sudo apt install --dry-run gnome-software flatpak gnome-software-plugin-flatpak; then
    echo
    echo "----------------------------------------"
    echo "  Simulação concluída com sucesso!"
    echo "----------------------------------------"
    echo
    echo "--> Iniciando a instalação real dos pacotes..."
    echo

    # Instalação real dos pacotes.
    if sudo apt install -y gnome-software flatpak gnome-software-plugin-flatpak; then
        echo
        echo "---------------------------------------------"
        echo "  Instalação concluída com sucesso!"
        echo "---------------------------------------------"
    else
        echo
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "  Ocorreu um erro durante a instalação dos pacotes."
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    fi
else
    echo
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "  A simulação (dry run) falhou. Verifique os erros acima."
    echo "  Nenhuma alteração foi feita no sistema."
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
