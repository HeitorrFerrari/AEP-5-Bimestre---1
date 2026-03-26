from enum import enum 

class categoria(Enum):
    ILUMINACAO = "Iluminação pública"
    BURACO = "Buraco nas ruas"
    PODA = "Podagem de árvores irregulares"
    SAUDE = "Duvidas ou solicitação de tarefa relacionada a saúde"
    LIMPEZA = "Limpeza e zeladoria"
    OUTRO = "Outro"

    def __str__(self):
        return self.value