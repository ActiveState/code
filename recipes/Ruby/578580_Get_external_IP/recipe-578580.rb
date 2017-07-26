#!/usr/bin/env ruby
require 'open-uri'
open("http://internet.yandex.ru/"){|f|f.read.scan(/IPv4:\s(\d+\.){3}\d+/);puts $~}
