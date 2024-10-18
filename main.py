import matplotlib.pyplot as plt
import os
import scipy.integrate
import time

import ode


def plot_figure_AB(sol, name: str, path: str | None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(sol.t, sol.y[:][5])
    ax1.set_title("Life cycle of A")
    ax1.set_xlim([0, 400])
    ax1.set_ylim([0, 2000])

    ax2.plot(sol.t, sol.y[:][7])
    ax2.set_title("Life cycle of R")
    ax2.set_xlim([0, 400])
    ax2.set_ylim([0, 2000])

    fig.suptitle(name)
    fig.tight_layout()
    fig.show()

    if path is not None:
        path = os.path.join(path, "figure" + time.strftime("%H%M%S") + ".eps")
        fig.savefig(path, format="eps")


def solve_my_IVP(method: str, initial_values: ode.Variables):
    start = time.time()
    sol = scipy.integrate.solve_ivp(ode.calc_ODE, t_span=[0, 400], y0=initial_values.to_array(), method=method)
    end = time.time()
    print(f"{method} uses {end - start :.3f}s. Total steps taken is {len(sol.t)}")
    return sol


def main() -> None:
    initial_values = ode.Variables( D_A=1,
                                    D_R=1,
                                    D_A_prime=0,
                                    D_R_prime=0,
                                    M_A=0,
                                    M_R=0,
                                    A=0,
                                    R=0,
                                    C=0,
                                    )
    for method in ("RK45", "Radau", "BDF"):
        sol = solve_my_IVP(method, initial_values)
        plot_figure_AB(sol, method, "figures")

    return

if __name__ == "__main__":
    main()
