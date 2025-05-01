"""
Proving Time vs Cycle Count (is-prime program)

Dependencies:
    pip install matplotlib numpy
"""

import numpy as np
import matplotlib.pyplot as plt

# ── Raw benchmark data ────────────────────────────────────────────────────────

cycle_miden = np.array([
    533, 821, 821, 3701, 2616, 74261,
    423_029, 448_085, 483_221, 551_477, 1_286_741       
], dtype=float)

time_miden_sec = np.array([
     39,    29,    26,    55,   270,   992,
   4_941, 5_027, 5_938, 14_353, 60_420                          
], dtype=float) / 1000.0

cycle_sp1 = np.array([
        394,     408,     408,     518,   1_376,   3_213,
     16_534,  17_491,  18_833,  21_440,  49_523, 3_165_901
], dtype=float)

time_sp1_sec = np.array([
   5_524,  6_252,  5_993,  6_171,  6_196,  6_027,
   8_305,  8_431,  6_136,  8_431,  9_452, 63_827
], dtype=float) / 1000.0

# ── Power-law fits (log–log linear regression) ────────────────────────────────
log_c_miden = np.log10(cycle_miden)
log_t_miden = np.log10(time_miden_sec)
slope_miden, intercept_miden = np.polyfit(log_c_miden, log_t_miden, 1)

log_c_sp1 = np.log10(cycle_sp1)
log_t_sp1 = np.log10(time_sp1_sec)
slope_sp1, intercept_sp1 = np.polyfit(log_c_sp1, log_t_sp1, 1)

# Generate smooth lines for the fits
x_line = np.logspace(
    np.log10(min(cycle_miden.min(), cycle_sp1.min())),
    np.log10(max(cycle_miden.max(), cycle_sp1.max())),
    200
)
y_fit_miden = 10 ** (intercept_miden + slope_miden * np.log10(x_line))
y_fit_sp1   = 10 ** (intercept_sp1 + slope_sp1 * np.log10(x_line))

# ── Plot ──────────────────────────────────────────────────────────────────────
plt.figure(figsize=(8, 5))

plt.scatter(cycle_miden, time_miden_sec, label="Miden data", color="orange")
plt.scatter(cycle_sp1,   time_sp1_sec,   label="SP1 data",   color="blue")

plt.plot(x_line, y_fit_miden, "--", color="orange",
         label=f"Miden fit: time ≈ {10**intercept_miden:.2e} · cycles^{slope_miden:.2f}")
plt.plot(x_line, y_fit_sp1,   "--", color="blue",
         label=f"SP1 fit: time ≈ {10**intercept_sp1:.2e} · cycles^{slope_sp1:.2f}")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Cycle Count")
plt.ylabel("Proving Time (s)")
plt.title("Proving Time vs Cycle Count (is-prime program)")
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# Save
plt.savefig("time_vs_cycles_with_fit.png", dpi=300)
plt.show()