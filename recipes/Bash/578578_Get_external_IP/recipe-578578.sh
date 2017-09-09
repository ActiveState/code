wget -qO - http://icanhazip.com | grep ^
# or
lynx --dump http://icanhazip.com | grep ^ | head -1
# or
curl -s http://icanhazip.com | grep ^
