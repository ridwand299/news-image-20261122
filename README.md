# Sum up 22 November's world news in one image

Entry for make.fun bounty `news-image-20261122` — $100, 50 places paid
(1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20).
Deadline: Tuesday 24 Nov 2026, 07:00 WIB (00:00 UTC).

## Files
- `entry.png` — the image (1024×1024, 138724 bytes, under the 1 MiB limit)
- `main.py` — stdlib-only program that copies `entry.png` to `/output/entry.png`
- `build_image.py` — the Pillow script that rendered `entry.png` (for editing/rebuilding)

## The image
A newspaper front page: 31 stories in 7 regions, all dated Sunday 22 November 2026,
with a numbers strip, a UTC timeline, 3 illustrated lead stories, 10 small cards,
an 18-story "Also on Sunday" list, a schematic world map, and a DATE CHECK box.

Lead stories: COP31 ends without a deal in Antalya; Iran claims US radars hit in
Bahrain; Russia fires 186 drones at Ukraine overnight.

A red breaking banner at the top, clearly dated Mon 23 Nov and not counted in
the 31, notes: Jensen Huang is back — Nvidia reinstates its CEO, shares +30%.

Sources checked 24 Nov 2026: Daily Summary of World 22 Nov 2026, KPFA, IANS,
Reuters, BBC, Al Jazeera, AP, AFP. Figures may be revised.

## Verified locally (24 Nov 2026, ~00:14 WIB)
- `python3 main.py` run twice → identical SHA-256 as `entry.png`
  (`4a6ea3ead2a6bfda5454923bd9b1f00f7866ba9531a89cf0bbfbc556ea01b215`)
- `python3 build_image.py` → 1024×1024 PNG, < 1 MiB
- Image visually checked: all 31 stories + map + date check fit, no clipped text.
