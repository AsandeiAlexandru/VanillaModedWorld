--- Fortune Cookie (Uncommon Joker)
--- When sold, creates 1 random Tarot card and 1 random Spectral card.
--- (Must have room; generates Spectral first if only 1 slot available).

SMODS.Atlas {
    key = "fortune_cookie",
    path = "j_fortune_cookie.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "fortune_cookie",
    loc_txt = {
        name = "Fortune Cookie",
        text = {
            "When {C:attention}sold{}, creates {C:attention}1{} random",
            "{C:tarot}Tarot{} card and {C:attention}1{} random",
            "{C:spectral}Spectral{} card",
            "{C:inactive}(Must have room; generates{}",
            "{C:spectral}Spectral{} {C:inactive}first if only 1 slot){}"
        }
    },
    rarity = 2, -- 1: Common, 2: Uncommon, 3: Rare, 4: Legendary
    cost = 6,
    blueprint_compat = false,
    atlas = "fortune_cookie",
    pos = { x = 0, y = 0 },
    calculate = function(self, card, context)
        if context.selling_self and not context.blueprint then
            if not G.consumeables or not G.consumeables.cards or not G.consumeables.config then return end
            local free_slots = G.consumeables.config.card_limit - (#G.consumeables.cards + (G.GAME.consumeable_buffer or 0))

            -- If at least 1 free slot, create Spectral card first
            if free_slots >= 1 then
                G.GAME.consumeable_buffer = (G.GAME.consumeable_buffer or 0) + 1
                G.E_MANAGER:add_event(Event({
                    trigger = 'before',
                    delay = 0.0,
                    func = function()
                        local card_spectral = create_card('Spectral', G.consumeables, nil, nil, nil, nil, nil, 'fortune_cookie_spectral')
                        card_spectral:add_to_deck()
                        G.consumeables:emplace(card_spectral)
                        G.GAME.consumeable_buffer = math.max(0, G.GAME.consumeable_buffer - 1)
                        return true
                    end
                }))
                card_eval_status_text(card, 'extra', nil, nil, nil, {
                    message = localize('k_plus_spectral'),
                    colour = G.C.SECONDARY_SET.Spectral
                })
            end

            -- If at least 2 free slots, create Tarot card second
            if free_slots >= 2 then
                G.GAME.consumeable_buffer = G.GAME.consumeable_buffer + 1
                G.E_MANAGER:add_event(Event({
                    trigger = 'before',
                    delay = 0.0,
                    func = function()
                        local card_tarot = create_card('Tarot', G.consumeables, nil, nil, nil, nil, nil, 'fortune_cookie_tarot')
                        card_tarot:add_to_deck()
                        G.consumeables:emplace(card_tarot)
                        G.GAME.consumeable_buffer = math.max(0, G.GAME.consumeable_buffer - 1)
                        return true
                    end
                }))
                card_eval_status_text(card, 'extra', nil, nil, nil, {
                    message = localize('k_plus_tarot'),
                    colour = G.C.SECONDARY_SET.Tarot
                })
            end
        end
    end
}
