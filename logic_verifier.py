import itertools
from logic_ast import *

class VerificadorLogico:
    
    def obter_variaveis(self, formula: Formula):
        match formula:
            case Simbolo(nome): return {nome}
            case Predicado(nome, args): return {str(formula)}
            case Nao(op): return self.obter_variaveis(op)
            case E(l, r) | Ou(l, r) | Implica(l, r) | Bicondicional(l, r):
                return self.obter_variaveis(l) | self.obter_variaveis(r)
            case ParaTodo(_, corpo) | Existe(_, corpo):
                return self.obter_variaveis(corpo)
            case _: return set()

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

    def construir_tabela_verdade(self, premissas, conclusao):
        """
        Generates full truth table data.
        Returns: (headers, rows, is_valid)
        """
        todas_vars = set()
        formulas = premissas + [conclusao]
        for f in formulas:
            todas_vars.update(self.obter_variaveis(f))
        vars_ordenadas = sorted(list(todas_vars))

        cabecalhos = vars_ordenadas + [str(p) for p in premissas] + ["PREMISSAS (ALL)", str(conclusao), "Valido?"]
        linhas = []
        eh_valido = True

        for valores in itertools.product([True, False], repeat=len(vars_ordenadas)):
            atribuicao = dict(zip(vars_ordenadas, valores))
            
            dados_linha = list(valores)
            
            evals_premissas = [self.avaliar(p, atribuicao) for p in premissas]
            dados_linha.extend(evals_premissas)
            
            todas_premissas_verdadeiras = all(evals_premissas)
            dados_linha.append(todas_premissas_verdadeiras)
            
            eval_conclusao = self.avaliar(conclusao, atribuicao)
            dados_linha.append(eval_conclusao)
            
            status_linha = "-"
            if todas_premissas_verdadeiras:
                if eval_conclusao:
                    status_linha = "OK"
                else:
                    status_linha = "INVALIDO" 
                    eh_valido = False
            
            dados_linha.append(status_linha)
            linhas.append(dados_linha)

        return cabecalhos, linhas, eh_valido

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
                return ParaTodo(v, self.substituir(b, nome_var, substituto)) if v != nome_var else formula
            case Existe(v, b): 
                return Existe(v, self.substituir(b, nome_var, substituto)) if v != nome_var else formula
            case _: return formula

    def expandir_quantificadores(self, formula: Formula, dominio):
        match formula:
            case ParaTodo(var, corpo):
                partes = [self.expandir_quantificadores(self.substituir(corpo, var, val), dominio) for val in dominio]
                if not partes: return Simbolo("True")
                res = partes[0]
                for p in partes[1:]: res = E(res, p)
                return res
            case Existe(var, corpo):
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