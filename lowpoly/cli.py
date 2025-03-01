import click

from loguru import logger

from lowpoly.args import (
    OutputPathChecker,
    InputPathChecker,
    PresetPathChecker,
    OptionalValueChecker,
)
from lowpoly.exception import (
    InvalidPolygonOutputError,
)
from lowpoly.helper import combine_arguments_by_batch
from lowpoly.polygon import PolygonMaker
from lowpoly.processing import ImageProcessing
from lowpoly.edgedetection import EdgeDetection
from lowpoly.svg import SVGmaker


@logger.catch
@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog="Repository: https://github.com/ToshY/lowpoly",
)
@click.option(
    "--input-path",
    "-i",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    required=False,
    multiple=True,
    callback=InputPathChecker(),
    show_default=True,
    default=["./input"],
    help="Path to input file or directory",
)
@click.option(
    "--output-path",
    "-o",
    type=click.Path(dir_okay=True, file_okay=True, resolve_path=True),
    required=False,
    multiple=True,
    callback=OutputPathChecker(),
    show_default=True,
    default=["./output"],
    help="Path to output file or directory",
)
@click.option(
    "--preset",
    "-p",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=False,
    multiple=True,
    callback=PresetPathChecker(),
    show_default=True,
    default=["./preset/default.json"],
    help="Path to JSON file with preset options",
)
@click.option(
    "--extension",
    "-e",
    type=click.Choice(['["svg", "png"]', '["svg"]', '["png"]']),
    required=False,
    multiple=True,
    callback=OptionalValueChecker(),
    show_default=True,
    default=['["svg", "png"]'],
    help="Output file extension",
)
@click.option(
    "--unique-filename/--no-unique-filename",
    is_flag=True,
    show_default=True,
    default=True,
    help="Create files with unique filenames by using current datetime suffix",
)
def cli(
    input_path,
    output_path,
    preset,
    extension,
    unique_filename,
):
    combined_result = combine_arguments_by_batch(
        input_path, output_path, preset, extension
    )

    polygon_maker = PolygonMaker()

    for item in combined_result:
        current_batch = item.get("batch")
        current_preset = item.get("preset")
        current_preset_type = current_preset.get("type", ["voronoi"])
        current_preset_canny = current_preset.get(
            "canny", {"threshold": {"min": 20, "max": 100}}
        )
        current_preset_grayscale = current_preset.get(
            "grayscale", {"threshold": {"min": 0, "max": 255}}
        )
        current_preset_points = current_preset.get(
            "points", {"add": {"factor": 10000}, "reduce": {"factor": 50}}
        )

        current_output_extension = item.get("extension")
        current_output = item.get("output").get("resolved")
        current_input_original_batch_name = item.get("input").get("given")
        current_input_files = item.get("input").get("resolved")
        total_current_input_files = len(current_input_files)

        for current_file_path_index, current_file_path in enumerate(
            current_input_files
        ):
            if current_file_path_index == 0:
                logger.info(
                    f"LowPoly batch `{current_batch}` for `{current_input_original_batch_name}` started."
                )

            # %% grayscale
            image_processing = ImageProcessing(current_file_path)
            grayscale_image = image_processing.colour_2_grayscale(
                image_processing.user_image
            )

            # %% edge detection
            edge_detection = EdgeDetection()
            canny_edge_detected_image = edge_detection.canny(
                grayscale_image,
                current_preset_canny["threshold"]["min"],
                current_preset_canny["threshold"]["max"],
            )
            canny_binary_image = edge_detection.edge_gray_threshold(
                canny_edge_detected_image,
                grayscale_image,
                current_preset_grayscale["threshold"]["min"],
                current_preset_grayscale["threshold"]["max"],
            )

            # %% binary image points
            binary_image_points = polygon_maker.add_additional_points_to_polygon(
                canny_binary_image,
                current_preset_points["add"]["factor"],
                current_preset_points["reduce"]["factor"],
                current_preset.get("seed", None),
            )

            # %% create polygons
            for preset_type in current_preset_type:
                polygon_output = {}
                if preset_type == "delaunay":
                    polygon_output = polygon_maker.delaunay(
                        binary_image_points, image_processing
                    )

                if preset_type == "voronoi":
                    polygon_output = polygon_maker.voronoi(
                        binary_image_points, image_processing
                    )

                if polygon_output == {}:
                    raise InvalidPolygonOutputError

                svg_maker = SVGmaker(
                    current_preset, [image_processing.width, image_processing.height]
                )
                xml_result = svg_maker.xml_result(polygon_output)
                for output_extension in current_output_extension:
                    output_path = svg_maker.prepare_output_path(
                        current_file_path,
                        current_output,
                        output_extension,
                        unique_filename,
                        preset_type,
                    )
                    if output_extension == "svg":
                        svg_maker.save_svg(xml_result, output_path)

                    if output_extension == "png":
                        svg_maker.save_png(xml_result, output_path)

                    logger.info(f"Saved LowPoly output to `{str(output_path)}`.")

            if current_file_path_index != total_current_input_files - 1:
                continue

            logger.info(
                f"LowPoly batch `{current_batch}` for `{current_input_original_batch_name}` finished."
            )
