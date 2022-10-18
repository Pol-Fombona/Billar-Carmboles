def create_cube(x, y, z, w, h, p, num_vertices_existing=0, tex_coord=False):
    vertices = [
        (x, y, z),
        (x + w, y, z),
        (x + w, y + h, z),
        (x, y + h, z),
        (x, y, z + p),
        (x + w, y, z + p),
        (x + w, y + h, z + p),
        (x, y + h, z + p),
    ]

    indices = [
        (
            0 + num_vertices_existing,
            2 + num_vertices_existing,
            1 + num_vertices_existing,
        ),
        (
            0 + num_vertices_existing,
            3 + num_vertices_existing,
            2 + num_vertices_existing,
        ),
        (
            4 + num_vertices_existing,
            5 + num_vertices_existing,
            6 + num_vertices_existing,
        ),
        (
            4 + num_vertices_existing,
            6 + num_vertices_existing,
            7 + num_vertices_existing,
        ),
        (
            0 + num_vertices_existing,
            1 + num_vertices_existing,
            4 + num_vertices_existing,
        ),
        (
            1 + num_vertices_existing,
            4 + num_vertices_existing,
            5 + num_vertices_existing,
        ),
        (
            2 + num_vertices_existing,
            3 + num_vertices_existing,
            7 + num_vertices_existing,
        ),
        (
            2 + num_vertices_existing,
            7 + num_vertices_existing,
            6 + num_vertices_existing,
        ),
        (
            1 + num_vertices_existing,
            2 + num_vertices_existing,
            6 + num_vertices_existing,
        ),
        (
            1 + num_vertices_existing,
            6 + num_vertices_existing,
            5 + num_vertices_existing,
        ),
        (
            0 + num_vertices_existing,
            4 + num_vertices_existing,
            7 + num_vertices_existing,
        ),
        (
            0 + num_vertices_existing,
            7 + num_vertices_existing,
            3 + num_vertices_existing,
        ),
    ]

    if tex_coord:
        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (2, 3, 0),
            (0, 1, 2),
            (2, 3, 0),
        ]

        return vertices, indices, tex_coord_vertices, tex_coord_indices

    return vertices, indices
