def contains_label(pixels: list[list[int]]) -> bool:
    for j in range(0, len(pixels)):
        for i in range(0, len(pixels[j])):
            if pixels[i][j] == 0:
                if pixels[i-1][j-1] != 255:
                    continue
                if pixels[i][j-1] != 255:
                    continue
                if pixels[i+1][j-1] != 255:
                    continue
                if pixels[i-1][j] != 255:
                    continue
                if pixels[i+1][j] != 255:
                    continue
                if pixels[i-1][j+1] != 255:
                    continue
                if pixels[i][j+1] != 255:
                    continue
                if pixels[i+1][j+1] != 255:
                    continue
                return True
    return False
