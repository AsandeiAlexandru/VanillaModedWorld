# 🃏 Vanilla Moded World

<p align="center">
  <img src="icon.png" width="96" height="96" alt="Vanilla Moded World Icon" />
</p>

<p align="center">
  <b>A seamless, high-polish vanilla-style expansion for Balatro.</b><br>
  Adding 40+ lore-friendly Jokers, custom Tarots, Spectrals, Secret Poker Hands, Planets, Vouchers, Decks, and Sleeves — all built with authentic Localthunk pixel art aesthetics and balanced mechanics.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Balatro-v1.0.1o-blue.svg?style=flat-square" alt="Balatro Version" />
  <img src="https://img.shields.io/badge/Steamodded-%3E%3D26.829.0-orange.svg?style=flat-square" alt="Steamodded" />
  <img src="https://img.shields.io/badge/Lovely-Compatible-green.svg?style=flat-square" alt="Lovely" />
  <img src="https://img.shields.io/badge/Version-0.1.0-purple.svg?style=flat-square" alt="Mod Version" />
</p>

---

## 📑 Table of Contents

- [📦 Requirements & Dependencies](#-requirements--dependencies)
- [📥 Installation Guide](#-installation-guide)
- [🃏 Implemented Content](#-implemented-content)
  - [🃏 Jokers (40)](#-jokers)
  - [🔮 Tarot Cards (3)](#-tarot-cards)
  - [👻 Spectral Cards (2)](#-spectral-cards)
  - [🖐️ Poker Hands & 🪐 Planets](#️-poker-hands--planets)
  - [🎟️ Vouchers (2)](#️-vouchers)
  - [🎴 Decks & Sleeves](#-decks--sleeves)
- [🤝 Compatibility](#-compatibility)
- [🛠️ Contributing & Roadmap](#️-contributing--roadmap)

---

## 📦 Requirements & Dependencies

**Vanilla Moded World** requires **Steamodded** and the **Lovely Injector** to run.

| Dependency | Required Version | Description & Links |
| :--- | :--- | :--- |
| **Lovely Injector** | `v0.5.0+` | Mod-loader injection hook for Balatro.<br>🔗 [GitHub Repository](https://github.com/ethangreen-dev/lovely-injector) \| [Latest Releases](https://github.com/ethangreen-dev/lovely-injector/releases) |
| **Steamodded (SMODS)** | `v1.0.0+` (or `26.829.0+`) | Core Lua modding framework for Balatro.<br>🔗 [GitHub Repository](https://github.com/SteamopolliS/Steamodded) \| [Releases](https://github.com/SteamopolliS/Steamodded/releases) |

---

## 📥 Installation Guide

### Step 1: Install Lovely
1. Head to the [Lovely Releases page](https://github.com/ethangreen-dev/lovely-injector/releases) and download the appropriate release:
   - **Windows**: Download `version.dll`
   - **macOS**: Download `libversion.dylib`
   - **Linux / Steam Deck**: Download `version.dll` or `libversion.so`
2. Open your Balatro game installation directory:
   - *Steam*: Right-click **Balatro** in your Steam library $\to$ **Manage** $\to$ **Browse local files**.
3. Place `version.dll` into the game directory right next to `Balatro.exe`.

### Step 2: Install Steamodded
1. Download the latest release `.zip` from [Steamodded GitHub Releases](https://github.com/SteamopolliS/Steamodded/releases).
2. Open your Balatro application data directory:
   - **Windows**: Press `Win + R`, paste `%AppData%\Balatro\Mods`, and press Enter. (Create the `Mods` folder if it doesn't exist).
   - **macOS**: `~/Library/Application Support/Balatro/Mods`
   - **Linux**: `~/.local/share/Balatro/Mods`
3. Extract Steamodded so it sits inside:
   `%AppData%\Balatro\Mods\Steamodded\`

### Step 3: Install Vanilla Moded World
1. Clone or download this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/VanillaModedWorld.git
   ```
   *(or download the `.zip` archive from GitHub and extract it).*
2. Place the `VanillaModedWorld` folder directly into your Balatro `Mods` folder:
   - **Windows**: `%AppData%\Balatro\Mods\VanillaModedWorld\`
   - **macOS**: `~/Library/Application Support/Balatro/Mods/VanillaModedWorld/`
   - **Linux**: `~/.local/share/Balatro/Mods/VanillaModedWorld/`
3. Launch Balatro! You should see **Vanilla Moded World** listed in the **Mods** menu in-game.

---

## 🃏 Implemented Content

### 🃏 Jokers

<details open>
<summary><b>Click to show/hide the Joker Gallery (40 Jokers)</b></summary>

| Sprite | Name | Rarity | Cost | Effect Summary |
| :---: | :--- | :---: | :---: | :--- |
| <img src="assets/2x/j_espresso.png" width="60" alt="Espresso" /> | **Espresso** | `Common` | $4 | **X2 Mult** on first hand of round. **1 in 20 chance** to transform into **Double Espresso**. |
| <img src="assets/2x/j_double_espresso.png" width="60" alt="Double Espresso" /> | **Double Espresso** | `Common` | $4 | Each played **2** gives **X2 Mult** when scored. *(Obtainable only when Espresso evolves!)* |
| <img src="assets/2x/j_lucky_clover.png" width="60" alt="Lucky Clover" /> | **Lucky Clover** | `Common` | $4 | Scored **Lucky 4 of Clubs** are guaranteed to trigger all Lucky effects (**+20 Mult** and **$20**). |
| <img src="assets/2x/j_hot_pepper.png" width="60" alt="Hot Pepper" /> | **Hot Pepper** | `Common` | $4 | Each played card gives **X1.2 Mult** when scored. **Self-destructs** when Boss Blind is defeated. |
| <img src="assets/2x/j_stone_tablet.png" width="60" alt="Stone Tablet" /> | **Stone Tablet** | `Common` | $4 | Retriggers all **Seals** on **Stone Cards** *(doubles their triggers and bonuses)*. |
| <img src="assets/2x/j_overkill.png" width="60" alt="Overkill" /> | **Overkill** | `Common` | $4 | Creates a **Spectral** card when Boss Blind is defeated if any single hand scored $\ge$ **2X** the Blind. |
| <img src="assets/2x/j_spotlight.png" width="60" alt="Spotlight" /> | **Spotlight** | `Common` | $4 | If played hand is a **5-card High Card**, **randomizes** the scoring card's Enhancement, Edition, and Seal. |
| <img src="assets/2x/j_short_circuit.png" width="60" alt="Short Circuit" /> | **Short Circuit** | `Common` | $4 | If a scored card is **retriggered**, has a **1 in 2 chance** to retrigger its **neighbors** as well. |
| <img src="assets/2x/j_sticky_note.png" width="60" alt="Sticky Note" /> | **Sticky Note** | `Common` | $4 | Retriggers the **first card** held in hand **2 additional times**. |
| <img src="assets/2x/j_camera.png" width="60" alt="Camera" /> | **Camera** | `Common` | $5 | First **numbered card** (2-10) held in hand gives **X2 Mult**. |
| <img src="assets/2x/j_antivirus.png" width="60" alt="Antivirus" /> | **Antivirus** | `Common` | $4 | **+2 Chips** for each **unique card** in your full deck *(starts at +104 Chips for 52 distinct cards)*. |
| <img src="assets/2x/j_the_bell.png" width="60" alt="The Bell" /> | **The Bell** | `Uncommon` | $6 | Scoring cards are **retriggered** based on distance from margins *(Gaussian distribution up to +2)*. |
| <img src="assets/2x/j_fortune_cookie.png" width="60" alt="Fortune Cookie" /> | **Fortune Cookie** | `Uncommon` | $6 | When **sold**, creates **1 Tarot** and **1 Spectral** card *(generates Spectral first if only 1 slot)*. |
| <img src="assets/2x/j_wrong_schematics.png" width="60" alt="Wrong Schematics" /> | **Wrong Schematics** | `Uncommon` | $7 | **1 in 2 chance** to copy right Joker or left Joker; copies **both** if probability reaches 2 in 2. |
| <img src="assets/2x/j_magifect.png" width="60" alt="Magifect" /> | **Magifect** | `Uncommon` | $6 | Retriggers all **Editions** (Foil, Holographic, Polychrome) for every Joker. |
| <img src="assets/2x/j_jackpot.png" width="60" alt="Jackpot" /> | **Jackpot** | `Uncommon` | $6 | If played hand contains at least **3 scoring 7s**, each scored 7 awards **$6**. |
| <img src="assets/2x/j_multifaces.png" width="60" alt="MultiFaces" /> | **MultiFaces** | `Uncommon` | $6 | Converts played **2s** into **Jacks**, **3s** into **Queens**, and **4s** into **Kings** when played. |
| <img src="assets/2x/j_bonus_stage.png" width="60" alt="Bonus Stage" /> | **Bonus Stage** | `Uncommon` | $6 | Retriggers all played **Bonus Cards**. |
| <img src="assets/2x/j_overdrive.png" width="60" alt="Overdrive" /> | **Overdrive** | `Uncommon` | $6 | Retriggers all played **Mult Cards**. |
| <img src="assets/2x/j_kaleidoscope.png" width="60" alt="Kaleidoscope" /> | **Kaleidoscope** | `Uncommon` | $6 | Retriggers all played **Wild Cards**. |
| <img src="assets/2x/j_the_anvil.png" width="60" alt="The Anvil" /> | **The Anvil** | `Uncommon` | $6 | Retriggers all played **Steel Cards**. |
| <img src="assets/2x/j_monolith.png" width="60" alt="Monolith" /> | **Monolith** | `Uncommon` | $6 | Retriggers all played **Stone Cards**. |
| <img src="assets/2x/j_bullion.png" width="60" alt="Bullion" /> | **Bullion** | `Uncommon` | $6 | Retriggers all played **Gold Cards**. |
| <img src="assets/2x/j_glassblower.png" width="60" alt="Glassblower" /> | **Glassblower** | `Uncommon` | $6 | Retrigger all played **Glass Cards**; **1 in 25 chance** to break when retriggering. |
| <img src="assets/2x/j_golden_horseshoe.png" width="60" alt="Golden Horseshoe" /> | **Golden Horseshoe** | `Uncommon` | $6 | **1 in 3 chance** to retrigger each played **Lucky Card**. |
| <img src="assets/2x/j_sphene.png" width="60" alt="Sphene" /> | **Sphene** | `Uncommon` | $6 | Played **Diamond** cards have a **1 in 3 chance** to be **retriggered**. |
| <img src="assets/2x/j_ruby_heart.png" width="60" alt="Ruby Heart" /> | **Ruby Heart** | `Uncommon` | $6 | Played **Heart** cards have a **1 in 3 chance** to be **retriggered**. |
| <img src="assets/2x/j_black_diamond.png" width="60" alt="Black Diamond" /> | **Black Diamond** | `Uncommon` | $6 | Played **Spade** cards have a **1 in 3 chance** to be **retriggered**. |
| <img src="assets/2x/j_emerald.png" width="60" alt="Emerald" /> | **Emerald** | `Uncommon` | $6 | Played **Club** cards have a **1 in 3 chance** to be **retriggered**. |
| <img src="assets/2x/j_frugal_joker.png" width="60" alt="Frugal Joker" /> | **Frugal Joker** | `Uncommon` | $6 | Each **Diamond** card held in hand gives **$1**. |
| <img src="assets/2x/j_fickle_joker.png" width="60" alt="Fickle Joker" /> | **Fickle Joker** | `Uncommon` | $6 | Each **Heart** card held in hand has a **1 in 4 chance** to give **X1.5 Mult**. |
| <img src="assets/2x/j_stoic_joker.png" width="60" alt="Stoic Joker" /> | **Stoic Joker** | `Uncommon` | $6 | Each **Spade** card held in hand gives **+25 Chips**. |
| <img src="assets/2x/j_stubborn_joker.png" width="60" alt="Stubborn Joker" /> | **Stubborn Joker** | `Uncommon` | $6 | Each **Club** card held in hand gives **+4 Mult**. |
| <img src="assets/2x/j_taxi_driver.png" width="60" alt="Taxi Driver" /> | **Taxi Driver** | `Rare` | $8 | Earn **$1** for each **scoring card** when hand is scored. |
| <img src="assets/2x/j_river.png" width="60" alt="River" /> | **River** | `Rare` | $8 | Adds the **Chips** and **Mult** of the poker hand currently held in hand to scoring. |
| <img src="assets/2x/j_doubler.png" width="60" alt="Doubler" /> | **Doubler** | `Rare` | $8 | When **sold**, doubles all numerical values of a random owned Joker. |
| <img src="assets/2x/j_burnt_offering.png" width="60" alt="Burnt Offering" /> | **Burnt Offering** | `Rare` | $8 | Destroys **1 random card** from 1st played hand of round and creates a random **Tarot**. |
| <img src="assets/2x/j_the_scythe.png" width="60" alt="The Scythe" /> | **The Scythe** | `Rare` | $8 | If 1st hand has 3 cards, destroys 2 side cards & creates a permanent copy of middle card. |
| <img src="assets/2x/j_stanczyk.png" width="60" alt="Stańczyk" /> | **Stańczyk** | `Legendary` | $20 | When Boss Blind is defeated, creates a **Negative + Eternal + Rental** copy of another owned Joker. |
| <img src="assets/2x/j_sommers.png" width="60" alt="Sommers" /> | **Sommers** | `Legendary` | $20 | Discarded **Blue Seals** permanently grant **+20 Chips**; discarded **Red Seals** grant **+X0.25 Mult**. |

</details>

---

### 🔮 Tarot Cards

| Sprite | Name | Target | Effect Summary |
| :---: | :--- | :--- | :--- |
| <img src="assets/2x/c_the_mirror.png" width="60" alt="The Mirror" /> | **The Mirror** (XVI) | 2 selected cards | Converts the **left card** into the **rank and suit** of the **right card** *(preserves Enhancements, Editions, and Seals on target card)*. |
| <img src="assets/2x/c_weakness.png" width="60" alt="Weakness" /> | **Weakness** (XI) | Up to 2 selected cards | **Decreases rank** of up to 2 selected cards by **1** *(2 wraps to Ace)*. Counterpart to *Strength*. |
| <img src="assets/2x/c_swaper.png" width="60" alt="Swaper" /> | **Swaper** (XVI) | 2 selected cards | **Swaps all Enhancements, Editions, and Seals** between 2 selected cards. |

---

### 👻 Spectral Cards

| Sprite | Name | Cost | Effect Summary |
| :---: | :--- | :---: | :--- |
| <img src="assets/2x/c_phantasm.png" width="60" alt="Phantasm" /> | **Phantasm** | $4 | Removes all **debuffs** from cards currently held in hand. Protects them from being re-debuffed during the round. *(Appears in shops; never spawns inside booster packs)*. |
| <img src="assets/2x/c_pact.png" width="60" alt="Pact" /> | **Pact** | $4 | Add **Eternal** to a random eligible Joker, gain **$25**. Cleanses *Perishable* if present. |

---

### 🖐️ Poker Hands & 🪐 Planets

| Type | Name | Sprite | Requirement / Hand | Base Stats / Bonus | Status |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **Poker Hand** | **Quarry** | — | **5 Stone Cards** | **200 Chips, 20 Mult**<br>*(+40 Chips, +4 Mult per level)* | Secret Hand |
| **Planet** | **Nibiru** | <img src="assets/2x/c_nibiru.png" width="60" alt="Nibiru" /> | Levels up **Quarry** | **+40 Chips, +4 Mult** | Softlocked *(appears once Quarry is played)* |

---

### 🎟️ Vouchers

| Sprite | Name | Tier | Cost | Prerequisite | Effect |
| :---: | :--- | :---: | :---: | :---: | :--- |
| <img src="assets/2x/v_market.png" width="60" alt="Market" /> | **Market** | Tier 1 | $10 | — | **+1 Booster Pack slot** available in shop. |
| <img src="assets/2x/v_supermarket.png" width="60" alt="Supermarket" /> | **Supermarket** | Tier 2 | $10 | Market | **+1 Voucher slot** available in shop. |

---

### 🎴 Decks & Sleeves

| Type | Name | Sprite | Effect Summary |
| :---: | :--- | :---: | :--- |
| **Deck** | **Echo Deck** | <img src="assets/2x/b_echo.png" width="60" alt="Echo Deck" /> | Retriggers all **Jokers 1 additional time** (2 triggers total). Required Blind chips scale by **X Ante base size** *(Ante 1 = 1x, Ante 2 = 2x, ..., Ante 8 = 8x)*. Standard 5 Joker slots & normal reroll costs. |
| **Sleeve** | **Echo Sleeve** | <img src="assets/2x/sleeve_echo.png" width="60" alt="Echo Sleeve" /> | **Standard**: Retriggers all Jokers **1 additional time**, Blinds scale by X Ante.<br>**Paired with Echo Deck**: Retriggers every **played card 1 additional time** (cards score twice!), **-1 hand size**. |

---

## 🤝 Compatibility

- **[CardSleeves](https://github.com/Larswijn/CardSleeves)**: Fully integrated optional support. The **Echo Sleeve** automatically registers and becomes available in the sleeve selection menu if CardSleeves is installed, and gracefully sleeps if it is not present.
- **[SlotManager](https://github.com/BlazeCrowner/SlotManager)**: Fully compatible — dynamically respects and allocates shop slots when **Market** (+1 Booster Pack slot) or **Supermarket** (+1 Voucher slot) are redeemed.
- **Vanilla Localthunk Style**: Strict 71×95 (1x) and 142×190 (2x) nearest-neighbor pixel enforcement with authentic Balatro palettes.

---

## 🛠️ Contributing & Roadmap

Detailed balance logs, art director prompts, and planned mechanics are documented in [`Feature_Added.md`](Feature_Added.md). Feel free to submit issues, balance feedback, or feature suggestions on the GitHub repository!
