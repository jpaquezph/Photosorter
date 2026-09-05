_Nombre provisorio:_ PhotoSorter

**Objetivo**:

Crear una aplicación para windows escritorio que ayude a la organización de las fotografías, organizarlas en carpetas separadas según su orientación.

**Usuario Objetivo:**

- Usuario de windows
- Sabe crear carpetas, copiar y pegar archivos
- No sabe programación ni comandos CMD
- Quiere organizar rápidamente fotografías

**Principio fundamental:**

La tecnología aplicada no es relevante para el usuario. para el usuario deberá ser:

Descargar -> Instalar -> Abrir -> Seleccionar carpeta -> Procesar

**Necesidad:**

- Separar fotos verticales y horizontales para sus diferentes usos.
- Consumo bajo de recursos para que se ejecute en cualquier computadora
- Lectura de formatos raw, nef, jpg, tiff, png y similares.

**Requerimientos funcionales:**

- RF-01: Seleccionar carpeta:
    - El usuario debe poder seleccionar una carpeta mediante el explorador de windows
- RF-02: Analizar imágenes:
    - La aplicación debe detectar automáticamente las imágenes en la carpeta seleccionada.
- RF-03: Formatos
    - La aplicación deberá entender com imagen, inicialmente a los archivos .jpg, .tiff, .webp, .raw, .jpeg, .png
- PF-04: Determinar orientación:
    - La aplicación debe clasificar imágenes como:  
        

| Condición | Categoría |
| --- | --- |
| Alto > Ancho | Vertical |
| --- | --- |
| Alto < Ancho | Horizontal |
| --- | --- |
| Alto = Ancho | Cuadrada |
| --- | --- |

- RF-05: Carpeta de destino:
    - La aplicación debe crear automáticamente:
        - Carpeta seleccionada
            - Verticales/
            - Horizontales/
            - Cuadradas/
- RF-06: Que copie las imágenes:
    - La aplicación deberá copiar las imágenes en su nuevo destino y no ejecutar cambios en las fotos originales ni su ubicación.

**Requerimientos no funcionales:**

- RNF-01: Sistema operativo:
    - Windows 10/11 64bits
- RNF-02: No requerir python:
    - El usuario final no debe instalar python, ni ninguna dependencia. La aplicación será distribuida como .exe mediante instalador.
- RNF-03: Interfaz gráfica:
    - No habrá interacción mediante CMD
- RNF-04: Procesamiento en lotes:
    - Debe procesar grandes cantidades de fotografías.  
        

| Cantidad | Rendimiento |
| --- | --- |
| 100 | Rápido |
| --- | --- |
| 1000 | Aceptable |
| --- | --- |
| 10000 | Usable |
| --- | --- |

- RNF-05: Seguridad:
    - La aplicación no debe modificar los archivos originales ni su ubicación.
- RNF-06: Errores
    - Si una fotografía esta corrupta, no debe detener todo el proceso, sino mostrar cual es la foto que no se pudo detectar.