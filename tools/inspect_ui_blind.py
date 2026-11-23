import zipfile

with zipfile.ZipFile('D:/GG/Balatro.v1.0.1o/game/Balatro.exe', 'r') as z:
    with z.open('functions/UI_definitions.lua') as f:
        lines = f.read().decode('utf-8', errors='ignore').splitlines()
        for idx in range(1540, 1565):
            print(f"{idx+1}: {lines[idx]}")
