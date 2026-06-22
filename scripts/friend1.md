# Friend 1 — Tobi (Tobias)

Status: raw extraction, scene order drafted, dialogue not yet written.

## Premise

A bootleg Pokémon-style GBC "game" Michel is giving Tobi to ask him to be his best man. Player is Michel-as-trainer, walks through a small overworld where each "room" is a memory with Tobi. Ends with the ask.

## Characters

- **Michel** (player sprite) — proxy = `gfx/player/chris.png` (Crystal protag, recolor TBD)
- **Tobi** — needs custom sprite (Gen-2 NPC style; tall-ish, hair color TBD). Possible NPC sprite reuse for prototype: `gfx/sprites/biker.png` or `gfx/sprites/cal.png` until custom art lands.

## Voice / tone

- Mixed. Comedy bits land hard, emotional bits land harder. Crystal-era Pokémon dialogue cadence (short lines, "...", `\n` line breaks, occasional ALL CAPS for emphasis).
- Michel calls Tobi: **TBD** (the casual name/nickname Michel actually uses in real life — important, drives every line)
- They're German — keep it English, but a stray "Alter" or German place name lands as authentic flavor, not affectation.

## Arc

Pokémon "town" structure: 5 rooms / memories, arranged as a short overworld walk. The walk itself is the spine — each door is a year of their lives. Pacing: 3 short scenes → 1 silent beat → 1 devastating scene → the ask. Comedy carries the player through the early stuff so the Aachen scene lands.

```
[TITLE]   →   [CLASSROOM]   →   [SCHOOLYARD]   →   [LIVING ROOM]   →   [SPAIN BAR]   →   [AACHEN STAIRS]   →   [PRESENT DAY / ASK]
                cold open      bonding montage     "trains" beat        comedy beat          climax              the question
```

---

## Scene 1 — Classroom (cold open, ~age 16)

**Setting:** A Pokémon Gen-2-style schoolroom interior. Desks in rows. Michel-sprite sits front-row in a dress shirt. Tobi-sprite in the back.

**Beats:**
- Player wakes up. Friday. Has to repeat the year because he played too much Counter-Strike: Source.
- Front row this time. Determined not to flunk again.
- Dress shirt — because Michel goes straight from school to Meerbusch to see his girlfriend on weekends. Tobi doesn't know this, just thinks Michel is the weird overdressed front-row kid.
- Tobi (off-screen narration via dialogue box later, or shown as a thought from his sprite) sums up: "Who's that guy?"

**Hook line (Tobi's POV, written for later in the game when revealed):**
> "Every Friday. Dress shirt. Sitting up front like a damn prefect.
>  I thought you were insane."

---

## Scene 2 — Schoolyard, in front of the gym (~age 16–17)

**Setting:** Outdoor schoolyard tile, gym building in the background. A small cluster of NPC sprites = friends.

**Beats:**
- Friend group talking about "this new game called World of Warcraft."
- This conversation seeds 20+ years of Michel's life. Still playing today.
- Light, hyped-teenager energy. Should *read* like the Pokémon Center conversations where NPCs tell you about something cool — "Have you heard about…?"

**Possible dialogue stub:**
> NPC: "Yo! Have you heard?
>  There's this new GAME...
>  WORLD OF WARCRAFT!"
> TOBI: "...we have to play this."
> [Michel, age 16, has no idea this conversation will still be running in his head in 2026.]

---

## Scene 3 — A friend's living room ("Trains" / Porcupine Tree)

**Setting:** Living room interior tile. Friends scattered as NPCs. Guitar on the floor or against the wall.

**Beats:**
- Quiet evening, just hanging out.
- Michel picks up the guitar, plays *Trains* by Porcupine Tree.
- Time seems to stand still.
- Tobi later tells Michel this was a very profound moment for him.

**Mechanically:** This is the silent beat. Almost no dialogue. Maybe just a "...". Maybe a few bars of a Porcupine Tree-flavored chiptune motif on Channel 3. The player feels the room go quiet. This is the scene the game *earns its way into the heart on* — if we can pull it off in 4-color GBC, it's the standout.

**Need from user:**
- The name of the friend whose living room (use real name or omit? "*'s living room")
- Whose guitar was it
- Any specific line either of you said, or did nobody speak

---

## Scene 4 — Spain, "La Cubanita" bar (vacation, comedy beat)

**Setting:** Bar interior tile. Two cute waitress NPC sprites. Bottles on shelves. Tobi-sprite increasingly wobbly.

**Beats:**
- On vacation in Spain together.
- Bar called something like La Cubanita (need exact name).
- Waitresses figured out the two of them were into them, kept feeding them drinks every visit.
- One night Tobi was so drunk he puked all over his bed.
- His dad was Not Amused when he and Tobi's mom got back.

**Tone:** Pure comedy. Drunk-text dialogue cadence. The bar visit can be a tiny gameplay loop: walk up to waitress → "ANOTHER ROUND?" → screen shake → fade out → cut to next morning, Tobi on bed.

**Need from user:**
- Actual bar name if you remember it
- Roughly what year / how old
- Was this just you two, or with others
- Tobi's dad — is he a character we should portray? Does he need a sprite?

---

## Scene 5 — Aachen, the club stairs (CLIMAX)

**Setting:** Street outside a club in Aachen, at night. Dark palette. Bouncer NPC silhouette by the door. Tobi-sprite alone on the stairs.

**Beats:**
- You both went out clubbing in Aachen.
- Michel notices Tobi has left the club, follows him out.
- Tobi is sitting on the stairs in front of the entrance.
- Michel sits down next to him.
- Tobi tells Michel his mom died that morning. He hasn't told anyone.
- He breaks down. Michel hugs him.
- "I knew I'd love this kid for the rest of my life like a brother."
- A few guys make fun of them for hugging. Michel flips his shit.

**Mechanically:** The whole scene is one fixed camera angle. No walking. Dialogue. The hug is a sprite overlap with a heart pixel (or no overlay at all — the dialogue carries it). The catcalling guys appear, brief confrontation, Michel-sprite turns and the screen flashes or shakes — keep it short, don't undercut the moment with extended combat.

This is the emotional load-bearing scene of the whole game. Every other scene exists to make the player (Tobi) trust the game enough to let this one land.

**Need from user:**
- The name of the club, or "a club in Aachen" if unspecified
- Are you comfortable with the catcalling-guys beat being explicit, or do you want it softer / cut entirely
- A line Michel actually said, or thought, that night — if you remember one

---

## Scene 6 — Present day / The Ask

**Setting:** TBD. Could be:
  (a) Michel's apartment (player wakes up, "20 years later…")
  (b) A wedding-themed location (church / venue)
  (c) Just a black screen with the question
  (d) Pokémon-credits-style scrolling montage of all the previous scenes' rooms, then the ask

**Beats:**
- The "you've come this far" moment.
- The actual question.
- A choice prompt: `YES` / `NO`. Both branches go to "YES" — but the NO branch should land a joke ("Press A to reconsider.") then accept YES.

**Need from user:**
- The actual ask line, in your voice. Even rough.
- Wedding date / "save the date" — does the game tell him a date?
- Anything you want to give him in-game as a "key item" — like a literal Pokémon-style item received notification: "TOBI received the BEST MAN BADGE!"

---

## Open questions / decisions

1. **Tobi's nickname** — what do you actually call him?
2. **Order of comedy scenes** — keep Spain before the gut-punch (comedy → devastation = strongest contrast), or put Spain after Aachen to land on a lighter note? My instinct: comedy first, then climax, then resolution. The current order.
3. **Should the "Trains" living-room scene have actual chiptune music** of the song, or just silence + an instrument icon? Silence might be more powerful given the constraint.
4. **Length budget** — total game length: 5–10 min walkthrough? Each scene gets ~30–60 seconds of dialogue.
5. **The girlfriend in Meerbusch** — she's set dressing for the dress-shirt joke. Stay anonymous or named?
6. **Other beats not yet placed:**
   - WoW sessions / "hanging out every day"
   - Starting the Japanese bachelor together (Tobi finished, Michel didn't)
   - "Big highs and lows" mentioned generally — is there one more specific high or low we should place?
   - 20 years of friendship leading to now — bridged in scene 6 or earned through a montage

## Asset map (so far)

| Scene | Tileset | Custom art needed |
|---|---|---|
| Classroom | Need school-interior tileset; closest in pret: `interior`, `kanto_pokecenter`-style desks | Tobi NPC sprite, school-uniform Michel |
| Schoolyard | `johto` outdoor tileset + custom gym building? | Friend-group NPC cluster |
| Living room | `house1.png` / `house2.png` interiors | Guitar item icon |
| Spain bar | Custom — closest pret match: any pub/cafe interior in `gfx/tilesets/` | 2× waitress NPC, drunk-Tobi sprite variant |
| Aachen stairs | Custom — could repurpose any night-exterior tile | Hug overlay or paired-sprite frame |
| Present / Ask | Custom — possibly black BG + portrait | Best Man Badge item sprite |

Most of this can reuse pret tilesets with palette swaps. Custom art = mostly Tobi's NPC sprite + the "best man badge."
