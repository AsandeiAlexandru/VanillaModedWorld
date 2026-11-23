--- The Bell Joker
--- Uncommon Joker
--- Played cards retrigger based on how far they are from the margin of the played hand (Gaussian / Bell curve).
--- 5 cards: [ +0, +1, +2, +1, +0 ]
--- 4 cards: [ +0, +1, +1, +0 ]
--- 3 cards: [ +0, +1, +0 ]
--- 2 cards: [ +0, +0 ]
--- 1 card:  [ +0 ]

SMODS.Atlas {
    key = "j_the_bell",
    path = "j_the_bell.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "The Bell",
    key = "the_bell",
    atlas = "j_the_bell",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "The Bell",
        text = {
            "Scoring cards are {C:attention}retriggered{}",
            "based on distance from margins",
            "{C:inactive}(ex: 5 cards -> +0, +1, +2, +1, +0){}"
        }
    },
    calculate = function(self, card, context)
        if context.repetition and context.cardarea == G.play then
            if context.scoring_hand and #context.scoring_hand > 0 then
                local idx = nil
                for i, other in ipairs(context.scoring_hand) do
                    if other == context.other_card then
                        idx = i
                        break
                    end
                end

                if idx then
                    local n = #context.scoring_hand
                    local reps = math.min(idx - 1, n - idx)
                    if reps > 0 then
                        return {
                            message = localize('k_again_ex'),
                            repetitions = reps,
                            card = card
                        }
                    end
                end
            end
        end
    end
}
