from collections import deque


def reverse1(s):
  if not s or len(s) < 2:
    return s
  l = 0
  r = len(s) - 1
  result = list(s)
  while l < r:
    temp = result[l]
    result[l] = result[r]
    result[r] = temp
    l += 1
    r -= 1
  return ''.join(result)


def reverse2(s):
  if not s or len(s) < 2:
    return s
  d = deque(s)
  d.reverse()
  return ''.join(d)


def reverse3(s):
  if not s or len(s) < 2:
    return s
  d = deque()
  for c in s:
    d.append(c)
  result = []
  while len(d):
    result.append(d.pop())
  return ''.join(result)


tests = [
    'abcdefg',
    'a',
    'ab',
    'abc',
    '',
    '123456789',
    '9876543',
]


for t in tests:
  print '%s => %s' % ( t, reverse1(t))
  print '%s => %s' % ( t, reverse2(t))
  print '%s => %s' % ( t, reverse3(t))
