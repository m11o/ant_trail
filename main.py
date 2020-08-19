from matplotlib import animation, rc
import matplotlib.pyplot as plt

from field.main_field import MainField
from ant import Ant

artists = []
searchers_count = []
returnees_count = []
servants_count = []
t = []


def draw_animation(X, Y, ant_amount, food_positions = None, nest_position = None):
    field = MainField(X, Y, food_positions=food_positions, nest_position=nest_position)
    ants = Ant.generate_ants(ant_amount, field)

    fig, ax = plt.subplots(dpi = 150)

    for i in range(1500):
        searchers = 0
        returnees = 0
        servants = 0

        for ant in ants:
            ant.move(field)

            if ant.is_searcher():
                searchers += 1
            elif ant.is_returnee():
                returnees += 1
            elif ant.is_servant():
                servants += 1

        searchers_count.append(searchers)
        returnees_count.append(returnees)
        servants_count.append(servants)
        t.append(i)

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
ani = draw_animation(100, 100, 500, food_positions = food_positions, nest_position = nest_position)
ani.save('anim.mp4', writer="ffmpeg")

figure = plt.figure()
plt.plot(t, searchers_count, color='blue', label='searcher')
plt.plot(t, returnees_count, color='red', label='returnee')
plt.plot(t, servants_count, color='black', label='servant')
figure.savefig('graph.png')
