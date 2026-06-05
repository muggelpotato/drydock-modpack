import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "pack", "mods")

def enforce_client_side():
    toml_files = glob.glob(os.path.join(MODS_DIR, "*.pw.toml"))
    updated_count = 0
    
    for file_path in toml_files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        has_side = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("side ="):
                has_side = True
                new_lines.append('side = "client"\n')
            else:
                new_lines.append(line)
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
            
    print(f"Updated {updated_count} files")

if __name__ == "__main__":
    enforce_client_side()
