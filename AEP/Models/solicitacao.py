from datetime import date, datetime, timedelta
from typing import Optional

from Models.categoria import TipoCategoria, TipoIdentificacao
from Models.historico import Movimentacao
from Enums.status import StatusSolicitacao
from Models.usuario import Usuario
from Enums.prioridade import Prioridade



class Solicitacao:
	def __init__(
		self,
		protocolo: str,
		categoria: TipoCategoria,
		descricao: str,
		localizacao: str,
		identificacao: TipoIdentificacao,
		prioridade: Prioridade,
		cidadao: Optional[Usuario] = None,
		anexo: Optional[str] = None,
		status: StatusSolicitacao = StatusSolicitacao.ABERTO,
		criado_em: Optional[datetime] = None,
		justificativa_atraso: Optional[str] = None,
	):
		self.protocolo = protocolo
		self.categoria = categoria
		self.descricao = descricao
		self.localizacao = localizacao
		self.identificacao = identificacao
		self.prioridade = prioridade
		self.cidadao = cidadao
		self.anexo = anexo
		self.status = status
		self.criado_em = criado_em or datetime.now()
		self.justificativa_atraso = justificativa_atraso
		self.historico = []
		self.logs = []

		self.descricao = self.descricao.strip()
		self.localizacao = self.localizacao.strip()
		self.anexo = self.anexo.strip() if self.anexo else None
		self._validar_campos_obrigatorios()
		self._validar_regra_anonimato()
		self.registrar_log("Solicitacao criada")

	def calcular_prazo_alvo(self) -> date:
		return (self.criado_em + timedelta(days=self.prioridade.get_sla_dias())).date()

	def esta_atrasada(self) -> bool:
		status_finais = {StatusSolicitacao.RESOLVIDO, StatusSolicitacao.ENCERRADO}
		return date.today() > self.calcular_prazo_alvo() and self.status not in status_finais

	def registrar_log(self, mensagem: str):
		self.logs.append(f"{datetime.now().isoformat()} - {mensagem}")

	def atualizar_status(
		self,
		novo_status: StatusSolicitacao,
		responsavel: Usuario,
		comentario: str,
		justificativa_atraso: Optional[str] = None,
		data_evento: Optional[datetime] = None,
	):
		comentario = comentario.strip()
		if not comentario:
			raise ValueError("Comentario obrigatorio para atualizar status.")

		if not self.status.pode_transicionar_para(novo_status):
			raise ValueError(f"Transicao invalida: {self.status} -> {novo_status}")

		if self.esta_atrasada() and not justificativa_atraso:
			raise ValueError("Solicitacao atrasada exige justificativa.")

		if justificativa_atraso:
			self.justificativa_atraso = justificativa_atraso.strip()

		self.status = novo_status
		self.historico.append(
			Movimentacao(
				status=novo_status,
				data=data_evento or datetime.now(),
				responsavel=responsavel,
				comentario=comentario,
			)
		)
		self.registrar_log(f"Status alterado para {novo_status}")

	def _validar_campos_obrigatorios(self):
		if not self.descricao:
			raise ValueError("Descricao obrigatoria.")
		if not self.localizacao:
			raise ValueError("Localizacao obrigatoria.")
		if len(self.descricao) < 10:
			raise ValueError("Descricao deve ter ao menos 10 caracteres.")

	def _validar_regra_anonimato(self):
		if self.identificacao == TipoIdentificacao.ANONIMO:
			if self.cidadao is not None:
				raise ValueError("Solicitacao anonima nao pode conter dados pessoais.")
			if len(self.descricao) < 20:
				raise ValueError("Solicitacao anonima exige descricao mais detalhada (minimo 20 caracteres).")
			if len(self.localizacao) < 3:
				raise ValueError("Solicitacao anonima exige localizacao minima.")
			return

		if self.identificacao == TipoIdentificacao.IDENTIFICADO and self.cidadao is None:
			raise ValueError("Solicitacao identificada exige dados do cidadao.")
