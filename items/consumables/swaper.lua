--- Swaper Tarot Card
--- Select 2 cards, swap Enhancements, Editions, and Seals between them.

SMODS.Atlas {
    key = "c_swaper",
    path = "c_swaper.png",
    px = 71,
    py = 95
}

SMODS.Consumable {
    set = "Tarot",
    key = "swaper",
    loc_txt = {
        name = "Swaper",
        text = {
            "Select {C:attention}#1#{} cards,",
            "{C:attention}swap{} all {C:attention}Enhancements{},",
            "{C:dark_edition}Editions{}, and {C:attention}Seals{}",
            "between them"
        }
    },
    config = { max_highlighted = 2 },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.max_highlighted } }
    end,
    atlas = "c_swaper",
    pos = { x = 0, y = 0 },
    cost = 3,
    can_use = function(self, card)
        if G.hand and G.hand.highlighted and #G.hand.highlighted == self.config.max_highlighted then
            local c1 = G.hand.highlighted[1]
            local c2 = G.hand.highlighted[2]
            if not c1 or not c2 then return false end
            local has_mod1 = (c1.seal ~= nil) or (c1.edition ~= nil) or (c1.config.center ~= G.P_CENTERS.c_base)
            local has_mod2 = (c2.seal ~= nil) or (c2.edition ~= nil) or (c2.config.center ~= G.P_CENTERS.c_base)
            return has_mod1 or has_mod2
        end
        return false
    end,
    use = function(self, card, area, copier)
        local used_tarot = copier or card
        if not G.hand or not G.hand.highlighted or #G.hand.highlighted < 2 then return end
        local card1 = G.hand.highlighted[1]
        local card2 = G.hand.highlighted[2]
        if not card1 or not card2 then return end
        local target_cards = { card1, card2 }

        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.4,
            func = function()
                play_sound('tarot1')
                used_tarot:juice_up(0.3, 0.5)
                return true
            end
        }))

        -- Flip cards face down
        for i = 1, #target_cards do
            local percent = 1.15 - (i - 0.999) / (#target_cards - 0.998) * 0.3
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    if target_cards[i] then
                        target_cards[i]:flip()
                        play_sound('card1', percent)
                        target_cards[i]:juice_up(0.3, 0.3)
                    end
                    return true
                end
            }))
        end

        delay(0.2)

        -- Perform swap while face down
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.1,
            func = function()
                -- 1. Swap Enhancements
                local center1 = card1.config.center
                local center2 = card2.config.center
                card1:set_ability(center2 or G.P_CENTERS.c_base)
                card2:set_ability(center1 or G.P_CENTERS.c_base)

                -- 2. Swap Editions
                local ed1 = card1.edition
                local ed2 = card2.edition
                card1:set_edition(ed2 and (ed2.key or copy_table(ed2)) or nil, true)
                card2:set_edition(ed1 and (ed1.key or copy_table(ed1)) or nil, true)

                -- 3. Swap Seals
                local seal1 = card1.seal
                local seal2 = card2.seal
                card1:set_seal(seal2, nil, true)
                card2:set_seal(seal1, nil, true)

                return true
            end
        }))

        -- Flip cards back face up with audio & juice
        for i = 1, #target_cards do
            local percent = 0.85 + (i - 0.999) / (#target_cards - 0.998) * 0.3
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    if target_cards[i] then
                        target_cards[i]:flip()
                        play_sound('tarot2', percent, 0.6)
                        target_cards[i]:juice_up(0.3, 0.3)
                    end
                    return true
                end
            }))
        end

        -- Unhighlight cards
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.2,
            func = function()
                if G.hand and G.hand.unhighlight_all then
                    G.hand:unhighlight_all()
                end
                return true
            end
        }))
        delay(0.5)
    end
}
