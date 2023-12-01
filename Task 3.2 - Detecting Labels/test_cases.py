test_cases = \
    [
        ([[12, 13, 14, 15],
         [0, 255, 255, 255],
         [0, 255, 0, 255],
         [255, 255, 255, 255]], True),

        ([[12, 255, 0, 255],
         [0, 255, 255, 255],
         [0, 255, 1, 255],
         [255, 255, 255, 255]], False),

        ([[255, 255, 255, 255, 255],
         [255, 0, 255, 0, 255],
         [255, 255, 255, 255, 255],
         [255, 0, 255, 0, 255],
         [255, 255, 255, 255, 255]], True),

        ([[0]], False),

        ([[255, 255, 255],
         [255, 0, 255],
         [255, 255, 255]], True),

        ([[255, 255, 254],
         [255, 0, 255],
         [255, 255, 255]], False),

        ([[145, 12, 31, 3, 123, 0],
         [41, 0, 255, 0, 255, 64],
         [255, 255, 255, 255, 255, 96],
         [255, 0, 255, 0, 255, 85],
         [1, 255, 255, 2, 0, 0],
         [255, 255, 255, 255, 255, 255]], False),

        ([[12, 57, 96, 12, 79, 84, 90],
          [0, 53, 30, 27, 58, 193, 231],
          [24, 161, 69, 95, 199, 204, 192],
          [255, 255, 255, 253, 197, 50, 29],
          [255, 0, 255, 127, 250, 93, 21],
          [255, 255, 255, 42, 202, 96, 89],
          [51, 190, 76, 83, 10, 197, 204]], True)
    ]
