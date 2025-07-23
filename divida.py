from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Endereco(BaseModel):
    logradouro: str
    numero: str
    bairro: str
    complemento: Optional[str] = None
    cep: str
    uf: str
    nomeMunicipio: str


class Pessoa(BaseModel):
    nomeIntegracao: dict
    documentoPrincipal: dict
    telefonePrincipal: dict
    emailPrincipal: dict
    enderecoIntegracao: Endereco


class Protesto(BaseModel):
    ordemNoProcesso: str
    nomeCartorio: str
    numero: str
    data: datetime
    tipo: dict


class AjuizamentoRemovido(BaseModel):
    dataRemocao: datetime
    dataAjuizamento: datetime
    numeroJudicial: str


class Ajuizamento(BaseModel):
    dataAjuizamento: datetime
    numeroJudicial: str


class SituacaoAtual(BaseModel):
    dataSituacao: datetime
    tipo: dict
    mensagemId: int


class Composicao(BaseModel):
    numero: str
    identificador: str
    valorMultaAtual: float
    valorJurosAtual: float
    valorCorrecaoAtual: float
    valorTotalInscricao: float
    valorTotalAtual: float
    valorHonorariosAtual: float
    situacaoAtual: dict


class Exercicio(BaseModel):
    ano: int
    vencimento: datetime


class Parcelamento(BaseModel):
    identificador: str
    numero: str
    dataConcessao: datetime
    dataUltimoPagamento: datetime
    parcelas: int
    parcelasEmAtraso: int
    valorParcelamento: float
    valorSaldo: float
    valorPago: float
    situacaoAtual: dict
    tipo: str


class Divida(BaseModel):
    identificador: str
    numero: str
    processoInscricao: str
    numeroBemFato: Optional[str]
    numeroDocumentoFato: Optional[str]
    fato: Optional[str]
    dataInscricao: datetime
    dataBase: Optional[str]
    dataLancamento: datetime
    dataConstituicaoCredito: datetime
    dataCienciaFato: datetime
    dataPrescricao: datetime
    categoria: dict
    infracao: Optional[dict]
    tributo: dict
    orgaoOrigemId: int
    natureza: str
    endereco: Endereco
    devedor: Pessoa
    ajuizamento: Optional[Ajuizamento]
    ajuizamentosRemovido: Optional[List[AjuizamentoRemovido]]
    situacaoAtual: SituacaoAtual
    composicoes: Optional[List[Composicao]]
    exercicios: Optional[List[Exercicio]]
    vencimentoExercicios: Optional[List[Exercicio]]
    parcelamento: Optional[Parcelamento]
    parcelamentosRompidos: Optional[List[Parcelamento]]

    valorTotalAtual: float
    valorTotalSemHonorarios: float
    valorImpostoAtual: float

    serie: str
    livro: str
    folha: str
