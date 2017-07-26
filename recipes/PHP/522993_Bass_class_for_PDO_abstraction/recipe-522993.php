<?php

class Foo extends PDO {
  /*
  * __constructor: create a new Foo object
  * @ param $cfg: usually a STDClass object with these properties
  * stdClass Object
  (
  [host] => localhost
  [db] => mysql
  [user] => username
  [pass] => password
  )
  */
  private $cfg;
  public $dsn;
  
  function __construct($cfg) {
    try {
      $this->dsn = "mysql:host=$cfg->host;dbname=$cfg->db";
      parent::__construct($this->dsn, $cfg->user, $cfg->pass);
      $this->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); // throw exceptions
      $this->cfg = $cfg;
    }
    catch(Exception $e) {
      // XXX need to look for Array output on all ops
      print "Error: " . $e->getMessage();
    }
  }
  
  /* implement crazy code here */
  
  
  
  /* handy utility functions */
  
  function _getAsRow($sql, $i = 0) {
    try {
      $sth = $this->query($sql);
      $arr = $sth->fetchAll();
      $out = array();
      foreach($arr as $row) {
        $out[] = $row[$i];
      }
      return array(
        1,
        $out
      );
    }
    catch(Exception $e) {
      return $this->_err($e);
    }
  }
  // get all data returned by the query
  
  function _getRows($sql) {
    try {
      $sth = $this->query($sql);
      return array(
        1,
        $sth->fetchAll(PDO::FETCH_ASSOC)
      );
    }
    catch(Exception $e) {
      return $this->_err($e);
    }
  }
  /* run a query that doesn't return data, we want the affected rows instead */
  
  function boolQuery($sql) {
    try {
      $sth = $this->query($sql);
      return array(
        1,
        $sth->rowCount
      );
    }
    catch(Exception $e) {
      return $this->_err($e);
    }
  }
  /* return the expected error structure */
  private function _err($e) {
    return array(
      0,
      $e->getMessage()
    );
  }
  // dumper
  
  function _dump($data) { // pass in $_GET, etc
    $args = func_get_args();
    if (count($args) > 1) {
      return "\n<pre>\n" . print_r($args, 1) . "\n</pre>\n";
    } else {
      return "\n<pre>\n" . print_r($data, 1) . "\n</pre>\n";
    }
  }
}
