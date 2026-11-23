--- Echo Deck (Custom Deck)
--- Retriggers every Joker 1 additional time (so every Joker triggers twice).
--- Blinds scale by X Ante base blind size (Ante 1 = 1x, Ante 2 = 2x, ..., Ante 8 = 8x).
--- No Joker slot penalty, no reroll cost penalty.

SMODS.Atlas {
    key = "b_echo",
    path = "b_echo.png",
    px = 71,
    py = 95
}

-- Global dynamic scaling helper for Echo Deck and Echo Sleeve
function VMW_update_echo_ante_scaling()
    if not G.GAME or not G.GAME.starting_params then return end
    local is_echo_deck = G.GAME.selected_back and (G.GAME.selected_back.effect.center.key == "b_vmw_echo_deck" or G.GAME.selected_back.effect.center.key == "b_echo_deck")
    local is_echo_sleeve = CardSleeves and G.GAME.selected_sleeve and (G.GAME.selected_sleeve == "sleeve_vmw_echo" or G.GAME.selected_sleeve == "sleeve_echo")

    if is_echo_deck or is_echo_sleeve then
        local ante = math.max(1, (G.GAME.round_resets and G.GAME.round_resets.ante) or 1)
        G.GAME.starting_params.ante_scaling = ante
    end
end

-- Hook game functions once to ensure ante_scaling is updated on every blind/ante transition
if not VMW_ECHO_SCALING_HOOKED then
    VMW_ECHO_SCALING_HOOKED = true

    if Blind and Blind.set_blind then
        local set_blind_ref = Blind.set_blind
        function Blind:set_blind(blind, reset, silent)
            VMW_update_echo_ante_scaling()
            set_blind_ref(self, blind, reset, silent)
        end
    end

    if ease_ante then
        local ease_ante_ref = ease_ante
        function ease_ante(mod)
            ease_ante_ref(mod)
            VMW_update_echo_ante_scaling()
        end
    end

    if reset_blinds then
        local reset_blinds_ref = reset_blinds
        function reset_blinds()
            reset_blinds_ref()
            VMW_update_echo_ante_scaling()
        end
    end
end

SMODS.Back {
    name = "Echo Deck",
    key = "echo_deck",
    loc_txt = {
        name = "Echo Deck",
        text = {
            "Retriggers all {C:attention}Jokers{}",
            "{C:attention}1{} additional time,",
            "Required Blind chips",
            "scale by {C:attention}X Ante{} base size"
        }
    },
    config = {},
    atlas = "b_echo",
    pos = { x = 0, y = 0 },
    apply = function(self, back)
        VMW_update_echo_ante_scaling()
    end,
    calculate = function(self, back, context)
        -- Keep ante_scaling updated when rounds end / ante changes
        if context.end_of_round and not context.individual and not context.repetition then
            VMW_update_echo_ante_scaling()
        end

        -- Retrigger all Jokers 1 additional time (so every Joker triggers twice)
        if context.retrigger_joker_check and not context.retrigger_joker then
            return {
                message = localize('k_again_ex'),
                repetitions = 1,
                card = context.other_card
            }
        end
    end
}
