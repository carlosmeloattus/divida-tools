💼 divida-tools

Gere e envie dados simulados de dívidas para os ambientes de TESTE ATTUS, facilitando testes.
🧱 Requisitos

    Python 3.10+

    Permissão de execução de scripts (.sh no Linux/macOS)

🚀 Instalação Rápida

```bash
git clone https://github.com/seu-usuario/divida-tools.git
cd divida-tools
./install.sh  # Configura ambiente e dependências automaticamente
```

⚙️ Configuração
🔑 Arquivo config.yml (Exemplo mínimo)

você deve configurar o config.yml com a parametrização que precisa, da seguinte forma:

```yaml
api:
  base_url: https://api.exemplo.com # URL base da API
  endpoint: /divida/dividas # Endpoint para envio de dívidas
  tenant: PGESP # Identificador do tenant (ex: PGESP, PGEBA, etc.)
  user: theBigBang@attus.ai # seu usuário de acesso
  password: sua_senha # sua senha de acesso

  auth:
    url: /uaa/oauth/token # URL de autenticação
    basic: "QVROOT1JTQVRVVVM6c2121X3NlY3JldA==" # Authorization Base64

generate:
  ano_inicio: 2022 # Ano de início para geração de dívidas
  ano_fim: 2024 # Ano de fim para geração de dívidas
  min_valor: 1000 # Valor mínimo dos valores das dívidas (são randomizados entre o mínimo e o máximo)
  max_valor: 200000 # Valor máximo dos valores das dívidas
  devedores: devedores.yml # Arquivo com dados dos devedores
  categoria_identificadores: [ "1", "4" ] # identificadores de categoria para as dívidas
  tributo_identificadores: [ "2" ] # identificadores de tributo para as dívidas
  situacao_tipo_ids: [ "1", "2", "3" ] # IDs de situação das dívidas
  orgao_origem_id: 1 # ID do órgão de origem das dívidas
```

👤 Arquivo devedores.yml (Estrutura)
o arquivo devedores.yml deve conter os dados dos devedores que serão usados para gerar as dívidas. se você criar 5 devedores aqui e selecionar 50 dividas, o script irá gerar 50 dívidas aleatórias entre esses 5 devedores.

```yaml
devedor:
  - nome: "Maria Silva"
    documentoPrincipal:
      tipo: CPF
      numero: "12345678901"
    telefonePrincipal:
      numero: "(11) 99999‑0000"
    emailPrincipal:
      nome: "maria.silva@email.com"
    enderecoIntegracao:
      logradouro: "Rua A"
      numero: "100"
      complemento: "AP 10"
      bairro: "Centro"
      cep: "01001000"
      uf: "SP"
      nomeMunicipio: "São Paulo"
```

🛠️ Uso via CLI (main.py)
📌 Comandos Básicos

```bash

source .venv/bin/activate # Ativar ambiente virtual

# Ver ajuda

python src/main.py --help

# Gerar 10 dívidas (padrão) e enviar para API

python src/main.py

# Gerar 5 dívidas em modo simulação (sem envio)

python src/main.py -q 5 -s

# Usar configuração personalizada

python src/main.py -c config_homolog.yml -q 20
```

🚨 Importante

    API Real: O comando que for preenchido sem a tag -simulacao faz requisições reais - use apenas em ambientes de teste!

    Modo Simulação (-simulacao ou -s): Ideal para validar dados antes de enviar a sua API

    Arquivo de Saída: Sempre gerado no formato dividas_AAAAMMDD_HHMMSS.json.

    Ambiente Virtual: Use source .venv/bin/activate antes de executar os scripts.