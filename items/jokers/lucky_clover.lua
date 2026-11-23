--- Lucky Clover Joker
--- Common Joker
--- If played hand contains a Lucky 4 of Clubs, guaranteed to trigger both Lucky Card effects (+20 Mult and $20).

SMODS.Atlas {
    key = "j_lucky_clover",
    path = "j_lucky_clover.png",
    px = 71,
    py = 95
}

-- Ensure Lucky 4 of Clubs always triggers money in get_p_dollars
local orig_get_p_dollars = Card.get_p_dollars
function Card:get_p_dollars(...)
    local ret = orig_get_p_dollars and orig_get_p_dollars(self, ...) or 0
    if not self.debuff and (self.ability.name == 'Lucky Card' or (SMODS.has_enhancement and SMODS.has_enhancement(self, 'm_lucky'))) then
        if self:get_id() == 4 and self:is_suit('Clubs') and #SMODS.find_card('j_vmw_lucky_clover') > 0 then
            self.lucky_trigger = true
            local p_dollars = self.ability.p_dollars or 20
            if ret < p_dollars then
                ret = ret + p_dollars
            end
        end
    end
    return ret
end

SMODS.Joker {
    name = "Lucky Clover",
    key = "lucky_clover",
    atlas = "j_lucky_clover",
    pos = { x = 0, y = 0 },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    config = {},
    loc_txt = {
        name = "Lucky Clover",
        text = {
            "Each scored {C:attention}Lucky 4 of Clubs{}",
            "is guaranteed to trigger",
            "all {C:attention}Lucky Card{} effects",
            "{C:inactive}(+20 Mult and $20){}"
        }
    },
    loc_vars = function(self, info_queue, card)
        info_queue[#info_queue + 1] = G.P_CENTERS.m_lucky
        return { vars = {} }
    end,
    calculate = function(self, card, context)
        -- Hook probability fixing for lucky_mult
        if context.fix_probability then
            local obj = context.trigger_obj
            if obj and type(obj) == 'table' and obj.is and obj:is(Card) then
                if obj:get_id() == 4 and obj:is_suit('Clubs') and (context.identifier == 'lucky_mult' or context.identifier == 'lucky_money') then
                    return { numerator = context.denominator }
                end
            end
        end

        -- In case individual scoring runs: guarantee trigger notification & lucky_trigger flag for Lucky Cat
        if context.individual and context.cardarea == G.play then
            local other = context.other_card
            if other:get_id() == 4 and other:is_suit('Clubs') and (other.ability.name == 'Lucky Card' or (SMODS.has_enhancement and SMODS.has_enhancement(other, 'm_lucky'))) then
                other.lucky_trigger = true
                return {
                    extra = { focus = other, message = localize('k_lucky_ex'), colour = G.C.MONEY },
                    card = card
                }
            end
        end
    end
}
