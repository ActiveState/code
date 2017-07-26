Console       = System::Console
ConsoleColor  = System::ConsoleColor
BitConverter  = System::BitConverter
HashAlgorithm = System::Security::Cryptography::HashAlgorithm

if ARGV.length != 0
  begin
    ARGV.each do |a|
      #retrieve full path for input file(s)
      item = File.expand_path(a)
      #break if file(s) has null length
      if File.lstat(item).size != 0
        Console.foreground_color=ConsoleColor.Green
        puts item
        Console.reset_color
        #available algorithms :)
        ['MD5', 'SHA1', 'SHA256', 'SHA384', 'SHA512', 'RIPEMD160'].each do |type|
          #byte array
          raw = HashAlgorithm.Create(type).ComputeHash(System::IO::File.ReadAllBytes(item))
          #get hashes
          puts BitConverter.ToString(raw).Replace('-', '').ToLower()
        end
      else
        puts "File #{a} has null length."
      end
    end
  rescue Exception => e
    puts e.Message
  end
else
  puts "No one file has been specified."
end
