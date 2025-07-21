def exibir_menu_principal(self):
	self.limpar_tela()
	print("=" * 50)
	print("      EDITOR DE VÍDEO - LINHA DE COMANDO      ")
	print("=" * 50)
	print("[1] Extrair áudio")
	print("[2] Criar legenda")
	print("[3] Fazer transcrição")
	print("[4] Cortar vídeo")
	print("[5] Juntar vídeos")
	print("[6] Resumir Transcrição de Reunião (IA)")
	print("[7] Comprimir vídeo")
	print("[8] Download video youtube")
	print("[0] Sair")
	print("=" * 50)

	try:
		opcao = int(input("Escolha uma opção: "))
		return opcao
	except ValueError:
		print("Opção inválida! Tente novamente.")
		time.sleep(1)
		return -1
