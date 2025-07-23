#!/bin/bash

print() {
  echo -e "\033[1;36m[INFO]\033[0m $1"
}

error() {
  echo -e "\033[1;31m[ERRO]\033[0m $1"
}

print "Verificando Python..."
if ! command -v python3 &> /dev/null; then
  error "Python3 não encontrado! Por favor, instale o Python 3.10 ou superior manualmente."
  exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ "$(echo "$PY_VER < 3.10" | bc -l)" == 1 ]]; then
  error "Versão do Python é $PY_VER. É necessário Python 3.10 ou superior."
  exit 1
fi

print "Python $PY_VER encontrado."

print "Criando ambiente virtual (venv)..."
python3 -m venv .venv || {
  error "Falha ao criar o ambiente virtual."
  exit 1
}

source .venv/bin/activate

print "Atualizando pip..."
pip install --upgrade pip

print "Instalando dependências do requirements.txt..."
pip install -r requirements.txt || {
  error "Erro ao instalar dependências."
  deactivate
  exit 1
}

print "✅ Instalação concluída!"
echo
echo "Agora você pode executar os comandos com o ambiente ativado: ;)"
echo "Agora vai lá ler o README.md seu preguiçoso!)"