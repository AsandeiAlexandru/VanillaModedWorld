--- Doubler (Rare Joker)
--- When sold, doubles the values of a random Joker.

SMODS.Atlas {
    key = "doubler",
    path = "j_doubler.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "doubler",
    loc_txt = {
        name = "Doubler",
        text = {
            "When {C:attention}sold{}, doubles the",
            "values of a random {C:attention}Joker{}"
        }
    },
    rarity = 3, -- 1: Common, 2: Uncommon, 3: Rare, 4: Legendary
    cost = 8,
    blueprint_compat = false,
    atlas = "doubler",
    pos = { x = 0, y = 0 },
    calculate = function(self, card, context)
        -- Triggers when this card is sold
        if context.selling_self and not context.blueprint then
            if not G.jokers or not G.jokers.cards then return end
            local eligible = {}
            for _, j in ipairs(G.jokers.cards) do
                if j ~= card then
                    eligible[#eligible + 1] = j
                end
            end

            if #eligible > 0 then
                local chosen = pseudorandom_element(eligible, pseudoseed('doubler'))
                G.E_MANAGER:add_event(Event({
                    func = function()
                        play_sound('tarot1')
                        chosen:juice_up(0.7, 0.7)

                        -- Double numerical values in ability.extra
                        if type(chosen.ability.extra) == 'number' then
                            chosen.ability.extra = chosen.ability.extra * 2
                        elseif type(chosen.ability.extra) == 'table' then
                            for k, v in pairs(chosen.ability.extra) do
                                if type(v) == 'number' then
                                    chosen.ability.extra[k] = v * 2
                                end
                            end
                        end

                        -- Double direct ability values if present
                        if chosen.ability.mult and type(chosen.ability.mult) == 'number' then
                            chosen.ability.mult = chosen.ability.mult * 2
                        end
                        if chosen.ability.chips and type(chosen.ability.chips) == 'number' then
                            chosen.ability.chips = chosen.ability.chips * 2
                        end
                        if chosen.ability.x_mult and type(chosen.ability.x_mult) == 'number' then
                            chosen.ability.x_mult = chosen.ability.x_mult * 2
                        end
                        if chosen.ability.t_mult and type(chosen.ability.t_mult) == 'number' then
                            chosen.ability.t_mult = chosen.ability.t_mult * 2
                        end
                        if chosen.ability.t_chips and type(chosen.ability.t_chips) == 'number' then
                            chosen.ability.t_chips = chosen.ability.t_chips * 2
                        end

                        card_eval_status_text(chosen, 'extra', nil, nil, nil, {
                            message = "Doubled!",
                            colour = G.C.MONEY
                        })
                        return true
                    end
                }))
            end
        end
    end
}
