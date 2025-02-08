import pytest
from service.next_release_service import (
    generate_customer_requirements_dict,
    select_customer,
    can_add,
    can_remove,
    heuristic_construction,
    run_heuristic,
)

@pytest.fixture
def sample_data():
    Q = [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]  # Requisitos para cada cliente
    w = [10, 20, 30]  # Pesos dos clientes
    c = [5, 10, 15, 20, 25]  # Custos dos requisitos
    b = 40  # Orçamento disponível
    n = len(c)  # Número de requisitos
    m = len(w)  # Número de clientes
    return Q, w, c, b, n, m

# Teste para verificar a geração do dicionário de requisitos por cliente
def test_generate_customer_requirements_dict(sample_data):
    Q, w, _, _, _, _ = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    assert customer_requirements[0]['weight'] == 10  # Cliente 0 tem peso 10
    assert set(customer_requirements[0]['requirements']) == {0, 1}  # Cliente 0 tem requisitos 0 e 1
    assert customer_requirements[2]['weight'] == 30  # Cliente 2 tem peso 30

# Teste para verificar a seleção de um cliente baseado no peso
def test_select_customer(sample_data):
    Q, w, _, _, _, m = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    remaining_customers = list(range(m))
    selected_customer = select_customer(remaining_customers, customer_requirements, 1.0)
    assert selected_customer in remaining_customers  # Cliente deve estar na lista original

# Teste para verificar se um cliente pode ser adicionado respeitando orçamento
def test_can_add(sample_data):
    Q, w, c, b, _, _ = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    total_cost = 0
    added_requirements = [0] * len(c)
    can_add_result, total_cost, added_requirements = can_add(0, total_cost, added_requirements, customer_requirements, c, b)
    assert can_add_result  # Deve ser possível adicionar o cliente 0
    assert total_cost == 15  # Custos dos requisitos 0 e 1

# Teste para verificar remoção de um cliente e ajuste do custo
def test_can_remove(sample_data):
    Q, w, c, _, _, _ = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    total_cost = 15
    added_requirements = [1, 1, 0, 0, 0]
    can_remove_result, total_cost, added_requirements = can_remove(0, total_cost, added_requirements, customer_requirements, c)
    assert can_remove_result  # Deve ser possível remover o cliente 0
    assert total_cost == 0  # Custo deve voltar para zero

# Teste para verificar construção heurística
def test_heuristic_construction(sample_data):
    Q, w, c, b, n, m = sample_data
    customer_requirements = generate_customer_requirements_dict(Q, w)
    solution = [0] * m
    added_requirements = [0] * n
    total_cost, selected_customers, obj_value = 0, [], 0
    solution, total_cost, selected_customers, added_requirements, obj_value = heuristic_construction(
        customer_requirements, solution, 1.0, added_requirements, total_cost, selected_customers, obj_value, m, c, b)
    assert total_cost <= b  # Total gasto deve ser menor ou igual ao orçamento
    assert sum(solution) > 0  # Pelo menos um cliente deve ser selecionado

# Teste para verificar execução completa da heurística
def test_run_heuristic(sample_data):
    Q, w, c, b, n, m = sample_data
    best_solution, best_selected_customers = run_heuristic(Q, w, c, b, n, m, 0.11, 0.38, 0.5, 0.1)
    assert sum(best_solution) > 0  # Deve haver pelo menos um cliente selecionado
    assert all(req in range(m) for req in best_selected_customers)  # Clientes selecionados devem estar dentro do limite