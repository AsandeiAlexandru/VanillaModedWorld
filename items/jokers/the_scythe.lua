--- The Scythe (Rare Joker)
--- If first hand of the round has exactly 3 cards,
--- destroys the 2 outer side cards and creates a copy of the middle card in hand.

SMODS.Atlas {
    key = "the_scythe",
    path = "j_the_scythe.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "the_scythe",
    loc_txt = {
        name = "The Scythe",
        text = {
            "If {C:attention}first hand{} has exactly {C:attention}3{} cards,",
            "{C:red}destroy{} the {C:attention}2{} side cards and",
            "add a copy of the {C:attention}middle{} card to hand"
        }
    },
    rarity = 3, -- 1: Common, 2: Uncommon, 3: Rare, 4: Legendary
    cost = 8,
    blueprint_compat = true,
    atlas = "the_scythe",
    pos = { x = 0, y = 0 },
    calculate = function(self, card, context)
        -- Trigger on first hand of round when exactly 3 cards are played
        if context.before and G.GAME.current_round.hands_played == 0 and context.full_hand and #context.full_hand == 3 then
            card.ability.scythe_mid = context.full_hand[2]
            card.ability.scythe_left = context.full_hand[1]
            card.ability.scythe_right = context.full_hand[3]
            card.ability.left_destroyed = false
            card.ability.right_destroyed = false

            -- Create permanent copy of middle card into deck and hand (DNA mechanic)
            G.playing_card = (G.playing_card and G.playing_card + 1) or 1
            local _copied = copy_card(card.ability.scythe_mid, nil, nil, G.playing_card)
            _copied:add_to_deck()
            G.deck.config.card_limit = G.deck.config.card_limit + 1
            table.insert(G.playing_cards, _copied)
            G.hand:emplace(_copied)
            _copied.states.visible = nil

            G.E_MANAGER:add_event(Event({
                func = function()
                    play_sound('tarot1')
                    card:juice_up(0.4, 0.4)
                    _copied:juice_up(0.3, 0.3)
                    return true
                end
            }))

            card_eval_status_text(card, 'extra', nil, nil, nil, {
                message = "Reaped!",
                colour = G.C.DARK_EDITION
            })
        end

        -- Destroy outer cards during scoring
        if context.destroying_card and not context.blueprint then
            if card.ability.scythe_left and context.destroying_card == card.ability.scythe_left then
                card.ability.left_destroyed = true
                return true
            end
            if card.ability.scythe_right and context.destroying_card == card.ability.scythe_right then
                card.ability.right_destroyed = true
                return true
            end
        end

        -- In case an outer card was not part of scoring_hand (e.g. Pair or High Card in 3-card hand),
        -- destroy it after scoring so both side cards are always reaped!
        if context.after and not context.blueprint then
            local function reap_card(c)
                if c and not c.destroyed then
                    c.destroyed = true
                    G.E_MANAGER:add_event(Event({
                        trigger = 'after',
                        delay = 0.1,
                        func = function()
                            c:start_dissolve()
                            return true
                        end
                    }))
                    for i = #G.playing_cards, 1, -1 do
                        if G.playing_cards[i] == c then
                            table.remove(G.playing_cards, i)
                            break
                        end
                    end
                end
            end

            if card.ability.scythe_left and not card.ability.left_destroyed then
                reap_card(card.ability.scythe_left)
                card.ability.left_destroyed = true
            end
            if card.ability.scythe_right and not card.ability.right_destroyed then
                reap_card(card.ability.scythe_right)
                card.ability.right_destroyed = true
            end

            -- Clean up references
            card.ability.scythe_mid = nil
            card.ability.scythe_left = nil
            card.ability.scythe_right = nil
        end

        -- Reset state at end of round
        if context.end_of_round then
            card.ability.scythe_mid = nil
            card.ability.scythe_left = nil
            card.ability.scythe_right = nil
            card.ability.left_destroyed = nil
            card.ability.right_destroyed = nil
        end
    end
}
