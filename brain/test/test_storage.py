def test(alan):

    print("\nTEST DE STORAGE")
    print("chaise (id : %i)" % alan.storage.store_concept("une chaise"))
    print("objet (id : %i)" % alan.storage.store_concept("un objet"))
    alan.storage.store_concept_association("une chaise", "est", "un objet")
    alan.storage.store_concept_association("une pince", "est", "un outils")
    alan.storage.store_concept_association("une choose", "est", "un truc")
    alan.storage.store_concept_association("une chaise", "est", "un aliment", negative=True)

    print(
        alan.storage.get_related_concept(
        "une chose",
        "est",
        negative=True))

    print(
        alan.storage.get_related_concept(
        "une chaise",
        "est",
        negative=True))

    print(
        alan.storage.get_related_concept(
        "une chaise",
        "est",
        negative=False))

    print("is related truc et chose : %s"
        % alan.storage.is_related_concept("un truc", "est", "une chose"))


    talk = [
        "Salut",
        "Salut",
        "Salut",
        "machin truc"
        ]

    for input_item in talk:
        print("> %s" % input_item)
        alan.get_response(input_item)

    print("latest statement logic : %s"
        % alan.storage.get_latest_response_extra_data(extra_data="logic_identifier"))

    print("latest statement speaker : %s"
        % alan.storage.get_latest_response_extra_data(extra_data="speaker"))

    print("conversation count : %s"
        % alan.storage.count_conv(alan.default_conversation_id))
