--- Fickle Joker
--- Uncommon Joker ($6)
--- Each Heart card held in hand has a 1 in 4 chance to give X1.5 Mult.

SMODS.Atlas {
    key = "j_fickle_joker",
    path = "j_fickle_joker.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Fickle Joker",
    key = "fickle_joker",
    atlas = "j_fickle_joker",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { odds = 4, x_mult = 1.5 } },
    loc_vars = function(self, info_queue, card)
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds
        local x_mult = (card and card.ability and card.ability.extra and card.ability.extra.x_mult) or self.config.extra.x_mult
        return { vars = { '' .. (G.GAME and G.GAME.probabilities.normal or 1), odds, x_mult } }
    end,
    loc_txt = {
        name = "Fickle Joker",
        text = {
            "Each {C:hearts}Heart{} card",
            "held in hand has a",
            "{C:green}#1# in #2#{} chance to give",
            "{X:mult,C:white}X#3#{} Mult"
        }
    },
    calculate = function(self, card, context)
        if context.individual and context.cardarea == G.hand and not context.end_of_round then
            if context.other_card:is_suit('Hearts') then
                if pseudorandom('fickle') < G.GAME.probabilities.normal / card.ability.extra.odds then
                    return {
                        x_mult = card.ability.extra.x_mult,
                        card = card
                    }
                end
            end
        end
    end
}
