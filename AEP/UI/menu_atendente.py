from Models.categoria import TipoCategoria
from Models.solicitacao import Prioridade
from Enums.status import StatusSolicitacao
from Models.usuario import Usuario
from Services.servico_solicitacoes import ServicoSolicitacoes
from UI.terminal_ui import (
	alerta,
	erro,
	ler_opcao,
	menu_opcoes,
	selecionar_indice,
	sucesso,
	titulo,
)


def menu_atendente(servico: ServicoSolicitacoes, atendente: Usuario):
	while True:
		titulo("Menu Atendente/Gestor")
		menu_opcoes([
			"1. Listar demandas",
			"2. Atualizar status",
			"0. Voltar",
		])
		opcao = ler_opcao()

		if opcao == "1":
			_listar_demandas(servico)
		elif opcao == "2":
			_atualizar_status(servico, atendente)
		elif opcao == "0":
			return
		else:
			alerta("Opcao invalida.")


def _listar_demandas(servico: ServicoSolicitacoes):
	prioridade = _filtro_prioridade()
	categoria = _filtro_categoria()

	demandas = servico.listar_demandas(prioridade=prioridade, categoria=categoria)
	if not demandas:
		alerta("Nenhuma demanda encontrada.")
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
		sucesso(f"Status atualizado para {solicitacao.status.value}.")
	except ValueError as exc:
		erro(str(exc))


def _filtro_prioridade():
	print("\nPrioridade (0 para todas):")
	opcoes = list(Prioridade)
	for i, p in enumerate(opcoes, start=1):
		print(f"{i}. {p.value}")
	escolha = ler_opcao()
	if escolha == "0" or not escolha:
		return None
	if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(opcoes):
		alerta("Filtro invalido. Nenhum filtro sera aplicado.")
		return None
	return opcoes[int(escolha) - 1]


def _filtro_categoria():
	print("\nCategoria (0 para todas):")
	opcoes = list(TipoCategoria)
	for i, c in enumerate(opcoes, start=1):
		print(f"{i}. {c.value}")
	escolha = ler_opcao()
	if escolha == "0" or not escolha:
		return None
	if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(opcoes):
		alerta("Filtro invalido. Nenhum filtro sera aplicado.")
		return None
	return opcoes[int(escolha) - 1]


def _selecionar_status() -> StatusSolicitacao:
	print("\nNovo status:")
	opcoes = list(StatusSolicitacao)
	for i, status in enumerate(opcoes, start=1):
		print(f"{i}. {status.value}")
	escolha = selecionar_indice(len(opcoes))
	return opcoes[escolha - 1]
