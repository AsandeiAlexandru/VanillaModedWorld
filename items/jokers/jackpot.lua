--- Jackpot Joker
--- Uncommon Joker
--- If played hand contains at least 3 scoring 7s, each scored 7 gives $6.

SMODS.Atlas {
    key = "j_jackpot",
    path = "j_jackpot.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Jackpot",
    key = "jackpot",
    atlas = "j_jackpot",
    pos = { x = 0, y = 0 },
    rarity = 2, -- Uncommon
    cost = 6,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { min_sevens = 3, dollars = 7 } },
    loc_txt = {
        name = "Jackpot",
        text = {
            "If played hand contains",
            "at least {C:attention}#1#{} scoring {C:attention}7s{},",
            "each scored {C:attention}7{} gives",
            "{C:money}$#2#{}"
        }
    },
    loc_vars = function(self, info_queue, card)
        local min_sevens = (card and card.ability and card.ability.extra and card.ability.extra.min_sevens) or self.config.extra.min_sevens
        local dollars = (card and card.ability and card.ability.extra and card.ability.extra.dollars) or self.config.extra.dollars
        return { vars = { min_sevens, dollars } }
    end,
    calculate = function(self, card, context)
        -- Trigger individually on each scored card
        if context.individual and context.cardarea == G.play then
            local sevens = 0
            if context.scoring_hand then
                for _, other in ipairs(context.scoring_hand) do
                    if other:get_id() == 7 then
                        sevens = sevens + 1
                    end
                end
            end

            if sevens >= card.ability.extra.min_sevens and context.other_card:get_id() == 7 then
                G.GAME.dollar_buffer = (G.GAME.dollar_buffer or 0) + card.ability.extra.dollars
                G.E_MANAGER:add_event(Event({
                    func = function()
                        G.GAME.dollar_buffer = 0
                        return true
                    end
                }))
                return {
                    dollars = card.ability.extra.dollars,
                    card = card
                }
            end
        end
    end
}
