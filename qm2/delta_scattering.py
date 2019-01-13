# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def arg(ρ, a=1, ħ=1, m=1, γ=1):
    """
    expression whichs argument is considered in the phase shift equation
    """
    return np.sin(ρ) + (ħ**2*ρ/a) / (2*m*γ) * np.exp(1j*ρ)

def δ(ρ, a=1, ħ=1, m=1, γ=1):
    """
    phase shift in potential
        V(r) = γ*δ(r-a)
    with ρ = k/a
    """
    return -ρ + np.angle(np.sin(ρ) + (ħ**2*ρ/a) / (2*m*γ) * np.exp(1j*ρ))

def σ(δ, ρ, **kwds):
    """
    scattering cross section for s-wave (l=0)
    δ - phase shift
    ρ = k/a
    """
    return 4*np.pi / (ρ/kwds.get('a', 1))**2 * np.sin(δ(ρ, **kwds))**2


x = np.linspace(0, 4*np.pi, 2000)

plt.figure()
plt.plot(x, 4*np.pi*np.sin(δ(x, γ=100))**2,
         label='$\sin(\delta)^2$, $\gamma$ = 100')
#  plt.plot(x, δ(x, γ=1), label='phase shift, $\gamma$ = 1')
plt.plot(x, δ(x, γ=100), label='phase shift, $\gamma$ = 100')
#  plt.plot(x, σ(δ, x, γ=1), label='scattering cross section, $\gamma$ = 1')
plt.plot(x, σ(δ, x, γ=100), label='scattering cross section, $\gamma$ = 100')
[plt.vlines(n*np.pi, -10, 10, color='grey', linestyle='--')
 for n in (1, 2, 3, 4)]
plt.xlabel('ka')
plt.ylabel('$\delta_0$, $\sigma_0$')
plt.legend()
#  plt.show()

plt.figure()
plt.plot(x, arg(x, γ=100).real, label='Re(f), $\gamma$ = 100')
plt.plot(x, arg(x, γ=100).imag, label='Im(f), $\gamma$ = 100')
plt.plot(x, np.angle(arg(x, γ=100)), label='arg(f), $\gamma$ = 100')
plt.xlabel('ka')
plt.ylabel('f')
plt.legend()
#  plt.show()

plt.figure()
plt.plot(arg(x, γ=100).real, arg(x, γ=100).imag,
         label='f in the complex plane, $\gamma$ = 100')
plt.xlabel('Re(f)')
plt.ylabel('Im(f)')
plt.legend()
#  plt.show()

for i in plt.get_fignums():
    f = plt.figure(i)
    f.tight_layout()
    f.savefig('fig%d.png' % i, dpi=300)


#  vim: set ff=dos tw=79 sw=4 ts=8 et ic ai :
