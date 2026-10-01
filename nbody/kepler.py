"""Exact (analytic) two-body orbits: a star and a companion orbiting their common centre of mass.

Units: AU, years and solar masses, so that G = 4 pi^2. Velocities are returned in km/s.

Geometry: both orbits lie in the x-y plane and are traversed anticlockwise, with the centre of mass
at the origin. The observer is far away; the line of sight makes an angle i (the inclination) with
the normal to the orbital plane (i = 90 degrees: orbit seen edge-on; i = 0: face-on), and its
projection onto the orbital plane points along the negative x-axis. The radial velocity is then
    v_rad = v_x sin i,
positive when the body moves away from the observer.
"""

import numpy as np

G = 4*np.pi**2                  # gravitational constant in AU^3 / (M_sun yr^2)
KM_S_PER_AU_YR = 4.740470       # 1 AU/yr in km/s
M_JUP = 9.5479e-4               # Jupiter mass in solar masses
R_SUN = 0.00465047              # solar radius in AU
DAYS_PER_YEAR = 365.25


def period(a, m_total):
    """Orbital period (years) for relative semi-major axis a (AU) and total mass (M_sun): Kepler III."""
    return 2*np.pi*np.sqrt(a**3/(G*m_total))


def plot_times(P, e, n=1000):
    """n times (years) covering one period P, evenly spaced in eccentric anomaly: dense near the
    pericentre, where the bodies move fastest, so that curves stay smooth at high eccentricity."""
    E = np.linspace(0, 2*np.pi, n)
    return (E - e*np.sin(E))*P/(2*np.pi)


def solve_kepler(mean_anomaly, e, tol=1e-12, max_iter=50):
    """Eccentric anomaly E solving Kepler's equation  E - e sin E = M  (Newton's method)."""
    M = np.mod(np.asarray(mean_anomaly, dtype=float), 2*np.pi)
    E = M + e*np.sin(M) if e < 0.8 else np.full_like(M, np.pi)   # standard starting guesses
    for _ in range(max_iter):
        dE = (E - e*np.sin(E) - M)/(1 - e*np.cos(E))
        E = E - dE
        if np.all(np.abs(dE) < tol):
            break
    return E


class Orbit:
    """Star and companion at times t (years after the pericentre passage).

    m_star, m_comp: masses (M_sun); a: semi-major axis of the relative orbit (AU); e: eccentricity;
    omega: direction of the companion's pericentre, measured anticlockwise from the +x axis (radians).

    Attributes: star_x, star_y, comp_x, comp_y (AU) and star_vx, star_vy, comp_vx, comp_vy (km/s).
    """

    def __init__(self, t, m_star=1.0, m_comp=M_JUP, a=1.0, e=0.0, omega=0.0):
        self.t = np.asarray(t, dtype=float)
        self.m_star, self.m_comp, self.a, self.e, self.omega = m_star, m_comp, a, e, omega
        m_total = m_star + m_comp
        self.period = period(a, m_total)

        # Relative orbit (companion as seen from the star)
        E = solve_kepler(2*np.pi*self.t/self.period, e)
        nu = 2*np.arctan2(np.sqrt(1 + e)*np.sin(E/2), np.sqrt(1 - e)*np.cos(E/2))   # true anomaly
        r = a*(1 - e*np.cos(E))
        phi = nu + omega                                   # direction of the separation vector
        v0 = np.sqrt(G*m_total/(a*(1 - e**2)))             # AU/yr
        v_r = v0*e*np.sin(nu)                              # radial velocity component
        v_phi = v0*(1 + e*np.cos(nu))                      # tangential velocity component
        x, y = r*np.cos(phi), r*np.sin(phi)
        vx = (v_r*np.cos(phi) - v_phi*np.sin(phi))*KM_S_PER_AU_YR
        vy = (v_r*np.sin(phi) + v_phi*np.cos(phi))*KM_S_PER_AU_YR

        # Centre of mass at rest at the origin: each body gets its share of the relative motion
        f_star, f_comp = m_comp/m_total, m_star/m_total
        self.star_x, self.star_y, self.star_vx, self.star_vy = -f_star*x, -f_star*y, -f_star*vx, -f_star*vy
        self.comp_x, self.comp_y, self.comp_vx, self.comp_vy = f_comp*x, f_comp*y, f_comp*vx, f_comp*vy

    def radial_velocity(self, inclination):
        """Radial velocities (km/s) of star and companion; inclination in radians (pi/2: edge-on)."""
        return self.star_vx*np.sin(inclination), self.comp_vx*np.sin(inclination)


def semi_amplitude(m_star, m_comp, a, e, inclination):
    """Radial-velocity semi-amplitude K (km/s) of the star and of the companion.

    K_star = (2 pi G / P)^(1/3) m_comp sin i / (m_star + m_comp)^(2/3) / sqrt(1 - e^2); K_comp follows
    from momentum conservation: K_comp / K_star = m_star / m_comp.
    """
    m_total = m_star + m_comp
    P = period(a, m_total)
    k_star = (2*np.pi*G/P)**(1/3)*m_comp*np.sin(inclination)/m_total**(2/3)/np.sqrt(1 - e**2)
    return k_star*KM_S_PER_AU_YR, k_star*KM_S_PER_AU_YR*m_star/m_comp
