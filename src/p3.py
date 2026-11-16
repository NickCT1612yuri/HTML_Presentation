from deck import *


def seq_lane(sl, x, y0, y1, label, fill='blue'):
    box(sl, x - 0.85, y0, 1.7, 0.55, label, fill=fill, color='white', size=15, bold=True)
    line(sl, x, y0 + 0.55, x, y1, color='line', w=2, head=None, dash=True)


def msg(sl, x1, x2, y, label, color='blue', above=True, size=14):
    line(sl, x1, y, x2, y, color=color, w=2.5)
    lx = min(x1, x2)
    text(sl, lx, y - (0.36 if above else -0.04), abs(x2 - x1), 0.33, label, size=size, color=color,
         bold=True, align='c')


def build(D):
    D.divider(3, ['Five problems a single-site DBMS never has', 'Locking with a distinguished copy, elections and voting',
                  'Distributed recovery and commit', 'Two-phase commit, its flaw, and three-phase commit'],
              say="""
Thank you. I'm Member 3. My part — sections 23.3 and 23.4 — is about correctness.
Member 2 just showed that one UPDATE can turn into work on several sites. Now: how do we make sure all those sites agree, even when machines crash and messages get lost? We'll look at locking, recovery, and the famous two-phase commit protocol.""")

    sl = D.slide('Five problems a single-site DBMS never has', sec='23.3', say="""
In a centralized database, concurrency control and recovery are already solved — Chapters 21 and 22. Distribution adds five new problems.
[click] One, multiple copies. If a data item is replicated, all copies must stay consistent. And when a site comes back after a failure, its copies must be brought up to date.
[click] Two, failure of individual sites. The rest of the system should keep going, and a recovered site must catch up before it rejoins.
[click] Three, failure of communication links. In the worst case, the network is partitioned, like Member 1 described.
[click] Four, distributed commit. A transaction that touched several sites must commit everywhere or nowhere — even if a site fails in the middle. That is what two-phase commit solves.
[click] Five, distributed deadlock. Transaction A waits for B at one site, B waits for A at another site. No single site sees the cycle.
[click] The key difference: in a centralized system, a crash stops everything. In a distributed system, some sites are up, some are down — and ACID must still hold.""",
                   cue='One sentence per card; spend time on #4 and #5.')
    probs = [('Multiple copies', 'Keep replicas consistent; refresh a copy after its site recovers.'),
             ('Site failures', 'Others keep running; the failed site catches up before rejoining.'),
             ('Link failures', 'Worst case: network partition.'),
             ('Distributed commit', 'Commit at **all** sites or **none**, even if one fails mid-way → 2PC.'),
             ('Distributed deadlock', 'A waits for B on site 1, B waits for A on site 2. No single site sees the cycle.')]
    for i, (t, d) in enumerate(probs):
        step(sl)
        x = 0.6 + i * 2.45
        box(sl, x, 1.7, 2.3, 3.4, fill='soft', radius=0.06)
        numdot(sl, x + 0.2, 1.9, i + 1, d=0.55, size=20, fill='orange_m' if i >= 3 else 'blue')
        text(sl, x + 0.2, 2.6, 1.95, 0.8, t, size=18, color='ink', bold=True)
        text(sl, x + 0.2, 3.35, 1.95, 1.7, d, size=14, color='body')
    step(sl)
    box(sl, 0.6, 5.35, 5.9, 1.2, [('**Centralized**', 17), ('One crash → everything stops. Simple.', 15)], fill='white', line='line', align='l', pad=0.25, gap=0.15, color='body')
    box(sl, 6.83, 5.35, 5.9, 1.2, [('**Distributed**', 17), ('Some sites up, some down, network split… and ACID must still hold.', 15)], fill='orange_s', align='l', pad=0.25, gap=0.15, color='body')

    sl = D.slide('Locking with a "distinguished copy"', sec='23.3.1', say="""
How do we lock data that has several copies? The idea: for each data item, we choose one copy to be the distinguished copy. All the locks for that item live with this copy, and every lock and unlock request is sent to its site.
[click] Think of an office with three identical meeting rooms booked through one receptionist. You can sit in any room, but bookings always go through that one receptionist, so two people never book the same slot.
In the diagram, transaction T at Site 1 wants item X. Copies of X exist at Sites 1, 2 and 3, but the distinguished copy is at Site 2. So T sends its lock request to Site 2 — that site acts as the coordinator for X.
[click] Two rules: once you have a read lock, you may read any copy — usually the nearest one. Once you have a write lock and change X, the DDBMS must update all copies before releasing the lock.
The methods on the next slides differ only in where the distinguished copies are kept.""",
                   cue='Follow the lock request arrow to Site 2.')
    for i, (lab, dist) in enumerate([('Site 1', False), ('Site 2', True), ('Site 3', False)]):
        x = 1.0 + i * 2.6
        server(sl, x, 2.5, 1.1, 1.2, label=lab, accent='orange_m' if dist else 'blue', line_c='orange_m' if dist else 'line')
        box(sl, x + 0.1, 3.95 + 0.2, 0.9, 0.45, 'X ★' if dist else 'X', fill='orange_s' if dist else 'blue_s',
            color='orange' if dist else 'blue_d', size=15, bold=True)
    box(sl, 0.4, 1.55, 1.6, 0.6, 'Transaction T', fill='blue', color='white', size=14, bold=True)
    line(sl, 2.0, 1.85, 3.9, 2.45, color='orange_m', w=2.5)
    text(sl, 2.2, 1.45, 2.6, 0.4, 'lock(X)?', size=15, color='orange', bold=True)
    text(sl, 1.0, 4.85, 7, 0.4, '★ = distinguished copy: it holds the locks for X', size=14, color='orange', bold=True)
    step(sl)
    callout(sl, 8.6, 1.55, 4.13, 2.1, 'Three identical rooms, **one receptionist** for all bookings.', size=15)
    step(sl)
    box(sl, 8.6, 3.85, 4.13, 1.1, [('Read lock granted', 15, 'blue'), '→ read **any** copy (the nearest)'], fill='blue_xs', size=14, align='l', pad=0.2, gap=0.1, color='body')
    box(sl, 8.6, 5.1, 4.13, 1.1, [('Write lock granted', 15, 'blue'), '→ update **all** copies before release'], fill='blue_xs', size=14, align='l', pad=0.2, gap=0.1, color='body')
    text(sl, 0.6, 5.5, 7.8, 0.9, 'The methods that follow differ only in **where** the distinguished copies are kept.', size=16, color='muted')

    sl = D.slide('Three ways to place the distinguished copies', sec='23.3.1', say="""
Here are the three methods side by side.
[click] Primary site: all distinguished copies are at one single site. That site is the coordinator for every item. It's a simple extension of centralized locking — with two-phase locking, schedules are serializable. But all lock requests go to one site, which becomes a bottleneck, and if it fails, the whole system is paralyzed.
[click] Primary site with backup: all locking information is kept at the primary and also at a backup site. If the primary fails, the backup takes over. That fixes the paralysis, but locking gets slower — every lock has to be recorded at both sites — and the overload problem remains.
[click] Primary copy: the distinguished copies of different items are spread over different sites. This spreads the load. If one site fails, only transactions that need locks on items whose primary copy is there are affected. It can also use backups.
Analogy: one receptionist for the whole building; one receptionist plus an assistant who copies every booking; or one receptionist per floor.""",
                   cue='Compare the three pictures left to right, then read the plus/minus rows.')
    meths = [('Primary site', 'All locks at **one** site', ['✓ Simple; with 2PL → serializable', '✗ Bottleneck', '✗ Its failure paralyzes the system'], 'One receptionist for the building'),
             ('Primary site + backup', 'Locks at primary **and** backup', ['✓ Backup takes over on failure', '✗ Slower: record at both', '✗ Overload remains'], '… plus an assistant who copies every booking'),
             ('Primary copy', 'Locks **spread** across sites', ['✓ Load is distributed', '✓ A failure affects only items coordinated there', '• Can also use backups'], 'One receptionist per floor')]
    for i, (t, s, pts, an) in enumerate(meths):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 1.65, 3.9, 4.95, fill='soft', radius=0.05)
        text(sl, x + 0.25, 1.75, 3.5, 0.5, t, size=21, color='ink', bold=True)
        text(sl, x + 0.25, 2.2, 3.5, 0.4, s, size=15, color='body')
        for k in range(4):
            if i == 0:
                star = k == 0
            elif i == 1:
                star = k in (0, 1)
            else:
                star = True
            sx = x + 0.3 + k * 0.85
            box(sl, sx, 2.75, 0.7, 0.8, '★' if star else '', fill='white', line='orange_m' if star else 'line',
                size=16, color='orange', bold=True, radius=0.15)
            if i == 1 and k == 1:
                text(sl, sx - 0.2, 3.55, 1.1, 0.3, 'backup', size=11, color='orange', align='c')
        text(sl, x + 0.25, 3.95, 3.5, 1.6, pts, size=15, color='body', gap=0.25)
        box(sl, x + 0.2, 5.65, 3.5, 0.75, an, fill='orange_s', color='orange', size=13, bold=True)

    sl = D.slide('When the coordinator fails: elections', sec='23.3.1', say="""
What happens when a coordinator site fails? It depends on the method.
With primary site and no backup, it's painful: all running transactions are aborted and restarted, and a new primary site and lock manager are created.
With a backup, processing is suspended while the backup becomes the new primary, a new backup is chosen, and all lock information is copied to it.
But what if there is no backup, or both are down? Then the surviving sites hold an election.
Step one: some site Y keeps trying to contact the coordinator and fails, so it assumes the coordinator is down. [click] Step two: Y sends a message to all running sites, proposing itself as the new coordinator. Step three: as soon as Y gets a majority of yes votes, it declares itself the new coordinator.
[click] It's like a class whose class rep disappears: one student says "I'll do it", and once most of the class agrees, it's decided. The real algorithm also handles two sites trying at the same time.""",
                   cue='Walk through the three steps on the diagram.')
    server(sl, 0.9, 1.9, 1.0, 1.1, label='Old coordinator', accent='red_m', line_c='red_m')
    box(sl, 1.05, 2.05, 0.7, 0.8, '✕', fill=None, color='red', size=40, bold=True)
    server(sl, 4.2, 3.2, 1.0, 1.1, label='Site Y', accent='orange_m', line_c='orange_m')
    line(sl, 4.2, 3.4, 2.0, 2.6, color='red_m', w=2, dash=True)
    text(sl, 2.55, 2.4, 2.0, 0.4, 'no reply… ×3', size=13, color='red', bold=True)
    step(sl)
    for k, lab in enumerate(['A', 'B', 'C', 'D']):
        sx = 7.0 + (k % 2) * 1.6
        sy = 1.8 + (k // 2) * 2.0
        server(sl, sx, sy, 0.8, 0.9, label=f'Site {lab}')
        line(sl, 5.3, 3.75, sx - 0.05, sy + 0.45, color='orange_m', w=2)
        box(sl, sx + 0.1, sy + 1.32, 0.6, 0.4, 'yes' if k < 3 else 'no', fill='green_s' if k < 3 else 'red_s',
            color='green' if k < 3 else 'red', size=13, bold=True)
    text(sl, 4.3, 2.35, 1.7, 0.6, '"I propose\nmyself"', size=13, color='orange', bold=True)
    step(sl)
    steps = ['Y keeps failing to reach the coordinator → assumes it is down.', 'Y asks all running sites: "make me coordinator?"',
             'Majority says yes → Y is the new coordinator.']
    for i, s in enumerate(steps):
        y = 4.75 + i * 0.6
        numdot(sl, 0.6, y, i + 1, d=0.45, size=15, fill='orange_m')
        text(sl, 1.2, y - 0.04, 6.0, 0.55, s, size=15, color='body', anchor='m')
    box(sl, 10.4, 1.7, 2.33, 4.4, [('If coordinator fails…', 15, 'ink'), ('**No backup:** abort & restart all running transactions', 13),
                                   ('**Backup:** suspend; backup becomes primary; choose new backup', 13),
                                   ('**Neither:** election', 13)], fill='soft', align='l', anchor='t', pad=0.18, gap=0.5, color='body')

    sl = D.slide('Voting: no distinguished copy at all', sec='23.3.2', say="""
A completely different approach is voting. There is no distinguished copy. Every copy keeps its own lock table and decides for itself.
A transaction that wants to lock item X sends the request to every site that has a copy of X. Each site grants or denies its own lock. If the transaction gets a majority of grants within a time-out, it holds the lock and tells all copies. If not, it cancels the request and tells everyone.
[click] In the diagram, five copies: three grant, one denies, one is silent. Three out of five is a majority, so the lock is granted.
It's like a poll in a group chat: no single admin decides — majority wins.
The advantage: it is truly distributed, no single site is in charge. The disadvantage: much more message traffic than the distinguished-copy methods, and the algorithm becomes very complex if sites fail during voting.""",
                   cue='Count the votes on screen: 3 of 5.')
    box(sl, 5.2, 1.7, 2.9, 0.75, 'T wants lock(X)', fill='blue', color='white', size=17, bold=True)
    votes = [('grant', 'green'), ('grant', 'green'), ('grant', 'green'), ('deny', 'red'), ('silent', 'muted')]
    for i, (v, c) in enumerate(votes):
        x = 0.9 + i * 2.4
        line(sl, 6.65, 2.45, x + 0.5, 3.1, color='line', w=2)
        server(sl, x, 3.15, 1.0, 1.0, label=f'Copy {i + 1}')
        box(sl, x - 0.1, 4.55, 1.2, 0.5, v, fill={'green': 'green_s', 'red': 'red_s', 'muted': 'soft'}[c], color=c, size=15, bold=True)
    step(sl)
    box(sl, 0.6, 5.3, 4.2, 1.2, '3 of 5 grant → **majority** → lock held', fill='green_s', color='green', size=17)
    box(sl, 5.0, 5.3, 3.75, 1.2, [('✓ Truly distributed', 15, 'green'), ('✗ More messages; complex if sites fail mid-vote', 14, 'red')],
        fill='soft', size=14, align='l', pad=0.2, gap=0.15)
    callout(sl, 8.95, 5.3, 3.78, 1.2, 'A group-chat poll: no admin, majority wins.', size=14)

    sl = D.slide('Recovery: the silent reply problem', sec='23.3.3', say="""
Now recovery. The basic difficulty is that a site often cannot tell what went wrong.
Site X sends a message to site Y and waits for an answer. Nothing comes back. There are three possible explanations.
[click] One: the message was lost on the way, so Y never received it.
[click] Two: Y has crashed and could not answer.
[click] Three: Y received it, did the work, and replied — but the reply was lost.
[click] From X's point of view, these three look exactly the same: silence.
You know this from texting: you send a message, no answer. Did it not arrive? Is their phone dead? Or did they reply and it got stuck? You can't tell without sending more messages. And for a database this matters a lot: in case three, Y already did the work.""",
                   cue='Texting analogy; stress case 3 (work already done).')
    cases = [('Message lost', 'Y never received it.', 'lost_fwd'), ('Y is down', 'Y crashed, cannot answer.', 'down'),
             ('Reply lost', 'Y did the work and replied, but the reply was lost.', 'lost_back')]
    for i, (t, d, kind) in enumerate(cases):
        step(sl)
        y = 1.75 + i * 1.45
        box(sl, 0.6, y, 7.2, 1.25, fill='soft', radius=0.08)
        box(sl, 0.85, y + 0.3, 0.7, 0.65, 'X', fill='blue', color='white', size=20, bold=True)
        box(sl, 4.25, y + 0.3, 0.7, 0.65, 'Y', fill='faint' if kind == 'down' else 'blue', color='white', size=20, bold=True)
        if kind == 'lost_fwd':
            line(sl, 1.6, y + 0.62, 2.8, y + 0.62, color='blue', w=2.5, head=None)
            text(sl, 2.75, y + 0.35, 0.6, 0.55, '✕', size=22, color='red', bold=True, align='c')
        elif kind == 'down':
            line(sl, 1.6, y + 0.62, 4.2, y + 0.62, color='blue', w=2.5)
            text(sl, 4.95, y + 0.3, 0.5, 0.6, '✕', size=22, color='red', bold=True)
        else:
            line(sl, 1.6, y + 0.48, 4.2, y + 0.48, color='blue', w=2.5)
            line(sl, 4.2, y + 0.82, 3.2, y + 0.82, color='green_m', w=2.5, head=None)
            text(sl, 2.65, y + 0.6, 0.6, 0.5, '✕', size=20, color='red', bold=True, align='c')
        text(sl, 5.5, y + 0.12, 2.25, 1.0, [t, (d, 13, 'body')], size=16, color='ink', bold=True, gap=0.1, anchor='m')
    step(sl)
    box(sl, 8.1, 1.75, 4.63, 1.6, 'From X\'s side, all three look the same: **silence**.', fill='red_s', color='ink', size=18)
    callout(sl, 8.1, 3.55, 4.63, 2.6, 'You text a friend; no reply. Message not delivered? Phone dead? Or they replied and it got stuck?\nYou can\'t tell without more messages.', size=15)

    sl = D.slide('Distributed commit and the global transaction manager', sec='23.3.3 · 23.4', say="""
The second recovery problem is distributed commit. A transaction that updated several sites may commit only when every site has safely written its changes to its own log on disk. Otherwise a crash could lose part of the transaction. The standard solution is the two-phase commit protocol.
Who runs it? Section 23.4 adds a new component: the global transaction manager. The site where the transaction started temporarily plays this role and coordinates with the local transaction managers at the other sites.
[click] It offers the usual operations: BEGIN, READ, WRITE, END, COMMIT and ROLLBACK. And each has a distributed meaning, shown on the right. READ returns a local copy if one is valid. WRITE makes sure the update is visible at every site with a copy. COMMIT makes the effects permanent at all copies. And ABORT makes sure no effect remains at any site.
Together with the concurrency control and recovery managers, this guarantees ACID for distributed transactions.""",
                   cue='Left: the role. Right: what each operation guarantees.')
    box(sl, 0.6, 1.7, 5.4, 1.4, 'A transaction may commit only when **every site** has written its changes to its **log on disk**.', fill='orange_s', size=17, color='ink', align='l', pad=0.25)
    box(sl, 1.8, 3.45, 3.0, 0.8, 'Global transaction manager', fill='blue', color='white', size=15, bold=True)
    text(sl, 0.6, 4.25, 5.4, 0.4, '(the site where the transaction started)', size=13, color='muted', align='c')
    for k in range(3):
        x = 0.85 + k * 1.75
        line(sl, 3.3, 4.6, x + 0.7, 5.25, color='faint', w=2)
        box(sl, x, 5.3, 1.45, 0.75, f'Local TM\nsite {k + 1}', fill='blue_s', color='blue_d', size=13, bold=True)
    step(sl)
    ops = [['Operation', 'Guarantee across sites'], ['READ', 'Returns a valid local copy'], ['WRITE', 'Update visible at all replicas'],
           ['COMMIT', 'Effects permanent at all copies'], ['ABORT / ROLLBACK', 'No effect at any site']]
    grid(sl, 6.5, 1.7, [2.3, 3.93], ops, rowh=0.66, size=15, align='c', bold_first_col=True)
    text(sl, 6.5, 5.15, 6.2, 0.9, 'Also: BEGIN_TRANSACTION, END_TRANSACTION. Atomic COMMIT/ABORT is done with **two-phase commit (2PC)**.', size=15, color='muted')

    sl = D.slide('Two-phase commit (2PC)', sec='23.4.1', say="""
Two-phase commit was covered in Chapter 22, section 22.6; here is a quick recap, because the rest of my part depends on it.
There is one coordinator and several participants.
Phase 1, voting. The coordinator asks everyone: "PREPARE — can you commit?" [click] Each participant writes its changes to its log on disk and answers yes, or answers no.
[click] Phase 2, decision. If everyone voted yes, the coordinator logs the decision and sends GLOBAL COMMIT. If anyone said no, it sends GLOBAL ABORT. [click] Each participant does it locally and acknowledges.
[click] Analogy: a group trip. The organizer asks: "Can everyone come on Saturday?" Each friend checks their calendar and books the day off — that's voting yes. Only when everyone has said yes does the organizer say "Booked, we're going!" If one person says no, the trip is cancelled for everyone.""",
                   cue='Read the messages top to bottom; then the group-trip story.')
    box(sl, 0.4, 2.45, 12.4, 1.75, fill='blue_xs', shape='rect')
    box(sl, 0.4, 4.35, 12.4, 1.95, fill='green_s', shape='rect')
    text(sl, 0.45, 2.5, 1.4, 0.6, 'PHASE 1\nVOTING', size=11, color='blue', bold=True)
    text(sl, 0.45, 4.4, 1.4, 0.6, 'PHASE 2\nDECISION', size=11, color='green', bold=True)
    seq_lane(sl, 2.0, 1.65, 6.4, 'Coordinator', 'blue')
    seq_lane(sl, 6.6, 1.65, 6.4, 'Participant A', 'faint')
    seq_lane(sl, 9.4, 1.65, 6.4, 'Participant B', 'faint')
    msg(sl, 2.0, 9.4, 3.05, 'PREPARE: can you commit?')
    step(sl)
    msg(sl, 9.4, 2.0, 3.85, 'YES (changes in log on disk)', color='green', above=True)
    step(sl)
    box(sl, 2.15, 4.62, 2.3, 0.42, 'All yes → log COMMIT', fill='white', color='green', size=12, bold=True)
    msg(sl, 2.0, 9.4, 5.25, 'GLOBAL COMMIT', color='green')
    step(sl)
    msg(sl, 9.4, 2.0, 6.0, 'ACK (done locally)', color='muted')
    step(sl)
    box(sl, 10.4, 2.6, 2.3, 1.5, 'Any NO →\nGLOBAL ABORT', fill='red_s', color='red', size=15, bold=True)
    callout(sl, 10.35, 4.5, 2.4, 1.7, '"Saturday OK?" → all yes → "We\'re going!"', size=13, label='ANALOGY')

    sl = D.slide('The flaw of 2PC: it can block', sec='23.4.2', say="""
2PC has one big weakness: it is a blocking protocol.
Look at the timeline. Participants A and B voted yes. They are now in the "prepared" state: they promised to commit if asked, so they are not allowed to change their minds alone. While they wait, they keep holding their locks.
[click] Now the coordinator crashes, before telling them the decision. [click] What can A and B do? They cannot commit — maybe someone else voted no. They cannot abort — maybe the coordinator already told another site to commit. So they wait, holding locks, until the coordinator recovers. Other transactions that need those locks pile up behind them, and performance degrades. Other failure combinations can even make the outcome nondeterministic.
Back to the group trip: everyone said yes and has blocked Saturday on their calendar. Then the organizer's phone dies. Nobody knows if the trip is on, so nobody can make other plans.""",
                   cue='Pause on the "?" — let the audience feel the stuck state.')
    seq_lane(sl, 2.0, 1.65, 6.0, 'Coordinator', 'blue')
    seq_lane(sl, 6.6, 1.65, 6.0, 'Participant A', 'faint')
    seq_lane(sl, 9.4, 1.65, 6.0, 'Participant B', 'faint')
    msg(sl, 2.0, 9.4, 2.75, 'PREPARE')
    msg(sl, 9.4, 2.0, 3.45, 'YES  /  YES', color='green')
    step(sl)
    box(sl, 1.35, 3.85, 1.3, 1.0, '✕', fill='red_s', color='red', size=36, bold=True, shape='oval')
    text(sl, 0.4, 4.9, 3.3, 0.4, 'coordinator crashes', size=14, color='red', bold=True, align='c')
    step(sl)
    for x in (6.6, 9.4):
        box(sl, x - 1.0, 4.0, 2.0, 1.15, [('? waiting', 17, 'orange'), ('holding locks', 13, 'body')], fill='orange_s', size=15, bold=True, gap=0.1)
    step(sl)
    box(sl, 0.6, 5.85, 3.8, 0.85, 'Can\'t commit: maybe someone said no.', fill='soft', size=14, color='body')
    box(sl, 4.6, 5.85, 4.1, 0.85, 'Can\'t abort: maybe someone already committed.', fill='soft', size=14, color='body')
    box(sl, 8.9, 5.85, 3.83, 0.85, '→ **blocked** until coordinator recovers', fill='red_s', size=14, color='red')
    callout(sl, 10.75, 1.65, 2.0, 2.1, 'Organizer\'s phone dies after everyone said yes.', size=12, label='ANALOGY')

    sl = D.slide('Three-phase commit (3PC) removes the block', sec='23.4.2', say="""
Three-phase commit fixes this. It splits the second phase into two sub-phases: prepare-to-commit and commit.
[click] After everyone votes yes, the coordinator first sends PREPARE-TO-COMMIT, sometimes called precommit. This message says only one thing: "everyone voted yes." [click] Then, in a separate step, it sends COMMIT.
[click] Why does this help? If a participant has received precommit, it knows that all the others voted yes. If it has not received precommit, the decision cannot have been commit yet, so it is safe to abort.
[click] So when the coordinator crashes, another participant can take over and finish the job: it simply asks the others whether they received prepare-to-commit. If nobody did, abort. The state can be recovered no matter which participant crashes.
3PC also sets a maximum time-out for commit or abort, so locks are released on time-out — nobody waits forever.
Group trip: the organizer first posts "everyone said yes!" in the chat before sending the final booking. If the organizer then disappears, the friends can check the chat and decide together.""",
                   cue='Point at the new middle step; that message is what un-blocks the others.')
    phases = [('1 · Vote', 'PREPARE → YES / NO', 'blue_s', 'blue_d'),
              ('2a · Prepare-to-commit', '"Everyone voted yes."', 'orange_s', 'orange'),
              ('2b · Commit', 'Same as 2PC phase 2', 'green_s', 'green')]
    for i, (a, b, f, c) in enumerate(phases):
        if i:
            step(sl)
        x = 0.6 + i * 4.15
        box(sl, x, 1.7, 3.8, 1.3, [a, (b, 15, 'body')], fill=f, color=c, size=20, bold=True, gap=0.15, shape='round')
        if i < 2:
            line(sl, x + 3.85, 2.35, x + 4.1, 2.35, color='faint', w=3)
    text(sl, 4.75, 3.05, 3.8, 0.4, '↑ the new step', size=15, color='orange', bold=True, align='c')
    step(sl)
    box(sl, 0.6, 3.65, 5.9, 1.35, [('Got precommit?', 17, 'green'), 'Then **everyone** voted yes → safe to commit.'], fill='soft', align='l', pad=0.25, size=16, gap=0.15, color='body')
    box(sl, 6.83, 3.65, 5.9, 1.35, [('No precommit?', 17, 'red'), 'Commit can\'t have happened yet → safe to **abort** and release locks.'], fill='soft', align='l', pad=0.25, size=16, gap=0.15, color='body')
    step(sl)
    box(sl, 0.6, 5.2, 5.9, 1.4, 'Coordinator crashes? **Another participant finishes the job** by asking who got precommit. A **time-out** bound releases locks.', fill='blue_xs', size=15, color='ink', align='l', pad=0.25)
    callout(sl, 6.83, 5.2, 5.9, 1.4, 'Organizer first posts "everyone said yes!" in the group chat — then books.', size=15)

    sl = D.slide('2PC vs. 3PC at a glance', sec='23.4.1 – 23.4.2', say="""
A quick side-by-side to remember.
2PC has two phases: vote, then decide. 3PC has three: vote, prepare-to-commit, commit.
If the coordinator crashes after the votes, 2PC participants are blocked, holding locks until it comes back. In 3PC, participants can decide among themselves: if anyone got precommit, finish the commit; if not, abort.
Locks: in 2PC they can be held for an unbounded time. In 3PC, a time-out bound releases them.
The cost: 3PC sends more messages — one extra round. That is the classic trade-off: more messages for no blocking.""",
                   cue='OPTIONAL — recap slide, skip if behind time. Read row by row.')
    rows = [['', '2PC', '3PC'], ['Phases', 'Vote → Decide', 'Vote → Prepare-to-commit → Commit'],
            ['Coordinator crashes after votes', 'Participants **blocked**', 'Participants decide among themselves'],
            ['Locks', 'Held until coordinator returns', 'Released on time-out'],
            ['Messages', 'Fewer', 'One extra round']]
    yy = 1.75
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            w = [3.6, 4.1, 4.4][c]
            x = 0.6 + sum([3.6, 4.1, 4.4][:c])
            head = r == 0
            f = 'blue' if head and c else ('white' if head else ('soft' if c == 0 else ('red_s' if c == 1 and r in (2, 3) else ('green_s' if c == 2 and r in (2, 3) else 'blue_xs'))))
            box(sl, x, yy, w - 0.05, 0.85 if r else 0.6, cell, fill=f, color='white' if head else 'ink', size=17 if r else 18,
                bold=head or c == 0, shape='rect')
        yy += (0.9 if r else 0.65)
    takeaway(sl, 'Trade-off: 3PC pays **one extra message round** to avoid blocking.', y=6.0)

    sl = D.slide('Help from the operating system', sec='23.4.3', say="""
The last topic in this section: what if the operating system supported transactions?
Today, a DBMS usually implements its own semaphores — little data structures that give exclusive access to a shared resource, like a lock. But these live in user space, and the OS kernel does not know about them.
That causes a problem. Suppose DBMS process A holds a semaphore and the OS decides to put A to sleep. Every process waiting for that resource is now stuck, and performance drops badly. It is like the building manager sending someone home for the day without knowing they have the only key to the meeting room.
[click] With OS support we get three benefits. One: the OS sees which process holds what, so it avoids deactivating a lock holder. Two: locking can be done with special hardware support, which makes one of the most common DBMS operations cheaper. Three: common transaction operations, like two-phase commit, can be implemented once in the kernel, so several DBMSs on the same machine don't each have to build their own.""",
                   cue='Key-holder analogy, then three benefits.')
    text(sl, 0.6, 1.6, 5.9, 0.4, 'Today', size=19, color='red', bold=True)
    box(sl, 0.6, 2.1, 5.9, 0.75, 'DBMS process A — holds a lock', fill='blue_s', color='blue_d', size=15, bold=True)
    box(sl, 0.6, 2.95, 5.9, 0.75, 'DBMS semaphores (user space)', fill='soft', color='body', size=15)
    box(sl, 0.6, 3.8, 5.9, 0.75, 'OS kernel — doesn\'t know about them', fill='faint', color='white', size=15, bold=True)
    text(sl, 0.6, 4.65, 5.9, 0.75, 'OS puts A to sleep → everyone waiting on A is **stuck**.', size=15, color='red')
    callout(sl, 0.6, 5.35, 5.9, 1.3, 'The building manager sends home the person who holds the only meeting-room key.', size=14)
    step(sl)
    text(sl, 6.83, 1.6, 5.9, 0.4, 'With OS-supported transactions', size=19, color='green', bold=True)
    bens = [('OS-aware locks', 'The OS sees who holds what and avoids putting a lock holder to sleep.'),
            ('Hardware locking', 'Makes one of the most common DBMS operations cheaper.'),
            ('Shared kernel operations', 'e.g. one 2PC in the kernel, reused by every DBMS on the machine.')]
    for i, (a, b) in enumerate(bens):
        y = 2.1 + i * 1.5
        box(sl, 6.83, y, 5.9, 1.35, fill='green_s', radius=0.08)
        numdot(sl, 7.03, y + 0.2, i + 1, d=0.5, fill='green', size=16)
        text(sl, 7.7, y + 0.12, 4.9, 1.2, [a, (b, 14, 'body')], size=17, color='ink', bold=True, gap=0.1)


    sl = D.slide('Why it matters: a bank transfer across two sites', kicker='IN PRACTICE · PART 3', say="""
Let's make distributed commit concrete with money.
An transfers 2,000,000 đồng to Bình. An's account is stored at the Hà Nội site; Bình's account is at the Hồ Chí Minh City site. So one transfer is two updates on two sites: minus two million in Hà Nội, plus two million in HCMC.
[click] Without an atomic commit protocol, two things can go wrong if a site or the network fails halfway. Case one: Hà Nội commits the debit, HCMC never commits the credit — two million đồng simply vanish. Case two: the credit commits but the debit is lost — the bank creates money out of nothing.
[click] With two-phase commit, both sites first vote "I can do it" and write it to their logs; only then does the coordinator say commit. Both updates happen, or neither does. That's atomicity — the A in ACID — across sites.""",
            cue='Tell the story with real names and amounts; two clicks.')
    server(sl, 0.9, 1.85, 1.1, 1.2, label='Hà Nội site')
    box(sl, 2.3, 1.9, 2.9, 1.1, [('An', 18, 'ink'), ('balance  −2,000,000₫', 15, 'red')], fill='white', size=15, bold=True, gap=0.1)
    server(sl, 11.3, 1.85, 1.1, 1.2, label='HCMC site')
    box(sl, 8.1, 1.9, 2.9, 1.1, [('Bình', 18, 'ink'), ('balance  +2,000,000₫', 15, 'green')], fill='white', size=15, bold=True, gap=0.1)
    line(sl, 5.35, 2.45, 7.95, 2.45, color='blue', w=3, flow=True)
    text(sl, 5.3, 1.95, 2.7, 0.4, 'one transfer', size=14, color='blue', bold=True, align='c')
    step(sl)
    box(sl, 0.6, 3.75, 5.9, 1.25, [('✗  Debit commits, credit lost', 17, 'red'), 'Two million đồng **vanish**.'], fill='red_s', size=16, color='ink', align='l', pad=0.3, gap=0.15)
    box(sl, 6.83, 3.75, 5.9, 1.25, [('✗  Credit commits, debit lost', 17, 'red'), 'The bank **creates money** from nothing.'], fill='red_s', size=16, color='ink', align='l', pad=0.3, gap=0.15)
    step(sl)
    box(sl, 0.6, 5.25, 12.13, 1.2, [('✓  With 2PC: both sites vote and log first, then commit together', 18, 'green'),
                                     'Both updates happen, or neither does → **atomicity across sites**.'], fill='green_s', size=16, color='ink', align='l', pad=0.3, gap=0.15)

    sl = D.slide('Where you will meet these ideas', kicker='IN PRACTICE · PART 3', say="""
Where do these protocols live today? Three examples.
[click] First, distributed transactions in ordinary business software. The XA standard lets an application server coordinate one transaction across several databases — and XA is two-phase commit. Same blocking risk we discussed, which is why engineers try not to span too many databases in one transaction.
[click] Second, Google Spanner, described in a 2012 paper. It is a database spread across data centers worldwide, and it still uses two-phase commit. Its trick against blocking: every participant, including the coordinator, is itself a replicated group, so one crashed machine doesn't stop the protocol.
[click] Third, quorum systems, such as Amazon's Dynamo design from 2007 and Apache Cassandra. A read or write succeeds when enough copies answer — for example a majority. That is the voting method from section 23.3.2.
So 2PC and voting aren't history: they're inside systems you use daily.
That ends my part. Member 4 will move from correctness to speed: how to answer queries cheaply.""",
            cue='One card per click; keep it short.')
    ex = [('XA transactions', 'Application servers coordinate one transaction over several databases.', 'XA = two-phase commit'),
          ('Google Spanner (2012)', 'Global database across data centers. Runs 2PC, but every participant is a replicated group, so no single machine blocks it.', '2PC + replication'),
          ('Quorum systems', 'Amazon Dynamo (2007), Apache Cassandra: a read or write succeeds when enough copies (e.g. a majority) answer.', 'Voting, §23.3.2')]
    for i, (t, d, tag) in enumerate(ex):
        step(sl)
        x = 0.6 + i * 4.1
        box(sl, x, 1.7, 3.9, 4.4, fill='white', radius=0.05)
        numdot(sl, x + 0.3, 1.95, i + 1, d=0.6, size=22, fill='orange_m')
        text(sl, x + 0.3, 2.75, 3.35, 0.9, t, size=21, color='ink', bold=True)
        text(sl, x + 0.3, 3.4, 3.35, 1.9, d, size=16, color='body')
        box(sl, x + 0.25, 5.25, 3.4, 0.6, tag, fill='blue_s', color='blue_d', size=15, bold=True)
