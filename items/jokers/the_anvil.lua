--- The Anvil Joker
--- Uncommon Joker
--- Retriggers all played Steel Cards.

SMODS.Atlas {
    key = "j_the_anvil",
    path = "j_the_anvil.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "The Anvil",
    key = "the_anvil",
    atlas = "j_the_anvil",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "The Anvil",
        text = {
            "Retrigger all played",
            "{C:attention}Steel Cards{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_steel
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_steel = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_steel'))
                or (other.ability and (other.ability.name == 'Steel Card' or other.ability.effect == 'Steel Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_steel)

            if is_steel then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = card
                }
            end
        end
    end
}
