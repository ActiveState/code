<?
/**
* This class checks the availability of a domain and gets the whois data
*
* @author    Sven Wagener <wagener_at_indot_dot_de>
* @copyright inDot media
* @include 	 Funktion:_include_
*/

class domain{
	var $domain="";
	
	/*******************************
	* Initializing server variables
	* array(top level domain,whois_Server,not_found_string or MAX number of CHARS: MAXCHARS:n)
	**/
	var $servers=array(
	array("ac","whois.nic.ac","No match"),
	array("ac.cn","whois.cnnic.net.cn","no matching record"),
	array("ac.jp","whois.nic.ad.jp","No match"),
	array("ac.uk","whois.ja.net","No such domain"),
	array("ad.jp","whois.nic.ad.jp","No match"),
	array("adm.br","whois.nic.br","No match"),
	array("adv.br","whois.nic.br","No match"),
	array("aero","whois.information.aero","is available"),
	array("ag","whois.nic.ag","Not found"),
	array("agr.br","whois.nic.br","No match"),
	array("ah.cn","whois.cnnic.net.cn","No entries found"),
	array("al","whois.ripe.net","No entries found"),
	array("am","whois.amnic.net","No match"),
	array("am.br","whois.nic.br","No match"),
	array("arq.br","whois.nic.br","No match"),
	array("at","whois.nic.at","nothing found"),
	array("au","whois.aunic.net","No Data Found"),
	array("art.br","whois.nic.br","No match"),
	array("as","whois.nic.as","Domain Not Found"),
	array("asn.au","whois.aunic.net","No Data Found"),
	array("ato.br","whois.nic.br","No match"),
        array("av.tr","whois.nic.tr","Not found in database"),
	array("az","whois.ripe.net","no entries found"),
	array("ba","whois.ripe.net","No match for"),
	array("be","whois.geektools.com","No such domain"),
	array("bg","whois.digsys.bg","does not exist"),
	array("bio.br","whois.nic.br","No match"),
	array("biz","whois.biz","Not found"),
        array("biz.tr","whois.nic.tr","Not found in database"),
	array("bj.cn","whois.cnnic.net.cn","No entries found"),
        array("bel.tr","whois.nic.tr","Not found in database"),
	array("bmd.br","whois.nic.br","No match"),
	array("br","whois.registro.br","No match"),
	array("by","whois.ripe.net","no entries found"),
	array("ca","whois.cira.ca","Status: AVAIL"),
	array("cc","whois.nic.cc","No match"),
	array("cd","whois.cd","No match"),
	array("ch","whois.nic.ch","We do not have an entry"),
	array("cim.br","whois.nic.br","No match"),
	array("ck","whois.ck-nic.org.ck","No entries found"),
	array("cl","whois.nic.cl","no existe"),
	array("cn","whois.cnnic.net.cn","No entries found"),
	array("cng.br","whois.nic.br","No match"),
	array("cnt.br","whois.nic.br","No match"),
	array("com","whois.crsnic.net","No match"),
	array("com.au","whois.aunic.net","No Data Found"),
	array("com.br","whois.nic.br","No match"),
	array("com.cn","whois.cnnic.net.cn","No entries found"),
	array("com.eg","whois.ripe.net","No entries found"),
	array("com.hk","whois.hknic.net.hk","No Match for"),
	array("com.mx","whois.nic.mx","Nombre del Dominio"),
        array("com.tr","whois.nic.tr","Not found in database"),
	array("com.ru","whois.ripn.ru","No entries found"),
	array("com.tw","whois.twnic.net","NO MATCH TIP"),
	array("conf.au","whois.aunic.net","No entries found"),
        array("co.at","whois.nic.at","nothing found"),
	array("co.jp","whois.nic.ad.jp","No match"),
	array("co.uk","whois.nic.uk","No match for"),
	array("cq.cn","whois.cnnic.net.cn","No entries found"),
	array("csiro.au","whois.aunic.net","No Data Found"),
	array("cx","whois.nic.cx","No match"),
	array("cy","whois.ripe.net","no entries found"),
	array("cz","whois.nic.cz","No data found"),
	array("de","whois.denic.de","not found"),
        array("dr.tr","whois.nic.tr","Not found in database"),
	array("dk","whois.dk-hostmaster.dk","No entries found"),
	array("dz","whois.ripe.net","no entries found"),
	array("ecn.br","whois.nic.br","No match"),
	array("ee","whois.eenet.ee","NOT FOUND"),
	//	array("edu","whois.verisign-grs.net","No match"),
	array("edu","whois.crsnic.net","No match"),
	array("edu.au","whois.aunic.net","No Data Found"),
	array("edu.br","whois.nic.br","No match"),
        array("edu.tr","whois.nic.tr","Not found in database"),
	array("eg","whois.ripe.net","No entries found"),
	array("es","whois.ripe.net","No entries found"),
	array("esp.br","whois.nic.br","No match"),
	array("etc.br","whois.nic.br","No match"),
	array("eti.br","whois.nic.br","No match"),
	array("eun.eg","whois.ripe.net","No entries found"),
	array("emu.id.au","whois.aunic.net","No Data Found"),
	array("eng.br","whois.nic.br","No match"),
	array("far.br","whois.nic.br","No match"),
	array("fi","whois.ripe.net","No entries found"),
	array("fj","whois.usp.ac.fj",""),
	array("fj.cn","whois.cnnic.net.cn","No entries found"),
	array("fm.br","whois.nic.br","No match"),
	array("fnd.br","whois.nic.br","No match"),
	array("fo","whois.ripe.net","no entries found"),
	array("fot.br","whois.nic.br","No match"),
	array("fst.br","whois.nic.br","No match"),
	array("fr","whois.nic.fr","No entries found"),
	array("gb","whois.ripe.net","No match for"),
	array("gb.com","whois.nomination.net","No match for"),
	array("gb.net","whois.nomination.net","No match for"),
	array("g12.br","whois.nic.br","No match"),
	array("gd.cn","whois.cnnic.net.cn","No entries found"),
	array("ge","whois.ripe.net","no entries found"),
        array("gen.tr","whois.nic.tr","Not found in database"),
	array("ggf.br","whois.nic.br","No match"),
	array("gl","whois.ripe.net","no entries found"),
	array("gr","whois.ripe.net","no entries found"),
	array("gr.jp","whois.nic.ad.jp","No match"),
	array("gs","whois.adamsnames.tc","is not registered"),
	array("gs.cn","whois.cnnic.net.cn","No entries found"),
	array("gov.au","whois.aunic.net","No Data Found"),
	array("gov.br","whois.nic.br","No match"),
	array("gov.cn","whois.cnnic.net.cn","No entries found"),
	array("gov.hk","whois.hknic.net.hk","No Match for"),
        array("gov.tr","whois.nic.tr","Not found in database"),
	array("gob.mx","whois.nic.mx","Nombre del Dominio"),
	array("gs","whois.adamsnames.tc","is not registered"),
	array("gz.cn","whois.cnnic.net.cn","No entries found"),
	array("gx.cn","whois.cnnic.net.cn","No entries found"),
	array("he.cn","whois.cnnic.net.cn","No entries found"),
	array("ha.cn","whois.cnnic.net.cn","No entries found"),
	array("hb.cn","whois.cnnic.net.cn","No entries found"),
	array("hi.cn","whois.cnnic.net.cn","No entries found"),
	array("hl.cn","whois.cnnic.net.cn","No entries found"),
	array("hn.cn","whois.cnnic.net.cn","No entries found"),
	array("hm","whois.registry.hm","(null)"),
	array("hk","whois.hknic.net.hk","No Match for"),
	array("hk.cn","whois.cnnic.net.cn","No entries found"),
	array("hu","whois.ripe.net","MAXCHARS:500"),
	array("id.au","whois.aunic.net","No Data Found"),
	array("ie","whois.domainregistry.ie","no match"),
	array("ind.br","whois.nic.br","No match"),
	array("imb.br","whois.nic.br","No match"),
	array("inf.br","whois.nic.br","No match"),
	array("info","whois.afilias.info","Not found"),
	array("info.au","whois.aunic.net","No Data Found"),
        array("info.tr","whois.nic.tr","Not found in database"),
	array("it","whois.nic.it","No entries found"),
	array("idv.tw","whois.twnic.net","NO MATCH TIP"),
	array("int","whois.iana.org","not found"),
	array("is","whois.isnic.is","No entries found"),
	array("il","whois.isoc.org.il","No data was found"),
	array("jl.cn","whois.cnnic.net.cn","No entries found"),
	array("jor.br","whois.nic.br","No match"),
	array("jp","whois.nic.ad.jp","No match"),
	array("js.cn","whois.cnnic.net.cn","No entries found"),
	array("jx.cn","whois.cnnic.net.cn","No entries found"),
        array("k12.tr","whois.nic.tr","Not found in database"),
	array("ke","whois.rg.net","No match for"),
	array("kr","whois.krnic.net","is not registered"),
	array("la","whois.nic.la","NO MATCH"),
	array("lel.br","whois.nic.br","No match"),
	array("li","whois.nic.ch","We do not have an entry"),
	array("lk","whois.nic.lk","No domain registered"),
	array("ln.cn","whois.cnnic.net.cn","No entries found"),
	array("lt","ns.litnet.lt","No matches found"),
	array("lu","whois.dns.lu","No entries found"),
	array("lv","whois.ripe.net","no entries found"),
	array("ltd.uk","whois.nic.uk","No match for"),
	array("ma","whois.ripe.net","No entries found"),
	array("mat.br","whois.nic.br","No match"),
	array("mc","whois.ripe.net","No entries found"),
	array("md","whois.ripe.net","No match for"),
	array("me.uk","whois.nic.uk","No match for"),
	array("med.br","whois.nic.br","No match"),
	array("mil","whois.nic.mil","No match"),
	array("mil.br","whois.nic.br","No match"),
        array("mil.tr","whois.nic.tr","Not found in database"),
	array("mk","whois.ripe.net","No match for"),
	array("mn","whois.nic.mn","Domain not found"),
	array("mo.cn","whois.cnnic.net.cn","No entries found"),
	array("ms","whois.adamsnames.tc","is not registered"),
	array("mt","whois.ripe.net","No Entries found"),
	array("mus.br","whois.nic.br","No match"),
	array("mx","whois.nic.mx","Nombre del Dominio"),
	array("name","whois.nic.name","No match"),
        array("name.tr","whois.nic.tr","Not found in database"),
	array("ne.jp","whois.nic.ad.jp","No match"),
	array("net","whois.crsnic.net","No match"),
	array("net.au","whois.aunic.net","No Data Found"),
	array("net.br","whois.nic.br","No match"),
	array("net.cn","whois.cnnic.net.cn","No entries found"),
	array("net.eg","whois.ripe.net","No entries found"),
	array("net.hk","whois.hknic.net.hk","No Match for"),
	array("net.lu","whois.dns.lu","No entries found"),
	array("net.mx","whois.nic.mx","Nombre del Dominio"),
	array("net.uk","whois.nic.uk","No match for "),
	array("net.ru","whois.ripn.ru","No entries found"),
        array("net.tr","whois.nic.tr","Not found in database"),
	array("net.tw","whois.twnic.net","NO MATCH TIP"),
	array("nl","whois.domain-registry.nl","is not a registered domain"),
	array("nm.cn","whois.cnnic.net.cn","No entries found"),
	array("no","whois.norid.no","no matches"),
	array("no.com","whois.nomination.net","No match for"),
	array("nom.br","whois.nic.br","No match"),
	array("not.br","whois.nic.br","No match"),
	array("ntr.br","whois.nic.br","No match"),
	array("nu","whois.nic.nu","NO MATCH for"),
	array("nx.cn","whois.cnnic.net.cn","No entries found"),
	array("nz","whois.domainz.net.nz","Not Listed"),
	array("plc.uk","whois.nic.uk","No match for"),
	array("odo.br","whois.nic.br","No match"),
	array("oop.br","whois.nic.br","No match"),
	array("or.jp","whois.nic.ad.jp","No match"),
        array("or.at","whois.nic.at","nothing found"),
	array("org","whois.pir.org","NOT FOUND"),
	array("org.au","whois.aunic.net","No Data Found"),
	array("org.br","whois.nic.br","No match"),
	array("org.cn","whois.cnnic.net.cn","No entries found"),
	array("org.hk","whois.hknic.net.hk","No Match for"),
	array("org.lu","whois.dns.lu","No entries found"),
	array("org.ru","whois.ripn.ru","No entries found"),
        array("org.tr","whois.nic.tr","Not found in database"),
	array("org.tw","whois.twnic.net","NO MATCH TIP"),
	array("org.uk","whois.nic.uk","No match for"),
	array("pk","whois.pknic.net","is not registered"),
	array("pl","whois.ripe.net","No information about"),
        array("pol.tr","whois.nic.tr","Not found in database"),
	array("pp.ru","whois.ripn.ru","No entries found"),
	array("ppg.br","whois.nic.br","No match"),
	array("pro.br","whois.nic.br","No match"),
	array("psi.br","whois.nic.br","No match"),
	array("psc.br","whois.nic.br","No match"),
	array("pt","whois.ripe.net","No match for"),
	array("qh.cn","whois.cnnic.net.cn","No entries found"),
	array("qsl.br","whois.nic.br","No match"),
	array("rec.br","whois.nic.br","No match"),
	array("ro","whois.ripe.net","No entries found"),
	array("ru","whois.ripn.ru","No entries found"),
	array("sc.cn","whois.cnnic.net.cn","No entries found"),
	array("sd.cn","whois.cnnic.net.cn","No entries found"),
	array("se","whois.nic-se.se","No data found"),
	array("se.com","whois.nomination.net","No match for"),
	array("se.net","whois.nomination.net","No match for"),
	array("sg","whois.nic.net.sg","NO entry found"),
	array("sh","whois.nic.sh","No match for"),
	array("sh.cn","whois.cnnic.net.cn","No entries found"),
	array("si","whois.arnes.si","No entries found"),
	array("sk","whois.ripe.net","no entries found"),
	array("slg.br","whois.nic.br","No match"),
	array("sm","whois.ripe.net","no entries found"),
	array("sn.cn","whois.cnnic.net.cn","No entries found"),
	array("srv.br","whois.nic.br","No match"),
	array("st","whois.nic.st","No entries found"),
	array("su","whois.ripe.net","No entries found"),
	array("sx.cn","whois.cnnic.net.cn","No entries found"),
	array("tc","whois.adamsnames.tc","is not registered"),
        array("tel.tr","whois.nic.tr","Not found in database"),
	array("th","whois.nic.uk","No entries found"),
	array("tj.cn","whois.cnnic.net.cn","No entries found"),
	array("tm","whois.nic.tm","No match for"),
	array("tn","whois.ripe.net","No entries found"),
	array("tmp.br","whois.nic.br","No match"),
	array("to","whois.tonic.to","No match"),
	// array("tr","whois.ripe.net","Not found in database"),
	array("trd.br","whois.nic.br","No match"),
	array("tur.br","whois.nic.br","No match"),
	array("tv","whois.nic.tv","MAXCHARS:75"),
	array("tv.br","whois.nic.br","No match"),
	array("tw","whois.twnic.net","NO MATCH TIP"),
	array("tw.cn","whois.cnnic.net.cn","No entries found"),
	array("ua","whois.ripe.net","No entries found"),
	array("uk","whois.thnic.net","No match for"),
	array("uk.com","whois.nomination.net","No match for"),
	array("uk.net","whois.nomination.net","No match for"),
	array("us","whois.nic.us","Not found"),
	array("va","whois.ripe.net","No entries found"),
	array("vet.br","whois.nic.br","No match"),
	array("vg","whois.adamsnames.tc","is not registered"),
	array("wattle.id.au","whois.aunic.net","No Data Found"),
        array("web.tr","whois.nic.tr","Not found in database"),
	array("ws","whois.worldsite.ws","No match for"),
	array("xj.cn","whois.cnnic.net.cn","No entries found"),
	array("xz.cn","whois.cnnic.net.cn","No entries found"),
	array("yn.cn","whois.cnnic.net.cn","No entries found"),
	array("yu","whois.ripe.net","No entries found"),
	array("za","whois.frd.ac.za","No match for"),
	array("zlg.br","whois.nic.br","No match"),
	array("zj.cn","whois.cnnic.net.cn","No entries found")
	);
	
	
	
	var $idn=array(224,225,226,227,228,229,230,231,232,233,234,235,240,236,237,238,239,241,242,243,244,245,246,248,254,249,250,251,252,253,255);
	//	var $idn=array("00E0","00E1","00E2","00E3","00E4","00E5","0101","0103","0105","00E6","00E7","0107","0109","010B","010D","010F","0111","00E8","00E9","00EA","00EB","0113","0115","0117","0119","011B","014B","00F0","011D","011F","0121","0123","0125","0127","00EC","00ED","00EE","00EF","0129","012B","012D","012F","0131","0135","0137","0138","013A","013C","013E","0142","00F1","0144","0146","0148","00F2","00F3","00F4","00F5","00F6","00F8","014D","014F","0151","0153","0155","0157","0159","015B","015D","015F","0161","0163","0165","0167","00FE","00F9","00FA","00FB","00FC","0169","016B","016D","016F","0171","0173","0175","00FD","00FF","0177","017A","017C","017E");
	
	/**
	* Constructor of class domain
	* @param string	$str_domainame    the full name of the domain
	* @desc Constructor of class domain
	*/
	function domain($str_domainname){
		$this->domain=$str_domainname;
	}
	
	/**
	* Returns the whois data of the domain
	* @return string $whoisdata Whois data as string
	* @desc Returns the whois data of the domain
	*/
	function info(){
		if($this->is_valid()){
			
			$tldname=$this->get_tld();
			$domainname=$this->get_domain();
			$whois_server=$this->get_whois_server();
			
			// If tldname have been found
			if($whois_server!=""){
				// Getting whois information
				$fp = fsockopen($whois_server,43);
				
				$dom=$domainname.".".$tldname;
//				fputs($fp, "$dom\r\n");
				
				// New IDN
				if($tldname=="de") {
					fputs($fp, "-C ISO-8859-1 -T dn $dom\r\n");
				} else {
					fputs($fp, "$dom\r\n");
				}
				
				// Getting string
				$string="";
				
				// Checking whois server for .com and .net
				if($tldname=="com" || $tldname=="net" || $tldname=="edu"){
					while(!feof($fp)){
						$line=trim(fgets($fp,128));
						
						$string.=$line;
						
						$lineArr=split(":",$line);
						
						if(strtolower($lineArr[0])=="whois server"){
							$whois_server=trim($lineArr[1]);
						}
					}
					// Getting whois information
					$fp = fsockopen($whois_server,43);
					
					$dom=$domainname.".".$tldname;
					fputs($fp, "$dom\r\n");
					
					// Getting string
					$string="";
					
					while(!feof($fp)){
						$string.=fgets($fp,128);
					}
					
					// Checking for other tld's
				}else{
					while(!feof($fp)){
						$string.=fgets($fp,128);
					}
				}
				fclose($fp);
				
				return $string;
			}else{
				return "No whois server for this tld in list!";
			}
		}else{
			return "Domainname isn't valid!";
		}
	}
	
	/**
	* Returns the whois data of the domain in HTML format
	* @return string $whoisdata Whois data as string in HTML
	* @desc Returns the whois data of the domain  in HTML format
	*/
	function html_info(){
		return nl2br($this->info());
	}
	
	/**
	* Returns name of the whois server of the tld
	* @return string $server the whois servers hostname
	* @desc Returns name of the whois server of the tld
	*/
	function get_whois_server(){
		$found=false;
		$tldname=$this->get_tld();
		for($i=0;$i<count($this->servers);$i++){
			if($this->servers[$i][0]==$tldname){
				$server=$this->servers[$i][1];
				$full_dom=$this->servers[$i][3];
				$found=true;
			}
		}
		return $server;
	}
	
	/**
	* Returns the tld of the domain without domain name
	* @return string $tldname the tlds name without domain name
	* @desc Returns the tld of the domain without domain name
	*/
	function get_tld(){
		// Splitting domainname
		$domain=split("\.",$this->domain);
		if(count($domain)>2){
			$domainname=$domain[0];
			for($i=1;$i<count($domain);$i++){
				if($i==1){
					$tldname=$domain[$i];
				}else{
					$tldname.=".".$domain[$i];
				}
			}
		}else{
			$domainname=$domain[0];
			$tldname=$domain[1];
		}
		return $tldname;
	}
	
	
	/**
	* Returns all tlds which are supported by the class
	* @return array $tlds all tlds as array
	* @desc Returns all tlds which are supported by the class
	*/
	function get_tlds(){
		$tlds="";
		for($i=0;$i<count($this->servers);$i++){
			$tlds[$i]=$this->servers[$i][0];
		}
		return $tlds;
	}
	
	/**
	* Returns the name of the domain without tld
	* @return string $domain the domains name without tld name
	* @desc Returns the name of the domain without tld
	*/
	function get_domain(){
		// Splitting domainname
		$domain=split("\.",$this->domain);
		return $domain[0];
	}

	/**
	* Returns the full domain
	* @return string $fulldomain
	* @desc Returns the full domain
	*/
	function get_fulldomain(){
		return $this->domain;
	}
	
	/**
	* Returns the string which will be returned by the whois server of the tld if a domain is avalable
	* @return string $notfound  the string which will be returned by the whois server of the tld if a domain is avalable
	* @desc Returns the string which will be returned by the whois server of the tld if a domain is avalable
	*/
	function get_notfound_string(){
		$found=false;
		$tldname=$this->get_tld();
		for($i=0;$i<count($this->servers);$i++){
			if($this->servers[$i][0]==$tldname){
				$notfound=$this->servers[$i][2];
			}
		}
		return $notfound;
	}
	
	/**
	* Returns if the domain is available for registering
	* @return boolean $is_available Returns 1 if domain is available and 0 if domain isn't available
	* @desc Returns if the domain is available for registering
	*/
	function is_available(){
		$whois_string=$this->info(); // Gets the entire WHOIS query from registrar
		$not_found_string=$this->get_notfound_string(); // Gets 3rd item from array
		$domain=$this->domain; // Gets current domain being queried
		
		$whois_string2=@ereg_replace("$domain","",$whois_string);
		
		$whois_string =@preg_replace("/\s+/"," ",$whois_string); //Replace whitespace with single space
		
		$array=split(":",$not_found_string);
		
		if($array[0]=="MAXCHARS"){
			if(strlen($whois_string2)<=$array[1]){
				return true;
			}else{
				return false;
			}
		}else{
			if(preg_match("/".$not_found_string."/i",$whois_string)){
				return true;
			}else{
				return false;
			}
		}
	}
	
	function get_cn_server($whois_text){
		
	}
	
	
	/**
	* Returns if the domain name is valid
	* @return boolean $is_valid Returns 1 if domain is valid and 0 if domain isn't valid
	* @desc Returns if the domain name is valid
	*/
	function is_valid(){
		
		$domainArr=split("\.",$this->domain);
		
		// If it's a tld with two Strings (like co.uk)
		if(count($domainArr)==3){
			
			$tld=$domainArr[1].".".$domainArr[2];
			$found=false;
			
			for($i=0;$i<count($this->servers) && $found==false;$i++){
				if($this->servers[$i][0]==$tld){
					$found=true;
				}
			}
			if(!$found){
				return false;
			}
			
		}else if(count($domainArr)>3){
			return false;
		}
		
		// Creating regular expression for
		if($this->get_tld()=="de"){
			for($i=0;$i<count($this->idn);$i++){
				$idn.=chr($this->idn[$i]);
				// $idn.="\x".$this->idn[$i]."";
			}
			$pattern="^[a-z".$idn."0-9\-]{3,}$";
		}else{
			$pattern="^[a-z0-9\-]{3,}$";
		}
		
		if(ereg($pattern,strtolower($this->get_domain())) && !ereg("^-|-$",strtolower($this->get_domain())) && !preg_match("/--/",strtolower($this->get_domain()))){
			return true;
		}else{
			return false;
		}
	}
}
?>
