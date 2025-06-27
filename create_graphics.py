import csv
import matplotlib.pyplot as plt

operacoes = []
tempos = []

with open('results_mongodb_benchmark.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        operacoes.append(row[0])
        tempos.append(float(row[1]))

plt.figure(figsize=(10, 6))
plt.bar(operacoes, tempos, color='royalblue')
plt.xlabel('Operações')
plt.ylabel('Tempo (s)')
plt.title('Benchmark de Desempenho no MySQL')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.savefig('grafico_benchmark.png')