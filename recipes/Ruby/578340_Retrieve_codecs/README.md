## Retrieve codecs  
Originally published: 2012-11-19 08:49:25  
Last updated: 2012-11-19 08:49:26  
Author: greg zakharov  
  
On WinXP (there is no other Windows in my VMWare Player :) you can do it with Ruby in the next way:

require 'win32/registry'

Win32::Registry::HKEY_CLASSES_ROOT.open(
  'CLSID\{083863F1-70DE-11d0-BD40-00A0C911CE86}\Instance'
) do |reg|
  reg.each_key do |key|
    val = reg.open(key)
    puts val['FriendlyName']
  end
end

But what about extended information, aah? I'm talking about script which shows additional data such as CLSID and codec location. With IronRuby it can be done so easy.