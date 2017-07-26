Convert = System::Convert
#array of char points
chrs = (65..90), (97..122)
#convert points to symbols
chrs.each do |pnt|
  pnt.each {|i| puts Convert.ToChar(i)}
end
