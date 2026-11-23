--- Stańczyk (Legendary Joker)
--- Follows the lore of legendary court jesters (Canio, Triboulet, Yorick, Chicot, Perkeo).
--- Creates a Negative, Eternal, and Rental copy of a random Joker when Boss Blind is defeated.

SMODS.Atlas {
    key = "stanczyk",
    path = "j_stanczyk.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "stanczyk",
    loc_txt = {
        name = "Stańczyk",
        text = {
            "Creates a {C:dark_edition}Negative{},",
            "{C:attention}Eternal{}, and {C:attention}Rental{} copy",
            "of a random other {C:attention}Joker{}",
            "when {C:attention}Boss Blind{} is defeated",
            "{C:inactive}(Stańczyk excluded){}"
        }
    },
    rarity = 4, -- Legendary
    cost = 20,
    blueprint_compat = false,
    atlas = "stanczyk",
    pos = { x = 0, y = 0 },
    soul_pos = { x = 0, y = 1 }, -- 3D floating soul layer
    loc_vars = function(self, info_queue, card)
        if info_queue then
            info_queue[#info_queue + 1] = G.P_CENTERS['e_negative']
            info_queue[#info_queue + 1] = { key = 'eternal', set = 'Other' }
            info_queue[#info_queue + 1] = { key = 'rental', set = 'Other', vars = { (G.GAME and G.GAME.rental_rate) or 3 } }
        end
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        -- Triggers when Boss Blind is defeated at end of round
        if context.end_of_round and not context.individual and not context.repetition and not context.blueprint then
            if G.GAME.blind and G.GAME.blind.boss then
                if not G.jokers or not G.jokers.cards then return end
                local eligible = {}
                for _, j in ipairs(G.jokers.cards) do
                    if j ~= card and j.config.center.key ~= "j_vmw_stanczyk" and j.ability.name ~= "Stańczyk" then
                        eligible[#eligible + 1] = j
                    end
                end

                if #eligible > 0 then
                    local chosen = pseudorandom_element(eligible, pseudoseed('stanczyk'))
                    G.E_MANAGER:add_event(Event({
                        func = function()
                            play_sound('timpani')
                            card:juice_up(0.6, 0.6)
                            local copied = copy_card(chosen, nil, nil, nil, false)
                            copied:set_edition({ negative = true }, true)
                            copied:set_eternal(true)
                            copied:set_rental(true)
                            copied:add_to_deck()
                            G.jokers:emplace(copied)
                            return true
                        end
                    }))
                    return {
                        message = localize('k_duplicated_ex'),
                        colour = G.C.DARK_EDITION
                    }
                end
            end
        end
    end
}
