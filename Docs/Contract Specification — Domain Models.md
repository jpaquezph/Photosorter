# **Contract Specification — Domain Models**

**Proyecto:** PhotoSorter  
**Versión:** V1  
**Documento:** Contract Specification — Domain Models  
**Estado:** Baseline para implementación  
**Propósito:** Definir los modelos de dominio y sus contratos, independientemente de la interfaz gráfica y de las implementaciones concretas de infraestructura.

## **1\. Objetivo**

Este documento define los **modelos de dominio** utilizados por PhotoSorter durante el procesamiento de fotografías.

Los modelos representan información y estados propios del negocio. No deben depender de:

- PySide6 u otra tecnología de UI.
- La librería concreta utilizada para leer imágenes.
- El sistema operativo.
- El sistema de archivos.
- Una base de datos.
- Un framework específico.

El objetivo es que el dominio pueda mantenerse estable aunque cambien las implementaciones técnicas.

# **2\. Principios de los modelos**

Los modelos deben cumplir las siguientes reglas:

### **2.1 Independencia tecnológica**

Los modelos no deben importar ni conocer clases provenientes de infraestructura o UI.

Ejemplo:

Photo

↓

PhotoMetadata

↓

Classification

Pero:

Photo

✗ no conoce PySide6

✗ no conoce Pillow

✗ no conoce rawpy

✗ no conoce Windows

✗ no conoce shutil

### **2.2 Inmutabilidad preferida**

Los modelos que representan resultados de procesamiento deberían ser preferentemente inmutables.

Esto reduce modificaciones accidentales durante el procesamiento y facilita:

- testing;
- concurrencia;
- debugging;
- trazabilidad;
- futuras ejecuciones paralelas.

### **2.3 Validación**

Los modelos deben impedir estados inválidos siempre que sea razonablemente posible.

Por ejemplo:

Classification = "vertical"

es válido.

Mientras que:

Classification = "banana"

no lo es.

### **2.4 Separación entre datos y comportamiento**

Los modelos contienen principalmente:

- datos;
- validaciones;
- invariantes;
- comportamiento mínimo relacionado directamente con su propia representación.

La lógica de procesamiento debe permanecer en los componentes correspondientes.

Por ejemplo:

Photo

no decide dónde copiarse.

Eso corresponde a:

DestinationResolver

# **3\. Flujo de modelos**

El flujo conceptual de datos de V1 es:

Filesystem

↓

Photo

↓

ImageReader

↓

PhotoMetadata

↓

Classifier

↓

Classification

↓

DestinationResolver

↓

DestinationPath

↓

FileOperator

↓

ProcessingResult

En caso de conflicto:

DestinationPath

↓

FileConflict

↓

ConflictResolution

↓

FileOperator

↓

ProcessingResult

# **4\. Modelo Photo**

## **4.1 Propósito**

Representa una fotografía identificada por PhotoSorter para ser procesada.

Photo representa el archivo físico de entrada, pero no contiene información específica sobre cómo será procesado.

## **4.2 Atributos**

| **Campo** | **Tipo** | **Obligatorio** |
| --- | --- | --- |
| source_path | Path | Sí  |
| --- | --- | --- |

### **source_path**

Ruta absoluta o normalizada al archivo de origen.

Ejemplo:

C:\\Fotos\\Vacaciones\\IMG_1234.CR3

## **4.3 Invariantes**

source_path debe:

1.  representar una ruta válida;
2.  apuntar a un archivo, no a un directorio;
3.  no estar vacío;
4.  estar normalizado antes de entrar al flujo de procesamiento.

El modelo no necesariamente debe comprobar que el archivo exista.

La existencia del archivo corresponde al componente encargado de interactuar con el filesystem.

## **4.4 Ejemplo**

Photo(

source_path=Path("C:/Fotos/Vacaciones/IMG_1234.CR3")

)

## **4.5 Estados inválidos**

Photo(source_path=None)

Photo(source_path="")

Photo(source_path=Path("C:/Fotos"))

si la ruta representa un directorio.

# **5\. Modelo PhotoMetadata**

## **5.1 Propósito**

Representa la información técnica relevante obtenida desde una fotografía.

Es el resultado producido por un ImageReader.

## **5.2 Atributos**

| **Campo** | **Tipo** | **Obligatorio** |
| --- | --- | --- |
| width | int | Sí  |
| --- | --- | --- |
| height | int | Sí  |
| --- | --- | --- |
| format | str | Sí  |
| --- | --- | --- |
| camera_make | str \| None | No  |
| --- | --- | --- |
| camera_model | str \| None | No  |
| --- | --- | --- |
| lens | str \| None | No  |
| --- | --- | --- |
| orientation | int \| None | No  |
| --- | --- | --- |

Para V1, los datos mínimos requeridos para clasificar una fotografía son:

width

height

El resto de los metadatos se considera información adicional y podrá ampliarse posteriormente.

## **5.3 Dimensiones**

### **width**

Ancho de la imagen en píxeles.

Debe cumplir:

width > 0

### **height**

Alto de la imagen en píxeles.

Debe cumplir:

height > 0

## **5.4 Formato**

format identifica el formato detectado por el lector.

Ejemplos:

JPEG

PNG

CR2

CR3

NEF

ARW

DNG

ORF

RW2

La lista definitiva de formatos soportados no forma parte del modelo.

La capacidad de leer cada formato pertenece a ImageReader.

## **5.5 Metadatos opcionales**

Los siguientes valores pueden no estar presentes:

camera_make

camera_model

lens

orientation

La ausencia de estos datos **no debe impedir clasificar la fotografía por orientación geométrica**.

## **5.6 Ejemplo**

PhotoMetadata(

width=6000,

height=4000,

format="JPEG",

camera_make="NIKON CORPORATION",

camera_model="NIKON D5200",

lens="18-55mm",

orientation=1

)

# **6\. Modelo Classification**

## **6.1 Propósito**

Representa el resultado de clasificar una fotografía según su relación entre ancho y alto.

V1 contempla tres categorías:

VERTICAL

HORIZONTAL

SQUARE

## **6.2 Valores permitidos**

Se recomienda implementar el modelo mediante un Enum.

Conceptualmente:

class Classification(Enum):

VERTICAL = "vertical"

HORIZONTAL = "horizontal"

SQUARE = "square"

## **6.3 Reglas**

La clasificación se determina utilizando:

width

height

### **Vertical**

height > width

Resultado:

VERTICAL

### **Horizontal**

width > height

Resultado:

HORIZONTAL

### **Cuadrada**

width == height

Resultado:

SQUARE

## **6.4 Ejemplos**

6000 × 4000 → HORIZONTAL

4000 × 6000 → VERTICAL

4000 × 4000 → SQUARE

## **6.5 Invariante**

Una fotografía debe tener exactamente una clasificación.

No debe existir un estado:

UNKNOWN

dentro del resultado normal de V1.

Si no es posible obtener las dimensiones necesarias, el procesamiento debe producir un error y no una clasificación artificial.

# **7\. Modelo DestinationPath**

## **7.1 Propósito**

Representa la ubicación de destino calculada para una fotografía.

Es importante separar este modelo de Classification.

La clasificación responde:

¿Qué tipo de fotografía es?

El destino responde:

¿Dónde debe copiarse?

Esto permite modificar posteriormente las reglas de organización sin modificar el clasificador.

## **7.2 Atributos**

| **Campo** | **Tipo** | **Obligatorio** |
| --- | --- | --- |
| path | Path | Sí  |
| --- | --- | --- |

## **7.3 Ejemplo**

DestinationPath(

path=Path("C:/Fotos/Organizadas/Verticales")

)

## **7.4 V1**

Los destinos predeterminados son:

Verticales/

Horizontales/

Cuadradas/

La implementación concreta de cómo se construyen estos paths pertenece a:

DestinationResolver

No debe codificarse esa lógica dentro de Classification.

# **8\. Modelo FileConflict**

## **8.1 Propósito**

Representa una situación en la que el archivo que se intenta copiar tiene como destino un archivo que ya existe.

V1 no permite sobrescritura silenciosa.

## **8.2 Atributos**

| **Campo** | **Tipo** | **Obligatorio** |
| --- | --- | --- |
| source_path | Path | Sí  |
| --- | --- | --- |
| destination_path | Path | Sí  |
| --- | --- | --- |

## **8.3 Ejemplo**

FileConflict(

source_path=Path(

"C:/Fotos/Viaje/IMG_001.CR3"

),

destination_path=Path(

"C:/Fotos/Organizadas/Verticales/IMG_001.CR3"

)

)

## **8.4 Requisito funcional**

El conflicto debe mostrar al usuario **las rutas completas** de ambos archivos.

Esto permite distinguir entre:

C:/Fotos/Viaje1/IMG_001.CR3

y:

C:/Fotos/Viaje2/IMG_001.CR3

aunque ambos tengan el mismo nombre.

# **9\. Modelo ConflictResolution**

## **9.1 Propósito**

Representa la decisión tomada frente a un conflicto.

## **9.2 Valores**

V1 debe contemplar como mínimo:

SKIP

OVERWRITE

Se puede considerar:

RENAME

como extensión futura, pero no forma parte del contrato funcional de V1 salvo que posteriormente se incorpore al PRD.

## **9.3 Definición conceptual**

class ConflictResolution(Enum):

SKIP = "skip"

OVERWRITE = "overwrite"

## **9.4 Reglas**

### **SKIP**

El archivo de origen permanece intacto y no se realiza la copia.

### **OVERWRITE**

El archivo de destino existente es reemplazado por el archivo de origen.

La operación debe quedar registrada en el resultado y en el log.

# **10\. Modelo ProcessingResult**

## **10.1 Propósito**

Representa el resultado individual del procesamiento de una fotografía.

Permite que el sistema diferencie entre:

- procesamientos exitosos;
- archivos omitidos;
- conflictos;
- errores.

## **10.2 Atributos**

| **Campo** | **Tipo** | **Obligatorio** |
| --- | --- | --- |
| source_path | Path | Sí  |
| --- | --- | --- |
| status | ProcessingStatus | Sí  |
| --- | --- | --- |
| destination_path | Path \| None | No  |
| --- | --- | --- |
| error | str \| None | No  |
| --- | --- | --- |

## **10.3 ProcessingStatus**

Se recomienda un Enum.

Valores iniciales:

class ProcessingStatus(Enum):

COPIED = "copied"

SKIPPED = "skipped"

OVERWRITTEN = "overwritten"

FAILED = "failed"

## **10.4 Reglas de consistencia**

### **COPIED**

Debe existir:

destination_path

y no debería existir:

error

### **OVERWRITTEN**

Debe existir:

destination_path

y no debería existir:

error

### **SKIPPED**

Puede contener:

destination_path

si el destino fue determinado.

No requiere error.

### **FAILED**

Debe existir información suficiente para determinar la causa del fallo.

Puede utilizar:

error

como representación inicial.

Posteriormente podría evolucionar hacia un modelo de error más estructurado.

# **11\. Modelo AppSettings**

## **11.1 Propósito**

Representa la configuración necesaria para ejecutar una operación de organización.

No representa configuración visual de la aplicación.

## **11.2 Atributos V1**

| **Campo** | **Tipo** | **Obligatorio** |
| --- | --- | --- |
| source_path | Path | Sí  |
| --- | --- | --- |
| destination_path | Path | Sí  |
| --- | --- | --- |
| recursive | bool | Sí  |
| --- | --- | --- |

## **11.3 Ejemplo**

AppSettings(

source_path=Path("C:/Fotos"),

destination_path=Path("C:/Fotos/Organizadas"),

recursive=True

)

## **11.4 Valores predeterminados**

La aplicación podrá establecer:

recursive = False

como comportamiento predeterminado, salvo que el PRD establezca posteriormente otro valor.

Los destinos internos serán:

Verticales/

Horizontales/

Cuadradas/

# **12\. Relaciones entre modelos**

Las relaciones principales son:

AppSettings

│

▼

Photo

│

▼

PhotoMetadata

│

▼

Classification

│

▼

DestinationPath

│

▼

FileConflict ──► ConflictResolution

│

▼

ProcessingResult

Una forma más precisa de visualizar el flujo:

Photo

│

│ ImageReader

▼

PhotoMetadata

│

│ Classifier

▼

Classification

│

│ DestinationResolver

▼

DestinationPath

│

│ FileOperator

├──────────────► ProcessingResult

│

└── conflict ─► FileConflict

│

│ user decision

▼

ConflictResolution

│

▼

FileOperator

│

▼

ProcessingResult

# **13\. Reglas de dependencia**

Los modelos de dominio **no deben depender de los componentes que los consumen**.

Correcto:

Classifier

↓

Classification

Incorrecto:

Classification

↓

Classifier

La misma regla aplica a:

Photo

PhotoMetadata

DestinationPath

FileConflict

ProcessingResult

# **14\. Modelo de errores**

En V1 no se establece todavía un modelo complejo de errores de dominio.

Los errores deben diferenciarse conceptualmente de los resultados normales.

Por ejemplo:

COPIED

es un resultado.

Mientras que:

FAILED

representa una condición de procesamiento fallido.

Los detalles de:

- excepciones;
- errores recuperables;
- errores no recuperables;
- errores de lectura RAW;
- errores de filesystem;
- cancelación;

serán definidos posteriormente en el **Component Contract Specification** y en el **Application Workflow Contract**.

# **15\. Extensibilidad**

Los modelos se diseñan considerando funcionalidades futuras.

### **MOVE**

No requiere modificar:

Photo

PhotoMetadata

Classification

DestinationPath

El cambio principal estará en la abstracción de operación de archivos.

### **Nuevas clasificaciones**

Podrían agregarse posteriormente:

PANORAMIC

PORTRAIT

LANDSCAPE

sin modificar necesariamente el resto del flujo.

### **Nuevas estrategias de destino**

El modelo:

DestinationPath

permanece válido aunque los destinos futuros sean:

2026/

2026/09/

Nikon/

D5200/

RAW/

Verticales/

La modificación se concentra en DestinationResolver.

### **Nuevos formatos**

Agregar soporte para:

CR3

NEF

ARW

RAF

ORF

RW2

DNG

no requiere modificar los modelos de dominio.

La implementación correspondiente debe quedar encapsulada dentro de ImageReader.

# **16\. Contratos que quedan establecidos**

Con este documento quedan formalizados los siguientes modelos:

Photo

PhotoMetadata

Classification

DestinationPath

FileConflict

ConflictResolution

ProcessingResult

ProcessingStatus

AppSettings

Y quedan establecidas las siguientes responsabilidades:

| **Modelo** | **Responsabilidad** |
| --- | --- |
| Photo | Representar el archivo de origen |
| --- | --- |
| PhotoMetadata | Representar metadata técnica |
| --- | --- |
| Classification | Representar orientación/clasificación |
| --- | --- |
| DestinationPath | Representar destino calculado |
| --- | --- |
| FileConflict | Representar una colisión de destino |
| --- | --- |
| ConflictResolution | Representar la decisión frente al conflicto |
| --- | --- |
| ProcessingResult | Representar resultado individual |
| --- | --- |
| ProcessingStatus | Representar estado del procesamiento |
| --- | --- |
| AppSettings | Representar configuración de ejecución |
| --- | --- |

# **17\. Estado del contrato**

Este documento constituye la **especificación base de los modelos de dominio de PhotoSorter V1**.

A partir de este punto, los componentes deberán diseñarse para consumir y producir estos modelos mediante contratos explícitos.

El siguiente documento debe ser:

**Contract Specification — Component Contracts**

con los contratos formales de:

FileScanner

ImageReader

Classifier

DestinationResolver

FileOperator

y sus:

- inputs;
- outputs;
- precondiciones;
- postcondiciones;
- errores;
- responsabilidades;
- invariantes;
- ejemplos de implementación;
- criterios de testing.