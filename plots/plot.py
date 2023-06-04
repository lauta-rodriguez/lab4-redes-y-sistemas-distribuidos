from parse import *
import matplotlib.pyplot as plt

AMOUNT_SIM = 5
SIM_TIME = 200

simulations = {
    'SIM_1': (1, 1),
    'SIM_2': (1, 2),
    'SIM_3': (2, 1),
    'SIM_4': (2, 2)
}

# TODO: definir colores para cada modulo en cada parte
# TODO: no hardcodear los nombres de los modulos, ponerlos en un diccionario

################################################################################
# SIMPLE PLOTS
################################################################################


def time_vs_buffer(module, sim, it=1):
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

        plt.plot(time, delay, label=f'{module}')
        plt.show()


def offered_vs_payload(sim):
    offered_load = [0]
    payload = [0]
    sent_packets = 0

    if sim[1] == 1:
        nodes = [0, 2]
    else:
        nodes = [0, 1, 2, 3, 4, 6, 7]

    # for each simulation
    for it in range(1, 0, -1):
        # for each transmitter node
        for _, key in enumerate(nodes):
            cant = get_data(f'Network.node[{key}].app', 'sent packets',
                            'value', 'scalars', sim, it)
            if (cant is not None):
                sent_packets += cant

        delivered_packets = get_data(
            f'Network.node[5].app', 'delivered packets', 'value', 'scalars', sim, it)

        print(sent_packets)
        print(delivered_packets)

        offered_load.append(float(sent_packets)/SIM_TIME)
        payload.append(float(delivered_packets)/SIM_TIME)

    plt.plot(offered_load, payload, label=f'caso {sim[1]}')


def offered_vs_delay(sim):
    offered_load = [0]
    delay = [0]
    sent_packets = 0

    if sim[1] == 1:
        nodes = [0, 2]
    else:
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

        print(sent_packets)
        print(avg_delay)

        offered_load.append(float(sent_packets)/SIM_TIME)
        delay.append(float(avg_delay))

    plt.plot(offered_load, delay, label=f'caso {sim[1]}')

################################################################################
# COMPUND PLOTS
################################################################################


def time_vs_buffer_cmp(sim):
    plt.figure()

    plt.suptitle('Tiempo vs tamaño de búfer')

    plt.xlim(0, 200)
    plt.ylim(0, 800)

    if sim[1] == 1:
        nodes = [0, 2]
    else:
        nodes = [0, 1, 2, 3, 4, 6, 7]

    for _, key in enumerate(nodes):
        time_vs_buffer(f'Network.node[{key}].lnk[0]', sim)
        time_vs_buffer(f'Network.node[{key}].lnk[1]', sim)

    plt.legend(loc='upper left')

    save_plot(f'time-buffer-p{sim[0]}c{sim[1]}.png')
    plt.show()
    # plt.clf()


def time_vs_delay_cmp(sim):
    plt.figure()

    plt.suptitle('Tiempo vs delay')

    plt.xlim(0, 200)
    plt.ylim(0, 200)

    time_vs_delay('Network.node[5].app', sim)

    plt.legend(loc='upper left')

    # save_plot(f'time-delay-p{sim[0]}c{sim[1]}.png')
    plt.show()
    # plt.clf()


def offered_vs_payload_cmp(sim):
    plt.figure()

    plt.suptitle('Carga ofrecida vs carga útil')

    plt.xlim(0, 10)
    plt.ylim(0, 10)

    plt.xlabel('Carga ofrecida')
    plt.ylabel('Carga útil')

    # for _, key in enumerate(simulations):
    offered_vs_payload(sim)

    plt.legend(loc='upper left')

    save_plot('offered-payload.png')
    # plt.show()
    plt.clf()


def offered_vs_delay_cmp(sim):
    plt.figure()

    plt.suptitle('Carga ofrecida vs delay')

    plt.xlim(0, 10)
    plt.ylim(0, 70)

    plt.xlabel('Carga ofrecida')
    plt.ylabel('Delay')

    # for _, key in enumerate(simulations):
    offered_vs_delay(sim)

    plt.legend(loc='upper left')

    save_plot('offered-delay.png')
    # plt.show()
    plt.clf()
