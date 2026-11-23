--- Nibiru Planet Card
--- Levels up the Quarry poker hand (+40 Chips, +4 Mult).
--- Softlocked until Quarry is played at least once in the run (like vanilla secret hand planets).

SMODS.Atlas {
    key = "nibiru",
    path = "c_nibiru.png",
    px = 71,
    py = 95
}

SMODS.Consumable {
    set = "Planet",
    key = "nibiru",
    config = { hand_type = "Quarry", softlock = true },
    pos = { x = 0, y = 0 },
    atlas = "nibiru",
    cost = 3,
    loc_txt = {
        name = "Nibiru",
        text = {
            "{S:0.8}({S:0.8,V:1}lvl.#2#{S:0.8}){} Level up",
            "{C:attention}#1#{}",
            "{C:mult}+#3#{} Mult and",
            "{C:chips}+#4#{} chips"
        }
    },
    loc_vars = function(self, info_queue, card)
        local hand = G.GAME and G.GAME.hands and G.GAME.hands["Quarry"] or { level = 1, l_mult = 4, l_chips = 40 }
        local lvl = hand.level or 1
        local colour = (lvl <= 1) and G.C.UI.TEXT_DARK or (G.C and G.C.HAND_LEVELS and G.C.HAND_LEVELS[math.min(lvl, 7)]) or G.C.UI.TEXT_LIGHT
        return {
            vars = {
                localize("Quarry", "poker_hands"),
                lvl,
                hand.l_mult or 4,
                hand.l_chips or 40,
                colours = { colour }
            }
        }
    end
}
