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
            opt = input("\n[1] Novo Argumento  [2] Sair\n> ")
            if opt == '1':
                return
            elif opt == '2':
                sys.exit(0)

    # Loop principal da aplicação
    def run(self):
        while True:
            self.limpar()
            print("\n" + "="*40)
            print("   VERIFICADOR LÓGICO")
            print("="*40)
            print("1. Lógica Proposicional")
            print("2. Lógica de Predicados")
            print("3. Sair")
            
            choice = input("> ")
            if choice == '3': break
            if choice not in ['1', '2']: continue
            
            try:
                if choice == '2':
                    d_in = self.obter_entrada("Domínio (ex: a,b,c): ", obrigatorio=True)
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