--- Burnt Offering (Rare Joker)
--- Each round, destroys a random playing card from the first hand played
--- and creates a random Tarot card.

SMODS.Atlas {
    key = "burnt_offering",
    path = "j_burnt_offering.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "burnt_offering",
    loc_txt = {
        name = "Burnt Offering",
        text = {
            "Destroys a random card from",
            "the {C:attention}first hand{} of round",
            "and creates a random {C:tarot}Tarot{} card",
            "{C:inactive}(Must have room){}"
        }
    },
    rarity = 3, -- 1: Common, 2: Uncommon, 3: Rare, 4: Legendary
    cost = 8,
    blueprint_compat = false,
    atlas = "burnt_offering",
    pos = { x = 0, y = 0 },
    calculate = function(self, card, context)
        -- In the first hand played, pick 1 random card to destroy
        if context.before and G.GAME.current_round.hands_played == 0 and not context.blueprint then
            if context.full_hand and #context.full_hand > 0 then
                card.ability.chosen_card = pseudorandom_element(context.full_hand, pseudoseed('burnt_offering'))
            end
        end

        -- Destroy the chosen card and create a random Tarot card
        if context.destroying_card and not context.blueprint then
            if card.ability.chosen_card and context.destroying_card == card.ability.chosen_card and G.GAME.current_round.hands_played == 0 then
                card.ability.chosen_card = nil

                if G.consumeables and G.consumeables.cards and G.consumeables.config and (#G.consumeables.cards + (G.GAME.consumeable_buffer or 0) < G.consumeables.config.card_limit) then
                    G.GAME.consumeable_buffer = (G.GAME.consumeable_buffer or 0) + 1
                    G.E_MANAGER:add_event(Event({
                        trigger = 'before',
                        delay = 0.0,
                        func = function()
                            local tarot = create_card('Tarot', G.consumeables, nil, nil, nil, nil, nil, 'burnt_offering')
                            tarot:add_to_deck()
                            G.consumeables:emplace(tarot)
                            G.GAME.consumeable_buffer = 0
                            return true
                        end
                    }))
                    card_eval_status_text(card, 'extra', nil, nil, nil, {
                        message = localize('k_plus_tarot'),
                        colour = G.C.SECONDARY_SET.Tarot
                    })
                end

                return true
            end
        end

        -- Reset state at end of round
        if context.end_of_round then
            card.ability.chosen_card = nil
        end
    end
}
