from Models.usuario import Cargo, Usuario
from Services.servico_solicitacoes import ServicoSolicitacoes
from UI.menu_atendente import menu_atendente
from UI.menu_cidadao import menu_cidadao
from UI.terminal_ui import alerta, habilitar_ansi, ler_opcao, menu_opcoes, tela_inicial, titulo


def main():
	habilitar_ansi()
	tela_inicial()
	servico = ServicoSolicitacoes()
	atendente = Usuario(
		nome="Atendente Padrao",
		documento="00000000000",
		cargo=Cargo.FUNCIONARIO_PUBLICO,
	)

	while True:
		titulo("Sistema de Solicitacoes Urbanas")
		menu_opcoes([
			"1. Area do cidadao",
			"2. Area do atendente/gestor",
			"0. Sair",
		])
		opcao = ler_opcao()

		if opcao == "1":
			menu_cidadao(servico)
		elif opcao == "2":
			menu_atendente(servico, atendente)
		elif opcao == "0":
			print("Encerrando sistema.")
			break
		else:
			alerta("Opcao invalida.")


if __name__ == "__main__":
	main()
