# main.py

import json
from pathlib import Path
from datetime import datetime
import typer
import yaml
import random

from generator import gera_divida, carregar_devedores
from api_client import APIClient

app = typer.Typer(add_completion=False, help="Ferramenta CLI para gerar e enviar dívidas fictícias")


def carregar_configuracao_yml(caminho: Path) -> dict:
    texto = caminho.read_text(encoding="utf-8")
    return yaml.safe_load(texto)


@app.callback(invoke_without_command=True)
def main(
        quantidade: int = typer.Option(10, "--quantidade", "-q", help="Número de dívidas a gerar"),
        arquivo_config: Path = typer.Option(Path("config.yml"), "--config", "-c", help="Arquivo de configuração YAML"),
        somente_simulacao: bool = typer.Option(False, "--simulacao", "-s", help="Gera JSON, não envia para a API"),
):
    """
    Gera um lote de dívidas fictícias e, se não for modo 'simulação', envia para a API configurada.
    """
    cfg = carregar_configuracao_yml(arquivo_config)
    cfg_geracao = cfg["generate"]
    cfg_api = cfg["api"]
    lista_devedores = carregar_devedores(cfg_geracao["devedores"])
    # 2) Exibe resumo das configurações na tela
    typer.secho("\n== CONFIGURAÇÕES DE GERAÇÃO ==", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"  • Quantidade  : {quantidade}")
    typer.echo(f"  • Intervalo   : {cfg_geracao['ano_inicio']} a {cfg_geracao['ano_fim']}")
    typer.echo(f"  • Valores min/max: {cfg_geracao['min_valor']} – {cfg_geracao['max_valor']}")

    typer.secho("\n== CONFIGURAÇÕES DA API ==", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"  • Base URL    : {cfg_api['base_url']}")
    typer.echo(f"  • Endpoint    : {cfg_api['endpoint']}")
    typer.echo(f"  • Auth path   : {cfg_api['auth']['url']}")
    typer.echo(f"  • Tenant      : {cfg_api['tenant']}")
    typer.echo(f"  • Simulação   : {'Sim' if somente_simulacao else 'Não'}")

    # 3) Confirmação interativa
    if not typer.confirm("\nDeseja continuar com estas configurações?"):
        typer.secho("🚫 Operação abortada pelo usuário.", fg=typer.colors.RED)
        raise typer.Exit()

    # 4) Se não for simulação, autentica na API
    cliente_api = None
    if not somente_simulacao:
        cliente_api = APIClient(
            base_url=cfg_api["base_url"],
            endpoint=cfg_api["endpoint"],
            auth_url=cfg_api["auth"]["url"],
            basic_auth=cfg_api["auth"]["basic"],
            tenant=cfg_api["tenant"],
            user=cfg_api["user"],
            password=cfg_api["password"],
        )
        typer.secho("✅ Autenticação bem‑sucedida!\n", fg=typer.colors.GREEN)

    # 5) Geração e (opcional) envio das dívidas
    lista_dividas = []
    for i in range(1, quantidade + 1):
        devedor = random.choice(lista_devedores)
        divida = gera_divida(cfg_geracao, devedor)
        payload = divida.model_dump(mode="json")

        if somente_simulacao:
            typer.echo(f"[{i}/{quantidade}] Dívida {payload['identificador']} — gerada (simulação)")
        else:
            resp = cliente_api.envia_divida(payload)
            typer.echo(f"[{i}/{quantidade}] Dívida {payload['identificador']} — enviada (HTTP {resp.status_code})")

        lista_dividas.append(payload)

    # 6) Salva todas as dívidas em um arquivo JSON timestamped
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = Path(f"dividas_{timestamp}.json")
    conteudo_json = json.dumps(lista_dividas, ensure_ascii=False, indent=2)

    nome_arquivo.write_text(conteudo_json, encoding="utf-8")
    typer.secho(f"\n✅ Arquivo salvo: {nome_arquivo}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
