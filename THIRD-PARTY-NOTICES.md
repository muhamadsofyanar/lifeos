# Third-party data and references

## Tanzil Quran metadata

Source: Tanzil Project, Quran Metadata v1.0
https://tanzil.net/docs/Quran_Metadata
Original download: https://tanzil.net/res/text/metadata/quran-data.xml

The source XML declares copyright (C) 2008–2009 Tanzil.info and license `cc-by`. An unchanged copy is included at `sources/quran-data.xml`. Generated `static/quran-meta.json` contains chapter labels and page boundaries derived from that source; it does not contain Quran verse text. Conversion expands page start markers into human-readable chapter/verse ranges. App guidance preserves the distinction between a page reference and a smaller line-based memorization unit.

The separate `unitTargets` records for Juz 29 were transcribed from the user's uploaded Jilid 2 mutabaah, not from Tanzil. They identify ranges as printed and do not reproduce verse text or full book pages. These are personal-study adaptations; no rights to redistribute the complete uploaded books are implied.

## Browser API implementation references

https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder
https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/isTypeSupported_static
https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia

No external runtime audio service or remote Quran metadata request is required by the application. All recording storage remains on the configured server volume.


## Quran text Uthmani v1.1

Source: https://tanzil.net/download/
Raw source URL used: https://tanzil.net/pub/download/index.php?quranType=uthmani&outType=txt&agree=true
File: static/quran-uthmani.txt. Downloaded 2026-11-01. The raw file and its full copyright block are unmodified; reader displays the corresponding verse lines without rewriting. License and attribution: https://tanzil.net/docs/Text_License.

SHA-256: ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af

## Amiri Quran font

Source: https://github.com/google/fonts/tree/main/ofl/amiriquran
Files: static/AmiriQuran-Regular.ttf and static/AmiriQuran-OFL.txt. License: SIL Open Font License 1.1.
