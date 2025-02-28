<h1 align="center"> 🖼️ LowPoly </h1>

<div align="center">
    <img src="https://img.shields.io/github/v/release/toshy/lowpoly?label=Release&sort=semver" alt="Current bundle version" />
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/lowpoly/codestyle.yml?branch=main&label=Black" alt="Black">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/lowpoly/codequality.yml?branch=main&label=Ruff" alt="Ruff">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/lowpoly/statictyping.yml?branch=main&label=Mypy" alt="Mypy">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/lowpoly/security.yml?branch=main&label=Security%20check" alt="Security check" />
    <br /><br />
    <div>A command-line utility for converting images to low polygon variants.</div>
</div>

## 📝 Quickstart

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest -h
```

## 📜 Documentation

The documentation is available at [https://toshy.github.io/lowpoly](https://toshy.github.io/lowpoly).

## 🖼️ Results

<p align="center" width="100%">
    <img width="32%" src="https://github.com/ToshY/lowpoly/blob/main/docs/images/input.jpeg" alt="input image">
    <img width="32%" src="https://github.com/ToshY/lowpoly/blob/main/docs/images/delaunay.png" alt="lowpoly delaunay">
    <img width="32%" src="https://github.com/ToshY/lowpoly/blob/main/docs/images/voronoi.png" alt="lowpoly voronoi">
</p>

> [!NOTE]
> From left-to-right:
> 1. `input/input.jpeg`
> 2. `output/input_delaunay_<%d-%m-%Y_%H-%M-%S-%f>.png`
> 3. `output/input_voronoi_<%d-%m-%Y_%H-%M-%S-%f>.png`

## 🛠️ Contribute

### Requirements

* ☑️ [Pre-commit](https://pre-commit.com/#installation).
* 🐋 [Docker Compose V2](https://docs.docker.com/compose/install/)
* 📋 [Task 3.37+](https://taskfile.dev/installation/)

## ❕ License

This repository comes with a [BSD 3-Clause License](./LICENSE).
