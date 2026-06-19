import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "pack", "mods")

def enforce_client_side():
    toml_files = glob.glob(os.path.join(MODS_DIR, "*.pw.toml"))
    updated_count = 0
    pinned_mods = []
    
    for file_path in toml_files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        has_side = False
        is_pinned = False
        mod_name = None
        filename = None
        
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("side ="):
                has_side = True
                new_lines.append('side = "client"\n')
            else:
                new_lines.append(line)
            
            if stripped.startswith("pin ="):
                parts = stripped.split("=")
                if len(parts) > 1 and parts[1].strip() == "true":
                    is_pinned = True
            elif stripped.startswith("name ="):
                parts = stripped.split("=")
                if len(parts) > 1:
                    mod_name = parts[1].strip().strip('"').strip("'")
            elif stripped.startswith("filename ="):
                parts = stripped.split("=")
                if len(parts) > 1:
                    filename = parts[1].strip().strip('"').strip("'")
                    
        if is_pinned:
            display_name = mod_name if mod_name else os.path.basename(file_path)
            version_str = f" ({filename})" if filename else ""
            pinned_mods.append(f"{display_name}{version_str}")

        if not has_side:
            inserted = False
            final_lines = []
            for line in new_lines:
                if line.strip().startswith("[") and not inserted:
                    final_lines.append('side = "client"\n\n')
                    inserted = True
                final_lines.append(line)
            if not inserted:
                final_lines.append('\nside = "client"\n')
            new_lines = final_lines
            
        if new_lines != lines:
            with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                f.writelines(new_lines)
            updated_count += 1
            print(f"Updated {os.path.basename(file_path)} -> side = \"client\"")
            
    print(f"Enforced client-side for {updated_count} files")
    
    if pinned_mods:
        print("\n" + "="*60)
        print("NOTICE: The following mods have frozen versions (pinned = true):")
        for pinned in sorted(pinned_mods):
            print(f"  - {pinned}")
        print("="*60 + "\n")

if __name__ == "__main__":
    enforce_client_side()
