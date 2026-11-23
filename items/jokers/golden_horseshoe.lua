--- Golden Horseshoe Joker
--- Uncommon Joker ($6)
--- 1 in 3 chance to retrigger played Lucky Cards.

SMODS.Atlas {
    key = "j_golden_horseshoe",
    path = "j_golden_horseshoe.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Golden Horseshoe",
    key = "golden_horseshoe",
    atlas = "j_golden_horseshoe",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { odds = 3 } },
    loc_txt = {
        name = "Golden Horseshoe",
        text = {
            "{C:green}#1# in #2#{} chance to",
            "retrigger each played",
            "{C:attention}Lucky Card{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_lucky
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds
        return { vars = { '' .. (G.GAME and G.GAME.probabilities.normal or 1), odds } }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_lucky = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_lucky'))
                or (other.ability and (other.ability.name == 'Lucky Card' or other.ability.effect == 'Lucky Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_lucky)

            if is_lucky then
                local odds = (card.ability and card.ability.extra and card.ability.extra.odds) or 3
                if pseudorandom('golden_horseshoe') < G.GAME.probabilities.normal / odds then
                    return {
                        message = localize('k_again_ex'),
                        repetitions = 1,
                        card = card
                    }
                end
            end
        end
    end
}
