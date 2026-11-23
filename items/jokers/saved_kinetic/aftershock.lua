--- Aftershock Joker
--- Common Joker ($5)
--- Played Club cards have a 1 in 3 chance to be retriggered.

SMODS.Atlas {
    key = "j_aftershock",
    path = "j_aftershock.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Aftershock",
    key = "aftershock",
    atlas = "j_aftershock",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 5,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { odds = 3, repetitions = 1 } },
    loc_vars = function(self, info_queue, card)
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds
        return { vars = { '' .. (G.GAME and G.GAME.probabilities.normal or 1), odds } }
    end,
    loc_txt = {
        name = "Aftershock",
        text = {
            "Played {C:clubs}Club{} cards have",
            "a {C:green}#1# in #2#{} chance",
            "to be {C:attention}retriggered{}"
        }
    },
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            if context.other_card:is_suit('Clubs') then
                if pseudorandom('aftershock') < G.GAME.probabilities.normal / card.ability.extra.odds then
                    return {
                        message = localize('k_again_ex'),
                        repetitions = card.ability.extra.repetitions,
                        card = card
                    }
                end
            end
        end
    end
}
