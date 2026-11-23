--- The Mirror Tarot Card
--- Converts the left card into the rank and suit of the right card (preserving enhancements, editions, and seals on the left card).

SMODS.Atlas {
    key = "the_mirror",
    path = "c_the_mirror.png",
    px = 71,
    py = 95
}

SMODS.Consumable {
    set = "Tarot",
    key = "the_mirror",
    loc_txt = {
        name = "The Mirror",
        text = {
            "Select {C:attention}#1#{} cards,",
            "convert the {C:attention}left{} card into the",
            "{C:attention}rank{} and {C:attention}suit{} of the {C:attention}right{} card",
            "{C:inactive}(Drag to rearrange){}"
        }
    },
    config = { max_highlighted = 2 },
    loc_vars = function(self, info_queue, card)
        return { vars = { self.config.max_highlighted } }
    end,
    atlas = "the_mirror",
    pos = { x = 0, y = 0 },
    cost = 3,
    can_use = function(self, card)
        return G.hand and G.hand.highlighted and #G.hand.highlighted == self.config.max_highlighted
    end,
    use = function(self, card, area, copier)
        local used_tarot = copier or card
        if not G.hand or not G.hand.highlighted or #G.hand.highlighted < 2 then return end
        local rightmost = G.hand.highlighted[1]
        local leftmost = G.hand.highlighted[2]
        if not rightmost or not leftmost then return end
        if leftmost.T.x > rightmost.T.x then
            leftmost, rightmost = rightmost, leftmost
        end
        local target_cards = { leftmost, rightmost }

        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.4,
            func = function()
                play_sound('tarot1')
                used_tarot:juice_up(0.3, 0.5)
                return true
            end
        }))

        for i = 1, #target_cards do
            local percent = 1.15 - (i - 0.999) / (#target_cards - 0.998) * 0.3
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    if target_cards[i] then
                        target_cards[i]:flip()
                        play_sound('card1', percent)
                        target_cards[i]:juice_up(0.3, 0.3)
                    end
                    return true
                end
            }))
        end

        delay(0.2)

        G.E_MANAGER:add_event(Event({
            trigger = 'after',
            delay = 0.1,
            func = function()
                if leftmost and rightmost and rightmost.config and rightmost.config.card then
                    leftmost:set_base(rightmost.config.card)
                end
                return true
            end
        }))

        for i = 1, #target_cards do
            local percent = 0.85 + (i - 0.999) / (#target_cards - 0.998) * 0.3
            G.E_MANAGER:add_event(Event({
                trigger = 'after',
                delay = 0.15,
                func = function()
                    if target_cards[i] then
                        target_cards[i]:flip()
                        play_sound('tarot2', percent, 0.6)
                        target_cards[i]:juice_up(0.3, 0.3)
                    end
                    return true
                end
            }))
        end

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
        delay(0.5)
    end
}
