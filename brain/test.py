def test(alan):

    print("\nTEST DE DISCUSSION")
    talk = [
        "Salut",
        "ca va ?",
        "t'as dit quoi ?"]

    for input_item in talk:
        print("> %s" % input_item)
        alan.get_response(input_item)

    print("\nTEST DE STORAGE")
    print("chaise (id : %i)" % alan.storage.store_concept("chaise"))
    print("objet (id : %i)" % alan.storage.store_concept("objet"))
