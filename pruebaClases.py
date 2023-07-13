from clasesExtra import SetItemsLR0

s1 = SetItemsLR0()

s1.agregar(23, 45)
# s1.agregar(23, 45)

for item in s1.conjunto:
    print(item.to_string)
