import re
from logic_ast import *

# Classe responsável por ler o texto e transformar em objetos lógicos (AST)
class ParserLogico:
    
    # Inicializa o parser e define a expressão regular para identificar tokens
    def __init__(self):
        # Regex para capturar conectivos, parênteses e identificadores
        self.padrao_token = re.compile(r'\s*(<->|->|&|\||~|\(|\)|,|forall|exists|[a-zA-Z0-9_]+)\s*')
        self.tokens = []
        self.pos = 0

    # Divide a string de entrada em uma lista de tokens
    def tokenizar(self, texto):
        self.tokens = [t for t in self.padrao_token.findall(texto) if t.strip()]
        self.pos = 0

    # Retorna o token atual sem avançar o cursor (lookahead)
    def token_atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    # Verifica se o token atual é o esperado e avança para o próximo
    def consumir(self, esperado=None):
        token = self.token_atual()
        if token is None:
            return None
        if esperado and token != esperado:
            raise SyntaxError(f"Esperado '{esperado}', encontrado '{token}'")
        self.pos += 1
        return token

    # Método principal: tokeniza e inicia a análise sintática
    def analisar(self, texto):
        self.tokenizar(texto)
        resultado = self.analisar_bicondicional()
        # Verifica se sobrou algo após a análise (erro de sintaxe)
        if self.pos < len(self.tokens):
            raise SyntaxError(f"Token inesperado no final: {self.token_atual()}")
        return resultado

    # Analisa expressões bicondicionais (<->) - Menor precedência
    def analisar_bicondicional(self):
        esquerda = self.analisar_implicacao()
        while self.token_atual() == '<->':
            self.consumir()
            direita = self.analisar_implicacao()
            esquerda = Bicondicional(esquerda, direita)
        return esquerda

    # Analisa implicações (->)
    def analisar_implicacao(self):
        esquerda = self.analisar_disjuncao()
        if self.token_atual() == '->':
            self.consumir()
            direita = self.analisar_implicacao() 
            esquerda = Implica(esquerda, direita)
        return esquerda

    # Analisa disjunções (|)
    def analisar_disjuncao(self):
        esquerda = self.analisar_conjuncao()
        while self.token_atual() == '|':
            self.consumir()
            direita = self.analisar_conjuncao()
            esquerda = Ou(esquerda, direita)
        return esquerda

    # Analisa conjunções (&)
    def analisar_conjuncao(self):
        esquerda = self.analisar_unario()
        while self.token_atual() == '&':
            self.consumir()
            direita = self.analisar_unario()
            esquerda = E(esquerda, direita)
        return esquerda

    # Analisa operadores unários (Negação e Quantificadores)
    def analisar_unario(self):
        token = self.token_atual()
        if token == '~':
            self.consumir()
            return Nao(self.analisar_unario())
        elif token == 'forall':
            self.consumir()
            var = self.consumir()
            return ParaTodo(var, self.analisar_unario())
        elif token == 'exists':
            self.consumir()
            var = self.consumir()
            return Existe(var, self.analisar_unario())
        else:
            return self.analisar_atomico()

    # Analisa elementos atómicos (Símbolos, Predicados e Parênteses)
    def analisar_atomico(self):
        token = self.token_atual()
        if token == '(':
            self.consumir()
            expr = self.analisar_bicondicional()
            self.consumir(')')
            return expr
        else:
            nome = self.consumir()
            # Se vier um '(', é um predicado com argumentos: P(a,b)
            if self.token_atual() == '(':
                self.consumir('(')
                args = []
                while self.token_atual() != ')':
                    args.append(self.consumir())
                    if self.token_atual() == ',':
                        self.consumir(',')
                self.consumir(')')
                return Predicado(nome, tuple(args))
            # Caso contrário, é apenas um símbolo: P
            return Simbolo(nome)