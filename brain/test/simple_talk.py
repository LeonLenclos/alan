def test(alan):
    #
    # print("\nTEST DE STORAGE")
    # print("chaise (id : %i)" % alan.storage.store_concept("une chaise"))
    # print("objet (id : %i)" % alan.storage.store_concept("un objet"))
    # alan.storage.store_concept_association("une chaise", "est", "un objet")
    # alan.storage.store_concept_association("une pince", "est", "un outils")
    # alan.storage.store_concept_association("une choose", "est", "un truc")
    # alan.storage.store_concept_association("un truc", "est", "une chose")
    #

    print("\nTEST DE DISCUSSION")



    talk = [
        "Salut",
        "bob",
        "mon nom est beb",
        "je m'en fous",
        "coucou",
        "coucou",
        "tu es qui ?",
        "Je suis aussi grand que toi",
        "oui",
        "non",
        "oui",
        "non",
        "tu connais quoi ?",
        "tu connais qui ?",
        "et toi ?",
        "bob",
        "mon nom est beb",
        "je m'en fous",
        "coucou",
        "coucou",
        "tu es qui ?",
        "Je suis aussi grand que toi",
        "oui",
        "non",
        "oui",
        "non",
        "tu connais quoi ?",
        "tu connais qui ?",
        "et toi ?",
        "bob",
        "mon nom est beb",
        "je m'en fous",
        "coucou",
        "coucou",
        "tu es qui ?",
        "Je suis aussi grand que toi",
        "oui",
        "non",
        "oui",
        "non",
        "tu connais quoi ?",
        "tu connais qui ?",
        "et toi ?",
        ]



    for input_item in talk:
        print("> %s" % input_item)
        alan.talk(input_item)

