import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from io import BytesIO
import base64

st.set_page_config(page_title="Predator-Prey Simulator", layout="wide")

# -----------------------------
# Utility functions
# -----------------------------
def rk4_step(f, t, y, dt, params):
    """Single RK4 step for system y' = f(t, y, params)"""
    k1 = f(t, y, params)
    k2 = f(t + dt/2, y + dt*k1/2, params)
    k3 = f(t + dt/2, y + dt*k2/2, params)
    k4 = f(t + dt, y + dt*k3, params)
    return y + dt*(k1 + 2*k2 + 2*k3 + k4)/6

def lotka_volterra_rhs(t, y, params):
    # y = [prey, predator]
    a = params['prey_birth']      # prey birth rate
    b = params['predation_rate']  # predation rate coefficient
    c = params['predator_eff']    # predator efficiency converting eaten prey to predator births
    d = params['predator_death']  # predator death rate
    prey, pred = y
    dprey = a * prey - b * prey * pred
    dpred = c * b * prey * pred - d * pred
    return np.array([dprey, dpred])

def simulate_lv(prey0, pred0, params, t_max=50.0, dt=0.01):
    times = np.arange(0, t_max + dt, dt)
    y = np.zeros((len(times), 2))
    y[0] = np.array([prey0, pred0], dtype=float)
    for i in range(1, len(times)):
        y[i] = rk4_step(lotka_volterra_rhs, times[i-1], y[i-1], dt, params)
        # clamp to non-negative
        y[i] = np.maximum(y[i], 0.0)
    df = pd.DataFrame({
        'time': times,
        'prey': y[:,0],
        'predator': y[:,1]
    })
    return df

# -----------------------------
# Spatial cellular automaton model
# -----------------------------
def init_grid(shape, prey_frac, pred_frac, seed=None):
    rng = np.random.default_rng(seed)
    grid = np.zeros(shape, dtype=int)  # 0 empty, 1 prey, 2 predator
    flat = rng.random(shape[0]*shape[1])
    flat_idx = np.arange(flat.size)
    # place prey
    prey_count = int(prey_frac * flat.size)
    pred_count = int(pred_frac * flat.size)
    rng.shuffle(flat_idx)
    prey_idx = flat_idx[:prey_count]
    pred_idx = flat_idx[prey_count:prey_count+pred_count]
    grid.flat[prey_idx] = 1
    grid.flat[pred_idx] = 2
    return grid

def step_grid(grid, p_prey_birth, p_pred_move, p_pred_eat, p_prey_move, p_pred_die, rng):
    rows, cols = grid.shape
    new_grid = grid.copy()
    # random visit order to avoid biases
    order = [(i, j) for i in range(rows) for j in range(cols)]
    rng.shuffle(order)
    for (i, j) in order:
        cell = grid[i, j]
        if cell == 1:  # prey
            # reproduction
            if rng.random() < p_prey_birth:
                # choose random neighbor to place offspring if empty
                neigh = neighbors_coords(i, j, rows, cols)
                empties = [(x, y) for (x, y) in neigh if new_grid[x, y] == 0]
                if empties:
                    x, y = rng.choice(empties)
                    new_grid[x, y] = 1
            # optional prey movement
            if p_prey_move > 0 and rng.random() < p_prey_move:
                neigh = neighbors_coords(i, j, rows, cols)
                empties = [(x, y) for (x, y) in neigh if new_grid[x, y] == 0]
                if empties:
                    x, y = rng.choice(empties)
                    new_grid[x, y] = 1
                    new_grid[i, j] = 0
        elif cell == 2:  # predator
            # try to eat neighbor prey first
            neigh = neighbors_coords(i, j, rows, cols)
            prey_neigh = [(x, y) for (x, y) in neigh if new_grid[x, y] == 1]
            if prey_neigh and rng.random() < p_pred_eat:
                x, y = rng.choice(prey_neigh)
                # predator moves into prey cell (eats it)
                new_grid[x, y] = 2
                new_grid[i, j] = 0
                # possible reproduction on eat: handled as probability of spawning in place
                if rng.random() < 0.5:  # small chance of reproduction when eating
                    # leave current cell as predator or spawn predator in adjacent empty cell
                    empties = [(a,b) for (a,b) in neighbors_coords(x, y, rows, cols) if new_grid[a,b]==0]
                    if empties:
                        a,b = rng.choice(empties)
                        new_grid[a,b] = 2
            else:
                # move randomly
                if rng.random() < p_pred_move:
                    empties = [(x, y) for (x, y) in neigh if new_grid[x, y] == 0]
                    if empties:
                        x, y = rng.choice(empties)
                        new_grid[x, y] = 2
                        new_grid[i, j] = 0
                # die with some probability
                if rng.random() < p_pred_die:
                    new_grid[i, j] = 0
    return new_grid

def neighbors_coords(i, j, rows, cols):
    # 8-neighborhood with wrap-around (toroidal)
    coords = []
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            coords.append(((i + di) % rows, (j + dj) % cols))
    return coords

def simulate_grid(shape, steps, init_prey_frac, init_pred_frac, params, seed=None, snapshot_interval=10):
    rng = np.random.default_rng(seed)
    grid = init_grid(shape, init_prey_frac, init_pred_frac, seed)
    rows, cols = shape
    history_counts = []
    snapshots = []
    for t in range(steps):
        counts = (grid == 1).sum(), (grid == 2).sum()
        history_counts.append({'time': t, 'prey': counts[0], 'predator': counts[1]})
        if t % snapshot_interval == 0:
            snapshots.append((t, grid.copy()))
        grid = step_grid(
            grid,
            p_prey_birth = params['p_prey_birth'],
            p_pred_move = params['p_pred_move'],
            p_pred_eat  = params['p_pred_eat'],
            p_prey_move = params['p_prey_move'],
            p_pred_die  = params['p_pred_die'],
            rng = rng
        )
    df_counts = pd.DataFrame(history_counts)
    return df_counts, snapshots

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🦌 Predator–Prey Simulator — Lotka–Volterra & Spatial")
st.markdown(
    "Interactive predator–prey models: a classic Lotka–Volterra ODE and a simple "
    "spatial cellular automaton. Use sliders to explore dynamics and export results."
)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Lotka–Volterra (ODE) settings")
    lv_prey0 = st.number_input("Initial prey population", value=40.0, min_value=0.0, step=1.0)
    lv_pred0 = st.number_input("Initial predator population", value=9.0, min_value=0.0, step=1.0)
    lv_prey_birth = st.slider("Prey birth rate (a)", 0.0, 2.0, 1.0, 0.01)
    lv_predation_rate = st.slider("Predation rate (b)", 0.0, 1.0, 0.02, 0.001)
    lv_predator_eff = st.slider("Predator efficiency (c)", 0.0, 2.0, 0.5, 0.01)
    lv_predator_death = st.slider("Predator death (d)", 0.0, 2.0, 0.5, 0.01)
    lv_tmax = st.number_input("Simulation time (t_max)", value=200.0, min_value=1.0, step=1.0)
    lv_dt = st.number_input("Time step (dt)", value=0.05, min_value=0.001, step=0.01, format="%.3f")
    if st.button("Run Lotka–Volterra simulation"):
        lv_params = {
            'prey_birth': lv_prey_birth,
            'predation_rate': lv_predation_rate,
            'predator_eff': lv_predator_eff,
            'predator_death': lv_predator_death
        }
        with st.spinner("Simulating ODE..."):
            df_lv = simulate_lv(lv_prey0, lv_pred0, lv_params, t_max=lv_tmax, dt=lv_dt)
        st.success("Simulation complete — see plots below.")
        # Time series plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df_lv['time'], df_lv['prey'], label='Prey')
        ax.plot(df_lv['time'], df_lv['predator'], label='Predator')
        ax.set_xlabel("Time")
        ax.set_ylabel("Population")
        ax.legend()
        st.pyplot(fig)
        # Phase space
        fig2, ax2 = plt.subplots(figsize=(4,4))
        ax2.plot(df_lv['prey'], df_lv['predator'])
        ax2.set_xlabel("Prey")
        ax2.set_ylabel("Predator")
        ax2.set_title("Phase space")
        st.pyplot(fig2)
        # Data download
        csv = df_lv.to_csv(index=False).encode('utf-8')
        st.download_button("Download ODE results (CSV)", csv, "lv_simulation.csv", "text/csv")

with col2:
    st.header("Spatial grid settings")
    grid_size = st.slider("Grid size (N×N)", 20, 200, 80, step=10)
    init_prey_frac = st.slider("Initial prey fraction", 0.0, 0.5, 0.2, 0.01)
    init_pred_frac = st.slider("Initial predator fraction", 0.0, 0.3, 0.05, 0.01)
    steps = st.number_input("Simulation steps", value=500, min_value=1, step=1)
    snapshot_interval = st.number_input("Snapshot interval (steps)", value=25, min_value=1, step=1)
    st.write("— Predator behavior")
    p_pred_move = st.slider("Predator move probability", 0.0, 1.0, 0.45, 0.01)
    p_pred_eat  = st.slider("Predator eat success prob", 0.0, 1.0, 0.6, 0.01)
    p_pred_die  = st.slider("Predator natural death prob per step", 0.0, 0.2, 0.02, 0.001)
    st.write("— Prey behavior")
    p_prey_birth = st.slider("Prey birth probability per step", 0.0, 0.4, 0.05, 0.01)
    p_prey_move  = st.slider("Prey move probability", 0.0, 1.0, 0.2, 0.01)
    seed = st.number_input("Random seed (0 for random)", value=0, step=1)
    if st.button("Run spatial simulation"):
        params = {
            'p_prey_birth': p_prey_birth,
            'p_pred_move': p_pred_move,
            'p_pred_eat': p_pred_eat,
            'p_prey_move': p_prey_move,
            'p_pred_die': p_pred_die
        }
        seed_val = None if int(seed) == 0 else int(seed)
        with st.spinner("Running spatial CA..."):
            df_grid, snapshots = simulate_grid(
                shape=(grid_size, grid_size),
                steps=int(steps),
                init_prey_frac=init_prey_frac,
                init_pred_frac=init_pred_frac,
                params=params,
                seed=seed_val,
                snapshot_interval=int(snapshot_interval)
            )
        st.success("Spatial simulation complete.")
        # plot time series counts
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(df_grid['time'], df_grid['prey'], label='Prey count')
        ax.plot(df_grid['time'], df_grid['predator'], label='Predator count')
        ax.set_xlabel("Step")
        ax.set_ylabel("Count")
        ax.legend()
        st.pyplot(fig)
        # show snapshots
        st.subheader("Grid snapshots")
        cols = st.columns(3)
        for idx, (t, grid_snapshot) in enumerate(snapshots[:3]):
            fig = plt.figure(figsize=(3,3))
            # create RGB-like color mapping: empty=white, prey=green, predator=red
            color_grid = np.zeros((grid_snapshot.shape[0], grid_snapshot.shape[1], 3), dtype=float)
            color_grid[grid_snapshot==0] = [1,1,1]
            color_grid[grid_snapshot==1] = [0.2,0.9,0.2]
            color_grid[grid_snapshot==2] = [0.9,0.2,0.2]
            plt.imshow(color_grid, interpolation='nearest')
            plt.title(f"t = {t}")
            plt.axis('off')
            cols[idx % 3].pyplot(fig)
        # allow stepping through snapshots interactive
        st.subheader("Step through snapshots")
        snap_times = [t for (t, _) in snapshots]
        if snap_times:
            sel = st.selectbox("Choose snapshot time", snap_times)
            grid_sel = [g for (t,g) in snapshots if t == sel][0]
            fig = plt.figure(figsize=(5,5))
            cmap = cm.get_cmap('viridis')
            color_grid = np.zeros((grid_sel.shape[0], grid_sel.shape[1], 3), dtype=float)
            color_grid[grid_sel==0] = [1,1,1]
            color_grid[grid_sel==1] = [0.2,0.9,0.2]
            color_grid[grid_sel==2] = [0.9,0.2,0.2]
            plt.imshow(color_grid, interpolation='nearest')
            plt.title(f"Snapshot at t={sel}")
            plt.axis('off')
            st.pyplot(fig)
        else:
            st.info("No snapshots available for these settings.")
        csv = df_grid.to_csv(index=False).encode('utf-8')
        st.download_button("Download spatial counts (CSV)", csv, "spatial_counts.csv", "text/csv")

st.markdown("---")
st.header("How to use / interpretation notes")
st.markdown(
    """
    - **Lotka–Volterra (ODE):** The classic non-spatial predator–prey model. It captures oscillatory dynamics (cycles)
      in populations but ignores space and stochasticity.
    - **Spatial grid CA:** Introduces local interactions, stochastic events, and spatial patterns (patches, waves).
      The parameters are intentionally simple; change them to see emergent behaviours.
    - **Tips:** Increase grid size and steps for richer spatial patterns (longer runtime). Use the RNG seed to reproduce runs.
    - **Export:** Download CSV data to analyze in Python, Excel, or other tools.
    """
)

st.markdown("### Implementation notes")
st.markdown(
    """
    - RK4 integrator used for numerical stability in ODE simulation.
    - Spatial model uses toroidal wrap-around neighbors (to avoid boundary artifacts).
    - This is a pedagogical tool: you can extend it with movement heuristics, energy budgets,
      mating rules, diffusion of resources, and visualization improvements (animations).
    """
)

st.markdown("---")
st.caption("If you want, I can add: (a) real-time animation, (b) resource diffusion (grass), (c) agent energy budgets, or (d) data export to PNG/Excel. Tell me which and I'll expand the app.")
