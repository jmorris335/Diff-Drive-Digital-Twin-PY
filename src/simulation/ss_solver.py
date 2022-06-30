# Modified from scipy.signal.lsim2, which could not handle multiple inputs
#
# Program: SS_Solver.py
# Author: modified by John Morris, jhmrrs@clemson.edu
# Date: 30 June 2022
# Purpose: Solve LTI systems composed within the scipy library (v. 1.8.1)
# Sources: https://github.com/scipy/scipy/blob/v1.8.1/scipy/signal/_ltisys.py#L1764-L1938

import numpy as np
from scipy import signal, integrate, interpolate

def ss_solver(system, T, U=None, X0=None, **kwargs):
    """
    Simulate output of a continuous-time linear system, by using
    the ODE solver `scipy.integrate.odeint`.

    Parameters
    ----------
    system : an instance of the `lti` class or a tuple describing the system.
        The following gives the number of elements in the tuple and
        the interpretation:

        * 1: (instance of `lti`)
        * 2: (num, den)
        * 3: (zeros, poles, gain)
        * 4: (A, B, C, D)

    T : array_like (1D or 2D), optional
        The time steps at which the input is defined and at which the
        output is desired.  The default is 101 evenly spaced points on
        the interval [0,10.0].
    U : array_like (1D or 2D), optional
        An input array describing the input at each time T.  Linear
        interpolation is used between given times.  If there are
        multiple inputs, then each column of the rank-2 array
        represents an input.  If U is not given, the input is assumed
        to be zero.
    X0 : array_like (1D), optional
        The initial condition of the state vector.  If `X0` is not
        given, the initial conditions are assumed to be 0.
    kwargs : dict
        Additional keyword arguments are passed on to the function
        `odeint`.  See the notes below for more details.

    Returns
    -------
    T : 1D ndarray
        The time values for the output.
    yout : ndarray
        The response of the system.
    xout : ndarray
        The time-evolution of the state-vector.

    Notes
    -----
    This function uses `scipy.integrate.odeint` to solve the
    system's differential equations.  Additional keyword arguments
    given to `lsim2` are passed on to `odeint`.  See the documentation
    for `scipy.integrate.odeint` for the full list of arguments.

    If (num, den) is passed in for ``system``, coefficients for both the
    numerator and denominator should be specified in descending exponent
    order (e.g. ``s^2 + 3s + 5`` would be represented as ``[1, 3, 5]``).
    """

    if isinstance(system, signal.lti): sys = system._as_ss()
    elif isinstance(system, signal.dlti):
        raise AttributeError('lsim2 can only be used with continuous-time systems.')
    else: sys = signal.lti(*system)._as_ss()

    if X0 is None: X0 = np.zeros(sys.B.shape[0], sys.A.dtype)

    T = np.atleast_1d(T)
    if len(T.shape) != 1: raise ValueError("T must be a rank-1 array.")

    if U is not None:
        U = np.atleast_1d(U)
        if len(U.shape) == 1: U = U.reshape(-1, 1)
        sU = U.shape
        if sU[0] != len(T):
            raise ValueError("U must have the same number of rows as elements in T.")

        if sU[1] != sys.inputs:
            raise ValueError("The number of inputs in U (%d) is not compatible with the" 
                             "number of system inputs (%d)" % (sU[1], sys.inputs))
        
        # Create a callable that uses linear interpolation to
        # calculate the input at any time.
        ufunc = interpolate.interp1d(T, U, kind='linear', axis=0, bounds_error=False)

        def fprime(x, t, sys, ufunc):
            """The vector field of the linear system."""
            return np.dot(sys.A, x) + np.squeeze(np.dot(sys.B, np.nan_to_num(ufunc([t])).T))
        xout = integrate.odeint(fprime, X0, T, args=(sys, ufunc), **kwargs)
        yout = np.dot(sys.C, np.transpose(xout)) + np.dot(sys.D, np.transpose(U))
    
    else:
        def fprime(x, t, sys):
            """The vector field of the linear system."""
            return np.dot(sys.A, x)
        xout = integrate.odeint(fprime, X0, T, args=(sys,), **kwargs)
        yout = np.dot(sys.C, np.transpose(xout))

    return T, np.squeeze(np.transpose(yout)), xout
