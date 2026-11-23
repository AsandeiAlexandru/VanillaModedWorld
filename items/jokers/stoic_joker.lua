--- Stoic Joker
--- Uncommon Joker ($6)
--- Each Spade card held in hand gives +25 Chips.

SMODS.Atlas {
    key = "j_stoic_joker",
    path = "j_stoic_joker.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Stoic Joker",
    key = "stoic_joker",
    atlas = "j_stoic_joker",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { chips = 25 } },
    loc_vars = function(self, info_queue, card)
        local chips = (card and card.ability and card.ability.extra and card.ability.extra.chips) or self.config.extra.chips
        return { vars = { chips } }
    end,
    loc_txt = {
        name = "Stoic Joker",
        text = {
            "Each {C:spades}Spade{} card",
            "held in hand",
            "gives {C:chips}+#1#{} Chips"
        }
    },
    calculate = function(self, card, context)
        if context.individual and context.cardarea == G.hand and not context.end_of_round then
            if context.other_card:is_suit('Spades') then
                return {
                    chips = card.ability.extra.chips,
                    card = card
                }
            end
        end
    end
}
