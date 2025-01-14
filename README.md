<p align="center">
  <img src="nextReleaseProblem-main/logo.png" alt="NEXOS Logo" width="80" height="80">
</p>

# NEXOS (Next Release Optimization System) - Back

Repositório referente ao back do trabalho de conclusão de curso.

###### Desenvolvedora: Luíza Nurnberg

![Em Desenvolvimento](https://img.shields.io/badge/Status-Em_Desenvolvimento-green)

## Tecnologias Utilizadas
[![Python](https://skillicons.dev/icons?i=python)](https://www.pyhton.com)
[![Mongo](https://skillicons.dev/icons?i=mongo)](https://www.mongodb.com)
[![Firebase](https://skillicons.dev/icons?i=firebase)](https://www.firebase.com)

- acessar tcc-nexos-server/venv/src e executar python3 -B main.py
- executar sempre o pip freeze > requirements.txt depois de instalar dependencias

- source venv/bin/activate para ativar a venv
- deactivate para desativar a venv 

python3 ig.py nrp1.txt 0.7 0.11 0.38 0.5

### Estrutura do arquivo:

1. **Níveis de requisitos**:
   - A primeira linha (`3`) indica o número de níveis de requisitos.
   - Em seguida, os próximos blocos de dados indicam:
     - O número de requisitos em cada nível (`20`, `40`, `80`), ou seja, são 20, 40 e 80 requisitos em três diferentes níveis.
     - A lista de custos para cada requisito nesses níveis, por exemplo:
       - `4 3 4 1 5 5 5 3 5 3 4 4 3 5 1 1 3 2 2 3` são os custos dos 20 primeiros requisitos.
       - `8 8 2 6 7 4 5 3 6 3 7 2 6 3 5 2 2 4 2 5 4 5 2 2 8 4 2 4 8 7 3 6 6 4 3 6 4 8 6 7` para os 40 requisitos do segundo nível.
       - `9 6 10 6 9 10...` para os 80 requisitos do terceiro nível.

2. **Dependências entre requisitos**:
   - O número `97` indica que há 97 dependências entre os requisitos.
   - Cada linha a seguir contém um par de números que indicam a relação de dependência entre dois requisitos. Por exemplo, `1 85` significa que o requisito 1 é um pré-requisito do requisito 85.

3. **Clientes**:
   - O número `100` indica o número de clientes.
   - Para cada cliente, são dados números que indicam:
     - O peso/profit do cliente (o valor que ele gera).
     - Os requisitos que esse cliente solicita. Por exemplo, `36 1 66` indica que o cliente tem um peso de 36 e solicita o requisito 66.

### Função de leitura `read()`:

- **Entrada de níveis e requisitos**:
  - O código lê os três níveis, adiciona os requisitos ao total (`n`), e para cada requisito, atribui um custo a partir das listas fornecidas. A lista `v[]` é inicializada como uma lista de zeros, que depois será atualizada com os valores dos clientes.

- **Dependências**:
  - A lista `P[]` é usada para armazenar as dependências entre os requisitos (como pares `(i, j)`, onde `i` é um pré-requisito para `j`).

- **Clientes e suas requisições**:
  - O código lê os clientes e para cada um, atribui um peso (valor) `w[]`. Em seguida, adiciona os pares `(i, k)` para a lista `Q[]`, onde o requisito `i` é solicitado pelo cliente `k`.

- **Cálculo do orçamento**:
  - O valor `b` é calculado como uma fração (fator) da soma total dos custos dos requisitos, ajustado para evitar erros de arredondamento.

- **Construção de `S[]`**:
  - A lista `S[]` mantém a relação entre requisitos e clientes, sendo uma lista de listas, onde cada índice corresponde a um requisito e contém os clientes que requisitaram esse requisito.

### Transformação `transformation1()`:

- **Propagação de dependências**:
  - A função busca propagar dependências entre requisitos para garantir que, se um cliente solicitar um requisito que depende de outro, o requisito pré-requisito também será incluído na solicitação desse cliente.

### Conclusão

O arquivo define um problema de otimização com:
- **Requisitos**: 20, 40 e 80 requisitos, cada um com um custo associado.
- **Dependências**: Relações entre os requisitos que definem pré-requisitos.
- **Clientes**: Cada cliente tem um peso e solicita um ou mais requisitos.

O código utiliza esses dados para calcular orçamentos, propagar dependências e associar requisitos aos clientes.