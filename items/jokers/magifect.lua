--- Magifect Joker
--- Retriggers only the Editions (Foil, Holographic, Polychrome) for every Joker.

SMODS.Atlas {
    key = "magifect",
    path = "j_magifect.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "magifect",
    loc_txt = {
        name = "Magifect",
        text = {
            "Retriggers all {C:dark_edition}Editions{}",
            "for every {C:attention}Joker{}"
        }
    },
    rarity = 2, -- 1: Common, 2: Uncommon, 3: Rare, 4: Legendary
    cost = 6,
    blueprint_compat = true,
    atlas = "magifect",
    pos = { x = 0, y = 0 },
    calculate = function(self, card, context)
        -- Triggers when any Joker (including itself) scores during hand evaluation
        if context.other_joker and context.other_joker.edition then
            local ed = context.other_joker.edition
            local ret = { card = card }
            local triggered = false

            if ed.foil or ed.chip_mod then
                ret.chip_mod = ed.chip_mod or 50
                ret.message = localize { type = 'variable', key = 'a_chips', vars = { ret.chip_mod } }
                ret.colour = G.C.CHIPS
                triggered = true
            elseif ed.holo or ed.mult_mod then
                ret.mult_mod = ed.mult_mod or 10
                ret.message = localize { type = 'variable', key = 'a_mult', vars = { ret.mult_mod } }
                ret.colour = G.C.MULT
                triggered = true
            elseif ed.polychrome or ed.x_mult_mod or ed.Xmult_mod then
                ret.Xmult_mod = ed.x_mult_mod or ed.Xmult_mod or 1.5
                ret.message = localize { type = 'variable', key = 'a_xmult', vars = { ret.Xmult_mod } }
                ret.colour = G.C.MULT
                triggered = true
            end

            if triggered then
                return ret
            end
        end
    end
}
