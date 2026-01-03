import numpy as np
import matplotlib.pyplot as plt
import RCFilterModel

if __name__ == "__main__":
    R = 10e+3
    C = 15e-9
    R2 = 10e+3
    C2 = C*5
    dt = 1e-5
    t_end = 2e-2

    # setup simulation
    rc_filter = RCFilterModel.RCFilter(R, C, dt)
    rc_filter2 = RCFilterModel.RCFilter(R2, C2, dt)
    
    t = np.arange(0, t_end, dt)
    Vin = np.heaviside(t - 0.01, 1.0)  # Step input at t=10ms
    Vout = []
    Vout2 = []
    Vin_Real = []

    # simulate system response
    for vin in Vin:
        if vin == 1:
            Vin_Real.append(vin + 0.1 * np.random.normal())  # Add noise to input only when vin is 1
        else:
            Vin_Real.append(vin)
        vout = rc_filter.step(Vin_Real[-1])  # Add noise to input
        Vout.append(vout)

    # Re-run simulation with same noisy input
    for vin in Vin_Real:
        vout2 = rc_filter2.step(vin)
        Vout2.append(vout2)


    tau1 = R * C
    tau2 = R2 * C2
    t_settle1 = -tau1 * np.log(1 - 0.98)  # Time to reach 98% of step
    t_settle2 = -tau2 * np.log(1 - 0.98)

    steady_start1 = int((0.01 + t_settle1) / dt)  # Step at 10ms
    steady_start2 = int((0.01 + t_settle2) / dt)

    Vout_steady = Vout[steady_start1:]
    Vout2_steady = Vout2[steady_start2:]

    std1 = np.std(Vout_steady)
    std2 = np.std(Vout2_steady)

    # Plot both simulations in the same window as two subplots
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # First simulation
    axs[0].plot(t, Vin, label='Vin (Step Input)')
    axs[0].plot(t, Vout, label='Vout (R = 1kΩ, C = 1μF)')
    axs[0].plot(t, Vin_Real, label='Vin (Noisy Input)', alpha=0.5)
    axs[0].set_ylabel('Voltage (V)')
    axs[0].set_title(f'System Response (R = 10kΩ, C = 1μF)\nSteady-state std: {std1:.5f} V or {100 * std1 / np.mean(Vout_steady):.2f}%\n98% settle: {t_settle1*1e3:.2f} ms')
    f"{100 * std1 / np.mean(Vout_steady):.2f}%"
    axs[0].legend()
    axs[0].grid(True)

    # Second simulation
    axs[1].plot(t, Vin_Real, label='Vin (Noisy Input)', alpha=0.5)
    axs[1].plot(t, Vout2, label='Vout (R = 10kΩ, C = 5μF)')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Voltage (V)')
    axs[1].set_title(f'System Response (R = 10kΩ, C = 5μF)\nSteady-state std: {std2:.5f} V or {100 * std2 / np.mean(Vout2_steady):.2f}%\n98% settle: {t_settle2*1e3:.2f} ms')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()
