## Retrieve codecs  
Originally published: 2012-11-19 08:49:25  
Last updated: 2012-11-19 08:49:26  
Author: greg zakharov  
  
On WinXP (there is no other Windows in my VMWare Player :) you can do it with Ruby in the next way:\n\nrequire 'win32/registry'\n\nWin32::Registry::HKEY_CLASSES_ROOT.open(\n  'CLSID\\{083863F1-70DE-11d0-BD40-00A0C911CE86}\\Instance'\n) do |reg|\n  reg.each_key do |key|\n    val = reg.open(key)\n    puts val['FriendlyName']\n  end\nend\n\nBut what about extended information, aah? I'm talking about script which shows additional data such as CLSID and codec location. With IronRuby it can be done so easy.