from dataclasses import dataclass
from typing import Tuple

# Classe base para todas as fórmulas lógicas
@dataclass(frozen=True)
class Formula:
    pass

# Representa um símbolo atómico (ex: P, Q)
@dataclass(frozen=True)
class Simbolo(Formula):
    nome: str
    
    # Retorna a representação em string do símbolo
    def __repr__(self):
        return self.nome

# Representa um predicado com argumentos (ex: H(x), Mortal(socrates))
@dataclass(frozen=True)
class Predicado(Formula):
    nome: str
    args: Tuple[str, ...]

    # Retorna a representação em string do predicado (ex: "P(a, b)")
    def __repr__(self):
        return f"{self.nome}({', '.join(self.args)})"

# Representa a operação de Negação (~)
@dataclass(frozen=True)
class Nao(Formula):
    operando: Formula

    def __repr__(self):
        return f"~{self.operando}"

# Representa a operação E (Conjunção)
@dataclass(frozen=True)
class E(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} & {self.direita})"

# Representa a operação Ou (Disjunção)
@dataclass(frozen=True)
class Ou(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} | {self.direita})"

# Representa a Implicação (->)
@dataclass(frozen=True)
class Implica(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} -> {self.direita})"

# Representa a Bicondicional (<->)
@dataclass(frozen=True)
class Bicondicional(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} <-> {self.direita})"

# Representa o quantificador Universal (Para Todo / forall)
@dataclass(frozen=True)
class ParaTodo(Formula):
    var: str
    corpo: Formula

    def __repr__(self):
        return f"(forall {self.var}){self.corpo}"

# Representa o quantificador Existencial (Existe / exists)
@dataclass(frozen=True)
class Existe(Formula):
    var: str
    corpo: Formula

    def __repr__(self):
        return f"(exists {self.var}){self.corpo}"