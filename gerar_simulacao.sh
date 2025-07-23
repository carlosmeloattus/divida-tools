#!/bin/bash

# Ativa o ambiente virtual, se existir
source .venv/bin/activate 2>/dev/null

echo "🔧 Gerando dívidas em modo simulação..."
python main.py --quantidade 10 --simulacao
