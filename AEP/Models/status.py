from enum import Enum


class StatusSolicitacao(Enum):
	ABERTO = "Aberto"
	TRIAGEM = "Triagem"
	EM_EXECUCAO = "Em execucao"
	RESOLVIDO = "Resolvido"
	ENCERRADO = "Encerrado"

	def __str__(self):
		return self.value

	def pode_transicionar_para(self, novo_status: "StatusSolicitacao") -> bool:
		fluxo = {
			StatusSolicitacao.ABERTO: StatusSolicitacao.TRIAGEM,
			StatusSolicitacao.TRIAGEM: StatusSolicitacao.EM_EXECUCAO,
			StatusSolicitacao.EM_EXECUCAO: StatusSolicitacao.RESOLVIDO,
			StatusSolicitacao.RESOLVIDO: StatusSolicitacao.ENCERRADO,
			StatusSolicitacao.ENCERRADO: None,
		}
		return fluxo[self] == novo_status
