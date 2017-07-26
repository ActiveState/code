#!/usr/bin/perl
use LWP::Simple;

if ((get "http://internet.yandex.ru/") =~ /(IPv4:\s(\d+\.){3}\d+)/) {
   print($&, "\n");
}
