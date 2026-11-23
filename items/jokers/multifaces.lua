--- MultiFaces Joker
--- Uncommon Joker
--- Converts played 2s into Jacks, 3s into Queens, and 4s into Kings when played.

SMODS.Atlas {
    key = "j_multifaces",
    path = "j_multifaces.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "MultiFaces",
    key = "multifaces",
    atlas = "j_multifaces",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "MultiFaces",
        text = {
            "Converts played {C:attention}2s{} into {C:attention}Jacks{},",
            "{C:attention}3s{} into {C:attention}Queens{}, and",
            "{C:attention}4s{} into {C:attention}Kings{} when played"
        }
    },
    calculate = function(self, card, context)
        if context.before and not context.blueprint then
            local targets = {}
            for _, played_card in ipairs(context.full_hand or context.scoring_hand) do
                local id = played_card:get_id()
                local target_rank = nil
                if id == 2 then
                    target_rank = 'Jack'
                elseif id == 3 then
                    target_rank = 'Queen'
                elseif id == 4 then
                    target_rank = 'King'
                end

                if target_rank then
                    table.insert(targets, { card = played_card, rank = target_rank })
                end
            end

            if #targets > 0 then
                for _, t in ipairs(targets) do
                    G.E_MANAGER:add_event(Event({
                        trigger = 'after',
                        delay = 0.15,
                        func = function()
                            t.card:flip()
                            play_sound('card1')
                            t.card:juice_up(0.3, 0.3)
                            return true
                        end
                    }))
                    G.E_MANAGER:add_event(Event({
                        trigger = 'after',
                        delay = 0.15,
                        func = function()
                            SMODS.change_base(t.card, nil, t.rank)
                            t.card:flip()
                            play_sound('tarot2')
                            t.card:juice_up(0.4, 0.4)
                            return true
                        end
                    }))
                end

                return {
                    message = localize('k_upgrade_ex'),
                    colour = G.C.MULT,
                    card = card
                }
            end
        end
    end
}
