import sys, base64

if len(sys.argv) < 3:
    print """Usage: %s in_b64_enc_file out_dec_file
    
              in_b64_enc_file  - The Base64 encoded file to be converted
              out_dec_file     - The output decoded file
          """%sys.argv[0]
    sys.exit(0)

base64.decode(open(sys.argv[1], 'rb'), open(sys.argv[2], 'wb')) 
