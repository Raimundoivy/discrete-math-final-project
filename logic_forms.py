from logic_ast import *

class IdentificadorFormas:
    
    def identificar(self, premissas, conclusao):
        if len(premissas) == 2:
            # Tenta formas proposicionais primeiro
            res = self._analisar_duas_premissas(premissas, conclusao)
            if res != "Forma Genérica / Não Identificada":
                return res
            # Se falhar, tenta silogismos (Lógica de Predicados)
            return self._analisar_silogismos(premissas, conclusao)
        
        # Suporte futuro para Sorites ou argumentos complexos
        if len(premissas) >= 3:
            return "Argumento Complexo (3+ premissas)"
            
        return "Forma Genérica / Não Identificada"

    def _analisar_duas_premissas(self, premissas, conclusao):
        p1, p2 = premissas[0], premissas[1]
        
        condicional = None
        outra = None
        
        # Identificação de Condicionais (Modus Ponens/Tollens)
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

        # Silogismo Hipotético
        if isinstance(p1, Implica) and isinstance(p2, Implica) and isinstance(conclusao, Implica):
            if p1.direita == p2.esquerda:
                if conclusao.esquerda == p1.esquerda and conclusao.direita == p2.direita:
                    return "Silogismo Hipotético (Válido)"
            if p2.direita == p1.esquerda:
                if conclusao.esquerda == p2.esquerda and conclusao.direita == p1.direita:
                    return "Silogismo Hipotético (Válido)"

        # Silogismo Disjuntivo
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

    def _analisar_silogismos(self, premissas, conclusao):
        """
        Analisa Silogismos Aristotélicos (Barbara, Celarent, Darii, Ferio).
        Estrutura básica: Quantificador(Var, Implica/E(Sujeito, Predicado))
        """
        def extrair_termos_universal(f):
            # ParaTodo(x, S(x) -> P(x)) retorna (S, P, True)
            # ParaTodo(x, S(x) -> ~P(x)) retorna (S, P, False) [Universal Negativa]
            if isinstance(f, ParaTodo) and isinstance(f.corpo, Implica):
                subj = f.corpo.esquerda
                pred = f.corpo.direita
                positivo = True
                if isinstance(pred, Nao):
                    pred = pred.operando
                    positivo = False
                return (str(subj), str(pred), positivo)
            return None

        def extrair_termos_existencial(f):
            # Existe(x, S(x) & P(x))
            if isinstance(f, Existe) and isinstance(f.corpo, E):
                subj = f.corpo.esquerda
                pred = f.corpo.direita
                positivo = True
                if isinstance(pred, Nao):
                    pred = pred.operando
                    positivo = False
                return (str(subj), str(pred), positivo)
            return None

        p1, p2 = premissas[0], premissas[1]
        
        # Tenta extrair estrutura das premissas (assume-se predicados unários simples P(x))
        # Simplificação: comparamos as strings de representação dos predicados (ex: "P(x)")
        
        uni_p1 = extrair_termos_universal(p1)
        uni_p2 = extrair_termos_universal(p2)
        uni_con = extrair_termos_universal(conclusao)
        
        ext_p1 = extrair_termos_existencial(p1)
        ext_p2 = extrair_termos_existencial(p2)
        ext_con = extrair_termos_existencial(conclusao)

        # BARBARA (AAA-1): Todo M é P, Todo S é M |- Todo S é P
        if uni_p1 and uni_p2 and uni_con:
            m1, p1_pred, pos1 = uni_p1
            s2, m2, pos2 = uni_p2
            sc, pc, posc = uni_con
            
            if pos1 and pos2 and posc: # Todos positivos
                # Verifica encadeamento do termo médio
                if m1 == m2 and s2 == sc and p1_pred == pc: # (M->P, S->M |- S->P)
                    return "Silogismo: Barbara (Válido)"
                if m2 == m1 and s2 == sc and p1_pred == pc: # Ordem inversa das premissas
                    return "Silogismo: Barbara (Válido)"

        # CELARENT (EAE-1): Nenhum M é P, Todo S é M |- Nenhum S é P
        # Universal Negativa (M->~P), Universal Positiva (S->M), Universal Negativa (S->~P)
        if uni_p1 and uni_p2 and uni_con:
            # Check p1 negative, p2 positive, conc negative
            # Permutação 1: P1 neg, P2 pos
            if not uni_p1[2] and uni_p2[2] and not uni_con[2]:
                m_neg, p_neg, _ = uni_p1
                s_pos, m_pos, _ = uni_p2
                s_conc, p_conc, _ = uni_con
                
                if m_neg == m_pos and s_pos == s_conc and p_neg == p_conc:
                    return "Silogismo: Celarent (Válido)"
            
            # Permutação 2: P2 neg, P1 pos
            if not uni_p2[2] and uni_p1[2] and not uni_con[2]:
                m_neg, p_neg, _ = uni_p2
                s_pos, m_pos, _ = uni_p1
                s_conc, p_conc, _ = uni_con
                
                if m_neg == m_pos and s_pos == s_conc and p_neg == p_conc:
                    return "Silogismo: Celarent (Válido)"

        # DARII (AII-1): Todo M é P, Algum S é M |- Algum S é P
        # Universal Pos, Existencial Pos |- Existencial Pos
        if (uni_p1 and ext_p2 and ext_con) or (uni_p2 and ext_p1 and ext_con):
            uni = uni_p1 if uni_p1 else uni_p2
            ext = ext_p2 if uni_p1 else ext_p1
            
            if uni[2] and ext[2] and ext_con[2]: # Todos positivos
                m_uni, p_uni, _ = uni
                s_ext, m_ext, _ = ext
                s_con, p_con, _ = ext_con
                
                if m_uni == m_ext and s_ext == s_con and p_uni == p_con:
                    return "Silogismo: Darii (Válido)"

        return "Forma Genérica / Não Identificada"