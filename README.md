# Simulation of solar system
#### author: Jędrzej Wydra

## Short summary
Created a Python-based simulation with Matplotlib animations to visualize planetary orbits as parametric curves, using mathematical modeling and local coordinate transformations to display trajectories from different reference points.

## Technical summary
Generated synthetic orbital paths with trigonometric parametric equations and computed relative motion by subtracting coordinate sets to change the frame of reference (e.g., Earth-, Mars-centered). Implemented animations via Matplotlib’s FuncAnimation to sequentially render multi-body trajectories. All orbital computations were derived analytically using mathematical modeling before implementation, demonstrating how simple parametric models can replicate complex dynamical behavior.

## History
I took on this project when I decided it was time to learn Python. I figured, why not challenge a bit of conventional wisdom? After all, it’s not just that Copernicus was right and all the planets orbit the Sun in ellipses — it’s only true when the Sun is your point of reference. But what if we chose a different planet as the reference point? Without worrying too much about scale, I set out to create an animation that shows the paths various celestial bodies would take if you changed the reference point. One scenario even closely resembles Copernicus’s heliocentric model, just for the sake of a fun comparison.
