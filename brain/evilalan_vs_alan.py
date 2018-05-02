#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This is the conversation between Alan and his perfect twin : Evil Alan

from alan import Alan

evil_alan = Alan(settings_files=['evilalan'])
evil_alan.name = "Evil Alan"
alan = Alan(settings_files=['base', 'interface/vs', 'logic'])

print("---------------")
print(alan.status())
print("----- VS ------")
print(evil_alan.status())
print("---------------")

last_response = 'Alors, Alan'
while True:
    last_response = evil_alan.get_response(alan.get_response(last_response))

print("---------------")
