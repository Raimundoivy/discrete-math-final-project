# Sistema Automatizado de Verificação de Argumentos Lógicos

> Um sistema robusto desenvolvido em Python para validação de argumentos em Lógica Proposicional e Lógica de Predicados de Primeira Ordem (sobre domínios finitos).

Este projeto utiliza uma arquitetura modular baseada em Árvores de Sintaxe Abstrata (AST) e Parsing Recursivo Descendente, sem dependências externas.

## Funcionalidades

### 1. Lógica Proposicional

*   **Parser Completo**: Suporte a operadores de Negação (`~`), Conjunção (`&`), Disjunção (`|`), Implicação (`->`) e Bicondicional (`<->`).
*   **Tabela Verdade Automatizada**: Gera e exibe tabelas verdade completas para validação semântica.
*   **Reconhecimento de Padrões**: Identifica automaticamente formas lógicas clássicas:
    *   **Válidos**: *Modus Ponens*, *Modus Tollens*, *Silogismo Hipotético*, *Silogismo Disjuntivo*.
    *   **Falácias**: *Afirmação do Consequente*, *Negação do Antecedente*.

### 2. Lógica de Predicados

*   **Quantificadores**: Suporte aos comandos `forall` (Universal) e `exists` (Existencial).
*   **Expansão de Domínio Finito**: Converte predicados em proposições compostas baseadas em um domínio fornecido pelo usuário (ex: `{a, b, c}`).
*   **Silogismos Aristotélicos**: Identificação automática de formas como *Barbara*, *Celarent* e *Darii*.


## Como Executar

### Pré-requisitos

*   Python 3.10 ou superior (O código utiliza a instrução `match/case`).

### Instalação

O projeto não possui dependências externas (bibliotecas do `pip`). Apenas a biblioteca padrão do Python é utilizada.

1.  Clone o repositório:
    ```sh
    git clone https://github.com/Raimundoivy/discrete-math-final-project.git
    ```
2.  Navegue até o diretório do projeto:
    ```sh
    cd discrete-math-project
    ```
3.  Execute o arquivo principal:
    ```sh
    python main.py
    ```

## Guia de Sintaxe

Ao inserir premissas e conclusões no terminal, utilize a seguinte notação:

| Operador      | Símbolo | Exemplo                    |
|---------------|:-------:|----------------------------|
| Negação       | `~`     | `~P`, `~Mortal(x)`         |
| Conjunção (E) | `&`     | `P & Q`                    |
| Disjunção (OU)| `|`     | `P | Q`                    |
| Implicação    | `->`    | `P -> Q`                   |
| Bicondicional | `<->`   | `P <-> Q`                  |
| Para Todo     | `forall`| `forall x (H(x) -> M(x))`  |
| Existe        | `exists`| `exists x (P(x) & Q(x))`   |

## Arquitetura do Projeto

O sistema foi desenhado seguindo princípios de **Separação de Preocupações (SoC)**:

```
discrete-math-project/
├── main.py              # Camada de Apresentação (CLI) e orquestração.
├── logic_ast.py         # Modelo de Dados: Define a estrutura da árvore (Dataclasses).
├── logic_parser.py      # Camada de Análise: Transforma texto bruto em objetos AST.
├── logic_verifier.py    # Camada de Lógica: Motor de inferência e tabelas verdade.
├── logic_forms.py       # Reconhecimento de Padrões: Identifica regras de inferência.
```

### Decisões Técnicas

*   **Imutabilidade**: As classes da AST (`logic_ast.py`) utilizam `@dataclass(frozen=True)` para garantir a integridade dos dados durante a recursão.
*   **Recursive Descent Parser**: O parser (`logic_parser.py`) foi implementado manualmente para lidar com a precedência de operadores e aninhamento de parênteses sem depender de bibliotecas externas como `ply` ou `antlr`.
*   **Duck Typing & Pattern Matching**: Uso extensivo de `match/case` (Python 3.10+) para percorrer a árvore de forma limpa e legível.

## Exemplos de Teste

### Exemplo 1: Modus Ponens

*   **Premissas**: `P -> Q`, `P`
*   **Conclusão**: `Q`
*   **Resultado Esperado**: `VÁLIDO` (Forma identificada: Modus Ponens).

### Exemplo 2: Lógica de Predicados (Sócrates)

*   **Domínio**: `socrates, platao`
*   **Premissas**:
    1.  `forall x (Homem(x) -> Mortal(x))`
    2.  `Homem(socrates)`
*   **Conclusão**: `Mortal(socrates)`
*   **Resultado Esperado**: `VÁLIDO` (Expansão no domínio finito confirma a tautologia).

## Autor

*   Desenvolvido como parte da disciplina de Matemática Discreta.
*   **Ciência da Computação**: [Raimundo, Júlia, Marco Vinícius, Guilherme, Gabriele, Miguel]
*   **03**: Dezembro/2025