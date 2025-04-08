# Golden Raspberry Awards REST API

Implementation of a RESTful API to enable reading the list of nominees and winners of the Worst Picture category of the Golden Raspberry Awards.

## Requirements

* [Python 3.13.2](https://www.python.org/downloads/)
* [Pip](https://pypi.org/project/pip/) - For dependency management (requirements.txt)
* [Pyenv - Optional](https://github.com/pyenv/pyenv#installation)
* [virtualenv - Optional](https://pypi.org/project/virtualenv/)

This project was implemented using Python 3.13.2.  
You can have multiple versions of Python (2.x and 3.x) installed on the same system without issues.  
I recommend and use pyenv (a Python version management tool) along with virtualenv (a tool to create isolated virtual environments in Python.)

## Run local Setup

1. Clone the repository:
```bash
    git clone <REPO_URL>
    cd <REPO_NAME>
```

2. Create a virtual environment (Optional) though recommended to isolate project dependencies.
Choose one method:

2.1. Using virtualenv:
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

2.2. Using native venv module:
```bash
    python -m venv venv
    source venv/bin/activate    # Linux/MacOS
```

3. Install dependencies:
```bash
    pip install -r requirements.txt
```

4. Run the API:
```bash
    uvicorn app.main:app --reload
```

## FastAPI Automatic Interactive Documentation:
[Swagger](http://127.0.0.1:8000/docs)  
[ReDoc](http://127.0.0.1:8000/redoc)

## API Doc
 
#### Retrieves the producer with:
- Longest interval between two consecutive awards (max)
- Shortest interval between two consecutive awards (min)
```http
  GET /api/v1/producers/intervals
```
Expected Response Format:
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

### Test Methods:
1. **Using curl** (direct terminal execution or import at Postman):
```bash
    curl -X 'GET' \
      'http://localhost:8000/api/v1/producers/intervals' \
      -H 'accept: application/json'
```

## Running Automated Tests
With the virtual environment activated and dependencies installed, run the following command:
```bash
pytest
```

## Author

* **Vagner Santos** 
* [GitHub](https://github.com/vagnerpgss)
* [LinkedIn](https://www.linkedin.com/in/vagnerit/)

## License
This project is licensed under the MIT License - see the LICENSE file for details

## Languages

- [Português](README.md)
- [English](README.en.md)