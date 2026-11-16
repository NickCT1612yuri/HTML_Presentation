from deck import *


def bars(sl, items, x=0.6, y=2.55, label_w=4.6, w_max=5.2, vmax=1_004_000, best=None, h=0.6, gap=0.95):
    for i, (lab, calc, v) in enumerate(items):
        step(sl)
        yy = y + i * gap
        good = best == i
        text(sl, x, yy - 0.05, label_w, h + 0.1, [lab, (calc, 13, 'muted')], size=16, color='ink', bold=True, anchor='m', gap=0.05)
        bar(sl, x + label_w + 0.1, yy, w_max, v, vmax, h=h, fill='green_m' if good else 'faint',
            label=f'{v:,} B' + ('  ✓ best' if good else ''), lsize=17, bold=good, lcolor='green' if good else 'ink')


def build(D):
    D.divider(4, ['The four stages of distributed query processing', 'Why the network dominates the cost',
                  'Worked example: three plans, real byte counts', 'Semijoin, and decomposing queries & updates'],
              say="""
Thank you. I'm Member 4 and I'll talk about distributed query processing — section 23.5.
So far we know where data is and how to keep it correct. Now the practical question: when a user sends a query, and the data is spread over several sites, how do we answer it cheaply? I'll show you real numbers from the textbook, and a clever trick called the semijoin.""")

    sl = D.slide('From one query to many local queries', sec='23.5.1', say="""
A distributed query goes through four stages.
Stage 1, query mapping. The SQL query is translated into relational algebra on the global tables, using the global conceptual schema — as if the database were not distributed. It is normalized, checked for semantic errors, simplified and restructured.
[click] Stage 2, localization. Now we use the fragmentation and replication information: the query on global tables is mapped onto separate queries on individual fragments.
[click] Stage 3, global optimization. Among many candidate plans — different orders of operations — we pick the one closest to optimal. Cost is measured in time.
[click] Stage 4, local optimization. Each site optimizes its own sub-query, with the same techniques a centralized DBMS uses.
[click] Stages 1 to 3 run at a central control site. Stage 4 runs at each local site.
Think of planning a road trip. First, decide where you want to go; then which roads exist; then choose the fastest route; then each driver handles their own part of the road.""",
                   cue='Walk the four chevrons; mention where each stage runs.')
    st = [('Query mapping', 'SQL → algebra on global tables'), ('Localization', 'Global tables → fragments'),
          ('Global optimization', 'Pick the cheapest plan'), ('Local optimization', 'Each site tunes its own part')]
    for i, (a, b) in enumerate(st):
        if i:
            step(sl)
        x = 0.6 + i * 3.08
        box(sl, x, 1.8, 3.15, 1.5, '', fill='blue' if i < 3 else 'green_m', shape='chevron' if i else 'pent')
        text(sl, x + (0.35 if i == 0 else 0.75), 1.8, 2.05 if i else 2.4, 1.5, [f'{i + 1}. {a}', (b, 13, 'white')], size=16, color='white', bold=True, anchor='m', align='c', gap=0.1)
    step(sl)
    box(sl, 0.6, 3.5, 9.0, 0.5, 'Stages 1–3: central control site', fill='blue_xs', color='blue', size=15, bold=True, shape='rect')
    box(sl, 9.7, 3.5, 3.03, 0.5, 'Stage 4: each site', fill='green_s', color='green', size=15, bold=True, shape='rect')
    callout(sl, 0.6, 4.4, 12.13, 1.4, 'Road trip: decide the destination → see which roads exist → choose the fastest route → each driver drives their own stretch.', size=16)

    sl = D.slide('The network is the expensive part', sec='23.5.1', say="""
How do we measure "cheapest"? The cost of a distributed query has three parts: CPU cost, disk I/O cost, and communication cost — the cost of sending data over the network. We can weight them: w1 times CPU, plus w2 times I/O, plus w3 times communication.
On a network — especially a wide-area network between cities — the communication term usually dominates. Moving one megabyte across the country takes far longer than reading it from a local disk.
[click] So in distributed query optimization the main goal is simple: minimize the amount of data transferred.
Analogy: you want to compare two big catalogs held in two cities. You could truck one whole catalog to the other city — or you could just send a short list of the items you need. Shipping is what costs money.""",
                   cue='Point at the big "Comm" block: that\'s what we minimize.')
    box(sl, 0.6, 1.7, 12.13, 0.9, 'Cost = w1 · CPU  +  w2 · I/O  +  w3 · Communication', fill='soft', size=24, color='ink', bold=True, shape='rect')
    parts = [('CPU', 1.3, 'blue_s', 'blue_d'), ('I/O', 1.8, 'blue_s', 'blue_d'), ('Communication (network)', 8.8, 'orange_m', 'white')]
    x = 0.6
    for lab, w, f, c in parts:
        box(sl, x, 3.0, w - 0.05, 1.0, lab, fill=f, color=c, size=17, bold=True, shape='rect')
        x += w
    text(sl, 0.6, 4.05, 12, 0.4, 'Typical share of the cost on a wide-area network (illustration)', size=13, color='muted')
    step(sl)
    box(sl, 0.6, 4.65, 5.9, 1.6, [('Goal', 15, 'blue'), 'Minimize the **amount of data transferred** between sites.'], fill='blue_xs', size=18, align='l', pad=0.25, gap=0.15, color='ink')
    callout(sl, 6.83, 4.65, 5.9, 1.6, 'Don\'t truck a whole catalog to another city — send a short list of what you need.', size=16)

    sl = D.slide('The example setup: two tables, three sites', sec='23.5.2 · Fig. 23.4', say="""
Here is the textbook's example — please remember these numbers, we'll use them for the next six slides.
Site 1 has EMPLOYEE: 10,000 rows, each 100 bytes. That's one million bytes — a big table.
Site 2 has DEPARTMENT: 100 rows, each 35 bytes. That's only 3,500 bytes — a tiny table.
The user is at Site 3, which has neither table. The result has to end up at Site 3.
The result row has three fields: first name, 15 bytes, last name, 15 bytes, department name, 10 bytes. So every result row is 40 bytes.
And no fragmentation, to keep it simple. Our goal: minimize the bytes sent over the network.""",
                   cue='Big table on the left, tiny table on the right, user at Site 3.')
    server(sl, 1.0, 1.9, 1.3, 1.5, label='Site 1')
    box(sl, 2.6, 1.85, 3.5, 1.65, [('EMPLOYEE', 20, 'blue_d'), '10,000 rows × 100 B', ('= 1,000,000 B', 18, 'ink')], fill='blue_s', size=16, color='body', bold=True, gap=0.1)
    server(sl, 7.0, 1.9, 1.3, 1.5, label='Site 2')
    box(sl, 8.6, 2.15, 2.6, 1.05, [('DEPARTMENT', 16, 'blue_d'), '100 rows × 35 B = 3,500 B'], fill='blue_s', size=13, color='body', bold=True, gap=0.05)
    server(sl, 4.4, 4.2, 1.3, 1.5, label='Site 3 (query here)', accent='orange_m', line_c='orange_m')
    person(sl, 3.5, 4.5, 0.65, fill='orange_m')
    line(sl, 2.0, 3.8, 4.3, 4.6, color='faint', w=2, head=None, dash=True)
    line(sl, 7.6, 3.8, 5.8, 4.6, color='faint', w=2, head=None, dash=True)
    box(sl, 6.6, 4.3, 6.13, 1.4, [('Result row = 40 B', 18, 'ink'), 'Fname 15  +  Lname 15  +  Dname 10'], fill='orange_s', size=15, color='body', bold=True, gap=0.15)
    takeaway(sl, 'Big table at Site 1, tiny table at Site 2, answer needed at Site 3. **Minimize bytes sent.**', y=6.1)

    sl = D.slide('Query Q: every employee with their department', sec='23.5.2', say="""
Query Q: for every employee, give the name and the name of their department. That's a join of EMPLOYEE and DEPARTMENT on Dno equals Dnumber. Every employee has a department, so the result has 10,000 rows times 40 bytes — 400,000 bytes.
Three possible plans.
[click] Plan 1: send both tables to Site 3 and join there. One million plus 3,500: 1,003,500 bytes.
[click] Plan 2: send EMPLOYEE to Site 2, join there, send the result to Site 3. One million plus 400,000: 1,400,000 bytes — the worst.
[click] Plan 3: send DEPARTMENT to Site 1, join there, send the result to Site 3. 3,500 plus 400,000: 403,500 bytes. The best.
[click] The lesson: move the small table to the big one, not the other way round. But notice: even in the best plan, the 400,000-byte result is most of the cost.""",
                   cue='Read the three bars; land on plan 3.')
    box(sl, 0.6, 1.6, 12.13, 0.65, 'π Fname, Lname, Dname ( EMPLOYEE ⋈ Dno = Dnumber DEPARTMENT )     →  result 10,000 × 40 B = 400,000 B',
        fill='soft', size=16, color='blue_d', bold=True, shape='rect', align='l', pad=0.25)
    bars(sl, [('1 · Both tables → Site 3', '1,000,000 + 3,500', 1_003_500),
              ('2 · EMPLOYEE → Site 2, result → Site 3', '1,000,000 + 400,000', 1_400_000),
              ('3 · DEPARTMENT → Site 1, result → Site 3', '3,500 + 400,000', 403_500)], vmax=1_400_000, best=2)
    step(sl)
    takeaway(sl, 'Ship the **small** table to the big one. Here the big result (400,000 B) still dominates.', y=5.75)

    sl = D.slide('Query Q′: each department with its manager', sec='23.5.2', say="""
Query Q-prime: for each department, give the department name and the manager's name. Now the join condition is Mgr_ssn equals Ssn.
The difference: only 100 employees are managers. So the result is only 100 rows times 40 bytes — 4,000 bytes.
[click] Plan 1: both tables to Site 3: still 1,003,500 bytes.
[click] Plan 2: EMPLOYEE to Site 2, result to Site 3: 1,000,000 plus 4,000 — 1,004,000.
[click] Plan 3: DEPARTMENT to Site 1, result to Site 3: 3,500 plus 4,000 — only 7,500 bytes.
[click] That is about 0.75 percent of plan 1 — a 99 percent saving! Same tables, same sites; only the query changed, and the best plan became more than a hundred times cheaper.
So the optimizer must consider not only table sizes, but also how big the result will be.""",
                   cue='Let the -99% sink in.')
    box(sl, 0.6, 1.6, 12.13, 0.65, 'π Fname, Lname, Dname ( DEPARTMENT ⋈ Mgr_ssn = Ssn EMPLOYEE )     →  result 100 × 40 B = 4,000 B',
        fill='soft', size=16, color='blue_d', bold=True, shape='rect', align='l', pad=0.25)
    bars(sl, [('1 · Both tables → Site 3', '1,000,000 + 3,500', 1_003_500),
              ('2 · EMPLOYEE → Site 2, result → Site 3', '1,000,000 + 4,000', 1_004_000),
              ('3 · DEPARTMENT → Site 1, result → Site 3', '3,500 + 4,000', 7_500)], vmax=1_400_000, best=2)
    step(sl)
    box(sl, 9.9, 4.35, 2.83, 1.1, '−99%', fill='green_s', color='green', size=36, bold=True)
    takeaway(sl, 'Only 100 of 10,000 employees are managers → small result → plan 3 wins **by far**.', y=5.75)

    sl = D.slide('Semijoin: send the guest list, not the phone book', sec='23.5.3', say="""
Can we do even better? Yes, with the semijoin.
Here's the idea. You are throwing a party, and you need the phone numbers of your 100 guests. The phone book of the whole city is in another town. You could ask them to mail you the whole phone book. [click] Or — much smarter — you send them your short guest list, they look up only those 100 people, and they send back just those 100 numbers.
[click] The semijoin does exactly that. Instead of shipping a whole table, we ship only the join column of one table to the other site. That site keeps only the rows that match, and ships back only those rows — and only the columns we need.
The goal is to reduce the number of rows before they cross the network. It works best when only a small fraction of the rows actually take part in the join.""",
                   cue='Tell the party story slowly; then map it to tables.')
    text(sl, 0.6, 1.6, 5.9, 0.4, '✗  Naive: ship the whole table', size=19, color='red', bold=True)
    box(sl, 0.6, 2.15, 1.6, 1.3, 'You', fill='blue_s', color='blue_d', size=18, bold=True)
    box(sl, 4.6, 2.0, 1.9, 1.6, 'Whole phone book\n(1,000,000 B)', fill='red_s', color='red', size=14, bold=True)
    line(sl, 4.5, 2.8, 2.3, 2.8, color='red_m', w=6)
    step(sl)
    text(sl, 6.83, 1.6, 5.9, 0.4, '✓  Semijoin: send the list first', size=19, color='green', bold=True)
    box(sl, 6.83, 2.15, 1.6, 1.3, 'You', fill='blue_s', color='blue_d', size=18, bold=True)
    box(sl, 10.83, 2.0, 1.9, 1.6, 'Phone book', fill='soft', color='body', size=15, bold=True)
    line(sl, 8.5, 2.45, 10.75, 2.45, color='blue', w=2.5, flow=True)
    text(sl, 8.5, 2.0, 2.3, 0.4, '① guest list (100 names)', size=12, color='blue', bold=True, align='c')
    line(sl, 10.75, 3.15, 8.5, 3.15, color='green_m', w=2.5, flow='green_m')
    text(sl, 8.5, 3.2, 2.3, 0.4, '② only 100 numbers', size=12, color='green', bold=True, align='c')
    step(sl)
    box(sl, 0.6, 4.1, 12.13, 1.5, [('In database terms', 15, 'blue'),
                                    'Send only the **join column** to the other site → it keeps only **matching rows** → sends back only those rows, with only the **needed columns**.'],
        fill='blue_xs', align='l', pad=0.3, size=17, gap=0.15, color='ink')
    takeaway(sl, 'Pays off when only a **small fraction** of rows take part in the join.', y=5.85)

    sl = D.slide('The semijoin, formally', sec='23.5.3', say="""
Formally, the semijoin of R and S on A equals B is written with this half-bowtie symbol. It is defined as: join R with S, then keep only R's attributes.
[click] In words: the result has only R's columns, and only R's rows that have a match in S. S itself is used only as a filter.
Two properties to remember. First, it is not commutative: R semijoin S is not the same as S semijoin R — the first keeps rows of R, the second keeps rows of S. Second, the result is never larger than R: it is always a subset of R.
The theory of semijoin processing comes from Bernstein and Goodman, 1981.""",
                   cue='Emphasize: "S is only used as a filter".')
    box(sl, 0.6, 1.7, 12.13, 1.0, 'R ⋉ A=B S   ≡   π attributes of R ( R ⋈ A=B S )', fill='soft', size=26, color='blue_d', bold=True, shape='rect')
    text(sl, 0.6, 2.85, 12, 0.5, 'Keep only R\'s columns, and only R\'s rows that **have a match** in S.  (S is just a filter.)', size=18, color='body')
    # mini illustration
    step(sl)
    grid(sl, 0.9, 3.55, [1.2, 1.2], [['R.A', 'R.x'], ['1', 'a'], ['2', 'b'], ['3', 'c'], ['4', 'd']], rowh=0.42, size=14,
         hl={(2, 0): 'green_s', (2, 1): 'green_s', (4, 0): 'green_s', (4, 1): 'green_s'})
    grid(sl, 3.8, 3.55, [1.2], [['S.B'], ['2'], ['4'], ['7']], rowh=0.42, size=14, head_fill='faint')
    text(sl, 5.15, 4.0, 0.8, 0.6, '→', size=30, color='muted', align='c')
    grid(sl, 6.0, 3.55, [1.2, 1.2], [['R.A', 'R.x'], ['2', 'b'], ['4', 'd']], rowh=0.42, size=14, head_fill='green')
    text(sl, 6.0, 4.85, 2.6, 0.4, 'R ⋉ S', size=15, color='green', bold=True, align='c')
    box(sl, 9.0, 3.55, 3.73, 1.0, [('Not commutative', 15, 'blue'), 'R ⋉ S ≠ S ⋉ R'], fill='blue_xs', size=15, gap=0.05, color='ink')
    box(sl, 9.0, 4.7, 3.73, 1.0, [('Never bigger than R', 15, 'blue'), 'R ⋉ S ⊆ R'], fill='blue_xs', size=15, gap=0.05, color='ink')
    text(sl, 0.6, 6.25, 12, 0.4, 'Theory: Bernstein & Goodman (1981)', size=13, color='muted')

    sl = D.slide('Semijoin in three steps', sec='23.5.3', say="""
In practice, a semijoin strategy for joining R at one site with S at another has three steps.
Step 1: at S's site, project only the join column of S. That's a small list — call it F. Send F to R's site.
[click] Step 2: at R's site, join F with R. This keeps only the rows of R that match. Project only the columns we need, plus the join column, and send that back to S's site.
[click] Step 3: back at S's site, join the reduced R with S to get the final answer.
In our example, R is EMPLOYEE at Site 1, S is DEPARTMENT at Site 2, and the result is needed at Site 2. Let's trace the numbers.""",
                   cue='Follow ① ② ③ on the diagram.')
    server(sl, 1.2, 2.0, 1.3, 1.5, label='Site 2: S (DEPARTMENT)')
    server(sl, 10.8, 2.0, 1.3, 1.5, label='Site 1: R (EMPLOYEE)')
    line(sl, 2.7, 2.3, 10.6, 2.3, color='blue', w=3, flow=True)
    box(sl, 4.2, 1.6, 4.9, 0.55, '① F = π join column (S)  — tiny', fill='blue_s', color='blue_d', size=15, bold=True)
    step(sl)
    line(sl, 10.6, 3.2, 2.7, 3.2, color='green_m', w=3, flow='green_m')
    box(sl, 4.2, 3.35, 4.9, 0.55, '② π needed columns (R ⋈ F)  — only matches', fill='green_s', color='green', size=15, bold=True)
    step(sl)
    box(sl, 0.6, 4.4, 5.5, 0.85, '③ At Site 2: join the reduced R with S → final result', fill='orange_s', color='orange', size=16, bold=True)
    steps = [('Step 1', 'project S\'s join column, ship it to R\'s site'), ('Step 2', 'filter R by it; ship back matching rows, needed columns'),
             ('Step 3', 'join locally with S — no more transfer')]
    for i, (a, b) in enumerate(steps):
        text(sl, 6.6, 4.3 + i * 0.6, 6.1, 0.55, f'**{a}:** {b}', size=15, color='body', anchor='m')

    sl = D.slide('Tracing the semijoin with real numbers', sec='23.5.3', say="""
Now the numbers, with the result needed at Site 2, where DEPARTMENT is.
For Q-prime, the managers query. Step 1: project Mgr_ssn from DEPARTMENT: 100 values times 9 bytes — 900 bytes go to Site 1. Step 2: join with EMPLOYEE; only the 100 managers match. Send Mgr_ssn, first name and last name: 39 bytes times 100 — 3,900 bytes back to Site 2. Step 3 is local. Total: 4,800 bytes.
For Q, every employee's department. Step 1: project Dnumber: 100 times 4 bytes, 400 bytes. Step 2: join with EMPLOYEE — but every employee matches! So we still send 10,000 rows of Dno, first name and last name, 34 bytes each — 340,000 bytes. Total: 340,400 bytes.
[click] Look at the table. For Q-prime, the semijoin beats even the best simple plan — 4,800 against 7,500 — and is 208 times smaller than shipping EMPLOYEE. For Q, the saving is small, because no rows were filtered out; only the rows got narrower.""",
                   cue='Do Q′ first (the success), then Q (the disappointment).')
    rows = [['Step (result at Site 2)', 'Q′ — managers', 'Q — all employees'],
            ['① send join column', 'Mgr_ssn: 100 × 9 = 900', 'Dnumber: 100 × 4 = 400'],
            ['② send matching rows', '100 rows × 39 = 3,900', '10,000 rows × 34 = 340,000'],
            ['③ local join', '0', '0'], ['Semijoin total', '4,800 B', '340,400 B']]
    grid(sl, 0.6, 1.65, [3.3, 3.0, 3.2], rows, rowh=0.58, size=15, bold_first_col=True,
         hl={(4, 1): ('green_s', 'green'), (4, 2): ('orange_s', 'orange')})
    step(sl)
    cmp = [['Plan', 'Q′', 'Q'], ['Ship EMPLOYEE', '1,000,000', '1,000,000'], ['DEPT → Site 1, result back', '7,500', '403,500'], ['Semijoin', '4,800', '340,400']]
    grid(sl, 0.6, 4.75, [3.3, 1.5, 1.7], cmp, rowh=0.45, size=14, head_fill='faint', bold_first_col=True,
         hl={(3, 1): ('green_s', 'green'), (3, 2): ('orange_s', 'orange')})
    box(sl, 10.3, 1.65, 2.43, 2.0, [('Q′', 22, 'green'), '208× less than shipping EMPLOYEE'], fill='green_s', size=15, color='ink', gap=0.1)
    box(sl, 7.4, 4.75, 5.33, 1.8, [('Q: only 16% better', 17, 'orange'), 'Every employee matches, so step ② filters **no rows** — they are just narrower (34 B vs 40 B).'],
        fill='orange_s', size=15, color='ink', align='l', pad=0.25, gap=0.15)
    text(sl, 0.6, 6.65, 12, 0.3, '34 B = Dno 4 + Fname 15 + Lname 15  ·  39 B = Mgr_ssn 9 + Fname 15 + Lname 15', size=12, color='muted')

    sl = D.slide('Scale it up: what these bytes mean in real life', kicker='IN PRACTICE · PART 4', say="""
A fair question: who cares about one megabyte? Today that's nothing. So let's scale the textbook example up a million times — ten billion employee rows, a terabyte — which is normal for a large company's logs or orders.
Assume a good dedicated link between two data centers: 1 gigabit per second, roughly 125 megabytes per second.
[click] Plan 1 for query Q — ship both tables: about one terabyte, over two hours of pure transfer.
[click] The best simple plan for Q: about 400 gigabytes — still almost an hour.
[click] For Q-prime, the best simple plan moves 7.5 gigabytes — one minute. And the semijoin: 4.8 gigabytes — under 40 seconds.
Same query, same data: the choice of plan is the difference between two hours and forty seconds. Cloud providers also charge per gigabyte moved between regions, so bad plans cost real money.
[click] And real engines do exactly what we just learned. Spark and Hadoop use a "broadcast join": copy the small table to every machine that holds the big one — that is plan 3. And they push filters, including semijoin-style Bloom filters, before moving data.""",
                   cue='Scale ×1,000,000; reveal rows one by one, then the right panel.')
    text(sl, 0.6, 1.55, 7.6, 0.45, 'Same plans, data **× 1,000,000**, link = 1 Gbit/s (≈125 MB/s)', size=17, color='body')
    rows_ = [('Q · ship both tables', '≈ 1.0 TB', '≈ 2 h 14 min', 'red_s', 'red'),
             ('Q · best simple plan', '≈ 404 GB', '≈ 54 min', 'orange_s', 'orange'),
             ('Q′ · best simple plan', '7.5 GB', '≈ 1 min', 'green_s', 'green'),
             ('Q′ · semijoin (result at Site 2)', '4.8 GB', '≈ 38 s', 'green_s', 'green')]
    grid(sl, 0.6, 2.1, [3.6, 1.8, 2.0], [['Plan', 'Data moved', 'Transfer time']], rowh=0.55, size=15)
    for k, (a, b, c, f, col_) in enumerate(rows_):
        if k != 3:
            step(sl)
        grid(sl, 0.6, 2.65 + k * 0.62, [3.6, 1.8, 2.0], [[a, b, c]], header=False, rowh=0.62, size=15,
             hl={(0, 2): (f, col_)}, bold_first_col=True)
    text(sl, 0.6, 5.2, 7.4, 0.9, 'Same query, same data: **2 hours vs. 40 seconds**. Moving data between cloud regions is also billed per GB.', size=15, color='muted')
    step(sl)
    box(sl, 8.5, 1.6, 4.23, 4.85, [('Real engines do this', 18, 'ink'),
                                   ('**Broadcast join** (Spark, Hadoop): copy the small table to every machine holding the big one = plan 3.', 15),
                                   ('**Filters first**: push predicates and semijoin-style Bloom filters before shuffling data.', 15),
                                   ('Optimizers estimate sizes — exactly the cost thinking of §23.5.', 15)],
        fill='blue_xs', align='l', anchor='t', pad=0.3, size=15, color='body', gap=0.6)

    sl = D.slide('Decomposition: guards route the work', sec='23.5.4 · Fig. 23.5', say="""
The last idea in this section: decomposition. With full distribution transparency, the user writes queries and updates on global tables. The DDBMS must break them into sub-queries and sub-updates for the fragments. To do that, the catalog stores, for each fragment, its attribute list and a guard condition.
A guard is the condition every row in that fragment must satisfy. Look at Site 2's catalog. EMPD5 holds some EMPLOYEE columns, with the guard "Dno equals 5". DEP5 holds all DEPARTMENT columns, guard "Dnumber equals 5". PROJS5: "Dnum equals 5". And WORKS_ON5: rows whose employee is in EMPD5, or whose project is in PROJS5 — that's exactly the row-plus-column idea Member 2 showed.
Site 3 has the same with 4. Site 1, headquarters, has guards that are simply TRUE — it holds everything.
Think of guards like sorting rules in a post office: "postcode starts with 5 → Site 2's bin".""",
                   cue='Read one guard per row; post-office analogy.')
    rows = [['Fragment (Site 2)', 'Attributes', 'Guard condition'], ['EMPD5', 'Fname, Minit, Lname, Ssn, Salary, Super_ssn, Dno', 'Dno = 5'],
            ['DEP5', 'all', 'Dnumber = 5'], ['DEP5_LOCS', 'all', 'Dnumber = 5'], ['PROJS5', 'all', 'Dnum = 5'],
            ['WORKS_ON5', 'all', 'Essn IN π Ssn (EMPD5)  OR  Pno IN π Pnumber (PROJS5)']]
    grid(sl, 0.6, 1.65, [2.2, 4.6, 5.33], rows, rowh=0.58, size=14, bold_first_col=True,
         hl={(r, 2): ('orange_s', 'orange') for r in range(1, 6)})
    text(sl, 0.6, 5.2, 7, 0.5, 'Site 3: same with 4.   Site 1 (HQ): every guard is **TRUE**.', size=16, color='body')
    callout(sl, 7.4, 5.2, 5.33, 1.35, 'Post-office sorting rule: "postcode 5xxx → Site 2\'s bin".', size=15)

    sl = D.slide('Update decomposition: one INSERT, two sites', sec='23.5.4', say="""
Here is how guards are used for an update. Someone inserts a new employee, Alex Coleman, in department 4.
The user writes one INSERT into the global EMPLOYEE table. The DDBMS checks the guards.
[click] Site 1's guard is TRUE, so the full tuple — all columns — goes into EMPLOYEE at Site 1.
[click] Site 3's EMPD4 guard is "Dno equals 4" — Alex matches. So a projected tuple, with only EMPD4's columns, goes into EMPD4 at Site 3.
[click] Site 2's guard is "Dno equals 5" — Alex doesn't match, so nothing happens at Site 2.
The user never had to know any of this — that's fragmentation transparency in action.""",
                   cue='Follow the INSERT into both arrows; Site 2 gets nothing.')
    box(sl, 0.6, 1.65, 12.13, 0.75, 'INSERT INTO EMPLOYEE VALUES (\'Alex\', \'B\', \'Coleman\', \'345671239\', …, 33000, \'987654321\', 4);',
        fill='soft', font='Consolas', size=15, color='blue_d', shape='rect', align='l', pad=0.25)
    tg = [('Site 1 · EMPLOYEE', 'guard TRUE', '✓ full tuple (all columns)', 'green_s', 'green'),
          ('Site 3 · EMPD4', 'guard Dno = 4', '✓ projected tuple:\n⟨Alex, B, Coleman, 345671239, 33000, 987654321, 4⟩', 'green_s', 'green'),
          ('Site 2 · EMPD5', 'guard Dno = 5', '✗ no match → nothing', 'soft', 'muted')]
    for i, (a, g, r, f, c) in enumerate(tg):
        step(sl)
        x = 0.6 + i * 4.1
        line(sl, 6.66, 2.45, x + 1.95, 3.0, color='faint', w=2.5)
        box(sl, x, 3.05, 3.9, 2.6, fill=f, radius=0.06)
        text(sl, x + 0.25, 3.15, 3.4, 0.45, a, size=19, color='ink', bold=True)
        box(sl, x + 0.25, 3.7, 1.9, 0.45, g, fill='white', color='orange', size=13, bold=True)
        text(sl, x + 0.25, 4.3, 3.45, 1.3, r, size=15, color=c, bold=True)
    takeaway(sl, 'The user writes one INSERT; the **guards** decide where it goes.', y=5.95)

    sl = D.slide('Query decomposition: a plan at Site 2', sec='23.5.4', say="""
And here is a query. At Site 2, a user asks: "retrieve the names and hours per week of every employee who works on a project controlled by department 5."
The DDBMS sees from the guards that all the department-5 projects and their WORKS_ON rows are at Site 2. But the employee names might belong to employees of other departments, which may not be at Site 2. So it builds a plan.
[click] T1, at Site 2: join PROJS5 with WORKS_ON5 and keep the employee Ssns. This is local.
[click] T2, at Site 1: join those Ssns with the full EMPLOYEE table to get first and last names.
[click] RESULT, back at Site 2: join T2 with WORKS_ON5 to add the hours.
[click] Does that look familiar? It is a semijoin plan — we ship a small list of Ssns, not the whole EMPLOYEE table. The alternative would be to send the whole query to Site 1, which has everything. The optimizer estimates both and picks the cheaper one.
That's the end of my part. Member 5 will zoom out to the types and architectures of distributed systems.""",
                   cue='Follow T1 → T2 → RESULT across sites.')
    box(sl, 0.6, 1.6, 12.13, 0.7, 'Q: names and hours of every employee who works on a **Dept 5 project**', fill='soft', size=18, color='ink', shape='rect', align='l', pad=0.25)
    steps = [('T1', '@ Site 2', 'π Essn ( PROJS5 ⋈ Pnumber=Pno WORKS_ON5 )', 'local: Dept 5 projects + their WORKS_ON rows', 'blue_s'),
             ('T2', '@ Site 1', 'π Essn, Fname, Lname ( T1 ⋈ Essn=Ssn EMPLOYEE )', 'fetch names from the full EMPLOYEE table', 'orange_s'),
             ('RESULT', '@ Site 2', 'π Fname, Lname, Hours ( T2 * WORKS_ON5 )', 'add the hours locally', 'blue_s')]
    for i, (a, s, e, d, f) in enumerate(steps):
        step(sl)
        y = 2.6 + i * 1.12
        box(sl, 0.6, y, 1.6, 0.95, [a, (s, 13, 'body')], fill=f, color='ink', size=18, bold=True, gap=0.05)
        box(sl, 2.35, y, 6.6, 0.95, [e, (d, 13, 'muted')], fill='white', line='line', size=15, color='blue_d', bold=True, align='l', pad=0.25, gap=0.1)
        if i < 2:
            line(sl, 1.4, y + 0.97, 1.4, y + 1.1, color='faint', w=2)
    step(sl)
    box(sl, 9.2, 2.6, 3.53, 3.2, [('This is a semijoin plan', 16, 'green'), 'Only a short list of Ssns travels to Site 1.',
                                  ('Alternative', 15, 'blue'), 'Send the whole query to Site 1 (it has everything).',
                                  ('The optimizer picks the cheaper estimate.', 14, 'ink')], fill='soft', align='l', anchor='t', pad=0.25, size=14, gap=0.3, color='body')

