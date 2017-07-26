wget -qO - http://internet.yandex.ru | grep IPv4 | awk '{print($2,$3)}'
# or
wget -qO - http://internet.yandex.ru | grep -oP 'IPv4:\s(\d+\.){3}\d+'
# or
lynx --dump http://internet.yandex.ru | grep IPv4 | awk '{print($2,$3)}'
