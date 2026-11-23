--- Sommers (Legendary Joker)
--- Follows the lore of legendary court jesters (Canio, Triboulet, Yorick, Chicot, Perkeo, Stańczyk).
--- Named after Will Sommers, the legendary court jester to King Henry VIII.
--- Gains +20 Chips when a card with a Blue Seal is discarded.
--- Gains X0.25 Mult when a card with a Red Seal is discarded.

SMODS.Atlas {
    key = "sommers",
    path = "j_sommers.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "sommers",
    loc_txt = {
        name = "Sommers",
        text = {
            "Gains {C:chips}+#1#{} Chips when a",
            "card with a {C:blue}Blue Seal{} is discarded,",
            "gains {X:mult,C:white}X#2#{} Mult when a",
            "card with a {C:red}Red Seal{} is discarded",
            "{C:inactive}(Currently {C:chips}+#3#{C:inactive} Chips and {X:mult,C:white}X#4#{C:inactive} Mult){}"
        }
    },
    config = {
        extra = {
            chip_mod = 20,
            x_mult_mod = 0.25,
            chips = 0,
            x_mult = 1
        }
    },
    rarity = 4, -- Legendary
    cost = 20,
    blueprint_compat = true,
    atlas = "sommers",
    pos = { x = 0, y = 0 },
    soul_pos = { x = 0, y = 1 }, -- 3D floating soul layer
    loc_vars = function(self, info_queue, card)
        local chip_mod = (card and card.ability and card.ability.extra and card.ability.extra.chip_mod) or self.config.extra.chip_mod
        local x_mult_mod = (card and card.ability and card.ability.extra and card.ability.extra.x_mult_mod) or self.config.extra.x_mult_mod
        local chips = (card and card.ability and card.ability.extra and card.ability.extra.chips) or self.config.extra.chips
        local x_mult = (card and card.ability and card.ability.extra and card.ability.extra.x_mult) or self.config.extra.x_mult
        return {
            vars = {
                chip_mod,
                x_mult_mod,
                chips,
                x_mult
            }
        }
    end,
    calculate = function(self, card, context)
        -- Trigger when discarding cards with Blue or Red Seal
        if context.discard and not context.blueprint then
            if context.other_card and not context.other_card.debuff then
                local seal = context.other_card.seal
                if seal == 'Blue' then
                    card.ability.extra.chips = card.ability.extra.chips + card.ability.extra.chip_mod
                    return {
                        message = localize { type = 'variable', key = 'a_chips', vars = { card.ability.extra.chips } },
                        colour = G.C.CHIPS,
                        card = card
                    }
                elseif seal == 'Red' then
                    card.ability.extra.x_mult = card.ability.extra.x_mult + card.ability.extra.x_mult_mod
                    return {
                        message = localize { type = 'variable', key = 'a_xmult', vars = { card.ability.extra.x_mult } },
                        colour = G.C.RED,
                        card = card
                    }
                end
            end
        end

        -- Scoring during joker_main
        if context.joker_main then
            local chips = card.ability.extra.chips
            local x_mult = card.ability.extra.x_mult
            local ret = {}
            if chips > 0 then
                ret.chips = chips
            end
            if x_mult > 1 then
                ret.Xmult_mod = x_mult
                ret.message = localize { type = 'variable', key = 'a_xmult', vars = { x_mult } }
            elseif chips > 0 then
                ret.message = localize { type = 'variable', key = 'a_chips', vars = { chips } }
            end
            if next(ret) then
                return ret
            end
        end
    end
}
