import os
import ffmpeg

def criar_legenda(objeto):
	"""Cria um arquivo de legenda SRT para um vídeo usando o Whisper"""
	objeto.limpar_tela()
	print("== CRIAR LEGENDA ==")

	if objeto.model is None:
		print("Modelo Whisper não está carregado. Tentando carregar...")
		objeto.carregar_whisper()
		if objeto.model is None:
			print("Não foi possível carregar o modelo Whisper.")
			input("Pressione ENTER para voltar ao menu principal...")
			return

	arquivos_video = objeto.listar_videos()
	if not arquivos_video:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	arquivo_selecionado = objeto.selecionar_arquivo(arquivos_video)
	if not arquivo_selecionado:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	nome_base = os.path.splitext(os.path.basename(arquivo_selecionado))[0]
	arquivo_audio_temp = os.path.join(objeto.diretorio_atual, f"{nome_base}_temp_audio_for_srt.mp3")
	arquivo_srt = os.path.join(objeto.diretorio_atual, f"{nome_base}.srt")

	try:
		print(f"\nProcessando vídeo {os.path.basename(arquivo_selecionado)}...")
		print("Extraindo áudio temporário...")
		ffmpeg.input(arquivo_selecionado).output(arquivo_audio_temp, acodec='libmp3lame', q=4).run(quiet=True, overwrite_output=True)

		print("Transcrevendo áudio com Whisper (isso pode demorar um pouco)...")
		resultado = objeto.model.transcribe(arquivo_audio_temp, fp16=False)

		with open(arquivo_srt, 'w', encoding='utf-8') as f:
			i = 1
			for segment in resultado["segments"]:
				start_time = objeto._formatar_tempo_srt(segment['start'])
				end_time = objeto._formatar_tempo_srt(segment['end'])
				texto = segment['text'].strip()
				f.write(f"{i}\n{start_time} --> {end_time}\n{texto}\n\n")
				i += 1
		
		print(f"Legenda criada com sucesso! Salva como: {os.path.basename(arquivo_srt)}")
	except Exception as e:
		print(f"Erro ao criar legenda: {e}")
	finally:
		if os.path.exists(arquivo_audio_temp):
			os.remove(arquivo_audio_temp)

	if input("\nDeseja criar legenda para outro vídeo? (s/n): ").lower() == 's':
		objeto.criar_legenda()
