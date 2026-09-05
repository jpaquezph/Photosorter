# **Technical Design Document (TDD)**

## **PhotoSorter — V1 Technical Design**

**Documento:** Technical Design Document  
**Proyecto:** PhotoSorter  
**Versión:** 1.0 — V1  
**Estado:** Draft for Review  
**Tipo de aplicación:** Desktop  
**Plataforma objetivo:** Windows  
**Lenguaje:** Python  
**UI:** PySide6

# **1\. Propósito del documento**

Este documento define el diseño técnico detallado de **PhotoSorter V1**, tomando como base los requerimientos funcionales definidos en el PRD y la arquitectura definida en el System Architecture Document (SAD).

Mientras que el SAD describe:

**Cómo está organizada la aplicación y cuáles son sus responsabilidades.**

Este documento describe:

**Cómo se comportarán concretamente los componentes y cómo se comunicarán entre sí.**

El objetivo es llegar a un nivel de definición suficiente para comenzar la implementación de manera controlada, evitando que decisiones importantes de diseño sean tomadas directamente durante la escritura del código.

# **2\. Relación con otros documentos**

PhotoSorter se documentará utilizando diferentes niveles de abstracción.

PRD

Product Requirements Document

│

│ ¿Qué debe hacer?

▼

SAD

System Architecture Document

│

│ ¿Cómo está organizada?

▼

TDD

Technical Design Document

│

│ ¿Cómo se implementa?

▼

Implementation

│

▼

Tests

### **PRD**

Define:

- alcance;
- comportamiento esperado;
- requerimientos;
- reglas funcionales;
- funcionalidades V1;
- funcionalidades futuras.

### **SAD**

Define:

- capas;
- componentes;
- responsabilidades;
- dependencias;
- principios arquitectónicos.

### **TDD**

Define:

- modelos;
- contratos;
- interfaces;
- flujo de datos;
- manejo de errores;
- comportamiento interno;
- decisiones técnicas;
- estructura del código.

# **3\. Alcance técnico de V1**

La V1 debe poder:

1.  Recibir una carpeta de origen.
2.  Analizar archivos de imagen.
3.  Trabajar de forma recursiva o no recursiva según configuración.
4.  Detectar formatos convencionales soportados.
5.  Detectar y procesar archivos RAW soportados.
6.  Obtener dimensiones y orientación.
7.  Clasificar fotografías como:
    - Vertical;
    - Horizontal;
    - Cuadrada.
8.  Determinar un destino.
9.  Crear las carpetas necesarias.
10. Copiar las fotografías.
11. Detectar conflictos.
12. Solicitar una decisión al usuario cuando corresponda.
13. Informar progreso.
14. Informar errores.
15. Permitir cancelar el procesamiento de manera controlada.
16. Generar un resultado final del procesamiento.

La V1 **no moverá ni eliminará archivos originales**.

# **4\. Principios de diseño**

El diseño técnico seguirá los siguientes principios.

## **4.1. Single Responsibility**

Cada componente debe tener una responsabilidad clara.

Scanner

→ encontrar archivos

Reader

→ leer información

Classifier

→ clasificar

DestinationResolver

→ determinar destino

FileOperator

→ ejecutar operación

## **4.2. Dependency Inversion**

Los componentes de alto nivel deben depender de contratos y no de implementaciones concretas.

Conceptualmente:

SorterService

↓

ImageReader

↓

RawImageReader

↓

RAW Library

y no:

SorterService

↓

RAW Library

## **4.3. Implementación reemplazable**

Las dependencias externas deben permanecer aisladas siempre que sea razonable.

Esto es especialmente importante para:

- librerías RAW;
- acceso al filesystem;
- UI;
- logging.

## **4.4. V1 simple, arquitectura extensible**

No se implementarán abstracciones que no tengan una utilidad concreta.

Sin embargo, las responsabilidades deberán quedar separadas de forma que futuras funcionalidades puedan incorporarse sin rediseñar completamente el sistema.

# **5\. Modelo general de ejecución**

El flujo técnico de V1 será:

User

│

▼

UI

│

▼

SorterService

│

▼

FileScanner

│

▼

Photo

│

▼

ImageReader

│

▼

PhotoMetadata

│

▼

Classifier

│

▼

Classification

│

▼

DestinationResolver

│

▼

DestinationPath

│

▼

FileOperator

│

▼

Copy

│

▼

Filesystem

Los errores y conflictos pueden interrumpir o desviar este flujo:

┌─────────────┐

│ Error │

└──────┬──────┘

│

▼

Error Handler

│

▼

UI

┌─────────────┐

│ Conflict │

└──────┬──────┘

│

▼

Conflict Handler

│

▼

UI

│

▼

User Decision

# **6\. Modelos de datos**

Los modelos representan la información que circula por la aplicación.

Los modelos deben ser independientes de la UI y de las librerías utilizadas para leer imágenes.

# **6.1. Photo**

Photo representa un archivo de fotografía que será procesado.

Conceptualmente:

Photo

├── source_path

├── filename

├── extension

└── metadata

### **Responsabilidad**

Representar la fotografía dentro del proceso de PhotoSorter.

### **Ejemplo**

Photo

source_path = C:\\Fotos\\CameraA\\DSC_0001.NEF

filename = DSC_0001.NEF

extension = .NEF

El objeto Photo no debería ser responsable de:

- leer el archivo;
- clasificarlo;
- copiarlo;
- decidir su destino.

Es una representación de datos.

# **6.2. PhotoMetadata**

PhotoMetadata representa información obtenida del archivo de imagen.

Este modelo es especialmente importante porque permite desacoplar los lectores de imágenes del resto de la aplicación.

Conceptualmente:

PhotoMetadata

├── width

├── height

├── orientation

├── format

└── ...

## **6.2.1. Dimensiones**

Debe almacenar:

width

height

Ejemplo:

width = 6048

height = 4024

## **6.2.2. Orientación EXIF**

La orientación física/lógica de una fotografía no debe determinarse únicamente mirando:

width > height

Los archivos pueden contener información EXIF de orientación.

Por lo tanto, el modelo debe permitir representar la orientación declarada por el archivo.

Conceptualmente:

orientation

podrá representar valores equivalentes a las orientaciones EXIF estándar.

La forma exacta de modelar estos valores se definirá durante la implementación.

## **6.2.3. Format**

Debe identificar el formato del archivo.

Ejemplos:

JPG

JPEG

PNG

TIFF

NEF

CR2

CR3

ARW

RAF

ORF

RW2

El listado final de formatos RAW soportados dependerá del RAW Spike.

## **6.2.4. Información adicional**

El modelo debe diseñarse de manera que permita incorporar metadata adicional posteriormente.

Ejemplos futuros:

camera_make

camera_model

lens

date_taken

iso

focal_length

shutter_speed

gps

Sin embargo, **estos campos no son obligatorios para V1** si no son necesarios para la clasificación.

La V1 debe evitar leer o almacenar metadata que no utilice.

# **6.3. Classification**

Representa el resultado de clasificar una fotografía.

V1 tendrá tres categorías:

VERTICAL

HORIZONTAL

SQUARE

Conceptualmente:

PhotoMetadata

│

▼

OrientationClassifier

│

▼

Classification

La clasificación deberá ser un valor controlado y no un string arbitrario.

Conceptualmente:

Classification.VERTICAL

Classification.HORIZONTAL

Classification.SQUARE

Esto reduce errores como:

"vertical"

"Vertical"

"VERTICAL"

"vert"

que podrían representar accidentalmente el mismo concepto.

# **6.4. DestinationPath**

Representa el destino calculado para una fotografía.

Ejemplo:

C:\\Fotos\\Organizadas\\Verticales\\DSC_0001.NEF

Este concepto puede representarse como una ruta de filesystem, pero debe mantenerse separado conceptualmente del objeto Photo.

La fotografía responde:

¿Qué archivo soy?

El destino responde:

¿Dónde debería terminar?

# **6.5. FileConflict**

Representa un conflicto entre el archivo de origen y el archivo que se pretende generar.

Debe contener suficiente información para que la UI pueda mostrar el conflicto.

Conceptualmente:

FileConflict

├── source_path

├── destination_path

└── conflict_type

Ejemplo:

Source:

C:\\Fotos\\CameraB\\DSC_0001.NEF

Destination:

C:\\Fotos\\Organizadas\\Verticales\\DSC_0001.NEF

# **6.6. ConflictResolution**

Representa la decisión tomada por el usuario.

Posibles valores iniciales:

SKIP

REPLACE

RENAME

CANCEL

El conjunto definitivo podrá ajustarse durante el diseño de UI.

# **6.7. ProcessingResult**

Representa el resultado final del procesamiento.

Conceptualmente:

ProcessingResult

├── total_files

├── processed_files

├── copied_files

├── skipped_files

├── error_files

├── vertical_count

├── horizontal_count

├── square_count

└── cancelled

Ejemplo:

Total: 1250

Procesados: 1248

Copiados: 1245

Omitidos: 3

Errores: 2

Verticales: 530

Horizontales: 690

Cuadradas: 28

Este modelo permite que la UI muestre un resumen sin conocer detalles internos del procesamiento.

# **6.8. AppSettings**

Representa la configuración seleccionada por el usuario.

V1 deberá contemplar como mínimo:

AppSettings

├── source_folder

├── recursive

└── operation

Ejemplo:

source_folder = C:\\Fotos\\Trabajo

recursive = true

operation = COPY

En V1:

operation = COPY

La posibilidad de:

MOVE

queda reservada para una futura versión.

# **7\. Interfaces y contratos**

Las interfaces representan los contratos utilizados entre las capas.

No representan la interfaz gráfica.

Su función principal es desacoplar el dominio de las implementaciones concretas.

# **7.1. FileScanner**

Responsabilidad:

Encontrar los archivos que deben procesarse.

Conceptualmente:

FileScanner

↓

List\[Photo\]

Entrada:

source_folder

recursive

Salida:

Photo\[\]

El Scanner no debe:

- leer metadata;
- clasificar fotografías;
- copiar archivos;
- modificar archivos.

# **7.2. ImageReader**

Responsabilidad:

Obtener información de un archivo de imagen.

Conceptualmente:

ImageReader

↓

PhotoMetadata

Entrada:

Photo / Path

Salida:

PhotoMetadata

Posibles implementaciones:

ImageReader

├── StandardImageReader

└── RawImageReader

# **7.3. Classifier**

Responsabilidad:

Determinar la categoría de una fotografía a partir de información previamente obtenida.

Entrada:

PhotoMetadata

Salida:

Classification

V1:

OrientationClassifier

Futuras implementaciones podrían incluir:

DateClassifier

CameraClassifier

LensClassifier

AIClassifier

# **7.4. DestinationResolver**

Responsabilidad:

Determinar el destino de una fotografía.

Entrada conceptual:

Photo

Classification

AppSettings

Salida:

DestinationPath

V1:

VERTICAL

↓

Verticales/

HORIZONTAL

↓

Horizontales/

SQUARE

↓

Cuadradas/

El resolver no copia archivos.

# **7.5. FileOperator**

Responsabilidad:

Ejecutar la operación sobre el archivo.

V1:

FileOperator

↓

CopyFileOperator

Entrada:

source_path

destination_path

Resultado:

success

o una excepción/error controlado.

Futuro:

FileOperator

├── CopyFileOperator

└── MoveFileOperator

# **8\. Dependency Flow**

Las dependencias principales serán:

SorterService

│

├── FileScanner

├── ImageReader

├── Classifier

├── DestinationResolver

└── FileOperator

El SorterService coordina las operaciones.

Los componentes especializados no deberían conocer al SorterService.

Por ejemplo:

CORRECTO

SorterService → Scanner

pero no:

INCORRECTO

Scanner → SorterService

Esto mantiene la dirección de las dependencias clara.

# **9\. Flujo detallado de procesamiento**

## **9.1. Inicio**

El usuario configura:

Source:

C:\\Fotos

Recursive:

YES

Operation:

COPY

La UI construye:

AppSettings

y solicita al SorterService iniciar el proceso.

# **9.2. Scanning**

SorterService solicita:

FileScanner.scan(settings)

El Scanner analiza:

C:\\Fotos

y devuelve una colección de fotografías.

Ejemplo:

Photo 1 → DSC_0001.NEF

Photo 2 → DSC_0002.CR3

Photo 3 → IMG_0003.JPG

# **9.3. Lectura**

Por cada fotografía:

Photo

↓

ImageReader

↓

PhotoMetadata

El sistema obtiene:

width

height

orientation

format

# **9.4. Clasificación**

El Classifier recibe:

PhotoMetadata

y devuelve:

Classification

Ejemplo:

6048 × 4024

↓

HORIZONTAL

# **9.5. Resolución de destino**

El DestinationResolver recibe la fotografía y su clasificación.

Ejemplo:

Classification:

VERTICAL

Destination:

C:\\Fotos\\Organizadas\\Verticales\\DSC_0001.NEF

# **9.6. Verificación de destino**

Antes de realizar la operación se verifica:

¿Existe el archivo destino?

### **No existe**

Continuar:

COPY

### **Existe**

Crear:

FileConflict

y solicitar una decisión.

# **9.7. Copia**

El CopyFileOperator ejecuta:

Source

↓

COPY

↓

Destination

Los archivos originales permanecen intactos.

# **9.8. Resultado**

Al terminar:

ProcessingResult

es enviado a la UI.

La UI muestra un resumen.

# **10\. Algoritmo conceptual de V1**

El algoritmo general será equivalente a:

START

Load settings

Scan source folder

FOR each photo:

Read image metadata

Classify orientation

Resolve destination

Check destination

IF destination does not exist:

Copy file

ELSE:

Create conflict

Ask user for resolution

Apply resolution

Update progress

Check cancellation

END FOR

Generate ProcessingResult

Display result

END

Este algoritmo representa el flujo funcional, no necesariamente la implementación exacta en Python.

# **11\. Determinación de orientación**

La orientación debe considerar correctamente:

1.  dimensiones de la imagen;
2.  metadata EXIF de orientación cuando corresponda.

Conceptualmente:

Raw/Image File

↓

ImageReader

↓

width

height

EXIF orientation

↓

OrientationClassifier

↓

VERTICAL / HORIZONTAL / SQUARE

El detalle exacto de cómo se normalizará EXIF Orientation será definido durante la implementación y los tests.

La regla deberá quedar centralizada en OrientationClassifier.

Ningún otro componente debe implementar su propia lógica de orientación.

# **12\. Manejo de archivos RAW**

El soporte RAW forma parte del alcance de V1.

Sin embargo, la implementación concreta del RawImageReader dependerá del resultado del **RAW Spike**.

El Spike deberá evaluar:

- compatibilidad con los RAW disponibles;
- soporte de distintas marcas;
- lectura de dimensiones;
- lectura de orientación;
- comportamiento ante archivos RAW problemáticos;
- rendimiento;
- dependencias;
- distribución;
- licencia.

La arquitectura deberá mantener el lector RAW detrás del contrato:

ImageReader

De esta manera:

SorterService

↓

ImageReader

↓

RawImageReader

↓

RAW Library

El SorterService no tendrá conocimiento directo de la librería RAW.

# **13\. Manejo de errores**

Los errores se dividirán conceptualmente en diferentes categorías.

## **13.1. Error de lectura**

Ejemplo:

RAW corrupto

Archivo incompleto

Formato no soportado

Comportamiento esperado:

Reader

↓

Error

↓

SorterService

↓

Registrar error

↓

Continuar con siguiente archivo

La aplicación no debería detener todo el procesamiento por un único archivo ilegible, salvo que el error sea de una naturaleza que impida continuar.

# **13.2. Error de filesystem**

Ejemplos:

No se puede crear carpeta

No hay permisos

Archivo bloqueado

Disco lleno

El comportamiento dependerá del error concreto.

Deberá evitarse ocultar el error.

# **13.3. Error de configuración**

Ejemplos:

Carpeta inexistente

Ruta inválida

Destino no accesible

Estos errores deberán detectarse preferentemente **antes de comenzar el procesamiento**.

# **14\. Política de errores**

Principio general:

**Un error individual de una fotografía no debería impedir procesar el resto de las fotografías cuando sea seguro continuar.**

Ejemplo:

1000 fotos

999 → procesadas

1 → error de lectura

Resultado:

ProcessingResult

processed = 999

errors = 1

En cambio, un error estructural como:

No se puede acceder al directorio de destino

podría requerir detener el proceso.

# **15\. Manejo de conflictos**

Los conflictos se tratarán como una situación funcional y no necesariamente como un error.

Ejemplo:

Source:

CameraB/DSC_0001.NEF

Destination:

Verticales/DSC_0001.NEF

Destination exists = TRUE

Se crea:

FileConflict

La UI presenta:

El archivo ya existe.

Origen:

C:\\Fotos\\CameraB\\DSC_0001.NEF

Destino:

C:\\Fotos\\Organizadas\\Verticales\\DSC_0001.NEF

El usuario toma una decisión.

# **16\. Operaciones de conflicto**

Las acciones previstas son:

SKIP

REPLACE

RENAME

CANCEL

### **SKIP**

No se copia el archivo actual.

### **REPLACE**

Reemplaza el archivo existente.

Esta acción deberá requerir confirmación según el diseño final de UI.

### **RENAME**

Genera un nuevo nombre para evitar el conflicto.

Ejemplo:

DSC_0001.NEF

DSC_0001_1.NEF

DSC_0001_2.NEF

La estrategia definitiva de nomenclatura deberá documentarse antes de implementarla.

### **CANCEL**

Solicita detener el procesamiento.

# **17\. Nombres de archivos**

La V1 mantendrá los nombres originales siempre que sea posible.

Ejemplo:

DSC_0001.NEF

se convertirá en:

Verticales/DSC_0001.NEF

No se implementará una estrategia global de renombrado en V1.

La arquitectura deberá permitir incorporar posteriormente diferentes estrategias de nomenclatura.

# **18\. Archivos duplicados**

Se asume que en una carpeta original no deberían existir dos archivos con el mismo nombre y extensión.

Sin embargo, la recursividad puede producir situaciones como:

CameraA/DSC_0001.NEF

CameraB/DSC_0001.NEF

Al organizar ambos en un mismo destino:

Verticales/DSC_0001.NEF

se genera un conflicto.

La aplicación no deberá sobrescribir silenciosamente.

El usuario deberá ser informado.

# **19\. Recursividad**

La opción de recursividad pertenece al FileScanner.

### **Recursividad desactivada**

Source/

├── DSC001.NEF

├── DSC002.NEF

└── CameraA/

└── DSC003.NEF

Se procesan únicamente:

DSC001.NEF

DSC002.NEF

### **Recursividad activada**

Se procesan:

DSC001.NEF

DSC002.NEF

CameraA/DSC003.NEF

La estructura original de subdirectorios no determina automáticamente la estructura de destino en V1.

# **20\. Destinos predeterminados**

V1 tendrá tres categorías:

Verticales/

Horizontales/

Cuadradas/

Ejemplo:

Organizadas/

│

├── Verticales/

├── Horizontales/

└── Cuadradas/

El DestinationResolver será responsable de esta decisión.

Esto permitirá posteriormente introducir otros resolvers sin modificar el clasificador.

# **21\. Futuras estrategias de destino**

La arquitectura permitirá incorporar posteriormente:

DefaultDestinationResolver

DateBasedDestinationResolver

CameraBasedDestinationResolver

CustomDestinationResolver

Ejemplo futuro:

2026/

├── Enero/

├── Febrero/

└── Marzo/

o:

Canon/

Nikon/

Sony/

Estas funcionalidades no forman parte de V1.

# **22\. Procesamiento en segundo plano**

La aplicación no debe bloquear la interfaz mientras procesa archivos.

Conceptualmente:

Main Thread

│

└── UI

│

└── Worker

│

└── SorterService

El Worker ejecutará el procesamiento.

La UI recibirá actualizaciones.

# **23\. Eventos de procesamiento**

El procesamiento deberá poder comunicar eventos como:

PROCESS_STARTED

FILE_STARTED

FILE_COMPLETED

PROGRESS_UPDATED

CONFLICT_DETECTED

ERROR_OCCURRED

PROCESS_CANCELLED

PROCESS_FINISHED

Estos eventos permiten desacoplar el procesamiento de la presentación.

# **24\. Progreso**

La UI debe poder mostrar progreso.

Ejemplo:

Procesando...

563 / 1250

45%

El SorterService no debería manipular directamente elementos gráficos.

Debe emitir información de progreso.

La UI decide cómo representarla.

# **25\. Cancelación**

La cancelación será cooperativa.

Flujo:

User

↓

Cancel

↓

UI

↓

Worker

↓

Cancellation Request

↓

SorterService

El procesamiento deberá comprobar periódicamente si existe una solicitud de cancelación.

No se deberá finalizar violentamente un proceso mientras una operación crítica de filesystem está en ejecución.

# **26\. Logging**

El sistema contará con logging interno.

Los logs deberán permitir diagnosticar:

- inicio de procesamiento;
- configuración utilizada;
- cantidad de archivos encontrados;
- archivos procesados;
- conflictos;
- errores;
- cancelación;
- finalización.

Ejemplo:

INFO Processing started

INFO Source: C:\\Fotos

INFO Recursive: true

INFO Files found: 1250

INFO DSC_0001.NEF -> VERTICAL

INFO DSC_0002.CR3 -> HORIZONTAL

WARNING Conflict: DSC_0003.NEF

ERROR Unable to read IMG_0045.CR3

INFO Processing finished

# **27\. Testing**

El diseño debe permitir probar cada componente independientemente.

## **27.1. Unit Tests**

Principalmente:

OrientationClassifier

DestinationResolver

Conflict handling

Models

Configuration

Ejemplos:

6000 × 4000 → HORIZONTAL

4000 × 6000 → VERTICAL

4000 × 4000 → SQUARE

# **27.2. Integration Tests**

Se probarán interacciones entre componentes.

Ejemplo:

Scanner

↓

Reader

↓

Classifier

↓

DestinationResolver

↓

FileOperator

# **27.3. End-to-End Tests**

Posteriormente se podrá probar el flujo completo:

Folder

↓

PhotoSorter

↓

Organized folders

# **28\. Test Dataset**

El proyecto deberá disponer de un conjunto controlado de fotografías para pruebas.

Especialmente importante:

JPEG

PNG

TIFF

RAW Nikon

RAW Canon

RAW Sony

RAW otras marcas disponibles

El dataset debe incluir:

- verticales;
- horizontales;
- cuadradas;
- diferentes orientaciones EXIF;
- nombres duplicados;
- archivos ilegibles;
- archivos no soportados;
- estructuras con subdirectorios.

El dataset no debe depender de fotografías personales reales cuando pueda evitarse.

# **29\. RAW Spike**

Antes de cerrar definitivamente la implementación de RawImageReader, se realizará un spike técnico.

El objetivo no es construir una funcionalidad definitiva, sino responder:

**¿Qué tecnología utilizará PhotoSorter para leer RAW de manera confiable y distribuible?**

## **29.1. Entrada**

El usuario ya dispone de un conjunto de prueba con RAW de diferentes fabricantes.

Ese conjunto será utilizado como dataset inicial.

## **29.2. Evaluación**

Cada alternativa será evaluada en:

Compatibilidad

Metadata

Orientación

Rendimiento

Estabilidad

Distribución

Dependencias

Licencia

Mantenimiento

## **29.3. Criterio de aceptación**

Una alternativa será candidata para V1 si:

1.  procesa los RAW necesarios;
2.  devuelve correctamente dimensiones;
3.  permite obtener orientación;
4.  tiene comportamiento estable;
5.  puede distribuirse con la aplicación;
6.  posee una licencia compatible con la estrategia open source prevista;
7.  no introduce una dependencia excesivamente pesada para el objetivo del producto.

# **30\. Licenciamiento**

El proyecto busca mantener una estrategia de licenciamiento **open source**.

Por este motivo, antes de incorporar una dependencia se deberá revisar:

- licencia;
- obligaciones de distribución;
- compatibilidad con la licencia futura del proyecto;
- distribución de binarios;
- dependencias transitivas relevantes.

No se deberá incorporar una librería únicamente porque funcione técnicamente.

La decisión final deberá considerar tanto:

Technical Fit

como:

License Fit

# **31\. Dependencias externas**

Las dependencias deberán mantenerse concentradas en las capas donde sean necesarias.

Ejemplo:

Infrastructure

├── Pillow

├── RAW Library

└── Filesystem APIs

La lógica de negocio no debería importar directamente esas librerías.

Esto permitirá:

- reemplazar dependencias;
- facilitar testing;
- reducir acoplamiento;
- simplificar futuras actualizaciones.

# **32\. Estructura conceptual del proyecto**

La estructura inicial propuesta será:

PhotoSorter/

│

├── src/

│ └── photosorter/

│ │

│ ├── ui/

│ │

│ ├── application/

│ │

│ ├── domain/

│ │ ├── models/

│ │ ├── interfaces/

│ │ └── services/

│ │

│ └── infrastructure/

│ ├── filesystem/

│ ├── image/

│ └── logging/

│

├── tests/

│ ├── unit/

│ ├── integration/

│ └── e2e/

│

├── raw_spike/

│

├── docs/

│

├── assets/

│

├── pyproject.toml

├── README.md

├── LICENSE

└── .gitignore

La estructura exacta de módulos podrá modificarse durante la implementación si se determina que una división resulta innecesariamente compleja.

# **33\. Separación del RAW Spike**

El RAW Spike debe permanecer separado del producto principal.

PhotoSorter/

│

├── src/

│ └── photosorter/

│

└── raw_spike/

El Spike existe para responder preguntas técnicas.

Una vez tomada la decisión:

RAW Spike

↓

Decision

↓

RawImageReader

↓

Production Code

El código experimental no debe convertirse automáticamente en código productivo.

# **34\. Packaging**

El objetivo final de V1 será distribuir la aplicación de manera que el usuario final no necesite conocimientos técnicos.

El usuario debería poder:

PhotoSorter.exe

↓

Double Click

↓

Application

Sin requerir:

- Python;
- CMD;
- instalación manual de paquetes;
- configuración de entorno virtual.

El mecanismo concreto de packaging se definirá durante la fase correspondiente.

# **35\. Actualizaciones futuras**

La arquitectura debe permitir incorporar nuevas versiones de manera incremental.

Ejemplo:

### **V1**

COPY

### **V2**

COPY

MOVE

### **V3**

COPY

MOVE

Custom Naming

### **V4**

COPY

MOVE

Custom Naming

Date Classification

El objetivo no es implementar toda esta funcionalidad desde el principio, sino evitar que V1 bloquee estas posibilidades.

# **36\. Matriz de responsabilidades**

| **Componente** | **Responsabilidad** | **No debe hacer** |
| --- | --- | --- |
| UI  | Interacción con usuario | Lógica de negocio |
| --- | --- | --- |
| SorterService | Orquestar workflow | Implementar detalles técnicos |
| --- | --- | --- |
| FileScanner | Encontrar archivos | Leer metadata |
| --- | --- | --- |
| ImageReader | Leer imágenes | Clasificar |
| --- | --- | --- |
| RawImageReader | Leer RAW | Copiar archivos |
| --- | --- | --- |
| Classifier | Clasificar | Manipular filesystem |
| --- | --- | --- |
| DestinationResolver | Resolver destino | Copiar archivos |
| --- | --- | --- |
| FileOperator | Ejecutar operación | Clasificar |
| --- | --- | --- |
| ConflictService | Gestionar conflictos | Leer imágenes |
| --- | --- | --- |
| Models | Representar datos | Ejecutar workflow |
| --- | --- | --- |
| Infrastructure | Implementar operaciones técnicas | Contener reglas de negocio |
| --- | --- | --- |

# **37\. Flujo de dependencias completo**

La arquitectura técnica puede resumirse como:

USER

│

▼

┌─────────────┐

│ UI │

└──────┬──────┘

│

▼

┌─────────────┐

│ SorterService│

└──────┬──────┘

│

┌────────────────┼────────────────┐

│ │ │

▼ ▼ ▼

FileScanner ImageReader Classifier

│ │

┌─────┴─────┐ │

▼ ▼ │

Standard RAW │

Reader Reader │

│ │ │

└─────┬─────┘ │

▼ │

PhotoMetadata ─────────┘

│

▼

Classification

│

▼

DestinationResolver

│

▼

DestinationPath

│

▼

FileOperator

│

▼

COPY

│

▼

FILESYSTEM

# **38\. Decisiones de diseño fundamentales**

Las siguientes decisiones quedan establecidas como base técnica de V1:

### **D1 — Operación segura**

V1 utiliza COPY y no modifica los archivos originales.

### **D2 — RAW desde V1**

El soporte RAW forma parte del alcance inicial y será validado mediante un RAW Spike.

### **D3 — Reader abstraction**

Los lectores de imágenes estarán detrás de ImageReader.

### **D4 — Classifier independiente**

La lógica de orientación estará centralizada en OrientationClassifier.

### **D5 — Destination separado**

La clasificación y la determinación del destino serán responsabilidades diferentes.

### **D6 — FileOperator abstraído**

La operación de filesystem estará detrás de FileOperator.

### **D7 — Conflictos explícitos**

No se sobrescribirán archivos silenciosamente.

### **D8 — UI desacoplada**

La UI no contendrá lógica de procesamiento.

### **D9 — Procesamiento en background**

El procesamiento se ejecutará fuera del hilo principal de la UI.

### **D10 — Dependencias reemplazables**

Las librerías externas estarán aisladas mediante las capas correspondientes.

### **D11 — Open Source**

Las dependencias deberán ser compatibles con la estrategia de licenciamiento prevista.

### **D12 — Sin persistencia innecesaria**

V1 no requiere una base de datos para realizar su función principal.

# **39\. Roadmap técnico**

El desarrollo se dividirá en milestones.

## **M0 — Technical Foundation**

Objetivo:

RAW / Image

↓

Reader

↓

Metadata

↓

Classifier

↓

Classification

Resultado esperado:

DSC_001.NEF → VERTICAL

DSC_002.CR3 → HORIZONTAL

IMG_003.JPG → SQUARE

Sin UI.

## **M1 — File Organization**

Agregar:

DestinationResolver

FileOperator

Resultado:

Organizadas/

├── Verticales/

├── Horizontales/

└── Cuadradas/

## **M2 — Conflict Handling**

Agregar:

FileConflict

ConflictResolution

ConflictService

y las reglas de interacción correspondientes.

## **M3 — Processing Control**

Agregar:

- progreso;
- cancelación;
- logging;
- resultados;
- manejo completo de errores.

## **M4 — Desktop UI**

Implementar:

Folder Selection

Configuration

Start

Progress

Conflicts

Errors

Results

## **M5 — Packaging**

Generar una aplicación distribuible:

PhotoSorter.exe

y probarla en un entorno Windows sin Python instalado.

# **40\. Criterio para comenzar la implementación**

La implementación de producción comenzará cuando estén cerrados:

✓ PRD V1

✓ SAD

✓ Modelos

✓ Interfaces

✓ Flujo principal

✓ Manejo de errores

✓ Reglas de conflictos

✓ RAW Spike

✓ Decisión de librería RAW

✓ Decisión de licenciamiento

No es necesario definir absolutamente cada detalle de UI antes de comenzar.

La prioridad es cerrar primero los **contratos y modelos que forman el núcleo del sistema**.

# **41\. Próximo paso técnico**

El siguiente paso será convertir este diseño conceptual en una especificación concreta de los contratos.

En particular:

Photo

PhotoMetadata

Classification

FileConflict

ConflictResolution

ProcessingResult

AppSettings

y posteriormente:

FileScanner

ImageReader

Classifier

DestinationResolver

FileOperator

Para cada uno se deberá definir:

- nombre;
- responsabilidad;
- entradas;
- salidas;
- errores;
- invariantes;
- comportamiento esperado;
- ejemplos;
- tests asociados.

El resultado de esta etapa será suficientemente preciso como para comenzar a escribir las primeras clases Python sin tener que tomar decisiones arquitectónicas importantes durante la implementación.

# **42\. Estado del diseño**

**Estado actual:**

PRD

✓

│

▼

SAD

✓

│

▼

TDD

✓ Conceptual

│

▼

Contract Specification

← SIGUIENTE ETAPA

│

▼

RAW Spike

│

▼

Implementation

El TDD establece la base técnica de PhotoSorter V1 y mantiene la separación entre **qué hace el producto**, **cómo está organizado** y **cómo se implementarán concretamente sus componentes**.