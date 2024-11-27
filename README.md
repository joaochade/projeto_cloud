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

## Parte 2:
- Na parte 2 do projeto, foi feito o deploy da aplicação na AWS. Para isso, foi necessário criar um cluster EKS (com o nome do cluster, a região e os 2 nodes), configurar o kubectl (passando o cluster e a região), assim como os arquivos .yaml do DB e do APP. Assim, é possível ver os nodes e o cvs, e usar a aplicação "deployada" no seguinte link:

http://ac3cce84cc4e1404abb7695a30a13d75-1579949756.us-east-2.elb.amazonaws.com/docs#/default/consultar_consultar_get

Link para o vídeo de funcionamento da aplicação na AWS: https://www.youtube.com/watch?v=3b4qonVwobg
