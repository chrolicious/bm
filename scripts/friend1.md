# Friend 1 — Tobi (Tobias)

Status: **finalized** — all 7 scenes drafted, polish pass complete, ready for engine integration + asset finalization. WoW handle: **Ozora**.

## Premise

A bootleg Pokémon-style GBC "game" Michel is giving Tobi to ask him to be his best man. Player is Michel-as-trainer, walks through a small overworld where each "room" is a memory with Tobi. Ends with the ask.

**Setting:** Kerkrade, Netherlands. School = **College Rolduc**, HAVO track, klas 3 (third year). Michel commutes back to Meerbusch (Germany) on weekends to see his girlfriend **Constanze / "Conzi."** The Netherlands → Germany border-crossing weekend ritual is the unspoken context for the dress-shirt mystery.

## Characters

- **Michel** (player sprite, WoW handle Xoh) — proxy = `gfx/player/chris.png` (Crystal protag, recolor TBD)
- **Tobi** (WoW handle Ozora) — needs custom sprite (Gen-2 NPC style; tall-ish, hair color TBD). Possible NPC sprite reuse for prototype: `gfx/sprites/biker.png` or `gfx/sprites/cal.png` until custom art lands.

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

Seven scenes, played as discrete tilemaps with `walk on →` transitions between them (no overworld map; the walk-on prompt is the spine). **Chronological order** — each scene later than the last. Pacing: light comedy through Sc 1–2 → quiet beat at Sc 3 → comedy at Sc 4 → comedy peak at Sc 5 (BWL chaos) → CLIMAX at Sc 6 (Aachen) → resolution + ask at Sc 7. The BWL chaos is what makes the silence of Aachen land — life was light right up until it wasn't.

```
[TITLE] → [CLASSROOM] → [SCHOOLYARD] → [LIVING ROOM] → [SPAIN BAR] → [BWL RAID] → [AACHEN STAIRS] → [ASK]
           cold open    WoW first hint   "trains" beat   comedy beat   comedy peak    climax              the question
```

The brother-truth named at the end of Aachen flows *directly* into the present-day ask with no comedy interlude between them.

---

## Scene 1 — Classroom (cold open, ~age 16)

**Setting:** A Pokémon Gen-2-style schoolroom interior. Desks in rows. Michel-sprite sits front-row in a dress shirt. Tobi-sprite in the back.

**Asset notes:** reuse `gfx/tilesets/elms_lab.png` palette-swapped, or `gfx/tilesets/players_room.png` repurposed; Michel-sprite = `gfx/player/chris.png` with dress-shirt palette; Tobi = placeholder NPC sprite for prototype.

**Draft dialogue (first pass, GBC-text-box sized):**

```
[COLLEGE ROLDUC. HAVO 3.
 Friday morning.]

[Michel-sprite sits front row.
Dress shirt. Notebook out.]

[Tobi-sprite in the back,
slumped on his desk.]

TOBI:     ugh
          [▼]
          look at this nerd
          [▼]
          front row AGAIN?
          [▼]
          who wears a dress
          shirt to school
          [▼]
          spasti.

[Bell rings.]

[NARRATOR: ▼ Walk to the door.]
```

**Notes on this draft:**
- All Tobi, no narrator confession. The "repeat year" backstory is omitted from the scene entirely — Tobi's mocking carries the setup without spelling it out.
- "ugh / look at this nerd / front row AGAIN?" is the actual cadence of a 16-year-old slumped at the back. Light, dismissive, fun.
- The Meerbusch dress-shirt detail is pure character flavor — no payoff in Scene 7 (we cut it; was making the moment bigger than it needed to be). Tobi just remembers it as "this weird kid in a dress shirt"; the player gets the same impression.
- "Spasti." is still the closer, but now it's a teen mutter, not a Shakespearean pronouncement.

---

## Scene 2 — Schoolyard, in front of the gym (~age 16–17)

**Setting:** Outdoor schoolyard tile, College Rolduc gym building in the background. **Friets, BramT, and Tobi** huddled, talking loud. Michel-sprite walks over.

**Asset notes:** Reuse `gfx/tilesets/johto.png` for outdoor ground. Three named NPC sprites for Friets, BramT, Tobi (pick distinct-silhouette sprites from `gfx/sprites/` — distinguishable at a glance matters since these three recur).

**Disambiguation:** This is **BramT** (the living-room/WoW-crew Bram, Benny's brother). The other Bram — **BramS** — is the best-man-to-be and shows up in Scene 7. They are different people; user calls them BramT/BramS to keep them straight. *Confirm with user if this Bram should actually be BramS instead.*

**Draft dialogue:**

```
[Outside the gym at College
Rolduc. Sun out.]

[Music: WOW TAVERN THEME,
GBC chiptune recreation.
Pulse 1 main melody, pulse 2
counter, wave channel for
warm bass. 3/4 time. Loops
through the whole scene.]

[Friets, BramT, and Tobi
huddled, talking loud.]

[Michel-sprite walks over.]

FRIETS:    bro you HAVE to
           try this game

BRAMT:     we just hit 60
           [▼]
           the elite zones are
           insane

TOBI:      michel.
           [▼]
           come play WORLD OF
           WARCRAFT.

MICHEL:    can't
           [▼]
           I'm grinding on
           STAR WARS GALAXIES

FRIETS:    bro

BRAMT:     bro

TOBI:      bro
           [▼]
           we'll boost you
           through DEADMINES

MICHEL:    ...what is deadmines

[NARRATOR: He would play this
game for 20 years...
[▼]
and counting.]
[NARRATOR: ▼ Walk on.]
```

**Notes:**
- "bro / bro / bro" — teen-friend peer pressure in pure form. Three NPCs, one syllable each, then Tobi closes the deal. Reads instantly.
- "Spasti." is *absent* this scene. Tobi doesn't need it — peer pressure is enough. Saves the word for the next two scenes where it lands harder.
- STAR WARS GALAXIES gets the proper-noun caps — Michel had a real game he loved, and the joke is that none of these jokers care.
- "DEADMINES" plants the *Michel-as-noob* setup that pays off in Scene 6 ("just gonna look around"). He was a noob from day one. Tobi was always there boosting.
- Scene ends mid-conversation on Michel's confused "...what is deadmines" — the narrator's "20 years" line carries the answer the scene doesn't bother to give. Sharper exit than spelling out the commitment.
- **Music: WoW Classic Tavern theme** as the BGM through the whole scene. Diegetic to the conversation, not the location — the music is the WoW excitement bleeding into the schoolyard. Any guildie of that era will recognize the melody within four bars. Same engineering channel-layout discipline as the Trains motif (pulse 1/2 + wave); these two tracks together prove the audio toolchain works for both folk-acoustic and chiptune-arrangement styles.

---

## Scene 3 — BramT's living room ("Trains" / Porcupine Tree)

**Setting:** Living room interior, evening. Four sprites scattered around: **BramT, Benny (BramT's brother), Tobi, Michel.** A guitar leaning against the couch.

**Asset notes:** Use `gfx/tilesets/house1.png` (Crystal house interior) palette-swapped warmer. NPC sprites: any 3 distinct ones for BramT/Benny/Tobi. Guitar = custom 8×8 prop sprite.

**Beats:**
- Quiet evening at BramT's place. Just the four of them.
- Michel picks up the guitar, starts playing *Trains* by Porcupine Tree.
- The room goes still.
- Tobi will tell Michel, much later, that this was a very profound moment for him.

**Mechanically:** This is the silent beat. Minimal dialogue — what carries the scene is the *music* (a chiptune motif based on the Trains intro, played on Channel 3 / wave — that's the GBC channel that best fakes a clean guitar) and the *stillness*: no one walks, no one speaks for several beats. After the music ends, one quiet line from Tobi. That's the whole scene.

**Draft dialogue:**

```
[BRAMT'S LIVING ROOM.
Evening. Lamp on.]
[BramT on the couch. Benny on
the floor. Tobi in the chair.
Guitar against the wall.]

[Michel-sprite walks in.]

BRAMT:    Yo Mich

BENNY:    sup

TOBI:     play something

[Michel-sprite walks to the
guitar. Picks it up.]

[Music: TRAINS main motif,
GBC chiptune recreation.
Wave channel carries the
arpeggio; pulse 1 a quiet
bass note underneath.
Six to eight bars.]

[The motif resolves.]

TOBI:     ...
          [▼]
          spasti.

[NARRATOR: ▼ Walk on.]
```

**Notes:**
- Trimmed of all the over-explaining. The music does the work; "..." then "spasti." is enough.
- This use of "spasti" is the *quiet affection* beat in the word's full arc (see Scene 7 notes for the complete arc). The shift happens in *how* Tobi says it, not in any narrator gloss.
- **Music (locked):** GBC chiptune recreation of the *Trains* main motif. Wave channel for the arpeggio (best-fakes plucked-string tone on GBC), pulse 1 for a sparse bass underneath. This is the *music centerpiece of the whole ROM* — the one motif we have to nail. **Reprises in Scene 7** under the ask: the same melody that meant "I love you, you idiot" here means "of course it's yes" there. The music is the bookend. If recreation proves impossible in the time budget, fall back order: (a) different recognizable Porcupine Tree phrase, (b) silence + single guitar-string SFX. (a) and (b) are emergency exits only.

---

## Scene 4 — Spain, "La Cubanita" bar (vacation, ~age 18)

**Setting:** Small bar interior, warm palette. Two waitress NPC sprites behind a counter. Bottles on shelves. Tables. Tobi-sprite and Michel-sprite at a table front-and-center. Tobi gets more wobble-frames as the scene progresses.

**Asset notes:** Use a Crystal cafe/pub tile from `gfx/tilesets/` (look in `mahogany_redgyarados`-area sets, or recolor a `house1` interior). Waitresses = reuse `gfx/sprites/beauty.png` palette-swapped. "Drunk Tobi" = the same NPC sprite with a tilted frame or sweat-drop emote (Pokémon has the canonical `gfx/emotes/` set — perfect).

**Beats:**
- Vacation in Spain. ~18 years old. Just the two of them at the bar (Tobi was there with his family, but the bar runs are him + Michel).
- A bar they keep returning to because the waitresses are cute.
- The waitresses know exactly what's happening and keep bringing more drinks.
- One night Tobi gets *catastrophically* drunk and pukes all over his bed.
- His parents come back from their trip out and find the aftermath. Tobi's dad: not amused.

**Mechanically:** The scene is a tiny loop. Player walks Michel-sprite up to the counter. A waitress prompt: `ANOTHER ROUND?` with two options that **degrade in legibility each round** — the options text itself is the slur meter. Four rounds, comically too many on purpose:
- Round 1: `YES / NO` (sober)
- Round 2: `Yeah ...hic / Nope` (the `...hic` is a WoW emote callback — `/hic` is the real /drunk hiccup action in WoW)
- Round 3: `Mrrghhh / Hnnffff` (pure mouth-sound gibberish)
- Round 4: `Yshhhrrgggh / Brbbblblbbb` (Tobi is leaning on the keyboard)

Tobi's wobble-frame intensifies each round. After round 4 the screen fades with a BURP, cut to the bedroom the next morning.

**Draft dialogue:**

```
[LA CUBANITA. Evening.]

[Music: LA CUCARACHA, GBC
chiptune. Pulse 1 + 2 carry
the melody; wave for the
oompah bass. Cheesy on
purpose — exactly what a
tourist bar called "La
Cubanita" would play.]

[Michel-sprite and Tobi-
sprite at a table near the
bar. Two waitresses behind
the counter, smiling.]

TOBI:     ...
          [▼]
          they're definitely
          flirting

MICHEL:   they're definitely
          flirting with our
          WALLETS

TOBI:     they want me

MICHEL:   they want our MONEY

TOBI:     spasti

[Player walks Michel-sprite
up to the bar.]

WAITRESS: hola guapo
          [▼]
          ANOTHER ROUND?

> YES
  NO

[YES.]
[Tobi-sprite gets a sweat-
drop emote. Wobble.]

WAITRESS: ...
          [▼]
          ANOTHER ROUND?

> Yeah ...hic
  Nope

[Yeah.]
[Tobi-sprite leans 30°.
Screen does a small shake.]

WAITRESS: ...
          ¿estás seguro?
          [▼]
          ANOTHER ROUND?

> Mrrghhh
  Hnnffff

[Either choice picks YES.]
[Tobi-sprite slides halfway
off the chair. Screen does
a bigger shake.]

WAITRESS: ...
          [▼]
          ¿en serio?
          [▼]
          ANOTHER ROUND?

> Yshhhrrgggh
  Brbbblblbbb

[Either choice picks YES —
Tobi is leaning on the
keyboard at this point.]

           * BURP *

[Screen fades to black.]

[CUT TO:
 BEDROOM. MORNING.]
[Tobi-sprite on the bed.
The bed has a "stained"
overlay tile. Tobi-sprite
is fully horizontal.]

TOBI:     ...
          [▼]
          oh no

[A door slam offscreen.]

TOBI'S DAD: (offscreen)
            TOBIAS.
            [▼]
            MAUEL.
            [▼]
            WAS.
            [▼]
            ZUM.
            [▼]
            FICK.

TOBI:     spasti.

MICHEL:   me?
          [▼]
          you puked on yourself

TOBI:     *sigh*

[NARRATOR: ▼ Walk on.]
```

**Notes:**
- "Spasti" used twice in this scene (once in banter, once after the puke) — now flowing between them, both directions. The word is fully theirs.
- "TOBIAS MAUEL" — first + last name from his dad off-screen. The universal *parent uses your full name when furious* move, plus a final "WAS ZUM FICK" for the kill shot. Each word on its own page break; pacing is the joke.
- The full bilingual touch ("hola guapo", "¿estás seguro?") in the waitress lines is enough to read as Spain without translating.
- Scene closes on Tobi's wordless `*sigh*` — surrender. Michel just told the truth ("you puked on yourself"), Dad has already used the full name, there's nothing left to argue. The sigh is the resignation that lands the comedy.

---


## Scene 5 — Blackwing Lair, first raid (comedy beat before the climax)

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

**Guild roster on Vent — using actual WoW handles, not real names** (Tobi will recognize all of these instantly; that's why we use them): **Aronian** (raidlead), **Ozora** = Tobi (heals), **Xoh** = Michel (warlock — player's tag in chat), **Friets** (same handle as IRL nickname), **Ayaro** = BramT, plus **Gerrit**, **Tita**, **Divinity**, **Aerendil** as other "Bound by Blood" guildmates. Every name is a real handle from a real raid — the authenticity is the joke and the love letter at once.

**Draft dialogue (first pass):**

```
[Years later.]
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
           < Bound by Blood >

[Banner fades after 2 seconds.
"Bound by Blood" lingers half
a second longer — that's the
guild Michel just joined.]

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
              <Ozora> xoh u
              hear that
              [▼]
              <Xoh> ya all good
              [▼]
              <Xoh> just gonna
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
              [▼]
              <Ayaro> well that's
              that

VENT CHAT:    <Aronian> WHO
              [▼]
              <Aronian> WHO
              PULLED
              [▼]
              <Ozora> oh my god
              [▼]
              <Ozora> oh my GOD
              [▼]
              <Aronian> WIPE IT
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
              <Ozora> uhhhh
              [▼]
              <Ozora> my friend
              [▼]
              <Gerrit> oof
              [▼]
              <Friets> RIP xoh
              [▼]
              <Aronian> hes off
              the team
              [▼]
              <Aronian> demoted.
              casual rank.
              [▼]
              <Tita> sorry xoh
              :(
              [▼]
              <Aerendil> a noble
              attempt friend
              [▼]
              <Divinity> ...
              [▼]
              <Ayaro> rough buddy
              [▼]
              <Ozora> xoh
              [▼]
              <Ozora> ...
              [▼]
              <Ozora> spasti.
              [▼]
              <Xoh> yeah ok
              fair

[Scene fades.
Both of them are laughing
by the end. You can tell.]
```

**Notes on this draft:**
- Vent chat formatted as a chat log inside the dialogue box — `<Name> text` cadence is instantly recognizable to anyone who voice-chatted in 2005.
- The "[Years later.]" caption at the top is the only time-skip marker the player needs — the BLACKWING LAIR banner does the rest of the re-orientation work.
- "<Ozora> spasti." in the post-wipe chat is the word in its established warm shared-shorthand mode (developed in Sc 3-4). Casual friend-banter affection in voice chat. (Aachen hasn't happened yet — this is the word still light, before it gets weaponized as a shield in Sc 6.)
- Aronian's "who is this guy" deliberately mirrors Tobi's Scene 1 line. Different room, same question, very different answer this time.
- Pokémon-style **`! ! !`** alarm (the same one used when a trainer spots you) for the spawn trigger — it's a perfect canonical glyph for "oh no."
- No music during the wipe. Music returns when the screen fades.

**Locked:**
- Guild: **Bound by Blood**
- Demotion: real.

**Still need (optional polish):**
- Year? (BWL was current content roughly 2005–2006 — sets your age.)
- Are the personality reads above (Friets = the LMAO guy, Aerendil = lore-serious, Divinity = quiet "...", Tita = the empath, Gerrit = the curt warrior) right or wrong? Easy to reassign if so.

---
## Scene 6 — Aachen, the club stairs (CLIMAX)

**Setting:** Two tilemaps, played as one continuous scene:
1. **Bar interior** — Aachen club, dark palette, a few dancing NPC silhouettes, bass-thump SFX, an exit door on one wall.
2. **Outside / stairs** — street, night, the club facade with a front stairway leading up to the door, bouncer NPC silhouette to one side.

The scene is a single emotional unit but visually transitions: bar → follow → exit → camera pan up the stairs → settle on Tobi.

**Asset notes:** Bar interior — palette-swap any Crystal nightclub-adjacent tile (or repurpose a dark cave tile). Outside — Crystal city street tile palette-swapped to night (three values, no whites). Bouncer = silhouette only. The hug = sprites pause adjacent, optional small `♥` icon (canonical Pokémon emote in `gfx/emotes/`) or just sprite overlap.

**The spine (per user's recollection):** Tobi knew his mom had died that morning. He spent the whole day with the group anyway, and the whole night, because he didn't want to ruin it. Michel realizing this — that Tobi chose to carry it alone for the friends' sake — is the moment the bond becomes brotherhood. *That* is what the player has to feel. Not the death. The choice.

**Word policy:** "spasti" is absent through the heavy beats of this scene — the word is too small for what's happening. Its absence is the signal that we're somewhere sacred. It returns at the very end, transformed once more: Michel's "Halt's Maul du Spasti" as a shield, then Tobi's "...Spastis." as a shared shield. The recovery happens *within* this scene, not after.

**Draft dialogue:**

```
[INSIDE THE CLUB. AACHEN.
Late. Dim red and blue tile
palette. Two NPC silhouettes
dancing. The exit door is on
the east wall.]

[Music: AACHEN BEAT —
generic four-on-the-floor
club track, GBC chiptune.
Pulse 1 + noise channel
carry the beat. Plays at
full volume inside; loops
through the entire scene
but gets MUFFLED (filtered,
lower-pitched, half-volume)
the moment the door closes.
Continues through the silence,
the hug, the narrator, the
snap. The world doesn't stop
partying just because Tobi's
has ended.]

[Michel-sprite stands near
the bar. Tobi-sprite is
across the room.]

[Tobi-sprite starts walking
toward the exit. No words.
He doesn't look back.]

[Player gets a prompt:]
NARRATOR: ▼ Follow.

[Player walks Michel-sprite
after Tobi, through the
door.]

[Door closes behind them.
Bass cuts to muffled.]

[BLACK. One beat of silence.]

[CAMERA fades up on the
street. Curb at the bottom
of the screen.]

[SCY pans up the screen,
revealing: street → bouncer
silhouette at the door →
stairway → Tobi-sprite
alone at the top, looking
at nothing.]

[Pan stops. Michel-sprite
fades in at the bottom of
the stairs.]

[Player walks Michel up the
stairs. Each step is one
frame, one beat.]

[Michel-sprite settles down
next to Tobi.]

[Long silence. The bass from
inside is muffled by the
door. The bouncer doesn't
look over.]

[A beat.]
[Another beat.]

TOBI:     ...

[Tobi-sprite shakes. Once.
Then again. Then doesn't
stop.]

[Michel reads it on his face.
Nothing said.]

[Michel-sprite scoots over.
The sprites overlap. A small
♥ floats up and fades.]

           - hug -

[They stay like that. The
bass keeps thumping. Time
passes. Neither of them
moves.]

[Long quiet.]

TOBI:     ...
          [▼]
          thanks.

MICHEL:   yeah.

[They sit there.]

[A long beat.]

NARRATOR: that night moved
          me.
          [▼]
          your strength —
          to have held this
          in all day.
          [▼]
          but it also moved
          me closer to you.
          [▼]
          you were my
          brother now.
          [▼]
          and i'd move
          heaven and earth
          to protect you.

[A beat. The bass keeps
thumping. Two NPC-sprites
saunter past the entrance,
elbowing each other.]

NPC 1:    HAH

NPC 2:    GAY!

[Michel-sprite stands up.
Fast.]

MICHEL:   Halt's Maul
          du Spasti.

           ! ! !

[Screen shakes. NPCs turn
and walk off fast. No
parting words.]

[Michel-sprite sits back
down. Close to Tobi.]

[A beat.]

TOBI:     ...
          [▼]
          ...Spastis.

MICHEL:   yeah.

[They sit there.]

[NARRATOR: ▼ Walk on.]
```

**Notes on this draft:**
- **Cold-open structure:** scene begins inside the bar, player follows Tobi out, camera pans up the stairs to reveal him sitting alone, player walks Michel up to him. The player physically performs the *noticing* and the *following*. No exposition needed — by the time they sit down together, the player has already committed to being there with Tobi.
- **Tobi doesn't say it out loud.** He just gives "..." and starts shaking. Michel reads it on his face. The player is left to infer what happened — and Tobi (the audience) doesn't need to be told what he already remembers. The narrator coda retroactively confirms the "all day" weight without a single explicit line of explanation. This is the strongest restraint in the whole ROM.
- **Music continues through everything.** The Aachen club beat doesn't stop when they walk out — it just gets muffled by the door, and keeps playing through the silence, the hug, the narrator, the snap. The world keeps partying while Tobi's world has ended. That contrast is the gut-punch.
- **Catcallers placed AFTER the narrator coda, not before.** The narrator declares the vow ("i'd move heaven and earth to protect you") — and within seconds, the world tests it. Michel doesn't fight; he just snaps back, in German, with the word that belongs to them. Declaration → test → action → recovery.
- **NPCs leave fast, no parting words.** They turn and walk off. The scene doesn't waste oxygen on them.
- **"spasti" spine of the scene:** Michel says "Halt's Maul du Spasti" pointing it outward as a shield. Tobi closes the scene with "...Spastis." — plural, German declension, *Tobi joining Michel in the protective stance*. The word is now their *shared* shield, not just Michel's. The arc through the whole ROM: dismissal → peer pressure (absent) → quiet affection → shared shorthand → Michel's outward shield → Tobi's plural echo confirming the alliance.
- "HAH" / "GAY!" — two NPCs, two words, syncopated jock mockery. Period-accurate teen homophobia, dispatched in two text boxes so the snap that follows hits harder.
- "Halt's Maul du Spasti" — the German switch is the *seriousness signal*. Michel doesn't snap in English. He goes home-language, which is the language he and Tobi share. The Aachen-Cologne contraction "Halt's" instead of "Halt dein" is dialect-accurate.
- The `- hug -` notification + tiny `♥` is intentionally Pokémon-shaped. It lets the moment have a *glyph* without being saccharine.
- "thanks." / "yeah." is the spoken bookend. Then long silence. Then the narrator lands.
- **Narrator block** — user's own words. Michel's thought arriving in the quiet after the words are done. This is the one moment in the scene the inside-voice surfaces, and it's why the rest of the scene can stay so spare.

**Scene 7 implications:**
- The "all day" insight is *named here*, in Scene 6, in the user's own words. Scene 7 must NOT re-explain it. Scene 7 acts on it instead: Michel asks because Tobi is the person revealed in this scene, and has been ever since. No re-narrating the same moment.

---

## Scene 7 — Garden BBQ / The Ask

**Inheriting from Scene 6:** The brother-truth was already named in Aachen ("you were my brother now. and i'd move heaven and earth to protect you."). Scene 7 must NOT re-narrate Aachen — that would deflate it. Scene 7 *acts on* what was named. Aachen flows *directly* into this scene (no comedy interlude between them); the narrator vow at the end of Sc 6 is the immediate setup for the ask.

**Setting:** Garden, afternoon, sunny. A BBQ smoking in the back. Friends scattered as NPC sprites at a picnic table or standing around. **BramS** (the best-man-to-be — handle: **Freak0r**, NOT the same person as BramT from Scene 3) by the grill with a beer. Tobi-sprite at a picnic table.

**IRL frame:** this scene matches the actual BBQ at which Michel will hand Tobi (and, separately, BramS) his cartridge. The in-game scene IS the live moment of presentation.

**Cover-art note:** BramS's handle **Freak0r** appears on BramS's cartridge cover. Tobi's cartridge cover correspondingly should feature **Ozora**. Each cartridge personalized to its recipient by handle — the shared brand reads "BESTMEN" with the recipient's handle as subtitle / sigil.

**Asset notes:** Outdoor day palette (`gfx/tilesets/johto.png` recolored sunny). Custom 8×8 props: grill (with smoke animation if budget allows), picnic table, beer bottles. BramS NPC sprite — pick a distinctive silhouette so Tobi knows instantly who it is.

**Draft dialogue:**

```
[GARDEN. AFTERNOON. SUN.]
[A BBQ smokes in the back.
BramS-sprite by the grill,
beer in hand. Friends as
NPC sprites scattered.]

[Tobi-sprite at a picnic
table.]

[Michel-sprite walks in.]

BRAMS:    Yo Mich

MICHEL:   yo

[Michel-sprite walks to the
picnic table. Sits down
opposite Tobi.]

MICHEL:   tobi.

TOBI:     ...
          [▼]
          michel.

[A beat. The BBQ smokes.]

MICHEL:   this whole game
          was a question.

[Music: TRAINS main motif
returns. Quiet. Same wave
channel as Scene 3. Carries
through the rest of the
scene.]

NARRATOR: 20+ years, tobi.
          [▼]
          everything we've
          been through.
          [▼]
          every fight.
          every laugh.
          every loss.
          [▼]
          and somehow it
          just kept getting
          deeper.
          [▼]
          stronger.
          [▼]
          every year.

MICHEL:   will you be my
          best man?

> Yes
  Heil Yes

[Either choice plays the
same response.]

       *POOF*
[♪ ITEM GET ♪ — short
fanfare on pulse channels;
TRAINS motif resumes after.]
TOBI got
BEST MAN BADGE!

[Beat.]

TOBI:     ...
          [▼]
          spasti.
          [▼]
          of course.

[Screen fades to title.
TRAINS motif resolves on
the title card.]

           ╔══════════════╗
           ║   BESTMEN    ║
           ║              ║
           ║   Ozora      ║
           ╚══════════════╝
```

(The title-card sigil = the recipient's WoW handle. Tobi's ROM ends on "Ozora." BramS's ROM ends on "Freak0r." Each man's own name as the closing chord.)

**Notes on this draft:**
- **No callbacks at the open.** Scene starts tight: "tobi." / "michel." A beat. Then the meta-collapse. Restraint over recap.
- **"this whole game was a question."** One sentence collapses the entire ROM. Doesn't recap a single scene; just names what the player has been doing for the last 8 minutes.
- **Storyteller narrator block** between the meta-collapse and the ask: names the *years*, the *through-things*, and the *direction* (deeper, stronger, every year). Doesn't list specific scenes — that would be recap. Names the *trajectory* the player has just walked through. The TRAINS motif plays under it, doing the emotional work in parallel.
- **No "ask it" permission line.** Tobi doesn't speak between the narrator block and the ask — Michel just goes straight from "every year." into "will you be my best man?" The narrator carries the entire bridge.
- **[Yes] / [Heil Yes].** Two yeses. The German pun on "Hell yes" lands in their shared vocabulary. Either choice leads to the same response — there is no "no" branch, because there never was.
- **BEST MAN BADGE.** Pure Pokémon item-get nostalgia. The fanfare, the floating item, the all-caps received-item line. Period-correct. Could even reuse the actual Crystal `♪ ITEM GET ♪` jingle if we can rip the macro.
- **Tobi's closing "spasti. of course."** The word's final use. Quiet again, like Scene 3. Means "yes, you idiot, of course it's yes."
- **Title card "BESTMEN / Ozora"** — recipient's WoW handle as sigil. BramS's ROM will end the same way on "Freak0r." Each cartridge is HIS game.
- **TRAINS motif reprise.** The same melody that played in Scene 3 returns when Michel says "this whole game was a question." Carries through the ask, the item-get fanfare, and resolves on the title card. The music answers what the words can't — and bookends the emotional core of the ROM.

**Open / optional:**
- Post-credits? Could roll a short credit scroll naming everyone — Tobi, BramS, BramT, Benny, Friets, Aronian, Gerrit, Tita, Divinity, Aerendil, Conzi — kind of a "the cast of your life" beat. Or end clean on the title card. Up to you.

---

## Status (project-level)

Drafted with dialogue: Sc 1, 2, 3, 4, 5, 6, 7.

**Locked decisions:** nickname (Tobi), spasti as recurring thread, BramT/BramS disambiguation, WoW handles (Ozora/Xoh/Ayaro/Friets/Freak0r), Bound by Blood guild name, real demotion in BWL, Aachen narrator coda (user's own words), catcallers after the coda (Halt's Maul du Spasti), Heil Yes option, BBQ as present-day setting, title-card sigil = handle.

**Music decisions (locked):**
- **TRAINS main motif** (Porcupine Tree) — GBC chiptune recreation. Debuts in Scene 3, reprises in Scene 7 under the ask, resolves on the title card. Music centerpiece of the ROM.
- **WOW CLASSIC TAVERN THEME** — GBC chiptune recreation. BGM through Scene 2, diegetic to the WoW conversation. Instant guildie-recognition.
- **LA CUCARACHA** — GBC chiptune. BGM through Scene 4 (La Cubanita bar). Cheesy on purpose — tourist-bar score.
- **AACHEN BEAT** — generic four-on-the-floor club track, GBC chiptune. Plays through Scene 6 entirely: full volume inside the bar; muffled (filtered + lower-pitched + half-volume) the moment the door closes. Continues unbroken through the silence, the hug, the narrator coda, and the snap. The world doesn't stop partying while Tobi's has ended.
- BWL scene (5) gets its own short combat-tense track or silence-with-SFX during the wipe; music returns after.
- Other scenes: silence + ambient SFX (BBQ crackle, etc.) unless a track earns its way in.

**Asset summary** (per-scene asset notes live in each scene's body; this is the rollup):
| Scene | Reuse from `gfx/pokecrystal-src/` | Custom needed |
|---|---|---|
| 1 Classroom | `gfx/tilesets/elms_lab.png` palette swap | Tobi NPC + dress-shirt Michel palette |
| 2 Schoolyard | `gfx/tilesets/johto.png` | Friets, BramT NPC sprites (or reuse Crystal NPCs) |
| 3 BramT living room | `gfx/tilesets/house1.png` | BramT, Benny NPC sprites + 8×8 guitar prop |
| 4 La Cubanita | recolor Crystal pub/cafe tile | waitress NPC palette, drunk-Tobi sprite variant, Tobi's-dad silhouette |
| 5 BWL | `gfx/tilesets/cave.png` red palette | dragon-egg props, zone-banner overlay, `! ! !` glyph (Crystal stock) |
| 6 Aachen | Crystal nightclub-adjacent tile + night street tile | bouncer silhouette, hug-pair frame or ♥ overlay |
| 7 BBQ | `johto.png` sunny palette | BramS NPC, grill 8×8 prop, BEST MAN BADGE item sprite, title-card overlay |

**Open / non-blocking:**
- Year for Scene 6 (BWL was current ~2005–2006; want it accurate?)
- Personality reads for guildmates in BWL chat (Friets = LMAO etc.) — confirm or reassign
- BramS line in Scene 7 or silent at grill (my instinct: silent)
- Post-credits "cast of your life" scroll or clean title-card exit
