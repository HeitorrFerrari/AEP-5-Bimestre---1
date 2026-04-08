from Models.categoria import TipoCategoria, TipoIdentificacao
from Models.solicitacao import Prioridade
from Models.usuario import Cargo, Usuario
from Services.servico_solicitacoes import ServicoSolicitacoes
from UI.terminal_ui import (
	alerta,
	erro,
	info,
	ler_opcao,
	menu_opcoes,
	selecionar_indice,
	sucesso,
	titulo,
)


def menu_cidadao(servico: ServicoSolicitacoes):
	while True:
		titulo("Menu do Cidadao")
		menu_opcoes([
			"1. Nova solicitacao",
			"2. Acompanhar por protocolo",
			"0. Voltar",
		])
		opcao = ler_opcao()

		if opcao == "1":
			_cadastrar_solicitacao(servico)
		elif opcao == "2":
			_acompanhar(servico)
		elif opcao == "0":
			return
		else:
			alerta("Opcao invalida.")


def _cadastrar_solicitacao(servico: ServicoSolicitacoes):
	categoria = _selecionar_enum("Categoria", list(TipoCategoria))
	prioridade = _selecionar_enum("Prioridade", list(Prioridade))
	identificacao = _selecionar_enum("Identificacao", list(TipoIdentificacao))

	descricao = input("Descricao: ").strip()
	localizacao = input("Localizacao/Bairro: ").strip()
	anexo = input("Anexo (opcional): ").strip() or None

	cidadao = None
	if identificacao == TipoIdentificacao.IDENTIFICADO:
		nome = input("Nome: ").strip()
		documento = input("Documento: ").strip()
		cidadao = Usuario(nome=nome, documento=documento, cargo=Cargo.CIDADAO)

	try:
		solicitacao = servico.cadastrar_solicitacao(
			categoria=categoria,
			descricao=descricao,
			localizacao=localizacao,
			identificacao=identificacao,
			prioridade=prioridade,
			cidadao=cidadao,
			anexo=anexo,
		)
		sucesso(f"Solicitacao criada. Protocolo: {solicitacao.protocolo}")
		info(f"Prazo alvo: {solicitacao.calcular_prazo_alvo()}")
	except ValueError as exc:
		erro(str(exc))


def _acompanhar(servico: ServicoSolicitacoes):
	protocolo = input("Informe o protocolo: ").strip()
	solicitacao = servico.buscar_por_protocolo(protocolo)
	if not solicitacao:
		alerta("Protocolo nao encontrado.")
		return

	print(f"Status: {solicitacao.status}")
	print(f"Categoria: {solicitacao.categoria.value}")
	print(f"Prioridade: {solicitacao.prioridade.value}")
	print(f"Prazo alvo: {solicitacao.calcular_prazo_alvo()}")
	print(f"Atrasada: {'Sim' if solicitacao.esta_atrasada() else 'Nao'}")
	if solicitacao.justificativa_atraso:
		print(f"Justificativa: {solicitacao.justificativa_atraso}")

	print("Historico:")
	if not solicitacao.historico:
		info("Sem movimentacoes ainda.")
		return

	for mov in solicitacao.historico:
		print(f"  - {mov.data} | {mov.status} | {mov.responsavel.nome} | {mov.comentario}")


def _selecionar_enum(titulo: str, opcoes: list):
	print(f"\n{titulo}:")
	for i, item in enumerate(opcoes, start=1):
		valor = item.value if hasattr(item, "value") else str(item)
		print(f"{i}. {valor}")
	indice = selecionar_indice(len(opcoes))
	return opcoes[indice - 1]
