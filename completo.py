#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import subprocess
import time
from pathlib import Path
import whisper
import ffmpeg
from datetime import datetime
import google.generativeai as genai
import re # Adicionado para a barra de progresso
from tqdm import tqdm # Adicionado para a barra de progresso

# Importação das funções
from funcoes.listar_videos import listar_videos
from funcoes.exibir_menu_principal import exibir_menu_principal
from funcoes.fazer_transcricao import fazer_transcricao
from funcoes.extrair_audio import extrair_audio
from funcoes.criar_legenda import criar_legenda
from funcoes.cortar_video import cortar_video
from funcoes.juntar_videos import juntar_videos
from funcoes.comprimir_video import comprimir_video
from funcoes.download_video_youtube import download_video_youtube


# --- Configuração para Resumo de Reunião ---
NOME_ARQUIVO_RESULTADO_REUNIAO = "resultado_reuniao.txt"
MODELO_GEMINI_REUNIAO = "gemini-1.5-flash-latest"

# Tenta carregar a chave API da variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("AVISO: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    print("A função 'Resumir Transcrição de Reunião' não funcionará.")
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("Google AI SDK configurado com sucesso.")
    except Exception as e:
        print(f"Erro ao configurar Google AI SDK: {e}")
        print("A função 'Resumir Transcrição de Reunião' pode não funcionar.")
        GOOGLE_API_KEY = None


class EditorVideo:
    def __init__(self):
        self.diretorio_atual = os.getcwd()
        self.model = None
        self.carregar_whisper()
        

    def carregar_whisper(self):
        """Carrega o modelo whisper para transcrição de áudio"""
        try:
            print("Carregando modelo Whisper... (pode demorar na primeira execução)")
            self.model = whisper.load_model("base")
            print("Modelo Whisper carregado com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar o modelo Whisper: {e}")
            print("As funções de legendas e transcrição podem não funcionar corretamente.")


    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def exibir_menu_principal(self): 
        return exibir_menu_principal(self)


    def listar_videos(self):
        return listar_videos(self.diretorio_atual)        


    def selecionar_arquivo(self, arquivos, tipo_arquivo="vídeo"):
        """Permite ao usuário selecionar um arquivo da lista"""
        if not arquivos:
            return None

        try:
            indice = int(input(f"\nSelecione o número do arquivo de {tipo_arquivo}: ")) - 1
            if 0 <= indice < len(arquivos):
                return arquivos[indice]
            else:
                print("Índice inválido! Tente novamente.")
                return None
        except ValueError:
            print("Entrada inválida! Tente novamente.")
            return None


    def extrair_audio(self):
        return extrair_audio(self)


    def criar_legenda(self):
        return criar_legenda(self)


    def _formatar_tempo_srt(self, segundos):
        """Converte segundos para o formato de tempo SRT (HH:MM:SS,MS)"""
        horas = int(segundos / 3600)
        minutos = int((segundos % 3600) / 60)
        segundos_rest = segundos % 60
        milissegundos = int((segundos_rest - int(segundos_rest)) * 1000)
        return f"{horas:02d}:{minutos:02d}:{int(segundos_rest):02d},{milissegundos:03d}"


    def fazer_transcricao(self):
        return fazer_transcricao(self)


    def cortar_video(self): 
        return cortar_video(self)


    def juntar_videos(self): 
        return juntar_videos(self)


    def comprimir_video(self):
        return comprimir_video(self)


    def download_video_youtube(self): 
        return download_video_youtube(self)


    # ... (cole aqui o resto das suas funções de resumo de reunião e a função executar) ...
    def _encontrar_arquivos_txt_reuniao(self):
        """Encontra todos os arquivos .txt no diretório atual."""
        diretorio_path = Path(self.diretorio_atual)
        arquivos_txt = list(diretorio_path.glob("*.txt"))
        # Exclui o próprio arquivo de resultado para não ser listado como opção
        arquivos_txt = [f for f in arquivos_txt if f.name != NOME_ARQUIVO_RESULTADO_REUNIAO]
        return arquivos_txt

    def _selecionar_arquivo_txt_reuniao(self, arquivos_encontrados):
        """Permite ao usuário selecionar um arquivo .txt de uma lista."""
        if not arquivos_encontrados:
            print("Nenhum arquivo .txt encontrado na pasta atual.")
            return None

        print("\nArquivos .txt disponíveis para resumo:")
        for i, arquivo in enumerate(arquivos_encontrados):
            print(f"[{i + 1}] {arquivo.name}")

        while True:
            try:
                escolha = int(input("Digite o número do arquivo .txt que deseja usar: "))
                if 1 <= escolha <= len(arquivos_encontrados):
                    return arquivos_encontrados[escolha - 1]
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        return None

    def _confirmar_arquivo_reuniao(self, caminho_arquivo):
        """Pergunta ao usuário se o arquivo selecionado é o correto."""
        if not caminho_arquivo:
            return False
        resposta = input(f"Você confirma o uso do arquivo '{caminho_arquivo.name}' para resumo? (s/n): ").strip().lower()
        return resposta == 's'

    def _ler_conteudo_arquivo_reuniao(self, caminho_arquivo):
        """Lê o conteúdo de um arquivo de texto."""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao ler o arquivo {caminho_arquivo.name}: {e}")
            return None

    def _enviar_para_google_ai_reuniao(self, texto_transcricao):
        """Envia o texto para o Google AI Studio e retorna a resposta."""
        prompt = f"""Abaixo está a transcrição de uma reunião, você deve extrair o seguinte:

1) Participantes da reunião;
2) Estrutura atual do Hospital/CME (se mencionado);
3) Considerações finais da reunião e próximos passos.

## Requisitos
O resultado deve vir no formato de Markdown com cada um dos tópicos anteriores em títulos (H2 ou H3).

## Transcrição da Reunião:
---
{texto_transcricao}
---
"""
        try:
            print(f"\nEnviando para o Google AI (modelo: {MODELO_GEMINI_REUNIAO})... Aguarde...")
            model = genai.GenerativeModel(MODELO_GEMINI_REUNIAO)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro ao comunicar com o Google AI: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Detalhes do erro da API: {e.response.text}")
            elif hasattr(e, 'message'):
                print(f"Detalhes: {e.message}")
            return None

    def _salvar_resultado_reuniao(self, conteudo):
        """Salva o conteúdo no arquivo de resultado, apagando o anterior se existir."""
        caminho_resultado = Path(self.diretorio_atual) / NOME_ARQUIVO_RESULTADO_REUNIAO
        try:
            with open(caminho_resultado, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            print(f"\nResultado salvo com sucesso em '{NOME_ARQUIVO_RESULTADO_REUNIAO}'")
        except Exception as e:
            print(f"Erro ao salvar o arquivo de resultado: {e}")

    def resumir_reuniao_transcrita(self):
        """Processa uma transcrição de reunião usando Google AI."""
        self.limpar_tela()
        print("== RESUMIR TRANSCRIÇÃO DE REUNIÃO (IA) ==")

        if not GOOGLE_API_KEY:
            print("ERRO: A chave API do Google não está configurada ou falhou ao configurar.")
            print("Esta função não pode continuar.")
            input("Pressione ENTER para voltar ao menu principal...")
            return

        arquivos_txt_encontrados = self._encontrar_arquivos_txt_reuniao()

        if not arquivos_txt_encontrados:
            print("Nenhum arquivo .txt de transcrição encontrado na pasta atual.")
            input("Pressione ENTER para voltar ao menu principal...")
            return

        arquivo_selecionado = None
        if len(arquivos_txt_encontrados) == 1:
            arquivo_selecionado = arquivos_txt_encontrados[0]
            print(f"Arquivo de transcrição encontrado: {arquivo_selecionado.name}")
        else:
            arquivo_selecionado = self._selecionar_arquivo_txt_reuniao(arquivos_txt_encontrados)

        if not arquivo_selecionado:
            print("Nenhum arquivo selecionado.")
            input("Pressione ENTER para voltar ao menu principal...")
            return

        if not self._confirmar_arquivo_reuniao(arquivo_selecionado):
            print("Operação cancelada pelo usuário.")
            input("Pressione ENTER para voltar ao menu principal...")
            return

        print(f"Utilizando o arquivo: {arquivo_selecionado.name}")

        conteudo_transcricao = self._ler_conteudo_arquivo_reuniao(arquivo_selecionado)
        if conteudo_transcricao is None:
            input("Pressione ENTER para voltar ao menu principal...")
            return

        resultado_ia = self._enviar_para_google_ai_reuniao(conteudo_transcricao)

        if resultado_ia:
            print("\n--- Resposta do Google AI ---")
            print(resultado_ia)
            print("---------------------------------")
            self._salvar_resultado_reuniao(resultado_ia)
        else:
            print("Não foi possível obter uma resposta do Google AI.")
        
    def executar(self):
        """Executa o programa principal"""
        while True:
            opcao = self.exibir_menu_principal()

            if opcao == 0:
                break
            elif opcao == 1:
                self.extrair_audio()
            elif opcao == 2:
                self.criar_legenda()
            elif opcao == 3:
                self.fazer_transcricao()
            elif opcao == 4:
                self.cortar_video()
            elif opcao == 5:
                self.juntar_videos()
            elif opcao == 6:
                self.resumir_reuniao_transcrita()
            elif opcao == 7:
                self.comprimir_video()
            elif opcao == 8: 
                self.download_video_youtube()
            else:
                print("Opção inválida! Pressione ENTER para tentar novamente.")
            
            if opcao != -1: 
                input("\nPressione ENTER para voltar ao menu principal...")

if __name__ == "__main__":
    editor = EditorVideo()
    editor.executar()
