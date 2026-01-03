import RCFilterModel
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    R = 10e+3      # 10,000 Ohms (10 kΩ)
    C = 15e-9      # 15 nanofarads (15 nF)
    R2 = 10e+3     # 10,000 Ohms (10 kΩ)
    C2 = C*5       # 75 nanofarads (75 nF)
    dt = 1e-5
    t_end = 5e-2

    # setup simulation
    rc_filter = RCFilterModel.RCFilter(R, C, dt)
    t = np.arange(0, t_end, dt)
    Vin = np.sin(2 * np.pi * 50 * t)
    Vout = []

    # simulate system response
    for vin in Vin:
        vout = rc_filter.step(vin)
        Vout.append(vout)
    # Re-run simulation with same input for different RC
    rc_filter2 = RCFilterModel.RCFilter(R2, C2, dt)
    Vout2 = []
    for vin in Vin:
        vout2 = rc_filter2.step(vin)
        Vout2.append(vout2)
    

    # Plot results for both RC filters in separate subplots on the same figure
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(t, Vin, label='Vin (Sine Input)')
    axs[0].plot(t, Vout, label='Vout (R={}, C={})'.format(R, C))
    axs[0].set_ylabel('Voltage (V)')
    axs[0].set_title('System Response for RC Filter 1')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(t, Vin, label='Vin (Sine Input)')
    axs[1].plot(t, Vout2, label='Vout2 (R={}, C={})'.format(R2, C2))
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Voltage (V)')
    axs[1].set_title('System Response for RC Filter 2')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()
