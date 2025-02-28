import base64
import datetime
import json
from pathlib import Path

from cairocffi import CairoError  # type: ignore[import-untyped]
from cairosvg import svg2png  # type: ignore[import-untyped]

from lowpoly.exception import InvalidViewBoxError, SvgToPngImageError


def _get_formatted_datetime():
    """
    Get formatted datetime.
    """

    return datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S-%f")


class SVGmaker:

    poly_placeholder = "%polygons%"

    svg_description = "Rendered with LowPoly | https://github.com/ToshY/lowpoly"

    def __init__(
        self,
        user_preset: dict,
        image_dimensions: list,
        image_view_box: list = [0, 0, -1, -1],
    ):
        self.preset = user_preset
        self.safe_base_encoded_preset = base64.b64encode(
            json.dumps(self.preset).encode("utf-8")
        ).decode("utf-8")

        # Initial image dimensions
        self.width, self.height = image_dimensions

        # The "resolution" denotes max pixels the width OR height of output image can be and the scale
        # for both width and height will be calculated and applied based on this setting.
        self.scale = user_preset.get("output", {}).get("resolution", 1)
        if self.scale != 1:
            self.scale = self.scale / max(image_dimensions)

        # Check scale does not exceed constraint and solve if needed
        user_mega_pixel_constraint = user_preset.get("output", {}).get(
            "mega_pixel_constraint", None
        )
        if user_mega_pixel_constraint is not None:
            mega_pixel_constraint = ((self.width * self.height) * self.scale**2) / 1e6
            if mega_pixel_constraint >= user_mega_pixel_constraint:
                self.scale = (
                    (round(user_mega_pixel_constraint) * 1e6)
                    / (self.width * self.height)
                ) ** (1 / 2)

        # Viewbox
        self.view_box = self._check_viewbox_dimensions(image_view_box)
        if self.view_box[-2:] == [-1, -1]:
            self.view_box[-2:] = image_dimensions

        # Scale
        if self.scale != 1:
            self.view_box = [self.scale * x for x in self.view_box]
            self.width, self.height = self.view_box[-2:]

    def xml_initialise(
        self,
    ) -> str:
        xml_string = '<?xml version="1.0" encoding="UTF-8"?>\r\n'
        xml_string += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\r\n'
        xml_string += (
            '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" preserveAspectRatio="'
            + self.preset.get("output", {})
            .get("svg", {})
            .get("preserveAspectRatio", "xMidYMid meet")
            + '" '
        )
        xml_string += (
            'width="' + str(self.width) + 'px" height="' + str(self.height) + 'px" '
        )
        xml_string += 'viewBox="' + self._join_view_box_list(self.view_box) + '">\r\n'
        xml_string += (
            '<g transform="scale('
            + str(self.scale)
            + ","
            + str(self.scale)
            + ')" style="shape-rendering: '
            + self.preset.get("output", {})
            .get("svg", {})
            .get("style", {})
            .get("shape-rendering", "geometricPrecision")
            + ';">\r\n'
        )
        xml_string += self.poly_placeholder
        xml_string += "</g>\r\n"
        xml_string += (
            "<desc>"
            + self.svg_description
            + " | Created at: "
            + _get_formatted_datetime()
            + " | Options: "
            + self.safe_base_encoded_preset
            + "</desc>"
        )
        xml_string += "</svg>"

        return xml_string

    def xml_polygon_points(self, polygon, colours):
        """Create polygon segments"""

        # Loop over points and format to svg polygon
        xml_polygon_string = ""
        for idx, (polygon_element, colour_element) in enumerate(zip(polygon, colours)):
            joined_svg_polygon_points = ""
            for p in polygon_element:
                joined_svg_polygon_points = " ".join(
                    [joined_svg_polygon_points, ",".join(str(e) for e in p)]
                )

            # Strip leading whitespace
            joined_svg_polygon_points = joined_svg_polygon_points.strip()

            # Get HEX colours
            polygon_hexadecimal_colours = self.rgb_to_hexadecimal_notation(
                colour_element[2], colour_element[1], colour_element[0]
            )
            # Append
            xml_polygon_string += (
                '<polygon points="'
                + joined_svg_polygon_points
                + '" style="fill:'
                + polygon_hexadecimal_colours
                + ';"/>'
            )

        return xml_polygon_string

    def xml_result(self, polygon_output) -> str:
        svg_str = self.xml_initialise()
        svg_poly = self.xml_polygon_points(
            polygon_output["polygons"], polygon_output["colours"]
        )

        return svg_str.replace(self.poly_placeholder, svg_poly)

    def prepare_output_path(
        self,
        input_file,
        output_path,
        output_extension,
        unique_output_file_name: bool = False,
        file_prefix: str = "",
    ) -> Path:
        output_extension_with_leading_dot = "." + output_extension.lstrip(".")
        if output_path.is_dir():
            output_file = output_path.joinpath(
                input_file.stem + output_extension_with_leading_dot
            )
        else:
            output_file = Path(
                f"{output_path.with_suffix('')}{output_extension_with_leading_dot}"
            )

        # Use file prefix in output filename
        output_file = Path(
            f"{output_file.with_suffix('')}{'_' + file_prefix if file_prefix else ''}{output_extension_with_leading_dot}"
        )

        if unique_output_file_name:
            output_file = f"{output_file.with_suffix('')}_{_get_formatted_datetime()}{output_extension_with_leading_dot}"

        return output_file

    def save_svg(self, content, output_path: Path) -> None:
        text_file = open(str(output_path), "wt")
        text_file.write(content)
        text_file.close()

    def save_png(self, content, output_path: Path) -> None:
        try:
            svg2png(bytestring=content, write_to=str(output_path))
        except CairoError as e:
            raise SvgToPngImageError(str(e))

    def _join_view_box_list(self, x, current_delimiter=" "):
        """Join lists/tuples to string"""

        return current_delimiter.join(map(str, x))

    def rgb_to_hexadecimal_notation(self, r, g, b):
        """RGB to Hexadecimal"""

        return "#{0:02x}{1:02x}{2:02x}".format(
            self._rgb_boundary(r), self._rgb_boundary(g), self._rgb_boundary(b)
        )

    def _rgb_boundary(self, integer_value):
        """RGB boundaries"""

        return max(0, min(integer_value, 255))

    def _check_viewbox_dimensions(self, view_box_dimensions):
        """Check viewbox numerical values"""

        view_box = [s for s in view_box_dimensions if isinstance(s, (int, float))]
        if len(view_box) != len(view_box_dimensions):
            raise InvalidViewBoxError

        return view_box
