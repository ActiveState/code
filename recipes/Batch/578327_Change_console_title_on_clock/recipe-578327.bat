@echo off
:begin
1>nul ping -n 2 127.0.0.1
title %time:~0,8% & goto:begin
