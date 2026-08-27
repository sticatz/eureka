# Customer Interviews — Coaching and Evidence Admission

Loaded on demand whenever a founder is about to talk to potential users, or has come back with what they heard and wants it recorded. Most often invoked from `idea-validate`; also from `idea-gtm` (channel and buying-process questions) and `idea-mvp` (scoping against observed behavior).

Two jobs, in order: coach the founder into interviews that can produce admissible evidence, then gate what comes back before any of it is recorded as evidenced. Interviews and desk research are the only two ways new facts enter the system, so an unfiltered interview claim lifts `evidence_strength` and can unlock a `go` verdict. Five friends saying "that sounds great, I'd use that" must never do that. Bad interview data is strictly worse than none: it converts uncertainty into a confident false positive.

## Core Principle

From Rob Fitzpatrick's *The Mom Test*: ask only questions that even the founder's mother could not answer with a well-meaning lie. Every technique below follows from one of three rules.

1. **Talk about their life, not the idea.** The founder is a researcher, not a salesperson.
2. **Ask about specific past behavior, never hypothetical future behavior.** What someone did last Tuesday is data. What someone would do next quarter is imagination, and imagination is systematically optimistic.
3. **Never pitch first.** Once the interviewee knows what the founder wants to hear, everything said afterward is contaminated, no matter how enthusiastic.

To brief a founder in one line: *leave with facts about their past, not opinions about your future.*

## Question Rewrites

Give these verbatim. Each is past-tense, specific, and answerable without knowing the idea exists.

| Instead of asking | Ask |
|---|---|
| "Would you use a tool that does X?" | "Walk me through the last time you had to do X. What did you actually do?" |
| "Do you think this is a good idea?" | "What have you already tried to fix this? What happened?" |
| "Would you pay $30/month for this?" | "What do you spend on this today — tools, contractors, your own hours? Show me the last invoice." |
| "How often does this happen?" | "When did it last happen? And the time before that?" |
| "Is this a big problem for you?" | "What did it cost you the last time it went wrong — hours, money, a customer?" |
| "Would you switch from [incumbent]?" | "How did you end up on [incumbent]? Who decided, and what else did you look at?" |
| "What features would you want?" | "What's the part of this you've built a workaround for? Show me the workaround." |
| "Would your boss buy this?" | "What was the last tool your team bought? Who signed off, how long did it take, out of whose budget?" |
| "Does this happen to other people too?" | "Who else do you know who deals with this? Would you introduce me?" |
| "Do you care about X?" | "The last time X came up, what did you do about it?" |

A question that cannot be rephrased into the past tense is usually not worth asking.

## Three Failure Modes and Their Deflections

**Compliments** — "great idea," "I love this," "you're onto something." Zero information, feels like progress. Deflect: *"That's kind — but tell me about the last time you hit this yourself. What did you do?"* Never record a compliment as anything.

**Generics** — "I usually do X," "we always end up Y," "people in my role typically…". Self-reported averages, and memory rounds toward the flattering. Deflect: *"Tell me about the most recent specific time, not the usual case,"* then push to an artifact: the calendar entry, the spreadsheet, the email thread, the invoice.

**Hypotheticals** — "I'd definitely use that," "if it did Z, I'd buy it." Highest enthusiasm, lowest value. Convert the future into a past or a commitment: *"What's stopping you from solving this today?"* or *"Can we book 30 minutes Thursday to walk through your current process?"* The response to the ask carries more signal than the promise did.

## Recruiting Five People This Week

| Segment type | How to get 5 conversations in a week |
|---|---|
| **B2B role** | Search LinkedIn by exact job title plus company size; message 30 to land 5. Ask for 20 minutes of advice about their workflow, never a demo. Second source: the founder's ex-colleagues in that role, plus referrals — end every call with "who else should I talk to?" |
| **Consumers** | Go where the behavior already happens — the store, the gym, the subreddit, the Discord — and ask about the behavior, not the product. Screen with one qualifying question ("when did you last do X?") before spending anyone's time. |
| **Niche community** | Approach the two or three moderators or regulars the community trusts, for context and for permission, then ask for introductions. Cold-posting a survey usually burns the channel and yields the least useful respondents. |
| **Existing audience** | Email 20 people from the list personally, one at a time, asking for a call. Blast sends get compliments; individual notes get calls. |

Constraints: no friends, family, co-founders, or investors unless one is literally the buyer; recruit separately so they do not hear each other. If five reachable people in the segment cannot be found in a week, record that as a GTM risk, not a scheduling inconvenience.

## The Currency of Commitment

Talk is free; commitment costs something. Rank what came back:

1. **Money** — prepayment, deposit, signed LOI with a number, paid pilot. Strongest.
2. **Reputation** — an introduction to their boss or peers, agreeing to be a named reference, bringing colleagues to the next call.
3. **Time** — a second meeting they show up to, sending real data over, walking through their process on a screenshare.
4. **Nothing** — praise, "keep me posted," an email address, a survey response.

A "yes" that costs nothing means nothing. Close every interview by asking for the next-largest currency and observing what happens; a decline is data.

## The Admission Rubric

Apply to **each individual claim** the founder brings back, not to the interview as a whole. Every question is yes/no. Any "no" means the claim is recorded as `**Assumption:** <claim>`, not as evidence.

1. **Past, not future?** — Does it describe something that already happened, rather than what the person would, might, or plans to do?
2. **Their life, not the idea?** — Is it about their own behavior or spending, rather than a reaction to the concept?
3. **Pitch-free?** — Was it said *before* the founder described the idea in that conversation?
4. **Anchored?** — Is there at least one specific: a date, a count, an amount, a named tool, a named workaround, a named person?
5. **In segment?** — Does the person match the target segment as the artifacts define it, rather than being whoever was reachable?
6. **"No" was available?** — Was the relationship arm's-length enough that disagreeing carried no social cost? (Friends, family, employees, existing investors: no.)
7. **Volunteered?** — Did it come from an open question rather than a leading one ("so the invoicing is the painful part, right?")?
8. **Independent?** — Was this person interviewed separately, without hearing the other interviewees?

**Disqualifiers**, any one of which fails the claim outright: hypothetical framing; pitch delivered first; compliment with no behavioral content; no anchor; wrong segment; group setting; the founder can only paraphrase the gist and has no note or quote.

**Default: when in doubt, record as assumption.** State the reason in one clause so the founder can go fix it: `**Assumption:** ops managers spend 5+ hrs/week on reconciliation — heard from 3 interviewees, but all were pitched first.`

**Split partially-admissible data; never average them down.** Most real interviews produce one of each. From "she said she'd pay $50/month for this":

- Evidenced: *Interviewee 3 currently pays a bookkeeper for this and spends about 3 hours a week on it herself.* `[interview: 1/5, ops managers, unprompted]`
- `**Assumption:** she would pay $50/month for this product` — hypothetical, stated after the pitch.

Tag every admitted claim inline with provenance: how many of how many interviewees, which segment, when, prompted or not. Do not invent dates, counts, or company names the founder did not supply — ask, or leave the tag incomplete and say so.

## How Many, and What to Do With Contradictions

Five admissible conversations *per segment* is the floor — not five spread across three segments. Stop when two consecutive interviews produce nothing new; saturation, not raw count, is the signal. Count only claims that passed the rubric: three admissible conversations beat ten pitched ones.

When findings contradict, do not average them and do not let the founder keep the half they liked. Look first for a segment boundary that explains the split — team size, tooling, tenure, budget authority. If one exists, that is a real finding: the segment was defined too broadly. If none explains it, the sample is too small to support either side; record both accounts, log the contradiction as a `key_risk`, and hold the claim as an assumption. A founder reporting zero contradictions across five interviews has usually been pitching — probe for that.

## What Interviews Cannot Establish

- **Willingness to pay in the abstract.** Stated prices are near-worthless. Interviews establish current spending and the shape of the budget; only a real charge establishes price.
- **Market size.** Interviews say nothing about how many such people exist. That is desk research.
- **Whether anyone will actually switch.** Interviews reveal switching *costs* and who decides; actual switching is only observable in a live test.
- **Feature prioritization.** People forecast their own preferences poorly. Existing workarounds rank better than stated wish lists.
- **Frequency, from memory alone.** Self-reported frequency drifts. Ask for the artifact — calendar, inbox, logs, invoices — and treat unverified frequency as an assumption.

When a founder tries to settle any of these with an interview quote, name which one it is and record the claim as an assumption.
