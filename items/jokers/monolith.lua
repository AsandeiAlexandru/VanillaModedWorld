--- Monolith Joker
--- Uncommon Joker
--- Retriggers all played Stone Cards.

SMODS.Atlas {
    key = "j_monolith",
    path = "j_monolith.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Monolith",
    key = "monolith",
    atlas = "j_monolith",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "Monolith",
        text = {
            "Retrigger all played",
            "{C:attention}Stone Cards{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_stone
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_stone = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_stone'))
                or (other.ability and (other.ability.name == 'Stone Card' or other.ability.effect == 'Stone Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_stone)

            if is_stone then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = card
                }
            end
        end
    end
}
