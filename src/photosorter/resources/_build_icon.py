"""Script de un solo uso para generar logo.png / icon.png / icon.ico / icon.icns a partir del logo fuente.

Ejecutar con: .venv/Scripts/python.exe src/photosorter/resources/_build_icon.py (Windows)
o .venv/bin/python src/photosorter/resources/_build_icon.py (macOS/Linux).
No forma parte del paquete distribuido (no se importa desde la app).
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

HERE = Path(__file__).parent
SOURCE = HERE / "source" / "Logo-Photosorter.png"
BG_COLOR = (7, 17, 31, 255)  # #07111F, mismo fondo que main_window.py (BG)
MARK_COLOR = (242, 245, 248)  # #F2F5F8, mismo texto primario que main_window.py
CANVAS_SIZE = 1024
CORNER_RADIUS = int(CANVAS_SIZE * 0.22)
MARK_PADDING_RATIO = 0.12  # margen entre la marca y el borde del icono
# Saturacion (0-255) a partir de la cual un pixel se considera "de color"
# (el broche) y conserva su tono original en vez de aclararse.
SATURATION_FULL = 110


def build_light_mark() -> Image.Image:
    """Marca recortada, con el trazo negro pasado a claro.

    El logo fuente es negro sobre transparente: sobre la paleta oscura de la
    app no se veria. Se aclara solo el trazo sin color (letras y marco); el
    broche conserva su tono.
    """
    logo = Image.open(SOURCE).convert("RGBA")
    alpha = logo.getchannel("A")
    logo = logo.crop(alpha.getbbox())
    alpha = logo.getchannel("A")

    red, green, blue = logo.convert("RGB").split()
    highest = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    lowest = ImageChops.darker(ImageChops.darker(red, green), blue)
    saturation = ImageChops.subtract(highest, lowest)
    keep_color = saturation.point(lambda value: min(255, value * 255 // SATURATION_FULL))

    light = Image.new("RGB", logo.size, MARK_COLOR)
    mark = Image.composite(logo.convert("RGB"), light, keep_color).convert("RGBA")
    mark.putalpha(alpha)
    return mark


def build_icon() -> None:
    mark = build_light_mark()

    # Version suelta (sin fondo) para usar dentro de la app: barra de titulo
    # y marca de agua de la galeria vacia.
    logo_path = HERE / "logo.png"
    mark.save(logo_path)

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

    # Icono nativo de macOS (bundle .app, ver packaging/build_mac.sh). Pillow
    # escribe el .icns completo (todas las resoluciones) sin depender de
    # iconutil.
    icns_path = HERE / "icon.icns"
    canvas.save(icns_path, format="ICNS")

    print(
        f"OK: {logo_path}, {png_path}, {ico_path} y {icns_path} generados "
        f"({CANVAS_SIZE}x{CANVAS_SIZE} master)."
    )


if __name__ == "__main__":
    build_icon()
