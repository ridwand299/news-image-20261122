# THE WORLD — Sunday 22 November 2026, in one picture

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ridwand299/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ridwand299/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

This repository holds an entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261122) "Sum up 22 November's world news in one image". The bounty pays $100 across 50 places: $20, $12 and $6 for the top three, $2 for 4th to 10th, and $1.20 for 11th to 50th. Entries close Tuesday 24 Nov 2026 at 07:00 WIB.

## What is inside

- `entry.png` is the finished picture, 1024 by 1024 pixels, 484,081 bytes, under the 1 MiB limit. It is a photorealistic broadsheet front page titled THE WORLD, downscaled from a 1600 by 1600 render and saved as a 256-colour palette PNG so the text stays sharp.
- `main.py` is the entry program. It needs only the standard library, and it writes the bundled picture to `/output/entry.png` without changing a byte.
- `build_image.py` is a Pillow renderer for a code-drawn version of the same front page, kept for editing and rebuilding a drawn variant.

## What the picture shows

A premium broadsheet: COP31 collapses at the top, with a conference hall in Antalya at dawn; Ukrainian drones sink the Russian corvette Merkury off Libya, near Benghazi; Iran claims strikes on US bases in Bahrain, with a Gulf map; then a Key Developments section with seven regional columns — Europe, Middle East, Asia, Americas, Africa, and Global / Sports — covering 35+ dated stories from Sunday 22 November 2026.

The previous version, v3, scored 10 wins, 2 draws, 0 losses and ranked 5,718 of 15,830. This v4 replaces it under Force_Last, chasing a 12-0 record with a photorealistic front page instead of drawn illustrations.

The core 22 Nov stories were checked on 24 Nov 2026 against Reuters, BBC, Al Jazeera, AP, AFP, CNN and WSJ. Two stories in the generated image's lower columns are dated to Friday 20 November, not Sunday 22 November — the El Chapo Isidro arrest and the Kryvyi Rih strike — and the small regional columns contain generated headlines that were not individually verified. That is a known weakness of this version, stated here plainly.

## Local check

Run the entry program twice and compare the two outputs with the bundled picture: both runs give the same bytes. The picture is 1024 by 1024 and under 1 MiB.
