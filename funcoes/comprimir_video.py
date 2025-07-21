import os
import ffmpeg
import re
from tqdm import tqdm
from datetime import datetime


def comprimir_video(objeto):
	"""Comprime um vídeo para uma resolução menor com barra de progresso."""
	objeto.limpar_tela()
	print("== COMPRIMIR VÍDEO ==")

	arquivos_video = objeto.listar_videos()
	if not arquivos_video:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	arquivo_selecionado = objeto.selecionar_arquivo(arquivos_video)
	if not arquivo_selecionado:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	print("\nSelecione a resolução de saída:")
	print("[1] 1080p")
	print("[2] 720p")
	print("[3] 480p")
	print("[4] 320p")
	print("[5] 144p")

	resolucoes = {1: 1080, 2: 720, 3: 480, 4: 320, 5: 144}

	try:
		escolha_str = input("\nEscolha uma opção de resolução: ")
		if not escolha_str.isdigit():
			print("Entrada inválida! Por favor, insira um número.")
			return

		escolha = int(escolha_str)
		if escolha not in resolucoes:
			print("Opção de resolução inválida!")
			return

		altura = resolucoes[escolha]
		nome_base, extensao = os.path.splitext(os.path.basename(arquivo_selecionado))
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		arquivo_saida = os.path.join(objeto.diretorio_atual, f"{nome_base}_{altura}p_{timestamp}{extensao}")

		print(f"\nAnalisando vídeo de entrada...")
		probe = ffmpeg.probe(arquivo_selecionado)
		total_duration = float(probe['format']['duration'])

		print(f"Comprimindo vídeo {os.path.basename(arquivo_selecionado)} para {altura}p...")

		# Configura o processo ffmpeg
		process = (
			ffmpeg
			.input(arquivo_selecionado)
			.output(arquivo_saida, vf=f'scale=-2:{altura}', vcodec='libx264', crf=23, acodec='aac', audio_bitrate='128k')
			.global_args('-progress', 'pipe:2', '-y') # -y para sobrescrever, -progress para stderr
			.run_async(pipe_stdout=True, pipe_stderr=True)
		)

		# Regex para encontrar 'time=HH:MM:SS.ms' na saída do ffmpeg
		time_re = re.compile(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})")

		with tqdm(total=round(total_duration), unit='s', desc="Progresso da Compressão") as pbar:
			while True:
				# Lê a saída de erro do ffmpeg linha por linha
				line = process.stderr.readline().decode('utf-8', errors='ignore')
				if not line and process.poll() is not None:
					break
				
				match = time_re.search(line)
				if match:
					h, m, s, ms = map(int, match.groups())
					current_time = h * 3600 + m * 60 + s + ms / 100
					pbar.update(current_time - pbar.n) # pbar.n é a posição atual

		process.wait() # Espera o processo terminar
		pbar.close()

		print(f"\nVídeo comprimido com sucesso! Salvo como: {os.path.basename(arquivo_saida)}")

	except ffmpeg.Error as e:
		print(f"\nOcorreu um erro durante a compressão com o ffmpeg.")
		print(f"Erro: {e.stderr.decode(errors='ignore') if e.stderr else 'Nenhuma saída de erro.'}")
	except ValueError:
		print("Entrada inválida! Por favor, insira um número.")
	except Exception as e:
		print(f"\nOcorreu um erro inesperado ao comprimir o vídeo: {e}")

	if input("\nDeseja comprimir outro vídeo? (s/n): ").lower() == 's':
		objeto.comprimir_video()
