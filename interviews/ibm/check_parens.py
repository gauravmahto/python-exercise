# input string ()[]{}. ..WAP to validate the string 

# ([)] => false

# ([]) => true
# ()[]{} => true

def is_valid_par(s):

  b_map = {
    ')': '(',
    ']': '[',
    '}': '{',
  }

  stack = []

  # Iterate through each character in the input string
  for char in s:
    # If the character is a closing bracket
    if char in b_map:
      # Check if the corresponding opening bracket is at the top of the stack
      if stack and stack[-1] == b_map[char]:
        stack.pop()  # Pop the matching opening bracket
      else:
        return False  # Not a valid pair
    else:
      stack.append(char)  # Push opening brackets onto the stack

  # If the stack is empty, all brackets are matched
  return not stack
      

inputs = [
  "()[]{}",
  "([)]",
  "([])"
]
print([is_valid_par(input) for input in inputs])
