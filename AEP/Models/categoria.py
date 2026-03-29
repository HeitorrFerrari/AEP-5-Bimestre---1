from enum import Enum


class TipoCategoria(Enum):
    ILUMINACAO = "Iluminação pública"
    BURACO = "Buraco nas ruas"
    PODA = "Podagem de árvores irregulares"
    SAUDE = "Duvidas ou solicitação de tarefa relacionada a saúde"
    LIMPEZA = "Limpeza e zeladoria"
    OUTRO = "Outro"

    def __str__(self):
        return self.value


class TipoIdentificacao(Enum):
    IDENTIFICADO = "Identificado"
    ANONIMO = "Anonimo"

    def __str__(self):
        return self.value


class Categoria:

    def __init__(self, tipo_categoria: TipoCategoria, descricao: str, opcao: TipoIdentificacao):
        self.tipo_categoria = tipo_categoria
        self.descricao = descricao
        self.opcao = opcao