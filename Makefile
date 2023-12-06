USERNAME ?= $(shell read -p "Entrez votre nom d'utilisateur mysql: " u && echo $$u)
PASSWORD ?= $(shell read -p "Entrez votre mot de passe mysql: " p && echo $$p)


# # Makefile
# create_venv:
# ifeq ($(OS),Windows_NT)
# 	python -m venv bizenv
# 	.\bizenv\Scripts\Activate
# else
# 	python -m venv bizenv
# 	source bizenv/bin/activate
# endif

# create_db:
# 	@read -p "Enter the MySql  username: " username; \
# 	read -s -p "Enter the MySql password: " password; \
# 	echo ""; \
# 	export DATABASE_URL="mysql+pymysql://$$username:$$password@localhost/bizappdb"; \
# 	python -c "from yourmodule import create_database; create_database()"

# requirements: create_venv
# 	pip install -r requirements.txt
# 	create_db 

# migrate:
# 	alembic revision --autogenerate -m "Initial migration"

# upgrade:
# 	alembic upgrade head

# install: requirements migrate upgrade
