"""HTML back-end with the same drawing API as kit.py/deck.py (inches in, px out)."""
import html, re, math, json

PX = 96.0          # px per inch (slide = 13.333in x 7.5in = 1280 x 720)
PT = 4.0 / 3.0     # px per pt
MIN_PT = 13        # nothing on a slide is smaller than this
C = {}             # kept for API compatibility
PARTS = {
    0: ('Opening', 'Member 1', ''),
    1: ('Foundations & Transparency', 'Member 1', '00:00 – 18:00'),
    2: ('Fragmentation, Replication & Allocation', 'Member 2', '18:00 – 35:00'),
    3: ('Concurrency, Recovery & Commit', 'Member 3', '35:00 – 52:00'),
    4: ('Distributed Query Processing', 'Member 4', '52:00 – 67:00'),
    5: ('Types, Architectures & Catalogs', 'Member 5', '67:00 – 83:00'),
    6: ('Wrap-up & Q&A', 'All members', '83:00 – 90:00'),
}


def f(v):
    return f'{v * PX:.1f}px'


def fill_var(tok):
    return 'transparent' if tok is None else f'var(--f-{tok})'


def text_var(tok):
    return f'var(--t-{tok})'


TOKEN = re.compile(r'(\*\*.+?\*\*|__.+?__|~~.+?~~|``.+?``)')


def runs(t):
    out = []
    for part in TOKEN.split(t):
        if not part:
            continue
        if part.startswith('**'):
            out.append(f'<b>{html.escape(part[2:-2])}</b>')
        elif part.startswith('__'):
            out.append(f'<b style="color:{text_var("blue")}">{html.escape(part[2:-2])}</b>')
        elif part.startswith('~~'):
            out.append(f'<b style="color:{text_var("orange")}">{html.escape(part[2:-2])}</b>')
        elif part.startswith('``'):
            out.append(f'<code>{html.escape(part[2:-2])}</code>')
        else:
            out.append(html.escape(part))
    return ''.join(out).replace('\n', '<br>')


def paras_html(paras, size, color, bold, align, italic, font, gap, line_h=1.05):
    if isinstance(paras, str):
        paras = [paras]
    out = []
    for i, t in enumerate(paras):
        psize, pcolor = size, color
        if isinstance(t, tuple):
            t, psize, pcolor = (t + (None, None))[:3]
            psize = psize or size
            pcolor = pcolor or color
        psize = max(psize, MIN_PT)
        bullet = ''
        if t.startswith('• '):
            bullet = '<span class="dot"></span>'
            t = t[2:]
        st = [f'font-size:{psize * PT:.1f}px', f'color:{text_var(pcolor)}', f'text-align:{dict(l="left", c="center", r="right")[align]}',
              f'line-height:{1.2 * line_h:.2f}']
        if bold:
            st.append('font-weight:700')
        if italic:
            st.append('font-style:italic')
        if font == 'Consolas':
            st.append('font-family:var(--mono)')
        if i:
            st.append(f'margin-top:{size * gap * PT:.1f}px')
        out.append(f'<p style="{";".join(st)}">{bullet}{runs(t)}</p>')
    return ''.join(out)


class Slide:
    def __init__(self, kind='std'):
        self.items = []
        self.kind = kind
        self.cur_step = 0

    def add(self, s):
        if self.cur_step:
            s = re.sub(r'^<(div|svg|h2)', lambda m: f'<{m.group(1)} data-step="{self.cur_step}"', s, count=1)
        self.items.append(s)


def step(sl):
    """Everything drawn after this call appears on the next click."""
    sl.cur_step += 1


def _anchor(a):
    return dict(t='flex-start', m='center', b='flex-end')[a]


def text(sl, x, y, w, h, paras, size=18, color='body', bold=False, align='l', anchor='t',
         italic=False, font=None, gap=0.35, line=1.05):
    if paras == 'Distributed Database Concepts' and size == 54:
        w, size = 8.6, 50
    body = paras_html(paras, size, color, bold, align, italic, font, gap, line)
    sl.add(f'<div class="el tx" style="left:{f(x)};top:{f(y)};width:{f(w)};height:{f(h)};justify-content:{_anchor(anchor)};'
           f'padding:{f(0.02)} {f(0.04)}">{body}</div>')


def box(sl, x, y, w, h, paras='', fill='soft', line=None, size=16, color='ink', bold=False,
        align='c', anchor='m', shape='round', radius=0.12, lw=1.25, dash=False,
        pad=0.1, italic=False, font=None, gap=0.3, rot=0, extra=''):
    if w > 13 and h > 7 and fill == 'white':
        fill = 'bg'
    st = [f'left:{f(x)}', f'top:{f(y)}', f'width:{f(w)}', f'height:{f(h)}', f'background:{fill_var(fill)}',
          f'justify-content:{_anchor(anchor)}', f'padding:{f(0.04)} {f(pad)}']
    cls = ['el', 'bx'] + ([extra] if extra else [])
    if shape == 'round':
        st.append(f'border-radius:{radius * min(w, h) * PX:.1f}px')
    elif shape == 'oval':
        st.append('border-radius:50%')
    elif shape == 'chevron':
        d = h * 0.5 * PX
        st.append(f'clip-path:polygon(0 0,calc(100% - {d:.0f}px) 0,100% 50%,calc(100% - {d:.0f}px) 100%,0 100%,{d:.0f}px 50%)')
    elif shape == 'pent':
        d = h * 0.5 * PX
        st.append(f'clip-path:polygon(0 0,calc(100% - {d:.0f}px) 0,100% 50%,calc(100% - {d:.0f}px) 100%,0 100%)')
    if line is not None:
        st.append(f'border:{lw * PT:.1f}px {"dashed" if dash else "solid"} {text_var(line) if line != "white" else "var(--f-white)"}')
    if fill in ('white',) and shape in ('round', 'rect') and line is None:
        cls.append('card')
    body = paras_html(paras, size, color, bold, align, italic, font, gap) if paras != '' else ''
    sl.add(f'<div class="{" ".join(cls)}" style="{";".join(st)}">{body}</div>')
    return _Adj()


class _Adj:
    adjustments = [0]


def line(sl, x1, y1, x2, y2, color='faint', w=2, head='end', dash=False, flow=False):
    X1, Y1, X2, Y2 = x1 * PX, y1 * PX, x2 * PX, y2 * PX
    sw = w * PT
    c = text_var(color)
    heads = []
    ends = [] if not head else ([(X1, Y1, X2, Y2), (X2, Y2, X1, Y1)] if head == 'both' else [(X1, Y1, X2, Y2)])
    sx1, sy1, sx2, sy2 = X1, Y1, X2, Y2
    L = max(1e-6, math.hypot(X2 - X1, Y2 - Y1))
    hl = max(9.0, sw * 3.2)
    for (ax, ay, bx, by) in ends:
        ux, uy = (bx - ax) / L, (by - ay) / L
        px_, py_ = -uy, ux
        tip = (bx, by)
        base = (bx - ux * hl, by - uy * hl)
        hw = hl * 0.55
        pts = [tip, (base[0] + px_ * hw, base[1] + py_ * hw), (base[0] - px_ * hw, base[1] - py_ * hw)]
        heads.append('<polygon points="%s" fill="%s"/>' % (' '.join(f'{a:.1f},{b:.1f}' for a, b in pts), c))
        if (bx, by) == (X2, Y2):
            sx2, sy2 = bx - ux * hl * 0.8, by - uy * hl * 0.8
        else:
            sx1, sy1 = bx - ux * hl * 0.8, by - uy * hl * 0.8
    da = f' stroke-dasharray="{sw * 3:.1f} {sw * 2.2:.1f}"' if dash else ' pathLength="1"'
    cls = 'el ln' + ('' if dash else ' draw')
    pk = ''
    if flow:
        dur = max(1.2, L / 260)
        for k in range(2):
            pk += (f'<circle class="packet" r="{max(3.5, sw * 1.6):.1f}" fill="{text_var(flow if isinstance(flow, str) else "blue")}">'
                   f'<animateMotion dur="{dur:.2f}s" begin="{k * dur / 2:.2f}s" repeatCount="indefinite" '
                   f'path="M{X1:.1f},{Y1:.1f} L{X2:.1f},{Y2:.1f}"/></circle>')
    sl.add(f'<svg class="{cls}" viewBox="0 0 1280 720"><line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" '
           f'stroke="{c}" stroke-width="{sw:.1f}" stroke-linecap="round"{da}/>{"".join(heads)}{pk}</svg>')


def db(sl, x, y, w, h, label='', fill='blue_s', line_c='blue', size=14, color='blue_d', bold=True):
    W, H = w * PX, h * PX
    e = H * 0.18
    fv, lv = fill_var(fill), text_var(line_c)
    svg = (f'<svg width="{W:.1f}" height="{H:.1f}" viewBox="0 0 {W:.1f} {H:.1f}" style="position:absolute;inset:0;overflow:visible">'
           f'<path d="M1,{e / 2:.1f} L1,{H - e / 2:.1f} A{W / 2 - 1:.1f},{e / 2:.1f} 0 0 0 {W - 1:.1f},{H - e / 2:.1f} L{W - 1:.1f},{e / 2:.1f}" '
           f'fill="{fv}" stroke="{lv}" stroke-width="2"/>'
           f'<ellipse cx="{W / 2:.1f}" cy="{e / 2:.1f}" rx="{W / 2 - 1:.1f}" ry="{e / 2:.1f}" fill="var(--f-bg)" stroke="{lv}" stroke-width="2"/>'
           f'<ellipse cx="{W / 2:.1f}" cy="{e / 2:.1f}" rx="{W / 2 - 1:.1f}" ry="{e / 2:.1f}" fill="{fv}" stroke="{lv}" stroke-width="2"/></svg>')
    body = paras_html(label, size, color, bold, 'c', False, None, 0.3) if label else ''
    sl.add(f'<div class="el bx" style="left:{f(x)};top:{f(y)};width:{f(w)};height:{f(h)};justify-content:center;'
           f'padding:{f(e / PX)} 2px 0">{svg}<div style="position:relative">{body}</div></div>')
    return _Adj()


def grid(sl, x, y, colw, rows, rowh=0.42, size=14, header=True, hl=None, gapc='white',
         head_fill='blue', body_fill='soft', align='c', bold_first_col=False):
    hl = hl or {}
    yy = y
    for r, row in enumerate(rows):
        xx = x
        for c, cell in enumerate(row):
            w = colw[c]
            is_h = header and r == 0
            fill = head_fill if is_h else body_fill
            color = 'white' if is_h else 'ink'
            b = is_h or (bold_first_col and c == 0)
            if (r, c) in hl:
                v = hl[(r, c)]
                fill, color = (v if isinstance(v, tuple) else (v, color))
            box(sl, xx, yy, w - 0.03, rowh - 0.03, str(cell), fill=fill, size=size, color=color,
                bold=b, shape='rect', align=align, pad=0.06)
            xx += w
        yy += rowh
    return yy


def callout(sl, x, y, w, h, body, kind='analogy', size=16, label=None):
    fill, lc, lab = dict(analogy=('orange_s', 'orange', 'EVERYDAY ANALOGY'),
                         example=('blue_xs', 'blue', 'EXAMPLE'),
                         key=('green_s', 'green', 'KEY IDEA'),
                         warn=('red_s', 'red', 'WATCH OUT'),
                         note=('soft', 'muted', 'NOTE'))[kind]
    box(sl, x, y, w, h, fill=fill, shape='round', radius=0.06)
    box(sl, x, y + 0.12, 0.07, h - 0.24, fill=lc, shape='rect')
    text(sl, x + 0.25, y + 0.14, w - 0.4, 0.3, label or lab, size=11, color=lc, bold=True)
    text(sl, x + 0.25, y + 0.42, w - 0.4, h - 0.5, body, size=size, color='ink', gap=0.25)


def takeaway(sl, body, y=6.42):
    box(sl, 0.6, y, 12.13, 0.56, fill='blue_xs', shape='rect')
    box(sl, 0.6, y, 0.08, 0.56, fill='blue', shape='rect')
    text(sl, 0.85, y, 11.8, 0.56, body, size=17, color='ink', anchor='m')


def numdot(sl, x, y, n, d=0.48, fill='blue', size=18):
    return box(sl, x, y, d, d, str(n), fill=fill, shape='oval', size=size, color='white', bold=True, pad=0, extra='pop')


def bar(sl, x, y, w_max, value, vmax, h=0.42, fill='blue', label='', lsize=15, bold=False, lcolor='ink'):
    w = max(0.04, w_max * value / vmax)
    box(sl, x, y, w, h, fill=fill, shape='rect', extra='grow')
    if label:
        text(sl, x + w + 0.12, y, 4.5, h, label, size=lsize, anchor='m', bold=bold, color=lcolor)


def person(sl, x, y, s=0.5, fill='blue', label=None, lsize=12):
    box(sl, x + s * 0.3, y, s * 0.4, s * 0.4, fill=fill, shape='oval')
    box(sl, x + s * 0.1, y + s * 0.44, s * 0.8, s * 0.56, fill=fill, shape='round', radius=0.45)
    if label:
        text(sl, x - 0.5, y + s + 0.03, s + 1.0, 0.3, label, size=lsize, align='c', color='muted')


def server(sl, x, y, w=0.9, h=1.0, label='', fill='white', line_c='line', accent='blue', lsize=13):
    box(sl, x, y, w, h, fill=fill, line=line_c, shape='round', radius=0.1, lw=1.5)
    for i in range(3):
        box(sl, x + 0.12, y + 0.14 + i * (h - 0.25) / 3, w - 0.24, (h - 0.25) / 3 - 0.07,
            fill='soft', shape='round', radius=0.3)
        box(sl, x + w - 0.3, y + 0.14 + i * (h - 0.25) / 3 + ((h - 0.25) / 3 - 0.07) / 2 - 0.04,
            0.08, 0.08, fill=accent, shape='oval')
    if label:
        text(sl, x - 0.6, y + h + 0.04, w + 1.2, 0.35, label, size=lsize, align='c', color='ink', bold=True)


class Deck:
    def __init__(self):
        self.slides = []
        self.entries = []
        self.part = 0

    def _new(self, kind='std'):
        sl = Slide(kind)
        self.slides.append(sl)
        return sl

    def _record(self, sl, title, say, cue, kind='std'):
        n = len(self.entries) + 1
        self.entries.append(dict(n=n, part=self.part, title=title, say=say, cue=cue, kind=kind))
        sl.kind = kind
        sl.n, sl.title, sl.say, sl.cue, sl.part = n, title, say.strip(), cue, self.part
        return n

    def _footer(self, sl, n, dark=False):
        name, who, _ = PARTS[self.part]
        lab = (f'Part {self.part} · {who}' if 1 <= self.part <= 5 else '')
        sl.footer = (lab, n, dark)

    def slide(self, title, say, cue='', kicker=None, sec=None):
        sl = self._new()
        n = self._record(sl, title, say, cue)
        name, who, _ = PARTS[self.part]
        k = kicker or (f'PART {self.part} · {name.upper()}' if 1 <= self.part <= 5 else '')
        if sec:
            k += f'   ·   §{sec}'
        kcls = 'el kicker' + (' practice' if k.startswith('IN PRACTICE') else '')
        sl.add(f'<div class="{kcls}" style="left:{f(0.6)};top:{f(0.3)};width:{f(12)}">{html.escape(k)}</div>')
        sl.add(f'<h2 class="el title" style="left:{f(0.6)};top:{f(0.56)};width:{f(12.1)}">{runs(title)}</h2>')
        self._footer(sl, n)
        return sl

    def divider(self, part, learn, say, cue='Section opener.'):
        self.part = part
        name, who, when = PARTS[part]
        sl = self._new()
        n = self._record(sl, f'Part {part}: {name}', say, cue, kind='divider')
        sl.add(f'<div class="el divpanel" style="left:0;top:0;width:{f(4.9)};height:720px"></div>')
        text(sl, 0.7, 1.0, 3.8, 0.5, f'PART {part}', size=20, color='onaccent_soft', bold=True)
        sl.add(f'<div class="el bignum" style="left:{f(0.55)};top:{f(1.35)}">0{part}</div>')
        text(sl, 0.7, 5.4, 3.9, 0.9, [who, (when + '  ·  Chapter 23', 15, 'onaccent_soft')], size=22, color='white', bold=True, gap=0.2)
        text(sl, 5.6, 1.15, 7.1, 1.6, name, size=40, color='ink', bold=True, anchor='b')
        text(sl, 5.6, 3.05, 7, 0.4, 'IN THIS PART', size=13, color='blue', bold=True)
        y = 3.55
        for i, l in enumerate(learn):
            numdot(sl, 5.6, y, i + 1, d=0.42, size=15)
            text(sl, 6.2, y - 0.03, 6.9, 0.5, l, size=18, color='body', anchor='m')
            y += 0.66
        self._footer(sl, n, dark=True)
        return sl

    def quiz(self, tag, question, options, correct, why, say_q, say_a, code=None):
        letters = 'ABCD'
        for reveal in (False, True):
            sl = self._new()
            title = 'Quick check' + (' — answer' if reveal else '')
            n = self._record(sl, f'{title}: {tag}', say_a if reveal else say_q,
                             'Reveal slide: correct option turns green.' if reveal else
                             'Read the question aloud; give the audience 20–30 seconds.', kind='quiz')
            sl.add(f'<div class="el quizbar" style="left:0;top:0;width:1280px;height:{f(1.25)}"></div>')
            text(sl, 0.6, 0.25, 9, 0.35, f'QUICK CHECK  ·  PART {self.part}', size=13, color='onaccent_soft', bold=True)
            text(sl, 0.6, 0.55, 12, 0.6, tag, size=28, color='white', bold=True)
            qh = 1.1 if code is None else 0.9
            text(sl, 0.6, 1.5, 12.1, qh, question, size=19, color='ink')
            y0 = 1.5 + qh + 0.1
            if code:
                box(sl, 0.6, y0, 12.1, 0.55, code, fill='soft', font='Consolas', size=17, color='blue_d', shape='rect', align='l', pad=0.25)
                y0 += 0.75
            oh = 0.95 if not reveal else 0.85
            for i, o in enumerate(options):
                cx = 0.6 + (i % 2) * 6.15
                cy = y0 + (i // 2) * (oh + 0.18)
                ok = reveal and letters[i] == correct
                fill = 'green_s' if ok else ('soft' if not reveal else 'white')
                lc = 'green' if ok else ('line' if reveal else None)
                box(sl, cx, cy, 5.95, oh, fill=fill, line=lc, shape='round', radius=0.1, lw=2 if ok else 1)
                numdot(sl, cx + 0.2, cy + oh / 2 - 0.24, letters[i], fill='green' if ok else ('faint' if reveal else 'blue'))
                text(sl, cx + 0.85, cy, 4.95, oh, o, size=16, anchor='m', color='ink' if (ok or not reveal) else 'faint', bold=ok)
            if reveal:
                yy = y0 + 2 * (oh + 0.18) + 0.05
                callout(sl, 0.6, yy, 12.1, 6.85 - yy, why, kind='key', size=14, label=f'ANSWER: {correct}  —  WHY')
            self._footer(sl, n)

    # ------------------------------------------------------------------ output
    def save(self, path):
        total = len(self.slides)
        out = []
        for i, sl in enumerate(self.slides):
            lab, n, dark = getattr(sl, 'footer', ('', i + 1, False))
            items = []
            counters = {}
            for it in sl.items:
                m = re.match(r'<\w+ data-step="(\d+)"', it)
                st_ = int(m.group(1)) if m else 0
                k = counters.get(st_, 0); counters[st_] = k + 1
                d = (min(k, 24) * 0.018) if st_ == 0 else (min(k, 14) * 0.03)
                it = it.replace('class="el', f'style-i="{d:.3f}" class="el', 1)
                items.append(it)
            body = '\n'.join(items)
            body = re.sub(r'style-i="([0-9.]+)" class="([^"]*)" style="', r'class="\2" style="--d:\1s;', body)
            body = re.sub(r'style-i="([0-9.]+)" class="([^"]*)" viewBox', r'class="\2" style="--d:\1s" viewBox', body)
            foot = (f'<div class="foot{" dark" if dark else ""}"><span>Distributed Database Concepts · Chapter 23</span>'
                    f'<span>{html.escape(lab)}<b>{n}</b></span></div>')
            notes = html.escape(getattr(sl, 'say', ''))
            cue = html.escape(getattr(sl, 'cue', ''))
            out.append(f'<section class="slide k-{sl.kind}" data-steps="{sl.cur_step}" data-title="{html.escape(getattr(sl, "title", ""))}" id="s{n}">'
                       f'<div class="accent"></div>{body}{foot}'
                       f'<aside class="notes" data-cue="{cue}">{notes}</aside></section>')
        tpl = open(__file__.replace('htmldeck.py', 'template.html')).read()
        open(path, 'w').write(tpl.replace('<!--SLIDES-->', '\n'.join(out)).replace('{{TOTAL}}', str(total)))
