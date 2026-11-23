--- Camera Joker
--- Common Joker ($5)
--- First numbered card held in hand gives X2 Mult.
--- Counterpart / continuation to Photograph (which buffs face cards).

SMODS.Atlas {
    key = "j_camera",
    path = "j_camera.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Camera",
    key = "camera",
    atlas = "j_camera",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 5,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { x_mult = 2 } },
    loc_vars = function(self, info_queue, card)
        local x_mult = (card and card.ability and card.ability.extra and card.ability.extra.x_mult) or self.config.extra.x_mult
        return { vars = { x_mult } }
    end,
    loc_txt = {
        name = "Camera",
        text = {
            "First {C:attention}numbered{} card",
            "held in hand gives",
            "{X:mult,C:white} X#1# {} Mult",
            "{C:inactive}(2, 3, 4... 10){}"
        }
    },
    calculate = function(self, card, context)
        if context.individual and context.cardarea == G.hand and not context.end_of_round then
            local first_numbered = nil
            if G.hand and G.hand.cards then
                for i = 1, #G.hand.cards do
                    local id = G.hand.cards[i]:get_id()
                    if id and id >= 2 and id <= 10 then
                        first_numbered = G.hand.cards[i]
                        break
                    end
                end
            end
            if first_numbered and context.other_card == first_numbered then
                if context.other_card.debuff then
                    return {
                        message = localize('k_debuffed'),
                        colour = G.C.RED,
                        card = card
                    }
                else
                    return {
                        x_mult = card.ability.extra.x_mult,
                        colour = G.C.RED,
                        card = card
                    }
                end
            end
        end
    end
}
