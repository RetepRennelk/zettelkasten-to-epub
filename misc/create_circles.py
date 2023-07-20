import matplotlib.pyplot as plt
import numpy as np

def get_rainbow_colors(num_colors):
    cmap = plt.get_cmap('rainbow')
    return [cmap(i) for i in np.linspace(0, 1, num_colors)]

# Function to create and save the animation
def create_circles(num_frames):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    colors = get_rainbow_colors(num_frames)

    for i in reversed(range(1, num_frames + 1)):
        radius = i / 2  # Change this factor to control the speed of the animation
        circle = plt.Circle((0, 0), radius, color=colors[i - 1], alpha=0.25)
        ax.add_artist(circle)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Save the frame with a unique filename (can be adjusted)
    plt.savefig(f'../Assets/circles.jpg', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close()

num_frames = 10  # Adjust this value to control the number of frames in the animation
create_circles(num_frames)
