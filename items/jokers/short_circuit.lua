--- Short Circuit Joker
--- Common Joker ($4)
--- If a card is retriggered, has a 1 in 2 chance to retrigger its neighbors as well.

SMODS.Atlas {
    key = "j_short_circuit",
    path = "j_short_circuit.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Short Circuit",
    key = "short_circuit",
    atlas = "j_short_circuit",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { odds = 2 } },
    set_ability = function(self, card, initial, delay_sprites)
        card.ability.extra = { odds = 2 }
        card.ability.extra_reps = {}
    end,
    loc_vars = function(self, info_queue, card)
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds
        return { vars = { '' .. (G.GAME and G.GAME.probabilities.normal or 1), odds } }
    end,
    loc_txt = {
        name = "Short Circuit",
        text = {
            "If a card is {C:attention}retriggered{},",
            "has a {C:green}#1# in #2#{} chance to",
            "retrigger its {C:attention}neighbors{} as well"
        }
    },
    calculate = function(self, card, context)
        -- Before scoring starts, identify retriggering cards and roll spark jumps to neighbors
        if context.before then
            card.ability.extra_reps = {}
            if context.scoring_hand and #context.scoring_hand > 1 then
                local retriggered_indices = {}

                -- Inspect each card in scoring hand for retriggering effects
                for i, c in ipairs(context.scoring_hand) do
                    local is_retriggered = false
                    -- 1. Red Seal
                    if c.seal == 'Red' then
                        is_retriggered = true
                    end
                    -- 2. Other owned Jokers
                    if not is_retriggered and G.jokers and G.jokers.cards then
                        for _, j in ipairs(G.jokers.cards) do
                            if j ~= card and j.ability and j.ability.set == 'Joker' then
                                local ret = j:calculate_joker({
                                    repetition = true,
                                    cardarea = G.play,
                                    other_card = c,
                                    scoring_hand = context.scoring_hand
                                })
                                if ret and ret.repetitions and ret.repetitions > 0 then
                                    is_retriggered = true
                                    break
                                end
                            end
                        end
                    end

                    if is_retriggered then
                        retriggered_indices[#retriggered_indices + 1] = i
                    end
                end

                -- For each retriggered card, roll odds to jump to left/right neighbors
                -- Capped at at most 1 spark per neighbor side (max +2 per card) to prevent runaway loops
                for _, idx in ipairs(retriggered_indices) do
                    for _, nbr_idx in ipairs({ idx - 1, idx + 1 }) do
                        if nbr_idx >= 1 and nbr_idx <= #context.scoring_hand then
                            if pseudorandom('short_circuit') < G.GAME.probabilities.normal / card.ability.extra.odds then
                                local nbr_card = context.scoring_hand[nbr_idx]
                                card.ability.extra_reps[nbr_card] = math.min((card.ability.extra_reps[nbr_card] or 0) + 1, 2)
                            end
                        end
                    end
                end
            end
        end

        -- During card repetition phase, award the extra retriggers to neighbor cards
        if context.repetition and context.cardarea == G.play then
            if card.ability.extra_reps and card.ability.extra_reps[context.other_card] and card.ability.extra_reps[context.other_card] > 0 then
                local reps = card.ability.extra_reps[context.other_card]
                card.ability.extra_reps[context.other_card] = 0 -- consume
                return {
                    message = "Zzzzt!",
                    repetitions = reps,
                    card = card
                }
            end
        end

        -- Clean up at end of round
        if context.end_of_round then
            card.ability.extra_reps = {}
        end
    end
}
