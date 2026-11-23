--- Wrong Schematics Joker
--- Blueprint/Brainstorm-style Joker.
--- Has a 1 in 2 chance to copy the Joker to the right, or Joker to the left.
--- When probability reaches 2 in 2 (e.g. Oops! All 6s), copies BOTH the left and right Jokers!

SMODS.Atlas {
    key = "wrong_schematics",
    path = "j_wrong_schematics.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "wrong_schematics",
    loc_txt = {
        name = "Wrong Schematics",
        text = {
            "{C:green}#1# in #2#{} chance to copy ability",
            "of Joker to the {C:attention}right{}, or",
            "Joker to the {C:attention}left{}"
        }
    },
    config = { extra = { odds = 2 } },
    rarity = 2, -- 1: Common, 2: Uncommon, 3: Rare, 4: Legendary
    cost = 7,
    blueprint_compat = true,
    atlas = "wrong_schematics",
    pos = { x = 0, y = 0 },
    loc_vars = function(self, info_queue, card)
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds
        return {
            vars = {
                (G.GAME and G.GAME.probabilities.normal) or 1,
                odds
            }
        }
    end,
    calculate = function(self, card, context)
        if not G.jokers or not G.jokers.cards then return end

        local my_pos = nil
        for i = 1, #G.jokers.cards do
            if G.jokers.cards[i] == card then
                my_pos = i
                break
            end
        end

        if not my_pos then return end

        local left_joker = G.jokers.cards[my_pos - 1]
        local right_joker = G.jokers.cards[my_pos + 1]

        local prob = (G.GAME and G.GAME.probabilities.normal) or 1
        local odds = (card and card.ability and card.ability.extra and card.ability.extra.odds) or self.config.extra.odds or 2

        if prob <= 0 then return end

        local targets = {}
        if prob >= odds then
            -- 2 in 2 or higher (e.g. Oops! All 6s): copy BOTH left and right!
            if left_joker and left_joker ~= card then
                table.insert(targets, left_joker)
            end
            if right_joker and right_joker ~= card then
                table.insert(targets, right_joker)
            end
        else
            -- 1 in 2: choose between right or left with 50/50 roll
            local roll_right = pseudorandom('wrong_schematics') < (prob / odds)
            local chosen = roll_right and right_joker or left_joker
            if chosen and chosen ~= card then
                table.insert(targets, chosen)
            end
        end

        if #targets == 0 then
            return
        elseif #targets == 1 then
            return SMODS.blueprint_effect(card, targets[1], context)
        else
            -- Multiple targets: copy both left and right Jokers in order
            local effects = {}
            for _, target in ipairs(targets) do
                local eff = SMODS.blueprint_effect(card, target, context)
                if eff then
                    table.insert(effects, eff)
                end
            end

            if #effects == 0 then
                return
            elseif #effects == 1 then
                return effects[1]
            else
                if SMODS.merge_effects then
                    return SMODS.merge_effects(effects)
                else
                    local ret = effects[1]
                    local cur = ret
                    for i = 2, #effects do
                        while cur.extra do
                            cur = cur.extra
                        end
                        cur.extra = effects[i]
                    end
                    return ret
                end
            end
        end
    end
}
