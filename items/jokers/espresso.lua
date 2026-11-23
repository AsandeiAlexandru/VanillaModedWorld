--- Espresso Joker
--- Gives X2 Mult on the first hand of each round.
--- 1 in 20 chance to transform into Double Espresso.

SMODS.Atlas {
    key = "espresso",
    path = "j_espresso.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "espresso",
    loc_txt = {
        name = "Espresso",
        text = {
            "{X:mult,C:white}X#1#{} Mult on {C:attention}first hand{}",
            "of round,",
            "{C:green}#2# in #3#{} chance to transform",
            "into {C:attention}Double Espresso{}",
        }
    },
    config = { extra = { x_mult = 2, odds = 20 } },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    atlas = "espresso",
    pos = { x = 0, y = 0 },
    loc_vars = function(self, info_queue, card)
        if info_queue and G.P_CENTERS and G.P_CENTERS['j_vmw_double_espresso'] then
            info_queue[#info_queue + 1] = G.P_CENTERS['j_vmw_double_espresso']
        end
        local x_mult = (card and card.ability and card.ability.extra and card.ability.extra.x_mult) or self.config.extra.x_mult
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds
        local num, denom = SMODS.get_probability_vars(card, 1, odds, 'espresso')
        return { vars = { x_mult, num, denom } }
    end,
    calculate = function(self, card, context)
        if context.joker_main and G.GAME.current_round.hands_played == 0 then
            local will_transform = not context.blueprint and SMODS.pseudorandom_probability(card, 'espresso', 1, card.ability.extra.odds)
            if will_transform then
                G.E_MANAGER:add_event(Event({
                    trigger = 'after',
                    delay = 0.4,
                    func = function()
                        play_sound('tarot1')
                        card:set_ability(G.P_CENTERS['j_vmw_double_espresso'])
                        card:juice_up(0.8, 0.5)
                        return true
                    end
                }))
            end
            return {
                Xmult_mod = card.ability.extra.x_mult,
                message = localize { type = 'variable', key = 'a_xmult', vars = { card.ability.extra.x_mult } }
            }
        end
    end
}
