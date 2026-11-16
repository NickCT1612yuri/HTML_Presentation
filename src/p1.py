from deck import *

CITIES = ['Chicago (HQ)', 'San Francisco', 'Los Angeles', 'New York', 'Atlanta']


def five_sites(sl, cx=6.66, cy=3.9, r=1.9, labels=None, w=1.9, h=0.62, fills=None, sub=None):
    """Hub-free 'network cloud' with five sites around it. Returns centres."""
    import math
    labels = labels or CITIES
    pts = []
    for i, lab in enumerate(labels):
        a = math.radians(-90 + i * 72)
        x, y = cx + r * 1.55 * math.cos(a), cy + r * math.sin(a)
        pts.append((x, y))
        line(sl, cx, cy, x, y, color='line', w=2.5, head=None)
    box(sl, cx - 1.25, cy - 0.45, 2.5, 0.9, 'network', fill='soft', line='line', shape='oval',
        size=14, color='muted')
    for i, (x, y) in enumerate(pts):
        f = (fills or {}).get(i, 'white')
        lc = 'blue' if f != 'white' else 'line'
        body = [labels[i]] + ([(sub[i], 12, 'muted')] if sub else [])
        box(sl, x - w / 2, y - h / 2, w, h, body, fill=f, line=lc, size=14, bold=True,
            color='ink', gap=0.05)
    return pts


def build(D):
    # ---------------- Title ----------------
    D.part = 0
    sl = D._new()
    D._record(sl, 'Title', say="""
Good morning everyone. Our group is presenting Chapter 23 of Elmasri and Navathe: Distributed Database Concepts.
Here is the one-sentence version of the whole chapter: a distributed database is one database whose data lives on many computers in different places, but which still feels like a single database to the people using it.
Over the next hour or so we will answer four simple questions. How do we split and place the data? How do we keep it correct when many sites update it at once? How do we answer queries cheaply when data is far away? And what kinds of distributed systems exist in practice?
This chapter is also the foundation for NoSQL in Chapter 24 and big data and cloud in Chapter 25.""",
                cue='Title slide. Smile, introduce the group, give the one-sentence summary.', kind='title')
    box(sl, 0, 0, 13.333, 7.5, fill='white', shape='rect')
    box(sl, 0, 0, 0.35, 7.5, fill='blue', shape='rect')
    text(sl, 1.0, 1.25, 8, 0.4, 'CHAPTER 23  ·  ELMASRI & NAVATHE, 7TH ED.', size=15, color='blue', bold=True)
    text(sl, 1.0, 1.75, 7.2, 2.2, 'Distributed Database Concepts', size=54, color='ink', bold=True)
    text(sl, 1.0, 4.05, 7.8, 1.0, 'One database. Many computers. It still feels like one.',
         size=22, color='muted')
    text(sl, 1.0, 5.9, 7, 0.4, 'Group presentation  ·  5 members  ·  ~90 minutes', size=15, color='body')
    # illustration: 4 sites + user
    cx, cy = 10.4, 3.7
    for (dx, dy) in [(-1.6, -1.6), (1.0, -1.6), (-1.6, 1.0), (1.0, 1.0)]:
        line(sl, cx, cy, cx + dx + 0.3, cy + dy + 0.3, color='line', w=2, head=None, flow=True)
    for (dx, dy) in [(-1.6, -1.6), (1.0, -1.6), (-1.6, 1.0), (1.0, 1.0)]:
        db(sl, cx + dx, cy + dy, 0.62, 0.72)
    box(sl, cx - 0.75, cy - 0.38, 1.5, 0.76, 'one view', fill='blue', size=16, color='white', bold=True)
    D._footer(sl, 1)

    # ---------------- Agenda ----------------
    sl = D.slide('Our roadmap', kicker='AGENDA', say="""
Here is our roadmap. There are five parts, one per presenter.
Part 1 explains what a distributed database is and what "transparency" means.
Part 2 is about design: how we cut tables into pieces called fragments, and where we put each piece and its copies.
Part 3 is about keeping data correct: locking, recovering from failures and committing a transaction on many sites at once.
Part 4 is about speed: how a query is answered when the data is spread out, and why the network is the expensive part.
Part 5 zooms out to the types and architectures of distributed systems, and how the system keeps track of where everything is.
In every part we use an everyday analogy, and we show where you meet the idea in real systems today.""",
                   cue='Point to each card as you name it.')
    items = [('Foundations & Transparency', 'What is a DDB? What does it hide from us?', '§23.1', 'Member 1'),
             ('Fragmentation & Replication', 'How do we split data and where do we put it?', '§23.2', 'Member 2'),
             ('Concurrency, Recovery & Commit', 'How do many sites stay correct together?', '§23.3–23.4', 'Member 3'),
             ('Distributed Query Processing', 'How do we answer queries cheaply?', '§23.5', 'Member 4'),
             ('Types, Architectures & Catalogs', 'What do real systems look like?', '§23.6–23.8', 'Member 5')]
    for i, (t, q, s, m) in enumerate(items):
        y = 1.65 + i * 0.92
        box(sl, 0.6, y, 12.13, 0.8, fill='soft', shape='round', radius=0.15)
        numdot(sl, 0.82, y + 0.15, i + 1, d=0.5)
        text(sl, 1.55, y + 0.05, 5.3, 0.7, t, size=20, color='ink', bold=True, anchor='m')
        text(sl, 6.6, y + 0.05, 4.4, 0.7, q, size=16, color='body', anchor='m')
        text(sl, 10.9, y + 0.05, 1.7, 0.7, [m, (s, 12, 'muted')], size=14, color='blue', bold=True,
             anchor='m', align='r', gap=0.05)
    text(sl, 0.6, 6.33, 12, 0.5, 'Every part: an everyday analogy + a real-world example  ·  Q&A at the end',
         size=15, color='muted')

    # ---------------- Hook ----------------
    sl = D.slide('Why not keep everything on one big server?', kicker='THE PROBLEM', say="""
Before definitions, let us feel the problem.
Imagine a company with offices in five cities, and all of its data sits on one server in Chicago. Look at the left side. [click]
Every time someone in Los Angeles opens a customer record, the request travels all the way to Chicago and back. That is slow.
If the Chicago server crashes, every office stops working at the same time. And when the company grows, that single machine becomes the bottleneck.
[click] Now look at the right side. Each office keeps the data it uses most, close to home. Requests are fast, one crash does not stop everyone, and we can grow by adding servers.
But the right side raises new questions: how do the offices stay consistent, and how does a user find data that lives somewhere else? That is exactly what this chapter answers.""",
                   cue='Contrast left (one server) vs right (data near each office).')
    # left: centralized
    text(sl, 0.6, 1.55, 5.8, 0.4, 'One central server', size=20, color='ink', bold=True)
    for (x, y, lab) in [(0.8, 2.2, 'LA'), (0.8, 4.3, 'NY'), (5.0, 2.2, 'SF'), (5.0, 4.3, 'ATL')]:
        line(sl, x + 0.35, y + 0.3, 3.4, 3.5, color='red_m', w=2, head=None, dash=True)
    db(sl, 2.85, 2.9, 1.1, 1.2, 'Chicago', size=13)
    for (x, y, lab) in [(0.8, 2.2, 'LA'), (0.8, 4.3, 'NY'), (5.0, 2.2, 'SF'), (5.0, 4.3, 'ATL')]:
        person(sl, x, y, 0.55, fill='faint')
        text(sl, x - 0.2, y + 0.58, 1, 0.3, lab, size=12, align='c', color='muted', bold=True)
    for i, t in enumerate(['Far away → slow', 'One crash → everyone stops', 'Hard to grow']):
        box(sl, 0.6 + i * 1.95, 5.35, 1.85, 0.75, t, fill='red_s', size=14, color='red', bold=True)
    # right: distributed
    step(sl)
    box(sl, 6.55, 1.55, 0.02, 4.6, fill='line', shape='rect')
    text(sl, 6.9, 1.55, 5.8, 0.4, 'Data close to each office', size=20, color='ink', bold=True)
    pos = [(7.2, 2.3, 'LA'), (7.2, 4.1, 'NY'), (11.2, 2.3, 'SF'), (11.2, 4.1, 'ATL'), (9.2, 3.2, 'CHI')]
    for (x, y, lab) in pos[:4]:
        line(sl, x + 0.5, y + 0.4, 9.7, 3.6, color='line', w=1.5, head=None, flow='green_m')
    for (x, y, lab) in pos:
        db(sl, x + 0.12, y, 0.75, 0.85, lab, size=12)
    for i, t in enumerate(['Fast local access', 'Failures stay local', 'Grow by adding sites']):
        box(sl, 6.9 + i * 1.95, 5.35, 1.85, 0.75, t, fill='green_s', size=14, color='green', bold=True)
    step(sl)
    takeaway(sl, 'New question: how do separate sites still behave like __one__ database?  →  Chapter 23')

    # ================= PART 1 =================
    D.divider(1, ['What a distributed database is', 'Transparency: what the system hides',
                  'Reliability, availability, scalability, autonomy', 'Why we bother: four advantages'],
              say="""
Thank you. I am Member 1 and I will cover the foundations, section 23.1.
By the end of my part you should be able to say what a distributed database is, name the kinds of transparency it gives users, and explain words like availability, scalability and autonomy that we will use for the rest of the talk.""")

    sl = D.slide('A distributed database in one picture', sec='23.1', say="""
Here is the definition in one picture.
A distributed database, or DDB, is a collection of multiple, logically related databases spread over a computer network. In the picture, three sites each hold part of the data.
The DDBMS — the distributed database management system — is the software that manages all of it and, importantly, makes the distribution transparent. The user at the top does not talk to Site 1 or Site 2. The user talks to one database.
So remember the two words: DDB is the data, DDBMS is the software that hides the distribution.
The chapter describes the technology as the combination of two worlds: database technology and distributed systems technology.""",
                   cue='Point at the user, then the single "one database" box, then the three sites.')
    person(sl, 2.2, 1.7, 0.7, label='User / application', lsize=13)
    line(sl, 2.55, 2.75, 2.55, 3.15, color='blue', w=2.5)
    box(sl, 0.9, 3.2, 3.3, 0.75, 'DDBMS: "one database"', fill='blue', color='white', size=17, bold=True)
    for i in range(3):
        x = 0.75 + i * 1.25
        line(sl, 2.55, 3.95, x + 0.4, 4.75, color='faint', w=1.8, flow=True)
        db(sl, x, 4.8, 0.8, 0.9, f'Site {i + 1}', size=12)
    text(sl, 0.6, 5.85, 4.2, 0.4, 'connected by a computer network', size=13, color='muted', align='c')
    box(sl, 5.3, 1.7, 7.4, 1.35, fill='soft')
    text(sl, 5.55, 1.8, 7, 1.2, ['__DDB__  (the data)',
                                 'A collection of multiple, **logically interrelated** databases distributed over a computer network.'],
         size=18, color='ink', gap=0.2)
    box(sl, 5.3, 3.2, 7.4, 1.35, fill='soft')
    text(sl, 5.55, 3.3, 7, 1.2, ['__DDBMS__  (the software)',
                                 'Manages the DDB and makes the distribution **transparent** (invisible) to users.'],
         size=18, color='ink', gap=0.2)
    box(sl, 5.3, 4.75, 3.3, 0.9, 'Database technology', fill='white', line='blue', size=16, color='blue_d', bold=True)
    text(sl, 8.6, 4.75, 0.5, 0.9, '+', size=28, color='muted', align='c', anchor='m', bold=True)
    box(sl, 9.1, 4.75, 3.6, 0.9, 'Distributed systems technology', fill='white', line='blue', size=16,
        color='blue_d', bold=True)
    takeaway(sl, 'DDB = the data spread over sites.  DDBMS = the software that makes it look like one.')

    sl = D.slide('The idea behind it: divide and conquer', sec='23.1', say="""
Where does the idea come from? From distributed computing in general.
Think about a big group assignment. Nobody can do the whole thing alone, so the team splits it: one person does research, one writes, one makes the slides. Each person works independently, but they coordinate so the final result is one report.
A distributed system does the same thing. Many processing sites, called nodes, are connected by a network. A big, unmanageable problem is split into smaller pieces, each node solves its piece, and the results are combined.
Each node is autonomous — it is managed on its own — but they cooperate on the shared task. Keep that word "autonomous" in mind; it comes back later.""",
                   cue='Tell the group-assignment story first, then map it to the diagram.')
    box(sl, 0.6, 2.2, 3.0, 1.6, 'One big,\nunmanageable task', fill='red_s', color='red', size=20, bold=True)
    line(sl, 3.75, 3.0, 4.75, 3.0, color='faint', w=3)
    for i, t in enumerate(['piece 1', 'piece 2', 'piece 3']):
        y = 1.75 + i * 0.95
        box(sl, 4.9, y, 1.7, 0.72, t, fill='blue_s', color='blue_d', size=16, bold=True)
        line(sl, 6.7, y + 0.36, 7.6, y + 0.36, color='faint', w=2)
        server(sl, 7.7, y - 0.05, 0.8, 0.82)
        line(sl, 8.6, y + 0.36, 9.6, 3.0, color='faint', w=2)
    text(sl, 7.0, 4.65, 2.3, 0.4, 'autonomous nodes', size=13, color='muted', align='c')
    box(sl, 9.75, 2.2, 3.0, 1.6, 'One combined\nresult', fill='green_s', color='green', size=20, bold=True)
    callout(sl, 0.6, 5.0, 12.13, 1.25,
            'A group assignment: split the work, each member works on their own part, then merge into one report.')

    sl = D.slide('Three conditions for calling it a DDB', sec='23.1.1', say="""
The book gives three minimum conditions.
One: the sites are connected by a computer network — a local network inside a building, or a wide-area network across countries.
Two: the data is logically interrelated. This is the condition people forget. Take a counter-example: all the websites on the internet are on a network, but their data has nothing to do with each other, so the internet is not a distributed database. A bank whose branches share one customer schema is.
Three: the sites do not have to be identical. One may run on Linux and another on Windows; they can even use different hardware or different DBMS software.
One small note at the bottom: the network topology — star, ring, mesh — affects performance and design, but not whether it is a DDB. Each site just needs some way to reach the others.""",
                   cue='Give the internet counter-example for condition 2.')
    cards = [('Connected by a network', 'LAN inside a building or WAN across cities.', 'Sites can send data and commands to each other.'),
             ('Logically related data', 'Data on different sites belongs to one design.',
              '✗ Random websites on the internet\n✓ Bank branches sharing one customer schema'),
             ('Not necessarily identical', 'Sites may differ in hardware, OS or DBMS.', 'e.g. one site on Linux + PostgreSQL, another on Windows + SQL Server')]
    for i, (t, d, e) in enumerate(cards):
        x = 0.6 + i * 4.1
        box(sl, x, 1.65, 3.9, 4.3, fill='soft', radius=0.06)
        numdot(sl, x + 0.3, 1.9, i + 1, d=0.6, size=22)
        text(sl, x + 0.3, 2.65, 3.4, 0.9, t, size=21, color='ink', bold=True)
        text(sl, x + 0.3, 3.45, 3.4, 0.9, d, size=16, color='body')
        box(sl, x + 0.25, 4.45, 3.4, 1.3, e, fill='white', size=14, color='body', align='l', anchor='m', pad=0.15)
    text(sl, 0.6, 6.2, 12.1, 0.6, '**Topology** (star, ring, mesh…) changes performance — not whether it is a DDB. Each site only needs to reach the others, directly or indirectly.',
         size=15, color='muted')

    sl = D.slide('Transparency = hiding the details', sec='23.1.2', say="""
The most important idea of Part 1 is transparency. Transparency means hiding implementation details from the user.
Think of shopping online. You click "buy", and the parcel arrives. You do not know — and you do not care — which warehouse it came from, or whether they split your order across two warehouses. The shop hides that from you.
[click] In a centralized database we already know one kind of transparency: data independence — you can change how data is stored without changing programs.
A distributed database adds more things to hide: where data is, how many copies exist, how tables were split. The more the system hides, the easier the developer's life — they barely need to know the details underneath.
On the next slides we look at each kind.""",
                   cue='Online-shop analogy, then preview the types.')
    person(sl, 0.9, 2.1, 0.75, label='Customer')
    box(sl, 2.1, 2.0, 2.6, 1.0, '"Buy"', fill='blue', color='white', size=22, bold=True)
    line(sl, 4.8, 2.5, 5.6, 2.5, color='faint', w=3)
    box(sl, 5.7, 1.65, 4.0, 1.75, fill='white', line='line', dash=True, radius=0.08)
    text(sl, 5.85, 1.7, 3.7, 0.35, 'hidden from the customer', size=12, color='muted', italic=True)
    for i, t in enumerate(['Warehouse A', 'Warehouse B', 'Warehouse C']):
        box(sl, 5.9 + i * 1.25, 2.15, 1.15, 1.05, t, fill='soft', size=13, color='body')
    line(sl, 9.8, 2.5, 10.6, 2.5, color='faint', w=3)
    box(sl, 10.7, 2.0, 2.0, 1.0, 'Parcel\narrives', fill='green_s', color='green', size=17, bold=True)
    step(sl)
    text(sl, 0.6, 3.95, 12, 0.4, 'A distributed DBMS hides…', size=18, color='ink', bold=True)
    hides = [('Location', 'where the data is'), ('Naming', 'the site in a name'),
             ('Replication', 'how many copies'), ('Fragmentation', 'how tables are split'),
             ('Design', 'how it was designed'), ('Execution', 'where it runs')]
    for i, (a, b) in enumerate(hides):
        x = 0.6 + i * 2.04
        box(sl, x, 4.5, 1.92, 1.25, [a, (b, 13, 'body')], fill='blue_xs', size=17, color='blue_d', bold=False, gap=0.15)
    takeaway(sl, 'Centralized DB hides storage (data independence). A DDB also hides **the network**.')

    sl = D.slide('Location & naming transparency', sec='23.1.2', say="""
The first group is called data organization transparency, also called distribution or network transparency. It has two parts.
Location transparency: the command you type does not depend on where the data is, or on which site you type it. Look at the code on the left. Without transparency, I have to write the server name and the site into my query — and if the DBA moves the table to another server, my program breaks.
[click] With location transparency, I just write SELECT from EMPLOYEE. The same query works from New York or from Los Angeles.
[click] Naming transparency means that once an object has a name, I can use that name unambiguously, without adding a site name to it. EMPLOYEE means the same table everywhere.""",
                   cue='Read both queries; stress that the right one keeps working if the table moves.')
    box(sl, 0.6, 1.7, 5.9, 0.5, '✗  Without transparency', fill='red_s', color='red', size=17, bold=True, shape='rect', align='l', pad=0.2)
    box(sl, 0.6, 2.2, 5.9, 1.4, 'SELECT * FROM\n  chicago_srv2.hr.EMPLOYEE\nWHERE Dno = 5;', fill='soft', font='Consolas',
        size=17, color='ink', shape='rect', align='l', pad=0.25)
    text(sl, 0.6, 3.7, 5.9, 0.8, 'Table moves to another server → the query breaks.', size=15, color='red')
    step(sl)
    box(sl, 6.83, 1.7, 5.9, 0.5, '✓  With transparency', fill='green_s', color='green', size=17, bold=True, shape='rect', align='l', pad=0.2)
    box(sl, 6.83, 2.2, 5.9, 1.4, 'SELECT * FROM\n  EMPLOYEE\nWHERE Dno = 5;', fill='soft', font='Consolas',
        size=17, color='ink', shape='rect', align='l', pad=0.25)
    text(sl, 6.83, 3.7, 5.9, 0.8, 'Same query from New York or LA — still works.', size=15, color='green')
    step(sl)
    box(sl, 0.6, 4.55, 5.9, 1.55, [('__Location transparency__', 18), 'The command does not depend on **where the data is** or **where the command is issued**.'],
        fill='blue_xs', align='l', anchor='t', size=16, color='body', pad=0.25, gap=0.2)
    box(sl, 6.83, 4.55, 5.9, 1.55, [('__Naming transparency__', 18), 'A name refers to one object everywhere — **no site prefix** needed.'],
        fill='blue_xs', align='l', anchor='t', size=16, color='body', pad=0.25, gap=0.2)

    sl = D.slide('Our running example: one company, five sites', sec='Fig. 23.1', say="""
Let us meet the example the textbook uses, and that we will come back to.
A company has five sites: headquarters in Chicago, and offices in San Francisco, Los Angeles, New York and Atlanta.
There are three tables: EMPLOYEE, PROJECT and WORKS_ON.
Chicago, the headquarters, keeps a copy of everything. Each office mostly keeps its own employees and its own projects — New York stores New York employees, Atlanta stores Atlanta employees.
Some data is stored in more than one place. For example, San Francisco also keeps the Los Angeles employees, and New York keeps all projects.
So this one picture already shows two big ideas: tables are split into pieces, and some pieces are copied to several sites. Next slide: the user should not see either of these.""",
                   cue='Walk around the five sites clockwise; point out the copies.')
    sub = ['EMP, PROJ, WORKS_ON: all', 'EMP: SF + LA · PROJ: SF', 'EMP: LA · PROJ: LA + SF',
           'EMP: NY · PROJ: all', 'EMP & PROJ: Atlanta']
    import math
    labels = ['Chicago (HQ)', 'San Francisco', 'Los Angeles', 'Atlanta', 'New York']
    sub = [sub[0], sub[1], sub[2], sub[4], sub[3]]
    five_sites(sl, cx=6.66, cy=3.95, r=1.85, labels=labels, w=2.8, h=0.85, sub=sub,
               fills={0: 'blue_s'})
    text(sl, 0.6, 6.4, 12.1, 0.45, 'Each office stores **its own** rows of WORKS_ON. Chicago (blue) holds a copy of everything.',
         size=15, color='muted', align='c')

    sl = D.slide('Replication & fragmentation transparency', sec='23.1.2', say="""
Now two more kinds of transparency, both visible in our example.
Replication transparency: copies of the same data are kept at several sites, for availability and speed. The user does not know the copies exist. In the picture, the New York projects are stored both in Chicago and in New York, but the user just sees PROJECT.
Fragmentation transparency: a table may be split into pieces. Horizontal fragmentation splits by rows — all New York employees here, all Atlanta employees there. This is also called sharding. Vertical fragmentation splits by columns.
[click] The user on the right writes a query against the whole EMPLOYEE table. The DDBMS finds the pieces, glues them together, and returns one table.
Analogy: a school with three campuses keeps three student lists, but the principal asks for "all students" and gets one list.""",
                   cue='Left: pieces on sites. Right: what the user sees.')
    text(sl, 0.6, 1.55, 6, 0.4, 'What is really stored', size=18, color='ink', bold=True)
    rows = [('New York', ['Ann', 'Bob']), ('Atlanta', ['Cid', 'Dee']), ('Los Angeles', ['Eve', 'Fay'])]
    for i, (site, names) in enumerate(rows):
        y = 2.05 + i * 1.25
        text(sl, 0.6, y + 0.3, 1.7, 0.4, site, size=15, color='muted', bold=True)
        grid(sl, 2.3, y, [1.4, 1.4], [['EMPLOYEE', 'city']] + [[n, {'New York':'NY','Atlanta':'ATL','Los Angeles':'LA'}[site]] for n in names], rowh=0.36,
             size=13, head_fill='faint')
    step(sl)
    line(sl, 5.6, 3.6, 7.1, 3.6, color='blue', w=4)
    text(sl, 5.4, 3.0, 1.9, 0.5, 'DDBMS\nglues', size=13, color='blue', bold=True, align='c')
    text(sl, 7.3, 1.55, 5.5, 0.4, 'What the user sees', size=18, color='ink', bold=True)
    box(sl, 7.3, 2.0, 5.4, 0.5, 'SELECT Name FROM EMPLOYEE;', fill='soft', font='Consolas', size=15,
        color='blue_d', shape='rect', align='l', pad=0.2)
    grid(sl, 8.3, 2.7, [1.7, 1.7], [['EMPLOYEE', 'city'], ['Ann', 'NY'], ['Bob', 'NY'], ['Cid', 'ATL'],
                                    ['Dee', 'ATL'], ['Eve', 'LA'], ['Fay', 'LA']], rowh=0.4, size=14)
    box(sl, 0.6, 5.85, 6.0, 0.95, [('__Replication__: copies at several sites; user never sees them.', 15)],
        fill='blue_xs', align='l', size=15, pad=0.2)
    box(sl, 6.73, 5.85, 6.0, 0.95, [('__Fragmentation__: rows (horizontal / sharding) or columns (vertical) split up; hidden.', 15)],
        fill='blue_xs', align='l', size=15, pad=0.2)

    sl = D.slide('Two more: design & execution transparency', sec='23.1.2', say="""
The last two types of transparency are short.
Design transparency: the user does not need to know how the distributed database was designed — which fragments exist, which copies exist, which site has what.
Execution transparency: the user does not need to know where a transaction actually runs. The DDBMS might run part of your query in Chicago and part in Atlanta.
A restaurant is a good picture. You order from the menu. You don't know the kitchen layout — that is design transparency — and you don't know which cook makes which dish — that is execution transparency.
So, in total: location, naming, replication, fragmentation, design and execution. And one honest note at the bottom: all this hiding has a cost. The system does extra work to hide things, and it should complement, not replace, the independence of local sites.""",
                   cue='Restaurant analogy; end on the trade-off line.')
    box(sl, 0.6, 1.7, 5.9, 2.2, fill='soft')
    text(sl, 0.9, 1.85, 5.4, 2.0, ['__Design transparency__', 'Freedom from knowing **how** the distributed database is designed (fragments, copies, placement).',
                                   ('Restaurant: you don\'t know the kitchen layout.', 15, 'orange')], size=17, gap=0.3)
    box(sl, 6.83, 1.7, 5.9, 2.2, fill='soft')
    text(sl, 7.13, 1.85, 5.4, 2.0, ['__Execution transparency__', 'Freedom from knowing **where** a transaction actually executes.',
                                    ('Restaurant: you don\'t know which cook made your dish.', 15, 'orange')], size=17, gap=0.3)
    text(sl, 0.6, 4.15, 12, 0.4, 'All six kinds, together', size=17, color='ink', bold=True)
    for i, t in enumerate(['Location', 'Naming', 'Replication', 'Fragmentation', 'Design', 'Execution']):
        box(sl, 0.6 + i * 2.04, 4.6, 1.92, 0.6, t, fill='blue', color='white', size=16, bold=True)
    callout(sl, 0.6, 5.45, 12.13, 1.2, 'Hiding costs **overhead**. Transparency should **complement**, not replace, local autonomy.',
            kind='warn', size=16, label='TRADE-OFF')

    sl = D.slide('Reliability vs. availability', sec='23.1.3', say="""
Now some system properties. First, two words that sound the same but are not: reliability and availability.
Think about an ATM. [click] Reliability asks: is the ATM working right now, at this moment? It is the probability the system is up at a certain point in time.
[click] Availability asks: was the ATM working the whole weekend, continuously? It is the probability the system stays available over a time interval.
On the timeline: reliability looks at a single point; availability looks at a whole stretch.
A real-world number: when a bank or a cloud provider promises "99.9 percent availability", that still allows about 8.8 hours of downtime per year; "99.99 percent" allows under an hour. That's why they replicate data across sites.
Distributed databases improve both, because if one site goes down the others keep working. In everyday writing people often use "availability" for both ideas, but the book separates them like this.""",
                   cue='Use the ATM: "right now" vs "all weekend".')
    text(sl, 0.6, 1.6, 12, 0.4, 'Timeline of one system', size=16, color='muted')
    segs = [(0.6, 3.2, 'green_m'), (3.8, 0.9, 'red_m'), (4.7, 4.2, 'green_m'), (8.9, 0.6, 'red_m'), (9.5, 3.23, 'green_m')]
    for x, w, f in segs:
        box(sl, x, 2.1, w, 0.45, fill=f, shape='rect')
    text(sl, 0.6, 2.6, 4, 0.3, 'up', size=12, color='green')
    text(sl, 3.8, 2.6, 1, 0.3, 'down', size=12, color='red')
    line(sl, 6.0, 1.75, 6.0, 2.1, color='blue', w=2.5)
    box(sl, 5.3, 1.25, 1.4, 0.45, 'instant t', fill='blue', size=13, color='white', bold=True)
    box(sl, 4.7, 2.95, 4.2, 0.2, fill='orange_m', shape='rect')
    text(sl, 4.7, 3.15, 4.2, 0.35, 'interval [t1, t2]', size=13, color='orange', bold=True, align='c')
    step(sl)
    box(sl, 0.6, 3.75, 5.9, 2.4, fill='blue_xs')
    text(sl, 0.9, 3.85, 5.4, 2.3, ['__Reliability__  — a point in time', 'Probability the system is **up at instant t**.',
                                   ('R(t) = P(up at t)', 17, 'blue_d'), ('ATM: "Is it working right now?"', 16, 'orange')], size=17, gap=0.3)
    step(sl)
    box(sl, 6.83, 3.75, 5.9, 2.4, fill='orange_s')
    text(sl, 7.13, 3.85, 5.4, 2.3, ['~~Availability~~  — a time interval', 'Probability the system is **continuously up** during an interval.',
                                    ('A = P(up throughout [t1, t2])', 17, 'orange'), ('ATM: "Did it work all weekend?"', 16, 'orange')], size=17, gap=0.3)
    takeaway(sl, 'Reliability = up **at a moment**.  Availability = up **for a period**.  (A "99.9%" service ≈ 8.8 h down per year.)')

    sl = D.slide('Fault → error → failure', sec='23.1.3', say="""
Why does a system go down? The book uses a chain of three words.
A fault is the cause — a defect. An error is a wrong internal state caused by that fault. A failure is when the behaviour the user sees is different from what was specified.
Cooking example: the recipe has a typo, "5 spoons of salt" instead of "1" — that is the fault. [click] The soup in the pot now has too much salt — that is the error, the wrong state. [click] The guests taste it and it's bad — that is the failure.
[click] There are two ways to deal with this. Fault tolerance accepts that faults will happen and detects and removes them before they become failures — for example, by keeping copies. Fault-free design tries to prevent faults through very careful design and testing, which is much stricter and more expensive.
In a DDB, recovery must handle transaction failures, hardware failures like losing memory or a disk, and network failures: messages that are lost, corrupted, or arrive out of order.""",
                   cue='Cooking story maps 1:1 onto the three boxes.')
    chain = [('Fault', 'the cause', 'Typo in the recipe: "5 spoons of salt"', 'red_s', 'red'),
             ('Error', 'a wrong internal state', 'Soup in the pot is too salty', 'orange_s', 'orange'),
             ('Failure', 'visible wrong behaviour', 'Guests taste it: dinner ruined', 'red_s', 'red')]
    for i, (a, b, c, f, lc) in enumerate(chain):
        if i:
            step(sl)
        x = 0.6 + i * 4.2
        box(sl, x, 1.7, 3.7, 1.1, [a, (b, 15, 'body')], fill=f, color=lc, size=24, bold=True, gap=0.1)
        box(sl, x, 2.95, 3.7, 0.85, c, fill='white', line='line', size=15, color='body', italic=True)
        if i < 2:
            line(sl, x + 3.75, 2.25, x + 4.15, 2.25, color='faint', w=3)
    step(sl)
    box(sl, 0.6, 4.1, 5.9, 1.45, [('__Fault tolerance__', 18), 'Faults will happen: detect and remove them **before** they cause a failure (e.g. keep copies).'],
        fill='blue_xs', align='l', anchor='t', size=16, pad=0.25, gap=0.2, color='body')
    box(sl, 6.83, 4.1, 5.9, 1.45, [('__Fault-free design__', 18), 'Prevent faults with exhaustive design, quality control and testing. Much stricter.'],
        fill='soft', align='l', anchor='t', size=16, pad=0.25, gap=0.2, color='body')
    text(sl, 0.6, 5.75, 12.1, 0.9, '**Recovery must handle:** transaction failures · hardware failures (memory or disk lost) · network failures (messages lost, corrupted or out of order).',
         size=15, color='muted')

    sl = D.slide('Scalability: grow out or grow up', sec='23.1.4', say="""
Scalability is how far the system can grow without its performance suffering.
There are two directions. Look at the supermarket picture. When the queue gets long, you can open more checkout lanes — that is horizontal scalability: add more nodes and move some of the data and the work onto them.
[click] Or you can give the single cashier a faster scanner — that is vertical scalability: make one node stronger, with more storage or more processing power.
Vertical scaling hits a ceiling — there is only so big one machine can get. Horizontal scaling is the natural strength of distributed databases, and it is the main idea behind NoSQL systems in the next chapter.""",
                   cue='Supermarket: more lanes vs faster cashier.')
    text(sl, 0.6, 1.6, 5.9, 0.4, 'Horizontal: add more nodes', size=20, color='blue', bold=True)
    for i in range(4):
        server(sl, 0.8 + i * 1.35, 2.3, 0.95, 1.15, accent='blue' if i < 2 else 'orange_m',
               line_c='line' if i < 2 else 'orange_m')
    text(sl, 3.4, 3.65, 2.6, 0.4, '+ new nodes', size=14, color='orange', bold=True, align='c')
    callout(sl, 0.6, 4.25, 5.9, 1.3, 'Open more checkout lanes.', size=16)
    step(sl)
    box(sl, 6.65, 1.6, 0.02, 4.0, fill='line', shape='rect')
    text(sl, 6.9, 1.6, 5.9, 0.4, 'Vertical: make one node bigger', size=20, color='blue', bold=True)
    server(sl, 7.4, 2.85, 0.75, 0.9)
    line(sl, 8.35, 3.0, 9.25, 3.0, color='faint', w=3)
    server(sl, 9.5, 2.1, 1.5, 1.85, accent='orange_m', line_c='orange_m')
    text(sl, 11.1, 2.6, 1.6, 0.9, 'more CPU,\nRAM, disk', size=14, color='orange', bold=True)
    callout(sl, 6.9, 4.25, 5.83, 1.3, 'Give the one cashier a faster scanner.', size=16)
    takeaway(sl, 'Vertical scaling hits a ceiling. Horizontal scaling is the DDB\'s strength (→ NoSQL, Ch. 24).', y=5.85)

    sl = D.slide('Partition tolerance: when the network splits', sec='23.1.4', say="""
In a distributed system the network itself can fail. When links between sites break, the sites can split into groups, called partitions. Sites inside one partition can still talk to each other, but not to sites in the other partition.
[click] Picture an island town during a storm. The bridge is closed, so the island is cut off from the mainland. But life on the island goes on: shops open, people buy bread. Then the bridge reopens and everything syncs up again.
Partition tolerance means the system can keep operating even while it is split like this. It is hard, and it is one of the main topics of NoSQL design in Chapter 24 — you may have heard of the CAP theorem.""",
                   cue='Point at the broken link; island-in-a-storm story.')
    for (x, y, l) in [(1.2, 2.0, 'A'), (2.9, 1.8, 'B'), (2.0, 3.6, 'C')]:
        server(sl, x, y, 0.85, 0.95, label=f'Site {l}')
    for (x, y, l) in [(8.7, 2.0, 'D'), (10.6, 2.5, 'E')]:
        server(sl, x, y, 0.85, 0.95, label=f'Site {l}')
    line(sl, 2.05, 2.5, 2.9, 2.3, color='green_m', w=2.5, head=None)
    line(sl, 1.6, 2.95, 2.3, 3.6, color='green_m', w=2.5, head=None)
    line(sl, 9.55, 2.5, 10.6, 2.9, color='green_m', w=2.5, head=None)
    line(sl, 3.85, 2.4, 5.8, 2.6, color='red_m', w=3, head=None, dash=True)
    line(sl, 6.6, 2.6, 8.7, 2.5, color='red_m', w=3, head=None, dash=True)
    box(sl, 5.7, 2.15, 1.0, 0.9, '✕', fill='red_s', color='red', size=30, bold=True, shape='oval')
    text(sl, 5.0, 3.1, 2.4, 0.4, 'link lost', size=14, color='red', bold=True, align='c')
    box(sl, 0.7, 1.4, 4.0, 3.75, fill=None, line='blue', dash=True, radius=0.1)
    text(sl, 0.85, 4.75, 3, 0.35, 'Partition 1', size=13, color='blue', bold=True)
    box(sl, 8.2, 1.4, 4.0, 3.75, fill=None, line='blue', dash=True, radius=0.1)
    text(sl, 8.35, 4.75, 3, 0.35, 'Partition 2', size=13, color='blue', bold=True)
    step(sl)
    callout(sl, 0.6, 5.4, 7.6, 1.3, 'A storm closes the bridge to an island town. The island keeps living on its own, then re-syncs when the bridge opens.', size=15)
    box(sl, 8.4, 5.4, 4.33, 1.3, 'Goal: keep operating **while partitioned**.', fill='blue_xs', size=17, color='ink')

    sl = D.slide('Autonomy: how independent is each site?', sec='23.1.5', say="""
Autonomy is how much each site — each local database — can operate independently. High autonomy means more flexibility and lets each site be maintained in its own way.
The book gives three dimensions. A restaurant franchise makes them easy to remember.
[click] Design autonomy: each restaurant can choose its own data model and its own transaction techniques — like choosing its own kitchen equipment and menu.
[click] Communication autonomy: each site decides what information it shares with other sites — like deciding what to report to headquarters.
[click] Execution autonomy: users at a site can act as they please locally — like running the daily operation without asking headquarters every time.
Remember these three; Member 5 will come back to them with federated databases.""",
                   cue='Franchise analogy: one card per dimension.')
    dims = [('Design autonomy', 'Choose its own data model and transaction techniques.', 'Own kitchen & menu'),
            ('Communication autonomy', 'Decide what information to share with other sites.', 'Decide what to report to HQ'),
            ('Execution autonomy', 'Users act as they please at their own site.', 'Run the day without asking HQ')]
    box(sl, 5.0, 1.6, 3.33, 0.8, 'Franchise HQ', fill='blue', color='white', size=18, bold=True)
    for i, (a, b, c) in enumerate(dims):
        step(sl)
        x = 0.6 + i * 4.1
        line(sl, 6.66, 2.4, x + 1.95, 2.95, color='faint', w=2, head=None)
        box(sl, x, 2.95, 3.9, 3.0, fill='soft', radius=0.06)
        text(sl, x + 0.2, 3.1, 3.6, 0.5, a, size=17, color='blue', bold=True)
        text(sl, x + 0.25, 3.65, 3.4, 1.2, b, size=16, color='body')
        box(sl, x + 0.25, 4.95, 3.4, 0.75, c, fill='orange_s', color='orange', size=15, bold=True)
    takeaway(sl, 'High autonomy = flexibility + local control. (Comes back in Part 5: federated systems.)')

    sl = D.slide('Four advantages of distributed databases', sec='23.1.6', say="""
So why go to all this trouble? Four advantages.
[click] One, easier application development. Because distribution is transparent, building and maintaining apps across many locations is easier.
[click] Two, higher availability. A fault stays at its own site, and the other sites keep running. If data was replicated before the failure, users may not notice anything at all. Surviving network partitions adds even more availability.
[click] Three, better performance. Data is kept close to where it is used — "data localization" — so there is less waiting on CPU, disk and the long-distance network. Each site has a smaller database and fewer transactions. And queries can run in parallel across sites.
[click] Four, easier expansion. Adding data, growing the database, or adding new sites is much easier than upgrading one central machine.
Before I hand over, let's see where you already meet these ideas in real life.""",
                   cue='Four icons; spend most time on availability and performance.')
    adv = [('Easier development', 'Distribution is transparent, so apps for many locations are easier to build and maintain.'),
           ('Higher availability', 'Failures stay at one site. With replicas, users may not notice at all.'),
           ('Better performance', 'Data close to its users · smaller local DBs · queries run in parallel across sites.'),
           ('Easier expansion', 'Add data or add sites without replacing one big machine.')]
    for i, (a, b) in enumerate(adv):
        step(sl)
        x = 0.6 + (i % 2) * 6.15
        y = 1.65 + (i // 2) * 2.35
        box(sl, x, y, 5.95, 2.15, fill='soft', radius=0.08)
        numdot(sl, x + 0.3, y + 0.3, i + 1, d=0.62, size=22)
        text(sl, x + 1.15, y + 0.3, 4.6, 0.6, a, size=22, color='ink', bold=True, anchor='m')
        text(sl, x + 1.15, y + 0.95, 4.6, 1.1, b, size=16, color='body')
    text(sl, 0.6, 6.4, 12, 0.4, 'Performance: inter-query and intra-query parallelism across sites.', size=14, color='muted')

    sl = D.slide('You already use distributed databases every day', kicker='IN PRACTICE · PART 1', say="""
These ideas are not just theory. You use distributed databases every day.
[click] Take a bank's ATM network. You opened your account in Hà Nội, but you withdraw cash in Đà Nẵng. The ATM does not know — and does not need to know — which data center holds your account row. That is location transparency, and the bank keeps copies so the ATM still works if one site is down.
[click] Now an online shop on a "11.11" flash-sale day. In a few minutes, orders jump many times above normal. The shop does not buy one giant computer for one day: it adds more servers for the peak. That is horizontal scalability.
[click] Finally, a chat app. Your messages are stored in more than one data center. If one data center has a problem, you can still read your old messages. That is replication giving availability.
So: transparency, scalability, replication — the three words from Part 1 — are exactly what these systems are selling.
That ends my part. Member 2 will now show how the data is actually cut into pieces and placed on sites.""",
                   cue='One card per click; ask the audience "who used an ATM this week?"')
    cases = [('Withdraw cash anywhere', 'Account opened in Hà Nội, cash withdrawn in Đà Nẵng. The ATM never asks where your account row is stored.', 'Location transparency + replicas'),
             ('A "11.11" flash sale', 'Orders jump many times above normal within minutes. The shop adds servers for the peak instead of one giant machine.', 'Horizontal scalability'),
             ('Chat messages never lost', 'Messages are copied to more than one data center. One has a problem — the app keeps working.', 'Replication → availability')]
    for i, (t, d, tag) in enumerate(cases):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 1.7, 3.9, 4.35, fill='white', radius=0.05)
        numdot(sl, x + 0.3, 1.95, i + 1, d=0.6, size=22, fill='orange_m')
        text(sl, x + 0.3, 2.75, 3.35, 0.9, t, size=21, color='ink', bold=True)
        text(sl, x + 0.3, 3.55, 3.35, 1.7, d, size=16, color='body')
        box(sl, x + 0.25, 5.2, 3.4, 0.6, tag, fill='blue_s', color='blue_d', size=15, bold=True)
    takeaway(sl, 'Transparency, scalability, replication: exactly what these services are built on.', y=6.3)
