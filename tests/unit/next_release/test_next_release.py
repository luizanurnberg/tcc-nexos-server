import pytest
from service.next_release_service import (
    generate_customer_requirements_dict,
    select_customer,
    can_add,
    can_remove,
    heuristic_construction,
    run_heuristic,
)
from service.pre_process_instance_service import reset, initialize_data, transformation1


@pytest.fixture
def sample_data():
    Q = [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]  # Requisitos para cada cliente
    w = [10, 20, 30]  # Pesos dos clientes
    c = [5, 10, 15, 20, 25]  # Custos dos requisitos
    b = 40  # Orçamento disponível
    n = len(c)  # Número de requisitos
    m = len(w)  # Número de clientes
    return Q, w, c, b, n, m


def test_generate_customer_requirements_dict(sample_data):
    # Arrange
    Q, w, _, _, _, _ = sample_data

    # Act
    customer_requirements = generate_customer_requirements_dict(Q, w)

    # Assert
    assert customer_requirements[0]["weight"] == 10
    assert set(customer_requirements[0]["requirements"]) == {0, 1}
    assert customer_requirements[2]["weight"] == 30


def test_select_customer(sample_data):
    # Arrange
    Q, w, _, _, _, m = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    remaining_customers = list(range(m))

    # Act
    selected_customer = select_customer(remaining_customers, customer_requirements, 1.0)

    # Assert
    assert selected_customer in remaining_customers


def test_can_add(sample_data):
    # Arrange
    Q, w, c, b, _, _ = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    total_cost = 0
    added_requirements = [0] * len(c)

    # Act
    can_add_result, total_cost, added_requirements = can_add(
        0, total_cost, added_requirements, customer_requirements, c, b
    )

    # Assert
    assert can_add_result
    assert total_cost == 15


def test_can_remove(sample_data):
    # Arrange
    Q, w, c, _, _, _ = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    total_cost = 15
    added_requirements = [1, 1, 0, 0, 0]

    # Act
    can_remove_result, total_cost, added_requirements = can_remove(
        0, total_cost, added_requirements, customer_requirements, c
    )

    # Assert
    assert can_remove_result
    assert total_cost == 0


def test_heuristic_construction(sample_data):
    # Arrange
    Q, w, c, b, n, m = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    solution = [0] * m
    added_requirements = [0] * n
    total_cost, selected_customers, obj_value = 0, [], 0

    # Act
    solution, total_cost, selected_customers, added_requirements, obj_value = (
        heuristic_construction(
            customer_requirements,
            solution,
            1.0,
            added_requirements,
            total_cost,
            selected_customers,
            obj_value,
            m,
            c,
            b,
        )
    )

    # Assert
    assert total_cost <= b
    assert sum(solution) > 0


def test_run_heuristic(sample_data):
    # Arrange
    Q, w, c, b, n, m = sample_data

    # Act
    best_solution, best_selected_customers = run_heuristic(
        Q, w, c, b, n, m, 0.11, 0.38, 0.5, 0.1
    )

    # Assert
    assert sum(best_solution) > 0
    assert all(req in range(m) for req in best_selected_customers)


def test_reset():
    instance = reset()
    expected_keys = {"n", "m", "c", "w", "v", "P", "Q", "b", "S"}
    assert isinstance(instance, dict)
    assert set(instance.keys()) == expected_keys
    assert instance["n"] == 0
    assert instance["m"] == 0
    assert instance["c"] == []
    assert instance["w"] == []
    assert instance["v"] == []
    assert instance["P"] == []
    assert instance["Q"] == []
    assert instance["b"] == 0
    assert instance["S"] == []


def test_initialize_data():
    # Arrange
    data = {
        "numberOfReq": 3,
        "numberOfClients": 2,
        "requirements": [
            {
                "id": 0,
                "budget": 10,
                "clientImportance": 3,
                "requirementImportance": 5,
                "clientId": 1,
            },
            {
                "id": 1,
                "budget": 20,
                "clientImportance": 2,
                "requirementImportance": 3,
                "clientId": 0,
            },
            {
                "id": 2,
                "budget": 15,
                "clientImportance": 4,
                "requirementImportance": 2,
                "clientId": 1,
            },
        ],
        "projectBudget": 100,
        "dependencyMatrix": ["0 1", "1 2"],
    }

    # Act
    instance = initialize_data(data)

    # Assert
    assert instance["n"] == 3
    assert instance["m"] == 2
    assert instance["c"] == [10, 20, 15]
    assert instance["w"] == [3, 2, 4]
    assert instance["v"] == [5, 3, 2]
    assert instance["Q"] == [(0, 1), (1, 0), (2, 1)]
    assert instance["b"] == 100
    assert instance["P"] == [(0, 1), (1, 2)]
    assert instance["S"] == [[1], [0], [1]]


def test_transformation1():
    # Arrange
    instance = {
        "n": 3,
        "m": 2,
        "c": [10, 20, 15],
        "w": [3, 2, 4],
        "v": [5, 3, 2],
        "P": [(0, 1), (1, 2)],  # Dependências entre requisitos
        "Q": [(2, 1)],  # O requisito 2 é solicitado pelo cliente 1
        "b": 100,
        "S": [[], [], [1]],  # Inicialmente, apenas o req 2 tem um cliente associado
    }

    # Act
    transformation1(instance)

    # Assert
    # Como 2 depende de 1 e 1 depende de 0, o cliente 1 deve ser propagado para 0 e 1 também
    assert sorted(instance["Q"]) == [(0, 1), (1, 1), (2, 1)]
    assert instance["S"] == [[1], [1], [1]]
