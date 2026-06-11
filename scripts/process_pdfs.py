import os
import pypdf

# Get the directory where the script is located, then find the parent repository directory
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.dirname(script_dir)

originais_dir = os.path.join(repo_dir, "originais")
compilados_dir = os.path.join(repo_dir, "compilados")

# Ensure compilados directory exists
os.makedirs(compilados_dir, exist_ok=True)

pdf_files = sorted([f for f in os.listdir(originais_dir) if f.lower().endswith(".pdf") and f.startswith("cap")])

print(f"Found {len(pdf_files)} chapter PDFs in originais/:")
for f in pdf_files:
    print(" -", f)

# Merge PDFs
writer = pypdf.PdfWriter()
for pdf_file in pdf_files:
    full_path = os.path.join(originais_dir, pdf_file)
    reader = pypdf.PdfReader(full_path)
    print(f"Merging {pdf_file} ({len(reader.pages)} pages)...")
    for page in reader.pages:
        writer.add_page(page)

merged_pdf_path = os.path.join(compilados_dir, "Curso_Gestao_Crises_IA_Completo.pdf")
with open(merged_pdf_path, "wb") as output:
    writer.write(output)
print(f"\nMerged PDF created successfully at: {merged_pdf_path}")

# Extract texts and compile to Markdown
markdown_content = []
markdown_content.append("# Guia de Estudos: Gestão de Crises com Sistema Preditivo em IA\n")
markdown_content.append("## Compilado de Capítulos para o Kindle\n\n")

for pdf_file in pdf_files:
    full_path = os.path.join(originais_dir, pdf_file)
    reader = pypdf.PdfReader(full_path)
    
    # Get title from first page
    first_page_text = reader.pages[0].extract_text()
    lines = [line.strip() for line in first_page_text.split('\n') if line.strip()]
    title_candidate = "Capítulo: " + pdf_file
    if lines:
        cleaned_lines = [l for l in lines if "PDF exclusivo" not in l and "rm559473" not in l and "@outlook" not in l]
        if cleaned_lines:
            title_candidate = f"Capítulo {pdf_file.replace('cap', '').replace('.pdf', '')}: {cleaned_lines[0]}"
            if len(cleaned_lines) > 1 and len(cleaned_lines[0]) < 10:
                title_candidate += " - " + cleaned_lines[1]
                
    print(f"Extracting text for {title_candidate}...")
    markdown_content.append(f"\n# {title_candidate}\n\n")
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        clean_text_lines = []
        for line in text.split('\n'):
            if "PDF exclusivo para Matheus Conciani" in line or "msconciani@outlook.com" in line or "rm559473" in line:
                continue
            clean_text_lines.append(line)
        cleaned_text = '\n'.join(clean_text_lines).strip()
        
        markdown_content.append(f"### Página {page_num + 1}\n\n")
        markdown_content.append(cleaned_text + "\n\n")

merged_md_path = os.path.join(compilados_dir, "Curso_Gestao_Crises_IA_Completo.md")
with open(merged_md_path, "w", encoding="utf-8") as f:
    f.writelines(markdown_content)

print(f"Markdown content written successfully to: {merged_md_path}")
