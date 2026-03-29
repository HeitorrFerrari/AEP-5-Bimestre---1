from enum import Enum


class Cargo(Enum):
	CIDADAO = "Cidadao"
	FUNCIONARIO_PUBLICO = "Funcionario publico"

	def __str__(self):
		return self.value


class Usuario:
	def __init__(self, nome: str, documento: str, cargo: Cargo = Cargo.CIDADAO):
		nome = nome.strip()
		documento = documento.strip()
		if not nome:
			raise ValueError("Nome do usuario e obrigatorio.")
		if not documento:
			raise ValueError("Documento do usuario e obrigatorio.")

		self.nome = nome
		self.documento = documento
		self.cargo = cargo
