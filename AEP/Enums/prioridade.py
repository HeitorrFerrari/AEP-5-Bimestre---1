from enum import Enum

class Prioridade(Enum):
	BAIXA = "Baixa"
	MEDIA = "Media"
	ALTA = "Alta"
	CRITICA = "Critica"

	def get_sla_dias(self) -> int:
		return {
			Prioridade.BAIXA: 15,
			Prioridade.MEDIA: 7,
			Prioridade.ALTA: 3,
			Prioridade.CRITICA: 1,
		}[self]

	def get_impacto_social(self) -> str:
		return {
			Prioridade.BAIXA: "Impacto localizado",
			Prioridade.MEDIA: "Impacto moderado",
			Prioridade.ALTA: "Impacto relevante",
			Prioridade.CRITICA: "Impacto social alto",
		}[self]

	def get_peso(self) -> int:
		return {
			Prioridade.BAIXA: 1,
			Prioridade.MEDIA: 2,
			Prioridade.ALTA: 3,
			Prioridade.CRITICA: 4,
		}[self]