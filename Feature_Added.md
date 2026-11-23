# 🃏 Vanilla Moded World — Features & Roadmap

A comprehensive registry of all implemented features and upcoming ideas for the **VanillaModedWorld** Balatro expansion mod.

---

## 📑 Quick Navigation

- [📋 Quick-Copy Templates](#-quick-copy-templates) *(Copy-paste to add new ideas quickly)*
- [🃏 Jokers](#-jokers)
  - [Implemented Jokers](#implemented-jokers)
  - [Planned Jokers (Backlog)](#planned-jokers-backlog)
- [🔮 Tarots](#-tarots)
  - [Implemented Tarots](#implemented-tarots)
  - [Planned Tarots (Backlog)](#planned-tarots-backlog)
- [👻 Spectrals](#-spectrals)
- [🖐️ Poker Hands](#️-poker-hands)
- [🪐 Planets](#-planets)
- [🎟️ Vouchers](#-vouchers)
  - [Implemented Vouchers](#implemented-vouchers)
  - [Planned Vouchers (Backlog)](#planned-vouchers-backlog)
- [🎴 Decks](#-decks)
  - [Implemented Decks](#implemented-decks)
  - [Planned Decks (Backlog)](#planned-decks-backlog)
- [🎴 Sleeves (CardSleeves Mod)](#-sleeves-cardsleeves-mod)
  - [Implemented Sleeves](#implemented-sleeves)
  - [Planned Sleeves (Backlog)](#planned-sleeves-backlog)
- [✨ Seals, Enhancements & Editions](#-seals-enhancements--editions)

---

## 📋 Quick-Copy Templates

Copy and paste any of these snippets below whenever you want to add a new card or feature!

### 🃏 Joker Template
```markdown
- **[Name]**
  - **Rarity**: Common / Uncommon / Rare / Legendary
  - **Cost**: $[Cost]
  - **Blueprint Compatible**: Yes / No
  - **Effect**: [Describe what the joker does]
  - **Art Concept**: [Describe the card visual, colors, and motif]
  - **Notes / Mechanics**: [Edge cases, formulas, interactions]
```

### 🔮 Consumable Template (Tarot / Spectral / Planet)
```markdown
- **[Name]**
  - **Type**: Tarot / Spectral / Planet
  - **Cost**: $[Cost]
  - **Target**: [e.g. 1 selected card / Hand type / Entire deck]
  - **Effect**: [Describe the consumable effect]
  - **Art Concept**: [Visual style, parchment symbols, color scheme]
```

### 🎴 Deck / Sleeve Template
```markdown
- **[Name]**
  - **Type**: Deck / Sleeve
  - **Base Effect**: [Effects when playing normally]
  - **Sleeve Combo / Alt Effect**: [Special synergy when paired with matching Deck]
  - **Art Concept**: [Card back pattern, pocket frame, colors]
```

---

## 🃏 Jokers

### Implemented Jokers

| Joker | Rarity | Cost | Blueprint | Effect Summary | File |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Espresso** | `Common` | $4 | Yes | **X2 Mult** on first hand of round; **1 in 20 chance** to transform into **Double Espresso** | [`espresso.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/espresso.lua) |
| **Double Espresso** | `Common` | $4 | Yes | Each played **2** gives **X2 Mult** when scored *(Only obtainable via Espresso transformation)* | [`double_espresso.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/double_espresso.lua) |
| **Lucky Clover** | `Common` | $4 | Yes | Scored **Lucky 4 of Clubs** are guaranteed to trigger all Lucky effects (**+20 Mult** and **$20**) | [`lucky_clover.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/lucky_clover.lua) |
| **Hot Pepper** | `Common` | $4 | Yes | Each played card gives **X1.2 Mult** when scored. **Self-destructs** when **Boss Blind** is defeated | [`hot_pepper.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/hot_pepper.lua) |
| **Stone Tablet** | `Common` | $4 | Yes | Retrigger all **Seals** on **Stone Cards** (doubles their effects) | [`stone_tablet.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stone_tablet.lua) |
| **Overkill** | `Common` | $4 | Yes | Creates a **Spectral** card when **Boss Blind** is defeated if any single hand scored at least **2X** the Blind requirement | [`overkill.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/overkill.lua) |
| **Spotlight** | `Common` | $4 | Yes | If played hand is a **5-card High Card**, **randomizes** the scoring card's **Enhancement**, **Edition**, and **Seal** | [`spotlight.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/spotlight.lua) |
| **Short Circuit** | `Common` | $4 | Yes | If a scored card is **retriggered**, has a **1 in 2 chance** to retrigger its **neighbors** as well | [`short_circuit.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/short_circuit.lua) |
| **Sphene** | `Uncommon` | $6 | Yes | Played **Diamond** cards have a **1 in 3 chance** to be **retriggered** | [`sphene.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/sphene.lua) |
| **Ruby Heart** | `Uncommon` | $6 | Yes | Played **Heart** cards have a **1 in 3 chance** to be **retriggered** | [`ruby_heart.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/ruby_heart.lua) |
| **Black Diamond** | `Uncommon` | $6 | Yes | Played **Spade** cards have a **1 in 3 chance** to be **retriggered** | [`black_diamond.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/black_diamond.lua) |
| **Emerald** | `Uncommon` | $6 | Yes | Played **Club** cards have a **1 in 3 chance** to be **retriggered** | [`emerald.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/emerald.lua) |
| **Sticky Note** | `Common` | $4 | Yes | Retriggers the **first card** held in hand **2 additional times** | [`sticky_note.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/sticky_note.lua) |
| **Camera** | `Common` | $5 | Yes | First **numbered** card (2-10) **held in hand** gives **X2 Mult** | [`camera.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/camera.lua) |
| **Frugal Joker** | `Uncommon` | $6 | Yes | Each **Diamond** card held in hand gives **$1** | [`frugal_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/frugal_joker.lua) |
| **Fickle Joker** | `Uncommon` | $6 | Yes | Each **Heart** card held in hand has a **1 in 4 chance** to give **X1.5 Mult** | [`fickle_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/fickle_joker.lua) |
| **Stoic Joker** | `Uncommon` | $6 | Yes | Each **Spade** card held in hand gives **+25 Chips** | [`stoic_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stoic_joker.lua) |
| **Stubborn Joker** | `Uncommon` | $6 | Yes | Each **Club** card held in hand gives **+4 Mult** | [`stubborn_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stubborn_joker.lua) |
| **The Bell** | `Uncommon` | $6 | Yes | Retriggers scoring cards based on distance from margins (Gaussian curve up to +2) | [`the_bell.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/the_bell.lua) |
| **Fortune Cookie** | `Uncommon` | $6 | No | When **sold**, creates **1** random **Tarot** and **1** random **Spectral** card *(Must have room; Spectral first)* | [`fortune_cookie.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/fortune_cookie.lua) |
| **Wrong Schematics** | `Uncommon` | $7 | Yes | **1 in 2 chance** to copy right Joker or left Joker; copies **both** if probability reaches 2 in 2 (e.g. *Oops! All 6s*) | [`wrong_schematics.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/wrong_schematics.lua) |
| **Magifect** | `Uncommon` | $6 | Yes | Retriggers all **Editions** (Foil, Holographic, Polychrome) for every Joker | [`magifect.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/magifect.lua) |
| **Jackpot** | `Uncommon` | $6 | Yes | If played hand contains at least **3 scoring 7s**, each scored 7 awards **$6** | [`jackpot.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/jackpot.lua) |
| **MultiFaces** | `Uncommon` | $6 | Yes | Converts played **2s** into **Jacks**, **3s** into **Queens**, and **4s** into **Kings** when played | [`multifaces.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/multifaces.lua) |
| **Bonus Stage** | `Uncommon` | $6 | Yes | Retrigger all played **Bonus Cards** | [`bonus_stage.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/bonus_stage.lua) |
| **Overdrive** | `Uncommon` | $6 | Yes | Retrigger all played **Mult Cards** | [`overdrive.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/overdrive.lua) |
| **Kaleidoscope** | `Uncommon` | $6 | Yes | Retrigger all played **Wild Cards** | [`kaleidoscope.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/kaleidoscope.lua) |
| **The Anvil** | `Uncommon` | $6 | Yes | Retrigger all played **Steel Cards** | [`the_anvil.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/the_anvil.lua) |
| **Monolith** | `Uncommon` | $6 | Yes | Retrigger all played **Stone Cards** | [`monolith.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/monolith.lua) |
| **Bullion** | `Uncommon` | $6 | Yes | Retrigger all played **Gold Cards** | [`bullion.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/bullion.lua) |
| **Glassblower** | `Uncommon` | $6 | Yes | Retrigger all played **Glass Cards**, **1 in 25 chance** to break when retriggering | [`glassblower.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/glassblower.lua) |
| **Golden Horseshoe** | `Uncommon` | $6 | Yes | **1 in 3 chance** to retrigger each played **Lucky Card** | [`golden_horseshoe.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/golden_horseshoe.lua) |
| **Antivirus** | `Common` | $4 | Yes | **+2 Chips** for each **unique card** in your full deck | [`antivirus.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/antivirus.lua) |
| **Taxi Driver** | `Rare` | $8 | Yes | Earn **$1** for each **scoring card** (when hand is scored) | [`taxi_driver.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/taxi_driver.lua) |
| **River** | `Rare` | $8 | Yes | Adds the **Chips** and **Mult** of the poker hand held in **hand** when hand is scored | [`river.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/river.lua) |
| **Doubler** | `Rare` | $8 | No | When **sold**, doubles all numerical values of a random owned Joker | [`doubler.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/doubler.lua) |
| **Burnt Offering** | `Rare` | $8 | Yes | Destroys **1 random card** from the 1st played hand of each round and creates a random **Tarot** | [`burnt_offering.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/burnt_offering.lua) |
| **The Scythe** | `Rare` | $8 | Yes | If first hand of round has **3 cards**, destroys 2 side cards & copies the middle card | [`the_scythe.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/the_scythe.lua) |
| **Stańczyk** | `Legendary` | $20 | No | Creates a **Negative + Eternal + Rental** copy of a random other owned Joker *(Stańczyk excluded)* when a **Boss Blind** is defeated | [`stanczyk.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stanczyk.lua) |
| **Sommers** | `Legendary` | $20 | Yes | Gains **+20 Chips** per discarded **Blue Seal** card; gains **X0.25 Mult** per discarded **Red Seal** card | [`sommers.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/sommers.lua) |

<details open>
<summary><b>🔍 Detailed Joker Profiles</b> (Click to collapse/expand)</summary>

#### ☕ Espresso
- **Key**: `j_vmw_espresso`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `{X:mult,C:white}X#1#{} Mult on {C:attention}first hand{} of round, {C:green}#2# in #3#{} chance to transform into {C:attention}Double Espresso{}. {C:inactive}(Played {C:attention}2s{} give {X:mult,C:white}X2{} Mult){}`
- **Art Concept**: Italian porcelain demitasse cup with gold-rimmed saucer, rich terracotta-ruby ceramic body, coffee bean crest, velvety hazelnut crema swirl with golden highlight glints, rising steam wisps, roasted coffee beans, and vertical `JOKER` lettering.
- **Files**: [`espresso.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/espresso.lua) | [`j_espresso.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_espresso.png)

#### ☕☕ Double Espresso
- **Key**: `j_vmw_double_espresso`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `Each played {C:attention}2{} gives {X:mult,C:white}X#1#{} Mult when scored.`
- **Availability**: Special Evolution only — cannot appear in shops or booster packs; obtainable only when **Espresso** transforms.
- **Art Concept**: Twin demitasse cups resting on an elongated porcelain saucer (front terracotta cup with double bean crest, back mahogany cup with gold rim), double swirling crema, intertwining double steam plumes, energetic golden coffee sparkles, and vertical `JOKER` lettering.
- **Files**: [`double_espresso.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/double_espresso.lua) | [`j_double_espresso.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_double_espresso.png)

#### 🔔 The Bell
- **Key**: `j_vmw_the_bell`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Scoring cards are {C:attention}retriggered{} based on distance from margins {C:inactive}(ex: 5 cards -> +0, +1, +2, +1, +0){}.`
- **Trigger Distribution**:
  - 5 cards played: `[ +0 | +1 | +2 | +1 | +0 ]` *(center card retriggers 2 times, flanks retrigger 1 time)*
  - 4 cards played: `[ +0 | +1 | +1 | +0 ]` *(middle two cards retrigger 1 time)*
  - 3 cards played: `[ +0 | +1 | +0 ]` *(center card retriggers 1 time)*
  - 2 cards played: `[ +0 | +0 ]` *(no retriggers)*
  - 1 card played:  `[ +0 ]` *(no retriggers)*
- **Art Concept**: Heavy golden cast cathedral bell suspended from a dark wooden headstock beam with iron bolts, flared sounding rim with specular highlights, dark interior mouth with swinging heavy bronze clapper, radiating cyan Gaussian / bell-curve acoustic waveform ripples, floating acoustic sparkles, and vertical `JOKER` lettering.
- **Files**: [`the_bell.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/the_bell.lua) | [`j_the_bell.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_the_bell.png)

#### 🍀 Lucky Clover
- **Key**: `j_vmw_lucky_clover`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `Each scored {C:attention}Lucky 4 of Clubs{} is guaranteed to trigger all {C:attention}Lucky Card{} effects {C:inactive}(+20 Mult and $20){}.`
- **Art Concept**: Four-leaf emerald clover with delicate golden venation, Celtic center knotting, curving stem, floating golden sparkles, and vertical `JOKER` lettering.
- **Files**: [`lucky_clover.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/lucky_clover.lua) | [`j_lucky_clover.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_lucky_clover.png)

#### 🥠 Fortune Cookie
- **Key**: `j_vmw_fortune_cookie`
- **Archetype**: Food / Consumable Economy
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: No (trigger on sell)
- **Effect**: `When {C:attention}sold{}, creates {C:attention}1{} random {C:tarot}Tarot{} card and {C:attention}1{} random {C:spectral}Spectral{} card. {C:inactive}(Must have room; generates {C:spectral}Spectral{} first if only 1 slot){}.`
- **Art Concept**: Crisp, golden-brown fortune cookie cracked cleanly in half with toasted highlight ridges, hollow caramel interior, and crumb flecks. A small white fortune paper slip protrudes from between the halves, printed with a tiny dithered cyan Planet symbol and purple Tarot symbol, surrounded by lucky golden sparkles and vertical `JOKER` lettering.
- **Files**: [`fortune_cookie.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/fortune_cookie.lua) | [`j_fortune_cookie.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_fortune_cookie.png)

#### 🌶️ Hot Pepper
- **Key**: `j_vmw_hot_pepper`
- **Archetype**: Food / Temporary Burst
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `Each played card gives {X:mult,C:white}X#1#{} Mult when scored. {C:red}Self-destructs{} when {C:attention}Boss Blind{} is defeated.`
- **Art Concept**: Curved, glossy bright red cayenne chili pepper with deep red shadow volume, radiant white specular shine streaks, and a fresh emerald-green stem calyx. Sits against a dynamic backdrop of roaring orange, gold, and white-hot fire tongues rising behind the pepper, with embers and heat sparks, inner coral border, and vertical `JOKER` lettering.
- **Files**: [`hot_pepper.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/hot_pepper.lua) | [`j_hot_pepper.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_hot_pepper.png)

#### 🚕 Taxi Driver
- **Key**: `j_vmw_taxi_driver`
- **Rarity**: Rare | **Cost**: $8
- **Blueprint Compatible**: Yes
- **Effect**: `Earn {C:money}$#1#{} for each {C:attention}scoring card{} {C:inactive}(when hand is scored){}`
- **Mechanics**:
  - Triggers during `context.joker_main` (hand calculation).
  - Inspects `context.scoring_hand` to count all scored cards (e.g., 5 cards for Flushes/Straights/Full Houses, 2 for Pairs, 1 for High Card), awarding $1 per scoring card.
  - Compatible with Blueprint and Brainstorm to duplicate the cash payout.
- **Art Concept**:
  - Starts directly from the authentic vanilla Jimbo (`j_joker`) character sprite, preserving Jimbo's iconic jester face, eye markings, red nose, and signature wide grin.
  - Wearing a taxi-yellow flat cabbie cap with a visor, an iconic black-and-white checkered brow band, and a golden brass taxi medallion in the center.
  - Illuminated yellow rooftop "TAXI" sign perched on top of his cap with amber indicator lights.
  - Taxi-yellow driver uniform with a black-and-white checkered necktie.
  - Gripping a circular 3-spoke driver steering wheel with white-gloved hands right in front of his chest.
  - Authentic standing posture with Jimbo's feet visible below the wheel.
- **Files**: [`taxi_driver.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/taxi_driver.lua) | [`j_taxi_driver.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_taxi_driver.png)

#### 🪨 Stone Tablet
- **Key**: `j_vmw_stone_tablet`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all {C:attention}Seals{} on {C:attention}Stone Cards{} {C:inactive}(doubles their effects){}`
- **Mechanics**:
  - Triggers whenever a **Stone Card** with a Seal activates its effect:
    - **Red Seal**: Retrigger the Stone Card 1 additional time (`repetitions = 1`), doubling its retrigger effect.
    - **Gold Seal**: Awards an additional **$3** (`dollars = 3`) when the Stone Card scores, doubling the payout to $6.
    - **Purple Seal**: Creates an additional **Tarot card** when the Stone Card is discarded (if consumable slots allow).
    - **Blue Seal**: Creates an additional **Planet card** for the final poker hand when held in hand at end of round (if room allows).
    - **Modded Seals**: Compatible with custom seals by triggering an additional evaluation pass.
  - Automatically displays the **Stone Card** tooltip via `info_queue`.
  - Fully compatible with **Blueprint** and **Brainstorm** to add further seal triggers.
- **Art Concept**:
  - Built directly on top of the authentic in-game **Stone Card** background texture extracted from vanilla Balatro.
  - Ancient weathered cracked stone face with a major organic fracture fissure running down the tablet face.
  - "JOKER" engraved horizontally across the top in ancient chiseled relief lettering with 3D stone shadows and sunlit highlights (no side text).
  - Two deeply engraved circular seal petroglyphs matching real stone petroglyphs:
    - Upper right seal: concentric double chiseled rings with a carved cross / X stamp mark.
    - Lower right seal: concentric double chiseled rings with carved flowing wave / spiral petroglyphs.
  - Left side petroglyphs: ancient carved sun-pillar, T-pillar with diagonal slashes, and triangular star glyph.
  - Everything looks carved directly into the living rock face.
- **Files**: [`stone_tablet.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stone_tablet.lua) | [`j_stone_tablet.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_stone_tablet.png)

#### 💥 Overkill
- **Key**: `j_vmw_overkill`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `Creates a {C:spectral}Spectral{} card when {C:attention}Boss Blind{} is defeated if any single hand scored at least {C:attention}2X{} the Blind requirement {C:inactive}(Must have room){}`
- **Mechanics**:
  - Triggers during `context.after` in a **Boss Blind** round:
    - Calculates the individual score achieved by the played hand (`SMODS.last_hand_score` or `hand_chips * mult`).
    - If `hand_score >= G.GAME.blind.chips * 2`, the condition is satisfied (`overkill_achieved = true`) and the Joker immediately flashes with an *"Overkill!"* spectral popup and juice animation.
    - As long as at least one single hand scored equal to or greater than 2X the Boss Blind's total chip requirement, the award is unlocked.
  - At `context.end_of_round`, upon defeating the Boss Blind:
    - If `overkill_achieved` is true and there is consumable room (`#G.consumeables.cards + G.GAME.consumeable_buffer < G.consumeables.config.card_limit`), creates 1 random **Spectral** card with authentic sound effects and juice.
    - Fully compatible with **Blueprint** and **Brainstorm** to spawn additional Spectral cards if consumable room allows.
- **Art Concept**:
  - Heavy cast iron mortar / artillery cannon angled up and to the right at 35 degrees with polished brass reinforcement bands and rivet details.
  - Engraved skull emblem stamped on the cannon breech chamber.
  - Wood-and-bronze wheeled artillery carriage holding the cannon base.
  - Massive billowing mushroom plume of spectral cyan ectoplasm smoke erupting from the muzzle.
  - Embedded grinning ghostly skull silhouette formed directly inside the spectral smoke vapors.
  - Floating cyan spectral stars, soul embers, and wisps drifting outwards.
  - Radial comic-book blast lines in the background.
  - Authentic vertical `JOKER` lettering along the margins with classic Balatro paper shadow.
- **Files**: [`overkill.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/overkill.lua) | [`j_overkill.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_overkill.png)

#### 🔦 Spotlight
- **Key**: `j_vmw_spotlight`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `If played hand is a {C:attention}5-card High Card{}, {C:attention}randomizes{} the scoring card's {C:attention}Enhancement{}, {C:dark_edition}Edition{}, and {C:attention}Seal{}`
- **Mechanics**:
  - Triggers during `context.before` (right before scoring begins) when the played hand evaluates to **High Card** and consists of exactly **5 cards** (`#context.full_hand == 5`).
  - Target card: The single card that scores (`context.scoring_hand[1]`).
  - Completely **randomizes** all 3 dimensions of the card:
    1. **Enhancement Pool**: Bonus, Mult, Wild, Glass, Steel, Gold, Lucky, Stone, and `Pass`. If a specific enhancement rolls, it transforms into that enhancement; if `Pass` rolls, it removes any existing enhancement (restoring to standard base card).
    2. **Edition Pool**: Foil, Holographic, Polychrome, and `Pass`. If an edition rolls, it gains or transforms into that edition; if `Pass` rolls, it removes any existing edition.
    3. **Seal Pool**: Red, Blue, Gold, Purple, and `Pass`. If a seal rolls, it gains or transforms into that seal; if `Pass` rolls, it removes any existing seal.
  - A card can gain, swap, or lose any combination of properties, reshaping the hero card with every 5-card High Card played!
  - Applied immediately before scoring so that the new enhancement, edition, or seal actively contributes to the hand's score.
- **Art Concept**:
  - Dark theatrical stage setting with wooden stage planks and dark purple curtain shadows.
  - Overhead studio spotlight fixture mounted at the top casting a brilliant, warm conical beam of golden and creamy light.
  - Single illuminated hero playing card standing proud in the dead center of the stage pool.
  - 4 shadowy card silhouettes standing back in the dark wings (the uncredited High Card fodder).
  - Floating golden stage dust motes and sparkling stars in the beam.
  - Authentic vertical `JOKER` typography along margins.
- **Files**: [`spotlight.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/spotlight.lua) | [`j_spotlight.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_spotlight.png)

#### ⚡ Short Circuit
- **Key**: `j_vmw_short_circuit`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `If a card is {C:attention}retriggered{}, has a {C:green}#1# in #2#{} chance to retrigger its {C:attention}neighbors{} as well`
- **Mechanics**:
  - Before scoring begins (`context.before`), inspects every card in `scoring_hand` to detect all retrigger events (Red Seals, Hack, Sock and Buskin, Dusk, The Bell, Monolith, Bullion, Glassblower, Hanging Chad, etc.).
  - For each retriggered card at index `i`, its left neighbor (`i - 1`) and right neighbor (`i + 1`) each roll a **1 in 2 chance** (`G.GAME.probabilities.normal / 2`, dynamically scaling with *Oops! All 6s* to 2 in 2 / guaranteed) to catch an electrical arc and be retriggered as well!
  - If a card sits between two retriggering cards, it gets independent chances to catch sparks from both sides!
  - Triggers during card repetition phase (`context.repetition`), showing a `"Zzzzt!"` electric spark popup and retriggering the card.
  - Fully compatible with **Blueprint** and **Brainstorm** to add duplicate arcs.
- **Art Concept**:
  - Printed circuit board (PCB) forest-green substrate covered with gold conductive bus traces, silver solder pads, microchip IC, and color-coded resistor.
  - Scorched burnt crater in the center where an electrical short circuit erupted.
  - Severed red and blue copper wires crossing and violently short-circuiting with bright cyan and core-white high-voltage lightning arcs.
  - Branching lightning bolts arcing outwards towards the left and right card edges (jumping to adjacent neighbor cards!).
  - Exploding electric sparks, plasma bursts, and rising smoke wisps.
  - Authentic vertical `JOKER` typography along margins.
- **Files**: [`short_circuit.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/short_circuit.lua) | [`j_short_circuit.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_short_circuit.png)

#### 💎 Sphene
- **Key**: `j_vmw_sphene`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Played {C:diamonds}Diamond{} cards have a {C:green}#1# in #2#{} chance to be {C:attention}retriggered{}`
- **Mechanics**:
  - Triggers on `context.repetition` for played scoring Diamond cards.
  - Probability scales dynamically with *Oops! All 6s* (`G.GAME.probabilities.normal / 3`).
- **Art Concept**:
  - Warm golden amber / honey plush velvet drape background.
  - Brilliant-cut Rhombus fire gemstone with glowing amber core, dazzling golden facets, signature yellow-green fire dispersion, and sparkling white facet gleams.
  - Authentic white vertical `JOKER` text along margins.
- **Files**: [`sphene.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/sphene.lua) | [`j_sphene.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_sphene.png)

#### 💖 Ruby Heart
- **Key**: `j_vmw_ruby_heart`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Played {C:hearts}Heart{} cards have a {C:green}#1# in #2#{} chance to be {C:attention}retriggered{}`
- **Mechanics**:
  - Triggers on `context.repetition` for played scoring Heart cards.
  - Probability scales dynamically with *Oops! All 6s* (`G.GAME.probabilities.normal / 3`).
- **Art Concept**:
  - Royal burgundy / crimson plush velvet drape background.
  - Brilliantly faceted heart-cut ruby gemstone with vivid crimson core, bright scarlet reflections, and sparkling white facet gleams.
  - Authentic white vertical `JOKER` text along margins.
- **Files**: [`ruby_heart.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/ruby_heart.lua) | [`j_ruby_heart.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_ruby_heart.png)

#### ♠️ Black Diamond
- **Key**: `j_vmw_black_diamond`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Played {C:spades}Spade{} cards have a {C:green}#1# in #2#{} chance to be {C:attention}retriggered{}`
- **Mechanics**:
  - Triggers on `context.repetition` for played scoring Spade cards.
  - Probability scales dynamically with *Oops! All 6s* (`G.GAME.probabilities.normal / 3`).
- **Art Concept**:
  - Deep midnight obsidian / charcoal plush velvet drape background.
  - Faceted Black Diamond with mirror jet-black table facet, brilliant steel-silver triangular crown reflections, and sharp white gleams.
  - Authentic white vertical `JOKER` text along margins.
- **Files**: [`black_diamond.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/black_diamond.lua) | [`j_black_diamond.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_black_diamond.png)

#### ❇️ Emerald
- **Key**: `j_vmw_emerald`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Played {C:clubs}Club{} cards have a {C:green}#1# in #2#{} chance to be {C:attention}retriggered{}`
- **Mechanics**:
  - Triggers on `context.repetition` for played scoring Club cards.
  - Probability scales dynamically with *Oops! All 6s* (`G.GAME.probabilities.normal / 3`).
- **Art Concept**:
  - Deep rich emerald green plush velvet drape background.
  - Brilliant 3-lobed Club gemstone in deep radiant emerald with luminous mint reflections, inner refraction facets, and white sparkle glints.
  - Authentic white vertical `JOKER` text along margins.
- **Files**: [`emerald.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/emerald.lua) | [`j_emerald.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_emerald.png)

> **Note on Reserved Kinetic Group**: The former Kinetic Joker names and designs (`Ricochet`, `Rebound`, `Backlash`, `Aftershock`) are preserved in [`items/jokers/saved_kinetic/`](file:///D:/GG/VanillaModedWorld/items/jokers/saved_kinetic/) for future expansion into a distinct joker archetype.

#### 📝 Sticky Note
- **Key**: `j_vmw_sticky_note`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger {C:attention}first{} card held in hand {C:attention}#1#{} additional times`
- **Mechanics**:
  - Triggers on `context.repetition and context.cardarea == G.hand` for the first card held in hand (`G.hand.cards[1]`).
  - Synergizes with Steel cards (extra X1.5 triggers), Gold cards (extra $3 triggers at end of round), Baron, Shoot the Moon, and the held-in-hand suit Jokers!
- **Art Concept**:
  - Transparent canvas (no white card border) — the entire sprite is the canary-yellow Post-it note pinned with a glossy 3D red pushpin / thumbtack.
  - Handwritten `"JOKER"` in dark ballpoint pen ink at top.
  - Big, detailed doodle of classic Jimbo (3-pointed jester cap with bells, full face oval outline, classic arched brows, nose, wide grin, and collar ruffles).
  - Bottom-right corner curled upward with soft paper drop shadow.
- **Files**: [`sticky_note.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/sticky_note.lua) | [`j_sticky_note.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_sticky_note.png)

#### 📷 Camera
- **Key**: `j_vmw_camera`
- **Rarity**: Common | **Cost**: $5
- **Blueprint Compatible**: Yes
- **Effect**: `First {C:attention}numbered{} card held in hand gives {X:mult,C:white} X#1# {} Mult` `(2, 3, 4... 10)`
- **Mechanics**:
  - Direct counterpart & complement to vanilla **Photograph** and held-in-hand staples like **Baron**: while Photograph buffs played face cards, Camera rewards keeping numbered cards (2 through 10) in hand!
  - Triggers on `context.individual and context.cardarea == G.hand and not context.end_of_round` for the first card in `G.hand.cards` with rank 2 through 10 (`id >= 2 and id <= 10`).
  - Synergizes with **Sticky Note** (retriggers first card held in hand 2 additional times for up to 3x X2 Mult!), **Mime**, **Baron**, and **Shoot the Moon**.
  - Respects debuffed cards (`k_debuffed`) just like vanilla Baron and Shoot the Moon.
- **Art Concept**:
  - High-fidelity pixel art of the modern **Polaroid Now+** instant camera on transparent canvas with soft ground drop shadow.
  - Matte black/charcoal curved plastic body with signature top-right viewfinder hump.
  - Custom `'joker'` branding printed in silver lowercase typography on the bottom-left camera chin.
  - Prominent central autofocus lens with stepped ribbed rings, cyan anti-reflective optical glass reflection arc, and white studio glint.
  - Iconic 5-stripe Polaroid rainbow (Red, Orange, Yellow, Green, Blue) centered beneath the lens.
  - Top-left flash window with frosted horizontal diffusion ridges and center bulb highlight.
  - Bold circular red shutter button on middle-left with 3D bevel.
  - Viewfinder window and glowing cyan `+` feature button on right side.
  - Horizontal film ejection slot along the bottom chin.
- **Files**: [`camera.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/camera.lua) | [`j_camera.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_camera.png)

#### 💰 Frugal Joker
- **Key**: `j_vmw_frugal_joker`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Each {C:diamonds}Diamond{} card held in hand gives {C:money}$#1#{}`
- **Mechanics**:
  - Triggers on `context.individual and context.cardarea == G.hand` when hand scores.
  - Grants $1 for every unplayed Diamond card remaining in hand.
- **Art Concept**:
  - Fluid **marble swirl background texture** recolored in warm golden-amber / honey variance with white margin `JOKER` text.
  - Unique merchant jester wearing a feathered velvet cap with gold diamond brooch, gold-framed jeweler's monocle over eye, white fur-trimmed ermine collar with black tail spots, and clutching an overflowing leather coin pouch with sparkling gold coins.
- **Files**: [`frugal_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/frugal_joker.lua) | [`j_frugal_joker.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_frugal_joker.png)

#### 💘 Fickle Joker
- **Key**: `j_vmw_fickle_joker`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Each {C:hearts}Heart{} card held in hand has a {C:green}#1# in #2#{} chance to give {X:mult,C:white}X#3#{} Mult`
- **Mechanics**:
  - Triggers on `context.individual and context.cardarea == G.hand` when hand scores.
  - Each Heart card in hand rolls 1 in 4 chance for X1.5 Mult (scales with *Oops! All 6s*).
- **Art Concept**:
  - Fluid **marble swirl background texture** recolored in candy ruby-crimson / rose variance with white margin `JOKER` text.
  - Unique romantic jester with sweeping curled horns ending in golden floating hearts, translucent ruby heart-shaped spectacle over eye, cute wink, rosy blushing cheeks, red rose clenched in teeth, and soft pink ruffled lace collar.
- **Files**: [`fickle_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/fickle_joker.lua) | [`j_fickle_joker.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_fickle_joker.png)

#### 🛡️ Stoic Joker
- **Key**: `j_vmw_stoic_joker`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Each {C:spades}Spade{} card held in hand gives {C:chips}+#1#{} Chips`
- **Mechanics**:
  - Triggers on `context.individual and context.cardarea == G.hand` when hand scores.
  - Grants +25 Chips for each Spade card held in hand.
- **Art Concept**:
  - Fluid **marble swirl background texture** recolored in royal midnight navy / deep slate-blue variance with white margin `JOKER` text.
  - Unique armored sentinel jester with steel knight-like helmet and sharp blade horns forming a spade silhouette, iron spade visor crest on forehead, unyielding stoic eyes, straight firm mouth, and rivet-studded steel gorget collar.
- **Files**: [`stoic_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stoic_joker.lua) | [`j_stoic_joker.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_stoic_joker.png)

#### 🔨 Stubborn Joker
- **Key**: `j_vmw_stubborn_joker`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Each {C:clubs}Club{} card held in hand gives {C:mult}+#1#{} Mult`
- **Mechanics**:
  - Triggers on `context.individual and context.cardarea == G.hand` when hand scores.
  - Grants +4 Mult for each Club card held in hand.
- **Art Concept**:
  - Fluid **marble swirl background texture** recolored in emerald jade / deep forest-green variance with white margin `JOKER` text.
  - Unique tough brawler jester with bandaged nose bridge (white cross tape), clenched toothpick/pipe stem with glowing cherry spark, furrowed bushy brows, studded green leather cap with heavy wooden club finials, and spiked studded collar.
- **Files**: [`stubborn_joker.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stubborn_joker.lua) | [`j_stubborn_joker.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_stubborn_joker.png)

#### 📐 Wrong Schematics
- **Key**: `j_vmw_wrong_schematics`
- **Rarity**: Uncommon | **Cost**: $7
- **Blueprint Compatible**: Yes
- **Effect**: `{C:green}#1# in #2#{} chance to copy ability of Joker to the {C:attention}right{}, or Joker to the {C:attention}left{}.`
- **Mechanics & Synergy**:
  - Normally (1 in 2): Rolls 50/50 between the Joker to its right and the Joker to its left, copying whichever is chosen.
  - With *Oops! All 6s* (2 in 2 or higher): Copies **both** the left Joker and the right Joker in left-to-right order, chaining their effects cleanly via `SMODS.merge_effects`.
- **Art Concept**: Blueprint cyan-blue grid (`#4B69CF`, `#7D93E2`), white drafting lines, crosshair target eyes, inverted question-mark smile, dimension arrows, and drafting `JOKER` font.
- **Files**: [`wrong_schematics.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/wrong_schematics.lua) | [`j_wrong_schematics.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_wrong_schematics.png)

#### ✨ Magifect
- **Key**: `j_vmw_magifect`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retriggers all {C:dark_edition}Editions{} ({C:dark_edition}Foil{}, {C:dark_edition}Holographic{}, {C:dark_edition}Polychrome{}) on all {C:attention}Jokers{}.`
- **Art Concept**: Dark cosmic slate base, split diagonal rainbow diffraction prisms (Foil cyan, Holo magenta, Poly rainbow), central 8-pointed sparkling star, and vertical `JOKER` lettering.
- **Files**: [`magifect.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/magifect.lua) | [`j_magifect.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_magifect.png)

#### 🎰 Jackpot
- **Key**: `j_vmw_jackpot`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `If played hand contains at least {C:attention}3{} scoring {C:attention}7s{}, each scored {C:attention}7{} gives {C:money}$6{}.`
- **Art Concept**: Vintage Vegas one-armed bandit slot machine in metallic teal (`#2A3C48`) with polished gold trim, arched neon dome, 3 spinning reels aligned on bold cherry-red **[ 7 ] [ 7 ] [ 7 ]**, side pull lever with red ball knob, overflowing coin hopper, floating sparkles, and vertical `JOKER` lettering.
- **Files**: [`jackpot.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/jackpot.lua) | [`j_jackpot.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_jackpot.png)

#### 🎭 MultiFaces
- **Key**: `j_vmw_multifaces`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Converts played {C:attention}2s{} into {C:attention}Jacks{}, {C:attention}3s{} into {C:attention}Queens{}, and {C:attention}4s{} into {C:attention}Kings{} when played.`
- **Art Concept**: Full-card canvas dual-split composition (Sock & Buskin style combined with cubist flowing multi-profile painting). Features an organic S-curve dividing warm ochre/ivory tones on the left from rich deep petrol teal on the right, interlocking cubist face profiles, almond eyes, sensual lips, flowing locks, and Sock & Buskin inverted typography (dark slate `JOKER` on top-left, crisp white inverted `JOKER` on bottom-right).
- **Files**: [`multifaces.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/multifaces.lua) | [`j_multifaces.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_multifaces.png)

#### 🕹️ Bonus Stage
- **Key**: `j_vmw_bonus_stage`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all played {C:attention}Bonus Cards{}.`
- **Art Concept**: Classic full-featured retro arcade cabinet: illuminated top marquee banner with red `BONUS` lettering, CRT monitor screen with scanlines and a glowing 8-bit golden star in the center, angled control deck with red ball-top joystick and three colored arcade push-buttons (cyan, gold, red), and lower dual steel coin door with glowing amber 25¢ slots, set directly on the authentic in-game **Bonus Card** chevron background.
- **Files**: [`bonus_stage.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/bonus_stage.lua) | [`j_bonus_stage.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_bonus_stage.png)

#### 🏎️ Overdrive
- **Key**: `j_vmw_overdrive`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all played {C:attention}Mult Cards{}.`
- **Art Concept**: High-performance hot-rod tachometer revved completely into the danger redline: heavy circular chrome bezel with corner mounting bolts and specular reflections, matte black gauge dial with white low-RPM ticks and a vibrant scarlet `OVERDRIVE` redline zone from 7,000 to 10,000+ RPM, pinned orange-red needle with sparks, top shift warning lamp, and twin chrome exhaust pipes at the base spitting backfire flames, set directly on the authentic in-game **Mult Card** fiery background.
- **Files**: [`overdrive.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/overdrive.lua) | [`j_overdrive.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_overdrive.png)

#### 🌈 Kaleidoscope
- **Key**: `j_vmw_kaleidoscope`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all played {C:attention}Wild Cards{}.`
- **Art Concept**: Polished brass optical cylinder featuring an intricate 4-suit stained-glass mosaic with central gem facets, set directly on the authentic in-game **Wild Card** 4-suit bleed background extracted from vanilla Balatro.
- **Files**: [`kaleidoscope.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/kaleidoscope.lua) | [`j_kaleidoscope.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_kaleidoscope.png)

#### 🔨 The Anvil
- **Key**: `j_vmw_the_anvil`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all played {C:attention}Steel Cards{}.`
- **Art Concept**: Heavy blacksmith cast-iron anvil resting on an oak stump with glowing red-hot steel struck by a forging hammer, set directly on the authentic in-game **Steel Card** brushed plate background extracted from vanilla Balatro.
- **Files**: [`the_anvil.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/the_anvil.lua) | [`j_the_anvil.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_the_anvil.png)

#### 🗿 Monolith
- **Key**: `j_vmw_monolith`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all played {C:attention}Stone Cards{}.`
- **Art Concept**: Ancient standing granite menhir slab carved with mystical glowing cyan Balatro runes, set directly on the authentic in-game **Stone Card** bedrock background extracted from vanilla Balatro.
- **Files**: [`monolith.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/monolith.lua) | [`j_monolith.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_monolith.png)

#### 🪙 Bullion
- **Key**: `j_vmw_bullion`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all played {C:attention}Gold Cards{}.`
- **Art Concept**: Tiered pyramid stack of polished 999.9 fine gold bullion bars with assay stamps, set directly on the authentic in-game **Gold Card** metallic golden sheen background extracted from vanilla Balatro.
- **Files**: [`bullion.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/bullion.lua) | [`j_bullion.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_bullion.png)

#### ✖️ Doubler
- **Key**: `j_vmw_doubler`
- **Rarity**: Rare | **Cost**: $8
- **Blueprint Compatible**: No (trigger on sell)
- **Effect**: `When {C:attention}sold{}, doubles all numerical values of a {C:attention}random Joker{}.`
- **Art Concept**: Casino gold felt texture, dark mahogany card border, giant glowing golden "×2" multiplier symbol with drop shadows and white bevels, flanked by playing card suits.
- **Files**: [`doubler.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/doubler.lua) | [`j_doubler.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_doubler.png)

#### 🔥 Burnt Offering
- **Key**: `j_vmw_burnt_offering`
- **Rarity**: Rare | **Cost**: $8
- **Blueprint Compatible**: Yes
- **Effect**: `Destroys {C:attention}1{} random card from the {C:attention}first hand{} of each round. Creates a random {C:tarot}Tarot{} card {C:inactive}(Must have room){}.`
- **Art Concept**: Stone altar base with charred ash heap, mystical purple flames licking upward, hovering miniature glowing Tarot card with gold trim, smoke curls, sparks, and vertical `JOKER` lettering.
- **Files**: [`burnt_offering.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/burnt_offering.lua) | [`j_burnt_offering.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_burnt_offering.png)

#### 🪞 Glassblower
- **Key**: `j_vmw_glassblower`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `Retrigger all played {C:attention}Glass Cards{}, {C:green}#1# in #2#{} chance to break when retriggering.`
- **Mechanics**: Retriggers each played Glass Card, with an authentic 1 in 25 chance to shatter upon retriggering (scales with *Oops! All 6s*).
- **Art Concept**: Artisan iron blowpipe holding a fragile molten crystal glass sphere with delicate white fracture facets, set directly on the authentic in-game **Glass Card** crystalline background extracted from vanilla Balatro.
- **Files**: [`glassblower.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/glassblower.lua) | [`j_glassblower.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_glassblower.png)

#### 🧲 Golden Horseshoe
- **Key**: `j_vmw_golden_horseshoe`
- **Rarity**: Uncommon | **Cost**: $6
- **Blueprint Compatible**: Yes
- **Effect**: `{C:green}#1# in #2#{} chance to retrigger each played {C:attention}Lucky Card{}.`
- **Mechanics**: Has a 1 in 3 chance to retrigger each played Lucky Card (scales with *Oops! All 6s*).
- **Art Concept**: 100% solid, unbroken continuous 24k gold horseshoe seamlessly uniting the upper heels with the bottom curve in rich yellow and gold highlights, with 7 square nail holes, emerald ribbon bow, and golden lucky stars, set directly on the authentic in-game **Lucky Card** aged parchment background extracted from vanilla Balatro.
- **Files**: [`golden_horseshoe.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/golden_horseshoe.lua) | [`j_golden_horseshoe.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_golden_horseshoe.png)

#### 🌾 The Scythe
- **Key**: `j_vmw_the_scythe`
- **Rarity**: Rare | **Cost**: $8
- **Blueprint Compatible**: Yes
- **Effect**: `If {C:attention}first hand{} of round has exactly {C:attention}3{} cards, destroys the {C:attention}2 side cards{} and creates a permanent copy of the {C:attention}middle card{}.`
- **Art Concept**: Curved Grim Reaper harvesting scythe blade with polished steel edge cutting across the canvas, surrounded by midnight indigo spectral mist. At the bottom, two side cards are severed in half while the middle card glows with duplicate golden aura, framed by vertical `JOKER` lettering.
- **Files**: [`the_scythe.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/the_scythe.lua) | [`j_the_scythe.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_the_scythe.png)

#### 🛡️ Antivirus
- **Key**: `j_vmw_antivirus`
- **Rarity**: Common | **Cost**: $4
- **Blueprint Compatible**: Yes
- **Effect**: `{C:chips}+#1#{} Chips for each {C:attention}unique card{} in your {C:attention}full deck{}. {C:inactive}(Currently {C:chips}+#2#{C:inactive} Chips)`
- **Mechanics & Uniqueness Criteria**:
  - Traverses `G.playing_cards` (the player's entire deck) to evaluate distinct playing card signatures.
  - A card is uniquely identified by the combination of its **Rank**, **Suit**, **Enhancement**, **Edition**, and **Seal** (Stone cards are evaluated by enhancement, edition, and seal).
  - Cards sharing the exact same properties (e.g. 2 identical Glass Kings of Hearts) only count once; applying a seal, edition, or different enhancement creates another unique card.
  - Dynamically updates its tooltip and awards `+2 Chips` per unique card on every played hand during scoring. (A fresh 52-card standard deck awards `+104 Chips`).
- **Art Concept**: Beveled titanium cybersecurity shield with a cyber-green CRT scanline display, sweeping radar beam, and a quarantined red pixel virus bug locked inside targeting reticles and a containment barrier. Crowned with a two-tone jester cap with brass bells, clean checkmark badge, and authentic vertical `JOKER` typography.
- **Files**: [`antivirus.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/antivirus.lua) | [`j_antivirus.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_antivirus.png)

#### 🏞️ River
- **Key**: `j_vmw_river`
- **Rarity**: Rare | **Cost**: $8
- **Blueprint Compatible**: Yes
- **Effect**: `Adds the {C:chips}Chips{} and {C:mult}Mult{} of the poker hand held in {C:attention}hand{} to scoring. {C:inactive}(Currently {C:attention}#1#{}{C:inactive}: {C:chips}+#2#{} {C:inactive}Chips, {C:mult}+#3#{} {C:inactive}Mult){}`
- **Mechanics**:
  - Triggers during `context.joker_main` (when jokers calculate on hand score).
  - Evaluates the cards remaining in `G.hand.cards` via `G.FUNCS.get_poker_hand_info(G.hand.cards)`.
  - Determines the highest valid poker hand held in hand (e.g. Flush, Straight, Two Pair, Full House, High Card) and fetches its current Chips and Mult values from `G.GAME.hands[text]`.
  - Automatically scales with **Planet Card** hand upgrades (e.g. if Flush is Level 3, it awards Level 3 Flush Chips and Mult).
  - Displays the detected hand name popup directly on the Joker (`Flush!`, `Full House!`), then adds both the Chips and Mult to the scoring tally.
  - Dynamically updates its tooltip during play to reflect the hand currently held in hand.
  - Fully compatible with **Blueprint** and **Brainstorm** to re-evaluate and re-add the held hand's score.
- **Art Concept**:
  - Full-surface scenic card illustration directly inspired by the user's landscape drawing, rendered in vibrant Balatro color palette.
  - 1-pixel crisp white card inner frame running along the perimeter of the card, cleanly framing the landscape.
  - Background: Grand mountain range featuring a towering horn-shaped central peak and flanking craggy peaks with snow crests and diagonal shadow hatching, under a sunny sky with a flock of soaring birds and a golden radiating sunburst with ray ticks and dots in the upper right.
  - Midground: Rolling lush green valley hills dotted with evergreen pine clusters and sketch contour ticks, framing a winding silver-blue river that carves through the pass.
  - Foreground: The river flows continuously through the lush valley meadows, gently curving back and forth, widening all the way down until it cleanly reaches the bottom border of the card (no waterfall cutoff).
  - Authentic vertical `JOKER` lettering framed along the left and right card margins with white edge contrast.
  - Framed within authentic Balatro rounded card boundaries with transparent corners.
- **Files**: [`river.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/river.lua) | [`j_river.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_river.png)

#### 👑 Stańczyk
- **Key**: `j_vmw_stanczyk`
- **Rarity**: Legendary | **Cost**: $20
- **Blueprint Compatible**: No
- **Effect**: `When {C:attention}Boss Blind{} is defeated, creates a {C:dark_edition}Negative{}, {C:attention}Eternal{}, and {C:attention}Rental{} copy of a random other owned {C:attention}Joker{} {C:inactive}(Stańczyk excluded){}.`
- **Balance & Mechanics**: Clones gain **Negative** (+1 Joker slot, no board clutter), **Eternal** (permanent, cannot be sold or sacrificed), and **Rental** ($3 per round fee). This creates immense long-term power while demanding constant economic management to afford the rental upkeep of each clone.
  > 📝 **Design Note / Alternative Option**: If the Rental tax is ever deemed too punitive or economic, Stańczyk can alternatively be changed to **Negative + Perishable** (clones expire after 5 rounds, giving an ante-and-a-half power burst without permanent bloat).
- **Art Concept**: Full authentic 2-layer Legendary format (71×190 / 142×380). Base layer features black & grey wavy marbled swirl texture with engraved gold plaque "STAŃCZYK". Floating soul layer displays the melancholic historical court jester in crimson robes and jester hood.
- **Files**: [`stanczyk.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/stanczyk.lua) | [`j_stanczyk.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_stanczyk.png)

#### 👑 Sommers
- **Key**: `j_vmw_sommers`
- **Rarity**: Legendary | **Cost**: $20
- **Blueprint Compatible**: Yes
- **Effect**: `Gains {C:chips}+#1#{} Chips when a card with a {C:blue}Blue Seal{} is discarded, gains {X:mult,C:white}X#2#{} Mult when a card with a {C:red}Red Seal{} is discarded. {C:inactive}(Currently {C:chips}+#3#{C:inactive} Chips and {X:mult,C:white}X#4#{C:inactive} Mult){}`
- **Mechanics**:
  - Scales permanently during the round whenever playing cards with seals are discarded.
  - Discarding a **Blue Seal** card grants **+20 Chips**.
  - Discarding a **Red Seal** card grants **X0.25 Mult**.
  - Discarding a **Red Seal** card grants **+X0.25 Mult**.
  - During scoring (`joker_main`), contributes its accumulated Chips and XMult to the played hand.
  - Fully Blueprint compatible during scoring (copies the accumulated Chips and XMult).
- **Art Concept**: Full authentic 2-layer Legendary format (71×190 / 142×380). Base layer features an authentic Localthunk wavy marbled swirl background mapped to electric **Cyan** with an engraved bottom plaque reading `SOMMERS`. Floating 3D soul layer displays the iconic Renaissance Tudor court jester Will Sommers with a two-tone cyan/navy cowl and golden bells, flanked by a glowing ethereal Blue Seal on his left and a glowing Red Seal on his right.
- **Files**: [`sommers.lua`](file:///D:/GG/VanillaModedWorld/items/jokers/sommers.lua) | [`j_sommers.png`](file:///D:/GG/VanillaModedWorld/assets/1x/j_sommers.png)

</details>

---

### Planned Jokers (Backlog)

*(Paste new planned Jokers here using the Joker template above)*

---

## 🔮 Tarots

### Implemented Tarots

| Tarot | Target | Effect Summary | File |
| :--- | :--- | :--- | :--- |
| **The Mirror** | 2 selected cards | Converts the **left** card into the **rank** and **suit** of the **right** card *(Drag to rearrange)* | [`the_mirror.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/the_mirror.lua) |
| **Weakness** | Up to 2 selected cards | **Decreases rank** of up to **2** selected cards by 1 (2 wraps to Ace) | [`weakness.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/weakness.lua) |
| **Swaper** | 2 selected cards | **Swaps all Enhancements, Editions, and Seals** between **2** selected cards | [`swaper.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/swaper.lua) |

<details open>
<summary><b>🔍 Detailed Tarot Profiles</b> (Click to collapse/expand)</summary>

#### 🪞 The Mirror (XVI - Mirror)
- **Key**: `c_vmw_the_mirror`
- **Effect**: `Select {C:attention}2{} cards, convert the {C:attention}left{} card into the {C:attention}rank{} and {C:attention}suit{} of the {C:attention}right{} card. {C:inactive}(Drag to rearrange){}`
- **Mechanics**:
  - Requires selecting exactly 2 cards in hand (`can_use = #G.hand.highlighted == 2`).
  - Converts the **left** card into the **rank and suit** of the **right** card using `set_base(rightmost.config.card)`.
  - **Preserves modifications on target card**: Any Enhancements (Glass, Steel, Stone, Gold, Lucky, etc.), Editions (Foil, Holo, Polychrome), and Seals on the left card are 100% preserved.
  - Does not copy enhancements, editions, or seals from the right card, serving as the pure rank & suit counterpart to **Death** (full copy) and **Swaper** (enhancement/edition/seal swap).
- **Art Concept**: 100% authentic Balatro Tarot woodcut style adhering strictly to the official 5-color palette (`#4F6367` Slate, `#A58547` Amber, `#DAB772` Gold, `#FFE5B4` Cream, `#FFFFFF` White). Features:
  - Authentic Balatro Tarot woodcut border and top Roman numeral cartouche plaque (**`XVI`**).
  - Detailed celestial radiating woodcut sunburst with alternating diagonal cross-hatching and cream beam bands across the sky.
  - Floating 4-point celestial diamond stars and stippled parchment depth.
  - Baroque ornate oval hand mirror with acanthus leaf crown crest, side curl flourishes, and fluted column handle.
  - Reflective beveled glass with twin playing card silhouettes and glowing diamond seal enhancement matrix.
  - Seamless authentic Balatro bottom banner with centered woodcut serif typography **`MIRROR`**.
- **Files**: [`the_mirror.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/the_mirror.lua) | [`c_the_mirror.png`](file:///D:/GG/VanillaModedWorld/assets/2x/c_the_mirror.png)

#### 🥀 Weakness (XI - Weakness)
- **Key**: `c_vmw_weakness`
- **Effect**: `Decreases the rank of up to {C:attention}2{} selected cards by {C:attention}1{}. {C:inactive}(2 wraps around to Ace){}.`
- **Art Concept**: 100% authentic Balatro Tarot woodcut style adhering strictly to the official 5-color palette (`#4F6367` Slate, `#A58547` Amber, `#DAB772` Gold, `#FFE5B4` Cream, `#FFFFFF` White). Features:
  - Authentic Balatro Tarot woodcut border and top Roman numeral cartouche plaque (**`XI`**, direct counterpart to *Strength* XI).
  - Detailed celestial shockwave rays and fine diagonal woodcut cross-hatching filling the background sky.
  - Weathered heraldic knight's heater shield with beveled golden rim and woodcut steel cross-hatching.
  - Ceremonial sword driven vertically through center with a violent, dramatic jagged fracture splitting blade and shield.
  - Snapped lower blade section deflected and angled with flying sharp steel shards and white glints.
  - Withered thorny briar vines and drooping wild rosebuds in woodcut cross-hatching.
  - Weeping sorrow power droplets draining downwards.
  - Seamless authentic Balatro bottom banner with centered woodcut serif typography **`WEAKNESS`**.
- **Files**: [`weakness.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/weakness.lua) | [`c_weakness.png`](file:///D:/GG/VanillaModedWorld/assets/2x/c_weakness.png)

#### 🔄 Swaper (XVI - Swapper)
- **Key**: `c_vmw_swaper`
- **Cost**: $3
- **Effect**: `Select {C:attention}2{} cards, {C:attention}swap{} all {C:attention}Enhancements{}, {C:dark_edition}Editions{}, and {C:attention}Seals{} between them.`
- **Mechanics**:
  - Requires exactly 2 selected cards in hand, where at least one card has an Enhancement, Edition, or Seal.
  - Flips both cards face down, cleanly swaps:
    1. **Enhancements**: Transfers enhancement centers (e.g. Glass, Steel, Stone, Gold, Lucky, Bonus, Mult, Wild) or reverts to plain base card if one card was unenhanced.
    2. **Editions**: Exchanges editions (Foil, Holographic, Polychrome, etc.) or removes/applies edition if one was un-editioned.
    3. **Seals**: Exchanges seals (Red, Blue, Gold, Purple, etc.) or moves seal to the un-sealed card.
  - Flips cards face up with authentic `tarot2` sound and card juice.
  - Prevents accidental usage if neither selected card has an Enhancement, Edition, or Seal.
- **Art Concept**: 100% authentic Balatro Tarot woodcut style adhering strictly to the official 5-color palette (`#4F6367` Slate, `#A58547` Amber, `#DAB772` Gold, `#FFE5B4` Cream, `#FFFFFF` White). Features:
  - Authentic Balatro Tarot woodcut frame and Roman numeral plaque (**`XVI`**).
  - Celestial radiating sunburst aura and fine diagonal woodcut hatching across the cream parchment canvas.
  - Two miniature playing card silhouettes in the background being swapped in pure Tarot woodcut style (ornate gold borders with celestial diamond & star woodcut pips; red/blue seals removed for 100% palette purity).
  - Prominent circular golden swap arrows with sharp arrowheads in dynamic clockwise rotation forming an exchange ring.
  - Swirling gold/white particle essence sparkles along the exchange arcs.
  - Central mystical exchange star glint and celestial corner tarot sparkles.
  - Authentic Balatro bottom banner with centered woodcut serif typography **`SWAPPER`**.
- **Files**: [`swaper.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/swaper.lua) | [`c_swaper.png`](file:///D:/GG/VanillaModedWorld/assets/2x/c_swaper.png)

</details>

---

### Planned Tarots (Backlog)

> 📖 **Full 78 Tarot Cards Meanings & Archetypes Reference**: See [`references/tarot_card_meanings_reference.md`](file:///D:/GG/VanillaModedWorld/references/tarot_card_meanings_reference.md) for the complete list of Major Arcana (0-XXI) and Minor Arcana (Wands, Cups, Swords, Pentacles) from Labyrinthos Academy.

*(Paste new planned Tarots here using the Consumable template)*

---

## 👻 Spectrals

### Implemented Spectrals

| Spectral | Cost | Target | Effect | Art Concept | File |
|---|---|---|---|---|---|
| **🔮 Phantasm** | $4 | Cards in hand | Removes all **debuffs** from cards currently held in **hand** *(Appears in shops; does not appear in booster packs)* | Hooded spectral phantom conjuring glowing golden seal matrices onto two floating playing cards, authentic spectral palette with pristine void background | [phantasm.lua](file:///D:/GG/VanillaModedWorld/items/consumables/phantasm.lua) |
| **📜 Pact** | $4 | 1 Random Joker | Add **Eternal** to a random **Joker**, gain **$25** | Golden Ouroboros infinity loop ($\infty$) snake eating its tail with fangs and blue eye, celestial radiant burst, gold coins at base, 100% clean spectral void background | [pact.lua](file:///D:/GG/VanillaModedWorld/items/consumables/pact.lua) |

#### 🔮 Phantasm
- **Key**: `c_vmw_phantasm`
- **Cost**: `$4`
- **Set**: `Spectral`
- **Description**: `"Removes all {C:red}debuffs{} from cards currently held in {C:attention}hand{}"`
- **Mechanics**:
  - Usable during rounds whenever cards are held in hand (`can_use = G.hand and #G.hand.cards > 0`).
  - Flips all cards currently in hand face down with authentic spectral sound and juice.
  - Clears debuffs from all cards in hand (`hand_card:set_debuff(false)`, `hand_card.debuff = false`, `hand_card.debuffed_by_blind = false`).
  - Sets `hand_card.ability.debuff_sources['phantasm'] = 'prevent_debuff'` on each card in hand so the current Boss Blind cannot re-debuff them for the remainder of the round.
  - Flips all hand cards back face up with `tarot2` audio and juice animations.
  - **Spawn Rules**: Unlike normal Spectral cards, Phantasm **appears in shops** (in consumable shop slots across all decks, and in Ghost Deck spectral slots) and **never appears in booster packs** (Spectral packs, Arcana packs with Omen Globe, etc.) where removing hand debuffs would be non-functional.
- **Visual Design**:
  - **Frame & Template**: Authentic vanilla Balatro spectral card frame with pristine void background and zero bleed-through from template cards.
  - **Nameplate**: Vanilla parchment white ribbon banner (`y=82..88`) with dark slate (`#4F6367`) 6px capital pixel font (`PHANTASM`).
  - **Background**: Deep dark navy spectral void (`#4E5779`) with subtle mid-navy celestial dither (`#5E7297`).
  - **Central Motif**: Floating hooded ethereal phantom spirit (`#E2EBF9`, `#FFFFFF`) with luminous spectral eyes (`#7AA4F2`) and outstretched hands channeling celestial energy tendrils into **two hovering playing cards** branded with glowing golden seal matrices (`#C7B24A`, `#A79C67`), surrounded by floating seal embers and runes.
- **Asset**: `c_phantasm.png` (1x: 71×95 px, 2x: 142×190 px)

#### 📜 Pact
- **Key**: `c_vmw_pact`
- **Cost**: `$4`
- **Set**: `Spectral`
- **Description**: `"Add {C:attention}Eternal{} to a random {C:attention}Joker{}, gain {C:money}$#1#{}"`
- **Mechanics**:
  - Checks that at least one Joker is eligible: `eternal_compat ~= false` and `not ability.eternal`.
  - Removes `perishable` if present so `eternal` can apply cleanly.
  - Applies `set_eternal(true)`, gives `$25` via `ease_dollars(25)`, and triggers gold seal sound effects (`gold_seal`) and juice animations.
  - Displays `{ key = 'eternal', set = 'Other' }` in `info_queue` tooltip preview.
- **Visual Design**:
  - **Frame & Template**: Authentic vanilla Balatro spectral card frame with 100% procedurally cleaned interior (zero yellow ring or blue aura bleed-through from Ankh).
  - **Nameplate**: Vanilla parchment white ribbon banner (`y=82..88`) with dark slate (`#4F6367`) 6px capital pixel font (`PACT`).
  - **Background**: Pristine deep dark navy spectral void (`#4E5779`) with subtle radial celestial dither (`#5E7297`).
  - **Central Motif**: The Golden Ouroboros Infinity Snake ($\infty$) devouring its tail, featuring segmented golden scales, brass shadows, pale ectoplasmic belly, sharp white fangs, and a glowing spectral blue eye, backed by celestial radiant sunburst rays, with a pyramid pile of gold coins ($25) at the base.
- **Asset**: `c_pact.png` (1x: 71×95 px, 2x: 142×190 px)


### Planned Spectrals (Backlog)

*(Paste new planned Spectrals here using the Consumable template)*

---

## 🖐️ Poker Hands

### Implemented Poker Hands

| Hand | Required Cards | Base Chips | Base Mult | Level Up (+Chips / +Mult) | Status | Associated Planet | File |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Quarry** | **5 Stone Cards** | **200** | **20** | +40 / +4 | Secret (`visible = false`) | **Nibiru** | [`quarry.lua`](file:///D:/GG/VanillaModedWorld/items/hands/quarry.lua) |

#### Detailed Mechanics:

- **Quarry**
  - **Requirement**: Played hand must contain at least **5 Stone Cards**.
  - **Base Stats**: **200 Chips, 20 Mult** (Base product: 4,000 — ranks above Flush Five in hand hierarchy).
  - **Level Up**: **+40 Chips, +4 Mult** per level.
  - **Discovery**: Secret hand (`visible = false`). Appears in the Run Info / poker hand list once played for the first time in a run.
  - **Associated Planet**: **Nibiru**.
  - **Mechanics**: Checks played cards for Stone card enhancement (`m_stone`). Since Stone cards possess neither rank nor suit, standard hands cannot form from pure Stone cards; Quarry serves as the ultimate payoff hand for heavy stone deck manipulation. All scoring Stone cards in the hand score their innate chip bonus (+50 chips each) on top of the base hand values.
  - **File**: [`items/hands/quarry.lua`](file:///D:/GG/VanillaModedWorld/items/hands/quarry.lua)

---

## 🪐 Planets

### Implemented Planets

| Planet | Cost | Poker Hand Upgraded | Stat Bonus / Level | Availability | File |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **Nibiru** | $3 | **Quarry** | **+40 Chips, +4 Mult** | Softlocked (Appears after Quarry is played) | [`nibiru.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/nibiru.lua) |

#### Detailed Mechanics:

- **Nibiru**
  - **Type**: Planet Consumable
  - **Cost**: $3
  - **Effect**: Increases the level of **Quarry** by 1 (**+40 Chips, +4 Mult**).
  - **Pool Availability**: `softlock = true`. Adheres strictly to vanilla secret hand planet rules: it cannot spawn in shops or celestial packs until Quarry has been played at least once during the current run.
  - **Art Concept**: Uses the authentic volcanic lava sphere texture with glowing molten magma fissures directly from the concept art. The planet size is balanced at 28 px diameter (comfortably between Pluto at 22 px and Mars at 38 px) and centered at exact vanilla coordinates `(CX=35.0, CY=52.0)`. The name **NIBIRU** is rendered using official vanilla Balatro pixel typography (decoded from Neptune and Jupiter letterforms: 6px `N`, 4px serif `I`, 4px `B`, 4px `R`, and 4px `U`). The namebox pill and bottom handbox have zero stray artifacts or dark ears, matching the center space teal (`#5B9BAA`). The left (`x=6, 7`) and right (`x=63, 64`) card borders are continuous 2px solid white (`#DFF5FC`) matching official Balatro cards. In the bottom panel, the 5 mini cards are rendered as gray Stone Cards (`m_stone`), each featuring an individual jagged fracture crack.
  - **File**: [`items/consumables/nibiru.lua`](file:///D:/GG/VanillaModedWorld/items/consumables/nibiru.lua)

### Planned Planets (Backlog)

*(Paste new planned Planets here using the Consumable template)*

---

## 🎟️ Vouchers

### Implemented Vouchers

| Voucher | Tier | Cost | Requires | Effect Summary | File |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Market** | `Tier 1` | $10 | — | **+1 Booster Pack slot** available in shop | [`market.lua`](file:///D:/GG/VanillaModedWorld/items/vouchers/market.lua) |
| **Supermarket** | `Tier 2` | $10 | Market | **+1 Voucher slot** available in shop | [`supermarket.lua`](file:///D:/GG/VanillaModedWorld/items/vouchers/supermarket.lua) |

<details open>
<summary><b>🔍 Detailed Voucher Profiles</b> (Click to collapse/expand)</summary>

#### 🛒 Market (Tier 1)
- **Key**: `v_vmw_market`
- **Cost**: $10
- **Effect**: `{C:attention}+#1#{} Booster Pack slot available in shop.`
- **Redeem Mechanism**: Calls `SMODS.change_booster_limit(1)`, immediately expanding shop booster capacity and spawning an extra pack if redeemed during shopping.
- **Art Concept**: Vintage market ticket with authentic top and bottom semicircular ticket punch holes, striped crimson & ivory market stall canopy awning, rustic wicker woven market basket packed with Balatro booster packs (Arcana eye, Celestial moon, Standard card pack), golden wax seal stamp, and bottom banner.
- **Files**: [`market.lua`](file:///D:/GG/VanillaModedWorld/items/vouchers/market.lua) | [`v_market.png`](file:///D:/GG/VanillaModedWorld/assets/1x/v_market.png)

#### 🏬 Supermarket (Tier 2)
- **Key**: `v_vmw_supermarket`
- **Cost**: $10
- **Requires**: `v_vmw_market` *(Market)*
- **Effect**: `{C:attention}+#1#{} Voucher slot available in shop.`
- **Redeem Mechanism**: Calls `SMODS.change_voucher_limit(1)`, immediately expanding shop voucher capacity and spawning an extra voucher if redeemed during shopping.
- **Art Concept**: Luxurious midnight indigo ticket with authentic top and bottom semicircular ticket punch holes, beveled 24k gold border, neon cyan and magenta department store marquee sign, polished chrome wire shopping cart overflowing with golden tickets and VIP passes, twin golden laurel branches, and star security insignia.
- **Files**: [`supermarket.lua`](file:///D:/GG/VanillaModedWorld/items/vouchers/supermarket.lua) | [`v_supermarket.png`](file:///D:/GG/VanillaModedWorld/assets/1x/v_supermarket.png)

</details>

---

### Planned Vouchers (Backlog)

*(Paste new planned Vouchers here)*

---

## 🎴 Decks

### Implemented Decks

| Deck | Effect Summary | File |
| :--- | :--- | :--- |
| **Echo Deck** | Retriggers all **Jokers 1 additional time** (2 triggers total), Required Blind chips scale by **X Ante base blind size** (Ante 1 = 1x, Ante 2 = 2x, ..., Ante 8 = 8x) | [`echo_deck.lua`](file:///D:/GG/VanillaModedWorld/items/decks/echo_deck.lua) |

<details open>
<summary><b>🔍 Detailed Deck Profiles</b> (Click to collapse/expand)</summary>

#### 🔊 Echo Deck
- **Key**: `b_vmw_echo_deck`
- **Effect**:
  - Retriggers all **Jokers** `{C:attention}1{} additional time`.
  - Required Blind chips scale by `{C:attention}X Ante{} base size` *(e.g. Ante 1 = 1x, Ante 2 = 2x, Ante 8 = 8x)*.
  - Standard 5 Joker slots *(no slot penalty)* and normal reroll costs *(no shop reroll penalty)*.
- **Art Concept**: Deep midnight slate base (`#182630`), concentric electric cyan (`#13AFCE`) and warm gold (`#F3B958`) acoustic soundwave ripple rings radiating from a central sonic diamond pulse.
- **Files**: [`echo_deck.lua`](file:///D:/GG/VanillaModedWorld/items/decks/echo_deck.lua) | [`b_echo.png`](file:///D:/GG/VanillaModedWorld/assets/1x/b_echo.png)

</details>

---

### Planned Decks (Backlog)

*(Paste new planned Decks here using the Deck template)*

---

## 🎴 Sleeves (CardSleeves Mod)

### Implemented Sleeves

| Sleeve | Normal Effect (With other decks) | Alt / Combo Effect (With matching deck) | File |
| :--- | :--- | :--- | :--- |
| **Echo Sleeve** | Retriggers all Jokers **1 additional time**, Blinds scale by **X Ante base size** | Retriggers every **played card 1 additional time**, **-1 hand size** | [`echo_sleeve.lua`](file:///D:/GG/VanillaModedWorld/items/sleeves/echo_sleeve.lua) |

<details open>
<summary><b>🔍 Detailed Sleeve Profiles</b> (Click to collapse/expand)</summary>

#### 🔊 Echo Sleeve
- **Key**: `sleeve_vmw_echo`
- **Mod Compatibility**: CardSleeves (automatically loads if CardSleeves is installed, gracefully skips if not).
- **Effects**:
  - **Standard (Any other deck)**: Retriggers all Jokers `{C:attention}1{} additional time`, Required Blind chips scale by `{C:attention}X Ante{} base size`.
  - **Alt Combo (Paired with Echo Deck)**: Retriggers every **played card** `{C:attention}1{} additional time` *(cards score twice!)*, but `{C:red}-1{} hand size`. Blind requirements scale by `{C:attention}X Ante{} base size` (from Echo Deck).
- **Art Concept**: Official CardSleeves 73×95 format with transparent downward notch at top, bordered plastic seams, and the Echo Deck's signature cyan and gold acoustic ripple motif.
- **Files**: [`echo_sleeve.lua`](file:///D:/GG/VanillaModedWorld/items/sleeves/echo_sleeve.lua) | [`sleeve_echo.png`](file:///D:/GG/VanillaModedWorld/assets/1x/sleeve_echo.png)

</details>

---

### Planned Sleeves (Backlog)

*(Paste new planned Sleeves here using the Sleeve template)*

---

## ✨ Seals, Enhancements & Editions

### Implemented
*None yet.*

### Planned (Backlog)

*(Paste new planned Seals, Card Enhancements, or Editions here)*

---

## 🛠️ Mod Information & Technical Summary
- **Mod Name:** Vanilla Moded World
- **Mod ID:** `VanillaModedWorld`
- **Prefix:** `vmw`
- **Target Frameworks:** Steamodded, Lovely, CardSleeves
- **Primary Workspace:** `D:\GG\VanillaModedWorld\`
- **Balatro Active Mods Symlink:** `%APPDATA%\Balatro\Mods\VanillaModedWorld\`
- **Asset Pipeline:** [`tools/sprite_builder.py`](file:///D:/GG/VanillaModedWorld/tools/sprite_builder.py) (strict 71×95 1x and 142×190 2x nearest-neighbor pixel enforcement)
