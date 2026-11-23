--- Overkill Joker
--- Common Joker ($4)
--- Creates a Spectral card when Boss Blind is defeated if any single hand scored at least 2X the Blind requirement.

SMODS.Atlas {
    key = "j_overkill",
    path = "j_overkill.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Overkill",
    key = "overkill",
    atlas = "j_overkill",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { overkill_achieved = false, overkill_notified = false } },
    loc_txt = {
        name = "Overkill",
        text = {
            "Creates a {C:spectral}Spectral{} card",
            "when {C:attention}Boss Blind{} is defeated",
            "if any single hand scored at",
            "least {C:attention}2X{} the Blind requirement",
            "{C:inactive}(Must have room){}"
        }
    },
    set_ability = function(self, card, initial, delay_sprites)
        card.ability.extra = {
            overkill_achieved = false,
            overkill_notified = false
        }
    end,
    calculate = function(self, card, context)
        -- Track each played hand during a Boss Blind
        if context.after and not context.blueprint then
            if G.GAME.blind and G.GAME.blind.boss and G.GAME.blind.chips then
                local hand_score = SMODS.last_hand_score or (hand_chips and mult and (hand_chips * mult)) or 0
                local is_overkill = false
                if to_big then
                    is_overkill = to_big(hand_score) >= to_big(G.GAME.blind.chips) * 2
                else
                    is_overkill = hand_score >= G.GAME.blind.chips * 2
                end

                if is_overkill then
                    card.ability.extra.overkill_achieved = true
                    if not card.ability.extra.overkill_notified then
                        card.ability.extra.overkill_notified = true
                        card_eval_status_text(card, 'extra', nil, nil, nil, {
                            message = "Overkill!",
                            colour = G.C.SECONDARY_SET.Spectral
                        })
                    end
                end
            end
        end

        -- Payout at end of round if Boss Blind is defeated and overkill was achieved
        if context.end_of_round and not context.individual and not context.repetition then
            if G.GAME.blind and G.GAME.blind.boss and card.ability.extra.overkill_achieved then
                if G.consumeables and G.consumeables.cards and G.consumeables.config and (#G.consumeables.cards + (G.GAME.consumeable_buffer or 0) < G.consumeables.config.card_limit) then
                    G.GAME.consumeable_buffer = (G.GAME.consumeable_buffer or 0) + 1
                    G.E_MANAGER:add_event(Event({
                        trigger = 'before',
                        delay = 0.0,
                        func = function()
                            local spectral = create_card('Spectral', G.consumeables, nil, nil, nil, nil, nil, 'overkill')
                            spectral:add_to_deck()
                            G.consumeables:emplace(spectral)
                            G.GAME.consumeable_buffer = 0
                            return true
                        end
                    }))
                    card_eval_status_text(card, 'extra', nil, nil, nil, {
                        message = localize('k_plus_spectral'),
                        colour = G.C.SECONDARY_SET.Spectral
                    })
                end
            end

            -- Reset overkill tracker for subsequent rounds
            if not context.blueprint then
                card.ability.extra.overkill_achieved = false
                card.ability.extra.overkill_notified = false
            end
        end
    end
}
