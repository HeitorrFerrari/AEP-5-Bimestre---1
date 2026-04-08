import ctypes
import os
import sys


class Cores:
	RESET = "\033[0m"
	BOLD = "\033[1m"
	CYAN = "\033[36m"
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