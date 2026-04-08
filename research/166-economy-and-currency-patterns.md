# 166 — Economy and currency patterns

## Question

What canonical in-game economy and currency primitives does GSPL ship in `economy.*` so that any genre can adopt single/dual/multi-currency systems, faucets/sinks, marketplaces, auctions, barter, and inflation control by composition rather than from scratch, and what are the bounds, signed-flow guarantees, and v0.1 reach for each?

## Why it matters (blast radius)

Economies are where game-design intent meets emergent player behavior most violently. A miscalibrated faucet creates inflation that breaks every later content tier; an unsigned currency mutation lets a duplication exploit drain the substrate's economic guarantees. Without typed economy primitives, every game reinvents currency from raw integers and loses the substrate's audit, balance, and anti-cheat capabilities. Brief 169 (loot/drop), Brief 186 (balance), Brief 213 (anti-cheat), Brief 214 (live-ops monetization), Brief 216 (monetization patterns), and the entire Tier E genre layer (esp. RPG, sim, strategy, sandbox families) depend on a typed `economy.*` namespace.

## What we know from the spec

- Brief 153 — ECS substrate; currency balances are typed components
- Brief 158 — save/load; balances are part of save state
- Brief 165 — progression; some progression primitives consume economy currency
- Brief 169 — loot system; faucets feed currency into players
- Brief 186 — balance tooling reads from typed economy graphs
- Brief 213 — anti-cheat needs every currency mutation to be signed and queryable
- Brief 149 — v0.1 frozen scope: economy ships at v0.1 for single-player, multiplayer auction defers to v0.3

## Findings

1. **Five canonical primitives.** Surveying *Game Mechanics: Advanced Game Design* (Adams & Dormans), Eve Online economic reports, Diablo 3's auction house postmortem, Stardew Valley, Animal Crossing, Path of Exile, and Hades, the irreducible economy primitive set is **five typed gseeds**: `economy.currency`, `economy.faucet`, `economy.sink`, `economy.exchange`, `economy.market`. Every shipped economy reduces to these five composed.

2. **`economy.currency`.** A typed currency definition. Parameters: `currency_id: CurrencyId`, `display_name: LocalKey`, `decimal_places: u8 ∈ [0, 6]`, `is_soft: bool`, `cap_per_holder: optional<u64>`, `cap_global: optional<u64>`, `decay_per_tick: optional<f32>`, `tradeability: enum{none, gift, market, full}`, `signing_authority: enum{client, server, federation}`. The substrate stores all balances as `u64` minor units (like cents) for deterministic arithmetic; the `decimal_places` field is for display only. Currency mutation is *always* a signed event going through `economy.flow`.

3. **`economy.faucet`.** A signed source of currency. Parameters: `faucet_id`, `currency_id`, `rate_model: enum{per_event, per_tick, per_milestone, per_loot_drop}`, `rate_params`, `attribution: gseed_ref`. Every coin entering the world has a faucet attribution. Balance tooling can answer "where did the player's gold come from this hour?" without instrumentation.

4. **`economy.sink`.** A signed drain. Parameters: `sink_id`, `currency_id`, `mode: enum{purchase, tax, decay, repair, gamble, sacrifice, loss_on_death}`, `rate_params`, `attribution`. Sinks are the half of the economy creators forget; the substrate tooling explicitly graphs faucet/sink ratios per game session and warns at imbalance thresholds (Brief 186 enforces).

5. **`economy.exchange`.** Static or formulaic conversion between currencies. Parameters: `from: currency_id`, `to: currency_id`, `rate: f32 | formula_ref`, `bidirectional: bool`, `fee_pct: f32 ∈ [0.0, 1.0]`, `availability_predicate: optional<predicate>`. Exchange is the core primitive of dual-currency designs (soft/hard separation in F2P, gold/gems in mobile, runes/orbs in PoE).

6. **`economy.market`.** Player-to-player or player-to-NPC trade venue. Parameters: `market_id`, `mode: enum{vendor, auction, order_book, barter, gift}`, `listing_lifetime_ticks`, `fee_pct`, `min_listing_price`, `tradeable_currencies`, `tradeable_items_predicate`, `signing_authority`. Markets are *the* multiplayer-anchored primitive — single-player games use them only for NPC vendors; v0.3+ unlocks player-to-player auction and order book.

7. **`economy.flow`.** Every currency mutation goes through a signed `economy.flow` event with `from: account_ref`, `to: account_ref`, `amount: u64_minor_units`, `currency_id`, `cause: faucet_ref | sink_ref | exchange_ref | market_ref`, `tick`, `lineage`. Flows are batched into the per-tick Merkle root (Brief 153). Server-authoritative in multiplayer (Brief 210). This is the substrate's anti-duplication guarantee: every coin's existence is traceable from faucet to current holder.

8. **Inflation control primitives.** Hardcoded patterns from Adams & Dormans + Eve Online's quarterly economy reports: (a) **decay**: per-tick percentage drain on idle balances; (b) **drain sinks**: equipment repair, taxes, fast travel costs; (c) **tier-locked sinks**: high-tier sinks only available to high-progression players, scaling drain with capacity; (d) **bound items**: the most powerful items are bind-on-pickup, removing them from the economy. The substrate ships all four as named flags on `economy.sink` and `economy.market`.

9. **Faucet/sink balance heuristic.** Per published Eve and Diablo postmortems: a healthy economy maintains faucet/sink ratio between 0.95 and 1.10 over a rolling 7-day window. The substrate's balance tooling (Brief 186) implements this as the default warning gate; creators can override per-currency.

10. **Single vs dual vs multi-currency.** Single-currency (Stardew gold) is the simplest; dual-currency (gold + gems, or hard + soft) is the F2P standard; multi-currency (Hades 6 currencies, Hollow Knight 5+) layers economic intent. The substrate has no preference; each `economy.currency` is independent and a game can have 1-32 currencies (cap from Brief 158 save schema field count).

11. **Marketplace modes.** Vendor (NPC fixed-price buy/sell), auction (timed bid), order book (continuous limit orders, Eve-style), barter (item-for-item, Animal Crossing/Diablo 2 style), gift (free transfer, social games). Each is a `mode` enum value on `economy.market` with the same flow signing discipline.

12. **Anti-cheat hooks.** Because every flow is signed and per-tick Merkle-batched, the multiplayer authority server (Brief 210) can verify any client claim against the lineage graph. Duplication exploits become impossible *by construction*: you cannot mint a coin without a faucet ID, and faucets are server-signed.

13. **Composition example: Hades.** Six currencies (gold/darkness/gemstones/diamonds/titan_blood/ambrosia), with explicit `economy.exchange` between gemstones and shop materials, sinks via the contractor and Charon, faucet attribution per boss/encounter, and Zagreus's death that returns him to the House but keeps darkness/gems while resetting gold. Every node is one of the five primitives; the *intent* lives in the composition graph.

14. **Composition example: Stardew.** One currency (gold), faucets via crops/fish/foraging/mining/quests, sinks via seeds/buildings/upgrades/marriage/community-center, no marketplace beyond NPC vendors. Single-currency single-player; the entire economy fits in 1 currency + ~12 faucets + ~10 sinks + 1 market in vendor mode.

15. **Currency decimals and arithmetic.** All math is integer minor units; conversion uses banker's rounding for determinism; display layer divides by 10^decimal_places. This avoids the floating-point determinism trap (Brief 020) and the "1.00 + 2.00 ≠ 3.00 in JS" class of bug.

16. **Save and replay.** Currency state is a typed component on the player entity (or on world entities for shared funds). The signed flow log is the rollback substrate's audit trail; replays can recompute current balances from the flow log alone, which doubles as anti-tamper.

17. **v0.1 reach.** All 5 primitives ship at v0.1. Vendor and gift markets ship; auction and order book defer to v0.3 multiplayer (the substrate exists, the runtime is gated). Federation-level cross-game economies (briefly considered) deferred to v0.5 — currencies are per-game in v0.1-v0.4 and have no cross-game value.

## Risks identified

1. **F2P monetization can poison creator intent.** A typed economy.market makes "spend $5 for 500 gems" trivial to add. Mitigation: Brief 216's monetization patterns library is a strict opt-in with an ethics gate; the substrate refuses to ship a game with `economy.market.mode=iap` unless the creator explicitly signs the monetization-disclosure gseed.

2. **Multi-currency complexity for casual creators.** A creator who just wants "coins" shouldn't have to think about faucets and sinks. Mitigation: `economy.preset.simple_coin` template ships at v0.1; one line of config equips a single currency with vendor sinks and quest faucets.

3. **Inflation in long-running sims.** v0.5's sim-loop games will run for hundreds of in-game years. Mitigation: decay primitive + tier-locked sinks + balance tooling alarms. Worst case is per-game; not a substrate risk.

4. **Cross-currency exploit chains.** A bidirectional exchange pair with even tiny rounding asymmetry can be exploited via repeated micro-trades. Mitigation: `economy.exchange.fee_pct` defaults to 0.5%; balance tooling flags any chain of exchanges with net zero round-trip cost.

5. **Item-not-currency dupes.** Items aren't in `economy.*` but in inventories (later brief in Tier B). Mitigation: items inherit the same flow signing discipline; cross-link from this brief into the inventory section.

## Recommendation

Ship the 5-primitive `economy.*` vocabulary with the schemas, integer-minor-unit arithmetic, signed flow log, and inflation-control flags above. Default new games to a `simple_coin` preset; require explicit composition for anything more complex. Wire balance tooling to read the typed flow graph from day one. Hold auction/order_book modes behind the v0.3 multiplayer gate but ship the schemas at v0.1 so creators can prototype.

## Confidence

**4/5.** The five-primitive decomposition is well-grounded in published economy postmortems (Eve, Diablo 3, PoE, Hades, Stardew) and the integer-minor-units + signed-flow model is the same approach used by financial systems and rollback fighting games. Held back from 5 because federation-level cross-game economy (deferred to v0.5) is the only piece without prior art and may need additional rounds.

## Spec impact

- Add `economy.*` namespace with 5 primitive sub-namespaces and `economy.flow` event type
- Specify integer-minor-units arithmetic and banker's rounding rule
- Add inflation-control flags to `economy.sink` and `economy.market`
- Cross-link to Brief 153 (ECS components), Brief 158 (save), Brief 169 (loot faucets), Brief 186 (balance), Brief 210 (server authority), Brief 213 (anti-cheat), Brief 216 (monetization gates)
- Mark auction and order_book v0.3-deferred per Finding 17

## New inventions

- **INV-665** Five-primitive canonical `economy.*` substrate vocabulary
- **INV-666** `economy.flow` signed currency mutation event with per-tick Merkle batching as the substrate-level anti-duplication guarantee
- **INV-667** Integer-minor-unit deterministic currency arithmetic with banker's rounding
- **INV-668** Faucet/sink ratio auto-graphing as substrate-native balance tooling input
- **INV-669** Monetization-disclosure ethics gate enforced at gseed sign time

## Open follow-ups

- Inventory and item-flow signing (next brief in Tier B section will pick this up implicitly via the loot brief)
- Federation cross-game currency proposal (deferred to v0.5 round)
- Specific recommended faucet/sink ratios per genre (Brief 230 cross-genre matrix)
- Localization-aware currency display (Brief 220 i18n)

## Sources

1. *Game Mechanics: Advanced Game Design*, Adams & Dormans, ch. on internal economies — primitives framework
2. CCP Games Eve Online quarterly economic reports (multiple years) — faucet/sink discipline at MMO scale
3. Diablo 3 real-money auction house postmortem, Blizzard, 2014 — anti-pattern lessons
4. Path of Exile currency design talk, GGG GDC 2018 — multi-currency intentional design
5. Hades currency talk, Supergiant GDC 2020 — six-currency composition
6. Stardew Valley postmortem, GDC 2017 — single-currency simple preset
7. Animal Crossing economic design retrospective, Nintendo, 2020 — gift mode and player trade
8. *A Theory of Fun*, Raph Koster — economy as system intent
9. RuneScape Grand Exchange paper, Jagex, 2007 — order book in MMO context
10. Brief 020 (this repo) — determinism contract that drives integer-minor-unit choice
11. Brief 153 (this repo) — ECS substrate that holds currency components
