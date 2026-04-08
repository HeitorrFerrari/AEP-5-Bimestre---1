from typing import Optional

from Models.categoria import TipoCategoria, TipoIdentificacao
from Models.solicitacao import Prioridade, Solicitacao
from Enums.status import StatusSolicitacao
from Models.usuario import Usuario
from Utils.protocolo import gerar_protocolo


class ServicoSolicitacoes:
	def __init__(self):
		self._solicitacoes: dict[str, Solicitacao] = {}

	def cadastrar_solicitacao(
		self,
		categoria: TipoCategoria,
		descricao: str,
		localizacao: str,
		identificacao: TipoIdentificacao,
		prioridade: Prioridade,
		cidadao: Optional[Usuario] = None,
	) -> Solicitacao:
		protocolo = gerar_protocolo()
		solicitacao = Solicitacao(
			protocolo=protocolo,
			categoria=categoria,
			descricao=descricao,
			localizacao=localizacao,
			identificacao=identificacao,
			prioridade=prioridade,
			cidadao=cidadao,
		)
		self._solicitacoes[protocolo] = solicitacao
		return solicitacao

	def buscar_por_protocolo(self, protocolo: str) -> Optional[Solicitacao]:
		return self._solicitacoes.get(protocolo)

	def listar_demandas(
		self,
		prioridade: Optional[Prioridade] = None,
		categoria: Optional[TipoCategoria] = None,
	) -> list[Solicitacao]:
		demandas = list(self._solicitacoes.values())
		if prioridade:
			demandas = [d for d in demandas if d.prioridade == prioridade]
		if categoria:
			demandas = [d for d in demandas if d.categoria == categoria]

		return sorted(
			demandas,
			key=lambda d: (-d.prioridade.get_peso(), d.calcular_prazo_alvo(), d.criado_em),
		)

	def atualizar_status(
		self,
		protocolo: str,
		novo_status: StatusSolicitacao,
		responsavel: Usuario,
		comentario: str,
		justificativa_atraso: Optional[str] = None,
	) -> Solicitacao:
		solicitacao = self.buscar_por_protocolo(protocolo)
		if not solicitacao:
			raise ValueError("Protocolo nao encontrado.")

		solicitacao.atualizar_status(
			novo_status=novo_status,
			responsavel=responsavel,
			comentario=comentario,
			justificativa_atraso=justificativa_atraso,
		)
		return solicitacao

	def listar_atrasadas(self) -> list[Solicitacao]:
		return [s for s in self._solicitacoes.values() if s.esta_atrasada()]
