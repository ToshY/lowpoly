## Requirements

- 🐋 [Docker](https://docs.docker.com/get-docker/)

## Pull image

```sh
docker pull ghcr.io/toshy/lowpoly:latest
```

## Run container

### 🐋 Docker

Run with `docker`.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest -h
```

### 🐳 Compose

Create a `compose.yaml` file.

```yaml
services:
  lowpoly:
    image: ghcr.io/toshy/lowpoly:latest
    volumes:
      - ./input:/app/input
      - ./output:/app/output
```

Run with `docker compose`.

```sh
docker compose run -u $(id -u):$(id -g) --rm lowpoly -h
```

## Volumes

The following volume mounts are **required**: 

- `/app/input`
- `/app/output`

The following volume mounts are **optional**: 

- `/app/preset`

!!! tip
    Check the [presets](presets.md) section for more info about presets.
