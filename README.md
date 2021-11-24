
## Code Structure
This project uses Zendesk's API, Python, the Flask library, Jinja templating, and some basic HTML/CSS to create a full-stack app that allows
users to manage their Zendesk tickets.

`app.py` handles most of the backend work (routing and redirecting etc.), relying on some utility functions from 
`utils.py`. `tests.py` tests the utility functions, the routing, and some basic authentication using flask-specific 
python testing frameworks. Note that these tests rely on `tickets.json` being loaded into the agent's account.
The `/templates` folder stores the HTML files that are accessed by the backend. 


## Installation
Assuming Python (>3.8) and `pip` are installed.
0. Clone this repository
```bash
git clone https://github.com/vsingh18567/zcc-singhvik.git
```
1. Install/update `pipenv`
```bash
pip install pipenv --upgrade
```
2. Start a `pipenv` envrionment. Ensure you are in the folder with `Pipfile`.
```bash
pipenv shell
pipenv install
```
3. Create a `.env` file in the root of the project and set the environment variables based on your Zendesk agent
credentials.
```bash
DOMAIN=zccdomain
EMAIL=email@email.com
TOKEN=hashedtoken
```

## Usage
Note that this app runs with `DEBUG=True`, and therefore should not be used in production
1. Run the flask app
```bash
pipenv run app
```
2. Navigate to http://localhost:8000
   - If you prefer to not use port 8000, you can set a custom port as a command line argument. For example, to use
    http://localhost:3000:
   ```bash
    pipenv run app 3000
   ```


### Routes
- `/`
  - Lists all the tickets, allowing for pagination and searching for tickets by ID.
- `/ticket/<id>`
  - Displays information about a specific ticket
### Error Messaging
- If there is ever a red banner across the header of the page, that means that either you attempted to access a ticket
that doesn't exist, or inputted some sort of other malformed URL.
- If there is ever simply an error message on the page asking to try again later, that indicates some sort of 
API issue - either issues with authentication or the API simply being down.

### Testing
To run the tests: (note that these tests rely on `tickets.json` being loaded and the ID/names of users matching)
```bash
pipenv run test
```
All these tests passed locally when using `zccsinghvik` as the domain.