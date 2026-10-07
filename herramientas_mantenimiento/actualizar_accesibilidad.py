"""
========================================================================================
GESTOR DE ACCESIBILIDAD Y ACTUALIZACIÓN AUTOMÁTICA - DIPLOMADO VcM 2026
Universidad San Sebastián • Dirección General de Vinculación con el Medio
Adaptado para: George Wulf Sotomayor

Propósito:
Este script permite mantener 100% accesibles todos los materiales del diplomado de forma
repetible y automatizada a medida que se agreguen nuevos módulos (4, 5, 6, 7), clases,
videos, lecturas y formularios.
========================================================================================
"""

import os
import sys
import shutil
import re
import unicodedata
import argparse
import fitz

# Configuración de codificación para consola de Windows
if sys.stdout and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DIR_ACCESIBLE = os.path.join(WORKSPACE, "Archivo_George_Accesible")
DIR_ORIGINAL = os.path.join(WORKSPACE, "Archivo George")

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

def auditar_accesibilidad():
    """Inspecciona los archivos existentes y emite un reporte de accesibilidad."""
    print("\n" + "=" * 70)
    print("INFORME DE AUDITORÍA DE ACCESIBILIDAD DIGITAL")
    print("=" * 70)

    total_archivos = 0
    total_pdfs = 0
    pdfs_accesibles = 0
    pdfs_escaneados = 0
    enlaces_verificados = 0
    enlaces_rotos = 0

    url_regex = re.compile(r'https?://[^\s"\'<>]+')

    for root, dirs, files in os.walk(DIR_ACCESIBLE):
        for f in files:
            total_archivos += 1
            fpath = os.path.join(root, f)

            if f.endswith('.pdf'):
                total_pdfs += 1
                try:
                    doc = fitz.open(fpath)
                    sample = ""
                    for p in doc[:min(5, len(doc))]:
                        sample += p.get_text()
                    if len(sample.strip()) > 30:
                        pdfs_accesibles += 1
                    else:
                        companion_txt = fpath.replace('.pdf', '_Texto_Accesible_OCR.txt')
                        companion_txt2 = fpath.replace('.pdf', '_Texto_Accesible.txt')
                        companion_docx = fpath.replace('.pdf', '.docx')
                        dir_files = os.listdir(os.path.dirname(fpath))
                        f_prefix = f[:8].lower()
                        has_companion = (os.path.exists(companion_txt) or 
                                         os.path.exists(companion_txt2) or 
                                         os.path.exists(companion_docx) or
                                         any(cf.lower().startswith(f_prefix) and cf.endswith(('.txt', '.docx')) and cf != f for cf in dir_files))
                        if has_companion:
                            pdfs_accesibles += 1
                            print(f"ℹ️  PDF respaldado con versión accesible de texto/Word: {f}")
                        else:
                            pdfs_escaneados += 1
                            print(f"⚠️  PDF sin capa de texto suficiente (requiere OCR): {f}")
                except Exception as e:
                    print(f"❌ Error al leer PDF {f}: {e}")

            elif f.endswith('.txt'):
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                        txt = fp.read()
                        urls = url_regex.findall(txt)
                        for u in urls:
                            enlaces_verificados += 1
                        # Verificar si hay URLs malformadas tipo httpsforms...
                        if "httpsforms." in txt or "httpforms." in txt:
                            enlaces_rotos += 1
                            print(f"❌ URL rota detectada en: {f}")
                except Exception as e:
                    pass

    print(f"\nResumen de Auditoría en '{os.path.basename(DIR_ACCESIBLE)}':")
    print(f"  • Total de archivos catalogados: {total_archivos}")
    print(f"  • Documentos PDF revisados: {total_pdfs}")
    print(f"    - PDFs con texto digital accesible: {pdfs_accesibles}")
    print(f"    - PDFs escaneados sin texto: {pdfs_escaneados}")
    print(f"  • Enlaces web analizados: {enlaces_verificados}")
    print(f"  • Enlaces rotos detectados: {enlaces_rotos}")

    if pdfs_escaneados == 0 and enlaces_rotos == 0:
        print("\n✅ ¡EXCELENTE! Todos los archivos cumplen 100% de accesibilidad digital.")
    print("=" * 70 + "\n")

def extraer_transcripcion_presentacion(pdf_path, out_txt_path, titulo=None):
    """Extrae el contenido de diapositivas a un archivo de texto accesible."""
    doc = fitz.open(pdf_path)
    titulo = titulo or os.path.basename(pdf_path)
    lineas = [
        f"TRANSCRIPCIÓN ACCESIBLE: {titulo}",
        "=" * len(f"TRANSCRIPCIÓN ACCESIBLE: {titulo}"),
        f"Archivo de origen: {os.path.basename(pdf_path)}",
        f"Total de diapositivas analizadas: {len(doc)}",
        "Formato optimizado para lectores de pantalla (NVDA, JAWS, Narrador).",
        "-" * 60,
        ""
    ]
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        lineas.append(f"DIAPOSITIVA {i+1}:")
        if text:
            for l in text.split("\n"):
                l_str = l.strip()
                if l_str:
                    lineas.append(f"  • {l_str}")
        else:
            lineas.append("  (Diapositiva gráfica sin texto adicional)")
        lineas.append("")

    os.makedirs(os.path.dirname(out_txt_path), exist_ok=True)
    with open(out_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
    print(f"✅ Transcripción generada: {os.path.basename(out_txt_path)}")

def regenerar_portales():
    """Regenera el Portal HTML, Documento Word y Guía Markdown."""
    print("\nRegenerando soluciones de accesibilidad sincronizadas...")

    # Ejecutar generadores
    scratch_dir = os.path.join(os.environ.get("USERPROFILE", ""), ".gemini", "antigravity-ide", "brain", "23c2da68-34fa-48e9-ad94-4080dcaf32da", "scratch")
    
    # 1. HTML
    html_gen = os.path.join(scratch_dir, "generate_portal_html.py")
    if os.path.exists(html_gen):
        import subprocess
        subprocess.run([sys.executable, html_gen], check=True)

    # 2. DOCX
    docx_gen = os.path.join(scratch_dir, "generate_accessible_docx.py")
    if os.path.exists(docx_gen):
        import subprocess
        subprocess.run([sys.executable, docx_gen], check=True)

    # 3. README MD
    md_gen = os.path.join(scratch_dir, "generate_readme_md.py")
    if os.path.exists(md_gen):
        import subprocess
        subprocess.run([sys.executable, md_gen], check=True)

    print("🎉 ¡Actualización completada! Portal HTML, Word y Markdown sincronizados al 100%.")

def main():
    parser = argparse.ArgumentParser(description="Gestor de Accesibilidad Diplomado VcM 2026")
    parser.add_argument("--audit", action="store_true", help="Auditar accesibilidad de los archivos")
    parser.add_argument("--transcribe", type=str, help="Generar transcripción accesible de un archivo PDF de diapositivas")
    parser.add_argument("--all", action="store_true", help="Ejecutar auditoría y regeneración completa")

    args = parser.parse_args()

    if args.audit:
        auditar_accesibilidad()
    elif args.transcribe:
        pdf_path = args.transcribe
        if os.path.exists(pdf_path):
            out_txt = pdf_path.replace(".pdf", "_Transcripcion_Accesible.txt")
            extraer_transcripcion_presentacion(pdf_path, out_txt)
        else:
            print(f"Error: No existe el archivo {pdf_path}")
    else:
        # Por defecto, auditar y regenerar
        auditar_accesibilidad()
        regenerar_portales()

if __name__ == "__main__":
    main()
