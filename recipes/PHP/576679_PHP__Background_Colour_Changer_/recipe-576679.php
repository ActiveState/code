<?php

// A list of the days of the week. 
$name_day = array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");

foreach ($name_day as $name);

{
  if ($name == "Sunday") 
      { // if day is Sunday background color is - Green.
        $background_color = "Green";
      }
  elseif ($name == "Monday") 
      {
       $background_color = "#ff9966";
      }
  elseif ($name == "Tuesday")  
      {
       $background_color = "#cccc33";
      }
  elseif ($name == "Wednesday")  
      {
       $background_color = "#999900";
      }
  elseif ($name == "Thursday") 
      {
       $background_color = "#66cc33";
      }
  elseif ($name == "Friday") 
      {
       $background_color = "#cc0000";
      }
  elseif ($name == "Saturday")  
      { // if day is not Sunday, but day is Saturday background color is - Purple.
       $background_color = "ff66ff";
      }
}   

$name_of = date("d-l-y"); // date, day, year.

echo "$name_of";
?>
