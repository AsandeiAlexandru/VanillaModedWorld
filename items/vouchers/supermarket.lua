--- Supermarket (Tier 2 Voucher)
--- Requires Market.
--- +1 Voucher slot available in shop.

SMODS.Atlas {
    key = "v_supermarket",
    path = "v_supermarket.png",
    px = 71,
    py = 95
}

SMODS.Voucher {
    key = "supermarket",
    atlas = "v_supermarket",
    pos = { x = 0, y = 0 },
    cost = 10,
    unlocked = true,
    discovered = true,
    requires = { "v_vmw_market" },
    config = { extra = 1 },
    loc_txt = {
        name = "Supermarket",
        text = {
            "{C:attention}+#1#{} Voucher slot",
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
                SMODS.change_voucher_limit(1)
                -- SlotManager mod compatibility: update SlotManager's cached limit and stock
                if SMODS.Mods and SMODS.Mods["SlotManager"] and SMODS.Mods["SlotManager"].config then
                    local sm_cfg = SMODS.Mods["SlotManager"].config
                    local expected = (G.GAME.starting_params and G.GAME.starting_params.vouchers_in_shop or 1) + (G.GAME.modifiers.extra_vouchers or 0)
                    sm_cfg.shop_vouchers = math.max(sm_cfg.shop_vouchers or 1, expected)
                    if G.GAME and G.GAME.slot_control_stock then
                        G.GAME.slot_control_stock.voucher_limit = sm_cfg.shop_vouchers
                    end
                end
                return true
            end
        }))
    end
}
