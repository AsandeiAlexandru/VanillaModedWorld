--- Frugal Joker
--- Uncommon Joker ($6)
--- Each Diamond card held in hand gives $1.

SMODS.Atlas {
    key = "j_frugal_joker",
    path = "j_frugal_joker.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Frugal Joker",
    key = "frugal_joker",
    atlas = "j_frugal_joker",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { dollars = 1 } },
    loc_vars = function(self, info_queue, card)
        local dollars = (card and card.ability and card.ability.extra and card.ability.extra.dollars) or self.config.extra.dollars
        return { vars = { dollars } }
    end,
    loc_txt = {
        name = "Frugal Joker",
        text = {
            "Each {C:diamonds}Diamond{} card",
            "held in hand",
            "gives {C:money}$#1#{}"
        }
    },
    calculate = function(self, card, context)
        if context.individual and context.cardarea == G.hand and not context.end_of_round then
            if context.other_card:is_suit('Diamonds') then
                return {
                    dollars = card.ability.extra.dollars,
                    card = card
                }
            end
        end
    end
}
