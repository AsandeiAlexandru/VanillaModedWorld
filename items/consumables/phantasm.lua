--- Phantasm Spectral Card
--- Removes all debuffs from cards currently held in hand.
--- Appears in shops, and does NOT appear in booster packs.

SMODS.Atlas {
    key = "c_phantasm",
    path = "c_phantasm.png",
    px = 71,
    py = 95
}

SMODS.Consumable {
    set = "Spectral",
    key = "phantasm",
    loc_txt = {
        name = "Phantasm",
        text = {
            "Removes all {C:red}debuffs{}",
            "from cards currently",
            "held in {C:attention}hand{}"
        }
    },
    config = {},
    loc_vars = function(self, info_queue, card)
        return { vars = {} }
    end,
    atlas = "c_phantasm",
    pos = { x = 0, y = 0 },
    cost = 4,
    can_use = function(self, card)
        return G.hand and G.hand.cards and #G.hand.cards > 0
    end,
    in_pool = function(self, args)
        -- Never appear in booster packs (Spectral packs, Arcana with Omen Globe, Buffoon, etc.)
        if args and args.source and type(args.source) == 'string' then
            if args.source == 'spe' or args.source == 'ar2' or args.source:find('pack') or args.source == 'buf' then
                return false
            end
            if args.source == 'sho' then
                return true
            end
        end
        if G.pack_cards and G.pack_cards.cards and #G.pack_cards.cards > 0 then
            return false
        end
        if G.STATES and G.STATE and (G.STATE == G.STATES.SPECTRAL_PACK or G.STATE == G.STATES.TAROT_PACK or G.STATE == G.STATES.PLANET_PACK or G.STATE == G.STATES.BUFFOON_PACK or G.STATE == G.STATES.STANDARD_PACK) then
            return false
        end
        return true
    end,
    use = function(self, card, area, copier)
        local used_card = copier or card

        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.4,
            func = function()
                play_sound('spectral1')
                used_card:juice_up(0.3, 0.5)
                return true
            end
        }))

        -- Flip hand cards face down
        if G.hand and G.hand.cards then
            for i = 1, #G.hand.cards do
                local percent = 1.15 - (i - 0.999) / (#G.hand.cards - 0.998) * 0.3
                local hand_card = G.hand.cards[i]
                G.E_MANAGER:add_event(Event({
                    trigger = 'after',
                    delay = 0.08,
                    func = function()
                        hand_card:flip()
                        play_sound('card1', percent)
                        hand_card:juice_up(0.3, 0.3)
                        return true
                    end
                }))
            end
        end

        delay(0.2)

        -- Remove all debuffs from hand cards and protect them
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.1,
            func = function()
                if G.hand and G.hand.cards then
                    for i = 1, #G.hand.cards do
                        local hand_card = G.hand.cards[i]
                        hand_card.ability.debuff_sources = hand_card.ability.debuff_sources or {}
                        hand_card.ability.debuff_sources['phantasm'] = 'prevent_debuff'
                        hand_card:set_debuff(false)
                        hand_card.debuff = false
                        hand_card.debuffed_by_blind = false
                    end
                end
                return true
            end
        }))

        -- Flip hand cards back face up with audio & juice
        if G.hand and G.hand.cards then
            for i = 1, #G.hand.cards do
                local percent = 0.85 + (i - 0.999) / (#G.hand.cards - 0.998) * 0.3
                local hand_card = G.hand.cards[i]
                G.E_MANAGER:add_event(Event({
                    trigger = 'after',
                    delay = 0.08,
                    func = function()
                        hand_card:flip()
                        play_sound('tarot2', percent, 0.6)
                        hand_card:juice_up(0.3, 0.3)
                        return true
                    end
                }))
            end
        end

        delay(0.5)
    end
}

-- Hook get_current_pool to allow Phantasm to appear in shop consumable slots even on non-Ghost decks
local get_current_pool_ref = get_current_pool
function get_current_pool(_type, _rarity, _legendary, _append)
    local pool, pool_key = get_current_pool_ref(_type, _rarity, _legendary, _append)
    if _type == 'Tarot' and _append == 'sho' then
        local has_phantasm = false
        if G.consumeables and G.consumeables.cards then
            for _, c in ipairs(G.consumeables.cards) do
                if c.config and c.config.center_key == 'c_vmw_phantasm' then
                    has_phantasm = true
                    break
                end
            end
        end
        if G.shop_jokers and G.shop_jokers.cards then
            for _, c in ipairs(G.shop_jokers.cards) do
                if c.config and c.config.center_key == 'c_vmw_phantasm' then
                    has_phantasm = true
                    break
                end
            end
        end
        if (not has_phantasm or (SMODS.showman and SMODS.showman('c_vmw_phantasm'))) and not (G.GAME and G.GAME.banned_keys and G.GAME.banned_keys['c_vmw_phantasm']) then
            table.insert(pool, 'c_vmw_phantasm')
        end
    end
    return pool, pool_key
end
