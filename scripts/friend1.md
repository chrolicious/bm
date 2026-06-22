# Friend 1 — Tobi (Tobias)

Status: raw extraction, scene order drafted, dialogue not yet written.

## Premise

A bootleg Pokémon-style GBC "game" Michel is giving Tobi to ask him to be his best man. Player is Michel-as-trainer, walks through a small overworld where each "room" is a memory with Tobi. Ends with the ask.

**Setting:** Kerkrade, Netherlands. School = **College Rolduc**, HAVO track, klas 3 (third year). Michel commutes back to Meerbusch (Germany) on weekends to see his girlfriend **Constanze / "Conzi."** The Netherlands → Germany border-crossing weekend ritual is the unspoken context for the dress-shirt mystery.

## Characters

- **Michel** (player sprite) — proxy = `gfx/player/chris.png` (Crystal protag, recolor TBD)
- **Tobi** — needs custom sprite (Gen-2 NPC style; tall-ish, hair color TBD). Possible NPC sprite reuse for prototype: `gfx/sprites/biker.png` or `gfx/sprites/cal.png` until custom art lands.

## Voice / tone

- Mixed. Comedy bits land hard, emotional bits land harder. Crystal-era Pokémon dialogue cadence (short lines, "...", `\n` line breaks, occasional ALL CAPS for emphasis).
- Speaker tag and in-dialogue name both: **TOBI** / **Tobi**.
- It's German-speaking teen banter on the Dutch border. Mostly English, but the in-jokes drop into German: **"spasti"** is the recurring affectionate insult between them. Use it as the punchline word — not a constant tic.

## Dialogue format

Every dialogue block in this doc maps to one Pokémon-style text box. Box is ~18 chars wide × 2 lines visible at once; a third line scrolls in. We'll use this format and let the engine paginate:

```
TOBI: line one (≤18 chars)
      line two (≤18 chars)
      [▼]
      line three
```

`[▼]` = "press A to continue" marker. `...` carries weight — leave it on its own line.

## Arc

Pokémon "town" structure: 5 rooms / memories, arranged as a short overworld walk. The walk itself is the spine — each door is a year of their lives. Pacing: 3 short scenes → 1 silent beat → 1 devastating scene → the ask. Comedy carries the player through the early stuff so the Aachen scene lands.

```
[TITLE] → [CLASSROOM] → [SCHOOLYARD] → [LIVING ROOM] → [SPAIN BAR] → [AACHEN STAIRS] → [BWL RAID] → [ASK]
           cold open    WoW first hint   "trains" beat   comedy beat   climax              comedy↺      the question
```

Seven scenes. The BWL raid sits *after* Aachen on purpose: life kept going. Tobi's mom is gone, the friendship deepened, and now you're two guys laughing on Ventrilo because Michel just wiped a 40-man raid. Heartbreak → recovery → resolution.

---

## Scene 1 — Classroom (cold open, ~age 16)

**Setting:** A Pokémon Gen-2-style schoolroom interior. Desks in rows. Michel-sprite sits front-row in a dress shirt. Tobi-sprite in the back.

**Asset notes:** reuse `gfx/tilesets/elms_lab.png` palette-swapped, or `gfx/tilesets/players_room.png` repurposed; Michel-sprite = `gfx/player/chris.png` with dress-shirt palette; Tobi = placeholder NPC sprite for prototype.

**Draft dialogue (first pass, GBC-text-box sized):**

```
[FADE IN. COLLEGE ROLDUC.
 HAVO 3. Friday morning.]
[The player wakes up in his
seat, front row.]

NARRATOR: Friday.
          You repeated a year.
          [▼]
          Too many late nights
          on COUNTER-STRIKE.
          [▼]
          Not this time.

[Michel takes a notebook out.
Tobi-sprite visible in back row.]

TOBI:     ...
          Who IS this guy?
          [▼]
          Dress shirt.
          AGAIN.
          [▼]
          Front row.
          Every. Damn. Day.
          [▼]
          Spasti.

[Michel doesn't notice. He's
already thinking about the
drive to Meerbusch tonight.
Tobi doesn't know about that
yet.]

NARRATOR: ▼ Walk to the door.
```

**Notes on this draft:**
- Two POVs in one scene: the player as Michel, but Tobi narrates the *judgement*. Sets up that this is a memory game with two perspectives. The Meerbusch reveal pays off in Scene 7 (the ask) — "Conzi. That was Conzi."
- "Spasti." — one word, last line, no exclamation point. The affectionate dismissal lands harder dry.
- "COUNTER-STRIKE" and "COLLEGE ROLDUC" in caps follow the Pokémon convention for proper nouns / items. Reads native to the genre.
- Scene ends with player having to physically walk Michel-sprite to the door. The walk is the transition to Scene 2.

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

## Scene 6 — Blackwing Lair, first raid (comedy beat after the climax)

**Setting:** The Razorgore egg room — a dim cave chamber with dragon eggs in the center, doorways on either side, mobs about to spawn. Tile-art note: we'll fake the BWL aesthetic with a cave palette (use `gfx/tilesets/cave.png` or `gfx/tilesets/dark_cave.png` from pokecrystal, palette-swap to red/black) and a couple of dragon-egg sprites as scenery. Player-Michel sprite, four NPC-raider sprites lined up behind him as a "raid party," a horde of orc-trash sprites just past the doorway.

**Beats:**
- Michel's first raid with Tobi's guild. He has NO idea how anything works.
- The raid is pre-pull, everyone is positioning.
- Michel-sprite drifts forward to look at the eggs.
- Body-pulls all the trash in the egg room. Mobs swarm.
- 40-man wipe.
- Kicked from the raid team. Demoted to the worse team.
- Tobi is dying laughing on Ventrilo / TeamSpeak.

**Mechanically:** This is a tiny anti-puzzle the player *can't win*. On scene enter, a WoW-style zone banner reads **"Blackwing Lair"** centered on the screen. The raid lead **Aronian** tells the player **"DEFINITELY DON'T WALK LEFT OR RIGHT."** That instruction *is* the trap — a Pokémon player given a "do not" will absolutely do it. The moment Michel-sprite walks one tile left or right, trash spawns from that side's doorway. The wipe is scripted; the gag is the explicit anti-instruction.

**Guild roster on Vent:** Aronian (raidlead, takes everything personally), Tobi (heals), and at minimum Gerrit, Tita, Divinity, Friets, Aerendil chiming in. Each gets one line in the post-wipe chaos — every name is a real person Tobi will instantly recognize.

**Draft dialogue (first pass):**

```
[CAVE INTERIOR. Red palette.
 Dragon eggs in the center.]
[Michel-sprite at the front
of a line of NPC raiders.
Tobi-sprite somewhere in
the back, on heals.]

[A banner slides in from the
top of the screen and rests
mid-screen, WoW zone-change
style:]

           ╔══════════════╗
           ║ BLACKWING    ║
           ║    LAIR      ║
           ╚══════════════╝

[Banner fades after 2 seconds.]

VENT CHAT:    <Aronian> ok we
              pull in 30 sec
              [▼]
              <Aronian>
              EVERYONE
              [▼]
              <Aronian>
              DEFINITELY DO NOT
              WALK LEFT OR RIGHT
              [▼]
              <Aronian> stay on
              your mark
              [▼]
              <Friets> lmao who
              would do that
              [▼]
              <Tobi> michel u
              hear that
              [▼]
              <Michel> ya all good
              [▼]
              <Michel> just gonna
              look around

[The player has control of
Michel-sprite. North wall =
eggs. East and west = dark
tunnel doorways. Forward
(north) is fine. Left or
right... is not.]

[Player presses ← or →.]

           ! ! !

[Orc trash floods in from
the doorway Michel walked
toward.]

VENT CHAT:    <Gerrit> ADDS
              [▼]
              <Tita> WHERE
              [▼]
              <Divinity> oh no
              [▼]
              <Aerendil> by the
              Light...
              [▼]
              <Friets> LMAOOOO

VENT CHAT:    <Raidlead> WHO
              [▼]
              <Raidlead> WHO
              PULLED
              [▼]
              <Tobi> oh my god
              [▼]
              <Tobi> oh my GOD
              [▼]
              <Raidlead> WIPE IT
              WIPE IT WIPE IT

[Screen flashes red.
"YOU HAVE DIED" text.
Then the rest of the raid.
40-man wipe.]

           * WIPE *

[Black screen.]

VENT CHAT:    <Aronian> ...
              [▼]
              <Aronian> who is
              this guy
              [▼]
              <Tobi> uhhhh
              [▼]
              <Tobi> my friend
              [▼]
              <Gerrit> oof
              [▼]
              <Friets> RIP
              michel
              [▼]
              <Aronian> hes off
              the team
              [▼]
              <Aronian> demoted.
              casual rank.
              [▼]
              <Tita> sorry
              michel :(
              [▼]
              <Aerendil> a noble
              attempt friend
              [▼]
              <Divinity> ...
              [▼]
              <Tobi> michel
              [▼]
              <Tobi> ...
              [▼]
              <Tobi> spasti.
              [▼]
              <Michel> yeah ok
              fair

[Scene fades.
Both of them are laughing
by the end. You can tell.]
```

**Notes on this draft:**
- Vent chat formatted as a chat log inside the dialogue box — `<Name> text` cadence is instantly recognizable to anyone who voice-chatted in 2005.
- The callback to "spasti" from Scene 1 lands here. The first time Tobi said it, he didn't know Michel. The second time, he says it because Michel is family.
- The raidlead's "who is this guy" mirrors Tobi's Scene 1 line. Different room, same question, very different answer.
- Pokémon-style **`! ! !`** alarm (the same one used when a trainer spots you) for the spawn trigger — it's a perfect canonical glyph for "oh no."
- No music during the wipe. Music returns when the screen fades.

**Need from user:**
- Guild name? (Pure flavor, but if you remember it, gold.)
- Year? (BWL was current content roughly 2005–2006 — sets your age.)
- Did Michel actually get demoted, or was that a joke that stuck? (Either works, but the current draft commits to "real demotion" because it's funnier.)
- Are the personality reads above (Friets = the LMAO guy, Aerendil = lore-serious, Divinity = quiet "...", Tita = the empath, Gerrit = the curt warrior) right or wrong? Easy to reassign if so.

---

## Scene 7 — Present day / The Ask

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
