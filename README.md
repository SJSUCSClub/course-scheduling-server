# course-scheduling

To get started, try out the docker compose. It requires that you have the following files in the project's root directory.

- `createdb.sql`
- `client_secret.json`

Assuming you do, then using the Docker compose is as simple as running `docker compose up`

To expose the backend to https traffic, you can use `ngrok` (or any reverse proxy). Simply run `ngrok http 8000` and you'll be able to access the backend on the url it provides.
