--- Bullion Joker
--- Uncommon Joker ($6)
--- Retriggers all played Gold Cards.

SMODS.Atlas {
    key = "j_bullion",
    path = "j_bullion.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Bullion",
    key = "bullion",
    atlas = "j_bullion",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "Bullion",
        text = {
            "Retrigger all played",
            "{C:attention}Gold Cards{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_gold
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_gold = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_gold'))
                or (other.ability and (other.ability.name == 'Gold Card' or other.ability.effect == 'Gold Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_gold)

            if is_gold then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = card
                }
            end
        end
    end
}
