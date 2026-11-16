"""Builds the presenter script (.docx) from the same slide content as the HTML deck."""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn as dqn
from docx.oxml import OxmlElement


def build_docx(D, PARTS, OUT):
    WPM = 130
    def words(s): return len(s.split())
    def mmss(sec): return f'{int(sec // 60)}:{int(sec % 60):02d}'

    doc = Document()
    st = doc.styles['Normal']; st.font.name = 'Arial'; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(dqn('w:eastAsia'), 'Arial')
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)
    BLUE = RGBColor(0x25, 0x63, 0xEB); INK = RGBColor(0x1E, 0x29, 0x3B); MUTED = RGBColor(0x64, 0x74, 0x8B); ORANGE = RGBColor(0xC2, 0x41, 0x0C)
    for name, size, color in (('Title', 26, INK), ('Heading 1', 18, BLUE), ('Heading 2', 13, INK)):
        h = doc.styles[name]; h.font.name = 'Arial'; h.font.size = Pt(size); h.font.color.rgb = color; h.font.bold = True

    def para(text, size=11, color=None, italic=False, bold=False, after=6):
        p = doc.add_paragraph()
        r = p.add_run(text); r.font.size = Pt(size); r.italic = italic; r.bold = bold
        if color: r.font.color.rgb = color
        p.paragraph_format.space_after = Pt(after)
        return p

    def shade(cell, hexfill):
        tcPr = cell._element.get_or_add_tcPr(); sh = OxmlElement('w:shd')
        sh.set(dqn('w:val'), 'clear'); sh.set(dqn('w:color'), 'auto'); sh.set(dqn('w:fill'), hexfill); tcPr.append(sh)

    doc.add_paragraph('Distributed Database Concepts', style='Title')
    para('Presentation script  ·  Chapter 23, Elmasri & Navathe (7th ed.)  ·  5 presenters  ·  ~90 minutes', 12, MUTED, after=14)

    doc.add_heading('How to use this script', level=1)
    for t in ['Every slide has three things: the slide number and title, an "On screen" cue (what to point at or do), and the words to say.',
              'The words are written to be spoken. You do not need to read them word for word: learn the flow, keep the examples, and say it in your own voice.',
              'The same text is in the speaker notes of Slides.html: press N for notes under the slide, or S for a presenter window with a timer.',
              'Times are estimates at a calm pace (~130 words per minute). Rehearse once with a timer.',
              'Many slides build step by step. [click] in the text marks where to press → (or click). The small dots at the bottom of the screen show how many parts of the slide are still hidden.',
              'Slides marked IN PRACTICE connect the theory to real systems (banks, online shops, Spark, Spanner…). Keep them lively — they are what the audience remembers.']:
        p = doc.add_paragraph(t, style='List Bullet'); p.paragraph_format.space_after = Pt(3)

    doc.add_heading('Timetable', level=1)
    rows = []
    for k in range(0, 7):
        es = [e for e in D.entries if e['part'] == k]
        if not es: continue
        sec = sum(words(e['say']) for e in es) / WPM * 60
        name, who, when = PARTS[k]
        rows.append((f'Part {k}: {name}' if 1 <= k <= 5 else name, who, f"{es[0]['n']}–{es[-1]['n']}", when or '—', mmss(sec)))
    # merge opening into part 1 row label
    t = doc.add_table(rows=1, cols=5); t.style = 'Table Grid'
    for i, h in enumerate(['Part', 'Presenter', 'Slides', 'Slot', 'Speaking time*']):
        c = t.rows[0].cells[i]; c.text = ''; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.color.rgb = RGBColor(255, 255, 255); shade(c, '2563EB')
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row): cells[i].text = v
    para('* Speaking time = script length only. Slots assume a normal pace (~140 words per minute). The Opening (slides 1–3) is part of Member 1\'s slot. Two recap slides are marked OPTIONAL — skip them if you are behind. Keep at least 5 minutes for Q&A.', 9, MUTED, italic=True, after=10)

    cur = None
    for e in D.entries:
        if e['part'] != cur:
            cur = e['part']
            name, who, when = PARTS[cur]
            doc.add_page_break() if cur != 0 else None
            title = f'Part {cur}: {name}' if 1 <= cur <= 5 else name
            doc.add_heading(title, level=1)
            if who: para(f'{who}' + (f'  ·  {when}' if when else ''), 11, MUTED, bold=True, after=10)
        sec = words(e['say']) / WPM * 60
        h = doc.add_heading(f"Slide {e['n']}  ·  {e['title']}", level=2)
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        r = p.add_run('On screen: '); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = ORANGE
        r = p.add_run(e['cue'] or '—'); r.italic = True; r.font.size = Pt(10); r.font.color.rgb = MUTED
        if e.get('steps'):
            r = p.add_run(f"   ·   {e['steps']} click{'s' if e['steps'] > 1 else ''}"); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = BLUE
        r = p.add_run(f'   ·   ~{mmss(sec)}'); r.font.size = Pt(10); r.font.color.rgb = MUTED
        for chunk in [c.strip() for c in e['say'].strip().split('\n') if c.strip()]:
            q = doc.add_paragraph(); q.paragraph_format.space_after = Pt(5)
            for k, seg in enumerate(chunk.split('[click]')):
                if k:
                    c = q.add_run('[click] '); c.bold = True; c.font.size = Pt(10); c.font.color.rgb = BLUE
                rr = q.add_run(seg.strip() + ' ' if seg.strip() else ''); rr.font.size = Pt(11); rr.font.color.rgb = INK
            q.paragraph_format.line_spacing = 1.15

    doc.add_page_break()
    doc.add_heading('Appendix A · Key terms in one line', level=1)
    gl = [('DDB / DDBMS', 'The data spread over sites / the software that manages it and hides the distribution.'),
          ('Transparency', 'Hiding details from users: location, naming, replication, fragmentation, design, execution.'),
          ('Reliability vs. availability', 'Up at a moment vs. up throughout a period.'),
          ('Horizontal fragment (shard)', 'A subset of rows: σ condition (R). Rebuild with UNION.'),
          ('Vertical fragment', 'A subset of columns, always including the primary key: π attributes (R). Rebuild with OUTER UNION / FULL OUTER JOIN.'),
          ('Mixed fragment', 'Rows then columns: π L (σ C (R)).'),
          ('Derived fragmentation', 'Fragment a table by its foreign key so it follows the fragments of the table it references.'),
          ('Full / partial / no replication', 'A copy at every site / some fragments copied / exactly one copy each.'),
          ('Distinguished copy', 'The one copy of an item that holds its locks (primary site, primary site + backup, primary copy).'),
          ('Election', 'Surviving sites choose a new coordinator by majority vote.'),
          ('Voting', 'No distinguished copy; a lock needs a majority of copies to grant it.'),
          ('2PC', 'Vote, then decide. Atomic, but participants block if the coordinator crashes.'),
          ('3PC', 'Vote, prepare-to-commit, commit. Survivors can finish; locks released on time-out.'),
          ('Semijoin', 'Ship only the join column, get back only matching rows. Good when few rows join.'),
          ('Guard', 'The condition every row in a fragment satisfies; used to route queries and updates.'),
          ('FDBS / multidatabase', 'Autonomous DBMSs with a shared global schema / with no global schema.'),
          ('Semantic heterogeneity', 'Same or related data with different meaning or interpretation in different components.'),
          ('GCS / LCS / LIS', 'Global conceptual schema / local conceptual schema / local internal schema.'),
          ('Export schema', 'The part of a component schema that it chooses to share with the federation.'),
          ('Birth site', 'The site where an object was created; in partially replicated catalogs, changes go there.')]
    t = doc.add_table(rows=0, cols=2); t.style = 'Table Grid'
    for a, b in gl:
        c = t.add_row().cells; c[0].text = ''; r = c[0].paragraphs[0].add_run(a); r.bold = True; c[1].text = b
        c[0].width = Cm(5); c[1].width = Cm(11.5)

    doc.add_heading('Appendix B · Likely questions in Q&A', level=1)
    qa = [('Is sharding the same as horizontal fragmentation?', 'Yes. Sharding is the NoSQL name for horizontal fragmentation; each shard is a horizontal fragment. (Member 2)'),
          ('Why keep the primary key in every vertical fragment?', 'Without it there is no way to match the columns back into the original rows. (Member 2)'),
          ('If replication is so good, why not replicate everything?', 'Every update must change every copy, and concurrency control and recovery become expensive. Replicate read-heavy data used at several sites; limit it for update-heavy data. (Member 2)'),
          ('Why is 3PC not used everywhere?', 'It costs an extra round of messages, and its guarantees rely on assumptions such as bounded time-outs. Many systems accept 2PC\'s rare blocking for lower cost. (Member 3)'),
          ('Is communication always the dominant cost?', 'On wide-area networks, usually yes. On a fast local network, CPU and I/O matter more, which is why the cost formula has weights. (Member 4)'),
          ('When is a semijoin a bad idea?', 'When almost every row joins (like query Q): you pay the extra step but filter out almost nothing. (Member 4)'),
          ('Federated vs. multidatabase — what is the real difference?', 'A federated system has a global schema shared by applications; a multidatabase has none and builds one per application. The book admits the line is not strict. (Member 5)'),
          ('Is a shared-nothing cluster a distributed database?', 'It looks similar, but its nodes are identical (symmetric, homogeneous), so the book classes it as a parallel database. (Member 5)')]
    for q, a in qa:
        p = para('Q: ' + q, 11, INK, bold=True, after=2)
        para('A: ' + a, 11, MUTED, after=8)

    doc.save(OUT)
    total = sum(words(e['say']) for e in D.entries)
    print(len(D.entries), 'slides;', total, 'words;', mmss(total / WPM * 60), 'speaking')
    for r in rows: print(r)

