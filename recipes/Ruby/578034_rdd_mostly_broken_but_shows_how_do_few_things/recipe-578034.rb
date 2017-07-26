#!/usr/bin/env ruby
#----------------------------------------------------------------@@@  Copyright

# Copyright: Mike 'Fuzzy' Partin 2012

#----------------------------------------------------------------@@@    License

# Licensed under the BSD License (Any version you like)

#----------------------------------------------------------------@@@  Changelog

# 02/05/2012 Basic argument handling and inititial code structure coming
#            together nicely.
# 02/05/2012 Have put together a rough draft of the Dd and Buffer classes that
#            Should give us some configurable buffered I/O and let us do some
#            adaption arguments for those variables later on.
# 02/05/2012 Everything but pipe= works at this point.

#----------------------------------------------------------------@@@    Roadmap
#----------------------------------------------------------------@@@   Requires
#----------------------------------------------------------------##      Stdlib

require 'net/ftp'     # Our HTTP/HTTPS/FTP support additions
require 'pty'         # pipe= support

#----------------------------------------------------------------##   3rd Party
#----------------------------------------------------------------##    Internal
#----------------------------------------------------------------@@@  Constants

VERSION = '1.0'
OPTS = {
  :if    => ARGF,        # By default (STDIN or data given on the cmdline)
  :of    => STDOUT,      # By default
  :bs    => 1048576,     # 1M
  :count => nil,         # No defaults
  :pipe  => nil,         # No defaults
  :gauge => 1            # Defaults to on
}
#----------------------------------------------------------------@@@    Modules

module Format
  module_function
  def format_time(secs=nil)
    return "#{secs}s"
  end

  module_function
  def format_size(bytes=nil)
    if bytes/1024 >= 1
      kbytes = Float(bytes)/1024.00
      if kbytes/1024 >= 1
        mbytes = Float(kbytes)/1024.00
        if mbytes/1024 >= 1
          gbytes = Float(mbytes)/1024.00
          retv = '%.02fTB' % Float(gbytes)/1024.00 if gbytes/1024 >= 1
          retv = '%.02fGB' % gbytes
        else
          retv   = '%.02fMB' % mbytes
        end
      else
        retv     = '%.02fKB' % kbytes
      end
    else
      retv       = '%dB' % bytes
    end
    return retv
  end

end

#----------------------------------------------------------------@@@    Classes

class DD
  include Format

  def initialize(args={})
    @OPTS = OPTS
    # This next bit only enforces that we get only supported options given
    # to us, and just ignores everything we don't know about entirely.
    OPTS.keys.each {|i| @OPTS[i] = args[i] if args.keys.include? i}
  end

  def gauge(cur=nil, tot=nil)
    if @OPTS[:gauge].to_i == 1 and ![cur, tot].include? nil
      STDERR.write "%8s of %8s (%3d%%)     \r" % [
        format_size(cur),
        format_size(tot),
        (Float(cur) / Float(tot)) * 100
      ] if tot > 0
      STDERR.write "%8s written     \r" % format_size(cur) if tot == 0
      STDERR.flush
    end
  end

  def transfer
    begin
      cnt         = 0
      tot         = 0
      STDERR.sync = true

      # Ok, now that the options and vars are all setup, lets take a few to
      # worry about our output and it's setup.
      @OPTS[:out] = File.open(@OPTS[:of], 'w+') if OPTS[:of]

      # And now lets setup our input and gets shit rollin
      if @OPTS[:if] =~ /^ftp:\/\/.*$/
        if_split = @OPTS[:if].split('/')
        info = {
          :path => "/#{if_split[3..(if_split.size - 2)].join('/')}",
          :file => @OPTS[:if].split('/')[(@OPTS[:if].split('/').size - 1)],
          :host => @OPTS[:if].split('/')[2],
          :user => 'ftp',
          :pswd => 'look@my.ass'
        }
        if info[:host] =~ /^.*:.*@.*$/
          info[:user], info[:pswd] = info[:host].split('@')[0].split(':')
          tmp = info[:host].split('@')[1]
          info[:host] = tmp
        end
        ftp = Net::FTP.open(info[:host], user=info[:user], passwd=info[:pswd])
        ftp.passive=true
        ftp.chdir(info[:path])
        size = ftp.size(info[:file])
        if @OPTS[:pipe]
          begin
            null = '/dev/null'
            IO.popen(@OPTS[:pipe], 'w') do|tmp|
              @OPTS[:out] = tmp
              begin
                ftp.getbinaryfile(info[:file], null, @OPTS[:bs].to_i) do|blk|
                  break if @OPTS[:count] and cnt == @OPTS[:count].to_i
                  @OPTS[:out].write(blk)
                  @OPTS[:out].flush
                  cnt += 1
                  tot += blk.size
                  gauge(tot, size)
                end
              end
            end
          end
        else
          ftp.getbinaryfile(info[:file], '/dev/null', @OPTS[:bs].to_i) do|blk|
            break if @OPTS[:count] and cnt == @OPTS[:count].to_i
            @OPTS[:out].write(blk)
            cnt += 1
            tot += blk.size
            gauge(tot, size)
          end
        end
        puts
      elsif @OPTS[:if] =~ /^(\.|\/|\~|[a-z]+).*$/
        @OPTS[:in]  = File.open(@OPTS[:if], 'r')
        size = @OPTS[:in].size
        if @OPTS[:pipe]
          begin
            null = '/dev/null'
            IO.popen(@OPTS[:pipe], 'w') do|tmp|
              @OPTS[:out] = tmp
              begin
                while 1
                  break if @OPTS[:count] and cnt == @OPTS[:count].to_i
                  blk = @OPTS[:in].read(@OPTS[:bs])
                  break if !blk
                  @OPTS[:out].write(blk)
                  cnt += 1
                  tot += blk.size
                  gauge(tot, size)
                end
              end
            end
          end
        else
          while 1
            break if @OPTS[:count] and cnt == @OPTS[:count].to_i
            blk = @OPTS[:in].read(@OPTS[:bs])
            break if !blk
            @OPTS[:out].write(blk)
            cnt += 1
            tot += blk.size
            gauge(tot, size)
          end
        end
        puts
      end
    rescue NoMethodError => msg
      puts msg
      puts 'debug your shit yo'
      exit
    end
  end
end

#----------------------------------------------------------------@@@    Methods

def usage
  puts "\nAdd (Advanced dd) v#{VERSION}"
  puts "\nUsage:"
  puts "add [opts]"
  puts "\nSupported options:"
  puts 'if=<INPUT> (currently supports ftp/file/stdin: DEFAULT stdin)'
  puts 'of=<OUTPUT> (supports file/stdout: DEFAULT stdout)'
  puts 'bs=<BLOCK_SIZE> (default 1M)'
  puts 'count=<ITERATIONS> (no defaults)'
  puts 'pipe=<COMMAND> (no defaults)'
  puts 'guage=(0|1)'
  puts "\nExample:"
  puts 'add if=ftp://10.0.0.1/src.tar.bz2 bs=1M pipe="tar -C /usr/src -jxf -"'
  puts
end

#----------------------------------------------------------------@@@ Main Logic

ARGV.each do|arg|
  if arg =~ /^.*help.*$/
    usage
    exit
  elsif arg =~ /^.*=.*$/
    key, val = arg.split('=')
    OPTS[key.to_sym] = val if OPTS.keys.include? key.to_sym
  end
end
# One final check, if OPTS[:pipe] is != nil, then OPTS[:of] must == nil as
# they are mutually exclusive. Pipe always overrides OPTS[:of]
OPTS[:of] = nil if OPTS[:pipe] != nil

begin
  o = DD.new(OPTS)
  o.transfer
rescue ArgumentError => msg
  puts msg
  usage
  exit
rescue Interrupt
  exit
end

#----------------------------------------------------------------@@@        End
