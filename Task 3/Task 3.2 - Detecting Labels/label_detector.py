# Time Complexity: O(n)
# Space Complexity: O(n)
# Extra Space Complexity: O(1)
# n: element count inside the matrix
def contains_label(pixels: list[list[int]]) -> bool:
    for j in range(1, len(pixels) - 1):
        for i in range(1, len(pixels[j]) - 1):
            if pixels[i][j] != 0:
                continue
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
