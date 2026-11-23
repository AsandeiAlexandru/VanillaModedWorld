--- Double Espresso Joker
--- Common Joker (evolved from Espresso or found in shop)
--- Each played 2 gives X2 Mult when scored.

SMODS.Atlas {
    key = "j_double_espresso",
    path = "j_double_espresso.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Double Espresso",
    key = "double_espresso",
    atlas = "j_double_espresso",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    in_pool = function(self, args)
        -- Cannot appear naturally in shops or booster packs;
        -- only obtainable when Espresso transforms into it!
        return false
    end,
    config = { extra = { x_mult = 2 } },
    loc_txt = {
        name = "Double Espresso",
        text = {
            "Each played {C:attention}2{}",
            "gives {X:mult,C:white}X#1#{} Mult",
            "when scored"
        }
    },
    loc_vars = function(self, info_queue, card)
        local x_mult = (card and card.ability and card.ability.extra and card.ability.extra.x_mult) or self.config.extra.x_mult
        return { vars = { x_mult } }
    end,
    calculate = function(self, card, context)
        if context.individual and context.cardarea == G.play then
            if context.other_card:get_id() == 2 then
                return {
                    x_mult = card.ability.extra.x_mult,
                    colour = G.C.RED,
                    card = card
                }
            end
        end
    end
}
