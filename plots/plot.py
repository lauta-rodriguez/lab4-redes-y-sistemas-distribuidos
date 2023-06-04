from parse import *
import matplotlib.pyplot as plt

AMOUNT_SIM = 3
SIM_TIME = 200

simulations = {
    'SIM_1': (1, 1),
    'SIM_2': (1, 2),
    'SIM_3': (2, 1),
    'SIM_4': (2, 2)
}

iterations = {
    '1': 0.3,
    '2': 0.6,
    '3': 1
}

# TODO: definir colores para cada modulo en cada parte
# TODO: no hardcodear los nombres de los modulos, ponerlos en un diccionario

################################################################################
# SIMPLE PLOTS
################################################################################


# time vs buffer plot for a single simulation
# uses vectors
def time_vs_buffer(module, sim, it):
    time = get_data(module, 'Buffer Size', 'time', 'vectors', sim, it)
    buffer_size = get_data(module, 'Buffer Size', 'value', 'vectors', sim, it)

    if (time is not None and buffer_size is not None):
        time = list(map(float, time))
        buffer_size = list(map(float, buffer_size))

        plt.plot(time, buffer_size, label=f'{module}')


def time_vs_delay(module, sim, it=1):
    time = get_data(module, 'Delay', 'time', 'vectors', sim, it)
    delay = get_data(module, 'Delay', 'value', 'vectors', sim, it)

    if (time is not None and delay is not None):
        time = list(map(float, time))
        delay = list(map(float, delay))

        plt.plot(
            time, delay, label=f'interArrivalTime = {iterations[str(it)]}')


def offered_vs_payload(sim):
    offered_load = [0]
    payload = [0]
    sent_packets = 0

    nodes = [0, 1, 2, 3, 4, 6, 7]

    # for each simulation
    for it in range(AMOUNT_SIM, 0, -1):
        # for each transmitter node
        for _, key in enumerate(nodes):
            cant = get_data(f'Network.node[{key}].app', 'sent packets',
                            'value', 'scalars', sim, it)
            if (cant is not None):
                sent_packets += cant

        delivered_packets = get_data(
            f'Network.node[5].app', 'delivered packets', 'value', 'scalars', sim, it)

        offered_load.append(float(sent_packets)/SIM_TIME)
        payload.append(float(delivered_packets)/SIM_TIME)

    print(f'Parte {sim[0]}, caso {sim[1]} - offered load {offered_load}')
    print(f'Parte {sim[0]}, caso {sim[1]} - payload      {payload}')

    plt.plot(offered_load, payload, label=f'Parte {sim[0]}, caso {sim[1]}')


def offered_vs_delay(sim):
    offered_load = [0]
    delay = [0]
    sent_packets = 0

    nodes = [0, 1, 2, 3, 4, 6, 7]

    # for each simulation
    for it in range(AMOUNT_SIM, 0, -1):

        if not simulation_exists:
            continue

        # for each transmitter node
        for _, key in enumerate(nodes):
            cant = get_data(f'Network.node[{key}].app', 'sent packets',
                            'value', 'scalars', sim, it)

            if (cant is not None):  # value not found
                sent_packets += cant

        avg_delay = get_data(
            f'Network.node[5].app', 'Average delay', 'value', 'scalars', sim, it)

        offered_load.append(float(sent_packets)/SIM_TIME)
        delay.append(float(avg_delay))

    plt.plot(offered_load, delay, label=f'Parte {sim[0]}, caso {sim[1]}')

################################################################################
# COMPUND PLOTS
################################################################################


# time vs buffer plot for every non empty buffer in the sim simulation
def time_vs_buffer_cmp(sim, iteration=1):
    plt.figure()

    # add whitespace at the bottom of the figure
    plt.subplots_adjust(bottom=0.16)

    # display plot info
    plt.suptitle(f'Parte {sim[0]}, caso {sim[1]}')
    plt.title('Tiempo vs tamaño de búfer')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Tamaño de búfer (paquetes)')
    plt.text(
        0.5, -0.2, f'interArrivalTime = {iterations[str(iteration)]}', transform=plt.gca().transAxes, ha='center', va='bottom')

    # set axis length
    plt.xlim(0, 200)
    plt.ylim(0, 800)

    # plot every non empty buffer
    nodes = [0, 1, 2, 3, 4, 6, 7]
    for _, key in enumerate(nodes):
        time_vs_buffer(f'Network.node[{key}].lnk[0]', sim, iteration)
        time_vs_buffer(f'Network.node[{key}].lnk[1]', sim, iteration)

    plt.legend(loc='upper left')

    save_plot(f'time-buffer-p{sim[0]}c{sim[1]}.png')
    # plt.show()
    plt.clf()


# time vs delay plot for every non empty buffer in the sim simulation, for every
# iteration
def time_vs_delay_cmp(sim):
    plt.figure()

    # add whitespace at the bottom of the figure
    plt.subplots_adjust(bottom=0.16)

    # display plot info
    plt.suptitle(f'Parte {sim[0]}, caso {sim[1]}')
    plt.title('Tiempo vs delay')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Delay (s)')

    plt.xlim(0, 80)
    plt.ylim(0, 80)

    for sim_iteration in range(AMOUNT_SIM, 0, -1):
        time_vs_delay('Network.node[5].app', sim, sim_iteration)

    plt.legend(loc='upper left')

    save_plot(f'time-delay-p{sim[0]}c{sim[1]}.png')
    # plt.show()
    plt.clf()


def offered_vs_payload_cmp():
    plt.figure()

    plt.suptitle('Carga ofrecida vs carga útil')

    plt.xlim(0, 10)
    plt.ylim(0, 10)

    plt.xlabel('Carga ofrecida')
    plt.ylabel('Carga útil')

    for _, sim in enumerate(simulations):
        offered_vs_payload(simulations[sim])

    plt.legend(loc='upper left')

    # save_plot('offered-payload.png')
    plt.show()
    # plt.clf()


# offered vs delay plot for each simulation
# made up of points for each iteration
def offered_vs_delay_cmp():
    plt.figure()

    plt.title('Carga ofrecida vs delay')

    plt.xlim(0, 40)
    plt.ylim(0, 85)

    plt.xlabel('Carga ofrecida')
    plt.ylabel('Delay')

    for _, sim in enumerate(simulations):
        offered_vs_delay(simulations[sim])

    plt.legend(loc='lower right')

    save_plot('offered-delay.png')
    # plt.show()
    plt.clf()
