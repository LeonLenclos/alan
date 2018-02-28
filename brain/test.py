def test(alan):
    print("\nTEST DE STORAGE")
    print("chaise (id : %i)" % alan.storage.store_concept("chaise"))
    print("objet (id : %i)" % alan.storage.store_concept("objet"))
    alan.storage.store_concept_association("chaise", "est", "objet")
    alan.storage.store_concept_association("pince", "est", "objet")
    alan.storage.store_concept_association("pince", "est", "outils")

    print("\nTEST DE DISCUSSION")
    talk = [
        "Salut",
        "ca va ?",
        "t'as dit quoi ?",
        "C'est quoi une chaise?"]

    for input_item in talk:
        print("> %s" % input_item)
        alan.get_response(input_item)
