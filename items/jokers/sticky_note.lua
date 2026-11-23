--- Sticky Note Joker
--- Common Joker ($4)
--- Retriggers first card held in hand 2 additional times.

SMODS.Atlas {
    key = "j_sticky_note",
    path = "j_sticky_note.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Sticky Note",
    key = "sticky_note",
    atlas = "j_sticky_note",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { repetitions = 2 } },
    loc_vars = function(self, info_queue, card)
        local reps = (card and card.ability and card.ability.extra and card.ability.extra.repetitions) or self.config.extra.repetitions
        return { vars = { reps } }
    end,
    loc_txt = {
        name = "Sticky Note",
        text = {
            "Retrigger {C:attention}first{} card",
            "held in hand",
            "{C:attention}#1#{} additional times"
        }
    },
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.hand then
            if G.hand and G.hand.cards and context.other_card == G.hand.cards[1] then
                return {
                    message = localize('k_again_ex'),
                    repetitions = card.ability.extra.repetitions,
                    card = card
                }
            end
        end
    end
}
