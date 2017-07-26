<?php

/** 
* Title: Single linked list
* Description: Implementation of a single linked list in PHP 
* @author Sameer Borate | codediesel.com
* @version 1.0 20th June 2008
*/

class ListNode
{
    /* Data to hold */
    public $data;
    
    /* Link to next node */
    public $next;
    
    
    /* Node constructor */
    function __construct($data)
    {
        $this->data = $data;
        $this->next = NULL;
    }
    
    function readNode()
    {
        return $this->data;
    }
}


class LinkList
{
    /* Link to the first node in the list */
    private $firstNode;
    
    /* Link to the last node in the list */
    private $lastNode;
    
    /* Total nodes in the list */
    private static $count;
    
    
    
    /* List constructor */
    function __construct()
    {
        $this->firstNode = NULL;
        $this->lastNode = NULL;
        self::$count = 0;
    }

    public function isEmpty()
    {
        return ($this->firstNode == NULL);
    }
    
    public function insertFirst($data)
    {
        $link = new ListNode($data);
        $link->next = $this->firstNode;
        $this->firstNode = &$link;
        
        /* If this is the first node inserted in the list
           then set the lastNode pointer to it.
        */
        if($this->lastNode == NULL)
            $this->lastNode = &$link;
            
        self::$count++;
    }
    
    public function insertLast($data)
    {
        if($this->firstNode != NULL)
        {
            $link = new ListNode($data);
            $this->lastNode->next = $link;
            $link->next = NULL;
            $this->lastNode = &$link;
            self::$count++;
        }
        else
        {
            $this->insertFirst($data);
        }
    }
    
    public function deleteFirstNode()
    {
        $temp = $this->firstNode;
        $this->firstNode = $this->firstNode->next;
        if($this->firstNode != NULL)
            self::$count--;
            
        return $temp;
    }
    
    public function deleteLastNode()
    {
        if($this->firstNode != NULL)
        {
            if($this->firstNode->next == NULL)
            {
                $this->firstNode = NULL;
                self::$count--;
            }
            else
            {
                $previousNode = $this->firstNode;
                $currentNode = $this->firstNode->next;
                
                while($currentNode->next != NULL)
                {
                    $previousNode = $currentNode;
                    $currentNode = $currentNode->next;
                }
                
                $previousNode->next = NULL;
                self::$count--;
            }
        }
    }
    
    public function deleteNode($key)
    {
        $current = $this->firstNode;
        $previous = $this->firstNode;
        
        while($current->data != $key)
        {
            if($current->next == NULL)
                return NULL;
            else
            {
                $previous = $current;
                $current = $current->next;
            }
        }
        
        if($current == $this->firstNode)
            $this->firstNode = $this->firstNode->next;
        else
            $previous->next = $current->next;
            
        self::$count--;   
    }
    
    public function find($key)
    {
        $current = $this->firstNode;
        while($current->data != $key)
        {
            if($current->next == NULL)
                return null;
            else
                $current = $current->next;
        }
        return $current;
    }
    
    public function readNode($nodePos)
    {
        if($nodePos <= self::$count)
        {
            $current = $this->firstNode;
            $pos = 1;
            while($pos != $nodePos)
            {
                if($current->next == NULL)
                    return null;
                else
                    $current = $current->next;
                    
                $pos++;
            }
            return $current->data;
        }
        else
            return NULL;
    }
    
    public function totalNodes()
    {
        return self::$count;
    }
    
    public function readList()
    {
        $listData = array();
        $current = $this->firstNode;
        
        while($current != NULL)
        {
            array_push($listData, $current->readNode());
            $current = $current->next;
        }
        return $listData;
    }
    
    public function reverseList()
    {
        if($this->firstNode != NULL)
        {
            if($this->firstNode->next != NULL)
            {
                $current = $this->firstNode;
                $new = NULL;
                
                while ($current != NULL)
                {
                    $temp = $current->next;
                    $current->next = $new;
                    $new = $current;
                    $current = $temp;
                }
                $this->firstNode = $new;
            }
        }
    }
}

?>


Test Case

<?php

require_once 'linklist.class.php';
require_once 'PHPUnit/Framework.php';

class LinkListTest extends PHPUnit_Framework_TestCase
{
    public function testLinkList()
    {
        
        $totalNodes = 100;
        
        $theList = new LinkList();
    
        for($i=1; $i <= $totalNodes; $i++)
        {
            $theList->insertLast($i);
        }
        
        $this->assertEquals($totalNodes, $theList->totalNodes());
        
        for($i=1; $i <= $totalNodes; $i++)
        {
            $theList->insertFirst($i);
        }
	
        $totalNodes = $totalNodes * 2;
        $this->assertEquals($totalNodes, $theList->totalNodes());
        
        $theList->reverseList();
        $this->assertEquals($totalNodes, $theList->totalNodes());
        
        $theList->deleteFirstNode();
        $this->assertEquals($totalNodes - 1, $theList->totalNodes());
        
        $theList->deleteLastNode();
        $this->assertEquals($totalNodes - 2, $theList->totalNodes());
        
        /* Delete node which has a value of '5' */
        $theList->deleteNode(5);
        $this->assertEquals($totalNodes - 3, $theList->totalNodes());
        
        /* Insert a node at the end of the list with a value of '22' */
        $theList->insertLast(22);
        $this->assertEquals($totalNodes - 2, $theList->totalNodes());
        
        /* Find a node with a value of '25' (is in the list) */
        $found = $theList->find(25);
        $this->assertEquals(25, $found->data);

        /* Find a node with a value of '125' (is not in the list) */
        $found = $theList->find(125);
        $this->assertNull($found);
        
        /* Return the data stored in the node at position '50' */
        $data = $theList->readNode(50);
        $this->assertEquals(50, $data);
        
        /* Return the data stored in the node at position '450' */
        $data = $theList->readNode(450);
        $this->assertNull($data);
    }
}

?>
