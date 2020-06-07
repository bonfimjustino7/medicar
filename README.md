# Medicar


## Instalação:
- Clonando o projeto:
```commandline
git clone https://github.com/bonfimjustino7/medicar.git
```
## Backend
- Criando virtualenv e instalando dependências: 
```commandline
cd medicar/backend
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
- Rodando migrates e criando super usuário:
```commandline
python manage.py migrate
python manage.py createsuperuser
```
- Executando servidor:
```commandline
python manage.py runserver
```
## Frontend
- Instalando dependências:
```commandline
cd frontend
npm install
```
- Rodando app:
```commandline
npm start
```