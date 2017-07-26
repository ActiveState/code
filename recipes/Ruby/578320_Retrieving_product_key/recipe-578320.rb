require 'System, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'

Registry = Microsoft::Win32::Registry

def DecodeProductKey(digitalProductID)
  map = ("BCDFGHJKMPQRTVWXY2346789").split('')
  key = []
  raw = []

  i = 52
  while i < 67:
     raw.Add(digitalProductID[i])
     i += 1
  end

  i = 28
  while i >= 0
     if (i + 1) % 6 == 0
        key[i] = '-'
     else
        k = 0
        j = 14
        while j >= 0
           k = (k * 256) ^ raw[j]
           raw[j] = (k / 24)
           k %= 24
           key[i] = map[k]
           j -= 1
        end
     end
     i -= 1
  end

  return key.to_s
end

def GetProductKey(key, val = 'DigitalProductId')
  reg = Registry.LocalMachine.OpenSubKey(key).GetValue(val)
  puts DecodeProductKey(reg)
end

GetProductKey('SOFTWARE\Microsoft\Windows NT\CurrentVersion')
