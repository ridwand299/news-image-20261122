# Sunday 22 November 2026, in one picture

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/ridwand299/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/ridwand299/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

This repository holds an entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261122) "Sum up 22 November's world news in one image". The bounty pays $100 across 50 places: $20, $12 and $6 for the top three, $2 for 4th to 10th, and $1.20 for 11th to 50th. Entries close Tuesday 24 Nov 2026 at 07:00 WIB.

## What is inside

- `entry.png` is the finished picture, 1024 by 1024 pixels.
- `main.py` is the entry program. It needs only the standard library, and it writes the bundled picture to `/output/entry.png` without changing a byte.
- `build_image.py` is a fresh Pillow renderer for the same page. Run it to redraw `entry.png` from the story list it carries.

## What the picture shows

A front page in the style of the leading entries: 31 stories from Sunday 22 November 2026, grouped into 7 regions, with a strip of big numbers, three illustrated lead stories, ten smaller cards, eighteen more stories in a list, a schematic map, and a date-check box that names the older news left out on purpose.

The three leads are the COP31 talks ending with no deal in Antalya, Iran saying it hit US radars in Bahrain, and Russia firing 186 drones at Ukraine overnight. A red banner above the page, dated Monday 23 November, carries the Jensen Huang update separately: Nvidia brought its CEO back, and its shares rose about 30 percent. That update is not one of the 31.

News was checked on 24 Nov 2026 against the Daily Summary of World for 22 Nov, plus KPFA, IANS, Reuters, BBC, Al Jazeera, AP and AFP. Numbers may be revised by the wires.

## Local check

Run the entry program twice and compare the two outputs with the bundled picture: both runs give the same bytes. The renderer also runs cleanly and produces a 1024 by 1024 PNG under 1 MiB.
