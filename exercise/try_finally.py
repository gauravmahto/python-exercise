def foo():
    try:
        return 1
        print("Hello")
    finally:
        print("HI")
        return 2

k = foo()
print(k)
