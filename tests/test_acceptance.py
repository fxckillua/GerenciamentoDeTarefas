from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Restante do código do teste aqui


def test_fluxo_completo_gerenciamento_tarefas():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000")

    # Cadastro de tarefa
    driver.find_element_by_name("titulo").send_keys("Título")
    driver.find_element_by_name("descricao").send_keys("Descrição")
    driver.find_element_by_name("responsavel").send_keys("Usuário1")
    driver.find_element_by_name("data_vencimento").send_keys("2024-07-01")
    driver.find_element_by_name("prioridade").send_keys("Alta")
    driver.find_element_by_id("cadastrar").click()

    # Verificar cadastro
    tarefas = driver.find_elements_by_class_name("tarefa")
    assert len(tarefas) == 1
    assert "Título" in tarefas[0].text

    # Editar tarefa
    driver.find_element_by_id("editar").click()
    driver.find_element_by_name("titulo").clear()
    driver.find_element_by_name("titulo").send_keys("Novo Título")
    driver.find_element_by_id("salvar").click()

    # Verificar edição
    tarefas = driver.find_elements_by_class_name("tarefa")
    assert "Novo Título" in tarefas[0].text

    # Remover tarefa
    driver.find_element_by_id("remover").click()

    # Verificar remoção
    tarefas = driver.find_elements_by_class_name("tarefa")
    assert len(tarefas) == 0

    driver.quit()
