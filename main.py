import sys
from logic_parser import ParserLogico
from logic_verifier import VerificadorLogico
from logic_forms import IdentificadorFormas

class AplicacaoLogica:
    def __init__(self):
        self.parser = ParserLogico()
        self.verificador = VerificadorLogico()
        self.identificador_formas = IdentificadorFormas()
        
        self.dominio = []
        self.premissas = []
        self.conclusao = None

    def limpar(self):
        self.dominio = []
        self.premissas = []
        self.conclusao = None

    def obter_entrada(self, prompt, obrigatorio=True):
        while True:
            valor = input(f"{prompt} ").strip()
            if not obrigatorio and not valor: return None
            if valor: return valor
            print("Entrada não pode ser vazia.")

    def imprimir_tabela(self, cabecalhos, linhas):
        larguras = [max(len(str(h)), 7) for h in cabecalhos]
        
        header_str = " | ".join(f"{str(h):^{w}}" for h, w in zip(cabecalhos, larguras))
        sep = "-" * len(header_str)
        
        print("\n" + sep)
        print(header_str)
        print(sep)
        
        for linha in linhas:
            vals = []
            for item in linha:
                if isinstance(item, bool): s = "V" if item else "F"
                else: s = str(item)
                vals.append(s)
            
            print(" | ".join(f"{v:^{w}}" for v, w in zip(vals, larguras)))
        print(sep + "\n")

    def executar_analise(self):
        print("\n=== RELATÓRIO DE ANÁLISE ===")
        
        if not self.dominio: 
            forma = self.identificador_formas.identificar(self.premissas, self.conclusao)
            print(f"[*] Forma Identificada: {forma}")
        else:
            print("[*] Forma: Análise de Predicados com Domínio Finito")

        premissas_ativas = self.premissas
        conclusao_ativa = self.conclusao
        
        if self.dominio:
            print(f"[*] Expandindo quantificadores para domínio: {self.dominio}")
            try:
                premissas_ativas = [self.verificador.expandir_quantificadores(p, self.dominio) for p in self.premissas]
                conclusao_ativa = self.verificador.expandir_quantificadores(self.conclusao, self.dominio)
            except Exception as e:
                print(f"[!] Erro na expansão: {e}")
                return

        cabecalhos, linhas, eh_valido = self.verificador.construir_tabela_verdade(premissas_ativas, conclusao_ativa)
        
        if eh_valido:
            print("\n>>> RESULTADO: ARGUMENTO VÁLIDO <<<")
        else:
            print("\n>>> RESULTADO: ARGUMENTO INVÁLIDO <<<")
            print("Existem linhas onde as Premissas são V e a Conclusão é F.")

        while True:
            opt = input("\n[1] Ver Tabela Completa  [2] Novo Argumento  [3] Sair\n> ")
            if opt == '1':
                self.imprimir_tabela(cabecalhos, linhas)
            elif opt == '2':
                return
            elif opt == '3':
                sys.exit(0)

    def run(self):
        while True:
            self.limpar()
            print("\n" + "="*40)
            print("   VERIFICADOR LÓGICO")
            print("="*40)
            print("1. Lógica Proposicional (P -> Q)")
            print("2. Lógica de Predicados (forall x P(x))")
            print("3. Sair")
            
            choice = input("> ")
            if choice == '3': break
            if choice not in ['1', '2']: continue
            
            try:
                if choice == '2':
                    d_in = self.obter_entrada("Domínio (ex: a,b,c): ")
                    self.dominio = [x.strip() for x in d_in.split(',')]

                qtd = int(self.obter_entrada("Número de Premissas: "))
                print("Sintaxe: use '->', '<->', '&', '|', '~', 'forall x', 'exists x'")
                for i in range(qtd):
                    p_txt = self.obter_entrada(f"Premissa {i+1}: ")
                    self.premissas.append(self.parser.analisar(p_txt))

                c_txt = self.obter_entrada("Conclusão: ")
                self.conclusao = self.parser.analisar(c_txt)
                
                self.executar_analise()

            except Exception as e:
                print(f"\n[Erro] {e}")
                input("Pressione Enter...")

if __name__ == "__main__":
    app = AplicacaoLogica()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nSaindo...")