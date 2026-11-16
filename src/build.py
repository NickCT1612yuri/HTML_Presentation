"""Rebuild the deck:  python build.py

Always builds ../Slides.html (needs only Python 3).
Also builds ../Script.docx if python-docx is installed, and the PDFs if Playwright is installed:
    pip install python-docx playwright && python -m playwright install chromium
"""
import os, sys, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import htmldeck
sys.modules['deck'] = htmldeck            # content files do `from deck import *`
import p1, p2, p3, p4, p5

D = htmldeck.Deck()
for m in (p1, p2, p3, p4, p5):
    m.build(D)
for e, sl in zip(D.entries, D.slides):
    e['steps'] = sl.cur_step
html_path = os.path.join(OUT, 'Slides.html')
D.save(html_path)
print(len(D.slides), 'slides ->', html_path)
try:
    from script_docx import build_docx
    build_docx(D, htmldeck.PARTS, os.path.join(OUT, 'Script.docx'))
except ImportError:
    print('python-docx not installed -> Script.docx not rebuilt')


async def pdfs():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for theme, name in (('light', 'Slides.pdf'), ('dark', 'Slides_dark.pdf')):
            pg = await b.new_page(viewport={'width': 1280, 'height': 720})
            await pg.goto('file://' + html_path)
            await pg.evaluate(f"document.documentElement.dataset.theme='{theme}'")
            await pg.wait_for_timeout(1500)
            await pg.pdf(path=os.path.join(OUT, name), width='1280px', height='720px', print_background=True, prefer_css_page_size=True)
            print('pdf ->', name)
        await b.close()

if '--no-pdf' not in sys.argv:
    try:
        import playwright  # noqa: F401
        asyncio.run(pdfs())
    except ImportError:
        print('Playwright not installed -> PDFs not rebuilt (open Slides.html in Chrome and press P instead)')
