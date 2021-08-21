# keyboard_distance
Code for computing distance fingers move while typing.

Inspired by [Matt Parker's video](https://youtu.be/Mf2H9WZSIyw).

## `two_finger.py`
Computes minimum distance required to type words using the two-finger "hunt and peck" method.
Makes no assumptions about what side of the keyboard each finger belongs to, so may find some solutions that are impossible if you have arms.

`./two_finger.py [path/to/dictionary]` will read words from the given dictionary file (default: `dictionary.txt`) and print out a TSV of (sanitized) words and the minimum distance required to type that word using two fingers.
