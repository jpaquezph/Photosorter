"""Script de un solo uso para generar icon.png / icon.ico a partir del logo fuente.

Ejecutar con: .venv/Scripts/python.exe src/photosorter/resources/_build_icon.py
No forma parte del paquete distribuido (no se importa desde la app).
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).parent
SOURCE = HERE / "source" / "Logo-Photosorter.png"
BG_COLOR = (7, 17, 31, 255)  # #07111F, mismo fondo que main_window.py (BG)
CANVAS_SIZE = 1024
CORNER_RADIUS = int(CANVAS_SIZE * 0.22)
MARK_PADDING_RATIO = 0.18  # margen entre la marca y el borde del icono


def build_icon() -> None:
    logo = Image.open(SOURCE).convert("RGBA")

    alpha = logo.split()[-1]
    bbox = alpha.getbbox()
    mark = logo.crop(bbox)

    target = CANVAS_SIZE * (1 - 2 * MARK_PADDING_RATIO)
    scale = min(target / mark.width, target / mark.height)
    new_size = (round(mark.width * scale), round(mark.height * scale))
    mark = mark.resize(new_size, Image.LANCZOS)

    canvas = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    mask = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, CANVAS_SIZE - 1, CANVAS_SIZE - 1), radius=CORNER_RADIUS, fill=255
    )
    bg_layer = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), BG_COLOR)
    canvas.paste(bg_layer, (0, 0), mask)

    offset = ((CANVAS_SIZE - new_size[0]) // 2, (CANVAS_SIZE - new_size[1]) // 2)
    canvas.paste(mark, offset, mark)

    png_path = HERE / "icon.png"
    canvas.save(png_path)

    ico_path = HERE / "icon.ico"
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    canvas.save(ico_path, format="ICO", sizes=sizes)

    print(f"OK: {png_path} y {ico_path} generados ({CANVAS_SIZE}x{CANVAS_SIZE} master).")


if __name__ == "__main__":
    build_icon()
