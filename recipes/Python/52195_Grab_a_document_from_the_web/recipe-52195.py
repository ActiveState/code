import perl
perl.require("LWP::Simple")
get = perl.get_ref("LWP::Simple::get")

doc = get("http://www.python.org")
print doc
