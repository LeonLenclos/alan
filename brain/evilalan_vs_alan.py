#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This is the conversation between Alan and his perfect twin : Evil Alan

from alan import Alan

evil_alan = Alan(settings_files=['evilalan'])
evil_alan.name = "Evil Alan"
alan = Alan(settings_files=['base', 'interface/none', 'logic'])

print("---------------")
print(alan.status())
print("----- VS ------")
print(evil_alan.status())
print("---------------")

alan_rep = 'Alors, Alan'
print("- {}".format(alan_rep))
evilalan_rep = ''
while True:
	evilalan_rep = evil_alan.get_response(alan_rep)
	print("- {}".format(evilalan_rep))
	alan_rep = alan.get_response(evilalan_rep)
	print("- {}".format(alan_rep))

print("---------------")
