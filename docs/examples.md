# Examples

## Basic

Add your files to the input directory of the mounted container.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest
```

By default, it will find all files from the `/app/input` directory (recursively) and write the output to the `/app/output` directory. If
no presets are provided, it will automatically use the [`preset/default.json`](presets.md#default).

<div style="display: flex; justify-content: space-between;">
    <figure style="width: 33%; text-align: center;">
        <img src="/images/input.jpeg" alt="Image 1" style="width: 100%; height: auto;">
        <figcaption style="margin-top: 5px;"><code>input/input.jpeg</code></figcaption>
    </figure>
    <figure style="width: 33%; text-align: center;">
        <img src="/images/delaunay.png" alt="Image 2" style="width: 100%; height: auto;">
        <figcaption style="margin-top: 5px;"><code>output/input_delaunay_<%d-%m-%Y_%H-%M-%S-%f>.png</code></figcaption>
    </figure>
    <figure style="width: 33%; text-align: center;">
        <img src="/images/voronoi.png" alt="Image 3" style="width: 100%; height: auto;">
        <figcaption style="margin-top: 5px;"><code>output/input_voronoi_<%d-%m-%Y_%H-%M-%S-%f>.png</code></figcaption>
    </figure>
</div>

!!! note

    By default, if no explicit `-e/--extension` argument is provided, both SVG and PNG output files will be created.

## Specific file

Convert only a specific file and writing output to `/app/output` (default).

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/nature.jpeg"
```

## Specific file with PNG extension only

Convert only a specific file and write the PNG output to `/app/output`.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/nature.jpeg" \
  -e '["png"]'
```

!!! note

    The `-e/--extension` argument requires one of the following values: 

    - `'["svg", "png"]'` (default)
    - `'["svg"]'`
    - `'["png"]'`


## Single file with output subdirectory

Convert only a specific file and writing output to `/app/output/result`.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/nature.jpeg" \
  -o "output/result"
```

## Specific subdirectory

Convert files in specific subdirectory and writing output to `/app/output/result`.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/nature" \
  -o "output/result"
```

## Multiple inputs

Convert files in multiple input subdirectories and writing output to `/app/output` (default).

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/dir1" \
  -i "input/dir2"
```

## Multiple inputs and outputs

Convert files in multiple input subdirectories and writing output to specific output subdirectories respectively.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -o "output/dir1" \
  -o "output/dir2"
```

## Multiple inputs, outputs and single preset

Convert files in multiple input subdirectories, with a single preset, and writing output to specific output subdirectories respectively.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  -v ${PWD}/preset/custom1.json:/app/preset/custom1.json \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -p "preset/custom1.json" \
  -o "output/dir1" \
  -o "output/dir2"
```

## Multiple inputs, outputs and presets

Convert files in multiple input subdirectories, with multiple presets, and writing output to specific output subdirectories respectively.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  -v ${PWD}/preset/custom1.json:/app/preset/custom1.json \
  -v ${PWD}/preset/custom2.json:/app/preset/custom2.json \
  ghcr.io/toshy/lowpoly:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -p "preset/custom1.json" \
  -p "preset/custom2.json" \
  -o "output/dir1" \
  -o "output/dir2"
```
