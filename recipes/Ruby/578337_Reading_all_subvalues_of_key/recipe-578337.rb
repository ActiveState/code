require 'win32/registry'
require 'pp'

Win32::Registry::HKEY_CURRENT_USER.open(
  'Software\Sysinternals'
) do |reg|
  reg.each_key do |key1, key2|
    val = reg.open(key1)
    pp val.inject([]) {|i, j| i << j}
  end
end
