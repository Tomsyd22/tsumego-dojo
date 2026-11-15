# Tsumego Dojo 詰碁

A fast, focused Go (baduk / weiqi) problem trainer that runs entirely in the browser. It's one HTML file with no build step, no account and no server.

Built by Tom Chen: 6-dan amateur, former Australian Go Champion, and six-time international representative for Australia.

## Features

- **Practice**: work through problems by rank (30k to 9d) and category. You can shuffle, skip problems you've solved, and rotate or flip each problem so you can't memorise the shape.
- **Rush**: 3-minute, 5-minute and Survival runs. Difficulty climbs as you go, and your best scores are saved.
- **Ladder**: a rank ladder that moves up and down with your results.
- **Real solution trees**: wrong moves get a refutation from the opponent. You can step back, retry, ask for a hint, or reveal the solution.
- **Bring your own problems**: open any folder of `.sgf` files. Rank folders (`12k`, `3d` …) set the difficulty.
- Keyboard-first (`←` `→` problems, `R` retry, `B` back, `H` hint, `A` solution), with light and dark themes. Works on phones.
- Progress is stored locally in your browser. Nothing is sent anywhere.

## Run it

```bash
git clone https://github.com/Tomsyd22/tsumego-dojo
cd tsumego-dojo
python3 -m http.server 8000
# open http://localhost:8000
```

Opening `index.html` directly also works for your own SGF folders. The built-in library needs the small local server because browsers block `fetch` on `file://`.

## Build a library from your own problems

Put one `.sgf` per problem in a folder per rank, then build:

```
sgf/
  30k/1.sgf
  25k/1.sgf
  3d/17.sgf
```

```bash
python3 tools/build_data.py sgf --out data
```

This writes `data/index.json`, chunked problem files (loaded only when needed), and `data/rush/index.json` for Rush mode.

**SGF conventions**
- Black or White to play is set with `PL[B]` / `PL[W]`.
- Mark winning lines with `RIGHT` at the start of the final move's comment, and failing lines with `WRONG`. Any move that isn't in the tree, or a line that ends without a mark, counts as wrong. If a problem has no `RIGHT` marks at all, reaching the end of the main line counts as solved.
- An optional `Type: life_and_death` line in the root comment sets the category (`life_and_death`, `tesuji`, `joseki`, `fuseki`, `endgame`, `best_move`, `elementary`, `other`).

The repo ships with three original sample problems so it works straight away. **Only build and publish problems you have the right to share.** Problem collections on other sites belong to their authors.

## Contributing

Issues and pull requests are welcome, especially:
- original problems with checked solution trees (every one is reviewed before it's merged)
- SGF edge cases the parser gets wrong
- accessibility and mobile improvements

## License

[MIT](LICENSE) © 2026 Tom Chen
