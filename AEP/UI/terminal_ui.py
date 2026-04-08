import ctypes
import os
import sys
from datetime import datetime


class Cores:
	RESET = "\033[0m"
	BOLD = "\033[1m"
	CYAN = "\033[36m"
	BLUE = "\033[34m"
	GREEN = "\033[32m"
	YELLOW = "\033[33m"
	RED = "\033[31m"
	GRAY = "\033[90m"


def habilitar_ansi() -> None:
	if os.name != "nt":
		return

	try:
		handle = ctypes.windll.kernel32.GetStdHandle(-11)
		mode = ctypes.c_uint32()
		if ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
			ctypes.windll.kernel32.SetConsoleMode(handle, mode.value | 0x0004)
	except Exception:
		# Mantem funcionamento mesmo sem suporte a ANSI.
		pass


def _usa_cores() -> bool:
	return sys.stdout.isatty() and os.getenv("NO_COLOR") is None


def colorir(texto: str, cor: str) -> str:
	if not _usa_cores():
		return texto
	return f"{cor}{texto}{Cores.RESET}"


def titulo(texto: str) -> None:
	barra = "=" * 52
	print(f"\n{colorir(barra, Cores.GRAY)}")
	print(colorir(texto.upper(), Cores.BOLD + Cores.CYAN))
	print(colorir(barra, Cores.GRAY))


def limpar_tela() -> None:
	os.system("cls" if os.name == "nt" else "clear")


def _quadro(linhas: list[str], largura: int = 64) -> None:
	topo = "+" + ("-" * (largura - 2)) + "+"
	print(colorir(topo, Cores.GRAY))
	for linha in linhas:
		conteudo = linha[: largura - 4]
		print(colorir(f"| {conteudo:<{largura - 4}} |", Cores.GRAY))
	print(colorir(topo, Cores.GRAY))


def tela_inicial() -> None:
	data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
	banner = [
		" ______  _____   ____   ______  _______ ",
		"|  ____|/ ____| / __ \ |  ____||__   __|",
		"| |__  | (___  | |  | || |__      | |   ",
		"|  __|  \___ \ | |  | ||  __|     | |   ",
		"| |____ ____) || |__| || |        | |   ",
		"|______|_____/  \____/ |_|        |_|   ",
	]

	limpar_tela()
	print()
	for linha in banner:
		print(colorir(linha, Cores.BOLD + Cores.BLUE))
	print(colorir("  Sistema de Solicitacoes Urbanas", Cores.BOLD + Cores.CYAN))
	print(colorir("  Atendimento digital da cidade", Cores.GRAY))
	print()
	_quadro(
		[
			"Bem-vindo(a)!",
			"Gerencie demandas com rapidez e transparencia.",
			f"Sessao iniciada em: {data_hora}",
		],
	)
	print()


def menu_opcoes(opcoes: list[str]) -> None:
	for opcao in opcoes:
		print(colorir(f"  {opcao}", Cores.CYAN))


def info(texto: str) -> None:
	print(colorir(f"[INFO] {texto}", Cores.GRAY))


def sucesso(texto: str) -> None:
	print(colorir(f"[OK] {texto}", Cores.GREEN))


def alerta(texto: str) -> None:
	print(colorir(f"[ALERTA] {texto}", Cores.YELLOW))


def erro(texto: str) -> None:
	print(colorir(f"[ERRO] {texto}", Cores.RED))


def ler_opcao(rotulo: str = "Escolha") -> str:
	return input(colorir(f"{rotulo}: ", Cores.BOLD)).strip()


def selecionar_indice(quantidade: int, permite_zero: bool = False) -> int:
	while True:
		escolha = ler_opcao()
		if permite_zero and escolha == "0":
			return 0
		if escolha.isdigit():
			indice = int(escolha)
			if 1 <= indice <= quantidade:
				return indice
		alerta("Opcao invalida. Tente novamente.")