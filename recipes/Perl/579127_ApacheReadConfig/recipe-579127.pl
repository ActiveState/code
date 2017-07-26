apache_config.pl
  ---------------- 
  package Apache::ReadConfig;
  
  $ServerName = `hostname`;
  if ( $ServerName !~ /^secure/) {
    $UserDir = "/var/www/httpdocs/";
  } else {
    $UserDir = "DISABLED";
  }
  
  1;

  httpd.conf
  ----------
  PerlRequire /var/www/httpdocs/perl/lib/apache_config.pl
  $Apache::Server::StrictPerlSections = 1
/usr/lib/apache/mod_include_modperl.so
/usr/sbin/httpdocs_modperl
