# Makefile for the okfn.org Django CMS site.
# `make` (no target) shows this help.

IMAGE := okfn
NAME  := okfn
PORT  := 8888

# Local Postgres 13 cluster — used by `make run-pg` and `make db-shell`.
# Override on the command line if you put the cluster on a different port,
# e.g. `make run-pg DB_HOST_PORT=5435`.
DB_HOST_PORT ?= 5434
DB_NAME      ?= okfn
DB_USER      ?= hermes
DB_PASSWORD  ?= devpass

# Detect if the container is currently running.
RUNNING := $(shell docker ps --filter name=^/$(NAME)$$ --format '{{.Names}}' 2>/dev/null)

.PHONY: help build run run-pg stop restart bash logs test check lint shell migrate css deps-compile db-shell fixtures-dump fixtures-load clean

# Tunable: number of CMS pages (treenodes) to include in the sample fixture.
MAX_PAGES ?= 100

help:
	@echo "Targets:"
	@echo "  make build         Build the Docker image ($(IMAGE))."
	@echo "  make run           Start the container with the SQLite fallback DB."
	@echo "  make run-pg        Start the container against the local PG 13 cluster ($(DB_NAME)@:$(DB_HOST_PORT))."
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
	@echo "  make db-shell      Open psql against the local PG 13 cluster."
	@echo "  make fixtures-dump Regenerate foundation/tests/fixtures/sample_data.json from the live DB (MAX_PAGES=$(MAX_PAGES))."
	@echo "  make fixtures-load Load the sample fixture into the container's DB."
	@echo "  make clean         Stop the container and prune dangling images."

build:
	docker build -t $(IMAGE) .

run:
	docker run -d --rm --name $(NAME) -p $(PORT):80 $(IMAGE)
	@echo "Container '$(NAME)' running on http://localhost:$(PORT)"

# Run the container against the host's local PG 13 cluster. Requires:
#   1. PG 13 cluster online (see `pg_lsclusters`).
#   2. Role $(DB_USER) has a TCP password set; pg_hba.conf accepts the
#      Docker bridge network (172.16.0.0/12) for that role.
# `--add-host host.docker.internal:host-gateway` makes the host reachable
# from inside the container by that hostname (Linux Docker convention).
# We write the DB settings to .env.docker-pg and mount it as /app/.env
# inside the container; settings.py reads `.env` *after* `.env.base`, so
# these values override the SQLite defaults. Plain `-e DB_HOST=...` flags
# don't work because settings.py reads `.env.base` with overwrite=True,
# clobbering the container env.
run-pg:
	@printf '%s\n' \
	    'DB_ENGINE=django.db.backends.postgresql_psycopg2' \
	    'DB_HOST=host.docker.internal' \
	    'DB_PORT=$(DB_HOST_PORT)' \
	    'DB_NAME=$(DB_NAME)' \
	    'DB_USER=$(DB_USER)' \
	    'DB_PASSWORD=$(DB_PASSWORD)' \
	    > .env.docker-pg
	docker run -d --rm --name $(NAME) \
	    -p $(PORT):80 \
	    --add-host host.docker.internal:host-gateway \
	    -v $(PWD)/.env.docker-pg:/app/.env:ro \
	    $(IMAGE)
	@echo "Container '$(NAME)' running on http://localhost:$(PORT) against PG 13 ($(DB_NAME)@:$(DB_HOST_PORT))"

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

# Quick psql shell against the local PG 13 cluster (uses peer auth — no password).
db-shell:
	psql -p $(DB_HOST_PORT) -d $(DB_NAME)

# Regenerate the sample fixture from the running container's DB. Requires
# `make run-pg` first (the container must be connected to a populated DB).
# Tune size with `make fixtures-dump MAX_PAGES=50` for a smaller slice.
fixtures-dump:
	docker exec $(NAME) python manage.py dump_sample --max-pages $(MAX_PAGES) --out /tmp/sample_data.json
	docker cp $(NAME):/tmp/sample_data.json foundation/tests/fixtures/sample_data.json
	@echo "Wrote foundation/tests/fixtures/sample_data.json"

# Load the sample fixture into the running container's DB. Useful for
# seeding a fresh `make run` (SQLite) container with realistic content.
fixtures-load:
	docker exec $(NAME) python manage.py loaddata /app/foundation/tests/fixtures/sample_data.json

clean: stop
	-docker image prune -f
