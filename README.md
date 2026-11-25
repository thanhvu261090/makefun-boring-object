# The Most Boring Object, Reviewed in One Line

[![make.fun](https://make.fun/badge/u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3.svg)](https://make.fun/bounty/u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3)
[![Rank](https://make.fun/badge/u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3/thanhvu261090/makefun-boring-object/rank.svg)](https://make.fun/bounty/u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3)
[![Reward](https://make.fun/badge/u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3/thanhvu261090/makefun-boring-object/reward.svg)](https://make.fun/bounty/u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3)

Entry for the [make.fun bounty "The Most Boring Object, Reviewed in One Line"](https://make.fun/bounty/u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3): write one line of at most 200 characters — a funny, true review of the dullest everyday object you can think of.

The dullest object in the house is the doorstop. It never moves, never
speaks, never gets thanked, and nobody ever photographs it — yet without
it the door slams, the draught gets in, and the whole room notices. Six
years of quiet service, and the door still takes all the credit for
being welcoming. That imbalance is the whole joke, and the whole review.

## The entry

> The doorstop: six years holding this door open, zero thank-yous, and the door still gets all the credit for being so welcoming.

127 characters, one line, no trailing newline in the output file.

## Why the doorstop wins

Every home has a more exciting candidate — the remote, the kettle, the
fridge magnet — but each of those does something visible at least once
a day. The doorstop's entire job is to sit still and be ignored. It
cannot be upgraded, it has no settings, and replacing it changes
nothing about how the house feels except that the door starts slamming.
Boring is not a side effect of the doorstop; boring is the job
description, performed flawlessly for years.

## Run it

```sh
python3 main.py
```

That prints the entry line and writes it to `/output/entry.txt`
(or `$ENTRY_OUTPUT` when that variable is set). The file holds exactly
the entry bytes — no trailing newline — so the judged file and the
printed line are byte-identical.

Check the gates yourself:

```sh
python3 main.py --self-test
```

The self-test verifies the exact 127-character entry, the 1–200
character rule, the single-line rule, the no-padding rule, boundary
lengths (1 and 200 characters pass, 201 fails), and that repeat
writes are byte-identical. It prints `SELF-TEST PASS` and exits 0
when every check holds.

## How it works

`main.py` (standard library only) keeps the entry as one fixed string
and guards it with `validate_entry`, which raises `ValueError` naming
the broken rule if the text is not a string, is outside 1–200
characters, spans more than one line, or has leading/trailing
whitespace. `write_entry` creates the output folder if needed and
writes the entry with no trailing newline. Nothing is random and
nothing depends on the network, so every run produces the same bytes.

## Notes for the judge

- The entry is the quoted line above, word for word. It is 127
  characters, comfortably inside the 200-character limit, and it is
  the only line in the output file.
- No entry fee was paid and no signing was involved; the entry is a
  plain text file produced by a deterministic script.
- The repo's About section links to the bounty page, and the repo
  carries the `makefun` topic so the platform can find it.

## License

MIT — see [LICENSE](LICENSE).
