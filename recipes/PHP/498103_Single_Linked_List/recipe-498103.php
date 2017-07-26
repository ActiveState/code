<?php
# Author: Andre Souza <ienliven@gmail.com>
# SingleLinkedList Proposal

class SingleLinkedList
{
    var $_vars;
    var $_next;
    
    function SingleLinkedItem()
    {
        $this->_vars = array();
        $this->_next = null;
    }
    
    private function __get($name)
    {
        if($name == "_last")
        {
            $last =& $this;
            while($last->_next != null)
                $last =& $last->_next;
            return $last;
        }
        
        if(isset($this->_vars[$name])) return $this->_vars[$name];
        else 
        {
            throw new Exception("variable: '$name' not found.");
        }
    }
    
    private function __set($name, $value)
    {
        $this->_vars[$name] = $value;
    }
}


# USE:
for($i = 0; $i < 10; $i++)
{
    if(!isset($SLL))
    {
        $SLL = new SingleLinkedList();
        $SLL->name = "Son_{$i}";
    }
    else
    {
        $SLL->_last->_next = new SingleLinkedList($SLL);
        $SLL->_last->name = "Son_{$i}";
    }
}

var_dump($SLL);
?>
