# Golden Raspberry Awards REST API

Implementação de uma API RESTful para possibilitar a leitura da lista de indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards

## Requerimentos

* [Python 3.13.2](https://www.python.org/downloads/)
* [Pip](https://pypi.org/project/pip/) Para instalação das dependências (requirements.txt)
* [Pyenv - Opcional](https://github.com/pyenv/pyenv#installation)
* [virtualenv - Opcional](https://pypi.org/project/virtualenv/)

Esse projeto foi implementado utilizando o Python 3.13.2.
Você pode ter várias versões do Python (2.x e 3.x) instaladas no mesmo sistema sem problemas.
Eu recomendo e uso o pyenv (ferramenta de gerenciamento de versões do Python) junto com o virtualenv (ferramenta para criar ambientes virtuais isolados em Python.)

## Como rodar o projeto localmente

1. Clone o projeto:
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

## Documentação interativa automática FastAPI:
[Swagger](http://127.0.0.1:8000/docs)  
[ReDoc](http://127.0.0.1:8000/redoc)

## Documentação da API:

#### Retorna o produtor com:
- Maior intervalo entre dois prêmios consecutivos (max)
- Menor intervalo entre dois prêmios consecutivos (min)
```http
  GET /api/v1/producers/intervals
```
Resposta esperada:
```json
{
  "min": 
  [{
    "producer": "Producer 1",
    "interval": 1,
    "previousWin": 2008,
    "followingWin": 2009
  },
  {
    "producer": "Producer 2",
    "interval": 1, 
    "previousWin": 2018, 
    "followingWin": 2019
  }]
},
  "max": [
  {
    "producer": "Producer 1",
    "interval": 99,
    "previousWin": 1900,
    "followingWin": 1999
  },
  {
    "producer": "Producer 2",
    "interval": 99,
    "previousWin": 2000,
    "followingWin": 2099
  }
]}
```

### Testando o endpoint:
1. **Usando curl** (direto no terminal ou pode ser importado no Postman):
```bash
    curl -X 'GET' \
      'http://localhost:8000/api/v1/producers/intervals' \
      -H 'accept: application/json'    
```

## Executando os testes automatizados:
Com o ambiente virtual ativado e as dependências instaladas, execute o comando abaixo:
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

- [Português](README.md)
- [English](README.en.md)