# Product's Wishlist

This projects is based on **LuizaLabs Backend Challenge**. Its is supposed to be part of a e-commerce system where users can add/get/remove itens from a wishlist.

---
## Installation
The application runs in a dockerized enviroment, you will need `docker` and `docker compose` installed to run it. Firing up the containers will automatically pull the images of *python3.10* and *postgres*, as well install all dependecies required.
> $ docker compose up

Note: Older versions of docker compose uses the `docker-compose` command (hyphen separated)

---
## Scripts
The scripts folder has a handful of alias for executing commands inside the `app` container.

> $ docker exec -it bash scripts/\$script_name

Available scripts:
- manage -> Django's manage
- shell -> Django's shell (ipython interface)
- pytest -> Runs the tests using *pytest* as runner
- unittest -> Runs the tests using *unittest* as runner
- start -> used as entrypoint, setup and starts Django server

---

## Tests

To run the test with the *pytest* runner (recommend), execute the following command:
> $ docker exec -it app scripts/pytest

Optional: There is also a script for running with *unittest* for legacy reasons, as it was used in the beggining of the project

