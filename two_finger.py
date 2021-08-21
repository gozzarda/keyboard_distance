#! /usr/bin/env python3

import numpy as np
import sys


class Keyboard:
    def __init__(self, layout, row_offsets, spacing_horz, spacing_vert):
        self.layout = layout
        self.row_offsets = row_offsets
        self.spacing_horz = spacing_horz
        self.spacing_vert = spacing_vert
        self.key_vecs = {}
        self.key_dists = {}

    def gen_key_vecs(self):
        self.key_vecs = {}
        for r, (row, offset) in enumerate(zip(self.layout, self.row_offsets)):
            for c, key in enumerate(row):
                self.key_vecs[key.upper()] = np.array(
                    [offset + c * self.spacing_horz, -r * self.spacing_vert])
        return self.key_vecs

    def key_dist(self, src, dst):
        if (src, dst) in self.key_dists:
            return self.key_dists[(src, dst)]
        if not self.key_vecs:
            self.gen_key_vecs()
        if src not in self.key_vecs:
            return 0
        if dst not in self.key_vecs:
            return 0
        dist = np.linalg.norm(self.key_vecs[dst] - self.key_vecs[src])
        self.key_dists[(src, dst)] = dist
        self.key_dists[(dst, src)] = dist
        return dist

    def reduce_word(self, word):
        if not self.key_vecs:
            self.gen_key_vecs()
        return ''.join(filter(lambda c: c in self.key_vecs, word.upper()))


KEY_SPACING = 19.05
QWERTY = Keyboard(layout=[
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M'], ],
    row_offsets=[0, KEY_SPACING / 4, KEY_SPACING * 3 / 4],
    spacing_horz=KEY_SPACING,
    spacing_vert=KEY_SPACING
)


def word_dist(word, keyboard=QWERTY):
    word = keyboard.reduce_word(word)

    dpt = {}

    def dp(rem=len(word), lkey=None, rkey=None):
        if rem == 0:
            return 0
        if (rem, lkey, rkey) in dpt:
            return dpt[(rem, lkey, rkey)]
        best = min(
            dp(rem - 1, word[rem - 1], rkey) + keyboard.key_dist(lkey, word[rem - 1]),
            dp(rem - 1, lkey, word[rem - 1]) + keyboard.key_dist(rkey, word[rem - 1])
        )
        dpt[(rem, lkey, rkey)] = best
        return best

    return dp(), word


def main():
    dict_path = 'dictionary.txt'
    try:
        dict_path = sys.argv[1]
    except IndexError:
        pass

    print(f'Loading dictionary from {dict_path}...', file=sys.stderr)
    words = None
    with open(dict_path, 'r') as dict_file:
        words = [word for word in dict_file]
    if not words:
        print('Failed to load dictionary', file=sys.stderr)
        return
    print(f'DONE: Loaded {len(words)} words', file=sys.stderr)

    print('Computing word distances...', file=sys.stderr)
    word_dists = list(map(word_dist, words))
    print('DONE', file=sys.stderr)

    print('Sorting words by distance...', file=sys.stderr)
    word_dists.sort()
    print('DONE', file=sys.stderr)

    for dist, word in word_dists:
        print(word, round(dist, 2), sep='\t')


if __name__ == '__main__':
    main()
