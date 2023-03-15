# Product's Wishlist

This projects is based on **LuizaLabs Backend Challenge**. Its is supposed to be part of a e-commerce system where users can add/get/remove itens from a wishlist.

---
## Installation
The application runs in a dockerized enviroment, you will need `docker` and `docker compose` installed to run it. Firing up the containers will automatically pull the images of *python3.10* and *postgres*, as well install all dependecies required.
> $ docker compose up

Note: Older versions of docker compose uses the `docker-compose` command (hyphen separated)

---
## Project Structure - Django Apps

- `django_root` -> Base app of the Django project, containing the settings and configarition of the API.
- `wishlist` -> responsible for CRUD a user's **product** items in a wishlist / favorites. Each items is unique in a user's wishlist, and a user does not have read/write permission on other user wishlist
- `product` -> retrieves detailed information on items available in the store. Its initial implementation used Django's Model, and was later migrated to use the **luiza_labs** client to retrieve the product data.
- `luiza_labs` -> client implementation for the Luiza Labs public API


**Note**: For user's authentication and authorization, <a hred='https://dj-rest-auth.readthedocs.io/en/latest/'>`dj_rest_auth`</a> is used.


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

