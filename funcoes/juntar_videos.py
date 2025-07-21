import os
import ffmpeg
import subprocess
from datetime import datetime


def juntar_videos(objeto):
	"""Junta múltiplos vídeos em um único arquivo"""
	objeto.limpar_tela()
	print("== JUNTAR VÍDEOS ==")

	arquivos_video = objeto.listar_videos()
	if not arquivos_video:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	arquivos_selecionados = []
	print("\nSelecione os vídeos para juntar (digite 0 para finalizar a seleção):")

	while True:
		try:
			indice = int(input("\nNúmero do arquivo (0 para finalizar): "))
			if indice == 0:
				break
			if 1 <= indice <= len(arquivos_video):
				arquivo = arquivos_video[indice-1]
				if arquivo in arquivos_selecionados:
					print("Este arquivo já foi selecionado.")
				else:
					arquivos_selecionados.append(arquivo)
					print(f"Adicionado: {os.path.basename(arquivo)}")
			else:
				print("Índice inválido! Tente novamente.")
		except ValueError:
			print("Entrada inválida! Tente novamente.")

	if len(arquivos_selecionados) < 2:
		print("\nÉ necessário selecionar pelo menos 2 arquivos para juntar.")
		input("Pressione ENTER para voltar ao menu principal...")
		return

	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	nome_saida = f"video_unido_{timestamp}.mp4"
	arquivo_saida = os.path.join(objeto.diretorio_atual, nome_saida)
	arquivo_lista = os.path.join(objeto.diretorio_atual, "lista_temp_ffmpeg_concat.txt")

	try:
		print("\nPreparando para juntar os vídeos...")
		with open(arquivo_lista, 'w', encoding='utf-8') as f:
			for arquivo in arquivos_selecionados:
				f.write(f"file '{os.path.abspath(arquivo)}'\n")
		
		cmd = [
			'ffmpeg', '-y', 
			'-f', 'concat',
			'-safe', '0', 
			'-i', arquivo_lista,
			'-c', 'copy',
			arquivo_saida
		]

		print("Juntando vídeos (isso pode demorar dependendo do tamanho dos arquivos)...")
		subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print(f"Vídeos unidos com sucesso! Salvo como: {os.path.basename(arquivo_saida)}")
	except subprocess.CalledProcessError as e:
		print(f"Erro ao juntar vídeos (ffmpeg): {e}")
		print(f"Comando: {' '.join(e.cmd)}")
		print(f"Stdout: {e.stdout.decode(errors='ignore')}")
		print(f"Stderr: {e.stderr.decode(errors='ignore')}")
	except Exception as e:
		print(f"Erro ao juntar vídeos: {e}")
	finally:
		if os.path.exists(arquivo_lista):
			os.remove(arquivo_lista)
