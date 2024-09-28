# course-scheduling

To get started, try out the docker compose. It requires that you have the following files in the project's root directory.

- `createdb.sql`
- `client_secret.json`

Assuming you do, then using the Docker compose is as simple as running `docker compose -f docker-compose.dev.yml up --build`. This will run the development Docker containers, allowing the Django server to restart whenever you make a change. It will also rebuild the docker container if any changes to the Dockerfile or the environment happened. If you want to build and run the production Django server, run `docker compose -f docker-compose.prod.yml up --build`.

To take down the Docker compose, make sure to run `docker compose -f <compose-file> down`.

To expose the backend to https traffic, you can use `ngrok` (or any reverse proxy). Simply run `ngrok http 8000` and you'll be able to access the backend on the url it provides.
