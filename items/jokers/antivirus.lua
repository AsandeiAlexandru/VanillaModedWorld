--- Antivirus Joker
--- Gives +2 Chips for each unique card in your full deck.
--- Cards are unique based on rank, suit, enhancement, edition, and seal.

local function get_unique_deck_cards()
    if not G.playing_cards then return 0 end
    local seen = {}
    local count = 0
    for _, c in ipairs(G.playing_cards) do
        local rank, suit
        if c.ability and c.ability.effect == 'Stone Card' then
            rank = 'Stone'
            suit = 'Stone'
        else
            rank = tostring((c.base and (c.base.value or c.base.id)) or 'none')
            suit = tostring((c.base and c.base.suit) or 'none')
        end

        local enh = (c.ability and c.ability.set == 'Enhanced' and (c.config.center.key or c.ability.name)) or 'none'

        local ed = 'none'
        if c.edition then
            if c.edition.key then
                ed = c.edition.key
            elseif c.edition.foil then
                ed = 'foil'
            elseif c.edition.holo then
                ed = 'holo'
            elseif c.edition.polychrome then
                ed = 'polychrome'
            elseif c.edition.negative then
                ed = 'negative'
            end
        end

        local seal = c.seal or 'none'

        local key = rank .. '_' .. suit .. '_' .. enh .. '_' .. ed .. '_' .. seal
        if not seen[key] then
            seen[key] = true
            count = count + 1
        end
    end
    return count
end

SMODS.Atlas {
    key = "antivirus",
    path = "j_antivirus.png",
    px = 71,
    py = 95
}

SMODS.Joker {
    key = "antivirus",
    loc_txt = {
        name = "Antivirus",
        text = {
            "{C:chips}+#1#{} Chips for each",
            "{C:attention}unique card{} in",
            "your {C:attention}full deck{}",
            "{C:inactive}(Currently {C:chips}+#2#{C:inactive} Chips)"
        }
    },
    config = { extra = { chips_per = 2 } },
    rarity = 1, -- Common
    cost = 4,
    unlocked = true,
    discovered = true,
    blueprint_compat = true,
    atlas = "antivirus",
    pos = { x = 0, y = 0 },
    loc_vars = function(self, info_queue, card)
        local chips_per = (card and card.ability and card.ability.extra and card.ability.extra.chips_per) or self.config.extra.chips_per
        local unique_count = get_unique_deck_cards()
        return {
            vars = {
                chips_per,
                unique_count * chips_per,
                unique_count
            }
        }
    end,
    calculate = function(self, card, context)
        if context.joker_main then
            local unique_count = get_unique_deck_cards()
            local total_chips = unique_count * ((card and card.ability and card.ability.extra and card.ability.extra.chips_per) or self.config.extra.chips_per)
            if total_chips > 0 then
                return {
                    chips = total_chips,
                    message = localize { type = 'variable', key = 'a_chips', vars = { total_chips } }
                }
            end
        end
    end
}
