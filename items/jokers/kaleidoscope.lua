--- Kaleidoscope Joker
--- Uncommon Joker
--- Retriggers all played Wild Cards.

SMODS.Atlas {
    key = "j_kaleidoscope",
    path = "j_kaleidoscope.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Kaleidoscope",
    key = "kaleidoscope",
    atlas = "j_kaleidoscope",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "Kaleidoscope",
        text = {
            "Retrigger all played",
            "{C:attention}Wild Cards{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_wild
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_wild = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_wild'))
                or (other.ability and (other.ability.name == 'Wild Card' or other.ability.effect == 'Wild Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_wild)

            if is_wild then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = card
                }
            end
        end
    end
}
