# **System Architecture Document (SAD)**

## **PhotoSorter — V1 Technical Architecture**

**Documento:** System Architecture Document  
**Proyecto:** PhotoSorter  
**Versión:** 1.0 — V1  
**Tipo de aplicación:** Desktop  
**Plataforma objetivo:** Windows  
**Lenguaje:** Python  
**Interfaz gráfica:** PySide6

# **1\. Propósito del documento**

Este documento describe la arquitectura técnica de **PhotoSorter**, una aplicación de escritorio orientada principalmente a fotógrafos.

El objetivo de PhotoSorter V1 es permitir que un usuario seleccione una carpeta que contenga fotografías y que la aplicación:

1.  Encuentre los archivos de imagen.
2.  Lea la información necesaria de cada fotografía.
3.  Determine su orientación.
4.  Clasifique cada fotografía como **Vertical, Horizontal o Cuadrada**.
5.  Determine el destino correspondiente.
6.  Copie las fotografías a las carpetas organizadas.
7.  Informe al usuario el progreso, errores y posibles conflictos.

La arquitectura está diseñada para ser **simple y liviana en V1**, pero manteniendo una separación clara entre responsabilidades para permitir futuras ampliaciones sin necesidad de reescribir la aplicación.

Este documento acompaña al diagrama de arquitectura de PhotoSorter y tiene como objetivo servir como material de:

- documentación;
- onboarding;
- estudio del proyecto;
- referencia durante el desarrollo;
- discusión de decisiones técnicas.

# **2\. Objetivos arquitectónicos**

La arquitectura de PhotoSorter se basa en los siguientes objetivos.

### **2.1. Simplicidad**

La aplicación debe ser suficientemente sencilla para poder desarrollarse, mantener y distribuir como una aplicación de escritorio independiente.

No se utilizarán tecnologías o patrones complejos cuando no aporten un beneficio real para V1.

### **2.2. Bajo acoplamiento**

Los componentes deben depender lo menos posible de las implementaciones concretas de otros componentes.

Por ejemplo:

SorterService

↓

ImageReader

y no:

SorterService

↓

Pillow

Esto permite reemplazar una implementación sin modificar el resto del sistema.

### **2.3. Separación de responsabilidades**

Cada componente debe tener una responsabilidad concreta.

Por ejemplo:

- Scanner encuentra archivos.
- Reader lee información.
- Classifier clasifica.
- DestinationResolver determina el destino.
- FileOperator realiza la operación.

Ninguno debería asumir las responsabilidades de los demás.

### **2.4. Extensibilidad**

La arquitectura debe permitir agregar funcionalidades futuras sin modificar innecesariamente componentes existentes.

Entre las funcionalidades potenciales se encuentran:

- mover archivos;
- nuevos formatos;
- nuevas reglas de clasificación;
- nuevos destinos;
- nomenclaturas personalizadas;
- clasificación por fecha;
- clasificación por cámara;
- clasificación mediante IA.

### **2.5. Seguridad de los archivos originales**

PhotoSorter V1 trabaja bajo el principio de que **los archivos originales no deben modificarse ni eliminarse**.

La operación principal de V1 será:

COPY

Las operaciones destructivas o potencialmente destructivas requerirán una decisión explícita del usuario.

# **3\. Principio arquitectónico general**

PhotoSorter no utiliza una arquitectura de microservicios.

Es una aplicación de escritorio monolítica, pero internamente está organizada en **componentes desacoplados y especializados**.

El concepto puede resumirse de la siguiente manera:

┌──────────────────────┐

│ User Interface │

└──────────┬───────────┘

│

▼

┌──────────────────────┐

│ Application Layer │

└──────────┬───────────┘

│

▼

┌──────────────────────┐

│ Domain Layer │

└──────────┬───────────┘

│

▼

┌──────────────────────┐

│ Infrastructure Layer │

└──────────────────────┘

Cada capa tiene una responsabilidad diferente.

# **4\. Capas de la arquitectura**

## **4.1. User Interface Layer**

La **User Interface Layer** representa el frontend de la aplicación.

La tecnología prevista para esta capa es **PySide6**.

Es la única parte del sistema que tiene como objetivo principal interactuar directamente con el usuario.

### **Responsabilidades**

La UI se ocupa de:

- seleccionar carpetas;
- mostrar configuraciones;
- iniciar el procesamiento;
- cancelar el procesamiento;
- mostrar progreso;
- mostrar errores;
- mostrar conflictos;
- solicitar decisiones al usuario;
- mostrar el resultado final.

### **La UI no debe encargarse de:**

- leer archivos RAW;
- determinar si una foto es vertical;
- copiar archivos;
- decidir la estructura de destino;
- implementar las reglas principales del negocio.

Por ejemplo, la UI puede recibir:

"DSC_0001.NEF es una fotografía vertical"

y mostrarlo al usuario.

Pero no debería ser la UI la que determine que:

height > width

significa vertical.

Esa decisión pertenece al dominio.

# **5\. Application Layer**

La **Application Layer** contiene el flujo de trabajo de la aplicación.

Su componente principal será:

SorterService

Este componente funciona como **orquestador**.

No realiza necesariamente cada tarea por sí mismo. Coordina los componentes especializados y determina el orden en el que deben trabajar.

## **5.1. Responsabilidades de SorterService**

El SorterService coordina un flujo similar a:

1\. Recibir configuración

2\. Solicitar archivos al Scanner

3\. Solicitar información al Reader

4\. Clasificar la fotografía

5\. Resolver el destino

6\. Ejecutar la operación de archivo

7\. Gestionar conflictos

8\. Registrar errores

9\. Informar progreso

10\. Finalizar el procesamiento

11\. Generar el resultado

Conceptualmente:

SorterService

│

┌────────────┼────────────┐

▼ ▼ ▼

Scanner Reader Classifier

│

▼

DestinationResolver

│

▼

FileOperator

El SorterService conoce el **flujo**, pero no necesita conocer los detalles internos de cada componente.

# **6\. Domain Layer**

La **Domain Layer** representa los conceptos, reglas y contratos propios de PhotoSorter.

Es el núcleo conceptual del sistema.

Esta capa debería ser independiente de tecnologías concretas siempre que sea posible.

Idealmente, el dominio no necesita saber si el programa está utilizando:

- Pillow;
- una librería RAW específica;
- PySide6;
- shutil;
- Windows API;
- otro mecanismo de filesystem.

El dominio define **qué necesita hacer el sistema**, mientras que Infrastructure define **cómo hacerlo técnicamente**.

# **7\. Models**

Los modelos representan los conceptos y datos que circulan dentro de la aplicación.

No representan necesariamente pasos del proceso, sino las entidades y resultados que el sistema necesita manejar.

## **7.1. Photo**

Representa una fotografía dentro del sistema.

Conceptualmente puede contener:

Photo

├── source_path

├── filename

├── extension

└── metadata

Ejemplo:

source_path:

C:\\Fotos\\CamaraA\\DSC_0001.NEF

filename:

DSC_0001.NEF

## **7.2. PhotoMetadata**

Representa la información obtenida del archivo.

Por ejemplo:

PhotoMetadata

├── width

├── height

├── orientation

└── format

Ejemplo:

width: 6048

height: 4024

format: NEF

El objetivo es que esta información tenga el mismo formato conceptual independientemente de si proviene de un JPEG, TIFF o RAW.

## **7.3. Classification**

Representa el resultado de una clasificación.

En V1:

VERTICAL

HORIZONTAL

SQUARE

Ejemplo:

PhotoMetadata

↓

OrientationClassifier

↓

VERTICAL

## **7.4. FileConflict**

Representa un conflicto detectado durante una operación.

Por ejemplo:

Source:

C:\\Fotos\\CameraB\\DSC_0001.NEF

Destination:

C:\\Fotos\\Verticales\\DSC_0001.NEF

si el archivo de destino ya existe.

El conflicto permite conservar la información necesaria para que la aplicación pueda solicitar una decisión al usuario.

## **7.5. ProcessingResult**

Representa el resultado global de una operación.

Podría contener información como:

Total: 1250

Processed: 1248

Errors: 2

Verticales: 530

Horizontales: 690

Cuadradas: 28

Este modelo permitirá que la UI muestre un resumen final sin tener que conocer cómo se realizó el procesamiento.

## **7.6. AppSettings**

Representa las opciones seleccionadas para una ejecución.

Por ejemplo:

AppSettings

├── source_folder

├── recursive

└── operation

En V1:

operation = COPY

Posteriormente podría existir:

operation = MOVE

sin necesidad de rediseñar todo el flujo.

# **8\. Interfaces**

En este contexto, **Interface no significa interfaz gráfica**.

Una interfaz es un **contrato** entre componentes.

Define qué puede hacer un componente sin especificar necesariamente cómo lo hace.

Por ejemplo:

ImageReader puede establecer conceptualmente:

"Cualquier componente que implemente ImageReader debe poder recibir un archivo de imagen y devolver la información necesaria sobre él."

La implementación concreta puede ser diferente.

ImageReader

▲

│

┌──────────┴──────────┐

│ │

▼ ▼

StandardImageReader RawImageReader

│ │

Pillow RAW Engine

El resto del sistema trabaja contra ImageReader, no directamente contra Pillow o el motor RAW.

## **8.1. ¿Por qué utilizar interfaces?**

Porque permiten sustituir implementaciones.

Por ejemplo, si actualmente:

RawImageReader

↓

RAW Library A

y posteriormente se decide utilizar:

RawImageReader

↓

RAW Library B

el resto del sistema puede permanecer igual.

El SorterService sigue trabajando con:

ImageReader

sin conocer qué librería concreta está detrás.

# **9\. Interfaces principales**

La arquitectura contempla inicialmente los siguientes contratos.

### **FileScanner**

Define la capacidad de buscar archivos.

Conceptualmente:

"Buscame los archivos que debo procesar."

### **ImageReader**

Define la capacidad de leer información de una imagen.

Archivo

↓

ImageReader

↓

PhotoMetadata

### **Classifier**

Define la capacidad de clasificar una fotografía.

PhotoMetadata

↓

Classifier

↓

Classification

### **DestinationResolver**

Define la capacidad de determinar dónde debe terminar un archivo.

Photo + Classification

↓

DestinationResolver

↓

Destination Path

### **FileOperator**

Define la operación que se realizará sobre el archivo.

En V1:

FileOperator

↓

CopyFileOperator

En el futuro:

FileOperator

├── CopyFileOperator

└── MoveFileOperator

# **10\. Infrastructure Layer**

La **Infrastructure Layer** contiene las implementaciones técnicas concretas necesarias para que la aplicación interactúe con el mundo exterior.

Mientras que Domain puede decir:

"Necesito leer una imagen."

Infrastructure implementa:

"Voy a utilizar esta librería para leerla."

Mientras Domain puede decir:

"Necesito copiar este archivo."

Infrastructure implementa:

"Voy a utilizar las herramientas de Python/Windows para copiarlo."

# **11\. Image Readers**

Los lectores de imágenes son responsables de obtener información de los archivos.

La arquitectura contempla dos grandes categorías.

ImageReader

│

┌─────────┴─────────┐

▼ ▼

StandardImageReader RawImageReader

## **StandardImageReader**

Procesará formatos de imagen convencionales.

Una posible implementación será mediante Pillow.

## **RawImageReader**

Procesará archivos RAW.

Este componente es especialmente importante porque PhotoSorter está orientado a fotógrafos y el soporte RAW forma parte de V1.

Los formatos concretos soportados dependerán de los resultados del **RAW Spike**.

El RAW Spike tendrá como objetivo evaluar:

- compatibilidad con distintas marcas;
- formatos RAW;
- lectura de dimensiones;
- orientación;
- rendimiento;
- archivos problemáticos;
- posibilidad de distribución dentro del .exe;
- licencia de las dependencias;
- compatibilidad con la futura estrategia open source del proyecto.

La arquitectura no debe quedar atada conceptualmente a una única librería RAW antes de realizar esta evaluación.

# **12\. Filesystem**

El sistema de archivos representa la interacción con el filesystem de Windows.

Dentro de esta responsabilidad existen diferentes operaciones.

## **Scanner**

Busca archivos.

Pregunta conceptual:

"¿Qué archivos existen dentro de esta carpeta?"

Puede trabajar con:

Recursividad = OFF

o:

Recursividad = ON

## **DestinationResolver**

Determina dónde debería terminar cada archivo.

Los destinos predeterminados de V1 serán:

Verticales/

Horizontales/

Cuadradas/

Por ejemplo:

Photo

↓

VERTICAL

↓

Verticales/

## **CopyFileOperator**

Realiza la operación de copia.

Origen

↓

COPY

↓

Destino

La V1 no moverá ni eliminará los originales.

# **13\. Recursividad**

La recursividad es una configuración del Scanner.

Ejemplo:

Fotos/

├── Camera A/

│ ├── DSC_001.NEF

│ └── DSC_002.NEF

│

└── Camera B/

└── DSC_003.NEF

Con recursividad activada, PhotoSorter puede analizar todos los niveles inferiores.

Sin embargo, la V1 no conservará necesariamente esa estructura en el destino.

Los archivos se organizarán en los destinos definidos:

Destino/

├── Verticales/

├── Horizontales/

└── Cuadradas/

Esto significa que archivos provenientes de diferentes subdirectorios pueden terminar en la misma carpeta.

# **14\. Manejo de conflictos**

Un conflicto ocurre cuando PhotoSorter intenta generar un archivo que ya existe en el destino.

Ejemplo:

Camera A/DSC_0001.NEF

Camera B/DSC_0001.NEF

ambos podrían intentar terminar en:

Verticales/DSC_0001.NEF

El sistema **no debe sobrescribir silenciosamente** el archivo existente.

El conflicto será representado mediante FileConflict.

El flujo será:

FileOperator

│

▼

FileConflict

│

▼

ConflictService

│

▼

UI

│

▼

User Decision

La UI deberá permitir al usuario tomar una decisión.

Entre las posibles acciones se encuentran:

- Omitir;
- Reemplazar;
- Renombrar;
- Cancelar.

La interfaz podrá mostrar las rutas completas de los archivos para ayudar al usuario a determinar si se trata de archivos provenientes de diferentes directorios o de una ejecución repetida sobre el mismo archivo.

También podrá existir una opción para aplicar una decisión a conflictos posteriores.

# **15\. Regla de seguridad**

La arquitectura adopta una regla explícita:

**Toda operación que pueda modificar, reemplazar, mover o eliminar archivos debe requerir una decisión explícita cuando exista riesgo de afectar archivos existentes.**

En V1 esto se traduce principalmente en:

- no modificar originales;
- no eliminar originales;
- no mover originales;
- no sobrescribir silenciosamente;
- solicitar decisión ante conflictos.

Esta regla deberá mantenerse como principio arquitectónico en futuras versiones.

# **16\. Flujo completo de V1**

El proceso completo puede representarse conceptualmente así:

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

▼

┌─────────────┐

│ Scanner │

└──────┬──────┘

│

▼

┌─────────────┐

│ ImageReader │

└──────┬──────┘

│

┌────────┴────────┐

▼ ▼

Standard RAW

Reader Reader

│ │

└────────┬────────┘

▼

PhotoMetadata

│

▼

OrientationClassifier

│

▼

Classification

│

▼

DestinationResolver

│

▼

FileOperator

│

▼

COPY FILE

│

▼

FILESYSTEM

# **17\. Concepto de responsabilidades**

Una manera sencilla de entender la arquitectura es asignar una pregunta a cada componente.

| **Componente** | **Pregunta que responde** |
| --- | --- |
| UI  | ¿Qué quiere hacer el usuario? |
| --- | --- |
| SorterService | ¿Qué pasos hay que ejecutar y en qué orden? |
| --- | --- |
| Scanner | ¿Qué archivos existen? |
| --- | --- |
| ImageReader | ¿Qué información tiene esta imagen? |
| --- | --- |
| Classifier | ¿A qué categoría pertenece? |
| --- | --- |
| DestinationResolver | ¿Dónde debería terminar? |
| --- | --- |
| FileOperator | ¿Qué operación hacemos con el archivo? |
| --- | --- |
| ConflictService | ¿Qué hacemos si existe un conflicto? |
| --- | --- |
| Models | ¿Qué información estamos manejando? |
| --- | --- |
| Interfaces | ¿Qué capacidades debe proporcionar cada componente? |
| --- | --- |
| Infrastructure | ¿Cómo implementamos técnicamente esas capacidades? |
| --- | --- |

Esta tabla constituye uno de los principales modelos mentales para comprender el sistema.

# **18\. Futuras extensiones**

La arquitectura contempla funcionalidades que no forman parte de V1 pero que pueden incorporarse posteriormente.

Estas funcionalidades se representan como **Futuro**.

"Futuro" significa:

**La arquitectura contempla dónde encajaría esta funcionalidad, pero todavía no forma parte de la implementación V1.**

Ejemplos:

Classifier

├── OrientationClassifier ← V1

├── DateClassifier ← Futuro

├── CameraClassifier ← Futuro

├── LensClassifier ← Futuro

└── AIClassifier ← Futuro

Y:

FileOperator

├── CopyFileOperator ← V1

└── MoveFileOperator ← Futuro

También podrían existir diferentes estrategias de destino:

DestinationResolver

├── DefaultDestinationResolver

├── DateBasedDestinationResolver

└── CustomDestinationResolver

La implementación de estas funcionalidades no forma parte del alcance actual.

# **19\. Ventaja de la arquitectura para futuras versiones**

La principal ventaja del diseño es que las futuras funcionalidades pueden incorporarse como nuevas implementaciones o componentes.

Por ejemplo, para agregar MOVE no debería ser necesario modificar:

Scanner

Reader

Classifier

PhotoMetadata

OrientationClassifier

El cambio estaría principalmente relacionado con:

FileOperator

↓

MoveFileOperator

De la misma forma, agregar una nueva estrategia de clasificación no debería requerir modificar el lector RAW.

Por ejemplo:

PhotoMetadata

↓

OrientationClassifier

podría coexistir posteriormente con:

PhotoMetadata

↓

DateClassifier

Esto permite que el crecimiento de la aplicación sea incremental.

# **20\. Threading y procesamiento en segundo plano**

La interfaz gráfica debe mantenerse responsiva durante el procesamiento.

Por este motivo, el trabajo de procesamiento no debería ejecutarse directamente en el hilo principal de la UI.

Conceptualmente:

Main Thread

│

└── UI

│

└── Worker

│

└── SorterService

El Worker ejecutará el procesamiento y comunicará eventos a la UI.

Entre ellos:

PROCESS_STARTED

FILE_STARTED

FILE_COMPLETED

PROGRESS_UPDATED

CONFLICT

ERROR

PROCESS_CANCELLED

PROCESS_FINISHED

La UI utiliza estos eventos para actualizar la información visual.

# **21\. Cancelación**

La cancelación será cooperativa.

El usuario podrá solicitar:

CANCEL

y el Worker comprobará periódicamente si debe detener el procesamiento.

No se buscará finalizar violentamente el thread, ya que una operación de filesystem podría encontrarse en progreso.

El objetivo es terminar el proceso de manera controlada.

# **22\. Logging**

PhotoSorter deberá contar con un sistema de logging interno.

El usuario final no necesariamente tendrá que interactuar directamente con los logs, pero serán importantes para diagnóstico y mantenimiento.

Ejemplo:

INFO Processing started

INFO Source: C:\\Fotos

INFO Recursive: true

INFO Files found: 1250

INFO DSC_0001.NEF → Verticales

INFO DSC_0002.JPG → Horizontales

ERROR IMG_0234.CR3 → Unable to read

INFO Processing completed

El logging permitirá investigar problemas sin tener que reproducir necesariamente todo el proceso manualmente.

# **23\. Testing**

La arquitectura debe permitir probar los componentes individualmente.

Ejemplos:

tests/

├── test_orientation_classifier.py

├── test_destination_resolver.py

├── test_scanner.py

├── test_conflicts.py

└── test_processing.py

El OrientationClassifier, por ejemplo, debería poder probarse sin utilizar la interfaz gráfica ni acceder al filesystem.

Ejemplos:

6000 × 4000 → HORIZONTAL

4000 × 6000 → VERTICAL

4000 × 4000 → SQUARE

Esto permite validar las reglas de negocio de manera independiente.

# **24\. Principios arquitectónicos de PhotoSorter**

La arquitectura completa puede resumirse en los siguientes principios:

1.  **La UI contiene presentación, no lógica de negocio.**
2.  **La Application Layer coordina el workflow.**
3.  **El Domain representa los conceptos y reglas de PhotoSorter.**
4.  **Los Models representan la información que circula por el sistema.**
5.  **Las Interfaces representan contratos entre componentes.**
6.  **Infrastructure contiene las implementaciones técnicas concretas.**
7.  **Los Readers leen información; no clasifican ni copian.**
8.  **El Classifier clasifica; no manipula archivos.**
9.  **DestinationResolver decide destinos; no realiza operaciones de filesystem.**
10. **FileOperator realiza operaciones; no decide la clasificación.**
11. **Los originales no se modifican en V1.**
12. **Los conflictos requieren una decisión explícita.**
13. **Las dependencias externas deben mantenerse reemplazables cuando sea razonable.**
14. **El soporte RAW debe ser evaluado mediante un spike técnico antes de fijar la implementación definitiva.**
15. **Las dependencias deben evaluarse también desde el punto de vista de licenciamiento.**
16. **Las funcionalidades futuras deben incorporarse preferentemente mediante nuevas implementaciones o componentes.**
17. **La aplicación debe mantenerse liviana y sin persistencia innecesaria en V1.**
18. **La arquitectura debe permitir que el proyecto evolucione sin convertirlo en una arquitectura innecesariamente compleja.**

# **25\. Resumen arquitectónico**

PhotoSorter V1 puede entenderse como una cadena de responsabilidades:

USER

│

▼

UI

│

▼

APPLICATION LAYER

│

SorterService

│

▼

DOMAIN LAYER

│

┌──────────────┼───────────────┐

▼ ▼ ▼

Scanner Reader Classifier

│

▼

DestinationResolver

│

▼

FileOperator

│

▼

INFRASTRUCTURE

│

┌────────────┴────────────┐

▼ ▼

Image Libraries Filesystem

La idea fundamental es que **cada componente haga una cosa y la haga bien**.

El sistema no está diseñado para que todos los componentes conozcan todos los detalles. Por el contrario, cada uno expone las capacidades que otros necesitan mediante contratos definidos en el dominio.

De esta manera, PhotoSorter puede comenzar como una aplicación relativamente pequeña, pero conservar una estructura suficientemente sólida para evolucionar hacia funcionalidades más avanzadas sin tener que reconstruir su arquitectura desde cero.

## **26\. Modelo mental final**

Para comprender PhotoSorter rápidamente, basta con recordar estas cinco preguntas:

1\. ¿QUÉ ARCHIVOS TENEMOS?

↓

Scanner

2\. ¿QUÉ SABEMOS DE CADA ARCHIVO?

↓

Reader

3\. ¿QUÉ TIPO DE FOTO ES?

↓

Classifier

4\. ¿DÓNDE DEBERÍA TERMINAR?

↓

DestinationResolver

5\. ¿QUÉ HACEMOS CON EL ARCHIVO?

↓

FileOperator

Y por encima de todo eso:

SorterService

│

coordina todo el proceso

│

▼

UI

muestra lo que ocurre

y recibe decisiones

Ese es el núcleo de la arquitectura de **PhotoSorter V1**.