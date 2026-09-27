# Teagar's 2.1

My personal custom skin for [osu!](https://osu.ppy.sh/), with assets and configurations for osu!standard and osu!mania.

![Teagar's 2.1 showcase](docs/showcase/overview.jpg)

## Preview

The images below are presentation mockups composed from the actual assets included in the skin. Their geometry and HUD placement were measured from the running osu!lazer client at 1920×1080.

| Main menu | osu!mania |
|:---:|:---:|
| ![Main menu preview](docs/showcase/menu.png) | ![osu!mania gameplay preview](docs/showcase/gameplay-mania.png) |

| osu!standard | Results |
|:---:|:---:|
| ![osu!standard gameplay preview](docs/showcase/gameplay-standard.png) | ![Results screen preview](docs/showcase/results.png) |

### Visual profile reproduced

The gameplay mockups follow the current local osu!lazer visual configuration:

- 1920×1080 fullscreen display at approximately 144 Hz
- osu!mania as the selected ruleset
- Current osu!mania preview reproduced in its observed 7K layout
- 100% gameplay background dim with no blur
- HUD always visible, with score and accuracy at the top-right
- Gameplay leaderboard disabled, with the custom key counter visible at the right
- 0.69 gameplay cursor size in osu!standard

## Installation

1. Download `Teagars-2.1.osk` from the [latest release](https://github.com/Teagar/teagar-osu-skin/releases/latest).
2. Open the downloaded file with osu!.
3. Select **Teagar's 2.1 [Teagar]** in the skin settings.

## Manual installation

Clone or download this repository and copy the contents of [`skin/`](skin/) into a folder under the osu! `Skins` directory.

## Repository structure

- [`skin/`](skin/) — complete skin source, ready for manual installation
- [`docs/showcase/`](docs/showcase/) — visual previews used in this README
- [`tools/`](tools/) — scripts used to generate the showcase

## Details

- Creator: Teagar
- Skin name: Teagar's 2.1
- Maintenance revision: v2.1
- Primary colour: `#00BAFF`
- Accent colour: `#00FF90`

### Compatibility

The v2.1 maintenance pass normalises metadata and asset references, provides valid silent audio files, and keeps legacy `skin.ini` compatibility alongside osu!lazer HUD metadata.
The 4K layout uses compact competitive-style circles and static ring receptors in the skin's symmetric white–blue–blue–white palette.
Mania hold trails use the colour of their corresponding notes at 69% opacity and rectangular ends; in 4K, their narrower profile keeps the circular heads distinct.
Mania hit lighting is fully disabled, including normal notes, long notes, and continuous key-press lighting.

## Regenerating the showcase

The preview images can be regenerated with Pillow:

```bash
python tools/generate_previews.py
```
