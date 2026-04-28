#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUIZ INTERATIVO DE ESTRUTURAS DE DADOS
Projeto Acadêmico - Ciência da Computação
Autor: Gustavo Goulart Ribeiro
Disciplina: Estruturas de Dados
Professora: Pauliane Cardoso
"""

import json
import os
import sys
from typing import List, Dict, Any, Optional

# ==========================================
# IMPLEMENTAÇÃO DAS ESTRUTURAS DE DADOS
# ==========================================

class Pilha:
    """Estrutura LIFO (Last In, First Out) para histórico e revisão."""
    def __init__(self):
        self.__itens: List[Any] = []

    def push(self, item: Any) -> None:
        self.__itens.append(item)

    def pop(self) -> Optional[Any]:
        return self.__itens.pop() if not self.is_empty() else None

    def peek(self) -> Optional[Any]:
        return self.__itens[-1] if not self.is_empty() else None

    def is_empty(self) -> bool:
        return len(self.__itens) == 0

    def size(self) -> int:
        return len(self.__itens)

    def to_list(self) -> List[Any]:
        return list(reversed(self.__itens))


class Fila:
    """Estrutura FIFO (First In, First Out) para controle da ordem das perguntas."""
    def __init__(self):
        self.__itens: List[Any] = []

    def enqueue(self, item: Any) -> None:
        self.__itens.append(item)

    def dequeue(self) -> Optional[Any]:
        return self.__itens.pop(0) if not self.is_empty() else None

    def is_empty(self) -> bool:
        return len(self.__itens) == 0

    def size(self) -> int:
        return len(self.__itens)


# ==========================================
# Engine usada no quiz
# ==========================================

class QuizEngine:
    """Gerencia o fluxo do quiz aplicando as estruturas de dados solicitadas."""

    def __init__(self):
        # Dicionário (Hash Map): associação direta ID -> dados da pergunta
        self.mapa_perguntas: Dict[str, Dict[str, Any]] = {}
        # Lista: armazenamento sequencial de IDs de perguntas
        self.lista_perguntas: List[str] = []
        # Fila: controle da ordem de apresentação
        self.fila_perguntas: Fila = Fila()
        # Pilha: histórico de navegação/respostas para revisão
        self.pilha_historico: Pilha = Pilha()
        
        self.pontuacao: int = 0
        self.total_perguntas: int = 0
        self.pergunta_atual: Optional[Dict] = None
        self.id_atual: Optional[str] = None

        self._carregar_perguntas_padrao()

    def _carregar_perguntas_padrao(self) -> None:
        """Carrega perguntas iniciais (simulando cadastro/armazenamento)."""
        perguntas_iniciais = [
            {
                "id": "Q1",
                "enunciado": "Qual estrutura de dados segue o princípio LIFO (Last In, First Out)?",
                "opcoes": ["A) Fila", "B) Lista", "C) Pilha", "D) Árvore"],
                "resposta_correta": "C",
                "explicacao": "A Pilha insere e remove elementos pela mesma extremidade (topo), seguindo LIFO."
            },
            {
                "id": "Q2",
                "enunciado": "Em uma Fila, qual operação remove o elemento mais antigo?",
                "opcoes": ["A) push", "B) pop", "C) enqueue", "D) dequeue"],
                "resposta_correta": "D",
                "explicacao": "O dequeue remove o elemento que está há mais tempo na fila (FIFO)."
            },
            {
                "id": "Q3",
                "enunciado": "Qual estrutura permite acesso direto por chave com complexidade O(1) em média?",
                "opcoes": ["A) Lista Encadeada", "B) Dicionário (Hash Map)", "C) Fila", "D) Pilha"],
                "resposta_correta": "B",
                "explicacao": "Dicionários usam tabelas hash para mapear chaves a valores, permitindo acesso O(1)."
            },
            {
                "id": "Q4",
                "enunciado": "Qual é a complexidade temporal média para busca em uma Lista não ordenada?",
                "opcoes": ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n²)"],
                "resposta_correta": "C",
                "explicacao": "É necessário percorrer até n elementos no pior caso, resultando em O(n)."
            }
        ]

        for p in perguntas_iniciais:
            self.cadastrar_pergunta(p)

    def cadastrar_pergunta(self, dados: Dict[str, Any]) -> None:
        """Cadastro e armazenamento usando Lista e Dicionário."""
        pid = dados["id"]
        if pid in self.mapa_perguntas:
            return  # Evita duplicatas
        
        # Dicionário: mapeamento rápido por ID
        self.mapa_perguntas[pid] = dados
        # Lista: armazenamento sequencial
        self.lista_perguntas.append(pid)
        # Fila: enfileira para o fluxo do jogo
        self.fila_perguntas.enqueue(pid)
        self.total_perguntas = len(self.lista_perguntas)

    def iniciar_quiz(self) -> None:
        """Inicia o loop principal do jogo."""
        print("\n" + "="*60)
        print("🎮 QUIZ DE ESTRUTURAS DE DADOS".center(60))
        print("="*60 + "\n")
        
        if self.fila_perguntas.is_empty():
            print("❌ Nenhuma pergunta cadastrada. Adicione perguntas primeiro.")
            return

        while not self.fila_perguntas.is_empty():
            self._mostrar_proxima_pergunta()
            self._processar_resposta()
            self._atualizar_progresso()

        self._exibir_resultados_finais()
        self._oferecer_revisao()

    def _mostrar_proxima_pergunta(self) -> None:
        """Exibe pergunta dinâmica com controle de progresso."""
        self.id_atual = self.fila_perguntas.dequeue()
        self.pergunta_atual = self.mapa_perguntas[self.id_atual]
        progresso = self.pilha_historico.size() + 1
        
        print(f"\n📌 Pergunta {progresso} de {self.total_perguntas}")
        print(f"💰 Pontuação: {self.pontuacao} pts")
        print("-" * 50)
        print(self.pergunta_atual["enunciado"])
        for opcao in self.pergunta_atual["opcoes"]:
            print(f"  {opcao}")
        print("-" * 50)

    def _processar_resposta(self) -> None:
        """Valida resposta, aplica pontuação e empilha no histórico."""
        while True:
            resposta = input("\n🔹 Sua resposta (A/B/C/D): ").strip().upper()
            if resposta in ["A", "B", "C", "D"]:
                break
            print("⚠️ Opção inválida. Digite apenas A, B, C ou D.")

        correta = self.pergunta_atual["resposta_correta"]
        acertou = resposta == correta

        if acertou:
            self.pontuacao += 10
            print("\n✅ CORRETO! +10 pontos")
        else:
            print(f"\n❌ INCORRETO! A resposta certa era {correta}")
        
        print(f"📘 Explicação: {self.pergunta_atual['explicacao']}")

        # Pilha: armazena histórico para revisão futura
        registro = {
            "id": self.id_atual,
            "pergunta": self.pergunta_atual["enunciado"],
            "sua_resposta": resposta,
            "correta": correta,
            "acertou": acertou
        }
        self.pilha_historico.push(registro)
        input("\n👉 Pressione ENTER para continuar...")

    def _atualizar_progresso(self) -> None:
        """Feedback de progresso em tempo real."""
        restantes = self.fila_perguntas.size()
        if restantes > 0:
            print(f"\n⏳ Faltam {restantes} pergunta(s) para concluir.")

    def _exibir_resultados_finais(self) -> None:
        """Exibe resultados finais consolidados."""
        print("\n" + "="*60)
        print("🏆 RESULTADO FINAL".center(60))
        print("="*60)
        print(f"📊 Perguntas respondidas: {self.pilha_historico.size()}/{self.total_perguntas}")
        print(f"💰 Pontuação total: {self.pontuacao}")
        porcentagem = (self.pontuacao / (self.total_perguntas * 10)) * 100
        print(f"📈 Aproveitamento: {porcentagem:.1f}%")
        
        if porcentagem >= 80:
            print("🌟 Excelente! Domínio consolidado das estruturas de dados.")
        elif porcentagem >= 50:
            print("👍 Bom desempenho. Revise os conceitos das questões erradas.")
        else:
            print("📚 Continue estudando. A prática leva à perfeição!")
        print("="*60)

    def _oferecer_revisao(self) -> None:
        """Permite revisar respostas usando a Pilha (histórico)."""
        if self.pilha_historico.is_empty():
            return
            
        while True:
            escolha = input("\n🔍 Deseja revisar suas respostas? (S/N): ").strip().upper()
            if escolha in ["S", "N"]:
                break
            print("⚠️ Digite S ou N.")

        if escolha == "N":
            return

        print("\n📖 REVISÃO (ordem inversa - Pilha LIFO):")
        print("-" * 50)
        # Cria uma cópia para não destruir a pilha original
        revisao_temp = Pilha()
        while not self.pilha_historico.is_empty():
            revisao_temp.push(self.pilha_historico.pop())

        while not revisao_temp.is_empty():
            reg = revisao_temp.pop()
            status = "✅" if reg["acertou"] else "❌"
            print(f"{status} {reg['pergunta']}")
            print(f"   Sua resposta: {reg['sua_resposta']} | Correta: {reg['correta']}")
            print("-" * 50)

    def cadastrar_nova_pergunta_interativa(self) -> None:
        """Permite adicionar perguntas durante a execução."""
        print("\n📝 CADASTRO DE NOVA PERGUNTA")
        pid = input("ID único (ex: Q5): ").strip().upper()
        if pid in self.mapa_perguntas:
            print("⚠️ ID já existe. Operação cancelada.")
            return
            
        enunciado = input("Enunciado: ").strip()
        opcoes = []
        for letra in ["A", "B", "C", "D"]:
            opcoes.append(input(f"Opção {letra}: ").strip())
        correta = input("Resposta correta (A/B/C/D): ").strip().upper()
        explicacao = input("Explicação: ").strip()

        self.cadastrar_pergunta({
            "id": pid,
            "enunciado": enunciado,
            "opcoes": [f"{l}) {op}" for l, op in zip(["A","B","C","D"], opcoes)],
            "resposta_correta": correta,
            "explicacao": explicacao
        })
        print("✅ Pergunta cadastrada com sucesso!")


# ==========================================
# INTERFACE PRINCIPAL (MENU)
# ==========================================

def menu_principal(engine: QuizEngine) -> None:
    """Loop de navegação do sistema."""
    while True:
        print("\n" + "="*40)
        print("🧩 MENU PRINCIPAL - QUIZ DS".center(40))
        print("="*40)
        print("1️⃣(1) Iniciar Quiz")
        print("2️⃣(2) Cadastrar Nova Pergunta")
        print("3️⃣(3) Sair")
        
        opcao = input("\n🔹 Escolha uma opção: ").strip()
        
        if opcao == "1":
            engine.iniciar_quiz()
        elif opcao == "2":
            engine.cadastrar_nova_pergunta_interativa()
        elif opcao == "3":
            print("\n👋 Encerrando sistema. Bons estudos!")
            sys.exit()
        else:
            print("\n⚠️ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        # Inicializa o motor com as estruturas de dados
        quiz = QuizEngine()
        # Executa o menu interativo
        menu_principal(quiz)
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema interrompido pelo usuário.")
        sys.exit(0)
