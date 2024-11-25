# Projeto de Cloud - João Chade

## Parte 1:
- Na parte 1 do projeto, foi feita a construção de uma API RESTful (usei FastAPI), capaz de cadastrar e autenticar usuários, além de permitir a consulta de dados de terceiros. Para isso, foram usados 3 endpoints (POST registrar, POST login e GET - para consultar a API "Geek Jokes"). Todas as etapas foram feitas considerando um **jwt token**, que era verificado antes das requisições.

- Em seguida, o projeto foi Dockerizado, com o uso de um Dockerfile e um compose.yaml. Para isso, o docker compose contém a aplicação que foi feita, e o banco de dados, para que as interações possam ser feitas.

- Por fim, o projeto foi publicado no Docker Hub.

Link API: https://geek-jokes.sameerkumar.website/api?format=json
