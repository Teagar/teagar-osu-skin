# Teagar's 2.0

My personal custom skin for [osu!](https://osu.ppy.sh/), with assets and configurations for osu!standard and osu!mania.

![Teagar's 2.0 showcase](docs/showcase/overview.jpg)

## Preview

The images below are presentation mockups composed from the actual assets included in the skin.

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
- 100% gameplay background dim with no blur
- HUD always visible, with score and accuracy at the top-right
- Gameplay leaderboard and key overlay disabled
- 0.69 gameplay cursor size in osu!standard

## Installation

1. Download `Teagars-2.0.osk` from the [latest release](https://github.com/Teagar/teagar-osu-skin/releases/latest).
2. Open the downloaded file with osu!.
3. Select **Teagar's 2.0 [Teagar]** in the skin settings.

## Manual installation

Clone or download this repository and copy its contents into a folder under the osu! `Skins` directory.

## Details

- Creator: Teagar
- Skin name: Teagar's 2.0
- Primary colour: `#00BAFF`
- Accent colour: `#00FF90`

## Regenerating the showcase

The preview images can be regenerated with Pillow:

```bash
python tools/generate_previews.py
```
