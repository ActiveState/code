<?php

/* A basic data class sort-of based on Ruby Structs */
class Struct implements Iterator {
    
    /* protected array that contains the class properties */
    protected $_data;
    
    /* constructor, takes in data */
    function __construct($mixed=array()) {

        $this->_data = array();

        if (!is_array($mixed) || func_num_args() > 1) {
            $mixed = func_get_args();
        }
        
        if ($this->_isAssoc($mixed)) {
            foreach ($mixed as $prop => $val) {
                if (!is_numeric($prop)) {
                    $this->_data[$prop] = $val;
                }
            }
        }
        else {
            foreach ($mixed as $prop) {
                if (!is_numeric($prop)) {
                    $this->_data[$prop] = FALSE;
                }
            }
        }
    }
    
    /* utility function to decide if an array is associative */
    protected function _isAssoc($var) {
        return is_array($var) && array_diff_key($var, array_keys(array_keys($var)));
    }
    
    /* implementation of __set, just chucks stuff in _data */
    function __set($name, $value) {
        $this->_data[$name] = $value;
    }
    
    /* grabs stuff from _data */
    function __get($name) {
        if (isset($this->_data[$name])) {
            return $this->_data[$name];
        }
        return FALSE;
    }
    
    function rewind() {
        reset($this->_data);
    }
    
    function current() {
        return current($this->_data);
    }
    
    function key() {
        return key($this->_data);
    }
    
    function next() {
        return next($this->_data);
    }
    
    function valid() {
        return ($this->current() !== FALSE);
    }
}
