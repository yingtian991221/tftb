import numpy as np
from numpy import pi
from scipy.signal import hilbert
from frequency_modulated import fmconst


def anaask(n_points, n_comp=None, f0=0.25):
    """Generate an amplitude shift (ASK) keying signal.

    :param n_points: number of points.
    :param n_comp: number of points of each component.
    :param f0: normalized frequency.
    :type n_points: int
    :type n_comp: int
    :type f0: float
    :return: Tuple containing the modulated signal and the amplitude modulation.
    :rtype: tuple(numpy.ndarray)
    """
    if n_comp is None:
        n_comp = np.round(n_points / 2)
    if (f0 < 0) or (f0 > 0.5):
        raise TypeError("f0 must be between 0 and 0.5")
    m = np.ceil(n_points / n_comp)
    jumps = np.random.rand(m)
    am = np.kron(jumps, np.ones((n_comp,)))[:n_points]
    fm, iflaw = fmconst(n_points, f0, 1)
    y = am * fm
    return y, am


def anabpsk(n_points, n_comp=None, f0=0.25):
    """Binary phase shift keying (BPSK) signal.

    :param n_points: number of points.
    :param n_comp: number of points in each component.
    :param f0: normalized frequency.
    :type n_points: int
    :type n_comp: int
    :type f0: float
    :return: BPSK signal
    :rtype: numpy.ndarray
    """
    if n_comp is None:
        n_comp = np.round(n_points / 5)
    if (f0 < 0) or (f0 > 0.5):
        raise TypeError("f0 must be between 0 and 0.5")
    m = np.ceil(n_points / n_comp)
    jumps = 2.0 * np.round(np.random.rand(m)) - 1
    am = np.kron(jumps, np.ones((n_comp,)))[:n_points]
    y = am * fmconst(n_points, f0, 1)[0]
    return y, am


def anafsk(n_points, n_comp=None, Nbf=4):
    """Frequency shift keying (FSK) signal.

    :param n_points: number of points.
    :param n_comp: number of points in each components.
    :param Nbf: number of distinct frequencies.
    :type n_points: int
    :type n_comp: int
    :type Nbf: int
    :return: FSK signal.
    :rtype: numpy.ndarray
    """
    if n_comp is None:
        n_comp = np.round(n_points / 5)
    m = np.ceil(n_points / n_comp)
    freqs = 0.25 + 0.25 * (np.floor(Nbf * np.random.rand(m, 1)) / Nbf - (Nbf - 1) / (2 * Nbf))
    iflaw = np.kron(freqs, np.ones((n_comp,))).ravel()
    y = np.exp(1j * 2 * pi * np.cumsum(iflaw))
    return y, iflaw


def anapulse(n_points, ti=None):
    """Analytic projection of unit amplitude impulse signal.

    :param n_points: Number of points.
    :param ti: time position of the impulse.
    :type n_points: int
    :type ti: float
    :return: analytic impulse signal.
    :rtype: numpy.ndarray
    """
    if ti is None:
        ti = np.round(n_points / 2)
    t = np.arange(n_points)
    x = t == ti
    y = hilbert(x.astype(float))
    return y


def anaqpsk(n_points, n_comp=None, f0=0.25):
    """Quaternary Phase Shift Keying (QPSK) signal.

    :param n_points: number of points.
    :param n_comp: number of points in each component.
    :param f0: normalized frequency
    :type n_points: int
    :type n_comp: int
    :type f0: float
    :return: complex phase modulated signal of normalized frequency f0
    :rtype: numpy.ndarray
    """
    if n_comp is None:
        n_comp = np.round(n_points / 5)
    if (f0 < 0) or (f0 > 0.5):
        raise TypeError("f0 must be between 0 and 0.5")
    m = np.ceil(n_points / n_comp)
    jumps = np.floor(4 * np.random.rand(m))
    jumps[jumps == 4] = 3
    pm0 = (np.pi * np.kron(jumps, np.ones((n_comp,))) / 2).ravel()
    tm = np.arange(n_points) - 1
    pm = 2 * np.pi * f0 * tm + pm0
    y = np.exp(1j * pm)
    return y, pm0


def anasing(n_points, t0=None, h=0.0):
    """Lipschitz singularity.

    :param n_points: number of points in time.
    :param t0: time localization of singularity
    :param h: strength of the singularity
    :type n_points: int
    :type t0: float
    :type h: float
    :return: N-point Lipschitz singularity centered around t0
    :rtype: numpy.ndarray
    """
    """Refer to the wiki page on `Lipschitz condition`, good test case."""
    if t0 is None:
        t0 = n_points / 2
    if h <= 0:
        step = 1.0 / n_points
        f = np.arange(step, 0.5 - 1.0 / n_points + 2*step, step=step)
        y = np.zeros((n_points / 2,), dtype=float)
        y[:n_points / 2] = (f ** (-1 - h)) ** np.exp(-1j * 2 * pi * f * (t0 - 1))
        x = np.real(np.fft.ifft(y, n_points))
        x = x / x.max()
        x = x - np.sign(x.min() * np.abs(x.min()))
    else:
        t = np.arange(n_points)
        x = np.abs(t - t0) ** h
        x = x.max() - x
    x = hilbert(x)
    return x


def anastep(n_points, ti=None):
    """Analytic projection of unit step signal.

    :param n_points: Number of points.
    :param ti: starting position of unit step.
    :type n_points: int
    :type ti: float
    :return: output signal
    :rtype: numpy.ndarray
    """
    if ti is None:
        ti = np.round(n_points / 2)
    t = np.arange(n_points)
    x = t > ti
    y = hilbert(x.astype(float))
    return y