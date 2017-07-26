def groupbyUnsorted(input, key=lambda x:x):
  yielded = set()
  keys = [ key(element) for element in input ]
  for i, wantedKey in enumerate(keys):
    if wantedKey not in yielded:
      yield (wantedKey,
          (input[j] for j in range(i, len(input)) if keys[j] == wantedKey))
    yielded.add(wantedKey)
