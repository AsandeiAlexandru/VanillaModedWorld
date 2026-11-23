--- Stubborn Joker
--- Uncommon Joker ($6)
--- Each Club card held in hand gives +4 Mult.

SMODS.Atlas {
    key = "j_stubborn_joker",
    path = "j_stubborn_joker.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Stubborn Joker",
    key = "stubborn_joker",
    atlas = "j_stubborn_joker",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { mult = 4 } },
    loc_vars = function(self, info_queue, card)
        local mult = (card and card.ability and card.ability.extra and card.ability.extra.mult) or self.config.extra.mult
        return { vars = { mult } }
    end,
    loc_txt = {
        name = "Stubborn Joker",
        text = {
            "Each {C:clubs}Club{} card",
            "held in hand",
            "gives {C:mult}+#1#{} Mult"
        }
    },
    calculate = function(self, card, context)
        if context.individual and context.cardarea == G.hand and not context.end_of_round then
            if context.other_card:is_suit('Clubs') then
                return {
                    mult = card.ability.extra.mult,
                    card = card
                }
            end
        end
    end
}
