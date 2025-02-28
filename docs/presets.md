## Usage

The following section shows the basic presets that are already available. You
can add your custom presets by mounting files to the `/app/preset` directory.

---

### 🐋 Docker

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  -v ${PWD}/preset/custom.json:/app/preset/custom.json \
  ghcr.io/toshy/lowpoly:latest
```

### 🐳 Compose

```yaml
services:
  lowpoly:
    image: ghcr.io/toshy/lowpoly:latest
    volumes:
      - ./input:/app/input
      - ./output:/app/output
      - ./preset/custom.json:/app/preset/custom.json
```

### Default

???+ example "`default.json`"

    Both delaunay and voronoi types are enabled in the default preset.

    ```json
    {
        "type": [
            "delaunay",
            "voronoi"
        ],
        "seed": 42,
        "canny": {
            "threshold": {
                "min": 20,
                "max": 100
            }
        },
        "grayscale": {
            "threshold": {
                "min": 0,
                "max": 255
            }
        },
        "points": {
            "add": {
                "factor": 10000
            },
            "reduce": {
                "factor": 50
            }
        },
        "output": {
            "resolution": 16000,
            "mega_pixel_constraint": null,
            "svg": {
                "preserveAspectRatio": "xMidYMid meet",
                "style": {
                    "shape-rendering": "crispEdges"
                }
            }
        }
    }
    ```

### Delaunay

???+ example "`delaunay.json`"

    ```json
    {
        "type": [
            "delaunay"
        ],
        "seed": 42,
        "canny": {
            "threshold": {
                "min": 20,
                "max": 100
            }
        },
        "grayscale": {
            "threshold": {
                "min": 0,
                "max": 255
            }
        },
        "points": {
            "add": {
                "factor": 10000
            },
            "reduce": {
                "factor": 50
            }
        },
        "output": {
            "resolution": 16000,
            "mega_pixel_constraint": null,
            "svg": {
                "preserveAspectRatio": "xMidYMid meet",
                "style": {
                    "shape-rendering": "crispEdges"
                }
            }
        }
    }
    ```

### Voronoi

???+ example "`voronoi.json`"

    ```json
    {
        "type": [
            "voronoi"
        ],
        "seed": 42,
        "canny": {
            "threshold": {
                "min": 20,
                "max": 100
            }
        },
        "grayscale": {
            "threshold": {
                "min": 0,
                "max": 255
            }
        },
        "points": {
            "add": {
                "factor": 10000
            },
            "reduce": {
                "factor": 50
            }
        },
        "output": {
            "resolution": 8000,
            "mega_pixel_constraint": null,
            "svg": {
                "preserveAspectRatio": "xMidYMid meet",
                "style": {
                    "shape-rendering": "crispEdges"
                }
            }
        }
    }
    ```

### Custom

???+ example "`custom.json`"

    You can fully customise the settings to your liking.

    - `type` - `list` - `["delaunay", "voronoi"]`
    - `seed` - `int` - The seed for the [NumPy generator](https://numpy.org/doc/stable/reference/random/generator.html).
    - `canny` - `dict` - Settings for the [Canny edge detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html).
        - `threshold` - `dict` - Settings for the threshold.
            - `min` - `int` - The minimum threshold.
            - `max` - `int` - The maximum threshold.
    - `grayscale` - `dict` - Settings for the grayscale image.
        - `threshold` - `dict` - Settings for [binary threshold](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html).
            - `min` - `int` - The minimum threshold.
            - `max` - `int` - The maximum threshold.
    - `points` - `dict` - Settings for the polygon points.
        - `add` - `dict` - Settings for adding addtional **non-edge** points.
            - `factor` - `int` - The factor for adding points.
        - `reduce` - `dict` - Settings for reducing **edge** points.
            - `factor` - `int` - The factor for reducing points.
    - `output` - `dict` - Settings for the output images.
        - `resolution` - `int` - The resolution denoting either max width or max height of desired output image.
        - `mega_pixel_constraint` - `float`|`int` - The mega pixel constraint for the output image in case the image goes beyond the specified resolution.
        - `svg` - `dict` - Settings for the SVG output.
            - `preserveAspectRatio` - `str` - The SVG tag option to preserve aspect ratio.
            - `style` - `dict` - The style of polygons.
                - `shape-rendering` - `str` - The [shape rendering](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/shape-rendering) style for the polygons.

    ```json
    {
        "type": [
            "voronoi"
        ],
        "seed": 123,
        "canny": {
            "threshold": {
                "min": 0,
                "max": 150
            }
        },
        "grayscale": {
            "threshold": {
                "min": 100,
                "max": 255
            }
        },
        "points": {
            "add": {
                "factor": 5000
            },
            "reduce": {
                "factor": 25
            }
        },
        "output": {
            "resolution": 16000,
            "mega_pixel_constraint": 182.5,
            "svg": {
                "preserveAspectRatio": "xMidYMid meet",
                "style": {
                    "shape-rendering": "geometricPrecision"
                }
            }
        }
    }
    ```
