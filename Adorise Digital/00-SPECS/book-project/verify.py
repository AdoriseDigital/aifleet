import zipfile
from PIL import Image
from PyPDF2 import PdfReader

epub_path = r'book-project\outputs\The-Solo-AI-Income-Engine.epub'
pdf_path = r'book-project\outputs\The-Solo-AI-Income-Engine.pdf'
cover_path = r'book-project\outputs\cover.jpg'

# EPUB
with zipfile.ZipFile(epub_path) as z:
    names = z.namelist()
    print('EPUB files:', len(names))
    print('  has cover:', any('cover' in n.lower() for n in names))
    print('  has nav  :', any('nav' in n.lower() for n in names))
    print('  has opf  :', any(n.endswith('.opf') for n in names))
    chapters = [n for n in names if 'chap_' in n.lower()]
    print('  chapters :', len(chapters))

# PDF
r = PdfReader(pdf_path)
print('PDF pages   :', len(r.pages))
print('PDF title   :', r.metadata.title)
print('PDF author  :', r.metadata.author)

# Cover
im = Image.open(cover_path)
print('Cover size  :', im.size, 'mode:', im.mode)
