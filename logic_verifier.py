import itertools
from logic_ast import *

# Classe responsável por avaliar a validade lógica e gerar tabelas verdade
class VerificadorLogico:
    
    # Percorre a fórmula recursivamente para encontrar todas as variáveis/símbolos únicos
    def obter_variaveis(self, formula: Formula):
        match formula:
            case Simbolo(nome): return {nome}
            case Predicado(nome, args): return {str(formula)} # Trata predicado completo como variável proposicional
            case Nao(op): return self.obter_variaveis(op)
            case E(l, r) | Ou(l, r) | Implica(l, r) | Bicondicional(l, r):
                return self.obter_variaveis(l) | self.obter_variaveis(r)
            case ParaTodo(_, corpo) | Existe(_, corpo):
                return self.obter_variaveis(corpo)
            case _: return set()

    # Calcula o valor de verdade (True/False) de uma fórmula dada uma atribuição
    def avaliar(self, formula: Formula, atribuicao):
        match formula:
            case Simbolo(nome): 
                return atribuicao.get(nome, False)
            case Predicado(nome, args):
                chave = str(formula)
                return atribuicao.get(chave, False)
            case Nao(op): return not self.avaliar(op, atribuicao)
            case E(l, r): return self.avaliar(l, atribuicao) and self.avaliar(r, atribuicao)
            case Ou(l, r): return self.avaliar(l, atribuicao) or self.avaliar(r, atribuicao)
            case Implica(l, r): return (not self.avaliar(l, atribuicao)) or self.avaliar(r, atribuicao)
            case Bicondicional(l, r): return self.avaliar(l, atribuicao) == self.avaliar(r, atribuicao)
            case _: raise ValueError(f"Formula desconhecida: {formula}")

    # Gera todos os dados da tabela verdade para verificar validade do argumento
    def construir_tabela_verdade(self, premissas, conclusao):
        # 1. Identificar todas as variáveis
        todas_vars = set()
        formulas = premissas + [conclusao]
        for f in formulas:
            todas_vars.update(self.obter_variaveis(f))
        vars_ordenadas = sorted(list(todas_vars))

        cabecalhos = vars_ordenadas + [str(p) for p in premissas] + ["PREMISSAS (ALL)", str(conclusao), "Valido?"]
        linhas = []
        eh_valido = True

        # 2. Gerar todas as combinações de V/F (True/False)
        for valores in itertools.product([True, False], repeat=len(vars_ordenadas)):
            atribuicao = dict(zip(vars_ordenadas, valores))
            
            dados_linha = list(valores)
            
            # Avaliar cada premissa
            evals_premissas = [self.avaliar(p, atribuicao) for p in premissas]
            dados_linha.extend(evals_premissas)
            
            # Verificar se todas as premissas são verdadeiras nesta linha
            todas_premissas_verdadeiras = all(evals_premissas)
            dados_linha.append(todas_premissas_verdadeiras)
            
            # Avaliar a conclusão
            eval_conclusao = self.avaliar(conclusao, atribuicao)
            dados_linha.append(eval_conclusao)
            
            # Verificar validade da linha (Premissas V -> Conclusão V)
            status_linha = "-"
            if todas_premissas_verdadeiras:
                if eval_conclusao:
                    status_linha = "OK"
                else:
                    status_linha = "INVALIDO" 
                    eh_valido = False # Se houver uma linha inválida, o argumento todo é inválido
            
            dados_linha.append(status_linha)
            linhas.append(dados_linha)

        return cabecalhos, linhas, eh_valido

    # Substitui uma variável livre por um valor específico (usado na expansão de quantificadores)
    def substituir(self, formula: Formula, nome_var: str, substituto: str) -> Formula:
        match formula:
            case Simbolo(nome): 
                return Simbolo(substituto) if nome == nome_var else formula
            case Predicado(nome, args):
                novos_args = tuple(substituto if a == nome_var else a for a in args)
                return Predicado(nome, novos_args)
            case Nao(op): return Nao(self.substituir(op, nome_var, substituto))
            case E(l, r): return E(self.substituir(l, nome_var, substituto), self.substituir(r, nome_var, substituto))
            case Ou(l, r): return Ou(self.substituir(l, nome_var, substituto), self.substituir(r, nome_var, substituto))
            case Implica(l, r): return Implica(self.substituir(l, nome_var, substituto), self.substituir(r, nome_var, substituto))
            case Bicondicional(l, r): return Bicondicional(self.substituir(l, nome_var, substituto), self.substituir(r, nome_var, substituto))
            case ParaTodo(v, b): 
                # Não substitui se a variável for mascarada por um novo quantificador
                return ParaTodo(v, self.substituir(b, nome_var, substituto)) if v != nome_var else formula
            case Existe(v, b): 
                return Existe(v, self.substituir(b, nome_var, substituto)) if v != nome_var else formula
            case _: return formula

    # Transforma fórmulas com quantificadores em cadeias de E/Ou baseadas no domínio finito
    def expandir_quantificadores(self, formula: Formula, dominio):
        match formula:
            case ParaTodo(var, corpo):
                # ParaTodo v vira: Corpo(v1) E Corpo(v2) E ...
                partes = [self.expandir_quantificadores(self.substituir(corpo, var, val), dominio) for val in dominio]
                if not partes: return Simbolo("True")
                res = partes[0]
                for p in partes[1:]: res = E(res, p)
                return res
            case Existe(var, corpo):
                # Existe v vira: Corpo(v1) OU Corpo(v2) OU ...
                partes = [self.expandir_quantificadores(self.substituir(corpo, var, val), dominio) for val in dominio]
                if not partes: return Simbolo("False")
                res = partes[0]
                for p in partes[1:]: res = Ou(res, p)
                return res
            case Nao(op): return Nao(self.expandir_quantificadores(op, dominio))
            case E(l, r): return E(self.expandir_quantificadores(l, dominio), self.expandir_quantificadores(r, dominio))
            case Ou(l, r): return Ou(self.expandir_quantificadores(l, dominio), self.expandir_quantificadores(r, dominio))
            case Implica(l, r): return Implica(self.expandir_quantificadores(l, dominio), self.expandir_quantificadores(r, dominio))
            case Bicondicional(l, r): return Bicondicional(self.expandir_quantificadores(l, dominio), self.expandir_quantificadores(r, dominio))
            case _: return formula