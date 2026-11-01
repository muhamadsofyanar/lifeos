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
