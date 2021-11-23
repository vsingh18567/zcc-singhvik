
## Installation
Assuming python and `pip` are installed.
1. Install `pipenv`
```bash
pip install pipenv
```
2. Start a `pipenv` envrionment. Ensure you are in the folder with `Pipfile`.
```bash
pipenv shell
pipenv install
```
3. Create a `.env` file in the root of the project and set the environment variables
```bash
EMAIL=email@email.com
TOKEN=hashedtoken
```

## Usage
1. Start up the Flask app
```bash
flask run
```
2. Navigate to http://127.0.0.1:5000/ 