def test(alan):


    print("\nTEST DE STORAGE")
    print("chaise (id : %i)" % alan.storage.store_concept("une chaise"))
    print("objet (id : %i)" % alan.storage.store_concept("un objet"))
    alan.storage.store_concept_association("une chaise", "est", "un objet")
    alan.storage.store_concept_association("une pince", "est", "un objet")
    alan.storage.store_concept_association("une pince", "est", "un outils")

    print("\nTEST DE DISCUSSION")
    talk = [
        "Salut",
        "ca va ?",
        "t'as dit quoi ?"]

    for input_item in talk:
        print("> %s" % input_item)
        alan.get_response(input_item)
