from Services.servico_solicitacoes import ServicoSolicitacoes
from Models.solicitacao import Solicitacao
from Models.status import StatusSolicitacao


class FilaAtendimento:
    def __init__(self, servico: ServicoSolicitacoes):
        self.servico = servico

    def listar_pendentes(self) -> list[Solicitacao]:
        pendentes = self.servico.listar_demandas()
        status_finais = {StatusSolicitacao.RESOLVIDO, StatusSolicitacao.ENCERRADO}
        return [s for s in pendentes if s.status not in status_finais]