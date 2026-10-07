# Guía Operativa para el Equipo Docente: Cómo Actualizar y Agregar Nuevos Materiales de Forma 100% Accesible

Este documento explica de forma clara y sencilla cómo mantener al día el repositorio accesible para **George Wulf Sotomayor** durante el desarrollo de los módulos restantes del diplomado (Módulos 4, 5, 6 y 7).

---

## 1. Dónde Colocar los Nuevos Archivos

Dentro de la carpeta `Archivo_George_Accesible/`, cada módulo cuenta con subcarpetas organizadas según el tipo de material:

```text
Archivo_George_Accesible/
├── Modulo 4 - Articulacion entre VcM y Generacion de Nuevo Conocimiento/
│   ├── bibliografia/            <- Nuevas lecturas y artículos en PDF
│   ├── grabaciones_sesiones/    <- Archivos .txt con los enlaces de YouTube
│   ├── material_estudio/        <- Guías de actividades, casos y talleres
│   └── presentaciones_clases/   <- PDFs de diapositivas y sus transcripciones
```

### Reglas de Oro de Accesibilidad al Guardar Archivos

1. **Nombres de archivo claros y descriptivos:**
   - ❌ **Evitar**: `1.txt`, `clase.pdf`, `Nuevo Documento de texto.txt`.
   - ✅ **Usar**: `Sesion_1_Clase_Sincronica_06_Octubre_YouTube.txt`, `01_Guia_Analisis_Casos.pdf`.
   - *Razón*: El lector de pantalla de George lee en voz alta el nombre del archivo. Un nombre claro le permite saber de inmediato qué contiene sin tener que abrirlo.

2. **Enlaces en archivos de texto (`.txt`):**
   - Para grabaciones de YouTube o formularios de Forms, guarde un archivo `.txt` que incluya:
     - Título claro del recurso.
     - Fecha y expositor.
     - La dirección web completa con `https://`.

3. **Presentaciones en diapositivas (PowerPoint / PDF):**
   - Cuando guarde un PDF de diapositivas, ejecute el generador de transcripciones (ver paso 2) para que George cuente con la versión en texto plano estructurada diapositiva por diapositiva.

4. **Documentos PDF (Lecturas y Papers):**
   - Asegúrese de que el PDF tenga texto digital seleccionable (no sea una foto o escaneo plano). Si es un escaneo, el sistema le avisará durante la auditoría.

---

## 2. Cómo Sincronizar el Portal Web y la Guía en Word

Cada vez que agregue nuevos archivos o enlaces, ejecute un solo comando en la terminal de PowerShell en la carpeta del diplomado:

```powershell
python actualizar_accesibilidad.py
```

### ¿Qué hace este comando automáticamente?

1. **Audita todos los archivos**: Revisa que todos los PDFs tengan texto y que no existan enlaces rotos.
2. **Regenera el Portal Web (`Portal_Accesible_George.html`)**: Añade los nuevos contenidos al buscador instantáneo y a la estructura accesible.
3. **Regenera la Guía en Word (`Guia_Accesible_Diplomado_VcM.docx`)**: Actualiza el índice formal en Word con enlaces y tablas accesibles.
4. **Regenera la Guía Markdown (`README_ACCESIBLE.md`)**.

---

## 3. Comandos Rápidos Adicionales

- **Solo auditar accesibilidad:**

  ```powershell
  python actualizar_accesibilidad.py --audit
  ```

- **Generar transcripción accesible de una presentación:**

  ```powershell
  python actualizar_accesibilidad.py --transcribe "ruta/a/la/presentacion.pdf"
  ```

---

## 4. Contacto y Soporte para George

Si George requiere asistencia directa con algún archivo o adaptación en audio, recuerde que todas las transcripciones en texto plano se encuentran disponibles en:
`Archivo_George_Accesible/transcripciones_accesibles/`.
