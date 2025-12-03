from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Formula:
    pass

@dataclass(frozen=True)
class Simbolo(Formula):
    nome: str
    
    def __repr__(self):
        return self.nome

@dataclass(frozen=True)
class Predicado(Formula):
    nome: str
    args: Tuple[str, ...]

    def __repr__(self):
        return f"{self.nome}({', '.join(self.args)})"

@dataclass(frozen=True)
class Nao(Formula):
    operando: Formula

    def __repr__(self):
        return f"~{self.operando}"

@dataclass(frozen=True)
class E(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} & {self.direita})"

@dataclass(frozen=True)
class Ou(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} | {self.direita})"

@dataclass(frozen=True)
class Implica(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} -> {self.direita})"

@dataclass(frozen=True)
class Bicondicional(Formula):
    esquerda: Formula
    direita: Formula

    def __repr__(self):
        return f"({self.esquerda} <-> {self.direita})"

@dataclass(frozen=True)
class ParaTodo(Formula):
    var: str
    corpo: Formula

    def __repr__(self):
        return f"(forall {self.var}){self.corpo}"

@dataclass(frozen=True)
class Existe(Formula):
    var: str
    corpo: Formula

    def __repr__(self):
        return f"(exists {self.var}){self.corpo}"