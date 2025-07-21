#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

# --- Configurações ---
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
MAIN_SCRIPT = "completo.py"

def get_executable_paths(venv_path):
    """Retorna os caminhos corretos para os executáveis Python e Pip no venv."""
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else: # Linux, macOS, etc.
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    return str(python_exe), str(pip_exe)

def create_virtual_env(venv_path):
    """Cria um ambiente virtual."""
    print(f"Criando ambiente virtual em '{venv_path}'...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("Ambiente virtual criado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao criar o ambiente virtual. {e}")
        print("Verifique se o seu Python tem o pacote 'venv' instalado (geralmente python3-venv em sistemas Linux).")
        sys.exit(1)

def install_requirements(pip_exe, requirements_path):
    """Instala os pacotes de um arquivo requirements.txt."""
    print(f"Instalando dependências de '{requirements_path}' (isso pode levar alguns minutos)...")
    try:
        command = [pip_exe, "install", "--disable-pip-version-check", "-q", "-r", requirements_path]
        subprocess.run(command, check=True)
        print("Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao instalar as dependências. {e}")
        sys.exit(1)

def main():
    """Função principal que gerencia o ambiente e executa o script."""
    print("--- Lançador do Editor de Vídeo ---")
    venv_path = Path(VENV_DIR)

    if not Path(REQUIREMENTS_FILE).exists():
        print(f"ERRO: Arquivo de dependências '{REQUIREMENTS_FILE}' não encontrado.")
        sys.exit(1)

    # 1. Verifica se o ambiente virtual existe
    if not venv_path.is_dir():
        create_virtual_env(venv_path)
        _, pip_exe = get_executable_paths(venv_path)
        install_requirements(pip_exe, REQUIREMENTS_FILE)
    else:
        print(f"Ambiente virtual '{VENV_DIR}' encontrado.")
        # Garante que as dependências estão instaladas/atualizadas a cada execução
        _, pip_exe = get_executable_paths(venv_path)
        install_requirements(pip_exe, REQUIREMENTS_FILE)

    # 2. Executa o script principal usando o Python do ambiente virtual
    python_exe, _ = get_executable_paths(venv_path)
    
    if not Path(python_exe).exists():
        print(f"ERRO: O executável Python não foi encontrado em '{python_exe}'.")
        print("Tente apagar a pasta 'venv' e executar novamente.")
        sys.exit(1)
        
    if not Path(MAIN_SCRIPT).exists():
        print(f"ERRO: O script principal '{MAIN_SCRIPT}' não foi encontrado neste diretório.")
        sys.exit(1)

    print(f"\nIniciando o programa principal '{MAIN_SCRIPT}'...")
    print("="*40)
    
    try:
        subprocess.run([python_exe, MAIN_SCRIPT])
    except Exception as e:
        print(f"\nERRO ao executar o script principal: {e}")

    print("="*40)
    print("Programa finalizado.")


if __name__ == "__main__":
    main()
