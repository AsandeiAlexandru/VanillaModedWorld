import zipfile

with zipfile.ZipFile('D:/GG/Balatro.v1.0.1o/game/Balatro.exe', 'r') as z:
    with z.open('functions/common_events.lua') as f:
        lines = f.read().decode('utf-8', errors='ignore').splitlines()
        for idx in range(2320, 2370):
            if idx < len(lines):
                print(f"{idx+1}: {lines[idx]}")
