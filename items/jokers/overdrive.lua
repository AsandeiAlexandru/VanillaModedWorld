--- Overdrive Joker
--- Uncommon Joker
--- Retriggers all played Mult Cards.

SMODS.Atlas {
    key = "j_overdrive",
    path = "j_overdrive.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Overdrive",
    key = "overdrive",
    atlas = "j_overdrive",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "Overdrive",
        text = {
            "Retrigger all played",
            "{C:attention}Mult Cards{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_mult
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_mult = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_mult'))
                or (other.ability and (other.ability.name == 'Mult' or other.ability.effect == 'Mult Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_mult)

            if is_mult then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = card
                }
            end
        end
    end
}
