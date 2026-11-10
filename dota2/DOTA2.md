# Dota 2 video workspace

This folder is a **Dota 2-only** video production workspace. It is a vendored copy of
[claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (MIT).

Everything made here is about Dota 2. Do not use this folder for unrelated topics — other
projects belong in their own folders, not here.

## Scope

In scope:

- Hero spotlights, patch/balance breakdowns, ability and item explainers
- Match and replay analysis, pro-scene recaps, tournament previews
- Guides: laning, drafting, roles, farming patterns, item timings
- Shorts built from Dota 2 clips, plus longer explainers with voiceover

Out of scope:

- Any non-Dota 2 game or topic
- Clips used without rights — see **Media** below

## Where things go

| Path | What |
|---|---|
| `projects/` | One folder per video (gitignored — your working files) |
| `templates/` | Starting points: `cp -r templates/<name> projects/<my-video>` |
| `assets/` | Shared Dota 2 art, fonts, logos |
| `brands/` | Dota 2 brand tokens and colours |

Run toolkit tools from **this folder** (the toolkit root), not from inside a project:

```bash
uv run tools/video_job.py catalog          # every template, example, brand
uv run tools/qc.py --project projects/<name>
```

## Media

- Valve's own material (hero art, ability icons, patch notes, in-game capture you recorded)
  is the safe default for a Dota 2 channel.
- Third-party clips, music and overlays need a licence you can point at. Keep the receipt.
- Record or export at the source resolution; do not upscale a compressed stream.

## Visual defaults

- Dark background, Dota 2 red/orange accents, condensed sans for numbers.
- Hero names and item names spelled exactly as in-game (e.g. "Anti-Mage", "Aghanim's Scepter").
- Patch numbers always shown with the version string (`7.39c`), never approximated.

## Voice and tone

- Talk to players who already know the game; explain the *why*, not the basics.
- Numbers over adjectives: "300 gold swing" beats "huge value".
- No hype filler. State the change, then what it means for a real game.
