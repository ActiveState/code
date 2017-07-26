###
## $name = input name for variables name in the html-form
## $class =class name for HTML/CSS
## $vl = default values or values that you get from mysql
## $year_range = range or year  will be displayed
##     $val-$year_range  to  $val+$year_range



$bulan = array (1=>'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember');
$maxbln= array(1=>31,         28,          31,     30,      31,     30,     31,     31,        30,          31,       30,           31);
$hari  = array ('Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu');
$harish  = array ('MG', 'SN', 'SL', 'RB', 'KM', 'JM', 'SA');

function list_date($name,$class,$vl,$year_range){
  //cek date format & fill now if blank

  global $bulan,$hari;

  $val=explode("-",$vl);
  $val[0]=$val[0]; //year
  $val[1]=$val[1]; //month
  $val[2]=$val[2]; //day

  //default values
  if(!checkdate($val[2],$val[1],$val[0])){
    $yy=date("Y");$dd="";$mm="";$yyyy="";
    $adds="<option value=\"\" selected></option>";
  } else{
    $dd=$val[2]; $mm=$val[1]; $yyyy=$val[0]; $yy=$yyyy;
    $adds="<option value=\"\"></option>";
  }

  //build day
  $selected="";echo "<select name=".$name."[2] class=$class >".$adds;
  for($i=1;$i<32;$i++){
    $selected=($i==$dd)?"selected":"";
    echo "<option value=\"$i\" $selected>$i</option>";
  } echo "</select>";


  //build month

  $selected="";echo "<select name=".$name."[1] class=$class >".$adds;
  for($i=0;$i<count($bulan);$i++){
    $selected=($i+1==$mm)?"selected":"";
    echo "<option value=\"".($i+1)."\" $selected>".$bulan[$i]."</option>";
  } echo "</select>";


  //build year
  $yf=$yy-$year_range;$yt=$yy+$year_range;
  $selected="";echo "<select name=".$name."[0] class=$class >".$adds;
  for($i=$yf;$i<$yt+1;$i++){
    $selected=($i==$yyyy)?"selected":"";
    echo "<option value=\"".$i."\" $selected>".$i."</option>";
  } echo "</select>";


}



### we can calling in our forms script like this
#  list_date("date_submit","mycss_inputselect",$date_submit,5);

## and for saving handle we can do like this
#  settype($date_submit,"array");
#  $date_char=$date_submit[0]."-".$date_submit[1]."-".$date_submit[2]

#  $sql="insert into some_table(some_date_column) values ('$date_char')";
#  mysql_query($sql);
