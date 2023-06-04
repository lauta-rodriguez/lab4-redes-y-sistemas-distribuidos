from plot import *
import matplotlib.pyplot as plt

simulations = {
    'SIM_1': (1, 1),
    'SIM_2': (1, 2),
    'SIM_3': (2, 1),
    'SIM_4': (2, 2)
}

AMOUNT_SIM = 3

for _, sim in enumerate(simulations):
    for sim_iteration in range(1, AMOUNT_SIM+1):
        time_vs_buffer_cmp(simulations[sim], sim_iteration)

# genera un gráfico por cada simulacion
for _, sim in enumerate(simulations):
    # grafica de time vs delay para una misma simulacion para cada interArrivalTime
    time_vs_delay_cmp(simulations[sim])

# grafica de offered load vs delay para cada simulacion sobre un mismo plot
offered_vs_delay_cmp()

# test
# offered_load = [0, 0.0, 3.295, 9.825]
# delay = [0, 0.98, 0.985, 0.985]
#
# plt.plot(offered_load, delay, label=f'Parte 1, caso 1')
# plt.show()
