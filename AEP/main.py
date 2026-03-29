from Models.usuario import Cargo, Usuario
from Services.servico_solicitacoes import ServicoSolicitacoes
from UI.menu_atendente import menu_atendente
from UI.menu_cidadao import menu_cidadao


def main():
	servico = ServicoSolicitacoes()
	atendente = Usuario(
		nome="Atendente Padrao",
		documento="00000000000",
		cargo=Cargo.FUNCIONARIO_PUBLICO,
	)

	while True:
		print("\n=== SISTEMA DE SOLICITACOES URBANAS ===")
		print("1. Area do cidadao")
		print("2. Area do atendente/gestor")
		print("0. Sair")
		opcao = input("Escolha: ").strip()

		if opcao == "1":
			menu_cidadao(servico)
		elif opcao == "2":
			menu_atendente(servico, atendente)
		elif opcao == "0":
			print("Encerrando sistema.")
			break
		else:
			print("Opcao invalida.")


if __name__ == "__main__":
	main()
