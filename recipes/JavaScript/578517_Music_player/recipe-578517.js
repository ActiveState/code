<html>
<lock>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Music search</title>

<style>
body,input,button{font-family:"Tahoma";}
body{background-color:#DDEEFF}

input.srch{border:solid MidnightBlue 1px;}
div.fdbk{border:solid MidnightBlue 1px;background-color:silver;}
b.artist{color:#0000BB}
.prgbar{
	background-color:MidnightBlue;
}
button,input.btn,.volctrl,.lnkhovr
{
 color:black;
 background-color:#AABBFF;
 border:solid #6688AA 1px;
}
button.fdbk
{
	color:yellow;
}
button.play
{
 border:solid #BBCCFF 1px;
}

a{text-decoration:none}
input.srch,.prgbar{width:200pt;}
div.fdbk{width:200pt;}
td.songtitle{height:40pt;vertical-align:top;}
.lnkhovr{border:0px;}
button.fdbk
{
  font-family:wingdings;
	border:none;
	background-color:transparent;
}
button.play
{
 font-family:wingdings;
}
.ctrl,.btn
{
  width:48pt;
  margin-right:1pt;
}
</style>

<script language="javascript" src="apptitle.js"></script>

<script>
/*************************
*                        *
*		 STRING FUNCTIONS    *
*                        *
**************************/

function remove_ext(s)
{
	// Remove the extension.
	s=""+s;
	var i_ext=s.lastIndexOf(".");
	if (i_ext>0)
	{
		s=s.substring(0,i_ext);
	}
	return s;
}

function last_char(s_str)
{
	var l=s_str.length;
	var r="";
	if (l>0) r=s_str.substring(l-1,l);
	return r;
}

function last_char_code(s_str)
{
	var l=s_str.length;
	var n=0;
	if (l>0) n=s_str.charCodeAt(l-1);
	return n;
}

function trim_a_char_from_right(s_str)
{
	var l=s_str.length-1;
	if (l>0) s_str=s_str.substring(0,l);
	return s_str;
}

function trim_chars_from_right(s_str, n)
{
    s_str=""+s_str;
	var l=s_str.length-n;
	if (l>0) s_str=s_str.substring(0,l);
	return s_str;
}


function trim_str(s)
{
	var i=0;
	var r='';
	var c='';
	var b_start=false;
	var end_index=0;
  s=''+s;
	for (i=s.length-1;i>0;i--)
	{
		c=s.charAt(i);
		if(c!=' ')
		{
			end_index=i;
			break;
		}
	}
	for (i=0;i<=end_index;i++)
	{
		c=s.charAt(i);
		if(c!=' ')b_start=true;
		if(b_start==true)r=r+c;
	}
	return r;
}

function replaceAll(txt, s_replace, with_this)
{  
	return txt.replace(new RegExp(s_replace, 'g'),with_this);
}

function SetCookie(name,value)
{
	var xDate = new Date();
	xDate.setDate(xDate.getDate() + 365);
	document.cookie=name+"="+escape(value)+";expires="+xDate;
}

function GetCookie(name)
{
	var arg=name+"=";
	var alen=arg.length;
	var clen=document.cookie.length;
	var i=0;
	while(i<clen)
	{
		var j=i+alen;
		if(document.cookie.substring(i,j)==arg)
		{
			return getCookieVal(j);
		}
		i=document.cookie.indexOf(" ",i)+1;
		if(i==0) break;
	}
	return ""; // instead of null
}

function getCookieVal(offset)
{
	var endstr=document.cookie.indexOf(";",offset);
	if(endstr==-1)
	{
		endstr=document.cookie.length;
	}
	return unescape(document.cookie.substring(offset,endstr));
}

function smart_set_focus(s)
{
	var e;
	try
	{
		e=document.getElementById(s);
		e.focus();
	}
	catch(err)
	{
	}
  return;
}

function capital_str(s)
{
	var c=s.charAt(0);
	c=c.toUpperCase();
	s=c+s.substring(1);
	return s;
}

function capitalize_str(s)
{
	var sc=s.toLowerCase();
	var r="";
	var c="";
	var b_got_cap=false;
	var i=0;
	for (i=0;i<sc.length;i++)
	{
		c=sc.charAt(i);
		if (c>="a" && c<="z" && b_got_cap==false)
		{
			c=c.toUpperCase();
			b_got_cap=true;
		}
		r+=c;
	}
	return r;
}

function is_upper_alpha_num(c)
{
	r = ((c>="A" && c<="Z") || (c>="0" && c<="9")) ? true : false;
	return r;
}

function string_ends_in(s_host,s_para)
{
	var b_result=false;
	var sl=s_host.length;
	var pl=s_para.length;
	var ns=sl-pl;
	var s_end_host="";
	if (ns>=0)
	{
		s_end_host=s_host.substring(ns,pl+ns);
		if (s_end_host==s_para) b_result=true;
	}
	return b_result;
}

function last_char_str(s)
{
	var c="";
	var n=s.length;
	if (n>0) c=s.charAt(n-1);
	return c;
}

function int_to_min_sec(time)
{
	var s="";
	var minutes = Math.floor(time / 60);
	var seconds = time - minutes * 60;
	if (seconds<10) seconds="0"+seconds;
	s=minutes + ":" + seconds;
	return s;
}

function is_valid_word(s)
{
	var i=0;
	var b_valid=false;
	var c="";
	for(i=0;i<s.length;i++)
	{
		c=s.charAt(i);
		if (c>="A" && c<="Z") 
		{
			b_valid=true;
		}
		else
		{
			b_valid=false;
			break;
		}
	}
	return b_valid;
}

function has_only_one_capital_letter(s)
{
	var r=-1;
	var n_cap=0;
	var n_first_cap=-1;
	var i=0;
	var c="";
  // Have to trick it for the double underscore.
	if (s.indexOf("__")>0)
	{
		r=s.indexOf("__")+1;
	}
	else
	{
		for (i=1;i<s.length;i++)
		{
			c=s.charAt(i);
			if (c=='.') break;
			if (c>="A" && c<="Z")
			{
				if (n_cap==0) n_first_cap=i;
				n_cap++;
			}
		}
		if (n_cap==1 && n_first_cap>0) r=n_first_cap;
	}
	return r;
}

function check_all_filenames()
{
	var i=0;
	var h="";
	for (i=0; i<a_songs.length; i++)
	{
		if (has_only_one_capital_letter(a_songs[i])<0)
			h+=a_songs[i]+"<br>\n";
	}
	var wnd=window.open("","_blank");
	wnd.document.write(h);
	wnd.document.close();
}

</script>


<script>
var g_youtube="";
var g_sequential=false; // whether or not it just plays the playlist in order from top to bottom.
var g_wnd;
var a_songs=new Array();
var a_caps=new Array();
var a_words=new Array();
var a_recent=new Array();
var a_playlist = new Array();
var m_play_list_ptr=-1;
var b_making_word_list=false;
var n_word_list_ptr=0;
var g_artist_search="";

// Do all initialization.

var g_enable=true;
var g_user_play=true;
var g_user_choice=false;
var g_seconds_not_playing=0;
var g_second_delay=0;
var g_previous_song=-1;
var g_current_song=-1;
var g_feedback_song=-1;

// Scoring
var a_indexes=new Array();
var a_scores=new Array();
var g_srch_ptr=0;
var g_busy_searching=false;
var g_repeat_search=false;
var g_busy_sorting=false;
var g_cancel_search=false;
var g_search_string="";
var g_sort_cycle_count=0;
var m_prev_elem="";
var m_muted=false;
var m_volume_at_begin=0; // for crank it feature

</script>

<script language="javascript" src="playlist.js"></script>
<script language="javascript" src="words.js"></script>
<script>

function getContentFromIframe(iFrameName)  
{  
	var myIFrame = document.getElementById(iFrameName);  
	var content = myIFrame.contentWindow.document.body.innerHTML;  
} 


function remove_playlist_item(n)
{
	var i=0;
	for (i=n;i<a_playlist.length-1;i++)
		a_playlist[i]=a_playlist[i+1];
	a_playlist.pop();
	redraw_playlist();
}

function add_song_to_playlist(n)
{
	a_playlist.push(n);
	redraw_playlist();
	show_playlist("p");
}

function redraw_playlist()
{
	var s_html="<table><th colspan=3 class=lnkhovr>Playlist</th>";
	var i=0;
	var s_song="";
	for (i=0;i<a_playlist.length;i++)
	{
		s_song=a_songs[a_playlist[i]];
		s_song=trim_chars_from_right(s_song,4);
		s_song=convert_to_song_and_artist(s_song);
  	var s_remove="<button onClick=\"remove_playlist_item(" + i + ");\"> - </button>"
		var s_on_click_cmd="do_link_click("+a_playlist[i]+"," + i + ");";
		var s_line=s_remove + "</td><td> <span class='lnkhovr' id=\"spnplst" + i + "\" onclick=\"" + s_on_click_cmd + "\" style='background-color:transparent'>" + s_song +"</span>";
		s_html+="<tr valign=top><td><nobr>"+s_line+"</td></tr>";
		
	}
	s_html+="</table>";
	var e=document.getElementById("txtplay");
	e.innerHTML=s_html;
	save_playlist();
}

function load_playlist()
{
	var s=GetCookie("playlist");
	var a=s.split(";");
	var i=0;
	var n=0;
	for (i=0;i<a.length;i++)
	{
		n=a[i];
		if (n.length>0) a_playlist.push(n);
	}
	redraw_playlist();
}

function save_playlist()
{
	var i=0;
	var s="";
	for (i=0;i<a_playlist.length;i++)

	{
		s+=a_playlist[i]+";";
	}
	SetCookie("playlist",s);
}

function exit_playlist()
{
	m_play_list_ptr=-1;
	highlight_playlist_item(m_play_list_ptr);
}

/*****************************
*                            *
*		 REGENERATE PLAYLIST     *
*                            *
*****************************/

// Search variables

function regenerate_master_playlist()
{
	s=show_input();
	var a=s.split("\n");
	var b="";
	var i=0;
	var r="";
	var l="";
	for (i=0;i<a.length;i++)
	{
		b=a[i];
		b=b.replace(/\\/g,"\\\\");
		b=b.replace(/\'/g,"\\\'");
		b=b.replace(/\"/g,"\\\"");
		if (last_char(b)!="3")
		{
			b=trim_a_char_from_right(b);
		}
		b=trim_str(b);
		if (b!="")
		{
			if (i>0) r+="\n";
			l="a_songs.push(\""+b+"\");";
			r+=l;
		}
	}
	show_data(r);
}

function show_data(r)
{
	var wnd=window.open("playlist.txt","_blank");
	wnd.document.write(r);
	wnd.document.title="playlist.js";
	wnd.document.close();
}


function show_input()
{
	g_wnd=window.open("playlist.txt","_blank");
	var s=g_wnd.document.body.innerHTML;
	s=s.replace("<PRE>","");
	s=s.replace("</PRE>","");
	g_wnd.close();
	return s;
}


function save_feedback_values()
{	
	var e_txt=document.getElementById("txtword");
	SetCookie("feedback",e_txt.value);
	return;
}

function load_feedback_values()
{
	var e_txt=document.getElementById("txtword");
	e_txt.value=GetCookie("feedback");
}




// make an array of capitalized, normalized strings to make searching faster and easier.
function init_caps()
{
	var i=0;
	var s="";
	for (i=0;i<a_songs.length;i++)
	{
		s=convert_string(a_songs[i]);
		s=trim_str(s);
		a_caps.push(s);
	}
}

init_caps();


function censored_str(s)
{
	s=replaceAll(s,"goddamn","g******");
	s=replaceAll(s,"bitch","b****");
	s=replaceAll(s,"fuck","f***");
	s=replaceAll(s,"shit","s***");
	s=replaceAll(s,"damn","d***");

	s=replaceAll(s,"Goddamn","g******");
	s=replaceAll(s,"Bitch","b****");
	s=replaceAll(s,"Fuck","f***");
	s=replaceAll(s,"Shit","s***");
	s=replaceAll(s,"Damn","d***");

	return s;
}


// If the filename is all lowercase except for one letter, then that is the artist.
function convert_to_song_and_artist(s)
{
	var i=0;
	var n_first_cap=-1;
	var c="";
	var r="";
	var lc="";
	var sp=s.lastIndexOf("\\");
	if (sp<=0) sp=0;
	var sc=s;
	var s_artist="";

	sc=s.replace("__","**");  // Trick it in case a group name starts with a number

	for (i=sp;i<sc.length;i++)
	{
		c=sc.charAt(i);
		if (c!="\'") // skip apost in can't, etc, so it is treated as one word.
		{
			if (!((c>="A" && c<="Z") || (c>="0" && c<="9") || (c>="a" && c<="z") || (c=='*') ))
			{
				c=" ";
			}
			if (c!=" " || lc!=" ")
			r+=c;
		}
	}

	r=censored_str(r);

	r=r.replace("**","__");
	n_first_cap=has_only_one_capital_letter(r);
	r=r.replace("__"," ");

	if (n_first_cap>0)
	{
		// title / artist
		s_artist=capitalize_str(r.substring(n_first_cap,r.length));
		r="<b title='song' style='color:blue'>" + capitalize_str(r.substring(0,n_first_cap-1))+ "</b><br><b onclick=\"do_artist_search('" + s_artist + "');\" style='color:navy' " + " >" + s_artist + "</b>";
	}
	else
		r="<b style='color:navy'>" + capitalize_str(r)+ "</b><br><b style='color:red'>Unknown artist</b>";

	r=fix_contractions(r);
	r=replace_all_upper(r,"i","I");

	if (string_ends_in(r.toUpperCase(),"EXPLICIT"))
		r=trim_chars_from_right(r,8)+" (explicit)";

	if (string_ends_in(r.toUpperCase(),"MSTR"))
		r=trim_chars_from_right(r,4);

	return r;
}


// takes the filename off the last part of the directory.
function convert_string(s)
{
	var r="";
	var c="";
	var lc="";
	s=s.toUpperCase();
	var i=0;
	var sp=s.lastIndexOf("\\");
	if (sp<=0) sp=0;
	for (i=sp;i<s.length;i++)
	{
		c=s.charAt(i);
		if (c!="\'") // skip apost in can't, etc, so it is treated as one word.
		{
			if (!is_upper_alpha_num(c)) c=" ";
			if (c!=" " || lc!=" ") r+=c;
		}
	}
	return r;
}

function convert_input_string(s)
{
	var r="";
	var c="";
	var lc="";
	s=s.toUpperCase();
	var i=0;
	for (i=0;i<s.length;i++)
	{
		c=s.charAt(i);
		if (c!="\'") // skip apost in can't, etc, so it is treated as one word.
		{
			if (!is_upper_alpha_num(c)) c=" ";
			if (c!=" " || lc!=" ")
			r+=c;
		}
	}
	return r;
}

function display_song_str(s)
{
	s=s.toLowerCase();
	s=censored_str(s);
	s=capitalize_str(s);
	return s;
}

// Replaces all uppercase words in a string, but preserves their case.
function replace_all_upper(s,s_word,s_word_with_apost)
{
	r=" "+s+" ";
	s_word=" "+s_word+" ";

	s_word_with_apost=" "+s_word_with_apost+" ";
	var u_word=capitalize_str(s_word);
	var u_word_with_apost=capitalize_str(s_word_with_apost);
	r=replaceAll(r,s_word,s_word_with_apost);
	r=replaceAll(r,u_word,u_word_with_apost);
	r=trim_str(r);
	return r;
}

function fix_contractions(s)
{
	var r=" "+s+" ";
	r=replace_all_upper(r,"youve","you've");
	r=replace_all_upper(r,"youre","you're");
	r=replace_all_upper(r,"weve","we've");
	r=replace_all_upper(r,"cant","can't");
	r=replace_all_upper(r,"isnt","isn't");
	r=replace_all_upper(r,"dont","don't");
	r=replace_all_upper(r,"aint","ain't");
	r=replace_all_upper(r,"talkin","talkin'");
	r=replace_all_upper(r,"its","it's");
	r=replace_all_upper(r,"ive","I've");
	r=replace_all_upper(r,"im","I'm");
	r=trim_str(r);
	return r;
}


/**********************
*                     *
*		    SCORING       *
*                     *
***********************/

function init_new_search()
{
	g_repeat_search=false;
	g_busy_searching=false;
	g_busy_sorting=false;
	g_cancel_search=false;
	do_search();
}

function get_checked_status(id)
{
	var r=false;
	var e;
	try
	{
		e=document.getElementById(id);
		if (e.checked) r=true;
	}
	catch(err)
	{
		r=false;
	}
	return r;
}


function do_search()
{
  var ed=document.getElementById("songsrch");
	var s=ed.value;
	var s_clean_str="";
	var d_start_time = new Date();
	var n_start_time = Date.parse(d_start_time);

	if (g_busy_searching==false && g_busy_sorting==false)
	{
		g_search_string="";
		a_indexes=new Array();
		a_scores=new Array();

		if (s=="admin")
		{
			ed.value="";
			show_feedback_data();
			return;
		}

		s=s.toLowerCase();
		s_clean_str=censored_str(s);
		ed.value=s_clean_str;

		s=convert_input_string(s);
		s=trim_str(s);
		if (s=="") return;

		check_search_words(s);
		g_search_string=s;
		g_srch_ptr=0;
		
		// Show the progress bar.
		var epr=document.getElementById("spnprog");
		epr.style.display="block";
		var esrch=document.getElementById("btnsrch");
		esrch.value="Cancel";
		g_busy_searching=true;
		g_busy_sorting=false;
		g_sort_cycle_count=0;
	}

	var i=g_srch_ptr;
	var n_srch_loop_count=0;

	if (g_cancel_search==false)
	{
	 	var epr=document.getElementById("spnprog");
		if (g_busy_searching==true)
		{
			for (i=g_srch_ptr;i<a_songs.length;i++)
			{
				var n_score=0;
				if (g_artist_search=="")
				{
					n_score=search_score(a_caps[i],g_search_string);
				}
				else
				{
					var ip=0;
					ip=a_songs[i].indexOf(g_artist_search);
					if (ip>0) n_score=1;
				}

				if (n_score>0)
				{
					a_indexes.push(i);
					a_scores.push(n_score);
				}
				n_srch_loop_count++;
				if (n_srch_loop_count>=2000) break;
			}
			g_srch_ptr=i;
	
			// Jump out after a time if it is not done.	
			if (g_srch_ptr<a_songs.length)
			{
				// show progress bar.
				var f_prog=g_srch_ptr/a_songs.length*172;
		 	 	var epr=document.getElementById("spnprog");
		 	 	
				var einp=document.getElementById("songsrch");
				epr.style.backgroundColor=einp.style.borderColor;
		 	 	
				f_prog=parseInt(f_prog);
				epr.style.width=f_prog+"pt";
				Timer=setTimeout("do_search()", 55);
				return;
			}
		}
		g_busy_searching=false;

		var d_end_time = new Date();
		var n_end_time = Date.parse(d_end_time);
		var n_time_diff=n_end_time-n_start_time;
	
		// Now sort them.
	
		var n_sort_loop_count=0;
		g_busy_sorting=true;
		var b_need_sort=true;
		while (b_need_sort==true)
		{
			b_need_sort=false;
			for (i=0;i<a_indexes.length-1;i++)
			{
				if (a_scores[i+1]>a_scores[i])
				{
					b_need_sort=true;
					var tmp_score=a_scores[i+1];
					var tmp_index=a_indexes[i+1];
					a_scores[i+1]=a_scores[i];
					a_indexes[i+1]=a_indexes[i];
					a_scores[i]=tmp_score;
					a_indexes[i]=tmp_index;
				}
			}
			n_sort_loop_count++;
			if (n_sort_loop_count>=200) 
			{
				if (b_need_sort==true)
				{
					// Progress bar for sorting.
					g_sort_cycle_count++;
					var f_prog=((g_sort_cycle_count % 5)+1)/5*172;
			 	 	var epr=document.getElementById("spnprog");
					f_prog=parseInt(f_prog);
					epr.style.width=f_prog+"pt";
					Timer=setTimeout("do_search()", 55);
					return;
				}
			}
		}
		g_busy_sorting=false;
		g_cancel_search=false;
	} // g_cancel_search==false

	g_busy_searching=false;
	g_busy_sorting=false;
	g_cancel_search=false;

	// Hide the progress bar.
	var epr=document.getElementById("spnprog");
	epr.style.width=0;
	epr.style.backgroundColor="transparent";

	var esrch=document.getElementById("btnsrch");
	esrch.value="Search";

  var em=document.getElementById("txtsrch");
	var s_table=draw_search_table();
	em.innerHTML=s_table;
	show_playlist("s");

	// go ahead and play the first one, unless it is an artist search.
	if (a_indexes.length>0 && g_artist_search=="")
	{
		change_sound(a_indexes[0]);
	}

	g_artist_search="";
	a_indexes=null;
	a_scores=null;

}

function search_item_common_string(n)
{
	var s_song="";
	var s_line="";
	var s_btn="";
	s_song=a_songs[n];
	var s_show=remove_ext(s_song);
	var s_on_click_cmd="";
	var s_add="";
	s_on_click_cmd="do_link_click("+n+", -1);";
	s_show=convert_to_song_and_artist(s_show);
	s_show="<span onclick=\"" + s_on_click_cmd + "\" onmouseover=\"this.style.backgroundColor=this.style.borderColor;\"; onmouseout=\"this.style.backgroundColor='transparent'\"; class='lnkhovr' style='background-color:transparent'>" + s_show + "</span>";
	s_add="<button onClick=\"add_song_to_playlist(" + n + ");\"> + </button>"
	s_score_str=""; // hide it now.
	s_btn="<button onClick=\"" + s_on_click_cmd + "\">&#x25BA;</button>";
	s_link="<a class=play href=\"" + s_song + "\">&#x25BC;</a>";
	s_line= s_add + s_btn + s_link + "@" + s_show;
	return s_line;
}

function search_item_string(n)
{
	var s_tmp=search_item_common_string(n);
	s_tmp=s_tmp.replace("@", " ");
	s_line="<nobr>" + s_tmp + "</nobr>";
	return s_line;
}

function search_item_table_row(n)
{
	var s_tmp=search_item_common_string(n);
	s_tmp=s_tmp.replace("@", "</td><td style='border-top:solid black 1px' width=90%>");
	s_line="<tr valign=top><td><nobr>"+ s_tmp + "</td></tr>";
	return s_line;
}

// show the results of the search.

function draw_search_table()
{
	var n_max_result=200;
	var s_result="";
	var s_song="";
	var s_line="";
	var s_btn="";
	var i=0;
	n_max_result=a_indexes.length;
	if (n_max_result>200) n_max_result=200;

	s_result="<table><th colspan=3 class=lnkhovr>Search results</th>";
	for (i=0;i<n_max_result;i++)
	{
		s_line=search_item_table_row(a_indexes[i]);
		s_result+=s_line;
	}
	s_result+="</table>";
	return s_result;
}

function do_link_click(n, n_playlist)
{
	if (g_busy_searching==false && g_busy_sorting==false) 
	{
		exit_playlist();
		g_user_choice=true;
		g_user_play=true;
		m_play_list_ptr=n_playlist;
		if (m_play_list_ptr>=0) 
		{
			highlight_playlist_item(m_play_list_ptr);
		}
		change_sound(n);
	}
}

function highlight_playlist_item(n)
{
	var this_elem="spnplst" + n;
	var e=document.getElementById(this_elem);
	var ep;
	if (m_prev_elem!="")
	{
		ep=document.getElementById(m_prev_elem);
		try
		{ep.style.backgroundColor="transparent";}
		catch(err) { }
	}
	m_prev_elem=this_elem;
	try
	{e.style.backgroundColor=e.style.borderColor;}
	catch(err) { }
}


function do_artist_search(s)
{
	g_artist_search=s;
	g_artist_search=replaceAll(g_artist_search," ","_");
  var ed=document.getElementById("songsrch");
	ed.value=s;
	if (g_busy_searching==false && g_busy_sorting==false) 
		init_new_search();
}

function do_search_button_click()
{
	// Either do the search or cancel it.
	g_repeat_search=false;
	if (g_busy_searching==false && g_busy_sorting==false) 
		init_new_search();
	else
		g_cancel_search=true;
}

function remove_duplicate_words(a)
{
	var i=0;;
	var j=0;
	for (i=0;i<a.length-1;i++)
	{
		for (j=i+1;j<a.length;j++)
		{
			if (a[i]==a[j]) a[j]="";
		}
	}
	var b=new Array();
	for (i=0;i<a.length;i++)
	{
		if (a[i]!="") b.push(a[i]);
	}
	return b;
}

// Should also do a comparison just to see how many raw letters match.
// Works, but it is really slow !
// Not used anymore - way too slow.
function compare_word_letters(s_host,s_para)
{
	var i=0;
	var r=0;
	var c="";
	
	for (i=0;i<s_para.length;i++)
	{
		c=s_para.charAt(i);
		if (is_upper_alpha_num(c))
			if (s_host.indexOf(c)>=0) r++;
	}
	return r;
}

function search_score(s_host, s_para)
{
	if (s_para=="") return 0;
	var n_score=0;
	var n_words_matched=0;
	if (s_host==s_para) n_score+=10000;
	if (s_host.indexOf(s_para)>=0) n_score+=2000; // exact match
	s_hw=s_host.split(" ");
	s_pw=s_para.split(" ");
	s_hw=remove_duplicate_words(s_hw);
	s_pw=remove_duplicate_words(s_pw);
	var i=0,j=0;
	for (i=0;i<s_hw.length;i++)
	{
		for (j=0;j<s_pw.length;j++)
		{
			if (s_hw[i]==s_pw[j]) 
			{
				n_words_matched++;
				n_score+=100;
			}
		}
	}

	// We also want it to score higher for words in the same order.
	var s_word_pair="";
	for (j=0;j<s_pw.length-1;j++)
	{
		s_word_pair=s_pw[j]+" "+s_pw[j+1];
		if (s_host.indexOf(s_word_pair)>=0) n_score+=2037;
	}

	if (n_words_matched==s_pw.length) n_score+=1000;

	return n_score;
}

function show_event(evt)
{
	if (evt.keyCode==13) init_new_search();
}

/**********************
*                     *
*		MEDIA CONTROLS    *
*                     *
***********************/

function change_sound(n)
{
	g_enable=false;
	var s="";
	var s_title="";
	var s_file="";
  var r=0;
	var b_explicit=false;

	r=Math.random()*a_songs.length;
  r=parseInt(r);
  var e=document.getElementById("chgsnd");

	if (n>=0)
	{
 		r=n;
	}
	
  if (g_sequential)
  {
    g_current_song++;
    if (g_current_song>=a_songs.length) g_current_song=0;
    r=g_current_song;
  }    
   
  s=a_songs[r];
  s_file=s;
	// Remove the extension.
	s=remove_ext(s);
	s_title=convert_to_song_and_artist(s);
	s=convert_string(s);
	if (string_ends_in(s,"EXPLICIT")) b_explicit=true;
	if (s.indexOf("BITCH")>=0) b_explicit=true;
	if (s.indexOf("RAPE")>=0) b_explicit=true;
	if (s.indexOf("FUCK")>=0) b_explicit=true;
	if (s.indexOf("JESUS")>=0) b_explicit=true;
	if (s.indexOf("DAMN")>=0) b_explicit=true;
	if (s.indexOf("DEVIL")>=0) b_explicit=true;
	if (s.indexOf("DEMON")>=0) b_explicit=true;
	if (s.indexOf("SATAN")>=0) b_explicit=true;
	if (s.indexOf("HELL")>=0) b_explicit=true;
	if (s.indexOf("GOD")>=0) b_explicit=true;

	if (b_explicit==true) 
	{
		if (g_user_choice==true)
		{
			var n=confirm("This song is explicit.\nPlay it anyway ?","Confirm","Confirm");
			if (n==false) return;
		}
		else
		{
			return;
		}
	}

	g_previous_song=g_current_song;
	g_current_song=r;
	g_user_choice=false;
	var em=document.getElementById("embplay");
	em.URL=s_file;
	em.AutoStart=false;
	smart_stop_player();
	m_volume_at_begin=volume_get();
	g_seconds_not_playing=0;
	g_second_delay=0;
  var en=document.getElementById("txtnow");
	
  s_title=search_item_table_row(r);
  en.innerHTML="<table>"+s_title+"</table>";
  update_recently_played(r);
  
  var ep=document.getElementById("txtprev");
	s="";
	if (g_previous_song>=0) 
	{
		ep.innerHTML="<table>"+search_item_table_row(g_previous_song)+"</table>";
  	var ef=document.getElementById("fdbprev");
		ef.style.display="inline";
	}
}



function update_recently_played(r)
{
  	var ef=document.getElementById("txtrecent");
  	var i=0;
  	var s="";
  	var g="";
  	var sh="<table><th colspan=3 class=lnkhovr>Recently played</th>";
		
	var recent_list_len=21;
  	
  	if (a_recent.length>=recent_list_len)
  	{
  		for (i=0;i<a_recent.length-1;i++)
  		{
  			a_recent[i]=a_recent[i+1];
  		}
  		a_recent.pop();
	}  		
  	a_recent.push(r);
	
	s=sh;
  	for (i=a_recent.length-2;i>=0;i--)
  	{
  		g=search_item_table_row(a_recent[i]);
			g=g.replace("<td", "<td align=right>"+(a_recent.length-i-1)+"<td");
  		s+=g+"\n";
  	}
  	s+="</table>";
  	ef.innerHTML=s;
}

function song_index_to_display_str(n)
{
	var s="";
	s=a_songs[n];
	s=remove_ext(s);
	s=convert_to_song_and_artist(s);
	return s;
}

function play_state_str(s)
{
	if (s=="3") s="Playing";
	if (s=="2") s="Paused";
	if (s=="1") s="Stopped";
	if (s=="0") s="Loading";
	if (s=="10") s="Loading";
	if (s=="9") s="Loading";
	return s;
}

function smart_play_state()
{
	var s="";
	try
	{
  	var em=document.getElementById("embplay");
		s=""+em.playstate;
	}
	catch(err)
	{
		s="Waiting";
	}
	return s;
}

function dec_timer()
{
	if (b_making_word_list==true) 
	{
		regenerate_word_list();
	}		
		
	if (g_busy_searching==false && g_busy_sorting==false)
	{
  var es=document.getElementById("txtstat");
  var s="";
  s=smart_play_state();
  es.innerHTML=play_state_str(s);
  
  if (s=="10")
  {
	  if (g_second_delay<10) 
	  {
		if (g_second_delay<=4) 
		{
	  	  move_current_position(0);
	  	}
	  	g_second_delay++;
		if (g_second_delay==4) 
		{
		  var em=document.getElementById("embplay");
		  em.controls.play();
		  set_mute(); // Make sure it doesn't come off mute when it switches songs.
		}
	  }
  }
  
  if (s!="3" && s!="2" && g_enable==true)
  {
		play_next_sound();
  }
  if (s=="3") 
	{
		g_enable=true;
		show_current_position();
	}
	else
	{
		// In case it hits an audio file that is really short.
		if (g_user_play==true)
		{
			g_seconds_not_playing++;
			if (g_seconds_not_playing>8)
				play_next_sound();
		}
	}
	} // if busy && busy	
  Timer=setTimeout("dec_timer()", 300);
}


function play_next_sound()
{
	if (m_play_list_ptr>=0)
	{
		// play the next song on the playlist.
		m_play_list_ptr++;
		if (m_play_list_ptr<a_playlist.length)
		{
			highlight_playlist_item(m_play_list_ptr);
			change_sound(a_playlist[m_play_list_ptr]);
		}
		else
		{
			exit_playlist();
		}
	}

	if (m_play_list_ptr<=-1)
  	change_sound(-1); // play a random sound.
}


function stop_sound()
{
	g_enable=false;
	g_user_play=false;
  var em=document.getElementById("embplay");
	try { em.controls.stop(); }
	catch(err) { }
}

function smart_stop_player()
{
  var em=document.getElementById("embplay");
	try { em.controls.stop(); }
	catch(err) { }
}

function play_sound()
{
	g_enable=false;
	g_user_play=true;
  var em=document.getElementById("embplay");
  em.controls.play();
	g_enable=true;
}


function pause_sound()
{
	g_enable=false;
	g_user_play=false;
  var em=document.getElementById("embplay");
  em.controls.pause();
}



function volume_soft()
{
	var em=document.getElementById("embplay");
	var n=parseInt(em.Volume);
	n-=2000;
	if (n>=0) n=0;
	em.Volume=n;
  var et=document.getElementById("songsrch");
	et.value=n;
}

function volume_get()
{
	var n=0;
	try {n=parseInt(em.Settings.volume);}	catch(err) { return 0; }
	return n;
}

function volume_set(i_dir)
{
	var em=document.getElementById("embplay");
	var n=0;
	try {n=parseInt(em.Settings.volume);}	catch(err) { return; }
	if (i_dir<0) 
	{
		n-=5;
	}
	if (i_dir>0) 
	{
		n+=5;
	}
	if (n<0) n=0;
	if (n>100) n=100;
	em.Settings.volume=n;
	var ev=document.getElementById("volvalue");
	var sv=volume_value(n);
	ev.innerHTML=""+n+"%";
}

function volume_up()
{
	var em=document.getElementById("embplay");
	var n=parseInt(em.Volume);
	n+=300;
	em.Volume=n;
}

function volume_value(n)
{
	n/=5;
	n=parseInt(n);
	return n;
}

function show_feedback(n)
{
	var e=document.getElementById("feedback");
	e.style.display="block";

  var ed=document.getElementById("txtsrch");
	ed.innerHTML="";

	var i=0;

	for (i=0;i<document.frmfdbk.btnfdbk.length;i++)
	{
		document.frmfdbk.btnfdbk[i].checked=false;
	}

	if (n==1)
	{
		g_feedback_song=g_current_song;
	}
	if (n==-1)
	{
		g_feedback_song=g_previous_song;
	}

  var ef=document.getElementById("fdbksong");
	ef.innerHTML=song_index_to_display_str(g_feedback_song);

}

function hide_feedback()
{
	var e=document.getElementById("feedback");
	e.style.display="none";
}

function cancel_feedback()
{
	hide_feedback();
}

function submit_feedback()
{
	var i=0;
	var s_code="";
	for (i=0;i<document.frmfdbk.btnfdbk.length;i++)
	{
		if (document.frmfdbk.btnfdbk[i].checked)
		{
			s_code=document.frmfdbk.btnfdbk[i].value;
		}
	}
	hide_feedback();
	if (s_code!="")
	{
		var s_text="";
		var e_txt=document.getElementById("txtword");
		s_text=e_txt.value;
		var s_file=a_songs[g_feedback_song];
		s_file=remove_ext(s_file);
		s_text+=s_file+s_code+";";
		e_txt.value=s_text;
		save_feedback_values();
	}
}

function feedback_code_str(c)
{
	var s="";
	switch(c)
	{
		case "x":s="Explicit";break;
		case "p":s="Poor Quality";break;
		case "i":s="Incomplete";break;
		case "l":s="Loud";break;
		case "s":s="Soft";break;
		case "e":s="Spike at end";break;
	}
	return s;
}


function parse_feedback_data()
{
	var e_txt=document.getElementById("txtword");
	var s=e_txt.value;
	var sline="";
	var scode="";
	var a=s.split(";")
	var i=0;
	var s_result="";
	for (i=0;i<a.length;i++)
	{
		sline=a[i];
		if (sline!="")
		{
			scode=last_char_str(sline);
			sline=trim_a_char_from_right(sline);
			s_result+=sline + " : " + feedback_code_str(scode) + "<br>\n";
		}
	}
	var wnd=window.open("","_blank");
	wnd.document.write(s_result);
	wnd.document.close();
}

function hide_feedback_data()
{
	var e=document.getElementById("adminfunc");
	e.style.display="none";
}

function show_feedback_data()
{
	var e=document.getElementById("adminfunc");
	e.style.display="block";
}


function do_all_init()
{
	dec_timer();
	load_feedback_values();
	load_playlist();
	volume_set(0);
	//regenerate_word_list();
	var e=document.getElementById("apptitle");
	e.innerHTML=g_app_title;
	return 0;
}

function do_decide_display(s)
{
	return;
	var e=document.getElementById("frmlyr");
	var ed=document.getElementById("divlyr");
	var s_disp="";
	if (s=="complete")
	{
		var x;
		var b_show=false;
		try {
		x=e.contentWindow.document;
		b_show=true;
		}
		catch(err) { }
		s_disp=b_show ? "block" : "none";
		if (b_show) show_playlist("l");
		e.style.display=s_disp;
	}
}


function toggle_mute()
{
	m_muted=!m_muted;
	set_mute();
}

function set_mute()
{
	var e=document.getElementById("btnmute");
	var ep=document.getElementById("embplay");
	ep.Settings.mute=m_muted;
	var s_txt=m_muted?"unmute":"mute";
	e.value=s_txt;
}

function display_block_checked_str(c)
{
	return c ? "inline" : "none";
}

function show_current_position()
{
	var ep=document.getElementById("embplay");
	var t=ep.Controls.currentPosition;
	t=parseInt(t);
	t=int_to_min_sec(t);
	var et=document.getElementById("timeelap");
	et.innerHTML=t;
}

function isNumber(n) 
{
  return !isNaN(parseFloat(n)) && isFinite(n);
}

function set_current_position()
{
	var ep=document.getElementById("embplay");
	var et=document.getElementById("txtsetpos");
	if (isNumber(et.value))
	{
		ep.Controls.currentPosition=et.value;
	}		
}

function move_current_position(t)
{
	var ep=document.getElementById("embplay");
	var n=ep.Controls.currentPosition;
	n+=t;
	if (n<0)n=0;
	ep.Controls.currentPosition=n;
}




function show_playlist(s)
{
	var cs=document.getElementById("chksrch");
	var cp=document.getElementById("chklist");
	var cl=document.getElementById("chklyrk");
	if (s=="s") cs.checked=true;
	if (s=="p") cp.checked=true;
	if (s=="l") cl.checked=true;

	var es=document.getElementById("txtsrch");
	var ep=document.getElementById("txtplay");

	var sc=document.getElementById("colsrch");
	var pc=document.getElementById("collist");

	var sw=100;
	var pw=100;

	if (!cs.checked) sw=0;
	if (!cp.checked) pw=0;
	if (cs.checked && cp.checked) {pw=50;sw=50;}

	sc.style.width=""+sw+"%";
	pc.style.width=""+pw+"%";

	es.style.display=display_block_checked_str(cs.checked);
	ep.style.display=display_block_checked_str(cp.checked);

}
</script>

  </head>
  <body onload="do_all_init();">

	<center>
	<span id="apptitle"></span>
	<table width=60% border=0><tr><td align=left>
		
		<table class=currplay border=0 width=100%>
		<tr><td></td><td colspan=2>

		<table border=0>
		<tr><td width=90%>
		<b id="txtstat"></b>&nbsp;<span id="timeelap"></span> 
		</td><td width=5%><nobr>
		<input type="text" size="4" id="txtsetpos" class="srch" style="width:32pt;">
		&nbsp;
		<button onclick="set_current_position();" >set</button> 
				<button onclick="move_current_position(-10);" ondblclick="move_current_position(-10);" >&lt;&lt;</button> 
		<button onclick="move_current_position(10);" ondblclick="move_current_position(10);" >&gt;&gt;</button> 
		</nobr>
		</td></tr></table>
		
		</td></tr>

		<tr><td class=songtitle>
		<nobr>
    <button onClick="show_feedback(1);" class="fdbk">x</button>
		</nobr>
		</td><td class=songtitle width=95%>
		<b id="txtnow"></b>
		<td valign=top>
		&nbsp;
		<input type="button" id="btncurr" onClick="do_youtube_current();" value="Youtube" class="btn">
		</td>
		</tr></table>

		<table class=currplay><tr><td class=songtitle>
		<nobr>
		<button id="fdbprev" onClick="show_feedback(-1);" style="display:none" class="fdbk">x</button>
		</nobr>
		</td><td class=songtitle width=95%>
		<span id="txtprev"></span>
		</td></tr></table>

		<hr>

    <p id="chgsnd" style="display:none;">
		
		<OBJECT id="embplay" width="320" height="240" 
			style="position:absolute; left:0;top:0;"
			CLASSID="CLSID:6BF52A52-394A-11d3-B153-00C04F79FAA6"
			type="application/x-oleobject">
			<PARAM NAME="URL" VALUE="">
			<PARAM NAME="SendPlayStateChangeEvents" VALUE="True">
			<PARAM NAME="AutoStart" VALUE="True">
			<PARAM name="uiMode" value="none">
			<PARAM name="PlayCount" value="1">
		</OBJECT>
	</p>		

    <button onClick="g_user_play=true;exit_playlist();change_sound(-1);">Random song</button>
		&nbsp;
    <button onClick="stop_sound();" class=ctrl>Stop</button>
    <button onClick="pause_sound();" class=ctrl>Pause</button>
    <button onClick="play_sound();" class=ctrl>Resume</button>
    <p id="txttimer"></p>
		<input id="songsrch" value="search" title="Enter your search here" onkeypress="show_event(event);" class="srch">
    <input type="button" id="btnsrch" onClick="do_search_button_click();" value="Search" class="btn">
		&nbsp;
    <input type="button" id="btnyou" onClick="do_youtube_search_bar();" value="Youtube" class="btn">
    
		<font color=red><small><span id="spnprog" style="width:0;display:block;background-color:transparent" class="prgbar">&nbsp;</span></small></font>
		Volume :&nbsp;
		<button onClick="volume_set(-1);" onDblClick="volume_set(-1);"> < </button><b id="volvalue" style="width:48pt;text-align:center;" class=volctrl></b>
		<button onClick="volume_set(1);" onDblClick="volume_set(1);"> > </button>
		<input type="button" id="btnmute" onClick="toggle_mute();" onDblClick="toggle_mute();" value="mute" class=btn>
		<br />
		<div id="feedback" class="fdbk" style="display:none;padding:8pt;">
		<b id="fdbksong"></b>
		<form name="frmfdbk">
		<input type="radio" value="x" name="btnfdbk">offensive content<br />
		<input type="radio" value="p" name="btnfdbk">poor audio quality<br />
		<input type="radio" value="i" name="btnfdbk">incomplete<br />
		<input type="radio" value="l" name="btnfdbk">too loud<br />
		<input type="radio" value="s" name="btnfdbk">not loud enough<br />
		<input type="radio" value="e" name="btnfdbk">spike at end<br />
		&nbsp;
		<button onClick="submit_feedback();" style="width:64pt;">Submit</button>
		&nbsp;
		<button onClick="cancel_feedback();" style="width:64pt;">Cancel</button>
		<br />
		</div>

		<br>
		<fieldset style="width:172pt">
		<input type="checkbox" value="s" id="chksrch" onClick="show_playlist('');">search results<br />
		<input type="checkbox" value="p" id="chklist" onClick="show_playlist('');">playlist<br />
		</fieldset>
		</form>
		
	<table width=100%><tr><td id="colsrch" valign=top>
	<span id="txtsrch" style="display:none;"></span>
	</td><td id="collist" valign=top>
	<span id="txtplay" style="display:none"></span>
	</td></tr></table>
	<div id="adminfunc" style="display:none">
    <textarea id="txtword" rows=10 cols=40></textarea>
		<br />
		<button onClick="parse_feedback_data();" style="width:64pt;">show</button>
		&nbsp;
		<button onClick="hide_feedback_data();" style="width:64pt;">hide</button>
		<br/>
		<button onClick="regenerate_master_playlist();" style="width:124pt;">regen playlist</button>
		<br/>
		<button onClick="regenerate_word_list();" style="width:124pt;">regen word list</button>		
		</div>
		
	<p id="txtrecent"></p>		
	</td></tr></table>
	
	</center>
<script>

function regenerate_word_list()
{
	var s="";
	var i=0,j=0;
	var k=0;
	if (b_making_word_list==true)
	{
		b_making_word_list=false;
		for (i=n_word_list_ptr;i<a_caps.length;i++)
		{
			s=a_caps[i];
			if (string_ends_in(s," MP3"))
				s=trim_chars_from_right(s,4);
			var w=s.split(" ");
			for (j=0;j<w.length;j++) 
			{
				if (is_valid_word(w[j])==true) smart_add_word(w[j]);
			}				
			k++;
			if (k>30)
			{
			 k=0;
			 b_making_word_list=true;
			 break;
			}
		}
		n_word_list_ptr=i;
		var e=document.getElementById("songsrch");
		e.value=""+n_word_list_ptr;
	}
	else
	{
		n_word_list_ptr=0;
		b_making_word_list=true;
		a_words=new Array();
	}
	
	if (b_making_word_list==true)
	{
		return;
	}
	
	var r="";
	for (i=0;i<a_words.length;i++)
	{
		r+="a_words.push(\""+a_words[i]+"\");\n";
	}
	alert(a_words.length);
	b_making_word_list=false;
	document.write(r);
}

function smart_add_word(s)
{
	var al=a_words.length;
	var i=0;
	var b_exists=false;
	for (i=0;i<al;i++)
	{
		if (a_words[i]==s) b_exists=true;
	}
	if (b_exists==false) a_words.push(s);
}

function word_exists(s)
{
	var r=false;
	for (i=0;i<a_words.length;i++)
	{
		if (a_words[i]==s)
		{
			r=true;
			break;
		}
	}
	return r;
}

function check_search_words(s)
{
	var e=document.getElementById("spnprog");
	e.style.display="none";
	var u=s.toUpperCase();
	var w=u.split(" ");
	var i=0;
	var r="";
	for (i=0;i<w.length;i++)
	{
		if (!word_exists(w[i]))
		{
			if (r!="") r+=",";
			r+=w[i].toLowerCase();
		}
	}
	if (r=="") r="&nbsp;";
	e.innerHTML=r;
}

function do_youtube_search_bar()
{
	var e=document.getElementById("songsrch");
	var s=e.value;
	do_youtube(s);
}	

function do_youtube(s)
{
	var s_url="";
	s=replaceAll(s,"/"," ");
	s=convert_input_string(s);
	s=replaceAll(s," ","+");
	s=s.replace("++","+");
	s=s.toLowerCase();
	s_url="http://www.youtube.com/results?search_query="+s;
	var newwindow=window.open(s_url,'name','resizable=1,scrollbars=1');
		if (window.focus) {newwindow.focus()}
}	

function do_youtube_current()
{
	var e=document.getElementById("txtnow");
	var s=""+e.innerText;
	do_youtube(s);
}

</script>
</body>
</html>
