from logic_ast import *

class IdentificadorFormas:
    
    def identificar(self, premissas, conclusao):
        if len(premissas) == 2:
            return self._analisar_duas_premissas(premissas, conclusao)
        
        if len(premissas) == 3:
            pass 
            
        return "Forma Genérica / Não Identificada"

    def _analisar_duas_premissas(self, premissas, conclusao):
        p1, p2 = premissas[0], premissas[1]
        
        condicional = None
        outra = None
        
        if isinstance(p1, Implica):
            condicional = p1
            outra = p2
        elif isinstance(p2, Implica):
            condicional = p2
            outra = p1
            
        if condicional:
            if outra == condicional.esquerda and conclusao == condicional.direita:
                return "Modus Ponens (Válido)"
        
        if condicional:
            if isinstance(outra, Nao) and outra.operando == condicional.direita:
                if isinstance(conclusao, Nao) and conclusao.operando == condicional.esquerda:
                    return "Modus Tollens (Válido)"

        if condicional:
            if outra == condicional.direita and conclusao == condicional.esquerda:
                return "FALÁCIA: Afirmação do Consequente (Inválido)"

        if condicional:
             if isinstance(outra, Nao) and outra.operando == condicional.esquerda:
                 if isinstance(conclusao, Nao) and conclusao.operando == condicional.direita:
                     return "FALÁCIA: Negação do Antecedente (Inválido)"

        if isinstance(p1, Implica) and isinstance(p2, Implica) and isinstance(conclusao, Implica):
            if p1.direita == p2.esquerda:
                if conclusao.esquerda == p1.esquerda and conclusao.direita == p2.direita:
                    return "Silogismo Hipotético (Válido)"
            if p2.direita == p1.esquerda:
                if conclusao.esquerda == p2.esquerda and conclusao.direita == p1.direita:
                    return "Silogismo Hipotético (Válido)"

        disjuncao = None
        negacao = None
        
        if isinstance(p1, Ou): disjuncao, negacao = p1, p2
        elif isinstance(p2, Ou): disjuncao, negacao = p2, p1
        
        if disjuncao and isinstance(negacao, Nao):
            if negacao.operando == disjuncao.esquerda and conclusao == disjuncao.direita:
                return "Silogismo Disjuntivo (Válido)"
            if negacao.operando == disjuncao.direita and conclusao == disjuncao.esquerda:
                return "Silogismo Disjuntivo (Válido)"

        return "Forma Genérica / Não Identificada"