--- Stone Tablet Joker
--- Common Joker
--- If a Stone Card has a Seal, retriggers (doubles) the seal's effect.

local function is_stone(c)
    return c and ((SMODS.has_enhancement and SMODS.has_enhancement(c, 'm_stone'))
        or (c.ability and (c.ability.name == 'Stone Card' or c.ability.effect == 'Stone Card'))
        or (c.config and c.config.center == G.P_CENTERS.m_stone))
end

SMODS.Atlas {
    key = "j_stone_tablet",
    path = "j_stone_tablet.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Stone Tablet",
    key = "stone_tablet",
    atlas = "j_stone_tablet",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "Stone Tablet",
        text = {
            "Retrigger all {C:attention}Seals{}",
            "on {C:attention}Stone Cards{}",
            "{C:inactive}(doubles their effects){}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_stone
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        -- 1. Red Seal (Retrigger card during scoring or held-in-hand scoring)
        if context.repetition and (context.cardarea == G.play or context.cardarea == G.hand) then
            if is_stone(context.other_card) and context.other_card.seal == 'Red' then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = card
                }
            end
        end

        -- 2. Gold Seal (Earn an extra $3 when scored)
        if context.individual and context.cardarea == G.play then
            if is_stone(context.other_card) and context.other_card.seal == 'Gold' then
                return {
                    dollars = 3,
                    card = card
                }
            end
        end

        -- 3. Purple Seal (Creates a Tarot card when discarded)
        if context.discard and not context.other_card.debuff then
            if is_stone(context.other_card) and context.other_card.seal == 'Purple' then
                if G.consumeables and G.consumeables.cards and G.consumeables.config and (#G.consumeables.cards + (G.GAME.consumeable_buffer or 0) < G.consumeables.config.card_limit) then
                    G.GAME.consumeable_buffer = (G.GAME.consumeable_buffer or 0) + 1
                    G.E_MANAGER:add_event(Event({
                        trigger = 'before',
                        delay = 0.0,
                        func = (function()
                            local card_tarot = create_card('Tarot', G.consumeables, nil, nil, nil, nil, nil, 'st_tab')
                            card_tarot:add_to_deck()
                            G.consumeables:emplace(card_tarot)
                            G.GAME.consumeable_buffer = 0
                            return true
                        end)
                    }))
                    card_eval_status_text(context.blueprint_card or card, 'extra', nil, nil, nil, {
                        message = localize('k_plus_tarot'),
                        colour = G.C.PURPLE
                    })
                    return {
                        card = card
                    }
                end
            end
        end

        -- 4. Blue Seal (Creates a Planet card for final played poker hand at end of round)
        if context.end_of_round and context.individual and context.cardarea == G.hand and not context.other_card.debuff then
            if is_stone(context.other_card) and context.other_card.seal == 'Blue' then
                if G.consumeables and G.consumeables.cards and G.consumeables.config and (#G.consumeables.cards + (G.GAME.consumeable_buffer or 0) < G.consumeables.config.card_limit) then
                    local card_type = 'Planet'
                    G.GAME.consumeable_buffer = (G.GAME.consumeable_buffer or 0) + 1
                    G.E_MANAGER:add_event(Event({
                        trigger = 'before',
                        delay = 0.0,
                        func = (function()
                            if G.GAME.last_hand_played then
                                local _planet = 0
                                for k, v in pairs(G.P_CENTER_POOLS.Planet) do
                                    if v.config.hand_type == G.GAME.last_hand_played then
                                        _planet = v.key
                                    end
                                end
                                local card_planet = create_card(card_type, G.consumeables, nil, nil, nil, nil, _planet, 'st_tab_blu')
                                card_planet:add_to_deck()
                                G.consumeables:emplace(card_planet)
                                G.GAME.consumeable_buffer = 0
                            end
                            return true
                        end)
                    }))
                    card_eval_status_text(context.blueprint_card or card, 'extra', nil, nil, nil, {
                        message = localize('k_plus_planet'),
                        colour = G.C.SECONDARY_SET.Planet
                    })
                    return {
                        card = card
                    }
                end
            end
        end

        -- 5. Fallback for custom / modded seals
        if is_stone(context.other_card) and context.other_card.seal and context.other_card.calculate_seal then
            local s = context.other_card.seal
            if s ~= 'Red' and s ~= 'Gold' and s ~= 'Purple' and s ~= 'Blue' then
                local res = context.other_card:calculate_seal(context)
                if res then
                    res.card = card
                    return res
                end
            end
        end
    end
}
