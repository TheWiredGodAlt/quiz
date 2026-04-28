# 🧩 Quiz Interativo de Estruturas de Dados

## 📌 Descrição
Sistema interativo (CLI) que aplica conceitos fundamentais de Estruturas de Dados através de um quiz educacional. O projeto integra teoria e prática, permitindo cadastro dinâmico de perguntas, fluxo controlado por fila, histórico navegável por pilha e acesso rápido via dicionário.

## 🎯 Objetivos
- Aplicar Listas, Filas, Pilhas e Dicionários em contexto real
- Desenvolver lógica de programação e validação de entrada
- Promover organização, modularidade e documentação de código

## 🛠️ Requisitos Atendidos
| Requisito | Implementação |
|-----------|---------------|
| Listas | `self.lista_perguntas`: armazenamento sequencial de IDs |
| Filas | `self.fila_perguntas`: controle FIFO da ordem de apresentação |
| Pilhas | `self.pilha_historico`: histórico LIFO para revisão de respostas |
| Dicionários | `self.mapa_perguntas`: mapeamento O(1) ID → dados completos |
| Cadastro | Função interativa + carregamento inicial |
| Pontuação/Feedback | Sistema de +10 pts, explicações e validação |
| Progresso/Resultados | Contador em tempo real + tela final com % |

## ▶️ Como Executar
```bash
python quiz_ds.py
