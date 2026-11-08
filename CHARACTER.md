# DEV — the HyperFrames presenter

**Canonical avatar for every video in this studio.** Every project gets the same person, not a new
illustration. Version **v2** (2026-11-08).

The art lives in `compositions/presenter.html` between `<!-- CHARACTER:START -->` and
`<!-- CHARACTER:END -->`. The live reference card is `compositions/character-sheet.html`.

---

## 1. Who he is

| | |
|---|---|
| **Name** | Dev |
| **Role** | The developer-narrator. He has shipped the thing he is explaining. |
| **Age / look** | Mid-20s, South Asian, round face, warm medium-tan skin, short black side-parted hair |
| **Wardrobe** | Charcoal hoodie, hood up at the back, white drawstrings with red aglets, kangaroo pocket |
| **Signature** | Thick round black glasses + a red enamel pin on the chest (viewer's left). The pin is always there. |
| **Voice** | Warm, quick, a little dry. Explains with his hands. Never smug, never shouting. |
| **Energy** | Curious builder. He points at the thing he just said and palms-up on the why. |

He is the same character in a React breakdown, a product launch, and a 9:16 short. Restyle the
**world** around him, never **him**.

---

## 2. Palette — do not substitute

| Token | Hex | Use |
|---|---|---|
| Ink | `#302018` | All outlines, 6 px, round caps and joins |
| Ink soft | `#C9825F` | Finger creases, ear inner line, nose shadow |
| Skin | `#F2C6A6` | Face, ears, hands |
| Skin shade | `#E8B896` | Neck |
| Skin deep | `#D69C79` | Under-jaw shadow |
| Blush | `#E08A6A` | Cheeks at 32 % |
| Hair | `#1B1815` | Hair |
| Hoodie | `#2E2B28` | Torso and sleeves |
| Hood | `#262320` | Hood collar |
| Hood inner | `#151312` | Inside of the hood (55 %) |
| Hoodie shade | `#201D1B` | Left-side body shade (50 %) |
| Cuff | `#3B3733` | Cuffs |
| Paper | `#FBFAF8` | Glasses lenses, drawstrings, teeth |
| Accent red | `#A31C14` | Pin, drawstring aglets, tongue, tongue accent |
| Iris | `#4A3427` | Iris ring behind the pupil |

If a project's brand colour is different, use it in the **scene**, not in the character. The red
`#A31C14` accent is part of him.

---

## 3. Rig and proportions (1080 × 1920)

- **Canvas:** `650 × 750` SVG, mounted at `left: 430px; top: 1170px` (bottom-right third).
- **Head:** ~226 wide × 244 tall, centred at `(325, 320)`. Chin at `y 456`.
- **Face landmarks:** glasses `y 298–358`; pupils `y 328`; nose `y 332–358`; mouth origin `(325, 392)`; ears centred `y 332`.
- **Neck:** `x 286–364`, `y 398–522`; hood collar `y 450–564`.
- **Shoulders:** torso begins at `y 504`, bottom edge is clipped by the frame.
- **Hands:** raised beside the chest, never over the face. `hand-point` is an index-up right hand,
  `hand-palm` is an open palm. Both enter from the bottom edge and park at `y: 500` when hidden.
- **Scale:** never scale the character to fit; change the scene around him. If a project is not
  1080 × 1920, keep the same head size and re-anchor the rig.

---

## 4. Required structure (IDs are contractual)

```
#presenter-rig        650×750 rig, positioned 430,1170
#body-breath          torso + hood + drawstrings + pocket + pin (idle breathing target)
#head-anchor          neck + ears + face + hair + brows + glasses + mouth (sway/nod target)
#glasses              lenses, bridge, temples, irises, pupils, specular dots
#eyelids              blink cover (toggled with opacity)
#mouths               mouth origin, translate(325, 392)
#m-0 … #m-9           10 visemes, toggled with display
#hand-point           raised index finger
#hand-palm            open palm
```

- One **paused** root timeline per composition, registered on `window.__timelines["presenter"]`.
- **Lip-sync** = `tl.set("#m-n", { display: "block" })` / `none` on a 33 ms grid, derived from the
  word timings in `transcript.json`.
- **Blink** = `tl.set("#eyelids", { opacity: 1 })` for 140 ms.
- **Sway** = `#head-anchor` rotate ±2.2°, x ±6, 1.4 s yoyo; **nods** are separate y-only tweens.
- **Breathing** = `#body-breath` y −6, 2.1 s yoyo. The head does not breathe.
- **Gestures** = y-only tweens on the hand groups. GSAP owns the group transform, so author hand
  art in local coordinates as if the group is at `translate(x, 0)`.
- Import GSAP 3.15.0 from the same CDN URL the project pins.

---

## 5. Do / don't

**Do**
- Copy the whole `CHARACTER:START … CHARACTER:END` block, then re-time only the performance.
- Keep the red pin, the white drawstrings with red aglets, and the hood collar.
- Keep the head size, eye line, and mouth origin stable so the lipsync timeline stays valid.
- Give him a new gesture, prop, or outfit colour only if it reads at 1080 wide and does not cover
  the eyes or mouth.
- Run `npm run check` and look at a mouth-open frame plus a gesture frame before rendering.

**Don't**
- Don't redesign the face, hair, glasses, or body silhouette per project.
- Don't change skin/hair/hoodie colours to match a brand palette.
- Don't put the hand in front of the face or above the head.
- Don't add sunglasses, hats, beards, headphones, or a different hairline — those become a
  different character.
- Don't scale the rig non-uniformly or flip it horizontally.
- Don't animate the character with wall-clock time; everything must be seekable.

---

## 6. Reusing him in a new project

1. Copy `compositions/presenter.html` and `CHARACTER.md` into the new project.
2. Keep the SVG block between `CHARACTER:START` / `CHARACTER:END` untouched.
3. Replace only the performance section: the lipsync `tl.set` list, blink times, nod times, and
   gesture cues. Derive mouth timings from the new `transcript.json`.
4. Mount him in the root composition:
   ```html
   <div
     class="clip"
     data-start="0"
     data-duration="44.0"
     data-composition-src="compositions/presenter.html"
     data-composition-id="presenter-embed"
   ></div>
   ```
5. Verify: `npm run check`, then
   `npx hyperframes snapshot --at <a mouth-open beat>,<a gesture beat>`.
6. If the project is not 9:16, re-anchor the rig but keep his scale and head size.

The reference card (`compositions/character-sheet.html`) mounts the live presenter, so it can never
drift from the actual character. Snapshot it when you need a quick visual sanity check.

---

## 7. Change log

- **v1** — initial flat avatar: cone hoodie, floating hands, helmet hair.
- **v2 (2026-11-08)** — canonical redesign: shoulders, hood, drawstrings, pocket, red pin; warmer
  skin; brown irises; blush; fixed hairline; hands moved from above the head to beside the chest
  with visible sleeves and cuffs; idle breathing; default half-smile.
