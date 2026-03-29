from Models.categoria import TipoCategoria
from Models.solicitacao import Prioridade
from Models.status import StatusSolicitacao
from Models.usuario import Usuario
from Services.servico_solicitacoes import ServicoSolicitacoes


def menu_atendente(servico: ServicoSolicitacoes, atendente: Usuario):
	while True:
		print("\n--- MENU ATENDENTE/GESTOR ---")
		print("1. Listar demandas")
		print("2. Atualizar status")
		print("0. Voltar")
		opcao = input("Escolha: ").strip()

		if opcao == "1":
			_listar_demandas(servico)
		elif opcao == "2":
			_atualizar_status(servico, atendente)
		elif opcao == "0":
			return
		else:
			print("Opcao invalida.")


def _listar_demandas(servico: ServicoSolicitacoes):
	prioridade = _filtro_prioridade()
	bairro = input("Filtro por bairro (opcional): ").strip() or None
	categoria = _filtro_categoria()

	demandas = servico.listar_demandas(prioridade=prioridade, bairro=bairro, categoria=categoria)
	if not demandas:
		print("Nenhuma demanda encontrada.")
		return

	for d in demandas:
		print(
			f"{d.protocolo} | {d.status.value} | {d.prioridade.value} | "
			f"{d.categoria.value} | {d.localizacao} | prazo: {d.calcular_prazo_alvo()}"
		)


def _atualizar_status(servico: ServicoSolicitacoes, atendente: Usuario):
	protocolo = input("Protocolo: ").strip()
	novo_status = _selecionar_status()
	comentario = input("Comentario (obrigatorio): ").strip()
	justificativa = input("Justificativa de atraso (se aplicavel): ").strip() or None

	try:
		solicitacao = servico.atualizar_status(
			protocolo=protocolo,
			novo_status=novo_status,
			responsavel=atendente,
			comentario=comentario,
			justificativa_atraso=justificativa,
		)
		print(f"Status atualizado para {solicitacao.status.value}.")
	except ValueError as exc:
		print(f"Erro: {exc}")


def _filtro_prioridade():
	print("\nPrioridade (0 para todas):")
	opcoes = list(Prioridade)
	for i, p in enumerate(opcoes, start=1):
		print(f"{i}. {p.value}")
	escolha = input("Escolha: ").strip()
	if escolha == "0" or not escolha:
		return None
	return opcoes[int(escolha) - 1]


def _filtro_categoria():
	print("\nCategoria (0 para todas):")
	opcoes = list(TipoCategoria)
	for i, c in enumerate(opcoes, start=1):
		print(f"{i}. {c.value}")
	escolha = input("Escolha: ").strip()
	if escolha == "0" or not escolha:
		return None
	return opcoes[int(escolha) - 1]


def _selecionar_status() -> StatusSolicitacao:
	print("\nNovo status:")
	opcoes = list(StatusSolicitacao)
	for i, status in enumerate(opcoes, start=1):
		print(f"{i}. {status.value}")
	escolha = int(input("Escolha: ").strip())
	return opcoes[escolha - 1]
