--- Spotlight Joker
--- Common Joker ($4)
--- If played hand is a 5-card High Card, the scoring card becomes Enhanced.
--- Can also gain an Edition or Seal through the upgrade pools.

SMODS.Atlas {
    key = "j_spotlight",
    path = "j_spotlight.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Spotlight",
    key = "spotlight",
    atlas = "j_spotlight",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    loc_txt = {
        name = "Spotlight",
        text = {
            "If played hand is a {C:attention}5-card High Card{},",
            "{C:attention}randomizes{} the scoring card's",
            "{C:attention}Enhancement{}, {C:dark_edition}Edition{}, and {C:attention}Seal{}"
        }
    },
    calculate = function(self, card, context)
        -- Triggers before scoring when playing a 5-card High Card
        if context.before and not context.blueprint then
            if context.scoring_name == "High Card" and context.full_hand and #context.full_hand == 5 and context.scoring_hand and #context.scoring_hand > 0 then
                local target = context.scoring_hand[1]
                local changed = false

                -- 1. Enhancement Pool (Pass removes existing enhancement)
                local enhancement_pool = {
                    'm_bonus',
                    'm_mult',
                    'm_wild',
                    'm_glass',
                    'm_steel',
                    'm_gold',
                    'm_lucky',
                    'm_stone',
                    'pass'
                }
                local chosen_enh = pseudorandom_element(enhancement_pool, pseudoseed('spotlight_enh'))
                if chosen_enh ~= 'pass' and G.P_CENTERS[chosen_enh] then
                    target:set_ability(G.P_CENTERS[chosen_enh])
                    changed = true
                elseif chosen_enh == 'pass' and target.config.center ~= G.P_CENTERS.c_base then
                    target:set_ability(G.P_CENTERS.c_base)
                    changed = true
                end

                -- 2. Edition Pool (Pass removes existing edition)
                local edition_pool = {
                    'foil',
                    'holo',
                    'polychrome',
                    'pass', 'pass', 'pass', 'pass', 'pass', 'pass', 'pass', 'pass', 'pass'
                }
                local chosen_ed = pseudorandom_element(edition_pool, pseudoseed('spotlight_ed'))
                if chosen_ed ~= 'pass' then
                    target:set_edition({ [chosen_ed] = true }, true)
                    changed = true
                elseif chosen_ed == 'pass' and target.edition then
                    target:set_edition(nil, true)
                    changed = true
                end

                -- 3. Seal Pool (Pass removes existing seal)
                local seal_pool = {
                    'Red',
                    'Blue',
                    'Gold',
                    'Purple',
                    'pass', 'pass', 'pass', 'pass', 'pass', 'pass'
                }
                local chosen_seal = pseudorandom_element(seal_pool, pseudoseed('spotlight_seal'))
                if chosen_seal ~= 'pass' then
                    target:set_seal(chosen_seal, nil, true)
                    changed = true
                elseif chosen_seal == 'pass' and target.seal then
                    target:set_seal(nil, nil, true)
                    changed = true
                end

                if changed then
                    G.E_MANAGER:add_event(Event({
                        func = function()
                            play_sound('tarot1')
                            target:juice_up(0.6, 0.6)
                            card:juice_up(0.4, 0.4)
                            return true
                        end
                    }))
                    card_eval_status_text(card, 'extra', nil, nil, nil, {
                        message = "Randomized!",
                        colour = G.C.GOLD
                    })
                end
            end
        end
    end
}
