# audacity2LMS
I saw a video by John Storms about [Polyphonic Transcription](https://youtu.be/SeoQSE3FlBc), but his script spits out XML snippets to manually copy and paste into an LMS file. He wanted a program that uses an XML library, so I created this Python script that handles sequence data with ElemenTree.

Features:
- Modifies LMS sequences by translating Audacity polyphonic transcription. 
- Automatically applies effects and timing tracks.


Possible new features to add:
- Multiple timing track processing
- Optional LMS synthesis (wouldn't require a starter lms file)
- Track color chooser
- Optional output filename chooser
- Ability to trim output tracks (currently outputs all 128 MIDI tracks)
