from __future__ import annotations
from dataclasses import asdict, dataclass


@dataclass
class CONSTANTS:
    alpha_A         = 50
    alpha_A_prime   = 500
    alpha_R         = 0.01
    alpha_R_prime   = 50
    beta_A          = 50
    beta_R          = 5
    delta_MA        = 10
    delta_MR        = 0.5
    delta_A         = 1
    delta_R         = 0.2
    gamma_A         = 1
    gamma_R         = 1
    gamma_C         = 2
    theta_A         = 50
    theta_R         = 100


@dataclass
class Variables:
    D_A: float
    D_R: float
    D_A_prime: float
    D_R_prime: float
    M_A: float
    A: float
    M_R: float
    R: float
    C: float

    @staticmethod
    def from_array(x: list[float]) -> Variables:
        return Variables(*x)

    def to_array(self):
        return list(asdict(self).values())


def calc_ODE(t: float, x: list[float]) -> list[float]:
    c = CONSTANTS()
    v = Variables.from_array(x)

    DA = c.theta_A * v.D_A_prime - c.gamma_A * v.D_A * v.A
    DR = c.theta_R * v.D_R_prime - c.gamma_R * v.D_R * v.A
    D_A_prime = c.gamma_A * v.D_A * v.A - c.theta_A * v.D_A_prime
    D_R_prime = c.gamma_R * v.D_R * v.A - c.theta_R * v.D_R_prime
    M_A = c.alpha_A_prime * v.D_A_prime + c.alpha_A * v.D_A - c.delta_MA * v.M_A
    A = c.beta_A * v.M_A + c.theta_A * v.D_A_prime + c.theta_R * v.D_R_prime - v.A * (c.gamma_A * v.D_A + c.gamma_R * v.D_R + c.gamma_C * v.R + c.delta_A)
    M_R = c.alpha_R_prime * v.D_R_prime + c.alpha_R * v.D_R - c.delta_MR * v.M_R
    R = c.beta_R * v.M_R - c.gamma_C * v.A * v.R + c.delta_A * v.C - c.delta_R * v.R
    C = c.gamma_C * v.A * v.R - c.delta_A * v.C

    return[DA, DR, D_A_prime, D_R_prime, M_A, A, M_R, R, C]

