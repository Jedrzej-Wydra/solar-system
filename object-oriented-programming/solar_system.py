import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

class CelestialBody:
    def __init__(self, name, radius, color, year, parent = None, theta0 = 0):
        self.name = name
        self.radius = radius
        self.color = color
        self.year = year
        self.theta0 = 2*np.pi*theta0/360
        self.parent = parent

    def __str__(self):
        return f"CelestialBody(name={self.name}, radius={self.radius}, color={self.color}, year={self.year})"
    
    def __repr__(self):
        return self.__str__()
    
    def position(self, t):
      if self.parent is None:  
        return (0.0, 0.0)
      theta = self.theta0 + 2*np.pi*(t/self.year)
      px, py = self.parent.position(t)
      x = self.radius * np.cos(theta) + px
      y = self.radius * np.sin(theta) + py
      return (x, y)

class SolarSystem:
    def __init__(self, star: CelestialBody):
        self.star = star
        self.center = star.name   # domyślnie gwiazda jako środek
        self.bodies = {star.name: star}
        self.orbits = {} 
    
    def set_center(self, name: str):
        if name not in self.bodies:
            raise ValueError(f"Body {name} not in the system!")
        self.center = name

    def add_planet(self, planet: CelestialBody):
        planet.parent = self.star
        self.bodies[planet.name] = planet
        self.orbits.setdefault(self.star.name, []).append(planet.name)

    def add_moon(self, moon: CelestialBody, planet_name: str):
        if planet_name not in self.bodies:
            raise ValueError(f"Planet {planet_name} not in the system!")
        moon.parent = self.bodies[planet_name]
        self.bodies[moon.name] = moon
        self.orbits.setdefault(planet_name, []).append(moon.name)

    def summary(self):
        print(f"The solar system centered on: {self.center}")
        for name, body in self.bodies.items():
            print(body)

    def positions(self, t, center_name: str | None = None, lens = None):
        
        pos_abs = {name: body.position(t) for name, body in self.bodies.items()}

        if center_name is None:
            return pos_abs

        if center_name not in pos_abs:
            raise ValueError(f"Center '{center_name}' not found in system")
        cx, cy = pos_abs[center_name]
        pos_frame = {name: (x - cx, y - cy) for name, (x, y) in pos_abs.items()}

        if lens is None:
          return pos_frame

        return {name: lens(np.array([x, y])) for name, (x, y) in pos_frame.items()}

class Lenses:
    def __init__(self, kind="radial_log", s=1.0, r0=1.0):
        self.kind = kind
        self.s = s
        self.r0 = r0

    def __call__(self, xy):
        v = np.asarray(xy, dtype=float)

        r = np.linalg.norm(v)
        if r == 0.0 and self.kind != "axis_symlog":
            return v.copy()

        if self.kind == "axis_symlog":
            return self.s * np.sign(v) * np.log(1 + np.abs(v) / self.r0)

        elif self.kind == "radial_log":
            rp = self.s * np.log(1 + r / self.r0)
            return v * (rp / r)

        elif self.kind == "linear":
            rp = self.s * r
            return v * (rp / r)

        else:
            raise ValueError(f"Unknown lens kind: {self.kind}")

sun = CelestialBody("Sun",
                    radius = None,
                    color = "yellow",
                    year = None,
                    parent = None)

mercury = CelestialBody("Mercury",
                        radius = 0.45,
                        color = "grey",
                        year = 88,
                        parent = sun)

venus = CelestialBody("Venus",
                      radius = 0.72,
                      color = "orange",
                      year = 225,
                      parent = sun)

earth = CelestialBody("Earth",
                      radius = 1.0,
                      color = "blue",
                      year = 365,
                      parent = sun)

moon = CelestialBody("Moon",
                     radius = 0.0026, 
                     color = "lightgray", 
                     year = 30, 
                     parent = earth)

mars = CelestialBody("Mars",
                     radius = 1.52,
                     color = "red",
                     year = 687,
                     parent = sun)

jupiter = CelestialBody("Jupiter",
                        radius = 5.21,
                        color = "brown",
                        year = 4333,
                        parent = sun)

saturn = CelestialBody("Saturn",
                       radius = 9.6,
                       color = "pink",
                       year = 10759,
                       parent = sun)

uranus = CelestialBody("Uranus",
                       radius = 19.2,
                       color = "cyan",
                       year = 30687)

neptune = CelestialBody("Neptune",
                        radius = 30.2,
                        color = "purple",
                        year = 60190)

system = SolarSystem(sun)
system.add_planet(mercury)
system.add_planet(venus)
system.add_planet(earth)
system.add_planet(mars)
system.add_planet(jupiter)
system.add_planet(saturn)
system.add_planet(uranus)
system.add_planet(neptune)
system.add_moon(moon, "Earth")

# =========================
# ANIMACJA → ZAPIS DO GIF (Pillow)
# =========================
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    from collections import deque

    # --- konfiguracja ---
    CENTER = "Sun"      # np. "Sun", "Earth", "Jupiter"
    FPS = 20                # klatki/sek
    DURATION_SEC = 120       # czas trwania filmu
    TRAIL_LEN = 400         # długość ogona śladu (liczba punktów)
    T_EARTH_SEC = 1.0      # ile sekund ma trwać „rok Ziemi” w animacji (tempo)

    # Soczewka (opcjonalnie)
    USE_LENS = True
    lens = Lenses(kind="radial_log", s=6.0, r0=1.0) if USE_LENS else None

    OUTFILE = "solar_system_Sun.gif"
    DPI = 70               # rozdzielczość renderu (niższe = mniejszy plik)

    # --- parametry czasu ---
    FRAMES = FPS * DURATION_SEC
    DAYS_PER_FRAME = system.bodies["Earth"].year / (FPS * T_EARTH_SEC)

    # --- lista ciał + próbkowanie do wyznaczenia granic osi (działa też z soczewką) ---
    names = list(system.bodies.keys())
    if CENTER not in names:
        raise SystemExit(f"Center '{CENTER}' not found. Available: {', '.join(names)}")

    YEARS_LIMITS = 3
    SAMPLES_LIMITS = 720
    t_days_limits = np.linspace(0.0, YEARS_LIMITS * 365.0, SAMPLES_LIMITS)
    all_x, all_y = [], []
    for td in t_days_limits:
        pos = system.positions(td, center_name=CENTER, lens=lens)
        for n in names:
            x, y = pos[n]
            all_x.append(x); all_y.append(y)
    all_x = np.array(all_x); all_y = np.array(all_y)
    mx = max(np.max(np.abs(all_x)), np.max(np.abs(all_y)))
    pad = 0.05 * mx if mx > 0 else 1.0

    # --- scena ---
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", "box")
    ax.set_xlim(-mx - pad, mx + pad)
    ax.set_ylim(-mx - pad, mx + pad)
    ax.axis("off")
    ax.grid(False)
    ax.set_title(f"Solar System (center={CENTER}"
                 f"{'' if lens is None else ', lens='+lens.kind})")

    # --- artyści: kropki + ślady (deque o maxlen=TRAIL_LEN) ---
    scatters = {}
    trail_lines = {}
    trails = {}

    for n in names:
        b = system.bodies[n]
        scatters[n] = ax.scatter([0.0], [0.0], s=(12 if n == "Moon" else 24), color=b.color, label=n)
        trails[n] = deque(maxlen=TRAIL_LEN)
        lw = 0.0 if n == CENTER else 0.8
        (trail_lines[n],) = ax.plot([], [], lw=lw, alpha=0.6, color=b.color)

    ax.legend(fontsize=8, ncol=2, loc="upper right")

    # --- funkcje animacji ---
    def init():
        for n in names:
            trails[n].clear()
            trail_lines[n].set_data([], [])
        pos0 = system.positions(0.0, center_name=CENTER, lens=lens)
        for n in names:
            x, y = pos0[n]
            scatters[n].set_offsets([x, y])
        return (*scatters.values(), *trail_lines.values())

    def update(frame_idx):
        t_days = frame_idx * DAYS_PER_FRAME
        pos = system.positions(t_days, center_name=CENTER, lens=lens)
        for n in names:
            x, y = pos[n]
            scatters[n].set_offsets([x, y])
            trails[n].append((x, y))
            if len(trails[n]) >= 2 and trail_lines[n].get_linewidth() > 0:
                xs, ys = zip(*trails[n])
                trail_lines[n].set_data(xs, ys)
            else:
                trail_lines[n].set_data([], [])
        return (*scatters.values(), *trail_lines.values())

    ani = FuncAnimation(
        fig, update,
        init_func=init,
        frames=FRAMES,
        interval=1000 / FPS,
        blit=True,
        cache_frame_data=False
    )

    # --- zapis do GIF (Pillow) ---
    writer = PillowWriter(fps=FPS)
    ani.save(OUTFILE, writer=writer, dpi=DPI)
    plt.close(fig)
    print(f"[OK] Saved animation to: {OUTFILE}")


