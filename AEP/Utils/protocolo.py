from datetime import datetime
from itertools import count


_sequencial = count(1)


def gerar_protocolo(prefixo: str = "SOL") -> str:
	numero = next(_sequencial)
	timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
	return f"{prefixo}-{timestamp}-{numero:04d}"
