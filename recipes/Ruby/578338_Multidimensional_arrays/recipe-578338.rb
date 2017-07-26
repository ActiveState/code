Console = System::Console

puts 'A rectangular array:'
#wake up, Neo! matrix has you :)
matrix = Array.new(6), Array.new(6)
i = 0
while i < 6
  j = 0
  while j < 6
    Console.Write((matrix[i, j] = i * j).ToString() + "\t")
    j += 1
  end
  puts
  i += 1
end

puts

puts 'A jagged array:'
#it is not a jagged array yet!
jagged = Array.new(5)
#creating jagged array
i = 0
while i < jagged.length
  jagged[i] = Array.new(i + 7)
  i += 1
end
#print contents
i = 0
while i < 5
  Console.Write("Length of row {0} is {1}:\t", i, jagged[i].length)
  j = 0
  while j < jagged[i].length
    Console.Write((jagged[i][j]).ToString() + " ")
    j += 1
  end
  puts
  i +=1
end
