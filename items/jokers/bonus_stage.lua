--- Bonus Stage Joker
--- Uncommon Joker
--- Retriggers all played Bonus Cards.

SMODS.Atlas {
    key = "j_bonus_stage",
    path = "j_bonus_stage.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Bonus Stage",
    key = "bonus_stage",
    atlas = "j_bonus_stage",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "Bonus Stage",
        text = {
            "Retrigger all played",
            "{C:attention}Bonus Cards{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_bonus
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_bonus = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_bonus'))
                or (other.ability and (other.ability.name == 'Bonus' or other.ability.effect == 'Bonus Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_bonus)

            if is_bonus then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = card
                }
            end
        end
    end
}
