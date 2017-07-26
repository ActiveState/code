$bulan = array (1=>'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember');
$maxbln= array(1=>31,         28,          31,     30,      31,     30,     31,     31,        30,          31,       30,           31);
$hari  = array ('Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu');
$harish  = array ('MG', 'SN', 'SL', 'RB', 'KM', 'JM', 'SA');


function showcalender(){
 global $calth,$calbln,$tgl;
 global $bulan,$hari,$harish,$maxbln;

 if(!isset($calth)) $calth=date("Y");
 if(!isset($calbln)) $calbln=date("n");



 echo "<form method=get><b>Kalender Agenda Kegiatan Alumni </b>";
 echo "<input type=hidden name=p value='agenda'>";
 echo "<input type=hidden name=tgl value='1'>";
 echo "<select name=calbln onchange=\"this.form.submit()\">";
 for($i=1;$i<count($bulan)+1;$i++){
   $selected=($i==$calbln)?"selected":"";
   echo "<option value=$i $selected>".$bulan[$i]."</option>";
 } echo "</select>";
 echo "<select name=calth  onchange=\"this.form.submit()\">";
  for($i=date("Y")-5;$i<date("Y")+5;$i++){
    $selected=($i==$calth)?"selected":"";
    echo "<option value=$i $selected>".$i."</option>";
  } echo "</select><br>";

 $maxbln[2]=($calth % 4==0) ? 29 :28;

 $maxday=$maxbln[$calbln];

 $set1dow=date("w",mktime (1,0,0,$calbln,1,$calth)); $st=0;
 echo "<table>"; $start=false; $val=""; echo "<tr>";
 for($i=0;$i<7;$i++){echo "<td class=mycal_header width=18>".$harish[$i]."</td>";} echo "</tr>";
 for($i=0;$i<42;$i++){
  if($i%7==0||$i==0){ echo "<tr>"; $ins=true; }
  if($i==$set1dow){ $start=true; $val=0; $st=$i-1; }
  if($i-$st>$maxday) {$start=false; $val=""; }

  if($start) $val++;
  if(is_numeric($val)){
    $class=($val==$tgl)?"mycal_value_light":"mycal_value";
    $tdlink="onclick=\"document.location='index.php?p=agenda&tgl=$val&calbln=$calbln&calth=$calth'\" onmouseover=\"this.oldclass=this.className;this.className='mycal_value_light2'\" onmouseout=\"this.className=this.oldclass\"";
    $link="<a href=\"index.php?p=agenda&tgl=$val&calbln=$calbln&calth=$calth\" class=mycal_link>$val</a>";}
  else{
    $link="&nbsp;";$tdlink="";
    $class="mycal_value_off";
  }
  echo "<td class=$class align=right $tdlink>$link</td>";
  if($i%7==0 && !$ins)echo "</tr>";$ins=false;
 } echo "</table>";echo "</form>";
}



### calling in your script by
# showcalender();
