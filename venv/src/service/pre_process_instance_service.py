def reset():
    return {
        "n": 0,  # número de requisitos
        "m": 0,  # número de clientes
        "c": [],  # custos de implementação dos requisitos
        "w": [],  # pesos/importâncias dos clientes (indicando a relevância de cada cliente) junto com o seu id
        "v": [],  # importâncias dos requisitos fornecidas pelos clientes (pode ser uma matriz n x m ou um vetor n)
        "P": [],  # conjunto de pares (i,j) onde o requisito i é um pré-requisito do requisito j
        "Q": [],  # conjunto de pares (i,k) onde o requisito i é solicitado pelo cliente k
        "b": 0,  # orçamento total (valor calculado)
        "S": [],  # conjunto de clientes associados a cada requisito (índice 0 até n-1)
    }


def initialize_data(data):
    instance = reset()

    # Obtém o número de requisitos e clientes da entrada
    number_of_req = data.get("numberOfReq")
    number_of_clients = data.get("numberOfClients")

    # Define o número de requisitos e clientes na instância
    instance["n"] = number_of_req
    instance["m"] = number_of_clients

    # Define os custos dos requisitos (extraídos do campo "budget" em "requirements")
    instance["c"] = [int(req["budget"]) for req in data.get("requirements", [])]

    # Define a importância/peso dos clientes (extraídos do campo "clientImportance")
    instance["w"] = {
        int(req["clientId"]): int(req["clientImportance"])
        for req in data.get("requirements", [])
    }

    # Define a importância dos requisitos segundo os clientes (extraídos de "requirementImportance")
    instance["v"] = [
        int(req["requirementImportance"]) for req in data.get("requirements", [])
    ]

    # Para cada requisito na entrada, adiciona o par (requisito, cliente) ao conjunto Q
    for req in data.get("requirements", []):
        client_id = int(req["clientId"])
        req_id = int(req["id"])
        instance["Q"].append((req_id, client_id))

    # Cálculo do orçamento total
    instance["b"] = data.get("projectBudget")

    # Monta os pares de dependência (P) a partir da matriz de dependências fornecida
    dependencies = data.get("dependencyMatrix", [])
    for dep in dependencies:
        values = dep.split()
        i = int(values[0])
        j = int(values[1])
        instance["P"].append((i, j))

    # Inicializa a lista de clientes associados a cada requisito (com listas vazias)
    instance["S"] = [[] for _ in range(instance["n"])]
    for req, cus in instance["Q"]:
        instance["S"][req].append(cus)

    print("instance", instance)
    return instance


# Função de transformação para propagar dependências e atualizar Q e S
def transformation1(instance):
    novel = True
    while novel:
        novel = False
        for req, cus in instance["Q"]:
            for reqi, reqj in instance["P"]:
                if req == reqj:
                    if (reqi, cus) not in instance["Q"]:
                        instance["Q"].append((reqi, cus))
                        novel = True

    # Atualiza o conjunto S, associando os clientes aos requisitos após a transformação
    instance["S"] = [[] for _ in range(instance["n"])]
    for req, cus in instance["Q"]:
        instance["S"][req].append(cus)
