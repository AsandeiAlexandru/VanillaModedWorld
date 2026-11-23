--- Hot Pepper (Common Joker)
--- Each played card gives X1.2 Mult when scored.
--- Self-destructs when Boss Blind is defeated.

SMODS.Atlas {
    key = "hot_pepper",
    path = "j_hot_pepper.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "hot_pepper",
    loc_txt = {
        name = "Hot Pepper",
        text = {
            "Each played card gives",
            "{X:mult,C:white}X#1#{} Mult when scored.",
            "{C:red}Self-destructs{} when",
            "{C:attention}Boss Blind{} is defeated"
        }
    },
    config = { extra = { x_mult = 1.2 } },
    rarity = 1, -- 1: Common, 2: Uncommon, 3: Rare, 4: Legendary
    cost = 4,
    blueprint_compat = true,
    atlas = "hot_pepper",
    pos = { x = 0, y = 0 },
    loc_vars = function(self, info_queue, card)
        local x_mult = (card and card.ability and card.ability.extra and card.ability.extra.x_mult) or self.config.extra.x_mult
        return { vars = { x_mult } }
    end,
    calculate = function(self, card, context)
        -- Each played card gives X1.2 Mult when scored
        if context.individual and context.cardarea == G.play then
            return {
                x_mult = card.ability.extra.x_mult,
                card = card
            }
        end

        -- Self-destructs when Boss Blind is defeated
        if context.end_of_round and not context.blueprint and not context.repetition and not context.individual then
            if G.GAME.blind and G.GAME.blind.boss and not card.ability.eternal then
                G.E_MANAGER:add_event(Event({
                    func = function()
                        play_sound('tarot1')
                        card.T.r = -0.2
                        card:juice_up(0.3, 0.4)
                        card.states.drag.is = true
                        card.children.center.pinch.x = true
                        G.E_MANAGER:add_event(Event({
                            trigger = 'after',
                            delay = 0.3,
                            blockable = false,
                            func = function()
                                G.jokers:remove_card(card)
                                card:remove()
                                card = nil
                                return true
                            end
                        }))
                        return true
                    end
                }))
                return {
                    message = "Burned Out!",
                    colour = G.C.RED
                }
            end
        end
    end
}
