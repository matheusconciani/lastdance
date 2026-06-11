import os
import re

# Get script and repository directory
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.dirname(script_dir)

compilados_dir = os.path.join(repo_dir, "compilados")

md_path = os.path.join(compilados_dir, "Curso_Gestao_Crises_IA_Completo.md")
html_path = os.path.join(compilados_dir, "Curso_Gestao_Crises_IA_Completo.html")

with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

html_content = []
html_content.append("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Guia de Estudos: Gestão de Crises com Sistema Preditivo em IA</title>
    <style>
        body {
            font-family: Georgia, serif;
            line-height: 1.6;
            margin: 20px;
            color: #111;
        }
        h1, h2, h3, h4 {
            font-family: "Helvetica Neue", Arial, sans-serif;
            color: #2c3e50;
        }
        h1 {
            border-bottom: 2px solid #34495e;
            padding-bottom: 10px;
            margin-top: 40px;
        }
        h2 {
            margin-top: 30px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }
        h3 {
            color: #7f8c8d;
            margin-top: 20px;
        }
        p {
            margin-bottom: 1.2em;
            text-align: justify;
        }
        .chapter {
            page-break-before: always;
        }
        .toc {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        .toc li {
            margin-bottom: 8px;
        }
        .toc a {
            text-decoration: none;
            color: #2980b9;
            font-weight: bold;
        }
        .toc a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
""")

html_content.append("<h1>Guia de Estudos: Gestão de Crises com Sistema Preditivo em IA</h1>")
html_content.append("<h2>Compilado para Kindle / Estudo</h2>")

# First, scan for chapters to build TOC
toc_entries = []
chapter_count = 0

chapter_pattern = re.compile(r"^#\s+(Capítulo\s+\d+:\s+.*)$")

for line in lines:
    match = chapter_pattern.match(line)
    if match:
        chapter_title = match.group(1).strip()
        chapter_count += 1
        anchor = f"chapter-{chapter_count}"
        toc_entries.append((chapter_title, anchor))

# Write TOC
html_content.append('<div class="toc">')
html_content.append('<h3>Índice</h3>')
html_content.append('<ul>')
for title, anchor in toc_entries:
    html_content.append(f'<li><a href="#{anchor}">{title}</a></li>')
html_content.append('</ul>')
html_content.append('</div>')

# Process content and convert basic MD to HTML
in_chapter = False
current_chapter_idx = 0

for line in lines:
    line_stripped = line.strip()
    if not line_stripped:
        continue
        
    chapter_match = chapter_pattern.match(line)
    if chapter_match:
        current_chapter_idx += 1
        anchor = f"chapter-{current_chapter_idx}"
        if in_chapter:
            html_content.append('</div><!-- end chapter -->\n')
        html_content.append(f'<div class="chapter" id="{anchor}">\n')
        html_content.append(f'<h1>{chapter_match.group(1).strip()}</h1>\n')
        in_chapter = True
        continue
        
    if line_stripped.startswith("## "):
        html_content.append(f'<h2>{line_stripped[3:]}</h2>\n')
    elif line_stripped.startswith("### "):
        html_content.append(f'<h3>{line_stripped[4:]}</h3>\n')
    elif line_stripped.startswith("#### "):
        html_content.append(f'<h4>{line_stripped[5:]}</h4>\n')
    else:
        txt = line_stripped
        txt = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', txt)
        txt = re.sub(r'\*(.*?)\*', r'<em>\1</em>', txt)
        html_content.append(f'<p>{txt}</p>\n')

if in_chapter:
    html_content.append('</div><!-- end chapter -->\n')

html_content.append("""
</body>
</html>
""")

with open(html_path, "w", encoding="utf-8") as f:
    f.writelines(html_content)

print(f"HTML version compiled successfully at: {html_path}")
