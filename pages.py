import os
import re

def final_clean():
    # Get all mp3 files
    files = [f for f in os.listdir('.') if f.endswith('.mp3')]
    files.sort()

    print("--- PASTE THIS INTO YOUR INDEX.HTML ---")
    
    for filename in files:
        # 1. Parse Data
        # Strips extension and splits by double space or dash
        display_name = filename.replace('.mp3', '')
        parts = re.split(r'\s{2,}-\s{2,}| - ', display_name)
        
        if len(parts) >= 2:
            artist = re.sub(r'^\d+\.\s*', '', parts[0]).strip()
            title = parts[1].strip()
        else:
            artist = "EDM"
            title = display_name

        # 2. Create Ultra-Safe Filename (no double dashes, all lowercase)
        clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', display_name).lower()
        clean_name = re.sub(r'\s+', '-', clean_name).strip('-') + ".mp3"
        
        # 3. Physical Rename
        try:
            os.rename(filename, clean_name)
            
            # 4. Generate HTML
            match = re.match(r'(\d+)', filename)
            track_num = match.group(1) if match else "00"
            
            # Clean up title/artist for the UI (remove those weird invisible spaces)
            ui_title = title.replace('\xa0', ' ').strip()
            ui_artist = artist.replace('\xa0', ' ').strip()

            print(f'<li><a class="track" href="{clean_name}" data-artist="{ui_artist}" data-title="{ui_title}"><span class="track-num">{track_num}</span> {ui_title}</a></li>')
        except Exception as e:
            continue

if __name__ == "__main__":
    final_clean()
