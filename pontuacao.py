import csv
import os
from datetime import date


def carregar_pontuacao():
    pontuacoes = []
    if os.path.exists('pontuacoes.csv'):
        with open('pontuacoes.csv', 'r') as arq:
            reader = csv.DictReader(arq)
            for linha in reader:
                pontuacao = int(linha['pontuacao'])
                pontuacoes.append(pontuacao)
    else:
        with open('pontuacoes.csv', 'w', newline='') as arq:
            writer = csv.writer(arq)
            writer.writerow(['data', 'pontuacao'])

    return pontuacoes

def salvar_pontuacao(pontuacoes):
    with open('pontuacoes.csv', 'w', newline='') as arq:
        writer = csv.writer(arq)
        writer.writerow(['data', 'pontuacao'])
        for pontuacao in pontuacoes:
            writer.writerow([date.today(), pontuacao])