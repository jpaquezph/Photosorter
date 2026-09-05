# **PhotoSorter**

## **Documento de Requisitos — V1.0**

**Estado:** Draft aprobado para diseño técnico  
**Versión del documento:** 0.1  
**Producto:** PhotoSorter  
**Plataforma objetivo:** Windows 10/11 — 64 bits  
**Tipo:** Aplicación de escritorio  
**Usuario objetivo:** Fotógrafos y usuarios que trabajan con grandes volúmenes de fotografías

# **1\. Propósito del producto**

PhotoSorter es una aplicación de escritorio destinada a fotógrafos que necesitan organizar rápidamente grandes cantidades de fotografías.

La primera versión permitirá seleccionar una carpeta y clasificar automáticamente las fotografías según su orientación:

- Vertical
- Horizontal
- Cuadrada

La aplicación deberá funcionar como un producto de escritorio convencional, sin que el usuario necesite conocimientos de programación, Python, CMD o instalación de dependencias.

El producto se diseñará desde el inicio para permitir futuras funcionalidades de organización y procesamiento de fotografías sin requerir una reestructuración de la arquitectura.

# **2\. Objetivo de la V1**

La V1 debe permitir al usuario:

1.  Seleccionar una carpeta.
2.  Elegir si desea procesar únicamente esa carpeta o también sus subcarpetas.
3.  Detectar fotografías compatibles.
4.  Leer correctamente su orientación, incluyendo información EXIF.
5.  Clasificar cada fotografía como:
    - Vertical
    - Horizontal
    - Cuadrada
6.  Crear las carpetas de destino necesarias.
7.  Copiar las fotografías a sus respectivas carpetas.
8.  Mantener intactos los archivos originales.
9.  Mostrar el progreso del procesamiento.
10. Informar al usuario el resultado final.
11. Informar errores individuales sin detener innecesariamente todo el proceso.

# **3\. Principios del producto**

## **3.1. Seguridad de los originales**

La V1 será exclusivamente una herramienta de **copia**.

La aplicación no deberá modificar, mover, eliminar ni sobrescribir los archivos originales durante una operación normal sin una decisión explícita del usuario.

Cuando un conflicto de nombre sea detectado, la aplicación deberá permitir al usuario seleccionar una acción y, opcionalmente, aplicar dicha acción a todos los conflictos restantes del procesamiento.

Esto constituye una decisión de diseño deliberada.

En versiones futuras podrá incorporarse una operación de "Mover" o "Cortar", pero deberá implementarse como una nueva capacidad del sistema sin modificar el comportamiento existente de la V1.

## **3.2. Orientación fotográfica real**

La clasificación no deberá basarse exclusivamente en las dimensiones físicas almacenadas del archivo.

La aplicación deberá contemplar la información de orientación contenida en EXIF cuando corresponda.

Ejemplo:

Una fotografía almacenada físicamente como:

6000 × 4000

puede tener una orientación EXIF que indique que debe visualizarse rotada.

La aplicación deberá clasificarla según su orientación visual final.

## **3.3. Diseñada para fotógrafos**

Aunque la V1 sea pequeña, el producto no estará diseñado como un simple script genérico para archivos.

El diseño deberá contemplar desde el inicio formatos y flujos habituales en fotografía digital, incluyendo fotografías RAW.

## **3.4. Arquitectura extensible**

Las funcionalidades deberán estar separadas por responsabilidades.

La incorporación futura de capacidades como:

- mover fotografías;
- nuevos formatos;
- diferentes nomenclaturas;
- nuevas estructuras de carpetas;
- filtrado;
- lectura de metadatos;
- clasificación por fecha;
- clasificación por cámara;
- detección de duplicados;

no debería requerir reescribir los componentes principales de la aplicación.

# **4\. Alcance de la V1**

## **Incluido**

### **Entrada**

- Selección de una carpeta mediante interfaz gráfica.
- Procesamiento de carpeta única.
- Procesamiento recursivo de subcarpetas.
- Detección de archivos de imagen compatibles.
- Lectura de dimensiones.
- Lectura de orientación EXIF.
- Lectura de fotografías RAW compatibles.

### **Clasificación**

- Vertical.
- Horizontal.
- Cuadrada.

### **Salida**

Creación automática de:

Verticales/

Horizontales/

Cuadradas/

y copia de los archivos correspondientes.

### **Interfaz**

- Selección de carpeta.
- Selector de procesamiento recursivo.
- Inicio del proceso.
- Progreso.
- Estado actual.
- Resumen final.
- Reporte de errores.
- Acceso a la carpeta de resultados.

# **5\. Fuera del alcance de la V1**

Las siguientes funcionalidades quedan explícitamente fuera de la primera versión:

- Mover/cortar archivos.
- Eliminar originales.
- Renombrado avanzado.
- Detección de fotografías duplicadas.
- Clasificación por fecha.
- Clasificación por cámara.
- Clasificación por lente.
- Clasificación por ISO.
- Clasificación por ubicación GPS.
- Edición fotográfica.
- Conversión RAW → JPEG.
- Procesamiento de imágenes.
- Detección mediante inteligencia artificial.
- Sincronización en la nube.
- Base de datos de fotografías.
- Aplicación móvil.
- Versión web.

Estas funcionalidades podrán formar parte de futuras versiones.

# **6\. Formatos de archivo**

## **6.1. Formatos raster**

La V1 deberá contemplar formatos fotográficos habituales, incluyendo como mínimo:

- JPG
- JPEG
- PNG
- TIFF
- WEBP

La arquitectura deberá permitir agregar nuevos formatos sin modificar el componente de clasificación.

# **6.2. RAW**

El soporte RAW es requisito de la V1.

La aplicación deberá diseñarse alrededor de un componente independiente de lectura de imágenes/formatos RAW.

La implementación deberá permitir incorporar o ampliar formatos RAW sin modificar el clasificador.

Los formatos RAW soportados inicialmente deberán definirse durante la fase de implementación y pruebas en función del motor RAW utilizado.

Como mínimo, se deberá evaluar soporte para formatos utilizados por las principales marcas, incluyendo:

- Nikon — NEF
- Canon — CR2 / CR3
- Sony — ARW
- Adobe — DNG
- Fujifilm — RAF
- Olympus/OM System — ORF
- Panasonic — RW2

El listado definitivo de formatos soportados deberá documentarse en la versión correspondiente del producto.

# **7\. Selección de carpetas**

El usuario deberá poder seleccionar una carpeta mediante el explorador de archivos de Windows.

Ejemplo:

C:\\Fotos\\Sesión Juan

La aplicación deberá validar que:

- la carpeta existe;
- el usuario tiene permisos de lectura;
- la carpeta es accesible.

Si la carpeta no puede procesarse, deberá mostrar un mensaje comprensible para un usuario no técnico.

# **8\. Procesamiento de subcarpetas**

El usuario deberá poder seleccionar entre:

### **Opción A — Solo carpeta seleccionada**

Se procesarán únicamente los archivos ubicados directamente dentro de la carpeta seleccionada.

### **Opción B — Incluir subcarpetas**

Se recorrerán recursivamente las subcarpetas.

Ejemplo:

Sesión/

├── IMG_001.jpg

├── IMG_002.jpg

│

├── Cámara 1/

│ ├── IMG_003.jpg

│ └── IMG_004.jpg

│

└── Cámara 2/

├── IMG_005.jpg

└── IMG_006.jpg

La aplicación deberá poder procesar todo el árbol cuando esta opción esté activada.

# **9\. Estructura de salida**

Por defecto, la aplicación deberá crear:

Carpeta seleccionada/

├── Verticales/

├── Horizontales/

└── Cuadradas/

Los archivos originales permanecerán en su ubicación original.

Ejemplo:

Fotos/

├── DSC_0001.NEF

├── DSC_0002.JPG

├── DSC_0003.CR3

│

├── Verticales/

│ ├── DSC_0001.NEF

│ └── DSC_0003.CR3

│

├── Horizontales/

│ └── DSC_0002.JPG

│

└── Cuadradas/

# **10\. Conflictos de archivos**

La aplicación deberá contemplar el caso en que el archivo de destino ya exista.

Ejemplo:

Verticales/

└── DSC_0001.JPG

y posteriormente se intente copiar otro archivo con el mismo nombre.

La V1 no deberá sobrescribir silenciosamente un archivo existente.

La estrategia concreta deberá definirse durante el diseño técnico.

Opciones a evaluar:

- agregar sufijo automático;
- conservar el archivo existente y omitir el nuevo;
- solicitar decisión al usuario;
- generar un nombre alternativo seguro.

La solución elegida deberá evitar pérdida de información.

# **11\. Archivos inválidos o corruptos**

Si un archivo posee una extensión compatible pero no puede ser leído:

La aplicación deberá:

1.  registrar el error;
2.  informar que el archivo no pudo procesarse;
3.  continuar con los demás archivos cuando sea posible.

Ejemplo de resultado:

Archivos encontrados: 1.250

Procesados: 1.247

Errores: 3

El error de un archivo individual no deberá provocar automáticamente la cancelación de toda la operación.

# **12\. Interfaz de usuario**

La interfaz deberá priorizar simplicidad.

El usuario no deberá necesitar conocer conceptos técnicos como:

- Python;
- CMD;
- terminal;
- dependencias;
- librerías;
- rutas de ejecución.

La ventana principal deberá contener como mínimo:

PHOTO SORTER

Carpeta:

\[ C:\\Fotos\\Sesión \] \[Examinar\]

\[ \] Incluir subcarpetas

\[ SEPARAR FOTOS \]

\--------------------------------------------

Estado:

Procesando DSC_1234.NEF

Progreso:

████████████████░░░░ 78%

Encontradas: 1.250

Procesadas: 975

Errores: 2

Al finalizar:

PROCESO FINALIZADO

Total: 1.250

Verticales: 530

Horizontales: 690

Cuadradas: 28

Errores: 2

\[ Abrir carpeta de resultados \]

# **13\. Cancelación del proceso**

La aplicación deberá contemplar la posibilidad de cancelar un procesamiento en curso.

La cancelación deberá ser segura.

Si el usuario cancela:

- no deberán iniciarse nuevas operaciones;
- los archivos ya copiados permanecerán en destino;
- los originales no deberán modificarse;
- deberá mostrar claramente que el proceso fue cancelado.

Ejemplo:

Proceso cancelado.

Procesadas: 643 / 1.250

Copiadas: 643

Errores: 1

# **14\. Progreso**

El usuario deberá poder conocer el estado del procesamiento.

Como mínimo:

- cantidad total detectada;
- cantidad procesada;
- cantidad restante;
- archivo actualmente procesado;
- porcentaje aproximado.

Para grandes cantidades de fotografías, la interfaz no deberá quedar bloqueada durante el procesamiento.

# **15\. Resultado del procesamiento**

Al finalizar, la aplicación deberá proporcionar un resumen.

Ejemplo:

PROCESAMIENTO COMPLETADO

1.250 fotografías analizadas

Verticales 530

Horizontales 690

Cuadradas 28

Errores 2

Archivos copiados: 1.248

\[ Abrir resultados \]

El usuario deberá poder identificar fácilmente si el proceso terminó correctamente o con errores.

# **16\. Criterios de aceptación**

La V1 será considerada funcional cuando pueda cumplir satisfactoriamente los siguientes casos.

### **CA-01 — Fotografía horizontal**

Dado un JPG horizontal:

6000 × 4000

deberá terminar en:

Horizontales/

### **CA-02 — Fotografía vertical**

Dado un JPG vertical:

4000 × 6000

deberá terminar en:

Verticales/

### **CA-03 — Fotografía cuadrada**

Dado un archivo:

4000 × 4000

deberá terminar en:

Cuadradas/

### **CA-04 — Orientación EXIF**

Una fotografía cuya orientación visual dependa del campo EXIF deberá clasificarse según su orientación visual y no únicamente según las dimensiones físicas almacenadas.

### **CA-05 — RAW**

La aplicación deberá poder procesar correctamente los formatos RAW definidos como soportados en la versión.

### **CA-06 — Subcarpetas**

Con "Incluir subcarpetas" desactivado:

Fotos/

├── IMG1.jpg

└── Evento/

└── IMG2.jpg

solo deberá procesarse IMG1.jpg.

Con la opción activada deberán procesarse ambos.

### **CA-07 — Originales**

Después del procesamiento, los archivos originales deberán permanecer intactos.

### **CA-08 — Error individual**

Si una fotografía está corrupta, las demás fotografías válidas deberán continuar procesándose.

### **CA-09 — Carpetas existentes**

Si Verticales, Horizontales o Cuadradas ya existen, la aplicación no deberá fallar ni eliminar su contenido.

### **CA-10 — Archivo duplicado**

Si el destino ya contiene un archivo con el mismo nombre, la aplicación no deberá sobrescribirlo silenciosamente.

### **CA-11 — Interfaz**

Un usuario sin conocimientos de programación deberá poder realizar todo el proceso sin utilizar CMD, PowerShell o una terminal.

### **CA-12 — Aplicación distribuible**

La aplicación deberá poder ejecutarse en un Windows objetivo sin requerir que el usuario instale Python ni las dependencias de desarrollo.

# **17\. Arquitectura conceptual requerida**

La aplicación deberá estructurarse en componentes independientes.

La V1 deberá contemplar conceptualmente:

┌──────────────────┐

│ UI │

└────────┬─────────┘

│

▼

┌──────────────────┐

│ Workflow │

│ / Controller │

└────────┬─────────┘

│

┌────────────┼────────────┐

▼ ▼ ▼

┌─────────┐ ┌────────────┐ ┌───────────┐

│ Scanner │ │ Classifier │ │ Organizer │

└────┬────┘ └──────┬─────┘ └─────┬─────┘

│ │ │

▼ ▼ ▼

Filesystem Image Filesystem

Reader

Los componentes deberán comunicarse mediante interfaces o contratos claros, evitando que la interfaz gráfica contenga lógica de negocio.

La arquitectura **no se considera una arquitectura de microservicios**.

Sin embargo, deberá adoptar un principio similar de independencia funcional:

Cada componente deberá tener una responsabilidad clara, una interfaz definida y el menor acoplamiento posible con los demás componentes.

Esto permitirá evolucionar componentes individuales sin afectar innecesariamente al resto del sistema.

# **18\. Extensibilidad prevista**

La arquitectura deberá dejar abiertas las siguientes posibilidades para futuras versiones.

## **Operaciones de archivos**

V1:

COPY

Futuras:

MOVE

DELETE

La operación de archivo deberá abstraerse para que agregar MOVE no requiera modificar el clasificador.

## **Clasificadores**

V1:

OrientationClassifier

Futuras posibilidades:

DateClassifier

CameraClassifier

LensClassifier

FileTypeClassifier

RatingClassifier

AIClassifier

## **Estructura de carpetas**

V1:

Verticales/

Horizontales/

Cuadradas/

Futuras configuraciones:

01 - Verticales/

02 - Horizontales/

03 - Cuadradas/

o:

Vertical/

Horizontal/

Square/

o estructuras más complejas.

La nomenclatura no debería estar distribuida por todo el código.

## **Formatos**

El lector de imágenes deberá ser extensible.

Agregar soporte para un nuevo formato no debería requerir modificar el clasificador ni la interfaz.

# **19\. Versionado previsto**

El producto utilizará versionado semántico:

MAJOR.MINOR.PATCH

Ejemplos:

1.0.0

1.1.0

1.1.1

2.0.0

Conceptualmente:

- **MAJOR:** cambios importantes o incompatibles.
- **MINOR:** nuevas funcionalidades compatibles.
- **PATCH:** correcciones y mejoras menores.

Ejemplo:

V1.0.0

→ Clasificación por orientación

V1.1.0

→ Soporte para nuevos RAW

V1.2.0

→ Operación MOVE

V1.3.0

→ Nuevas estructuras de carpetas

V2.0.0

→ Sistema de organización más avanzado

La incorporación de MOVE no deberá requerir convertir toda la aplicación en una nueva arquitectura.

# **20\. Restricciones técnicas iniciales**

La implementación de la V1 utilizará:

- Python.
- PySide6 para interfaz gráfica.
- Pillow para formatos de imagen compatibles.
- Un motor adecuado para lectura RAW.
- PyInstaller para distribución inicial.

La selección definitiva del motor RAW y las librerías específicas deberá validarse durante la fase de prototipo técnico.

# **21\. Criterio de éxito del producto**

La V1 será considerada exitosa si un fotógrafo puede:

Abrir la aplicación → seleccionar una carpeta → elegir si incluye subcarpetas → iniciar → esperar el procesamiento → encontrar sus fotografías clasificadas → sin utilizar una terminal y sin riesgo de modificar los originales.

El producto deberá sentirse como una aplicación terminada, no como una herramienta técnica de Python.

# **22\. Roadmap preliminar**

### **V1.0 — PhotoSorter**

- GUI.
- Selección de carpeta.
- Subcarpetas.
- JPG/JPEG/PNG/TIFF/WEBP.
- RAW.
- EXIF Orientation.
- Vertical/Horizontal/Cuadrada.
- Copia.
- Progreso.
- Cancelación.
- Manejo de errores.
- Distribución Windows.

### **V1.x**

Posibles mejoras compatibles:

- Más formatos RAW.
- Configuración de nombres de carpetas.
- Preferencias.
- Mejor manejo de duplicados.
- Logs.
- Historial de operaciones.
- Mejoras de rendimiento.

### **V2.x**

Posibles nuevas capacidades:

- Mover archivos.
- Clasificación por fecha.
- Clasificación por cámara/lente.
- Renombrado.
- Reglas de organización.
- Presets.
- Detección de duplicados.
- Más herramientas específicas para fotógrafos.

# **23\. Decisión fundamental de arquitectura**

El proyecto deberá seguir el siguiente principio:

**La V1 debe ser pequeña en funcionalidad, pero no pequeña en arquitectura.**

No se implementarán funcionalidades futuras antes de necesitarlas.

Sin embargo, las responsabilidades se separarán desde el principio para que esas funcionalidades puedan incorporarse posteriormente sin rehacer la base del proyecto.

La aplicación deberá ser **simple para el usuario, modular internamente y extensible técnicamente**.