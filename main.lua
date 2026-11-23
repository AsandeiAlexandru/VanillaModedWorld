--- STEAMODDED HEADER
--- !MOD_NAME: Vanilla Moded World
--- !MOD_ID: VanillaModedWorld
--- !MOD_AUTHOR: [User]
--- !MOD_DESCRIPTION: A vanilla-style expansion adding new Jokers, Tarots, and more.
--- !PREFIX: vmw
--- !VERSION: 0.1.0

-- Optional SMODS features
SMODS.optional_features = SMODS.optional_features or {}
SMODS.optional_features.retrigger_joker = true

-- Mod icon atlas (shows in the Mods menu)
SMODS.Atlas {
    key = "modicon",
    path = "icon.png",
    px = 32,
    py = 32
}

-- Safe loader helper
local function load_item(path)
    local func, err = SMODS.load_file(path)
    if err then
        print("[VanillaModedWorld ERROR] Failed to load " .. path .. ": " .. tostring(err))
    else
        func()
        print("[VanillaModedWorld] Successfully loaded: " .. path)
    end
end

-- Load Jokers
load_item("items/jokers/espresso.lua")
load_item("items/jokers/double_espresso.lua")
load_item("items/jokers/the_bell.lua")
load_item("items/jokers/wrong_schematics.lua")
load_item("items/jokers/magifect.lua")
load_item("items/jokers/stanczyk.lua")
load_item("items/jokers/doubler.lua")
load_item("items/jokers/burnt_offering.lua")
load_item("items/jokers/jackpot.lua")
load_item("items/jokers/lucky_clover.lua")
load_item("items/jokers/multifaces.lua")
load_item("items/jokers/bonus_stage.lua")
load_item("items/jokers/overdrive.lua")
load_item("items/jokers/kaleidoscope.lua")
load_item("items/jokers/glassblower.lua")
load_item("items/jokers/the_anvil.lua")
load_item("items/jokers/monolith.lua")
load_item("items/jokers/bullion.lua")
load_item("items/jokers/golden_horseshoe.lua")
load_item("items/jokers/fortune_cookie.lua")
load_item("items/jokers/hot_pepper.lua")
load_item("items/jokers/the_scythe.lua")
load_item("items/jokers/antivirus.lua")
load_item("items/jokers/sommers.lua")
load_item("items/jokers/taxi_driver.lua")
load_item("items/jokers/river.lua")
load_item("items/jokers/stone_tablet.lua")
load_item("items/jokers/overkill.lua")
load_item("items/jokers/spotlight.lua")
load_item("items/jokers/short_circuit.lua")
load_item("items/jokers/sphene.lua")
load_item("items/jokers/ruby_heart.lua")
load_item("items/jokers/black_diamond.lua")
load_item("items/jokers/emerald.lua")
load_item("items/jokers/sticky_note.lua")
load_item("items/jokers/camera.lua")
load_item("items/jokers/frugal_joker.lua")
load_item("items/jokers/fickle_joker.lua")
load_item("items/jokers/stoic_joker.lua")
load_item("items/jokers/stubborn_joker.lua")

-- Load Consumables (Tarots, Planets, Spectrals)
load_item("items/consumables/the_mirror.lua")
load_item("items/consumables/weakness.lua")
load_item("items/consumables/phantasm.lua")
load_item("items/consumables/pact.lua")
load_item("items/consumables/swaper.lua")
load_item("items/consumables/nibiru.lua")

-- Load Poker Hands
load_item("items/hands/quarry.lua")

-- Load Vouchers
load_item("items/vouchers/market.lua")
load_item("items/vouchers/supermarket.lua")

-- Load Decks
load_item("items/decks/echo_deck.lua")

-- Load Sleeves (CardSleeves compatibility)
load_item("items/sleeves/echo_sleeve.lua")

-- SlotManager compatibility: ensure SlotManager respects G.GAME.modifiers.extra_vouchers
if Game and Game.update_shop then
    local orig_update_shop = Game.update_shop
    Game.update_shop = function(self, ...)
        if G.GAME and G.GAME.modifiers and G.GAME.modifiers.extra_vouchers and G.GAME.modifiers.extra_vouchers > 0 then
            if SMODS.Mods and SMODS.Mods["SlotManager"] and SMODS.Mods["SlotManager"].config then
                local sm_cfg = SMODS.Mods["SlotManager"].config
                local expected = (G.GAME.starting_params and G.GAME.starting_params.vouchers_in_shop or 1) + G.GAME.modifiers.extra_vouchers
                if (sm_cfg.shop_vouchers or 0) < expected then
                    sm_cfg.shop_vouchers = expected
                    if G.GAME.slot_control_stock then
                        G.GAME.slot_control_stock.voucher_limit = expected
                    end
                end
            end
        end
        return orig_update_shop(self, ...)
    end
end

