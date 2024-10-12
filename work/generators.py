def generator(start, stop):
  for i in range(start, stop):
    yield i

  return "Done"

print(list(generator(0, 10)))

gen = generator(100, 110)

for i in gen:
  print(i)

gen_2 = generator(5, 8)

print(next(gen_2))
print(next(gen_2))
print(next(gen_2))

# Generator expression
squares_gen = (x ** 2 for x in range(2, 5))

print(next(squares_gen))
