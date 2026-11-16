from deck import *

EMP = [['Fname', 'Ssn', 'Salary', 'Dno'],
       ['John', '123456789', '30000', '5'],
       ['Franklin', '333445555', '40000', '5'],
       ['Alicia', '999887777', '25000', '4'],
       ['Jennifer', '987654321', '43000', '4'],
       ['Ramesh', '666884444', '38000', '5'],
       ['Joyce', '453453453', '25000', '5'],
       ['Ahmad', '987987987', '25000', '4'],
       ['James', '888665555', '55000', '1']]
DCOL = {'5': 'blue_s', '4': 'orange_s', '1': 'green_s'}


def build(D):
    D.divider(2, ['Cutting tables into fragments (rows, columns, both)', 'Rules a good fragmentation must follow',
                  'Replication and allocation: who stores what', 'A full worked example on the COMPANY database'],
              say="""
Thanks. I'm Member 2, and my part is distributed database design — section 23.2.
Member 1 told you the system hides fragments and copies. Now we open the box: how do we actually cut tables into fragments, how many copies do we keep, and on which site do we put each one? At the end we'll do the full textbook example on the COMPANY database.""")

    sl = D.slide('The design question: which site stores what?', sec='23.2', say="""
Every distributed design answers one question: which site stores which part of the database?
The simplest answer is to put whole tables on sites — EMPLOYEE in Chicago, PROJECT in New York. But usually it is better to cut tables into smaller pieces called fragments, so each site gets exactly the rows or columns it needs.
The design happens in steps, shown left to right. We start from the global schema — all tables, as if the database were central. [click] The fragmentation schema says how each table is cut into fragments. [click] The allocation schema says which site or sites each fragment goes to; if a fragment goes to more than one site, it is replicated. [click] Finally, the data sits on the physical sites.
[click] All this information is stored in a global directory, so the DDBMS — and not the user — knows where everything is.""",
                   cue='Read the pipeline left to right.')
    steps = [('Global schema', 'All tables, as if central'), ('Fragmentation schema', 'How each table is cut'),
             ('Allocation schema', 'Which site(s) get each fragment'), ('Sites', 'Where the copies physically live')]
    for i, (a, b) in enumerate(steps):
        if i:
            step(sl)
        x = 0.6 + i * 3.1
        box(sl, x, 1.8, 2.75, 1.6, [a, (b, 14, 'body')], fill='blue_s' if i < 3 else 'green_s',
            color='blue_d' if i < 3 else 'green', size=19, bold=True, gap=0.25)
        if i < 3:
            line(sl, x + 2.8, 2.6, x + 3.05, 2.6, color='faint', w=3)
    text(sl, 6.8, 3.45, 2.8, 0.35, '>1 site = replicated', size=13, color='orange', bold=True, align='c')
    step(sl)
    box(sl, 0.6, 4.1, 5.9, 2.0, fill='soft')
    text(sl, 0.9, 4.2, 5.4, 1.9, ['**Unit of distribution**', '• Simplest: a whole table at one site.',
                                  '• Usually better: cut tables into **fragments**.'], size=17, gap=0.3)
    callout(sl, 6.83, 4.1, 5.9, 2.0, 'All fragmentation, allocation and replication info lives in a **global directory** that the DDBMS consults.',
            kind='key', size=16)

    sl = D.slide('Three ways to cut a table', sec='23.2.1', say="""
There are three ways to cut a table. Look at the three pictures.
Horizontal fragmentation cuts by rows. Each fragment keeps all the columns but only some rows — for example, the employees of department 5 in one fragment, department 4 in another. It's like a teacher splitting the school list by class: same columns, different students.
[click] Vertical fragmentation cuts by columns. Each fragment keeps all the rows but only some columns — for example, personal details in one fragment and salary details in another. It's like keeping a student's contact sheet in the office and their grades sheet with the teacher.
[click] Mixed, or hybrid, fragmentation does both: first cut rows, then cut columns.
The next slides take each one in turn.""",
                   cue='Point at the coloured stripes in each mini-table.')
    def mini(x, y, mode):
        for r in range(6):
            for c in range(4):
                if mode == 'h':
                    f = 'blue_s' if r < 2 else ('orange_s' if r < 4 else 'green_s')
                elif mode == 'v':
                    f = 'blue_s' if c < 2 else 'orange_s'
                else:
                    f = ('blue_s' if c < 2 else 'blue') if r < 3 else ('orange_s' if c < 2 else 'orange_m')
                box(sl, x + c * 0.78, y + r * 0.4, 0.74, 0.36, fill=f, shape='rect')
    titles = [('Horizontal', 'cut by **rows**', 'Split a school list by class', 'h'),
              ('Vertical', 'cut by **columns**', 'Contact sheet vs. grades sheet', 'v'),
              ('Mixed (hybrid)', 'rows **and** columns', 'Both at once', 'm')]
    for i, (t, s, a, m) in enumerate(titles):
        if i:
            step(sl)
        x = 0.6 + i * 4.15
        text(sl, x, 1.6, 3.9, 0.5, t, size=24, color='ink', bold=True)
        text(sl, x, 2.1, 3.9, 0.4, s, size=17, color='body')
        mini(x + 0.35, 2.7, m)
        box(sl, x, 5.3, 3.85, 0.8, a, fill='orange_s', color='orange', size=15, bold=True)
    takeaway(sl, 'Every fragment must still let us rebuild the original table.')

    sl = D.slide('Horizontal fragmentation (sharding)', sec='23.2.1', say="""
Horizontal fragmentation. A horizontal fragment is a subset of the rows of a table. We define it with a selection condition — in relational algebra, sigma of C applied to R.
Here is EMPLOYEE, coloured by department number. [click] Fragment 1 is "Dno equals 5", the blue rows, which go to Site 2. [click] Fragment 2 is "Dno equals 4", the orange rows, going to Site 3. [click] Fragment 3 is "Dno equals 1", the green row, staying at Site 1.
Why do this? Because Site 2 is the department-5 office; its users mostly need department-5 employees. Each office gets its own rows.
[click] In the NoSQL world, horizontal fragmentation is called sharding, and each fragment is a shard. To get the full table back, we simply take the UNION of all fragments.""",
                   cue='Follow one colour from the table to its site.')
    hl = {}
    for r in range(1, len(EMP)):
        for c in range(4):
            hl[(r, c)] = DCOL[EMP[r][3]]
    grid(sl, 0.6, 1.7, [1.3, 1.5, 1.1, 0.8], EMP, rowh=0.47, size=14, hl=hl)
    frs = [('σ Dno=5 (EMPLOYEE)', 'Site 2', 'blue_s', 'blue'), ('σ Dno=4 (EMPLOYEE)', 'Site 3', 'orange_s', 'orange'),
           ('σ Dno=1 (EMPLOYEE)', 'Site 1', 'green_s', 'green')]
    for i, (f, s, fl, lc) in enumerate(frs):
        step(sl)
        y = 1.8 + i * 1.05
        line(sl, 5.5, y + 0.4, 6.1, y + 0.4, color='faint', w=2.5)
        box(sl, 6.2, y, 3.6, 0.8, f, fill=fl, color='ink', size=17, bold=True)
        line(sl, 9.85, y + 0.4, 10.5, y + 0.4, color='faint', w=2.5)
        server(sl, 10.6, y - 0.05, 0.75, 0.85)
        text(sl, 11.45, y + 0.15, 1.3, 0.5, s, size=16, color='ink', bold=True)
    step(sl)
    box(sl, 6.2, 5.0, 6.53, 1.15, [('Fragment = **σ condition (R)**  — a subset of rows', 17),
                                   ('Rebuild:  R = F1 ∪ F2 ∪ … ∪ Fn', 17, 'blue_d')], fill='blue_xs', align='l', pad=0.25, gap=0.2)
    text(sl, 0.6, 6.15, 5.4, 0.6, 'NoSQL name: **sharding**, each fragment is a **shard**.', size=16, color='muted')

    sl = D.slide('Complete and disjoint: the two checks', sec='23.2.1', say="""
A set of horizontal fragments should pass two checks.
Complete: every row of the table must land in at least one fragment. Mathematically, every tuple satisfies C1 or C2 or ... Cn. No row is lost.
Disjoint: no row lands in two fragments. No tuple satisfies two conditions at the same time.
[click] Look at the bad example on the right. Fragment A is "Salary greater than 50,000", fragment B is "Dno equals 4". Joyce earns 25,000 and is in department 5 — she is in neither fragment, so the set is not complete. And someone in department 4 earning 60,000 would be in both — so it is not disjoint either.
The good example on the left, splitting by Dno 5, 4 and 1, passes both checks — every employee belongs to exactly one department.""",
                   cue='Find Joyce in the bad example: she falls through the gaps.')
    box(sl, 0.6, 1.65, 5.9, 0.6, '✓  Good: Dno = 5 | Dno = 4 | Dno = 1', fill='green_s', color='green', size=18, bold=True, shape='rect', align='l', pad=0.25)
    for i, (lab, f) in enumerate([('Dno = 5', 'blue_s'), ('Dno = 4', 'orange_s'), ('Dno = 1', 'green_s')]):
        box(sl, 0.8 + i * 1.85, 2.55, 1.7, 1.2, lab, fill=f, size=17, color='ink', bold=True)
    text(sl, 0.6, 3.95, 5.9, 0.9, 'Each employee is in **exactly one** fragment.', size=17, color='green')
    step(sl)
    box(sl, 6.83, 1.65, 5.9, 0.6, '✗  Bad: Salary > 50000 | Dno = 4', fill='red_s', color='red', size=18, bold=True, shape='rect', align='l', pad=0.25)
    box(sl, 7.2, 2.45, 2.7, 1.5, 'A: Salary > 50000', fill='blue_s', shape='oval', size=15, color='ink', bold=True)
    box(sl, 9.3, 2.45, 2.7, 1.5, 'B: Dno = 4', fill='orange_s', shape='oval', size=15, color='ink', bold=True)
    text(sl, 6.83, 4.05, 5.9, 0.9, 'Joyce (25000, Dno 5) → in **neither**: not complete.\nDno 4 earning 60000 → in **both**: not disjoint.', size=15, color='red')
    step(sl)
    for i, (a, b) in enumerate([('Complete', 'Every row is in **some** fragment.  C1 ∨ C2 ∨ … ∨ Cn covers all rows.'),
                                ('Disjoint', 'No row is in **two** fragments.  Ci ∧ Cj is never true (i ≠ j).')]):
        x = 0.6 + i * 6.23
        box(sl, x, 5.05, 5.9, 1.2, [('__' + a + '__', 18), (b, 15)], fill='blue_xs', align='l', pad=0.25, gap=0.15)

    sl = D.slide('Derived horizontal fragmentation', sec='23.2.1', say="""
Here is a useful trick: derived horizontal fragmentation.
We fragment one primary table — DEPARTMENT, by department number. Then we let related tables follow it through their foreign keys. EMPLOYEE has Dno, PROJECT has Dnum — both point to a department. So all employees and projects of department 5 end up in the same place as department 5.
[click] Why? Because queries usually join these tables. If an employee row sits on the same site as its department row, the join happens locally and no data has to cross the network.
Think of moving house: you don't pack the kitchen into one truck and the cutlery into another. Things that are used together travel together.""",
                   cue='Follow the arrows: DEPARTMENT is split, the others follow via FK.')
    box(sl, 0.6, 1.8, 3.3, 1.0, 'DEPARTMENT\nsplit by Dnumber', fill='blue', color='white', size=17, bold=True)
    text(sl, 0.6, 2.85, 3.3, 0.4, 'primary relation', size=13, color='muted', align='c')
    line(sl, 1.2, 3.25, 1.2, 4.95, color='faint', w=2.5, head=None)
    for i, (t, fk) in enumerate([('EMPLOYEE', 'via Dno'), ('PROJECT', 'via Dnum')]):
        y = 3.35 + i * 1.15
        line(sl, 1.2, y + 0.45, 2.7, y + 0.45, color='faint', w=2.5)
        box(sl, 2.75, y, 2.6, 0.9, [t, (fk, 13, 'body')], fill='blue_s', color='blue_d', size=16, bold=True, gap=0.05)
    step(sl)
    text(sl, 5.9, 1.75, 6.8, 0.4, 'Result: everything about Dept 5 is together', size=18, color='ink', bold=True)
    for j, (d, f, site) in enumerate([('5', 'blue_s', 'Site 2'), ('4', 'orange_s', 'Site 3')]):
        x = 5.9 + j * 3.45
        box(sl, x, 2.3, 3.2, 2.6, fill=f, radius=0.06)
        text(sl, x + 0.2, 2.4, 2.8, 0.4, site, size=16, color='ink', bold=True)
        for k, t in enumerate([f'DEPARTMENT {d}', f'EMPLOYEEs of dept {d}', f'PROJECTs of dept {d}']):
            box(sl, x + 0.2, 2.9 + k * 0.62, 2.8, 0.52, t, fill='white', size=14, color='body')
    text(sl, 5.9, 5.0, 6.8, 0.5, 'Joins between them run **locally** — no network transfer.', size=16, color='green')
    callout(sl, 0.6, 5.6, 12.13, 0.95, 'Moving house: things used together (plates and cutlery) go in the same box.', size=16)

    sl = D.slide('Vertical fragmentation: cut by columns', sec='23.2.1', say="""
Vertical fragmentation cuts a table by columns. Each fragment is a projection: pi of a list of attributes, applied to R.
[click] Here we split EMPLOYEE into two fragments. L1 has the personal information: Ssn, name, birth date, address, sex. L2 has the work information: Ssn, salary, supervisor and department. Maybe HR uses L1 and payroll uses L2.
Notice that Ssn — the primary key — is in both fragments. That is essential. Without the key, we would have two piles of columns and no way to match them back together.
[click] To rebuild the table, we use the OUTER UNION of the fragments — or, equivalently, a FULL OUTER JOIN on Ssn.
The completeness rule for vertical fragmentation: together, the fragments must cover all attributes, and any two fragments should share only the primary key.""",
                   cue='Point at Ssn in both halves: "this is the glue".')
    cols = ['Ssn', 'Name', 'Bdate', 'Address', 'Sex', 'Salary', 'Super_ssn', 'Dno']
    for i, c in enumerate(cols):
        f = 'green_s' if c == 'Ssn' else ('blue_s' if i < 5 else 'orange_s')
        box(sl, 0.6 + i * 1.52, 1.7, 1.47, 0.55, c, fill=f, size=15, color='ink', bold=True, shape='rect')
    text(sl, 0.6, 2.3, 12, 0.4, 'EMPLOYEE (all columns)', size=13, color='muted')
    step(sl)
    line(sl, 3.4, 2.75, 3.0, 3.25, color='faint', w=2.5)
    line(sl, 9.2, 2.75, 9.6, 3.25, color='faint', w=2.5)
    for j, (lab, cs, f, who) in enumerate([('L1 — personal info', ['Ssn', 'Name', 'Bdate', 'Address', 'Sex'], 'blue_s', 'used by HR'),
                                           ('L2 — work info', ['Ssn', 'Salary', 'Super_ssn', 'Dno'], 'orange_s', 'used by payroll')]):
        x = 0.6 + j * 6.45
        text(sl, x, 3.3, 5.8, 0.4, f'**{lab}**  ·  {who}', size=17, color='ink')
        for i, c in enumerate(cs):
            box(sl, x + i * 1.16, 3.8, 1.12, 0.55, c, fill='green_s' if c == 'Ssn' else f, size=12, color='ink',
                bold=True, shape='rect')
    step(sl)
    box(sl, 0.6, 4.75, 5.9, 1.45, [('Fragment = **π attribute list (R)**', 17), ('Rebuild: OUTER UNION (or FULL OUTER JOIN on Ssn)', 15, 'blue_d')],
        fill='blue_xs', align='l', pad=0.25, gap=0.25)
    callout(sl, 6.83, 4.75, 5.9, 1.45, 'Keep the **primary key** (Ssn) in every fragment — it is the glue to rebuild rows.',
            kind='key', size=16)

    sl = D.slide('Mixed fragmentation: rows, then columns', sec='23.2.1', say="""
Mixed, or hybrid, fragmentation combines the two. First select rows, then project columns: pi of L, applied to sigma of C, of R.
The small table on the left is a nice way to see that all four cases are the same formula. If the condition C is TRUE — all rows — and L is not all attributes, it is vertical. If C is a real condition and L is all attributes, it is horizontal. If both are restricted, it is mixed. If C is TRUE and L is everything, the fragment is just the whole table.
[click] The grid on the right shows the textbook's example: three horizontal fragments of EMPLOYEE, by department, times two vertical fragments, personal and work, gives six mixed fragments.
To rebuild, we apply UNION and OUTER UNION in the right order.""",
                   cue='Use the C/L table: one formula covers every case.')
    text(sl, 0.6, 1.65, 6, 0.5, 'One formula:  F = π L ( σ C ( R ) )', size=22, color='blue_d', bold=True)
    rows = [['Condition C', 'Attributes L', 'Fragment type'], ['TRUE (all rows)', 'some columns', 'Vertical'],
            ['real condition', 'all columns', 'Horizontal'], ['real condition', 'some columns', 'Mixed'],
            ['TRUE (all rows)', 'all columns', 'Whole table']]
    grid(sl, 0.6, 2.35, [2.1, 2.0, 1.8], rows, rowh=0.62, size=15, hl={(3, 2): ('orange_s', 'orange')})
    step(sl)
    text(sl, 7.2, 1.7, 5.5, 0.5, 'Example: 3 × 2 = 6 fragments', size=18, color='ink', bold=True)
    text(sl, 8.6, 2.25, 2, 0.35, 'Personal', size=14, color='muted', align='c', bold=True)
    text(sl, 10.65, 2.25, 2, 0.35, 'Work', size=14, color='muted', align='c', bold=True)
    for r, (d, f) in enumerate([('Dno 5', 'blue_s'), ('Dno 4', 'orange_s'), ('Dno 1', 'green_s')]):
        y = 2.65 + r * 0.95
        text(sl, 7.2, y + 0.2, 1.3, 0.45, d, size=15, color='muted', bold=True)
        for c in range(2):
            box(sl, 8.6 + c * 2.05, y, 1.95, 0.85, f'F{r * 2 + c + 1}', fill=f, size=18, color='ink', bold=True, shape='rect')
    takeaway(sl, 'Rebuild with **UNION** (for the row cuts) and **OUTER UNION / OUTER JOIN** (for the column cuts).', y=5.75)

    sl = D.slide('Rules every fragmentation must follow', sec='23.2.1', say="""
Let's pull the rules together. A fragmentation schema is the set of fragments, and it must follow these rules.
Think of a jigsaw puzzle.
[click] Completeness: all the pieces must be there. Every attribute and every tuple of the database is in some fragment.
[click] Reconstruction: you must be able to put the puzzle back together. The whole database can be rebuilt using OUTER UNION or OUTER JOIN and UNION.
[click] Disjointness: pieces should not overlap. This one is useful but optional — the only allowed overlap is the repeated primary key in vertical or mixed fragments.
Then the allocation schema says where each fragment goes — and that leads us to replication.""",
                   cue='OPTIONAL — recap slide, skip if behind time. Jigsaw analogy: all pieces, re-assemblable, no overlap.')
    rules = [('Completeness', 'All pieces are there.', 'Every attribute and every tuple appears in some fragment.', 'blue'),
             ('Reconstruction', 'The puzzle can be re-assembled.', 'Rebuild the DB with UNION and OUTER UNION / OUTER JOIN.', 'blue'),
             ('Disjointness', 'Pieces don\'t overlap.', 'Useful, optional. Only the primary key may repeat (vertical / mixed).', 'muted')]
    for i, (t, a, b, c) in enumerate(rules):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 1.7, 3.9, 4.3, fill='soft', radius=0.06)
        numdot(sl, x + 0.3, 1.95, i + 1, d=0.6, size=22, fill=c)
        text(sl, x + 0.3, 2.7, 3.4, 0.5, t, size=23, color='ink', bold=True)
        box(sl, x + 0.25, 3.35, 3.4, 0.8, a, fill='orange_s', color='orange', size=16, bold=True)
        text(sl, x + 0.3, 4.35, 3.35, 1.5, b, size=16, color='body')
    text(sl, 0.6, 6.25, 12, 0.5, 'Disjointness is grey because it is **optional**.', size=15, color='muted')

    sl = D.slide('Replication: how many copies?', sec='23.2.2', say="""
Now replication: how many copies of each fragment do we keep? It's a spectrum.
[click] At one end, full replication: a copy of the whole database at every site. Reads are fast because every site can answer locally, and the system keeps running as long as one site is up. But every update must change every copy, and concurrency control and recovery get expensive.
[click] At the other end, no replication: each fragment is stored at exactly one site. This is called non-redundant allocation. Updates are cheap — there's only one copy — but if a site fails, its data is unavailable.
[click] In between is partial replication: some fragments copied, others not, anywhere from one to n copies. This is described by a replication schema.
Analogy: important documents. Full replication is a photocopy in every office. No replication is one original in one drawer.""",
                   cue='Left = many copies, right = one copy; partial in the middle.')
    cols3 = [('Full replication', 'copy at every site', [3, 3, 3], 'green_s',
              ['✓ Reads answered locally', '✓ Works while one site is up', '✗ Every update hits every copy']),
             ('Partial replication', '1 to n copies per fragment', [2, 1, 2], 'blue_xs',
              ['• Some fragments copied, others not', '• Described by a replication schema']),
             ('No replication', 'exactly one copy each', [1, 1, 1], 'orange_s',
              ['✓ Cheap updates', '✗ Site down → its data unavailable', '• Fragments must be disjoint'])]
    line(sl, 0.8, 1.75, 12.5, 1.75, color='faint', w=2.5, head='both')
    text(sl, 0.6, 1.25, 4, 0.4, 'more copies', size=13, color='muted')
    text(sl, 8.7, 1.25, 4, 0.4, 'fewer copies', size=13, color='muted', align='r')
    for i, (t, s, counts, f, pts) in enumerate(cols3):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 2.0, 3.9, 4.2, fill=f, radius=0.06)
        text(sl, x + 0.25, 2.1, 3.4, 0.5, t, size=21, color='ink', bold=True)
        text(sl, x + 0.25, 2.55, 3.4, 0.4, s, size=14, color='muted')
        for k, cnt in enumerate(counts):
            sx = x + 0.4 + k * 1.15
            server(sl, sx, 3.05, 0.7, 0.75, accent='blue')
            for m in range(cnt):
                box(sl, sx + 0.05 + m * 0.22, 3.9, 0.18, 0.25, fill='blue', shape='rect')
        text(sl, x + 0.25, 4.35, 3.45, 1.8, pts, size=15, color='body', gap=0.2)
    text(sl, 0.6, 6.35, 12, 0.5, 'Small blue blocks = copies of the data held by that site.', size=13, color='muted')

    sl = D.slide('Allocation: put data where it is used', sec='23.2.2', say="""
Choosing copies and sites is called data allocation. Each fragment, or each copy, is assigned to a site.
The choice follows the workload. Some rules of thumb from the book, one per click. If you need high availability, the transactions can be submitted anywhere and most of them only read — use full replication. If a fragment is used mostly at one site, store it at that site. If it is used at several sites, replicate it at those sites. But if there are many updates, limit replication, because every copy has to be updated.
[click] A special case is the mobile sales team: each salesperson carries a partial copy of the database on a laptop and synchronizes with the server from time to time.
Finding the truly optimal allocation is a complex optimization problem — in practice we use heuristics like these.""",
                   cue='Read the four rules as "if … then …".')
    rules = [('Need high availability, mostly reads, from any site', 'Full replication'),
             ('Fragment used mainly at one site', 'Store it at that site'),
             ('Fragment used at several sites', 'Replicate at those sites'),
             ('Many updates', 'Limit replication')]
    for i, (a, b) in enumerate(rules):
        step(sl)
        y = 1.7 + i * 0.9
        box(sl, 0.6, y, 6.4, 0.75, 'If: ' + a, fill='soft', size=17, color='body', align='l', pad=0.25)
        line(sl, 7.05, y + 0.37, 7.65, y + 0.37, color='faint', w=2.5)
        box(sl, 7.7, y, 5.03, 0.75, b, fill='blue', size=17, color='white', bold=True)
    step(sl)
    callout(sl, 0.6, 5.4, 7.6, 1.25, 'Mobile sales staff carry a **partial replica** on their laptops and sync it with the server periodically.',
            kind='example', size=15)
    box(sl, 8.4, 5.4, 4.33, 1.25, 'The optimal allocation is a hard optimization problem → use heuristics.',
        fill='soft', size=15, color='body')

    sl = D.slide('Worked example: distributing the COMPANY DB', sec='23.2.3', say="""
Let's put everything together with the textbook's example: the COMPANY database on three sites.
Site 1 is headquarters; it keeps the entire database — so everything at sites 2 and 3 is also a replica of something at site 1.
Site 2 is the office for department 5, Research. Site 3 is the office for department 4, Administration.
Four design steps, one per click. One: fragment DEPARTMENT horizontally by department number. Two: derive the fragments of EMPLOYEE, PROJECT and DEPT_LOCATIONS from it through their foreign keys. Three: for EMPLOYEE at the department sites, keep only some columns — name, Ssn, salary, supervisor and department number. Four: Site 1 keeps everything.
Next slide shows what Site 2 and Site 3 actually hold.""",
                   cue='Introduce the three sites, then the four steps.')
    sites = [('Site 1', 'Headquarters', 'Whole database', 'green_s'), ('Site 2', 'Dept 5 · Research', 'Dept 5 fragments', 'blue_s'),
             ('Site 3', 'Dept 4 · Administration', 'Dept 4 fragments', 'orange_s')]
    for i, (a, b, c, f) in enumerate(sites):
        x = 0.6 + i * 4.1
        box(sl, x, 1.7, 3.9, 1.6, fill=f, radius=0.08)
        server(sl, x + 0.25, 1.95, 0.8, 0.95)
        text(sl, x + 1.3, 1.85, 2.5, 1.3, [a, (b, 14, 'body'), (c, 14, 'muted')], size=20, color='ink', bold=True, gap=0.1)
    steps = ['Fragment **DEPARTMENT** horizontally by Dnumber.', 'Derive **EMPLOYEE, PROJECT, DEPT_LOCATIONS** from it via foreign keys.',
             'At sites 2 and 3, EMPLOYEE keeps only **Name, Ssn, Salary, Super_ssn, Dno**.', 'Site 1 holds everything → sites 2 and 3 hold **replicas**.']
    for i, s in enumerate(steps):
        step(sl)
        y = 3.6 + i * 0.68
        numdot(sl, 0.6, y, i + 1, d=0.48, size=16)
        text(sl, 1.25, y - 0.02, 11.3, 0.55, s, size=18, color='body', anchor='m')

    sl = D.slide('What sites 2 and 3 actually hold', sec='Fig. 23.2', say="""
Here is the result for EMPLOYEE, from Figure 23.2.
Site 2, department 5, holds EMPD_5: the four employees of department 5 — John Smith, Franklin Wong, Ramesh Narayan and Joyce English — with only the selected columns.
Site 3, department 4, holds EMPD_4: Alicia Zelaya, Jennifer Wallace and Ahmad Jabbar.
Below each table you can see the other fragments the site holds: its department row, its department locations, its projects and its WORKS_ON rows.
Notice this is horizontal plus vertical — mixed fragmentation — and all of it is also stored at headquarters.""",
                   cue='Read a couple of names; point at the list of other fragments.')
    E5 = [['Name', 'Ssn', 'Salary', 'Super_ssn', 'Dno'], ['John Smith', '123456789', '30000', '333445555', '5'],
          ['Franklin Wong', '333445555', '40000', '888665555', '5'], ['Ramesh Narayan', '666884444', '38000', '333445555', '5'],
          ['Joyce English', '453453453', '25000', '333445555', '5']]
    E4 = [['Name', 'Ssn', 'Salary', 'Super_ssn', 'Dno'], ['Alicia Zelaya', '999887777', '25000', '987654321', '4'],
          ['Jennifer Wallace', '987654321', '43000', '888665555', '4'], ['Ahmad Jabbar', '987987987', '25000', '987654321', '4']]
    for j, (t, rows, f, extra) in enumerate([('Site 2 · EMPD_5', E5, 'blue', 'Also: DEP_5 (Research) · DEP_5_LOCS · PROJS_5 (ProductX, Y, Z) · WORKS_ON_5'),
                                             ('Site 3 · EMPD_4', E4, 'orange_m', 'Also: DEP_4 (Administration) · DEP_4_LOCS · PROJS_4 (Computerization, Newbenefits) · WORKS_ON_4')]):
        x = 0.6 + j * 6.25
        text(sl, x, 1.6, 5.9, 0.45, t, size=19, color='ink', bold=True)
        grid(sl, x, 2.1, [1.75, 1.15, 0.85, 1.15, 0.6], rows, rowh=0.44, size=12, head_fill=f)
        text(sl, x, 4.45, 5.9, 0.9, extra, size=14, color='muted')
    takeaway(sl, 'Rows by department + only some columns = **mixed** fragmentation. Site 1 keeps a full copy.', y=5.7)

    sl = D.slide('The tricky table: WORKS_ON', sec='23.2.3', say="""
Now the tricky part. WORKS_ON connects employees to projects: Essn, Pno, Hours. It is a many-to-many relationship.
The problem: an employee in one department can work on a project controlled by a different department. Look at the example row: employee 333445555, Franklin Wong, is in department 5, but he works 10 hours on project 10, which belongs to department 4.
So where should this row go? Site 2, because the employee is there? Or Site 3, because the project is there? Both have a reason to want it.
[click] The textbook's solution is to fragment WORKS_ON twice: first by the employee's department, then by the project's controlling department. The condition looks like this: the employee condition C AND Pno IN the projects of department d.
Three departments times three departments gives nine fragments. Let's see them.""",
                   cue='Ask the audience: "Site 2 or Site 3?" before revealing the answer.')
    person(sl, 1.2, 2.1, 0.9, fill='blue', label='Franklin  ·  Dept 5', lsize=14)
    box(sl, 9.8, 2.1, 2.6, 1.0, 'Project 10\n(controlled by Dept 4)', fill='orange_s', color='orange', size=15, bold=True)
    line(sl, 2.3, 2.55, 9.7, 2.55, color='faint', w=3)
    box(sl, 3.9, 2.1, 4.4, 0.85, 'WORKS_ON ⟨333445555, 10, 10.0⟩', fill='soft', size=17, color='ink', bold=True, font='Consolas')
    box(sl, 1.0, 3.6, 3.6, 0.9, 'Site 2? (employee is there)', fill='blue_s', color='blue_d', size=16, bold=True)
    text(sl, 4.6, 3.6, 4.1, 0.9, 'or', size=22, color='muted', align='c', anchor='m')
    box(sl, 8.7, 3.6, 3.6, 0.9, 'Site 3? (project is there)', fill='orange_s', color='orange', size=16, bold=True)
    step(sl)
    box(sl, 0.6, 4.85, 12.13, 1.25, [('Fragment twice: by **employee\'s dept**, then by **project\'s dept**', 18),
                                     ('Ci = C  AND  Pno IN (SELECT Pnumber FROM PROJECT WHERE Dnum = d)', 15, 'blue_d')],
        fill='blue_xs', align='l', pad=0.3, gap=0.25)
    text(sl, 0.6, 6.25, 12, 0.5, '3 employee depts × 3 project depts = **9 fragments** (G1 … G9)', size=17, color='ink')

    sl = D.slide('Nine fragments of WORKS_ON', sec='Fig. 23.3', say="""
Here are the nine fragments as a three-by-three grid. Rows are the employee's department: 5, 4, 1. Columns are the project's department: 5, 4, 1.
G1 is "department-5 employees on department-5 projects" — the common case, seven rows. G2 is department-5 employees on department-4 projects — that's Franklin's row from the last slide, one tuple. G5 is department 4 on department 4, five rows.
Several fragments are empty — G4, G7, G8 — because in this data, nobody does that combination.
[click] Two ways to read the grid: a whole row, G1 union G2 union G3, is all the work done by department-5 staff. A whole column, G1 union G4 union G7, is all the work on department-5 projects.
Keep this grid in mind; the next slide uses it to decide where to put the fragments.""",
                   cue='Explain rows = employee dept, columns = project dept.')
    cells = [[('G1', '7 rows'), ('G2', '1 row'), ('G3', '1 row')], [('G4', 'empty'), ('G5', '5 rows'), ('G6', '1 row')],
             [('G7', 'empty'), ('G8', 'empty'), ('G9', '1 row')]]
    depts = ['5', '4', '1']
    text(sl, 3.3, 1.55, 6, 0.4, "Project's department →", size=15, color='muted', bold=True, align='c')
    for c in range(3):
        text(sl, 3.0 + c * 2.15, 1.95, 2.05, 0.4, f'Dept {depts[c]} projects', size=14, color='ink', bold=True, align='c')
    for r in range(3):
        text(sl, 0.6, 2.55 + r * 1.2, 2.3, 0.9, f"Dept {depts[r]}\nemployees", size=15, color='ink', bold=True, anchor='m', align='r')
        for c in range(3):
            g, n = cells[r][c]
            empty = n == 'empty'
            box(sl, 3.0 + c * 2.15, 2.4 + r * 1.2, 2.05, 1.1, [g, (n, 13, 'muted' if empty else 'body')],
                fill='white' if empty else 'blue_s', line='line' if empty else None, size=20,
                color='faint' if empty else 'blue_d', bold=True, gap=0.05)
    text(sl, 0.6, 3.6, 1.5, 0.5, '↓ employee\'s\ndepartment', size=12, color='muted')
    step(sl)
    box(sl, 9.7, 2.4, 3.03, 1.6, [('Row', 16, 'blue'), 'G1 ∪ G2 ∪ G3 = all work **by** Dept 5 staff'], fill='soft', size=14, align='l', anchor='t', pad=0.2, gap=0.15, color='body')
    box(sl, 9.7, 4.15, 3.03, 1.6, [('Column', 16, 'blue'), 'G1 ∪ G4 ∪ G7 = all work **on** Dept 5 projects'], fill='soft', size=14, align='l', anchor='t', pad=0.2, gap=0.15, color='body')
    text(sl, 0.6, 6.2, 12, 0.5, 'Example rows:  G1 ⟨123456789, 1, 32.5⟩ · G2 ⟨333445555, 10, 10.0⟩ · G9 ⟨888665555, 20, NULL⟩', size=14, color='muted')

    sl = D.slide('Allocating the nine fragments', sec='Fig. 23.3', say="""
Now allocation. Site 2, for department 5, takes its whole row — work by its staff — plus its whole column — work on its projects. So WORKS_ON_5 is G1, G2, G3, G4 and G7.
[click] Site 3, for department 4, does the same with row 4 and column 4: G4, G5, G6, G2 and G8.
[click] Look at the orange cells: G2 and G4 are stored at both sites. This is deliberate partial replication.
What do we gain? Every WORKS_ON row that joins with a local employee, or with a local project, is stored locally. So those joins can run with zero network transfer. We pay a little extra storage and update cost for G2 and G4, and in return we get local joins.
That is the core design trade-off of this whole section: replication buys locality and availability, at an update cost. Let's see that update cost in one concrete example.""",
                   cue='Trace the row and column for each site; orange = stored twice.')
    def g(x, site_r, site_c, title, union):
        text(sl, x, 1.6, 5.8, 0.45, title, size=19, color='ink', bold=True)
        for r in range(3):
            for c in range(3):
                n = r * 3 + c + 1
                inside = (r == site_r) or (c == site_c)
                both = n in (2, 4)
                f = 'orange_m' if (inside and both) else ('blue' if inside else 'soft')
                box(sl, x + c * 1.25, 2.15 + r * 0.95, 1.15, 0.85, f'G{n}', fill=f,
                    color='white' if inside else 'faint', size=18, bold=True, shape='rect')
        text(sl, x, 5.1, 5.8, 0.45, union, size=16, color='blue_d', bold=True)
    g(0.8, 0, 0, 'Site 2 (Dept 5): row 5 + column 5', 'G1 ∪ G2 ∪ G3 ∪ G4 ∪ G7')
    step(sl)
    g(7.2, 1, 1, 'Site 3 (Dept 4): row 4 + column 4', 'G4 ∪ G5 ∪ G6 ∪ G2 ∪ G8')
    step(sl)
    box(sl, 4.85, 2.4, 1.9, 2.2, [('G2 and G4', 16, 'orange'), ('stored at **both** sites', 14)], fill='orange_s', size=14, color='body', gap=0.15)
    takeaway(sl, 'Every join with a local EMPLOYEE or PROJECT row is local → **no network transfer**.', y=5.8)

    sl = D.slide('Example: one UPDATE that moves a row', sec='Exercise 23.29', say="""
Here is a concrete example of that update cost, from exercise 23.29 in the book.
A bookstore chain fragments its BOOKS table by price. Fragment B2 holds books from 20 to 50 dollars, and it is replicated at two sites, MIDDLE and WEST. Fragment B3 holds books from 50 to 100 dollars, stored only at WEST.
Someone at MIDDLE changes the price of book 1234 from 45 to 55 dollars.
[click] Price is the fragmentation attribute. At 55 dollars the row no longer satisfies B2's condition — it belongs in B3. So the row must move.
[click] Step 1: delete it from B2 at MIDDLE. Step 2: delete it from the B2 copy at WEST. Step 3: insert it into B3 at WEST.
[click] So one innocent UPDATE statement became a transaction touching two sites and two fragments. Keeping that correct when a site can crash in the middle is exactly Member 3's topic.""",
                   cue='Tell it as a story; three clicks.')
    box(sl, 0.6, 1.6, 12.13, 0.75, 'UPDATE BOOKS SET Price = 55 WHERE Book# = 1234;      -- was $45', fill='soft', font='Consolas', size=17, color='blue_d', shape='rect', align='l', pad=0.25)
    sites = [('MIDDLE', [('B2  $20–$50', 'blue_s')]), ('WEST', [('B2  $20–$50', 'blue_s'), ('B3  $50–$100', 'orange_s')])]
    for j, (s, frs) in enumerate(sites):
        x = 0.9 + j * 4.0
        server(sl, x, 2.75, 1.0, 1.1, label=s)
        for k, (fr, fl) in enumerate(frs):
            box(sl, x + 1.3, 2.7 + k * 0.7, 2.2, 0.58, fr, fill=fl, size=15, color='ink', bold=True)
    step(sl)
    box(sl, 9.0, 2.6, 3.73, 1.5, [('$55 fails B2, fits B3', 17, 'orange'), 'Price is the **fragmentation attribute** → the row must move.'], fill='orange_s', size=15, color='ink', gap=0.15)
    step(sl)
    acts = [('1', 'DELETE from B2 @ MIDDLE', 'red_s', 'red'), ('2', 'DELETE from B2 @ WEST', 'red_s', 'red'), ('3', 'INSERT into B3 @ WEST', 'green_s', 'green')]
    for k, (n, a, f, c) in enumerate(acts):
        x = 0.6 + k * 4.1
        box(sl, x, 4.6, 3.9, 0.85, a, fill=f, color=c, size=17, bold=True)
        numdot(sl, x - 0.1, 4.45, n, d=0.42, size=14, fill=c)
    step(sl)
    takeaway(sl, 'One UPDATE → a **multi-site transaction** (2 sites, 2 fragments). Correctness = Part 3.', y=5.9)

    sl = D.slide('Sharding in practice: choosing the shard key', kicker='IN PRACTICE · PART 2', say="""
In real systems, horizontal fragmentation is called sharding, and the single most important design decision is the shard key — the attribute you split on, like Dno in our example.
Imagine an online shop with an ORDERS table split over three shards. Three choices:
[click] Shard by region — North, Central, South. Just like our Dno example: queries for one region stay on one shard. But if the South has most of the customers, the South shard is overloaded.
[click] Shard by order date. All of today's orders go to the newest shard — this is called a hot shard — while the old shards sit idle. Popular choice, often a mistake.
[click] Shard by a hash of the customer ID. The load is spread evenly. The price: a query like "all orders in March" must ask every shard.
Real systems — MongoDB, Cassandra, Vitess for MySQL — all ask you to pick this key, and changing it later is painful. So Section 23.2 is exactly the decision engineers make on day one.
That's my part. Member 3 will now show how all these sites stay correct when many users update them at once.""",
                   cue='Point at the tallest bar each time: that is the overloaded shard.')
    text(sl, 0.6, 1.55, 12, 0.45, 'An online shop splits its **ORDERS** table over 3 shards. Which column decides where a row goes?', size=18, color='body')
    opts = [('Shard by region', 'North · Central · South', [0.45, 0.6, 1.0], 'Queries for one region stay local', 'South is much bigger → uneven load'),
            ('Shard by order date', 'Jan–Apr · May–Aug · Sep–Dec', [0.08, 0.08, 1.0], 'Range queries by date are easy', '"Hot shard": all new orders hit one shard'),
            ('Shard by hash(customer)', 'hash(id) mod 3', [0.7, 0.68, 0.72], 'Load spread evenly', '"All orders in March" asks every shard')]
    for i, (t, s, loads, good, bad) in enumerate(opts):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 2.15, 3.9, 4.0, fill='white', radius=0.05)
        text(sl, x + 0.25, 2.25, 3.5, 0.45, t, size=18, color='ink', bold=True)
        text(sl, x + 0.25, 2.7, 3.4, 0.35, s, size=14, color='muted')
        for k, ld in enumerate(loads):
            hh = 1.3 * ld
            f = 'red_m' if ld >= 0.95 and min(loads) < 0.5 else 'blue'
            box(sl, x + 0.55 + k * 1.0, 4.45 - hh, 0.75, hh, fill=f, shape='rect')
            text(sl, x + 0.4 + k * 1.0, 4.5, 1.05, 0.3, f'shard {k + 1}', size=13, color='muted', align='c')
        text(sl, x + 0.25, 4.95, 3.45, 1.15, ['✓ ' + good, ('✗ ' + bad, 15, 'red')], size=15, color='green', gap=0.2)
    text(sl, 0.6, 6.35, 12.13, 0.45, 'MongoDB, Cassandra and Vitess (MySQL) all call this **sharding** and ask you to choose the key — the decision of §23.2.', size=15, color='muted')
