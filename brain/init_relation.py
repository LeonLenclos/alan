import alan

rel = [
    ("une chaise", "est", "un objet"),
    ("Alan", "est", "un robot"),
    ("Alan", "est", "super"),
    ("Alan", "aime", "les fraises"),
]

neg_rel = [
    ("une chaise", "est", "un aliment"),
    ("Alan", "est", "méchant"),
]
alan = alan.Alan()
for r in rel:
    alan.storage.store_concept_association(*r)
for r in neg_rel:
    alan.storage.store_concept_association(*r, negative=True)
