i = 0
try:
  while True:
      print(i)
      i +=1 
      if (i > 10):
        raise Exception('More than 10')
      if (i > 5):
        raise Exception('More than 5 okay')
except Exception as e:
    if (e.args[0] == 'More than 10'):
      raise e
    else:
      pass
