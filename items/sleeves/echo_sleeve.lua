--- Echo Sleeve (Custom Sleeve for CardSleeves mod)
--- When paired with any other deck:
---   Copies Echo Deck ability:
---   - Retriggers all Jokers 1 additional time (triggers 2 times total).
---   - Required Blind chips scale by X Ante base blind size.
---
--- When paired with Echo Deck (b_vmw_echo_deck or b_echo_deck):
---   Combo / Stacked effect:
---   - Retriggers every played card 1 additional time.
---   - -1 hand size.

if not CardSleeves then
    print("[VanillaModedWorld] CardSleeves mod not detected; skipping Echo Sleeve.")
    return
end

SMODS.Atlas {
    key = "sleeve_echo",
    path = "sleeve_echo.png",
    px = 73,
    py = 95
}

-- Ensure Sleeve localization table exists and inject entries as fallback
G.localization = G.localization or {}
G.localization.descriptions = G.localization.descriptions or {}
G.localization.descriptions.Sleeve = G.localization.descriptions.Sleeve or {}

local normal_desc = {
    name = "Echo Sleeve",
    text = {
        "Retriggers all {C:attention}Jokers{}",
        "{C:attention}1{} additional time,",
        "Required Blind chips",
        "scale by {C:attention}X Ante{} base size"
    }
}

local combo_desc = {
    name = "Echo Sleeve",
    text = {
        "Retriggers all {C:attention}played cards{}",
        "{C:attention}1{} additional time,",
        "{C:red}-1{} hand size"
    }
}

G.localization.descriptions.Sleeve["sleeve_vmw_echo"] = normal_desc
G.localization.descriptions.Sleeve["sleeve_vmw_echo_alt"] = combo_desc
G.localization.descriptions.Sleeve["sleeve_echo"] = normal_desc
G.localization.descriptions.Sleeve["sleeve_echo_alt"] = combo_desc
G.localization.descriptions.Sleeve["echo"] = normal_desc
G.localization.descriptions.Sleeve["echo_alt"] = combo_desc

-- Helper to detect if the selected or viewed deck is Echo Deck
local function is_echo_deck_key(key)
    if not key then return false end
    return (key == "b_vmw_echo_deck" or key == "b_echo_deck" or key == "echo_deck" or (type(key) == "string" and key:find("echo_deck") ~= nil))
end

-- Helper to check if the combo (Echo Deck + Echo Sleeve) is active
function VMW_is_echo_sleeve_combo()
    if not CardSleeves or not G.GAME then return false end
    local is_echo_sleeve = (G.GAME.selected_sleeve == "sleeve_vmw_echo" or G.GAME.selected_sleeve == "sleeve_echo")
    local deck_key = G.GAME.selected_back and G.GAME.selected_back.effect and G.GAME.selected_back.effect.center and G.GAME.selected_back.effect.center.key
    return is_echo_sleeve and is_echo_deck_key(deck_key)
end

CardSleeves.Sleeve {
    key = "echo",
    name = "Echo Sleeve",
    atlas = "sleeve_echo",
    pos = { x = 0, y = 0 },
    unlocked = true,
    discovered = true,
    config = {},
    loc_vars = function(self)
        local deck_key = nil
        if self.get_current_deck_key then
            deck_key = self.get_current_deck_key()
        elseif CardSleeves and CardSleeves.Sleeve and CardSleeves.Sleeve.get_current_deck_key then
            deck_key = CardSleeves.Sleeve.get_current_deck_key()
        end
        if not deck_key and G.GAME then
            if G.GAME.viewed_back and G.GAME.viewed_back.effect and G.GAME.viewed_back.effect.center then
                deck_key = G.GAME.viewed_back.effect.center.key
            elseif G.GAME.selected_back and G.GAME.selected_back.effect and G.GAME.selected_back.effect.center then
                deck_key = G.GAME.selected_back.effect.center.key
            end
        end

        local is_echo = is_echo_deck_key(deck_key)
        local key = is_echo and (self.key .. "_alt") or self.key
        return { key = key, vars = {} }
    end,
    apply = function(self, sleeve)
        CardSleeves.Sleeve.apply(self)
        if VMW_is_echo_sleeve_combo and VMW_is_echo_sleeve_combo() then
            G.GAME.starting_params.hand_size = (G.GAME.starting_params.hand_size or 8) - 1
            if G.GAME.round_resets and G.GAME.round_resets.hands_size then
                G.GAME.round_resets.hands_size = G.GAME.round_resets.hands_size - 1
            end
            if G.hand then
                G.hand:change_size(-1)
            end
        else
            if VMW_update_echo_ante_scaling then
                VMW_update_echo_ante_scaling()
            end
        end
    end,
    calculate = function(self, sleeve, context)
        local deck_key = (G.GAME.selected_back and G.GAME.selected_back.effect and G.GAME.selected_back.effect.center and G.GAME.selected_back.effect.center.key)
        local is_echo = is_echo_deck_key(deck_key)

        if is_echo then
            -- When stacked with Echo Deck: Retrigger each played card 1 additional time
            if context.repetition and context.cardarea == G.play then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = context.other_card
                }
            end
        else
            -- When on any other deck: copy Echo Deck ability (retrigger each Joker 1 additional time & ante scaling)
            if context.end_of_round and not context.individual and not context.repetition then
                if VMW_update_echo_ante_scaling then
                    VMW_update_echo_ante_scaling()
                end
            end
            if context.retrigger_joker_check and not context.retrigger_joker then
                return {
                    message = localize('k_again_ex'),
                    repetitions = 1,
                    card = context.other_card
                }
            end
        end
    end
}
