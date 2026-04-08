from datetime import datetime

from Enums.status import StatusSolicitacao
from Models.usuario import Usuario


class Movimentacao:
	def __init__(self, status: StatusSolicitacao, data: datetime, responsavel: Usuario, comentario: str):
		self.status = status
		self.data = data
		self.responsavel = responsavel
		self.comentario = comentario
