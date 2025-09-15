## FluxCat – Catalyst‑Poisoning Simulator for Fixed Bed Reactors
**FluxCat** is a lightweight, Kivy‑based Python application that lets you explore the transient behaviour of a fixed bed catalytic reactor under poisoning conditions.

The model is based on the mass balance from the DeVault partial differential equation and extended with axial dispersion and a Langmuir adsorption isotherm. It is a **demonstration tool** – not a production‑grade simulator – but it reproduces the key physics that appear in the literature (Bohart‑Adams, Wheeler‑Jonas, etc.) and allows you to see how the various parameters influence the breakthrough curve and the catalyst life.
Catalyst deactivation is a major bottleneck in many petrochemical processes. Experimental data are scarce and the literature is full of simplified models that ignore intraparticle diffusion or the effect of axial dispersion. FluxCat implements a more complete, yet still tractable, description that can be used for teaching, quick‑look studies, or as a starting point for more detailed modelling.

## Table of Contents
1. Section | Description
	1.1 Background
	1.2 Literature context and model motivation
	1.3 Features | What the app can do 
2. Installation
	2.1 How to get it running
3. Usage
	3.1 Running the GUI, adjusting parameters, interpreting results

## 1. Section | Description [Background]
    1.1 Background
    Catalyst deactivation in fixed bed reactors is a complex, multi‑step process. Classic works (Bohart‑Adams, Wheeler‑Jonas) treat it as a simple first‑order loss of activity, but real systems show:
    
    1.2 Literature context and model motivation
        **Intraparticle diffusion resistance** – especially for chemisorption of poisons such as sulfur or coke precursors.
        **Axial dispersion** – which skews breakthrough curves and alters the apparent deactivation rate.
        **Non‑linear sorption isotherms** – Langmuir. Appropriate for chemisorption at low concentrations.
        **Linear Driving Force** models are used in the sorbents performance prediction and results in a asymmetric breakthrough curve behavior. 
        FluxCat uses a different approach and extends it with a diffusion term that is linked to the Bodenstein number.
        The result is a set of partial differential equations that can be solved numerically to give the concentration profile under isothermal assumption.
        This reflects the catalyst activity as a function of time.
    1.3 Features | What the app can do
        **Interactive GUI** | Built with Kivy – cross‑platform, touch‑friendly.
        **Parameter toggle buttons** | Reaction temperature, fluid density, poison level, outlet level, bed geometry, diffusion coefficients, etc.
        Different units can be handled. The simulator directly calculates the estimated time to achieve the maximum outlet concentration of the poisoning compound.

## 2. Installation
    2.1 How to get it running
        **Prerequisites**
            python 3.8 – 3.13
            pip (Python package manager)

        1. Clone the repo:
        git clone https://github.com/mschindler779/FluxCat.git\
        cd FluxCat

        2. Create a virtual environment (optional but recommended)
        python -m venv /path/to/new/virtual/environment
        source /path/to/new/virtual/environment/bin/activate

        3. Install dependencies
        python -m pip install -r requirements.txt

## 3. Running the GUI
    python FluxCat.py
    The GUI window will appear. If you see a “Kivy not found” error, make sure the virtual environment is activated and that Kivy is installed correctly.

    Usage:
    **Launch** the app (`FluxCat.py`).
    **Set parameters** using the toggle buttons and numeric entry fields.
    **Reaction Temperature (°C)** – Isothermal assumption.
    **Fluid Density (kg/m³)** – Depends on feed pressure / temperature.
    **Poison Level (ppm)** – Initial concentration of the poison precursor.
    **Outlet Level (ppm)** – Threshold at which the catalyst is considered dead (e.g., 50 % of the original poison level.
    **Bed Geometry** – Diameter, length, bulk density, void fraction.
    **Bodenstein Number** – Controls axial dispersion.
    **Film Diffusion Coefficient** – Usually negligible for low‑pressure, low‑surface‑area systems.
    **Total Capacity** – Maximum uptake of the chemisorbed species.
    **Run** the simulation by pressing the **“Calculate”** button.
    **View** the estimated performance time until catalyst degrades.

## File Structure
├──FluxCat.py		# Main Kivy application ets up the GUI, handles user input, and calls the solver.
├──FVSorption.py	# Core model implementation (PDE solver)
├──content.kv		# Kivy layout file
├──network.png		# GUI’s background
├──solution.png		# Pre-computed general sample breakthrough curve
├──requirements.txt	# Python dependencies
├──README.md        # This file
└──LICENSE          # MIT license

**Kivy Documentation** – https://kivy.org

## License
MIT © 2025 Markus Schindler
