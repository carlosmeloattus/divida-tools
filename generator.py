# generator.py

import random
from datetime import datetime, timedelta
from faker import Faker
from divida import (
    Divida,
    Endereco,
    Pessoa,
    Protesto, SituacaoAtual
)
import yaml

fake = Faker("pt_BR")


def load_config(path: str = "config.yml") -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)["generate"]


def random_date(ano_inicio: int, ano_fim: int) -> datetime:
    inicio = datetime(ano_inicio, 1, 1)
    fim = datetime(ano_fim, 12, 31)
    delta = fim - inicio
    return inicio + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def gera_endereco() -> Endereco:
    return Endereco(
        logradouro=fake.street_name(),
        numero=str(fake.building_number()),
        bairro=fake.bairro(),
        complemento=f"APTO {fake.building_number()}",
        cep=fake.postcode().replace("-", ""),
        uf=fake.estado_sigla(),
        nomeMunicipio=fake.city(),
    )


def gera_pessoa() -> Pessoa:
    endereco = gera_endereco()
    return Pessoa(
        nomeIntegracao={"nome": fake.name()},
        documentoPrincipal={"tipo": "CPF", "numero": fake.cpf()},
        telefonePrincipal={"numero": fake.phone_number()},
        emailPrincipal={"nome": fake.free_email()},
        enderecoIntegracao=endereco,
    )


def gera_protesto() -> Protesto:
    return Protesto(
        ordemNoProcesso=str(random.randint(1, 10)),
        nomeCartorio=fake.company(),
        numero=str(fake.random_number(digits=8)),
        data=random_date(cfg["ano_inicio"], cfg["ano_fim"]),
        tipo={"identificadorNoCliente": str(random.choice(["PT1", "PT2"]))},
    )


def carregar_devedores(path: str) -> list[Pessoa]:
    with open(path, encoding="utf-8") as f:
        lista_devedores = yaml.safe_load(f)

    pessoas = []
    for devedor in lista_devedores["devedor"]:
        endereco = Endereco(**devedor["enderecoIntegracao"])
        pessoa = Pessoa(
            nomeIntegracao={"nome": devedor["nome"]},
            documentoPrincipal=devedor["documentoPrincipal"],
            telefonePrincipal=devedor["telefonePrincipal"],
            emailPrincipal=devedor["emailPrincipal"],
            enderecoIntegracao=endereco,
        )
        pessoas.append(pessoa)

    return pessoas


def gera_divida(config: dict, devedor: Pessoa) -> Divida:
    # Datas
    dl = random_date(config["ano_inicio"], config["ano_fim"])
    dc = random_date(config["ano_inicio"], config["ano_fim"])
    df = random_date(config["ano_inicio"] + 3, config["ano_fim"] + 3)

    # Valores
    imposto = round(random.uniform(config["min_valor"], config["max_valor"]), 2)
    juros = round(random.uniform(0, config.get("max_juros", 0)), 2)
    multa = round(random.uniform(0, config.get("max_multa", 0)), 2)
    honor = round(random.uniform(0, config.get("max_honorarios", 0)), 2)

    numero = fake.unique.random_number(digits=10, fix_len=True)
    numero_sem_pontos = f"{numero:010d}"
    numero_com_pontos = f"{numero_sem_pontos[0]}.{numero_sem_pontos[1:4]}.{numero_sem_pontos[4:7]}.{numero_sem_pontos[7:]}"

    categoria_id = random.choice(config.get("categoria_identificadores", ["1"]))
    tributo_id = random.choice(config.get("tributo_identificadores", ["1"]))
    situacao_tipo_id = random.choice(config.get("situacao_tipo_ids", ["1"]))
    orgao_origem_id = config.get("orgao_origem_id", 1)

    # Cria o objeto Divida
    return Divida(
        identificador=numero_com_pontos,
        numero=numero_sem_pontos,
        processoInscricao=str(fake.unique.random_number(digits=13)),
        numeroBemFato=None,
        numeroDocumentoFato=None,
        fato=None,
        dataInscricao=dl,
        dataBase=str(config["ano_fim"]),
        dataLancamento=dl,
        dataAtualizacaoValores=datetime.now(),
        dataConstituicaoCredito=dc,
        dataCienciaFato=df,
        dataPrescricao=df,
        categoria={"identificadorNoCliente": categoria_id},
        infracao=None,
        composicoes=[],
        tributo={"identificadorNoCliente": tributo_id},
        orgaoOrigemId=orgao_origem_id,
        natureza="TRIBUTARIA",
        endereco=devedor.enderecoIntegracao,
        devedor=devedor,
        ajuizamento=None,
        ajuizamentosRemovido=[],
        situacaoAtual=SituacaoAtual(
            dataSituacao=datetime.now(),
            tipo={"id": situacao_tipo_id},
            mensagemId=0
        ),
        exercicios=[],
        vencimentoExercicios=None,
        parcelamento=None,
        parcelamentosRompidos=None,
        valorTotalAtual=round(imposto + juros + multa + honor, 2),
        valorTotalSemHonorarios=round(imposto + juros + multa, 2),
        valorImpostoAtual=imposto,
        serie="1",
        livro="1",
        folha="1",
    )


if __name__ == "__main__":
    cfg = load_config()
    devedores = carregar_devedores("devedores.yml")
    lista = [gera_divida(cfg, random.choice(devedores)) for _ in range(cfg.get("default_count", 10))]
    print(f"Geradas {len(lista)} dívidas.")
