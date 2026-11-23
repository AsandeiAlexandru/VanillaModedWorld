--- River Joker
--- Rare Joker
--- Adds the Chips and Mult of the poker hand held in hand when hand is scored.
--- Full-surface card art depicting a scenic mountain valley with flowing river.

SMODS.Atlas {
    key = "j_river",
    path = "j_river.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "River",
    key = "river",
    atlas = "j_river",
    pos = { x = 0, y = 0 },
    rarity = 3, -- Rare
    cost = 8,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    loc_txt = {
        name = "River",
        text = {
            "Adds the {C:chips}Chips{} and {C:mult}Mult{}",
            "of the poker hand held",
            "in {C:attention}hand{} to scoring",
            "{C:inactive}(Currently {C:attention}#1#{}{C:inactive}: {C:chips}+#2#{} {C:inactive}Chips, {C:mult}+#3#{} {C:inactive}Mult){}"
        }
    },
    loc_vars = function(self, info_queue, card)
        local hand_name = "None"
        local chips = 0
        local mult = 0
        if G.hand and G.hand.cards and #G.hand.cards > 0 and G.FUNCS and G.FUNCS.get_poker_hand_info and G.GAME and G.GAME.hands then
            local text, loc_disp_text = G.FUNCS.get_poker_hand_info(G.hand.cards)
            if text and text ~= 'NULL' and G.GAME.hands[text] then
                hand_name = loc_disp_text or text
                chips = G.GAME.hands[text].chips or 0
                mult = G.GAME.hands[text].mult or 0
            end
        end
        return { vars = { hand_name, chips, mult } }
    end,
    calculate = function(self, card, context)
        if context.joker_main then
            if G.hand and G.hand.cards and #G.hand.cards > 0 and G.FUNCS and G.FUNCS.get_poker_hand_info and G.GAME and G.GAME.hands then
                local text, loc_disp_text = G.FUNCS.get_poker_hand_info(G.hand.cards)
                if text and text ~= 'NULL' and G.GAME.hands[text] then
                    local hand_data = G.GAME.hands[text]
                    local chips_to_add = hand_data.chips or 0
                    local mult_to_add = hand_data.mult or 0

                    if chips_to_add > 0 or mult_to_add > 0 then
                        card_eval_status_text(context.blueprint_card or card, 'extra', nil, nil, nil, {
                            message = loc_disp_text or text,
                            colour = G.C.CHIPS
                        })
                        return {
                            chips = chips_to_add,
                            mult = mult_to_add,
                            card = card
                        }
                    end
                end
            end
        end
    end
}
