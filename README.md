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


## Para executar
- source venv/bin/activate para ativar a venv
- executar sempre o pip freeze > requirements.txt depois de instalar dependencias
- acessar tcc-nexos-server/venv/src e executar python3 -B main.py
- deactivate para desativar a venv 
- para rodar os testes, executar o comando na raiz do projeto PYTHONPATH=venv/src pytest -s tests/
- para verificar o codecoverage PYTHONPATH=venv/src pytest --cov=route.kanban.route
- para remover o pycache find . -type d -name "__pycache__" -exec rm -rf {} +

