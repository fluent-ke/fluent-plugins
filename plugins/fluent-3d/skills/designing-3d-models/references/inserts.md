# NFC tags and other inserts

## Method

One print that pauses, not two glued halves: model a sealed pocket, pause before the layer that roofs it, drop the insert in, resume. NFC keychains on MakerWorld use this, and tag sellers offer 25 mm tags made for it with a "26x1 mm slot".

## Geometry

| Rule | Value |
|---|---|
| Pocket | tag diameter + 1 mm; depth at least the tag thickness (26 x 1 mm for a 25 mm NTAG213) |
| Under the tag | at least 1.2 mm |
| Over the tag | about 1–2 mm reads best; phone read range is 2–5 cm |
| Heights | pocket floor and roof on layer-height multiples |
| Metal | none behind or near the antenna |
| Magnets and nuts | pocket 0.1–0.2 mm oversize; the insert must sit flush with or below the rim |

## Pause

- Pause height = pocket roof + one layer height. Earlier and the walls are unfinished; later and the insert is buried or knocked loose by the nozzle.
- Avoid pausing in the first few layers.
- The bed stays hot while paused, so resume promptly. A faint line can show on the side wall at that height.

## The tag

1. Buy genuine NTAG213 (144 bytes, plenty for a URL) or NTAG215.
2. Program the URL before printing (a URI record in an app such as NFC Tools) and test it on an iPhone and an Android phone.
3. At the pause: peel the backing, press the tag flat adhesive-side down, check it sits below the rim, resume.
4. Tap-test the finished part. Lock the tag only once the URL is final.

## Sources

- [Premy: pausing at a layer in Bambu Studio](https://premy.co/en/blog/bambu-studio-pause-at-layer)
- [MakerWorld: Keychain with integrated NFC tag](https://makerworld.com/en/models/134452-keychain-with-integrated-nfc-tag)
- [lostboyslab: 25 mm NFC tag for integration during 3D printing](https://www.lostboyslab.shop/products/nfc-tag-25-mm-for-integration-during-3d-printing-100)
- [PrintPal: embedding NFC tags in 3D prints](https://printpal.io/resources/how-to-use-nfc-tags-in-3d-prints)
- [Threads: tag flew off after a mistimed pause](https://www.threads.com/@prettywiredbuilds/post/DOkk44AFWmm)
