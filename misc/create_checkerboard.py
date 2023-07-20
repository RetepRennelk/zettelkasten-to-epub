import matplotlib.pyplot as plt
import numpy as np

def create_checkerboard(rows, cols, square_size=30):
    checkerboard = np.zeros((rows * square_size, cols * square_size, 3), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                color = [255, 255, 255]  # White
            else:
                color = [0, 0, 0]        # Black

            checkerboard[i * square_size: (i + 1) * square_size,
                         j * square_size: (j + 1) * square_size] = color

    return checkerboard

if __name__ == '__main__':
    rows = 8  # Number of rows in the checkerboard
    cols = 8  # Number of columns in the checkerboard
    square_size = 50  # Size of each square in pixels

    checkerboard_image = create_checkerboard(rows, cols, square_size)

    plt.imshow(checkerboard_image)
    plt.axis('off')
    plt.savefig(f'../Assets/checkerboard.png', bbox_inches='tight', pad_inches=0.1)
    plt.close()