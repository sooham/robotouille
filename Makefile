FLASK_APP="$(shell pwd)/website/server.py"
FLASK_DEBUG=1

all: setup run

setup: 
	pip install -r requirements.txt
run:
	echo "GOTO https://127.0.0.1:5000"
	FLASK_APP=$(FLASK_APP) flask run
clean:
	unset FLASK_APP
	unset FLASK_DEBUG
	find . -name "*.pyc" | xargs rm -rf 

.PHONY: all setup run clean
