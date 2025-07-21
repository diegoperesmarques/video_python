# Editor de Vídeo e Utilitário de Mídia com IA

Este é um conjunto de ferramentas de linha de comando em Python para automação de tarefas de edição de vídeo, transcrição de áudio, legendagem e resumo de textos com inteligência artificial.

## Descrição

O projeto consiste em um script principal (`completo.py`) que oferece um menu interativo para executar diversas funções de manipulação de vídeo e áudio. [cite_start]Ele utiliza bibliotecas como `ffmpeg-python` para processamento de mídia, `openai-whisper` para transcrições de alta qualidade [cite: 1] [cite_start]e a API do `google-generativeai` para funcionalidades de resumo inteligente[cite: 1].

[cite_start]Para facilitar a instalação e o gerenciamento de dependências, o projeto inclui um script de inicialização (`iniciar.py`) que cria um ambiente virtual isolado [cite: 1] [cite_start]e instala todas as bibliotecas necessárias[cite: 1].

## Funcionalidades

O script oferece as seguintes opções:

* **Extrair Áudio de Vídeo**: Separa a faixa de áudio de um arquivo de vídeo e a salva como um arquivo MP3.
* **Criar Legendas (SRT)**: Transcreve o áudio de um vídeo e gera um arquivo de legenda no formato `.srt`, com sincronização de tempo.
* **Fazer Transcrição de Áudio/Vídeo**: Gera um arquivo de texto (`.txt`) com a transcrição completa do conteúdo falado no arquivo de mídia.
* **Cortar Vídeo**: Permite cortar um trecho específico de um vídeo informando o tempo de início e fim.
* **Juntar Múltiplos Vídeos**: Combina vários arquivos de vídeo (do mesmo formato) em um único arquivo.
* **Resumir Transcrição de Reunião (IA)**: Utiliza a API do Google Gemini para ler um arquivo de transcrição `.txt` e gerar um resumo estruturado.
* **Comprimir Vídeo**: Reduz o tamanho de um arquivo de vídeo, útil para compartilhamento e armazenamento.
* **Baixar Vídeo do YouTube**: Faz o download de um vídeo do YouTube a partir de sua URL.

## Requisitos

[cite_start]O projeto utiliza as seguintes bibliotecas Python[cite: 1]:

* [cite_start]`ffmpeg-python` [cite: 1]
* [cite_start]`openai-whisper` [cite: 1]
* [cite_start]`google-generativeai` [cite: 1]
* [cite_start]`tqdm` [cite: 1]
* [cite_start]`yt-dlp` [cite: 1]
* [cite_start]`googletrans==4.0.0-rc1` [cite: 1]

Além das bibliotecas, é **necessário ter o [FFmpeg](https://ffmpeg.org/download.html) instalado** no sistema e acessível pelo `PATH` do sistema operacional.

## Como Usar

1.  **Clone ou baixe os arquivos do projeto** para um diretório em seu computador.

2.  **(Opcional, mas recomendado)** Para a funcionalidade de resumo com IA, você precisará de uma chave de API do Google AI Studio.
    * Crie sua chave no [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Configure a chave como uma variável de ambiente no seu sistema com o nome `GOOGLE_API_KEY`.
        * **No Windows (temporário):**
            ```bash
            set GOOGLE_API_KEY="SUA_CHAVE_API_AQUI"
            ```
        * **No Linux/macOS (temporário):**
            ```bash
            export GOOGLE_API_KEY="SUA_CHAVE_API_AQUI"
            ```
    * Para uma configuração permanente, adicione o comando acima ao seu perfil de shell (`.bashrc`, `.zshrc`) ou configure nas variáveis de ambiente do sistema.

3.  **Execute o script de inicialização**. Este script irá automaticamente:
    * [cite_start]Verificar se o Python e o módulo `venv` estão disponíveis. [cite: 1]
    * [cite_start]Criar um ambiente virtual na pasta `venv/`. [cite: 1]
    * [cite_start]Instalar todas as dependências listadas em `requirements.txt` dentro deste ambiente. [cite: 1]
    * [cite_start]Iniciar o programa principal (`completo.py`). [cite: 1]

    Execute o seguinte comando no seu terminal:
    ```bash
    python3 iniciar.py
    ```
    Ou, se `python` for o seu interpretador Python 3:
    ```bash
    python iniciar.py
    ```

4.  **Navegue pelo menu**. Após a inicialização, um menu interativo será exibido no terminal. Digite o número da opção desejada e pressione `Enter` para executá-la. Siga as instruções na tela para selecionar arquivos e fornecer as informações necessárias.

## Estrutura do Projeto

* [cite_start]`iniciar.py`: Script de bootstrap para configurar o ambiente e iniciar a aplicação. [cite: 1]
* `completo.py`: O coração da aplicação, contém a lógica principal, o menu e a orquestração das diferentes funcionalidades.
* [cite_start]`requirements.txt`: Lista de todas as dependências Python do projeto. [cite: 1]
* `funcoes/`: (Estrutura inferida a partir dos `imports` em `completo.py`) Recomenda-se que as funções individuais (como `listar_videos`, `cortar_video`, etc.) sejam organizadas neste diretório para manter o código principal mais limpo.
