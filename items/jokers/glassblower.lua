--- Glassblower Joker
--- Uncommon Joker ($6)
--- Retriggers all played Glass Cards, 1 in 25 chance to break when retriggering.

SMODS.Atlas {
    key = "j_glassblower",
    path = "j_glassblower.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Glassblower",
    key = "glassblower",
    atlas = "j_glassblower",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { odds = 25 } },
    loc_txt = {
        name = "Glassblower",
        text = {
            "Retrigger all played",
            "{C:attention}Glass Cards{},",
            "{C:green}#1# in #2#{} chance to",
            "break when retriggering"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_glass
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds
        return { vars = { '' .. (G.GAME and G.GAME.probabilities.normal or 1), odds } }
    end,
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            local other = context.other_card
            local is_glass = (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_glass'))
                or (other.ability and (other.ability.name == 'Glass Card' or other.ability.effect == 'Glass Card'))
                or (other.config and other.config.center == G.P_CENTERS.m_glass)

            if is_glass then
                local odds = (card.ability and card.ability.extra and card.ability.extra.odds) or 25
                if not card.shattered and pseudorandom('glassblower') < G.GAME.probabilities.normal / odds then
                    card.shattered = true
                    G.E_MANAGER:add_event(Event({
                        func = function()
                            play_sound('glass' .. math.random(1, 6))
                            card:shatter()
                            return true
                        end
                    }))
                    return {
                        message = localize('k_extinct_ex'),
                        repetitions = 1,
                        card = card
                    }
                else
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
