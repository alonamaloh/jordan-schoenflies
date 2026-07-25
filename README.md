# The Jordan–Schönflies theorem

A complete, elementary proof that every homeomorphism between two Jordan
curves extends to a homeomorphism of the plane.

Nothing heavier than metric topology of the plane, compactness, and finite
graph theory goes in. The Jordan curve theorem and the crosscut theorem are
not assumed — they are proved along the way.

## The two documents

| File | Pages | What it is |
| --- | --- | --- |
| [`jordan_schoenflies_compact.tex`](jordan_schoenflies_compact.tex) | 25 | The paper. Written at ordinary mathematical granularity, with figures. |
| [`jordan_schoenflies.tex`](jordan_schoenflies.tex) | 49 | The same proof expanded to formalization granularity, with a statement-level citation index, a suggested module order, and an explicit imported-background appendix. |

Both follow the same route and are sectioned alike, so any step in the
compact paper can be expanded by consulting the long one. Where they differ,
it is because an argument has been shared between two places in the compact
text rather than written out twice; the long text also splits faces by a
whole ear where the compact one inserts a single crosscut edge.

Compiled PDFs are committed alongside the sources.

## The route

**Part I — separation.** For a polygonal curve, separation is arithmetic: a
point is inside precisely when a horizontal ray to the right crosses the
curve an odd number of times. Two-sided strips bound the number of
complementary regions by two; the crossing parity shows the bound is
attained; and the identity `π_C = π_{J₁} + π_{J₂}` is the whole of the
polygonal crosscut theorem. From that follows the one nonplanarity fact
needed — that `K₃,₃` has no plane drawing — which is the lever that reaches
arbitrary curves. A curve that failed to separate would let us draw `K₃,₃`;
so would a curve whose complement had three regions. A simple arc cannot
separate, because a chain of small squares laid along it has a corridor for
an outer face. Those three facts are the Jordan curve theorem.

Part I never approximates a Jordan curve by polygons. It approximates the
paths that would have to cross it, which is far cheaper to control.

**Part II — extension.** No homeomorphism from the closed Jordan domain to a
square is ever written down. Instead a sequence of finite combinatorial
matches is built: pairs of finite cell decompositions, one of the domain and
one of the square, isomorphic to each other and already agreeing with the
given boundary map. A refinement made on either side can be copied to the
other, because both sides are at every finite stage plane graphs governed by
the crosscut theorem. Alternating the two directions drives the cells small
on both sides at once, each point of the domain comes to sit in a nested
sequence of closed stars whose partners shrink to a single point, and that
point is its image. Inversion handles the exterior.

## Building

Requires a TeX distribution with `mathpazo`, `microtype`, `tikz`, and
`caption`. No bibliography processor is needed.

```sh
pdflatex jordan_schoenflies_compact.tex   # run twice, for cross-references
pdflatex jordan_schoenflies.tex           # run three times, for the table of contents
```

## License

[CC BY 4.0](LICENSE). Share and adapt with attribution.
