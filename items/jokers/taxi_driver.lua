--- Taxi Driver Joker
--- Rare Joker
--- Earn $1 for each scoring card (when hand is scored).

SMODS.Atlas {
    key = "j_taxi_driver",
    path = "j_taxi_driver.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    name = "Taxi Driver",
    key = "taxi_driver",
    atlas = "j_taxi_driver",
    pos = { x = 0, y = 0 },
    rarity = 3, -- Rare
    cost = 8,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = { extra = { dollars = 1 } },
    loc_txt = {
        name = "Taxi Driver",
        text = {
            "Earn {C:money}$#1#{} for each",
            "{C:attention}scoring card{}",
            "{C:inactive}(when hand is scored){}"
        }
    },
    loc_vars = function(self, info_queue, card)
        local dollars = (card and card.ability and card.ability.extra and card.ability.extra.dollars) or self.config.extra.dollars
        return { vars = { dollars } }
    end,
    calculate = function(self, card, context)
        if context.joker_main then
            local count = (context.scoring_hand and #context.scoring_hand) or 0
            local per_card = (card and card.ability and card.ability.extra and card.ability.extra.dollars) or 1
            local total_dollars = count * per_card
            if total_dollars > 0 then
                return {
                    dollars = total_dollars,
                    card = card
                }
            end
        end
    end
}
