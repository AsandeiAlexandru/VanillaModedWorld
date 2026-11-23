--- Quarry Poker Hand
--- Requires 5 Stone Cards played in the hand.
--- Base stats: 200 Chips, 20 Mult (Level up: +40 Chips, +4 Mult)

local function is_stone(card)
    if not card then return false end
    if SMODS.has_enhancement and SMODS.has_enhancement(card, 'm_stone') then
        return true
    end
    if card.ability and (card.ability.name == 'Stone Card' or card.ability.effect == 'Stone Card') then
        return true
    end
    if card.config and card.config.center == G.P_CENTERS.m_stone then
        return true
    end
    return false
end

SMODS.PokerHandPart {
    key = 'quarry_stones',
    prefix_config = { key = false },
    func = function(hand)
        local stones = {}
        for i = 1, #hand do
            if is_stone(hand[i]) then
                stones[#stones + 1] = hand[i]
            end
        end
        if #stones >= 5 then
            return { stones }
        end
        return {}
    end
}

SMODS.PokerHand {
    key = 'Quarry',
    prefix_config = { key = false },
    mult = 20,
    chips = 200,
    l_mult = 4,
    l_chips = 40,
    visible = false,
    example = {
        { 'S_A', true, enhancement = 'm_stone' },
        { 'D_A', true, enhancement = 'm_stone' },
        { 'C_A', true, enhancement = 'm_stone' },
        { 'H_A', true, enhancement = 'm_stone' },
        { 'S_K', true, enhancement = 'm_stone' },
    },
    loc_txt = {
        name = 'Quarry',
        description = {
            '5 Stone Cards'
        }
    },
    evaluate = function(parts, hand)
        local part = parts.quarry_stones or parts.vmw_quarry_stones
        if part and next(part) then
            return part
        end
        return {}
    end
}
