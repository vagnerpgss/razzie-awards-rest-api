# Golden Raspberry Awards REST API

Implementação de uma API RESTful para possibilitar a leitura da lista de indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards

## Requerimentos

* [Python 3.13.2](https://www.python.org/downloads/)
* [Pyenv - Opcional](https://github.com/pyenv/pyenv#installation)
* [virtualenv - Opcional](https://pypi.org/project/virtualenv/)

Esse projeto foi implementado utilizando o Python 3.13.2.
Você pode ter várias versões do Python (2.x e 3.x) instaladas no mesmo sistema sem problemas.
Eu recomendo e uso o pyenv (ferramenta de gerenciamento de versões do Python) junto com o virtualenv (ferramenta para criar ambientes virtuais isolados em Python.)

## Como rodar o projeto

1. Clone o repositório:
```bash
    git clone <URL_DO_REPO>
    cd <NOME_DO_REPO>
```

2. Crie um ambiente virtual (Opcional) porém recomendo o uso de um ambiente virtual para isolar as dependências do projeto.
Escolha uma das opções:

2.1. Usando virtualenv:
```bash
    # Substitua <python_version> pela versão desejada (ex: 3.11.0)
    virtualenv --python=<python_version> venv --clear
    
    # Ativar ambiente
    source venv/bin/activate    # Linux/MacOS
    # ou
    venv\Scripts\activate       # Windows
    
    # Verificar versão
    python --version
```
2.2. Usando módulo nativo venv:
```bash
    python -m venv venv
    source venv/bin/activate    # Linux/MacOS
```

3. Instale as dependências:
```bash
    pip install -r requirements.txt
```

4. Execute a API:
```bash
    uvicorn app.main:app --reload
```

5. Executando os testes:
```bash
    pytest
```

## Author

* **Vagner Santos** 
* [GitHub](https://github.com/vagnerpgss)
* [LinkedIn](https://www.linkedin.com/in/vagnerit/)

## Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE.md) para detalhes

## Linguagens

- [English](README.md)
- [Português](README.pt-br.md)