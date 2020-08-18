from matplotlib import animation, rc
import matplotlib.pyplot as plt

from field.main_field import MainField
from ant import Ant


def draw_animation(X, Y, ant_amount, food_positions = None, nest_position = None):
    field = MainField(X, Y, food_positions=food_positions, nest_position=nest_position)
    ants = Ant.generate_ants(ant_amount, field)

    fig, ax = plt.subplots(dpi = 150)

    artists = []

    for i in range(1000):
        for ant in ants:
            ant.move(field)

        for pheromones in field.pheromones_field.field:
            for pheromone in pheromones:
                if bool(pheromone):
                    pheromone.decrease()

        im = ax.matshow(field.field, interpolation='none', cmap="binary")
        ax.set_aspect('equal')
        artists.append([im])

    ani = animation.ArtistAnimation(fig, artists, interval=100)
    rc('animation', html='jshtml')
    return ani


food_positions = [[90, 10], [80, 20]]
nest_position = [10, 50]
ani = draw_animation(100, 100, 300, food_positions = food_positions, nest_position = nest_position)
ani.save('anim.mp4', writer="ffmpeg")
