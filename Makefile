# Makefile for the okfn.org Django CMS site.
# `make` (no target) shows this help.

IMAGE := okfn
NAME  := okfn
PORT  := 8888

# Detect if the container is currently running.
RUNNING := $(shell docker ps --filter name=^/$(NAME)$$ --format '{{.Names}}' 2>/dev/null)

.PHONY: help build run stop restart bash logs test check lint shell migrate css deps-compile clean

help:
	@echo "Targets:"
	@echo "  make build         Build the Docker image ($(IMAGE))."
	@echo "  make run           Start the container detached on port $(PORT)."
	@echo "  make stop          Stop the running container."
	@echo "  make restart       Stop + run."
	@echo "  make bash          Open an interactive shell inside the container."
	@echo "  make logs          Tail the container logs (Ctrl-C to exit)."
	@echo "  make test          Run Django's test suite inside the container."
	@echo "  make check         Run 'manage.py check'."
	@echo "  make lint          Run flake8 against the project code."
	@echo "  make shell         Open the Django shell (REPL)."
	@echo "  make migrate       Apply pending migrations."
	@echo "  make css           Compile Tailwind/PostCSS to static/css/styles.css."
	@echo "  make deps-compile  Recompile requirements.txt + requirements.dev.txt from .in files."
	@echo "  make clean         Stop the container and prune dangling images."

build:
	docker build -t $(IMAGE) .

run:
	docker run -d --rm --name $(NAME) -p $(PORT):80 $(IMAGE)
	@echo "Container '$(NAME)' running on http://localhost:$(PORT)"

stop:
	-docker stop $(NAME)

restart: stop run

# Use exec if the container is running, otherwise spin up a one-shot.
bash:
ifeq ($(RUNNING),$(NAME))
	docker exec -it $(NAME) bash
else
	docker run --rm -it -w /app --entrypoint bash $(IMAGE)
endif

logs:
	docker logs -f $(NAME)

test:
ifeq ($(RUNNING),$(NAME))
	docker exec $(NAME) python manage.py test
else
	docker run --rm --entrypoint python $(IMAGE) manage.py test
endif

check:
ifeq ($(RUNNING),$(NAME))
	docker exec $(NAME) python manage.py check --settings=foundation.settings
else
	docker run --rm --entrypoint python $(IMAGE) manage.py check --settings=foundation.settings
endif

# flake8 is in requirements.dev.txt, not in the production image, so install it
# on the fly. The .flake8 config sets max-line-length=120 and ignores W503.
lint:
ifeq ($(RUNNING),$(NAME))
	docker exec $(NAME) sh -c "pip install -q flake8 && flake8 --config=/app/.flake8 ."
else
	docker run --rm -w /app --entrypoint sh $(IMAGE) -c "pip install -q flake8 && flake8 --config=/app/.flake8 ."
endif

shell:
	docker exec -it $(NAME) python manage.py shell

migrate:
	docker exec $(NAME) python manage.py migrate

# Run on the host — needs Node 20 + a local node_modules (`npm install`).
css:
	npm run build

# Run on the host — needs `uv` installed locally.
deps-compile:
	uv pip compile requirements.in     -o requirements.txt
	uv pip compile requirements.dev.in -o requirements.dev.txt

clean: stop
	-docker image prune -f
