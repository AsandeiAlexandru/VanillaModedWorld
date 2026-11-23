--- Pact Spectral Card
--- Adds Eternal to a random Joker, gain $25.

SMODS.Atlas {
    key = "pact",
    path = "c_pact.png",
    px = 71,
    py = 95
}

SMODS.Consumable {
    set = "Spectral",
    key = "pact",
    loc_txt = {
        name = "Pact",
        text = {
            "Add {C:attention}Eternal{} to a",
            "random {C:attention}Joker{},",
            "gain {C:money}$#1#{}"
        }
    },
    config = { extra = 25 },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = { key = 'eternal', set = 'Other' }
        return { vars = { (card and card.ability and card.ability.extra) or self.config.extra or 25 } }
    end,
    atlas = "pact",
    pos = { x = 0, y = 0 },
    cost = 4,
    can_use = function(self, card)
        if not G.jokers or not G.jokers.cards then return false end
        for _, j in ipairs(G.jokers.cards) do
            if (j.config.center.eternal_compat ~= false) and not j.ability.eternal then
                return true
            end
        end
        return false
    end,
    use = function(self, card, area, copier)
        local used_tarot = copier or card
        local dollars = (card and card.ability and card.ability.extra) or self.config.extra or 25

        if not G.jokers or not G.jokers.cards then return end

        local eligible_jokers = {}
        for _, j in ipairs(G.jokers.cards) do
            if (j.config.center.eternal_compat ~= false) and not j.ability.eternal then
                table.insert(eligible_jokers, j)
            end
        end

        if #eligible_jokers > 0 then
            local chosen_joker = pseudorandom_element(eligible_jokers, pseudoseed('pact'))

            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.4,
                func = function()
                    play_sound('tarot1')
                    used_tarot:juice_up(0.3, 0.5)
                    return true
                end
            }))

            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.2,
                func = function()
                    -- If the joker had perishable, remove it so eternal can be set cleanly
                    if chosen_joker.ability.perishable then
                        chosen_joker.ability.perishable = nil
                        chosen_joker.ability.perish_tally = nil
                    end
                    chosen_joker:set_eternal(true)
                    play_sound('gold_seal', 1.2, 0.4)
                    chosen_joker:juice_up(0.5, 0.5)
                    return true
                end
            }))

            delay(0.4)

            ease_dollars(dollars)
            delay(0.3)
        end
    end
}
