# uls2sqlite

This is the docker version of uls2sqlite. All of the credit for this tool goes to [Chris Goff](https://chrisapproved.com/blog/convert-fcc-uls-database-to-sql.html), I simply made a docker container out of his project.
This tool downloads the weekly FCC ULS dat files and converts them to a sqlite database file.

## Quick Setup

1. Install Docker and Docker-Compose

- [Docker Install documentation](https://docs.docker.com/install/)
- [Docker-Compose Install documentation](https://docs.docker.com/compose/install/)

2. Create a docker-compose.yml file:

```yml
version: '3'

services:
  sqliterest:
    image: christracy/uls2sqlite
    volumes:
      - /path/to/database:/databases
```

3. Bring up your stack by running

```bash
docker-compose up -d

# If using docker-compose-plugin
docker compose up -d

```
