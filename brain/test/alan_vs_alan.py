def test(Alan):
    alan = Alan()
    nala = Alan()

    nala_response = alan_response = ""
    for i in range(10):
        alan_response = alan.get_response(nala_response)
        print("> %s" % alan_response)
        nala_response = nala.get_response(alan_response)
        print("> %s" % nala_response)
