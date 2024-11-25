# Projeto de Cloud - João Chade

## Parte 1:
- Na parte 1 do projeto, foi feita a construção de uma API RESTful (usei FastAPI), capaz de cadastrar e autenticar usuários, além de permitir a consulta de dados de terceiros. Para isso, foram usados 3 endpoints (POST registrar, POST login e GET - para consultar a API "Geek Jokes"). Todas as etapas foram feitas considerando um **jwt token**, que era verificado antes das requisições.

- Em seguida, o projeto foi Dockerizado, com o uso de um Dockerfile e um compose.yaml. Para isso, o docker compose contém a aplicação que foi feita, e o banco de dados, para que as interações possam ser feitas.

- Por fim, o projeto foi publicado no Docker Hub.

### Uso da aplicação:
1. O novo usuário é criado no endpoint "Registrar", a partir de "nome", "email" e "senha". Em caso de sucesso, você deve receber como retorno um jwt token
2. Em seguida, opcionalmente, usando o endpoint "Login", você consegue logar com o seu email e senha criados anteriormente. Novamente, como resposta você receberá o mesmo jwt token da etapa anterior
3. Por fim, é necessário ir em "Authorize", no canto superior direito, e inserir seu email e senha. Assim, uma vez autorizado, você pode fazer requests no endpoint GET, e receber como retorno uma piada geek!

Link do funcionamento e uso da aplicação: https://www.youtube.com/watch?v=67Fg_k9zV-c
Link para o DockerHub do projeto: https://hub.docker.com/repository/docker/joaochade123/cloud/general
Link API de piadas usada: https://geek-jokes.sameerkumar.website/api?format=json
