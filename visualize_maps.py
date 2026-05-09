import subprocess
import sys
import os

def run_script(folder, script_name):
    print(f"\n🚀 Running {script_name} in {folder}...")
    try:
        # Change CWD to the folder so it finds the csp_solver and saves images there
        subprocess.run([sys.executable, script_name], cwd=folder, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")

if __name__ == "__main__":
    print("🎨 Map Coloring Constraint Satisfaction Program")
    print("1. Australia Map Coloring (Real Geography)")
    print("2. Nairobi Map Coloring (Real Geography)")
    print("3. Both")
    
    choice = input("Select an option (1, 2, or 3): ").strip()
    
    if choice == '1':
        run_script("Australia", "australia_map.py")
    elif choice == '2':
        run_script("Nairobi", "nairobi_map.py")
    elif choice == '3':
        run_script("Australia", "australia_map.py")
        run_script("Nairobi", "nairobi_map.py")
    else:
        print("Invalid choice.")
