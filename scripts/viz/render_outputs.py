#!/usr/bin/env python3
# 렌더 산출물 버전 보관 — 같은 이름으로 덮어쓰지 않고 매번 새 파일로 남긴다
"""Keep every render instead of overwriting it.

Look development is a long sequence of near-misses, and the one from four
tries ago is often the one worth going back to. Writing each render to a fixed
path throws all of that away silently. Everything here goes to
`dist/_scratch/renders/<name>/NNN-<stamp>-<label>.png`, numbered in order, with
a `<name>-latest.png` copy alongside so a habitual path still works.

`dist/` is gitignored, so this is an archive on disk rather than in history —
which is the right place for a few hundred megabytes of look tests.
"""

import os
import shutil
import time

ROOT = 'dist/_scratch/renders'


def save_versioned(image, name, label='', root=ROOT):
    """Write a PIL image as the next numbered version of `name`."""
    folder = os.path.join(root, name)
    os.makedirs(folder, exist_ok=True)
    n = 1 + len([f for f in os.listdir(folder) if f.endswith('.png')])
    stamp = time.strftime('%Y%m%d-%H%M%S')
    tail = f'-{label}' if label else ''
    path = os.path.join(folder, f'{n:03d}-{stamp}{tail}.png')
    image.save(path)
    shutil.copyfile(path, os.path.join(root, f'{name}-latest.png'))
    return path


def versions(name, root=ROOT):
    """Every kept render for `name`, oldest first."""
    folder = os.path.join(root, name)
    if not os.path.isdir(folder):
        return []
    return [os.path.join(folder, f) for f in sorted(os.listdir(folder))
            if f.endswith('.png')]
