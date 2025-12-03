import sys
from logic_parser import ParserLogico
from logic_verifier import VerificadorLogico
from logic_forms import IdentificadorFormas

# Classe principal que gerencia a interação com o usuário (CLI)
class AplicacaoLogica:
    def __init__(self):
        # Inicializa os módulos auxiliares
        self.parser = ParserLogico()
        self.verificador = VerificadorLogico()
        self.identificador_formas = IdentificadorFormas()
        
        # Estado atual do argumento
        self.dominio = []
        self.premissas = []
        self.conclusao = None

    # Reseta os dados para permitir um novo argumento
    def limpar(self):
        self.dominio = []
        self.premissas = []
        self.conclusao = None

    # Função auxiliar para ler input do usuário com validação
    def obter_entrada(self, prompt, obrigatorio=True):
        while True:
            valor = input(f"{prompt} ").strip()
            if not obrigatorio and not valor: return None
            if valor: return valor
            print("Entrada não pode ser vazia.")

    # Exibe um guia completo de sintaxe
    def exibir_ajuda_sintaxe(self):
        print("\n" + "="*65)
        print("                 GUIA DE SINTAXE E OPERADORES")
        print("="*65)
        print(f"{'TIPO':<15} | {'SÍMBOLO':<10} | {'EXEMPLO':<30}")
        print("-" * 65)
        print(f"{'Negação':<15} | {'~':<10} | {'~P, ~Mortal(x)':<30}")
        print(f"{'Conjunção (E)':<15} | {'&':<10} | {'P & Q':<30}")
        print(f"{'Disjunção (OU)':<15} | {'|':<10} | {'P | Q':<30}")
        print(f"{'Implicação':<15} | {'->':<10} | {'P -> Q':<30}")
        print(f"{'Bicondicional':<15} | {'<->':<10} | {'P <-> Q':<30}")
        print("-" * 65)
        print("QUANTIFICADORES (Lógica de Predicados):")
        print(f"{'Universal':<15} | {'forall':<10} | {'forall x (H(x) -> M(x))':<30}")
        print(f"{'Existencial':<15} | {'exists':<10} | {'exists x (P(x) & Q(x))':<30}")
        print("-" * 65)
        print("DOMÍNIO (Como inserir):")
        print(" Definição: Lista de objetos finitos que as variáveis 'x', 'y' representam.")
        print(" Sintaxe:   Nomes separados por vírgula (sem parênteses ou chaves).")
        print(" Entrada:   pedro, maria, joao")
        print(" Efeito:    'forall x P(x)' será testado como 'P(pedro) & P(maria) & P(joao)'")
        print("-" * 65)
        print("PRECEDÊNCIA (da maior prioridade para a menor):")
        print(" 1. Parênteses ()")
        print(" 2. Negação (~), Quantificadores (forall, exists)")
        print(" 3. Conjunção (&)")
        print(" 4. Disjunção (|)")
        print(" 5. Implicação (->)")
        print(" 6. Bicondicional (<->)")
        print("="*65 + "\n")
        input("Pressione Enter para voltar...")

    # Formata e imprime a tabela verdade no console de forma alinhada
    def imprimir_tabela(self, cabecalhos, linhas):
        larguras = [max(len(str(h)), 7) for h in cabecalhos]
        
        # Cria cabeçalho
        header_str = " | ".join(f"{str(h):^{w}}" for h, w in zip(cabecalhos, larguras))
        sep = "-" * len(header_str)
        
        print("\n" + sep)
        print(header_str)
        print(sep)
        
        # Imprime as linhas de valores
        for linha in linhas:
            vals = []
            for item in linha:
                if isinstance(item, bool): s = "V" if item else "F"
                else: s = str(item)
                vals.append(s)
            
            print(" | ".join(f"{v:^{w}}" for v, w in zip(vals, larguras)))
        print(sep + "\n")

    # Coordena a análise lógica completa
    def executar_analise(self):
        print("\n=== RELATÓRIO DE ANÁLISE ===")
        
        # Tenta identificar o nome da forma lógica (ex: Modus Ponens)
        forma = self.identificador_formas.identificar(self.premissas, self.conclusao)
        print(f"[*] Forma Identificada: {forma}")

        print("[*] Modo: Verificação em Domínio Finito (Tabela Verdade)")
        premissas_ativas = self.premissas
        conclusao_ativa = self.conclusao
        
        # Se houver domínio, expande quantificadores (forall/exists)
        if self.dominio:
            print(f"[*] Expandindo quantificadores para domínio: {self.dominio}")
            try:
                premissas_ativas = [self.verificador.expandir_quantificadores(p, self.dominio) for p in self.premissas]
                conclusao_ativa = self.verificador.expandir_quantificadores(self.conclusao, self.dominio)
            except Exception as e:
                print(f"[!] Erro na expansão: {e}")
                return

        # Gera e avalia a tabela verdade
        cabecalhos, linhas, eh_valido = self.verificador.construir_tabela_verdade(premissas_ativas, conclusao_ativa)
        
        if eh_valido:
            print("\n>>> RESULTADO: ARGUMENTO VÁLIDO <<<")
        else:
            print("\n>>> RESULTADO: ARGUMENTO INVÁLIDO <<<")
            print("Existem linhas onde as Premissas são V e a Conclusão é F.")

        # Imprime automaticamente a tabela completa
        self.imprimir_tabela(cabecalhos, linhas)

        # Menu pós-análise
        while True:
            opt = input("\n[1] Novo Argumento  [2] Voltar ao Menu\n> ")
            if opt == '1':
                return
            elif opt == '2':
                # Apenas sai do método, retornando ao loop run()
                return

    # Loop principal da aplicação
    def run(self):
        while True:
            self.limpar()
            print("\n" + "="*40)
            print("   VERIFICADOR LÓGICO")
            print("="*40)
            print("1. Nova Análise (Proposicional / Predicados)")
            print("2. Guia de Sintaxe")
            print("3. Sair")
            
            choice = input("> ")
            if choice == '3': 
                break
            
            if choice == '2':
                self.exibir_ajuda_sintaxe()
                continue
            
            if choice != '1': 
                continue
            
            # Fluxo de Nova Análise
            try:
                tipo = input("Possui domínio finito (Lógica de Predicados)? (s/n): ").lower().strip()
                
                if tipo == 's':
                    d_in = self.obter_entrada("Domínio (ex: a,b,c): ", obrigatorio=True)
                    self.dominio = [x.strip() for x in d_in.split(',')]

                print("\n--- Inserção de Premissas ---")
                print("(Digite 'ajuda' para ver a sintaxe ou Enter para parar de adicionar premissas)")
                
                # Loop flexível para inserir premissas
                while True:
                    i = len(self.premissas) + 1
                    p_txt = input(f"Premissa {i} (ou Enter p/ encerrar): ").strip()
                    
                    if p_txt.lower() == 'ajuda':
                        self.exibir_ajuda_sintaxe()
                        continue
                    
                    if not p_txt:
                        if len(self.premissas) == 0:
                            print("Adicione pelo menos uma premissa.")
                            continue
                        break
                        
                    try:
                        parsed = self.parser.analisar(p_txt)
                        self.premissas.append(parsed)
                    except Exception as e:
                        print(f"Erro de Sintaxe: {e}")

                c_txt = ""
                while not c_txt:
                    c_txt = input("Conclusão: ").strip()
                    if c_txt.lower() == 'ajuda':
                        self.exibir_ajuda_sintaxe()
                        c_txt = "" # Reseta para pedir de novo
                    elif c_txt:
                        try:
                            self.conclusao = self.parser.analisar(c_txt)
                        except Exception as e:
                            print(f"Erro de Sintaxe: {e}")
                            c_txt = ""
                
                self.executar_analise()

            except Exception as e:
                print(f"\n[Erro Crítico] {e}")
                input("Pressione Enter...")

if __name__ == "__main__":
    app = AplicacaoLogica()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nSaindo...")