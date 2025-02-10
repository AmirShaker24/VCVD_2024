import argparse
import numpy as np
import matplotlib.pyplot as plt

# Constants (Extracted from Table 2 & 3 in the paper)
COEFFICIENTS = {
    "Fy": [-22.1, 1011, 1078, 1.82, 0.208, 0.000, -0.354, 0.707],
    "Fx": [-21.3, 1144, 49.6, 226, 0.069, -0.006, 0.056, 0.486]
}
C_VALUES = {"Fy": 1.30, "Fx": 1.65}


def magic_formula(Fz, slip_angle, coeffs, C_value):
    """Implements the Magic Formula for tire forces."""
    a1, a2, a3, a4, a5, a6, a7, a8 = coeffs
    
    D = a1 * Fz**2 + a2 * Fz
    B = (a3 * Fz**2 + a4 * Fz) / (C_value * D)
    E = a5 * Fz**2 + a7 * Fz + a8
    phi = (1 - E) * slip_angle + (E / B) * np.arctan(B * slip_angle)
    force = D * np.sin(C_value * np.arctan(B * phi))
    
    return force


def compute_tire_forces(Fz, slip_angles):
    """Computes side force and brake force based on Magic Formula."""
    side_forces = magic_formula(Fz, slip_angles, COEFFICIENTS["Fy"], C_VALUES["Fy"])
    brake_forces = magic_formula(Fz, slip_angles, COEFFICIENTS["Fx"], C_VALUES["Fx"])
    return side_forces, brake_forces


def plot_forces(slip_angles, side_forces, brake_forces):
    """Plots the side force and brake force over longitudinal slip."""
    plt.figure()
    plt.plot(slip_angles, side_forces, label="Side Force (Fy)", linestyle='-', color='b')
    plt.plot(slip_angles, brake_forces, label="Brake Force (Fx)", linestyle='--', color='r')
    plt.xlabel("Slip Angle (Degrees)")
    plt.ylabel("Force (N)")
    plt.title("Side & Brake Force vs. Slip Angle")
    plt.legend()
    plt.grid()
    plt.savefig("tire_forces_plot.png")
    plt.show()


def main():
    """Main function to parse arguments and run calculations."""
    parser = argparse.ArgumentParser(description="Compute and plot tire forces based on slip angle.")
    parser.add_argument("--slip", type=float, required=True, help="Slip angle in degrees.")
    parser.add_argument("--weight", type=float, required=True, help="Vehicle weight in kg.")
    parser.add_argument("--mu", type=float, required=True, help="Coefficient of friction.")
    
    args = parser.parse_args()
    
    Fz = (args.weight * 9.81) / 4  # Assume equal distribution over 4 wheels
    slip_angles = np.linspace(0, args.slip, 100)
    side_forces, brake_forces = compute_tire_forces(Fz, slip_angles)
    plot_forces(slip_angles, side_forces, brake_forces)
    
    print(f"Computed tire forces for slip angle {args.slip} degrees and weight {args.weight} kg:")
    print(f"Max Side Force: {max(side_forces):.2f} N")
    print(f"Max Brake Force: {max(brake_forces):.2f} N")


if __name__ == "__main__":
    main()
