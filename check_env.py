import os
import sys
import importlib

def check_package(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def main():
    print("🔍 Checking RTD Environment...")
    
    packages = ["gradio", "pydantic", "toml", "aiohttp", "playwright"]
    all_ok = True
    
    print("\n📦 Packages:")
    for pkg in packages:
        status = "✅" if check_package(pkg) else "❌"
        print(f"  {status} {pkg}")
        if status == "❌":
            all_ok = False
            
    print("\n⚙️ Configuration:")
    config_path = "config/config.toml"
    if os.path.exists(config_path):
        print(f"  ✅ {config_path} exists")
    else:
        print(f"  ❌ {config_path} missing (Please run 'cp config/config.example.toml config/config.toml')")
        all_ok = False
        
    print("\n📂 Workspace:")
    workspace_path = "workspace"
    if os.path.exists(workspace_path):
        print(f"  ✅ {workspace_path} directory exists")
    else:
        os.makedirs(workspace_path)
        print(f"  ✅ {workspace_path} directory created")
        
    if all_ok:
        print("\n🚀 RTD is ready to go!")
    else:
        print("\n⚠️ Some issues were found. Please fix them before running RTD.")

if __name__ == "__main__":
    main()
