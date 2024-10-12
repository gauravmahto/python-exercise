import asyncio

async def print_numbers():
  for i in range(10):
    print(i)
    await asyncio.sleep(1)

async def print_letters():
  for letter in "abcde":
    print(letter)
    await asyncio.sleep(1)

async def main():

  # Gather multiple coroutines into one
  await asyncio.gather(print_numbers(), print_letters())
  
  # OR

  # Create tasks
  # t1 = asyncio.create_task(print_numbers())
  # t2 = asyncio.create_task(print_letters())

  # Wait for tasks to complete
  # await t1
  # await t2

asyncio.run(main())
