--- The Weakness Tarot Card
--- Exact counterpart to vanilla "Strength" (c_strength).
--- Decreases the rank of up to 2 selected cards by 1.

SMODS.Atlas {
    key = "weakness",
    path = "c_weakness.png",
    px = 71,
    py = 95
}

SMODS.Consumable {
    set = "Tarot",
    key = "weakness",
    loc_txt = {
        name = "The Weakness",
        text = {
            "Decreases rank of",
            "up to {C:attention}#1#{} selected",
            "cards by {C:attention}1{}"
        }
    },
    config = { max_highlighted = 2 },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.max_highlighted } }
    end,
    atlas = "weakness",
    pos = { x = 0, y = 0 },
    cost = 3,
    can_use = function(self, card)
        return G.hand and G.hand.highlighted and #G.hand.highlighted >= 1 and #G.hand.highlighted <= self.config.max_highlighted
    end,
    use = function(self, card, area, copier)
        local used_tarot = copier or card
        if not G.hand or not G.hand.highlighted then return end
        local targets = {}
        for i = 1, #G.hand.highlighted do
            if G.hand.highlighted[i] then
                targets[#targets + 1] = G.hand.highlighted[i]
            end
        end
        if #targets == 0 then return end

        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.4,
            func = function()
                play_sound('tarot1')
                used_tarot:juice_up(0.3, 0.5)
                return true
            end
        }))

        -- Flip cards face down
        for i = 1, #targets do
            local percent = 1.15 - (i - 0.999) / (#targets - 0.998) * 0.3
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    if targets[i] then
                        targets[i]:flip()
                        play_sound('card1', percent)
                        targets[i]:juice_up(0.3, 0.3)
                    end
                    return true
                end
            }))
        end

        delay(0.2)

        -- Decrease rank by 1 (2 wraps to Ace 14)
        for i = 1, #targets do
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.1,
                func = function()
                    local c = targets[i]
                    if c and c.base and c.base.id then
                        local suit_prefix = string.sub(c.base.suit, 1, 1) .. '_'
                        local rank_suffix = c.base.id == 2 and 14 or (c.base.id - 1)
                        if rank_suffix < 10 then
                            rank_suffix = tostring(rank_suffix)
                        elseif rank_suffix == 10 then
                            rank_suffix = 'T'
                        elseif rank_suffix == 11 then
                            rank_suffix = 'J'
                        elseif rank_suffix == 12 then
                            rank_suffix = 'Q'
                        elseif rank_suffix == 13 then
                            rank_suffix = 'K'
                        elseif rank_suffix == 14 then
                            rank_suffix = 'A'
                        end
                        if G.P_CARDS and G.P_CARDS[suit_prefix .. rank_suffix] then
                            c:set_base(G.P_CARDS[suit_prefix .. rank_suffix])
                        end
                    end
                    return true
                end
            }))
        end

        -- Flip cards face up
        for i = 1, #targets do
            local percent = 0.85 + (i - 0.999) / (#targets - 0.998) * 0.3
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    if targets[i] then
                        targets[i]:flip()
                        play_sound('tarot2', percent, 0.6)
                        targets[i]:juice_up(0.3, 0.3)
                    end
                    return true
                end
            }))
        end

        -- Unhighlight
        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.2,
            func = function()
                if G.hand and G.hand.unhighlight_all then
                    G.hand:unhighlight_all()
                end
                return true
            end
        }))
    end
}
