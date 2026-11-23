--- Market (Tier 1 Voucher)
--- +1 Booster Pack slot available in shop.

SMODS.Atlas {
    key = "v_market",
    path = "v_market.png",
    px = 71,
    py = 95
}

SMODS.Voucher {
    key = "market",
    atlas = "v_market",
    pos = { x = 0, y = 0 },
    cost = 10,
    unlocked = true,
    discovered = true,
    config = { extra = 1 },
    loc_txt = {
        name = "Market",
        text = {
            "{C:attention}+#1#{} Booster Pack slot",
            "available in shop"
        }
    },
    loc_vars = function(self, info_queue, card)
        local extra = (card and card.ability and card.ability.extra) or self.config.extra
        return { vars = { extra } }
    end,
    redeem = function(self, card)
        G.E_MANAGER:add_event(Event({
            func = function()
                SMODS.change_booster_limit(1)
                return true
            end
        }))
    end
}
