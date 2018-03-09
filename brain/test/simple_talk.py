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
        "machin truc",
        "c'est pas mon name wesh",
        "oui"
        ]
    talk = ["tu aimes %s ?" % i for i in range(50)]



    for input_item in talk:
        print("> %s" % input_item)
        alan.get_response(input_item)
