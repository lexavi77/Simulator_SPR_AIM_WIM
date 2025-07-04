from modes_aim import run_mode_1, run_mode_2, run_mode_3
from plot_sensitive_structure import plot_figures_of_merit_comparative


def main():
    print("Select simulation mode:")
    print("1 - Analyze a specific material")
    print("2 - Plot 22 reflectance curves per metal (final report requirement)")
    print("3 - Plot sensitive structure (TOPAS + d=55nm) for 3 metals (6 analytes)")

    mode = input("Mode (1, 2, 3 ): ").strip()

    if mode == "1":
        run_mode_1()
    elif mode == "2":
        run_mode_2()
    elif mode == "3":
        run_mode_3()
    else:
        print("Invalid option. Exiting program.")

if __name__ == "__main__":
    main()
