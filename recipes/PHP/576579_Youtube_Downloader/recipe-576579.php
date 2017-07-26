<?php
/*

	This is a basic functions used to show real URI of FLV files at youtube.com so we can
	download the file and play it offline. 
*/

function get_content_of_url($url){
	$ohyeah = curl_init();
	curl_setopt($ohyeah, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ohyeah, CURLOPT_URL, $url);
	$data = curl_exec($ohyeah);
	curl_close($ohyeah);
	return $data;
}


function get_flv_link($string) {  
	if (eregi("watch_fullscreen(.*)plid", $string, $out)) {  
		$outdata = $out[1];
	}  
	$arrs = (explode('&',$outdata));
	foreach($arrs as $arr){
		list($i,$x) = explode("=",$arr);
		$$i = $x;
	}
	$link = 'http://www.youtube.com/get_video?video_id='.$video_id.'&t='.$t;
	return array($video_id,$link);
} 

function get_youtube($url){
	$stream = get_content_of_url($url);
	return get_flv_link($stream);
}


/* ######## SAMPLE OF USAGE ##########
 * <?php
 * require_once('youtube.lib.php');
 * $link = get_youtube($youtube_url); 
 * echo $link[0];
 * ?>
 * 
 */
