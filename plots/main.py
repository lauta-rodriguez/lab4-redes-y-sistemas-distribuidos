from plot import *

simulations = {
    'SIM_1': (1, 1),
    'SIM_2': (1, 2),
    'SIM_3': (2, 1),
    'SIM_4': (2, 2)
}

# time_vs_buffer_cmp(simulations['SIM_4'])
# time_vs_delay('Network.node[5].app', simulations['SIM_4'], it=1)
# offered_vs_payload_cmp(simulations['SIM_4'])
offered_vs_delay_cmp(simulations['SIM_4'])
