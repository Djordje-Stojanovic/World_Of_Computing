# I-0282 Image Search And Media Prep Toolchain

Status: promoted setup pass, with 9 pass / 0 warn / 0 fail QA.

## Verified

- Local media-prep packages installed under ignored `.tooling/i0282/python`.
- Candidate intake covers photo, near-duplicate photo, transparent logo, person/profile image, and web-image retrieval/fallback.
- Resizing and cropping produced book-wide, thumbnail, logo-square, and portrait variants.
- Logo alpha channel survived the square derivative.
- Perceptual hashing grouped the deliberate near-duplicate pair.
- Quality scoring records size, aspect ratio, brightness, contrast, sharpness, dominant color, phash, and gate.
- Contact sheet: `assets\source_media\i0282_probe\contact_sheet_i0282.jpg` (ignored raster, visually inspected).

## Limits

- This pass does not promote real photos, logos, or person images into the book.
- Public image retrieval is tested as a workflow; future acquisition rows still need source URL, access date, owner/creator, private-use note, and blocked-claim text.
- Probe rasters and installed packages stay local and ignored.
