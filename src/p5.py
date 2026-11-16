from deck import *


def build(D):
    D.divider(5, ['Types: homogeneous, federated, multidatabase', 'Federated systems and semantic heterogeneity',
                  'Architectures: parallel, pure, federated, 3-tier', 'Distributed catalogs, then a summary'],
              say="""
Thank you. I'm Member 5, the last presenter. My part covers sections 23.6 to 23.9.
We zoom out now: what kinds of distributed database systems exist, how are they built — their architectures — and how does the system keep track of where everything is? Then I'll wrap up the whole chapter.""")

    sl = D.slide('Homogeneous or heterogeneous?', sec='23.6', say="""
All distributed database systems have one thing in common: data and software are spread across sites connected by a network. But they differ in many ways.
The first factor is homogeneity. If every server and every client uses identical software — say, all sites run the same DBMS product — the system is homogeneous. [click] If not, it is heterogeneous: one site may run a relational DBMS, another an old network DBMS, another an object DBMS. Then we need a common, canonical query language and translators for each server.
[click] The second factor is local autonomy. If a site cannot work on its own as a standalone DBMS, there is no local autonomy. If local transactions can access the server directly, the site has some autonomy.
Analogy: a homogeneous system is a chain where every branch uses the same cash-register software. A heterogeneous one is a group of independent shops, each with its own system, that agreed to cooperate.""",
                   cue='Left: same software everywhere. Right: different systems + translators.')
    text(sl, 0.6, 1.6, 5.9, 0.45, 'Homogeneous', size=22, color='blue', bold=True)
    for i in range(3):
        db(sl, 0.9 + i * 1.8, 2.25, 1.1, 1.2, 'DBMS X', size=12)
    text(sl, 0.6, 3.6, 5.9, 0.7, 'Identical software at every server and client.', size=16, color='body')
    step(sl)
    text(sl, 6.83, 1.6, 5.9, 0.45, 'Heterogeneous', size=22, color='orange', bold=True)
    for i, t in enumerate(['Relational', 'Network', 'Object']):
        db(sl, 7.1 + i * 1.8, 2.25, 1.15, 1.2, t, fill='orange_s', line_c='orange_m', color='orange', size=12)
    text(sl, 6.83, 3.6, 5.9, 0.7, 'Different DBMSs → need a **canonical language** + **translators**.', size=16, color='body')
    step(sl)
    box(sl, 0.6, 4.45, 12.13, 0.95, [('**Local autonomy**: can a site work on its own?', 17), ('No standalone operation → none.   Local transactions can access the server directly → some autonomy.', 15, 'body')],
        fill='soft', align='l', pad=0.3, gap=0.15, color='ink')
    callout(sl, 0.6, 5.6, 12.13, 1.05, 'A chain where every branch uses the same till software  vs.  independent shops that agreed to cooperate.', size=15)

    sl = D.slide('Classifying DDBMSs: three dimensions', sec='23.6 · Fig. 23.6', say="""
The textbook classifies systems along three independent axes: distribution, autonomy and heterogeneity. Four points are marked.
[click] Point A is a traditional centralized database: full autonomy, but no distribution and no heterogeneity.
Point B is a pure distributed database system. To the user it looks like one centralized DBMS: there is one single conceptual schema and no local autonomy.
Point C is a federated database system, or FDBS. Each server is an independent, autonomous DBMS with its own users and DBA — high autonomy — but there is a global view, a global schema, shared by the applications.
Point D is a multidatabase system: full local autonomy and no global schema at all; the application builds one as needed. With full heterogeneity as well, D can also be a peer-to-peer database system.
In practice, the line between C and D isn't strict, and the book calls both FDBSs.""",
                   cue='Point at each letter; read the legend.')
    ox, oy = 2.3, 5.4
    line(sl, ox, oy, ox + 3.7, oy, color='ink', w=2.5)
    line(sl, ox, oy, ox, oy - 3.3, color='ink', w=2.5)
    line(sl, ox, oy, ox - 1.5, oy + 0.9, color='ink', w=2.5)
    text(sl, ox + 2.3, oy + 0.08, 1.8, 0.4, 'Autonomy', size=15, color='ink', bold=True)
    text(sl, ox + 0.15, oy - 3.4, 2.4, 0.4, 'Distribution', size=15, color='ink', bold=True, align='l')
    text(sl, ox - 1.55, oy + 0.95, 2.0, 0.4, 'Heterogeneity', size=15, color='ink', bold=True)
    pts = [('A', ox + 3.2, oy - 0.45, 'green_m'), ('B', ox + 0.45, oy - 2.6, 'blue'), ('C', ox + 1.8, oy - 2.0, 'orange_m'), ('D', ox + 2.8, oy - 1.2, 'red_m')]
    step(sl)
    for (l, x, y, f) in pts:
        box(sl, x - 0.28, y - 0.28, 0.56, 0.56, l, fill=f, shape='oval', color='white', size=17, bold=True, pad=0)
    rows = [['', 'System', 'Global schema?'], ['A', 'Traditional centralized DB', 'one DB, full autonomy'],
            ['B', 'Pure distributed DB', 'one schema, zero autonomy'], ['C', 'Federated DB (FDBS)', 'a shared global view'],
            ['D', 'Multidatabase / peer-to-peer', 'none — built as needed']]
    grid(sl, 7.0, 1.8, [0.6, 2.75, 2.38], rows, rowh=0.72, size=15, bold_first_col=True,
         hl={(1, 0): ('green_m', 'white'), (2, 0): ('blue', 'white'), (3, 0): ('orange_m', 'white'), (4, 0): ('red_m', 'white')})
    text(sl, 7.0, 5.55, 5.73, 0.7, 'C and D: each server is an independent DBMS with its own users and DBA.', size=14, color='muted')

    sl = D.slide('Federated databases: what makes them hard', sec='23.6.1', say="""
Let's focus on federated systems — independent databases that agree to cooperate. Think of a group of university libraries that share one joint search catalog, while each library keeps its own system.
The hard part is heterogeneity. The book lists several sources.
[click] Differences in data models: one database might be relational, another hierarchical, another just files. Even with the same model, the same fact can be stored differently — as an attribute in one database, as a separate relation in another, or even as a value.
[click] Differences in constraints: one system has ER-style relationships, another uses referential integrity, another uses triggers — and the rules may even conflict.
[click] Differences in query languages: even "SQL" comes in versions — SQL-89, SQL-92, SQL-99, SQL:2008 — each with its own data types and operators.
[click] And the biggest hurdle of all is semantic heterogeneity, which is next.""",
                   cue='Library-consortium analogy; three source cards.')
    callout(sl, 0.6, 1.65, 12.13, 1.05, 'A group of university libraries share one joint search catalog — but each library keeps its own system.', size=16)
    srcs = [('Data models', 'Relational, hierarchical, network, object, files. The same fact can be an attribute, a relation or a value.'),
            ('Constraints', 'ER relationships vs. referential integrity vs. triggers — and the rules may conflict.'),
            ('Query languages', 'SQL-89, SQL-92, SQL-99, SQL:2008 … each with its own types and operators.')]
    for i, (t, d) in enumerate(srcs):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 2.95, 3.9, 2.55, fill='soft', radius=0.06)
        text(sl, x + 0.25, 3.05, 3.4, 0.5, t, size=20, color='ink', bold=True)
        text(sl, x + 0.25, 3.6, 3.45, 1.8, d, size=15, color='body')
    step(sl)
    box(sl, 0.6, 5.7, 12.13, 0.8, 'The biggest hurdle: **semantic heterogeneity** →', fill='orange_s', color='orange', size=18)

    sl = D.slide('Semantic heterogeneity: same word, different meaning', sec='23.6.1', say="""
Semantic heterogeneity means differences in the meaning, interpretation and intended use of the same or related data. It happens because each component database was designed independently — design autonomy.
Look at the example. Two banks join a federation. Both have a table called ACCOUNT with a column "balance". But in the US bank, balance is in dollars and includes pending transactions. In the Japanese bank, balance is in yen and excludes them. Same name, different meaning. [click] If we simply add them up, the result is nonsense.
[click] The book lists what designers decide differently. The universe of discourse — the US versus Japan ACCOUNT, with currency rates. Representation and naming. The understanding, meaning and subjective interpretation of data — this is the chief contributor. Transaction and policy constraints. And the derivation of summaries — how totals and aggregates are computed.""",
                   cue='Do the two-bank example first; then list the five causes.')
    for j, (bank, cur, inc, f, c) in enumerate([('US bank', 'USD $', 'includes pending', 'blue_s', 'blue_d'), ('Japanese bank', 'JPY ¥', 'excludes pending', 'orange_s', 'orange')]):
        x = 0.6 + j * 3.35
        box(sl, x, 1.7, 3.15, 2.6, fill=f, radius=0.06)
        text(sl, x + 0.2, 1.8, 2.8, 0.4, bank, size=18, color=c, bold=True)
        box(sl, x + 0.2, 2.3, 2.75, 0.5, 'ACCOUNT.balance', fill='white', font='Consolas', size=14, color='ink')
        text(sl, x + 0.2, 2.95, 2.8, 1.3, [f'Currency: **{cur}**', f'Balance **{inc}**'], size=15, color='body', gap=0.3)
    step(sl)
    text(sl, 0.6, 4.45, 6.5, 0.9, 'Same name, different meaning → adding them up gives **nonsense**.', size=16, color='red')
    step(sl)
    text(sl, 7.5, 1.65, 5.2, 0.4, 'Where meanings differ', size=18, color='ink', bold=True)
    causes = ['Universe of discourse (US vs. Japan, currency rates)', 'Representation and naming',
              '**Meaning & subjective interpretation** — the chief contributor', 'Transaction and policy constraints', 'Derivation of summaries (aggregates)']
    for i, c in enumerate(causes):
        y = 2.15 + i * 0.68
        numdot(sl, 7.5, y + 0.05, i + 1, d=0.42, size=14, fill='orange_m' if i == 2 else 'blue')
        text(sl, 8.05, y, 4.7, 0.55, c, size=15, color='body', anchor='m')
    takeaway(sl, 'Cause: each component was designed independently (**design autonomy**).', y=5.6)

    sl = D.slide('FDBS: cooperate, but stay independent', sec='23.6.1', say="""
So the challenge of a federated system is to let the components interoperate, while each keeps its autonomy. Besides design autonomy, the book names three more kinds a component wants to keep.
[click] Communication autonomy: the component decides whether to communicate with another component at all.
[click] Execution autonomy: it can run its local operations without interference from outside, and decide the order in which to run them.
[click] Association autonomy: it decides whether, and how much, of its data and functionality to share with the federation.
Back to the libraries: each library decides whether to join the joint search at all, runs its own lending desk its own way, and chooses which collections to show in the joint catalog — maybe not the rare books.
[click] In practice, this gap is bridged by middleware, application servers like WebLogic or WebSphere, and ERP systems like SAP.""",
                   cue='One card per autonomy, with the library example.')
    auts = [('Communication', 'Decide **whether** to talk to other components.', 'Join the joint search or not'),
            ('Execution', 'Run local operations **without outside interference**, in its own order.', 'Run its own lending desk'),
            ('Association', 'Decide **whether and how much** data and functionality to share.', 'Hide the rare-book collection')]
    for i, (t, d, a) in enumerate(auts):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 1.7, 3.9, 3.4, fill='soft', radius=0.06)
        text(sl, x + 0.2, 1.85, 3.6, 0.5, t + ' autonomy', size=17, color='blue', bold=True)
        text(sl, x + 0.25, 2.45, 3.45, 1.5, d, size=16, color='body')
        box(sl, x + 0.2, 4.1, 3.5, 0.8, a, fill='orange_s', color='orange', size=14, bold=True)
    step(sl)
    box(sl, 0.6, 5.35, 12.13, 1.15, 'Bridged in practice by **middleware**, **application servers** (WebLogic, WebSphere) and **ERP** systems (SAP).',
        fill='blue_xs', size=17, color='ink')

    sl = D.slide('Parallel architectures: what do processors share?', sec='23.7.1', say="""
Now architectures. First, an important distinction: parallel versus distributed.
There are three ways to build a multiprocessor database machine, and the question is: what do the processors share? Let me use roommates as the analogy.
[click] Shared memory: processors share both the disk and the main memory. This is tightly coupled — also called shared-everything. Like roommates sharing the kitchen and the fridge.
[click] Shared disk: processors share the disk, but each has its own memory. Loosely coupled. Like roommates who share only the fridge, each cooking in their own kitchen.
[click] Shared nothing: each processor has its own memory and its own disk, and they talk over a fast network — a bus or a switch. Like neighbours in separate apartments who just text each other.
Systems built on shared memory or shared disk are called parallel DBMSs, not distributed, because processors communicate without exchanging messages over a network. Shared-nothing is also considered a parallel database environment — next slide explains why.""",
                   cue='Roommate analogy for each column.')
    archs = [('Shared memory', 'disk + memory shared', 'tight · "shared-everything"', 'Share kitchen and fridge', True, True),
             ('Shared disk', 'only disk shared', 'loose', 'Share only the fridge', False, True),
             ('Shared nothing', 'nothing shared; fast interconnect', 'bus or switch', 'Separate apartments, text each other', False, False)]
    for i, (t, s, c, a, smem, sdisk) in enumerate(archs):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 1.65, 3.9, 4.95, fill='soft', radius=0.05)
        text(sl, x + 0.25, 1.75, 3.4, 0.45, t, size=21, color='ink', bold=True)
        text(sl, x + 0.25, 2.2, 3.4, 0.4, s, size=14, color='muted')
        for k in range(3):
            px = x + 0.3 + k * 1.15
            box(sl, px, 2.8, 0.95, 0.5, 'CPU', fill='blue', color='white', size=12, bold=True)
            if not smem:
                box(sl, px, 3.4, 0.95, 0.45, 'Mem', fill='blue_s', color='blue_d', size=12, bold=True)
            if not sdisk:
                db(sl, px + 0.1, 3.95, 0.75, 0.65, '', fill='orange_s', line_c='orange_m')
        if smem:
            box(sl, x + 0.3, 3.4, 3.25, 0.45, 'Shared memory', fill='blue_s', color='blue_d', size=12, bold=True)
        if sdisk:
            db(sl, x + 1.3, 3.95, 1.3, 0.7, 'Shared disk', fill='orange_s', line_c='orange_m', color='orange', size=11)
        else:
            box(sl, x + 0.3, 4.75, 3.25, 0.35, 'switch / bus', fill='white', line='line', size=11, color='muted')
        text(sl, x + 0.25, 5.2, 3.4, 0.35, c, size=13, color='muted')
        box(sl, x + 0.2, 5.6, 3.5, 0.8, a, fill='orange_s', color='orange', size=14, bold=True)

    sl = D.slide('Parallel vs. distributed: three pictures', sec='23.7.1 · Fig. 23.7', say="""
Figure 23.7 shows three architectures.
Picture a: shared-nothing. Several identical computers, each with CPU, memory and its own database, connected by a switch. It looks like a distributed database, but there is a key difference: the nodes are symmetric and homogeneous — all the same. So it counts as a parallel database.
Picture b: a centralized database with distributed access. Only the central site in Chicago has the database; the other cities just connect to it over the network. That is not a distributed database either — the data isn't distributed.
Picture c: a truly distributed database. Every site has its own database, connected by a communications network — and different hardware and operating systems at each site are very common.
So the test is: is the data really spread across autonomous sites, and are those sites allowed to be different?""",
                   cue='a: same nodes; b: only one DB; c: real DDB.')
    titles = [('(a) Shared-nothing', 'Identical nodes → **parallel** DB'), ('(b) Centralized, networked', 'Only one site has data → **not** a DDB'),
              ('(c) Truly distributed', 'Data at every site, often different hardware/OS')]
    for i, (t, s) in enumerate(titles):
        x = 0.6 + i * 4.1
        box(sl, x, 1.65, 3.9, 4.0, fill='soft', radius=0.05)
        text(sl, x + 0.2, 1.75, 3.5, 0.45, t, size=19, color='ink', bold=True)
        text(sl, x + 0.2, 4.85, 3.5, 0.75, s, size=14, color='body')
    for k in range(3):
        db(sl, 0.95 + k * 1.15, 2.4, 0.75, 0.85, 'DB', size=11)
    box(sl, 0.9, 3.65, 3.3, 0.45, 'switch', fill='white', line='line', size=12, color='muted')
    box(sl, 4.95, 3.6, 3.2, 0.45, 'network', fill='white', line='line', size=12, color='muted')
    db(sl, 6.1, 2.3, 0.9, 1.0, 'Chicago', size=10)
    for k, c in enumerate(['SF', 'NY', 'LA', 'ATL']):
        box(sl, 4.95 + k * 0.82, 4.2, 0.72, 0.45, c, fill='white', line='line', size=11, color='muted')
    box(sl, 9.05, 3.6, 3.3, 0.45, 'communications network', fill='white', line='line', size=12, color='muted')
    for k in range(4):
        f, lc = [('blue_s', 'blue'), ('orange_s', 'orange_m'), ('green_s', 'green_m'), ('blue_s', 'blue')][k]
        db(sl, 9.05 + k * 0.85, 2.4, 0.7, 0.85, f'S{k + 1}', fill=f, line_c=lc, size=11)
    takeaway(sl, 'A real DDB: data spread over **autonomous**, often **different** sites.', y=5.9)

    sl = D.slide('Pure DDB architecture: GCS, LCS, LIS', sec='23.7.2 · Fig. 23.8', say="""
Now the schema architecture of a pure distributed database. It extends the three-level architecture from Chapter 2 to many sites.
At the top, users see external views.
[click] Below that is the global conceptual schema, the GCS. It is one unified, consistent logical view of all the data at all nodes, as if it were one database. The GCS gives network transparency.
Each site then has a local conceptual schema, LCS — the logical organization of the data at that site — and a local internal schema, LIS — the physical storage at that site. Because each site has its own LIS, sites can be different — this allows heterogeneity.
The mappings between the GCS and the LCSs provide fragmentation and replication transparency.
Analogy: a shopping mall directory is the GCS: one map of all shops. Each shop has its own floor plan — that's the LCS — and its own storeroom layout — the LIS.""",
                   cue='Top-down: views → GCS → per-site LCS → LIS.')
    for k in range(2):
        box(sl, 1.6 + k * 3.0, 1.6, 2.6, 0.55, 'External view', fill='white', line='line', size=14, color='body')
        line(sl, 2.9 + k * 3.0, 2.15, 2.9 + k * 3.0, 2.45, color='faint', w=2)
    box(sl, 0.6, 2.5, 7.4, 0.75, 'Global Conceptual Schema (GCS)', fill='blue', color='white', size=19, bold=True)
    for k, s in enumerate(['Site 1', 'Site 2', 'Site n']):
        x = 0.6 + k * 2.55
        line(sl, 4.3, 3.25, x + 1.1, 3.6, color='faint', w=2)
        box(sl, x, 3.6, 2.3, 2.5, fill='soft', radius=0.06)
        text(sl, x, 3.65, 2.3, 0.35, s, size=14, color='ink', bold=True, align='c')
        box(sl, x + 0.2, 4.05, 1.9, 0.5, 'LCS', fill='blue_s', color='blue_d', size=14, bold=True)
        box(sl, x + 0.2, 4.65, 1.9, 0.5, 'LIS', fill='orange_s', color='orange', size=14, bold=True)
        db(sl, x + 0.75, 5.25, 0.8, 0.7, '', size=10)
    expl = [('GCS', 'One logical view of all data → **network transparency**', 'blue'),
            ('LCS', 'Logical data at each site. GCS↔LCS mappings → **fragmentation & replication transparency**', 'blue_d'),
            ('LIS', 'Physical storage at each site → room for **heterogeneity**', 'orange')]
    for i, (a, b, c) in enumerate(expl):
        step(sl)
        y = 1.6 + i * 1.12
        box(sl, 8.4, y, 4.33, 1.0, [(a, 16, c), (b, 13, 'body')], fill='white', line='line', size=14, align='l', pad=0.2, gap=0.08, bold=False)
    callout(sl, 8.4, 5.0, 4.33, 1.4, 'Mall directory = GCS. Each shop\'s floor plan = LCS; its storeroom = LIS.', size=14)

    sl = D.slide('Who does what: global vs. local components', sec='23.7.2', say="""
The same figure also shows the components.
On the global level: the global query compiler checks the query against the global conceptual schema and its constraints, using the global system catalog. The global query optimizer uses both the global and local schemas to turn a global query into optimized local queries. It estimates the cost of each candidate plan from CPU, I/O and network delay, plus the estimated sizes of intermediate results — very important for joins, as Member 4 showed — and picks the cheapest. The global transaction manager coordinates execution across sites, together with the local transaction managers.
[click] On the local level, every site keeps its own local query optimizer, local transaction manager, execution engine, and local system catalog with its local schemas.
So it is a two-level team: a global planner on top, and local workers at each site.""",
                   cue='Top row global, bottom row local.')
    glob = [('Global query compiler', 'checks the query against the GCS (global catalog)'),
            ('Global query optimizer', 'global → optimized local queries; cost = CPU + I/O + network + intermediate sizes'),
            ('Global transaction manager', 'coordinates execution across sites with the local TMs')]
    text(sl, 0.6, 1.6, 12, 0.4, 'GLOBAL', size=14, color='blue', bold=True)
    for i, (a, b) in enumerate(glob):
        x = 0.6 + i * 4.1
        box(sl, x, 2.0, 3.9, 1.65, [a, (b, 13, 'blue_s')], fill='blue', color='white', size=17, bold=True, gap=0.15)
    for i in range(3):
        line(sl, 2.55 + i * 4.1, 3.7, 2.55 + i * 4.1, 4.15, color='faint', w=2.5, head='both')
    step(sl)
    text(sl, 0.6, 4.2, 12, 0.4, 'LOCAL (at every site)', size=14, color='green', bold=True)
    for i, t in enumerate(['Local query optimizer', 'Local transaction manager', 'Local execution engine', 'Local system catalog']):
        x = 0.6 + i * 3.08
        box(sl, x, 4.6, 2.95, 1.0, t, fill='green_s', color='green', size=16, bold=True)
    takeaway(sl, 'A global **planner** on top, local **workers** at each site.', y=5.9)

    sl = D.slide('Federated databases: a five-level schema', sec='23.7.3 · Fig. 23.9', say="""
Federated systems need more levels, because the components are independent. This is the five-level architecture from Sheth and Larson, 1990. Read it bottom-up.
[click] Level 1, local schema: the full conceptual schema of a component database, in its own data model.
[click] Level 2, component schema: the local schema translated into a common data model, the CDM, with mappings for commands. Now all components "speak the same language".
[click] Level 3, export schema: the subset of the component schema that the component is willing to share with the federation. This is how a component keeps its association autonomy.
[click] Level 4, federated schema: the global schema that integrates all the shareable export schemas.
[click] Level 5, external schema: a view for one user group or application.
Analogy: a shop's full inventory is the local schema; translating it into a standard format is the component schema; the shop window — only what it wants to show — is the export schema; the whole mall's catalog is the federated schema; and a "kids' shopping" guide is an external schema.""",
                   cue='Bottom-up; stop on "export = shop window".')
    levels = [('5 · External', 'a view for one user group / application', 'Kids\' shopping guide', 'soft', 'body'),
              ('4 · Federated', 'integrates all export schemas', 'Whole-mall catalog', 'blue_s', 'blue_d'),
              ('3 · Export', 'the part a component **chooses to share**', 'Shop window', 'orange_s', 'orange'),
              ('2 · Component', 'local schema translated to the common data model (CDM)', 'Inventory in a standard format', 'blue_s', 'blue_d'),
              ('1 · Local', 'full conceptual schema of a component DB', 'Shop\'s full inventory', 'soft', 'body')]
    for i, (a, b, an, f, c) in reversed(list(enumerate(levels))):
        step(sl)
        y = 1.65 + i * 0.93
        w = 5.6 + i * 0.5
        box(sl, 0.6, y, 2.6, 0.8, a, fill=f, color=c, size=17, bold=True)
        box(sl, 3.3, y, 5.4, 0.8, b, fill='white', line='line', size=15, color='body', align='l', pad=0.2)
        box(sl, 8.85, y, 3.88, 0.8, an, fill='orange_s' if i == 2 else 'white', line=None if i == 2 else 'line', color='orange', size=14, bold=True)
    text(sl, 8.85, 6.35, 3.88, 0.4, 'Analogy: a shopping mall', size=12, color='muted', align='c')
    text(sl, 0.6, 6.35, 8, 0.4, 'Export schemas protect **association autonomy**; the CDM + federation give **interoperability**.', size=14, color='muted')

    sl = D.slide('Federation in practice: a hospital network', kicker='IN PRACTICE · PART 5', say="""
Here is what a federated system looks like in real life.
Picture three hospitals in one region. Hospital A runs PostgreSQL, Hospital B runs Oracle, and a small clinic still keeps records in old files. Each has its own IT team and its own patients — full autonomy. None of them will give up its system.
[click] But the region wants one portal where a doctor can see a patient's history from all three. So each hospital exports only a subset — say, diagnoses and allergies, not billing. That's the export schema, and the portal integrating them is the federated schema.
[click] And now semantic heterogeneity bites. Is 03/04 the third of April or the fourth of March? Is the patient identified by national ID or by insurance number? Is weight in kilograms or pounds? Every one of these must be mapped, or the portal shows wrong data.
[click] Tools exist for this: query-federation engines such as Trino — formerly PrestoSQL — let you run one SQL query across many different databases. Exactly the FDBS idea.""",
                   cue='Hospitals story; three clicks.')
    for k, (t, s) in enumerate([('Hospital A', 'PostgreSQL'), ('Hospital B', 'Oracle'), ('Clinic C', 'old files')]):
        x = 0.8 + k * 2.55
        db(sl, x + 0.55, 3.75, 1.1, 1.05, '', size=11)
        text(sl, x, 4.85, 2.2, 0.6, [t, (s, 13, 'muted')], size=15, color='ink', bold=True, align='c', gap=0.05)
    step(sl)
    box(sl, 1.5, 1.6, 5.9, 0.8, 'Regional health portal  =  federated schema', fill='blue', color='white', size=17, bold=True)
    for k in range(3):
        x = 0.8 + k * 2.55
        line(sl, x + 1.1, 3.7, 4.45, 2.45, color='blue', w=2, flow=True)
        box(sl, x + 0.2, 2.9, 1.8, 0.45, 'export', fill='orange_s', color='orange', size=13, bold=True)
    text(sl, 0.6, 5.6, 7.2, 0.8, 'Each hospital shares **only a subset** (diagnoses, allergies — not billing).', size=15, color='body')
    step(sl)
    box(sl, 8.1, 1.6, 4.63, 2.75, [('Semantic traps', 17, 'red'), '• 03/04 = 3 April or 4 March?', '• Patient ID: national ID or insurance no.?', '• Weight in kg or lb?'],
        fill='red_s', align='l', anchor='t', pad=0.3, size=15, color='ink', gap=0.35)
    step(sl)
    box(sl, 8.1, 4.55, 4.63, 1.9, [('Tools', 17, 'blue'), 'Query-federation engines such as **Trino** run one SQL query across many different databases.'],
        fill='blue_xs', align='l', anchor='t', pad=0.3, size=15, color='ink', gap=0.3)

    sl = D.slide('Three-tier client/server', sec='23.7.4 · Fig. 23.10', say="""
Full-scale distributed DBMSs are actually rare in practice. Most distributed database applications today are built on a three-tier client/server architecture — especially on the web.
A restaurant is the perfect picture.
[click] Tier 1, the presentation layer or client: the web browser, with HTML and JavaScript. It handles user input and output. That's the customer at the table.
[click] Tier 2, the application server: the business logic, written in Java, C#, and so on. It builds queries, checks security and identity, and formats results. That's the waiter: takes the order, checks it, brings the food.
[click] Tier 3, the database server: query and transaction processing — SQL, stored procedures, often returning XML. That's the kitchen.
The tiers talk through standard interfaces: HTTP between browser and application server, and ODBC, JDBC, SQL/CLI or SQLJ between the application server and the database.""",
                   cue='Restaurant: customer, waiter, kitchen.')
    tiers = [('1 · Client (presentation)', 'Web browser, HTML, JavaScript — input & output', 'Customer', 'soft'),
             ('2 · Application server (business logic)', 'Java, C#… builds queries, checks security, formats results', 'Waiter', 'blue_s'),
             ('3 · Database server', 'SQL, stored procedures, results often as XML', 'Kitchen', 'orange_s')]
    links = ['HTTP', 'ODBC · JDBC · SQL/CLI · SQLJ']
    for i, (a, b, an, f) in enumerate(tiers):
        step(sl)
        y = 1.65 + i * 1.6
        box(sl, 0.6, y, 8.4, 1.15, [a, (b, 14, 'body')], fill=f, color='ink', size=18, bold=True, align='l', pad=0.3, gap=0.1)
        box(sl, 9.3, y, 3.43, 1.15, an, fill='orange_s', color='orange', size=20, bold=True)
        if i < 2:
            line(sl, 2.0, y + 1.17, 2.0, y + 1.58, color='faint', w=2.5, head='both')
            text(sl, 2.2, y + 1.18, 5, 0.4, links[i], size=13, color='muted', bold=True)
    takeaway(sl, 'Most "distributed" apps are built this way, not on a full DDBMS.', y=6.35)

    sl = D.slide('The application server as the coordinator', sec='23.7.4', say="""
In this architecture, the application server can play the role of the distributed coordinator. It keeps a data dictionary that says how data is distributed among the database servers, and it has modules to decompose global queries.
Here's how a query flows. [click] Step 1: the application server builds the query from the client's input and decomposes it into independent site queries, each sent to the right database server. [click] Step 2: each database server runs its local query and sends the result back — increasingly as XML. [click] Step 3: the application server combines the results, formats them, for example into HTML, and sends them to the client.
[click] So who handles the hard distributed problems? The application server is responsible for: generating a distributed execution plan, keeping replicas consistent, and global recovery and atomicity.
If the DDBMS offers distribution transparency, the application server can just write global queries as if the database were centralized.""",
                   cue='Follow ① ② ③; then the three responsibilities.')
    box(sl, 4.6, 1.65, 4.1, 0.75, 'Application server', fill='blue', color='white', size=18, bold=True)
    for k in range(3):
        x = 1.6 + k * 3.6
        line(sl, 6.65, 2.4, x + 0.6, 3.25, color='blue', w=2.2, flow=True)
        db(sl, x, 3.3, 1.2, 1.0, f'DB server {k + 1}', size=10)
    box(sl, 0.6, 1.65, 3.6, 0.75, 'Client', fill='soft', color='body', size=16, bold=True)
    line(sl, 4.25, 2.02, 4.55, 2.02, color='faint', w=2.5, head='both')
    steps = ['Decompose the user query into **site queries** and send each to its DB server.',
             'Each DB server runs its **local query** and returns the result (often XML).',
             'Combine the results, format as **HTML**, send to the client.']
    for i, s in enumerate(steps):
        step(sl)
        y = 4.6 + i * 0.6
        numdot(sl, 0.6, y, i + 1, d=0.45, size=15)
        text(sl, 1.2, y - 0.04, 6.6, 0.55, s, size=15, color='body', anchor='m')
    step(sl)
    box(sl, 8.2, 4.55, 4.53, 1.85, [('It is responsible for:', 15, 'ink'), '• distributed execution plan', '• replica consistency', '• global recovery & atomicity'],
        fill='orange_s', align='l', anchor='t', pad=0.25, size=15, gap=0.15, color='body')

    sl = D.slide('Distributed catalogs: who knows where things are?', sec='23.8', say="""
Last topic: the catalog. A catalog is itself a database — the metadata saying which tables, fragments and copies exist, and where. Think of a company phone directory. There are three schemes.
[click] Centralized: the whole catalog sits at one site — one directory at head office. Easy to build, but it hurts reliability, availability and autonomy. A remote read locks the entry at the centre, copies it, then sends an acknowledgment to unlock it, and every update goes through the centre — a bottleneck for write-heavy applications.
[click] Fully replicated: a complete copy at every site — a printed directory in every office. Reads are local and fast, but every update is broadcast to all sites as a transaction under centralized two-phase commit, so many writes mean heavy network traffic.
[click] Partially replicated: each site keeps the full catalog for its own data and may cache entries from other sites, with no guarantee they're fresh. Changes go straight to the object's birth site — where it was created — and stale caches are refreshed on next use. Synonyms for remote objects keep transparency. This scheme preserves site autonomy.
Now let me wrap up the whole chapter.
""",
                   cue='Three cards, one analogy each.')
    sch = [('Centralized', 'Whole catalog at **one** site.', ['✓ Easy to implement', '✗ Hurts reliability, availability, autonomy', '✗ All updates via the centre → bottleneck'], 'One directory at head office'),
           ('Fully replicated', 'A **complete copy** at every site.', ['✓ Fast local reads', '✗ Every update broadcast to all sites (centralized 2PC)', '✗ Write-heavy → heavy traffic'], 'A printed directory in every office'),
           ('Partially replicated', 'Each site: its **own data** + cached remote entries.', ['✓ Preserves site autonomy', '• Changes go to the object\'s **birth site**', '• Stale caches refreshed on next access'], 'Own staff list + a few saved numbers')]
    for i, (t, s, pts, an) in enumerate(sch):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 1.65, 3.9, 4.95, fill='soft', radius=0.05)
        text(sl, x + 0.25, 1.75, 3.4, 0.45, t, size=21, color='ink', bold=True)
        text(sl, x + 0.25, 2.25, 3.45, 0.8, s, size=15, color='body')
        text(sl, x + 0.25, 3.05, 3.45, 2.3, pts, size=14, color='body', gap=0.35)
        box(sl, x + 0.2, 5.6, 3.5, 0.8, an, fill='orange_s', color='orange', size=14, bold=True)
    text(sl, 0.6, 6.68, 12, 0.3, 'A catalog is itself a database of metadata. The right scheme depends on the data and the access patterns.', size=12, color='muted')

    D.part = 6
    sl = D.slide('Chapter 23 in five sentences', kicker='SUMMARY  ·  §23.9', say="""
Let me summarize the whole chapter in five sentences — one per part.
[click] Part 1: a distributed database spreads logically related data over networked sites, and transparency hides that distribution from users — at the cost of some overhead.
[click] Part 2: we cut tables into fragments that must be complete and rebuildable, and replicate them where they are used — buying availability and locality at an update cost.
[click] Part 3: locking uses distinguished copies, elections and voting; two-phase commit gives atomicity but can block; three-phase commit removes the block.
[click] Part 4: the network dominates query cost, so we minimize bytes transferred — and the semijoin wins when few rows take part in the join.
[click] Part 5: real systems range from pure DDBMSs to federated and multidatabase systems, and in practice they are held together by three-tier application servers and distributed catalogs.""",
                   cue='One sentence per part. Slow down.')
    summ = [('Foundations', 'Data spread over sites; **transparency** hides it (at some overhead).'),
            ('Design', 'Fragments must be **complete & rebuildable**; replication buys availability at an update cost.'),
            ('Correctness', 'Distinguished copies, elections, voting; **2PC** is atomic but blocks — **3PC** doesn\'t.'),
            ('Queries', 'The **network** dominates cost; **semijoin** wins when few rows join.'),
            ('Systems', 'Pure DDBMS → **federated** → multidatabase; held together by app servers and catalogs.')]
    for i, (a, b) in enumerate(summ):
        step(sl)
        y = 1.65 + i * 0.95
        box(sl, 0.6, y, 12.13, 0.82, fill='soft', shape='round', radius=0.15)
        numdot(sl, 0.8, y + 0.16, i + 1, d=0.5, size=17)
        text(sl, 1.5, y, 2.4, 0.82, a, size=19, color='blue', bold=True, anchor='m')
        text(sl, 3.9, y, 8.7, 0.82, b, size=17, color='body', anchor='m')

    sl = D.slide('Where this leads next', kicker='SUMMARY  ·  §23.9', say="""
And where does this lead? [click] Everything in this chapter is the base for the next two chapters.
[click] Chapter 24, NoSQL: systems like MongoDB or Cassandra are basically distributed databases built for huge scale. Sharding is horizontal fragmentation; their replication and consistency choices are exactly the trade-offs we discussed; and partition tolerance is at the heart of the CAP theorem.
[click] Chapter 25, big data and cloud: MapReduce and Hadoop process data where it is stored — the same "don't ship the data" idea Member 4 showed with the semijoin.
To practise, the book's review questions 23.13 to 23.17 and 23.19 to 23.23 are a good check.""",
                   cue='Connect three ideas to NoSQL and big data.')
    flow = [('Ch. 23', 'Distributed DB concepts', 'Fragmentation · replication · commit · query cost', 'blue'),
            ('Ch. 24', 'NoSQL', 'Sharding · replication · CAP & partition tolerance', 'orange_m'),
            ('Ch. 25', 'Big data & cloud', 'MapReduce · Hadoop · move computation to the data', 'green_m')]
    for i, (a, b, c, f) in enumerate(flow):
        step(sl)
        x = 0.6 + i * 4.15
        box(sl, x, 1.9, 3.8, 3.0, fill='soft', radius=0.06)
        box(sl, x, 1.9, 3.8, 0.75, a, fill=f, color='white', size=20, bold=True, shape='rect')
        text(sl, x + 0.15, 2.85, 3.5, 0.6, b, size=19, color='ink', bold=True, align='c')
        text(sl, x + 0.25, 3.6, 3.3, 1.2, c, size=15, color='body', align='c')
        if i < 2:
            line(sl, x + 3.85, 3.4, x + 4.1, 3.4, color='faint', w=3)
    text(sl, 0.6, 5.4, 12.13, 0.5, 'Practice: review questions **23.13 – 23.17** and **23.19 – 23.23**.', size=17, color='body', align='c')

    sl = D._new()
    D._record(sl, 'Thank you — questions?', say="""
That's the end of our presentation. Thank you very much for listening.
We are happy to take your questions now — about any part. Each of us will answer questions about our own part.""",
              cue='All members come to the front. Q&A, ~8 minutes.')
    box(sl, 0, 0, 13.333, 7.5, fill='blue', shape='rect')
    text(sl, 1.0, 2.2, 11, 1.3, 'Thank you!', size=66, color='white', bold=True)
    text(sl, 1.0, 3.6, 11, 0.8, 'Questions?', size=36, color='blue_s')
    parts = ['1 · Foundations', '2 · Design', '3 · Correctness', '4 · Queries', '5 · Systems']
    for i, t in enumerate(parts):
        box(sl, 1.0 + i * 2.3, 5.0, 2.15, 0.6, t, fill='blue_d', color='white', size=14, bold=True)
    D._footer(sl, len(D.entries), dark=True)
