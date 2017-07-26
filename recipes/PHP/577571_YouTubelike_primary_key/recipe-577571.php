-------------------- dbHelper.php --------------------

class dbHelper
{
	public static function createUID($len = 16)
	{
		$index = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-_";
		$tc = strlen($index) - 1;
		
		$pk = '';
		
		for ($i = 0; $i < $len; $i++)
		{
			$pk .= $index[rand(0, $tc)];
		}
		
		return $pk;
	}
	
	public static function arCreateUID($obj, $len = 16)
	{
		$pk = $obj->get_primary_key(true);
		while (empty($obj->$pk) || $obj->$pk === 'NULL')
		{
			$obj->$pk = self::createUID($len);
			
			try
			{
				$r = $obj->find('first', array(
					'conditions' => array($pk . '=?', $obj->$pk)
				));
				
				if (is_null($r))
				{
					break;
				}
			} catch (\ActiveRecord\RecordNotFound $e) {
				break;
			}
		}
	}
}


-------------------- MyTable.php --------------------

class MyTable extends \ActiveRecord\Model
{
	static $before_create = array('create_uid');
	
	public function create_uid()
	{
		dbHelper::arCreateUID($this);
	}
}
