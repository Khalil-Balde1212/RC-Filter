import numpy as np

import matplotlib.pyplot as plt

class RCFilter:
    def __init__(self, R, C, delta_t):
        self.R = R
        self.C = C
        self.delta_t = delta_t
        self.Vout = 0.0  # Initial output voltage

    def step(self, Vin):
        # ODE: 
        self.Vout = self.Vout + self.delta_t/(self.R * self.C) * (Vin - self.Vout)
        return self.Vout

if __name__ == "__main__":
    R = 1e+3
    C = 1e-6  
    dt = 1e-5
    t_end = 2e-2

    # setup simulation
    rc_filter = RCFilter(R, C, dt)
    t = np.arange(0, t_end, dt)
    Vin = np.heaviside(t - 0.01, 1.0)  # Step input at t=10ms
    Vout = []

    # simulate system response
    for vin in Vin:
        vout = rc_filter.step(vin)
        Vout.append(vout)


    # Plot results
    plt.plot(t, Vin, label='Vin (Step Input)')
    plt.plot(t, Vout, label='Vout (RC Filter Output)')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title('System Response')
    plt.legend()
    plt.grid(True)
    plt.show()