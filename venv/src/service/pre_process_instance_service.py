def reset():
    return {
        "n": 0,  # number of requirements
        "m": 0,  # number of customers
        "c": [],  # costs of requirements
        "w": [],  # weights/profits of customers
        "v": [],  # weights of requirements given by customers (can be a n x m matrix or a n vector)
        "P": [],  # set of pairs (i,j) where requirement i is a prerequisite of requirement j
        "Q": [],  # set of pairs (i,k) where requirement i is requested by customer k
        "f": 0.7,  # multiplication factor to compute b
        "b": 0,  # budget
        "S": [],  # set of customers associated with each requirement
    }


def initialize_data(data):
    instance = reset()

    print("data:", data)

    instance["n"] = data.get("numberOfReq")
    instance["m"] = data.get("numberOfClients")

    instance["c"] = [int(req["budget"]) for req in data.get("requirements", [])]
    instance["w"] = [
        int(req["clientImportance"]) for req in data.get("requirements", [])
    ]
    instance["v"] = [
        int(req["requirementImportance"]) for req in data.get("requirements", [])
    ]

    print(instance["w"])

    # Adiciona o par (requisito, cliente) ao conjunto Q
    for req in data.get("requirements", []):
        client_id = req["client"]
        req_id = int(req["id"])
        instance["Q"].append((req_id, client_id))

    # Cálculo do orçamento
    instance["b"] = sum(instance["c"]) * instance["f"]

    # Monta os pares de dependencia
    dependencies = data.get("dependencyMatrix", [])
    for dep in dependencies:
        values = dep.split()
        i = int(values[0])  # i é o pré-requisito
        j = int(values[1])  # j depende de i
        instance["P"].append((i, j))

    # Ajuste de arredondamento do orçamento
    if instance["b"] - int(instance["b"]) == 0.5:
        instance["b"] += 0.01
    instance["b"] = round(instance["b"])

    # Inicializa a lista de clientes por requisito
    instance["S"] = [[] for _ in range(instance["n"])]  # Inicializa S diretamente com listas vazias
    for req, cus in instance["Q"]:
        instance["S"][req].append(cus)

    print("instance:", instance)
    return instance


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

    instance["S"] = [[] for _ in range(instance["n"])]
    for req, cus in instance["Q"]:
        instance["S"][req].append(cus)
