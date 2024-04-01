# FastAPI Login with Auth0

## English

This is a Python application developed with FastAPI focusing on demonstrating login using the third-party site Auth0.

Before starting the application, the developer will need to create an account at https://auth0.com/ and start an authentication application of the regular web application type. After this initial step, they should configure the basic config as shown in:

![Auth0 Basic Config](https://github.com/ma_bittar/auth0_example/blob/master/asset/auth0_basic.jpg?raw=true)

And also configure the allowed callback URI, as shown in:

![Auth0 Callback URI Config](https://github.com/ma_bittar/auth0_example/blob/master/asset/auth0_config.png)

To generate the `APP_SECRET_KEY` environment variable, execute the following command in the shell: `openssl rand -hex 32` (for Windows, a similar command can be used, such as `openssl rand -hex 32`). The `AUTHORIZED_EMAIL` variable will be the only email allowed access to the application after user validation.

To initialize the application, follow these steps:

1. Clone the repository.
2. Navigate to the project directory.
3. If necessary, install Python from https://www.python.org/.
4. Create a virtual environment and install dependencies listed in the requirements.txt file.
5. Create a .env file in the root of the project based on the .env-model provided, filling in the necessary information obtained from the Auth0 application panel.
6. Execute the command: `python -m uvicorn src.main:app --reload` to start the application, or use the debug mode of VSCode, which is pre-configured in the project.

## Português

Este é um exemplo de aplicação em Python usando o framework FastAPI para demonstrar como implementar o login utilizando o serviço de autenticação Auth0.

Antes de iniciar, certifique-se de ter uma conta no [Auth0](https://auth0.com/) e criar uma aplicação de autenticação do tipo "regular web application". Após isso, siga as instruções abaixo para configurar o ambiente e executar a aplicação.

![Auth0 Basic Config](https://github.com/ma_bittar/auth0_example/blob/master/asset/auth0_basic.jpg?raw=true)

Configure também a URI de callback para:

![Auth0 Callback URI Config](https://github.com/ma_bittar/auth0_example/blob/master/asset/auth0_config.png)

Para gerar a variável de ambiente `APP_SECRET_KEY`, execute o seguinte comando no terminal: `openssl rand -hex 32` (para Windows, um comando similar pode ser usado, como `openssl rand -hex 32`). A variável `AUTHORIZED_EMAIL` será o único e-mail permitido a acessar a aplicação após a validação do usuário.

Para inicializar a aplicação, siga estes passos:

1. Clone o repositório.
2. Navegue até o diretório do projeto.
3. Caso necessário, instale o Python em https://www.python.org/.
4. Crie um ambiente virtual e instale as dependências listadas no arquivo requirements.txt.
5. Crie um arquivo .env na raiz do projeto com base no .env-model fornecido, preenchendo as informações necessárias obtidas no painel da aplicação Auth0.
6. Execute o comando: `python -m uvicorn src.main:app --reload` para iniciar a aplicação, ou utilize o modo de depuração do VSCode, que já está pré-configurado no projeto.
