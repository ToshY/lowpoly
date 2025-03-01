import numpy as np
from scipy.spatial import Delaunay, Voronoi  # type: ignore[import-untyped]
from shapely.geometry import Polygon  # type: ignore[import-untyped]

from lowpoly.exception import (
    InvalidPolygonGeometryError,
    InvalidPolygonError,
)


class PolygonMaker:
    def voronoi(self, binary_image_points, image_processing):
        voronoi = Voronoi(binary_image_points)
        regions, vertices = self._get_voronoi_finite_polygons(voronoi)

        # Clip box from image dimensions
        box = Polygon(
            [
                (0, 0),
                (image_processing.width, 0),
                (image_processing.width, image_processing.height),
                (0, image_processing.height),
            ]
        )

        voronoi_polygons = []
        for idx, region in enumerate(regions):
            polygon = Polygon(vertices[region])

            if not polygon.is_valid:
                try:
                    polygon = polygon.buffer(0)
                except TypeError | ValueError:
                    raise InvalidPolygonGeometryError

            # Clipping polygon to image dimensions
            poly = polygon.intersection(box)

            # Append to list
            voronoi_polygons.append(
                list(map(list, np.array([p for p in poly.exterior.coords])))
            )

        return {
            "colours": self._get_colours(
                image_processing.user_image, binary_image_points
            ),
            "polygons": voronoi_polygons,
        }

    def delaunay(self, binary_image_points, image_processing):
        tri = Delaunay(binary_image_points)
        aot = binary_image_points[tri.simplices].shape[0]
        triangle_centre = np.empty([aot, 2], dtype=int)

        for idx, s in enumerate(binary_image_points[tri.simplices]):
            triangle_centre[idx] = self._get_polygon_centre(s)

        return {
            "colours": self._get_colours(image_processing.user_image, triangle_centre),
            "polygons": binary_image_points[tri.simplices],
        }

    def _get_polygon_centre(self, poly, rounded=True):
        """Get polygon center"""

        # Amount of points
        amount_of_points = poly.shape[0]

        if amount_of_points == 3:
            # Triangle
            ply = poly.mean(axis=0)
            if rounded:
                return np.round(ply)
            else:
                return ply
        elif amount_of_points > 3:
            # Polygons
            Cx = Cy = A = 0.0
            for i in range(len(poly)):
                # If at last entry, the i+1 entry should be first: poly[j]=poly[0]
                if i != len(poly) - 1:
                    j = i + 1
                else:
                    j = 0

                # Factor
                f = poly[i][0] * poly[j][1] - poly[j][0] * poly[i][1]
                # Centre
                Cx += (poly[i][0] + poly[j][0]) * f
                Cy += (poly[i][1] + poly[j][1]) * f
                # Area
                A += f

            Af = np.absolute(A)
            ply = np.abs(np.array([(Cx / (3 * Af)), (Cy / (3 * Af))]))

            if rounded:
                return np.round(ply)
            else:
                return ply
        else:
            # <3 points = no center
            raise InvalidPolygonError(amount_of_points)

    def add_additional_points_to_polygon(
        self,
        binary_image,
        middle_addition_factor: int = 10,
        edges_reduction_factor: int = 50,
        seed: int | None = None,
    ):
        """Add more corner, edge, and middle points"""

        image_height, image_width = binary_image.shape
        image_y, image_x = np.nonzero(binary_image)

        image_coordinates = np.column_stack((image_x, image_y))
        image_coordinates_len = image_coordinates.shape[0]

        # Corners
        image_corner_points = np.array(
            [
                [0, 0],
                [0, image_height - 1],
                [image_width - 1, 0],
                [image_width - 1, image_height - 1],
            ]
        )

        # Generator based on seed
        generator = np.random.default_rng(seed=seed)

        # Get fraction of the points of the edge image
        image_edge_points = image_coordinates[
            generator.permutation(image_coordinates_len)[
                : (int(np.round(image_coordinates_len / edges_reduction_factor)))
            ]
        ]

        # Addition of random points
        random_points = generator.random((middle_addition_factor, 2))
        random_points[:, 0] = np.round(random_points[:, 0] * image_width)
        random_points[:, 1] = np.round(random_points[:, 1] * image_height)

        # Complete (unique_output_file_name) point set
        image_point_set = np.unique(
            np.vstack((image_edge_points, random_points, image_corner_points)), axis=0
        ).astype(int)

        # Replace points if do not comply with image height/width
        point_set_width = image_point_set[:, 0]
        point_set_height = image_point_set[:, 1]
        point_set_height[point_set_height >= image_height] = image_height - 1
        point_set_width[point_set_width >= image_width] = image_width - 1

        return np.fliplr(
            np.concatenate(
                (
                    self._numpy_transpose(self._shape2_d(point_set_height)),
                    self._numpy_transpose(self._shape2_d(point_set_width)),
                ),
                axis=1,
            )
        )

    def _get_voronoi_finite_polygons(self, voronoi, radius=None):
        """
        Reconstruct infinite voronoi regions in a 2D diagram to finite
        regions.
        Parameters
        ----------
        voronoi : Voronoi
            Input diagram
        radius : float, optional
            Distance to 'points at infinity'.
        Returns
        -------
        regions : list of tuples
            Indices of vertices in each revised Voronoi regions.
        vertices : list of tuples
            Coordinates for revised Voronoi vertices. Same as coordinates
            of input vertices, with 'points at infinity' appended to the
            end.

        Sklavit/e05f0b61cb12ac781c93442fbea4fb55
        """

        if voronoi.points.shape[1] != 2:
            raise ValueError("Requires 2D input")

        new_regions = []
        new_vertices = voronoi.vertices.tolist()

        center = voronoi.points.mean(axis=0)
        if radius is None:
            radius = np.ptp(voronoi.points).max() * 2

        # Construct a map containing all ridges for a given point
        all_ridges = {}
        for (p1, p2), (v1, v2) in zip(voronoi.ridge_points, voronoi.ridge_vertices):
            all_ridges.setdefault(p1, []).append((p2, v1, v2))
            all_ridges.setdefault(p2, []).append((p1, v1, v2))

        # Reconstruct infinite regions
        for p1, region in enumerate(voronoi.point_region):
            vertices = voronoi.regions[region]

            if all(v >= 0 for v in vertices):
                # finite region
                new_regions.append(vertices)
                continue

            # reconstruct a non-finite region
            ridges = []
            if p1 in all_ridges:
                ridges = all_ridges[p1]

            new_region = [v for v in vertices if v >= 0]

            for p2, v1, v2 in ridges:
                if v2 < 0:
                    v1, v2 = v2, v1
                if v1 >= 0:
                    # finite ridge: already in the region
                    continue

                # Compute the missing endpoint of an infinite ridge
                t = voronoi.points[p2] - voronoi.points[p1]  # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = voronoi.points[[p1, p2]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = voronoi.vertices[v2] + direction * radius

                new_region.append(len(new_vertices))
                new_vertices.append(far_point.tolist())

            # sort region counterclockwise
            vs = np.asarray([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
            new_region = np.array(new_region)[np.argsort(angles)]

            # finish
            new_regions.append(new_region.tolist())

        return new_regions, np.asarray(new_vertices)

    def _get_colours(self, image, points):
        return image[
            self._numpy_transpose(self._shape2_d(points[:, 1])),
            self._numpy_transpose(self._shape2_d(points[:, 0])),
            :,
        ].reshape(-1, 3)

    def _shape2_d(self, element):
        return np.reshape(element, (1, element.size))

    def _numpy_transpose(self, element):
        return np.transpose(element)
