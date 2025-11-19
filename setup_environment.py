import subprocess
import sys
import os

def install_requirements():
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_directories():
    folders = [
        'config',
        'data',
        'assets',
        'assets/icons',
        'pages',
        'utils',
        'export/charts',
        'export/reports',
        'logs'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")
    
    init_files = ['config', 'utils', 'pages', 'data']
    for folder in init_files:
        with open(f"{folder}/__init__.py", 'w') as f:
            f.write('')
        print(f"Created __init__.py in: {folder}")
    
    print("Directory structure created successfully!")

if __name__ == "__main__":
    create_directories()
    install_requirements()