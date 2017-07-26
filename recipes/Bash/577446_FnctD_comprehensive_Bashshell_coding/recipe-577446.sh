### Array-Meta,
### This Array Hold Main Section Header Name, to
### Access to a somewhat management Layer, thru
### Python Bash-Management-Generator. (PyBMG)
declare -a ArrayMetaMgmt=( Unset ReadOnly Empty DefaultConfList IntDefaultConfList SingleSet ) ;

### Sub-Function List
declare -a ArraySubFuncCall=( _sub_ssh_handler _sub_call_locality _sub_fnctCreateLocalityFuncParam fnct__in_for _sub_FParamDisplayValue _sub__in_while _sub_ImbriqIf  _sub_fnctCmdEval _sub_GetSpacer _sub_EvalKeyFuncStartOnCond _sub_parse_spacer_list _sub_call_default_display_Var _sub_UpdateMount_ShareVolume _sub_Zenity_OTS_Resume _sub_FuncParam fnct_filesystem _sub_setup_py_extra_cmd _sub_Monitor_Script _sub_AptOnCd_Handler _sub_aufs_fnct _sub_Git _sub_jack_script _sub_Generator  ) ;

################################################
### Main Section Array configuration :
### Array Statement Holder :
### Will Hold by both All Section in read-only section, Un-Initializer, Array Variable, Empty-Form,
### Default Configuration set's...

declare ABaseRoot="/etc/init.d/fnct.d/"

declare -a ArrayUnset=(           ZenityDefaultInterface  StrZenityTextTitle IntZenityTextWidth     IntZenityTextHeight ZenityOption       IntZenityListWidth     IntZenityListHeight     IntMinZenityScaleValue IntMaxZenityScaleValue IntZenityScaleStepValue StrQuestionZenityText             StrZenityQuestionYes      StrZenityQuestionNo   StrZenityTextHeader StrZenityColumnName     StrZenityColumnName     StrZenitySep            StrZenityScaleText    ArrayCharSpacerName   ArrayCharSpacerConv ) ;
declare -a ArrayReadOnly=(        Type__InitFuncState ) ;
declare -a ArrayEmpty=(           ZenityDefaultInterface  ArrayTimeToVoltage ZenityDefaultInterface StrZenityTextTitle  IntZenityTextWidth IntZenityTextHeight    ZenityOption            IntZenityListWidth     IntZenityListHeight    StrZenityTextHeader     StrZenityColumnName               StrZenityColumnName       StrZenitySep          StrZenityScaleText  IntMinZenityScaleValue  IntMaxZenityScaleValue  IntZenityScaleStepValue StrQuestionZenityText StrZenityQuestionYes  StrZenityQuestionNo   ArrayCharSpacerName ArrayCharSpacerConv ) ;
declare -a ArrayDefaultConfList=( TypedVarDeclaration     TypeDebugKey       ServicesType           ArrayAwkScriptPath  ArraySedScriptPath ArrayObjDumpOptionType ArrayObjDumpSymbolsType ArrayDateFormat        ArraFloatRegExp        ArrayFindPrintf         RightMemberVariableTypeRegExpDecl ArrayVariableTypeBase64   ArrayDPKG_QueryHeader ArrayPython26Lib    ArrayTestFS             ArraySedSysCtl          ArraySedVariableEval    ArraySysCtlKeyName    LZMAFormat            IndentFormat          HexdumpFormat       BatterryPath          ArrayCFLAGS ArrayInitType ArrayHWInfo ) ;

declare -a ArrayIntDefaultConfList=(      IntDateNormalFormat   IntTestPath   IntTestFile   IntTestExist   IntTestExec   IntSedNumFormatSedSysCtlKey   IntSedNumFormatSedSysCtlCSV   IntSedNumFormatSedSysCtlValue   IntSysCtlFileMax   IntZenityTextInterface   IntZenityListInterface   IntZenityScaleInterface   IntZenityQuestionInterface   IntInitUniqueID   IntInitShaSumID   IntInitCatId   IntInitDate   IntInitWhile   IntInitWordCountFileSize     IntInitEgrepCount   IntEAwkScriptPath   IntESedScriptPath   IntEparamTypeDebugDecl   IntEParamNoDebugDecl   IntEFunctionTypeDecl   IntEGlobalTypeDecl   IntEShellType   IntDefaultCharSpacer ) ;
declare -a ArrayIntDefaultConfListValue=( IntDateNormalFormat=0 IntTestPath=0 IntTestFile=1 IntTestExist=2 IntTestExec=3 IntSedNumFormatSedSysCtlKey=0 IntSedNumFormatSedSysCtlCSV=1 IntSedNumFormatSedSysCtlValue=2 IntSysCtlFileMax=0 IntZenityTextInterface=0 IntZenityListInterface=1 IntZenityScaleInterface=2 IntZenityQuestionInterface=3 IntInitUniqueID=0 IntInitShaSumID=1 IntInitCatId=2 IntInitDate=3 IntInitWhile=4 IntInitWordCountFileSize=5   IntInitEgrepCount=6 IntEAwkScriptPath=0 IntESedScriptPath=0 IntEparamTypeDebugDecl=0 IntEParamNoDebugDecl=1 IntEFunctionTypeDecl=0 IntEGlobalTypeDecl=1 IntEShellType=2 IntDefaultCharSpacer=1 ) ;

declare -a ArraySingleSet=(               CFLAGS                StrQuestionZenityText       StrZenityQuestionYes         StrZenityQuestionNo           StrZenityTextHeader           StrZenityColumnName             StrZenityColumnName                         StrZenitySep             StrZenityScaleText  ) ;

### End-Main Section.
################################################

### Un-Initializer.
unset ZenityDefaultInterface StrZenityTextTitle IntZenityTextWidth IntZenityTextHeight ZenityOption IntZenityListWidth IntZenityListHeight StrZenityTextHeader StrZenityColumnName StrZenityColumnName StrZenitySep StrZenityScaleText IntMinZenityScaleValue IntMaxZenityScaleValue IntZenityScaleStepValue StrQuestionZenityText StrZenityQuestionYes StrZenityQuestionNo ;

### Read Only Variable
function R_OnlyVar()
{
 local CmdEval=() ;
 CmdEval[0]="""declare -r Type__InitFuncState=disable""" ;
 function __eval()
 {
   local ArrayArg=( $* ) ;
   ${ArrayArg[0]} ;
 }
 for(( intx=0;intx<=$(( ${#CmdEval[@]}-1 ));intx++)); do 
  __eval "${CmdEval[${intx}]}" ;
 done
}
R_OnlyVar > /dev/null;


### Common Array Variable
declare -a TypedVarDeclaration=( "local" "declare" "declare -a" "declare -f" );
declare -a TypeDebugKey=( debug nodebug ) ;
declare -a ServicesType=( start stop help restart ask ) ;
declare -a ArrayAwkScriptPath=( "/etc/init.d/fnct.d/awk-script" ) ;
declare -a ArraySedScriptPath=( "/etc/init.d/fnct.d/sed-script" ) ;
declare -a ArrayObjDumpOptionType=( "--all-headers --section=import" "--all-headers --full-contents --include=/usr/local/src/ubuntu/caps-0.4.2 --all-headers" ) ;
declare -a ArrayObjDumpSymbolsType=( --syms --dynamic-syms ) ;
declare -a ArrayDateFormat=( "%F %H:%M:%S.%s.%N" "%Y%m%d_%s" "%Y%m%d" "%s.%N" ) ;
declare -a ArraFloatRegExp=( "[+-]\?[0-9]\+\(\.[0-9]\{2\}\)\?" ) ;
declare -a ArrayFindPrintf=( "\nFromSearchPath:${StrPathFind}\nPath:%h\nFullFileName:%p\nDepth:%d\nFilePermission:%m\nSize:%s\nGUID:%G\nUID:%U\n\n" "%p " ) ;
declare -a RightMemberVariableTypeRegExpDecl=( "=[a-zA-Z0-9_\-\$\\\/+\=\:\"\'\.\%]{1,}|[a-zA-Z0-9_]{1,}\[[\)\(\$\}\{]{0,}[0-9]{1,}[\)\(\$\}\{]{0,}\]" ) ;
declare -a ArrayVariableTypeBase64=( "64|base64|baseuuencode|uuencodetype|type64|typebase64|typeuuencode|uuencodetype" ) ;
declare -a ArrayDPKG_QueryHeader=( "Architecture" "Bugs" "Conffiles" "Config-Version" "Conflicts" "Breaks" "Depends" "Description" "Enhances" "Essential" "Filename" "Homepage" "Installed-Size" "MD5sum" "MSDOS-Filename" "Maintainer" "Origin" "Package" "Pre-Depends" "Priority" "Provides" "Recommends" "Replaces" "Revision" "Section" "Size" "Source" "Status" "Suggests" "Tag" "Triggers-Awaited" "Triggers-Pending" "Version" ) ;
declare -a ArrayPython26Lib=( /usr/lib/pyshared/python2.6 ) ;
declare -a ArrayPython26Path=( /usr/lib/python2.6/dist-packages /usr/local/lib/python2.6/dist-packages );
declare -a ArrayPythonVer=( 2.5 2.6 2.7 3.0 3.1 ) ;
declare -a ArrayTestFS=( "-d" "-f" "-e" "-x" ) ;
declare -a ArraySedSysCtl=( "s/\(^[[:alpha:]\.=-]*\)\([\t\ =]*\)\([[:digit:]|[:xdigit:]|[:alpha:]\_\.\-]*\)/\1/g" "s/\(^[[:alpha:]\.=-]*\)\([\t\ =]*\)\([[:digit:]|[:xdigit:]|[:alpha:]\_\.\-]*\)/\2/g" "s/\(^[[:alpha:]\.=-]*\)\([\t\ =]*\)\([[:digit:]|[:xdigit:]|[:alpha:]\_\.\-]*\)/\3/g" ) ;
declare -a ArraySedVariableEval=( "s/\([Ss]tr\|[Ii]nt\|[Tt]ype|[Cc]har|[Bb]ase\)\([a-zA-Z0-9_]*\)/\$\{\1\2\}/g" "s/\([Aa][Rr][Rr][Aa][Yy]\)\([a-zA-Z0-9_]*\)/\$\{\1\2\[__INT__]}/g" "s/\([Aa][Rr][Rr][Aa][Yy]\)\([a-zA-Z0-9_]*\)/\$\{#\1\2\[@]}/g" "s/\([Aa][Rr][Rr][Aa][Yy]\)\([a-zA-Z0-9_]*\)/\$\{\1\2\[@]:__IntStart__:__IntStop__}/g" "s/\([Aa][Rr][Rr][Aa][Yy]\)\([a-zA-Z0-9_]*\)/\$\{\1\2\[__INT__]:__IntStart__:__IntStop__}/g" "s/\([Aa][Rr][Rr][Aa][Yy]\)\([a-zA-Z0-9_]*\)/\$\{\1\2\[__INT__]\/__REGEXP__\/__REPLACE__}/g" );
declare -a ArraySysCtlKeyName=( "fs.file-max" "kernel.slow-work.max-threads" );
declare -a LZMAFormat=( "-9zc --force --format=lzma --lzma1=dict=64Mi --memory=675Mi" ) ;
declare -a IndentFormat=( "-bbb -bl -i1 -bli1 -cbi1 -cli1 -pi1 -cs -blf -bls -nut -pcs -ppi1 -prs -sai -saw -st" ) ;
declare -a HexdumpFormat=( "-x | tr '[:cntrl:]' ' ' | sed -r 's/[0-9a-fA-F]{7}//g;s/[\\t\ ]+//g'" ) ;
declare -a BatterryPath=( "/proc/acpi/battery" ) ;
declare -a ArrayCFLAGS=( ${CFLAGS[@]} ) ;
declare -a ArrayInitType=( "uuidgen -r" "sha1sum -b __FILE__" "cat __FILE__" "date +'__DATEFORMAT__'" "while [ 1 ] ; do __SERVICE__ ; done " "wc -c __FILE__" "egrep -ic __PATTERN__") ;
declare -a ArrayCharSpacerName=( Tab Space Tiret Dot LPThesis RPThesis LBrace RBrace LowerThan GreaterThan Star Slash BSlash Pipe DAnd DOr DCirc CtrlR Dollar Guill FrLGuill FrRGuill LBraceExec RBraceExec LBraceVar RBraceVar TriGuill ) ;
declare -a ArrayCharSpacerConv=( "\t" " " "-" "." "(" ")" "{" "}" "<" ">" "*" "/" "\\" "|" "\&\&" "\|\|" "\^\^" "\n" "\$" "\"" "«" "»" "$(" ")" "\${" "}" "\"\"\"" ) ;
declare -a ArrayFileRegExp=( "/usr/lib/libcuda.so.[0-9][0-9][0-9].[0-9][0-9].[0-9][0-9]" ) ;
declare -a ArrayIDLRegExp=( "GLIBC_(2.[0-9].[0-9]|2.[0-9] )" );
declare -a ArrayHWInfo=( all bios block bluetooth braille bridge camera cdrom chipcard cpu disk dsl dvb fingerprint floppy framebuffer gfxcard hub ide isapnp isdn joystick keyboard memory modem monitor mouse netcard network partition pci pcmcia pcmcia-ctrl pppoe printer scanner scsi smp sound storage-ctrl sys tape tv usb usb-ctrl vbe wlan zip ) ;

### Single Set Variable

### Sequential Variable Assignation
### This is boggus, but some information embedded can not
### be inserted all in one-shoot. Maybe some error in insertion.
ZenityDefaultInterface[${IntZenityTextInterface}]="--text-info --editable --title=\${StrZenityTextTitle:=\"This Title\"} --width=\${IntZenityTextWidth:=800} --height=\${IntZenityTextHeight:=600} ${ZenityOption[@]}" ;

ZenityDefaultInterface[${IntZenityListInterface}]="--list --width=\${IntZenityListWidth:=800} --height=\${IntZenityListHeight:=600} --text=\${StrZenityTextHeader:=\"Displayed result\"} --column=\${StrZenityColumnName[0]:=\"__SELECTED__\"} --column=\${StrZenityColumnName[1]:=\"__ITEM__\"} --checklist --editable --separator \${StrZenitySep:=\"\n\"} ${ZenityOption[@]}"  ;
ZenityDefaultInterface[${IntZenityScaleInterface}]="--scale --text=\${StrZenityScaleText:=\"Scaling value of command item __ITEM__\"} --min-value=\${MinZenityScaleValue:=0} --max-value=\${MaxZenityScaleValue:=100} --step=\${IntZenityScaleStepValue:=2} ${ZenityOption[@]} " ;
ZenityDefaultInterface[${IntZenityQuestionInterface}]="--question --text=\"\${StrQuestionZenityText:=do you want to keep same value for this item}\" --ok-label=\${StrZenityQuestionYes:=yes} --cancel-label=\${StrZenityQuestionNo:=no} \${ZenityOption[@]} " ;

### Management Array/Variable  :
if [ ${USER} != 'root' ] ; then
  declare -a ArrayVariableLoader=( __Env___UUIDRandomPolicyConfig  __Env_DPKG_config __Env_GoogleConfig  );
  eval "declare -a ArrayPath${USER}=( \$( find ./ -mount -maxdepth 1 -ignore_readdir_race -type d -not -uid 1000 -uid ${UID} -printf \"%p \" ) )" ;
else
  declare -a ArrayVariableLoader=( __Env___UUIDRandomPolicyConfig __Env_CpuFreqSysConfig __Env_DPKG_config __Env_GoogleConfig  );
  eval "declare -a ArrayPath${USER}=( \$( find ./ -mount -maxdepth 1 -ignore_readdir_race -type d -not -uid 0 -uid ${UID} -printf \"%p \" ) )" ;
fi

UpdateIncludeHeader()
{
 local ArrayArg=( $* ) ;
 local StrFuncName=( UpdateIncludeHeader ) ;
 function FindAction()
 {
  local ArrayArg=( $* ) ;
  find /usr/include/ -type f -iname "*.h" -printf "%p " ;
 }
 unset ArrayFileInclude ;
 echo -ne "Function ${StrFuncName}:\n\tUpdating Array Include header, will be update in Array ArrayFileInclude\n" > /dev/stderr ;
 declare -a ArrayFileInclude=( $( FindAction ) ) ;
 echo -ne "Function ${StrFuncName}:\n\tEnd of update\n" > /dev/stderr ;
}


__call_locality()
{
 local ArrayArgInfo=( $* ) ;
 local StrFuncName=( __call_locality ) ;
 local ArrayLocalityScheme=( CreateFuncName CreateFuncEval DisplayFunctionInformation FinalizeLocality ) ; 
 
 function ArrayArg.Property.NumberId()
 {
  local ArrayArg=( $* ) ;
  local StrFuncName=( ArrayArg Property NumberId ) ;
  local IntLength=${#ArrayArg[@]} ;
  if [ ${IntLength} -gt 0 ] ; then
   ArrayArg.Setter.NumberId ${ArrayArg[@]} ;
  else
   ArrayArg.Getter.NumberId 
  fi
 }
 
 function ArrayArg.Getter.NumberId()
 {
  local ArrayArg=( $* ) ;
  local StrFuncName=( ArrayArg Getter NumberId ) ;
  local IntLength=${#ArrayArg[@]} ;
  echo "${ArrayArg[NumberId]}" ;
 }

 function ArrayArg.Setter.NumberId()
 {
  local ArrayArg=( $* ) ;
  local StrFuncName=( ArrayArg Setter NumberId ) ;
  local IntLength=${#ArrayArg[@]} ;
  ArrayArg[NumberId]="${ArrayArg[@]}" ;
 }
 
 echo eval "local ArrayArg=( \$* ) ; " ;
 eval "local StrNewFuncName=\${${StrFuncName[0]}LocalName}" ;
 eval "local IsDisplayFunctionEntry=\${${StrFuncName[0]}DisplayFunctionEntry}" ;

 IsDisplayFunctionEntry=${IsDisplayFunctionEntry:=0} ;
 StrNewFuncName=${StrNewFuncName:=DefaultSubFunction} ; 
 eval "local DefaultFunc=\${${StrFuncName[0]}DefaultFunc:=DisplayLocal}" ;
 
 function InitVarLocality()
 {
    IsDisplayFunctionEntry=${IsDisplayFunctionEntry:=0} ;
    StrNewFuncName=${StrNewFuncName:=DefaultSubFunction} ; 
    eval "local DefaultFunc=\${${StrFuncName[0]}DefaultFunc:=DisplayLocal}" ;
 }
 
 #echo -ne "function DisplayLocalEval()\t{ eval \$( __call_localityLocalName=DisplayLocal __call_locality ) ; echo -ne \"\${ArrayArg[0]}\n\" ; }" ; 
 ###
 ### This one only need few modification, to work, it simple design the Default display instead of echo in __in_for
 ### ... Probably need some clear-eyes to find-it out... 
 ###
 ### And The goal :
 ###     To generate Pre-designed sub-function here. Creating Function for CmdEval and you coumpound element and
 ### choose the moment to display or execute them... You make any suggestion, The blog is here to 
 ### promote C.O.R.P. ( Conflicting-Object-Resolution-Pattern... ).
 ###
 
 function CreateFuncName()
 {
    local TypeNoVal="None" ;
    local StrLMember="${StrNewFuncName:=${TypeNoVal}}";
    local StrRMember="${TypeNoVal}";
    local StrNewMember="local StrFuncName=\( \${StrNewFuncName} \)"
    echo -ne  "if [ ${StrLMember} != ${StrRMember} ] ; then echo \"eval ${StrNewMember} ;\" ; fi ;"  ; 
 }
 
 function CreateFuncEval()
 {
   local TypeNoVal="None" ;
    local StrLMember="${DefaultFuncEval:=${TypeNoVal}}";
    local StrRMember="${TypeNoVal}";
    local StrNewMember="local StrFuncName=\( \${StrNewFuncName} \)"
   echo -ne  "if [ ${StrLMember} != ${StrRMember} ] ; then echo \"eval \"local DefaultFunc=\( \${${StrFuncName[0]}DefaultFuncEval:=DisplayLocalEval} \) ; \"\" ; fi ;" ;
 }
 
 function DisplayFunctionInformation
 {
   local StrDisplay="From Function:[ ${StrNewFuncName} ]" ;
   echo -ne "if [ \${IsDisplayFunctionEntry:=0} -ne 0 ] ; then echo \"${StrDisplay}\" > /dev/stderr ; fi ;" ;
 }
 function FinalizeLocality()
 {
    echo -ne  "eval \"local StrHelperVarName=ArrayHelper${StrNewFuncName}\"" ;
 }

 echo """
   for(( intY=0 ; intY <= (( \${#ArrayArg[@]}-1 )) ; intY++ )) ; do 
     eval \"\$( ${TypedVarDeclaration[${#TypedVarDeclaration[@]}]} ArrayArg.Property.NumberId | sed 's/\NumberId/${intY}/g')\"  ; 
     eval \"\$( ${TypedVarDeclaration[${#TypedVarDeclaration[@]}]} ArrayArg.Getter.NumberId | sed 's/\NumberId/${intY}/g')\" ;  
     eval \"\$( ${TypedVarDeclaration[${#TypedVarDeclaration[@]}]} ArrayArg.Setter.NumberId | sed 's/\NumberId/${intY}/g')\"  ; 
   done ;
   """ ; 
 for(( intx=0;intx<=$((${#ArrayLocalityScheme[@]}-1));intx++ )); do
  eval "eval \$( ${ArrayLocalityScheme[${intx}]} )";
 done
}


IsfnctCreateLocalityFuncParam=True ;

function __fnctCreateLocalityFuncParam()
{
  ### All Pre Declaration Variable are prefixed to : 
  ### FParam
  ### FParam${Suffix}=Value 
  ### FParam${Suffix}=Value __fnctCreateLocalityFuncParam
  ### ParamList :
  ### FParamFuncName
  ### FParamSuffixName
  ### FParamVarName
  ### FParamDefaultValue
  ### FParamInterpretVar
  ### FParamBase64
  ### 
  ### Note : To produce a valid command issued from this function it need evaluated-executive-parenthesis 
  ### 'eval $( FParamFuncName=${StrFuncName} FParamSuffixName=__SUFFIX__ FParamVarName=__VARNAME__ 
  ### FParamDefaultValue=__VALUE__ __fnctCreateLocalityFuncParam )'
  ###
  ### Typical uses : eval $( FParamFuncName= FParamSuffixName= FParamVarName= FParamDefaultValue= __fnctCreateLocalityFuncParam )
  
  eval $( __call_localityLocalName=FParam __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
  eval "local StrFuncNameOut=\${${StrFuncName}FuncName:=${StrFuncName}}" ; 
  eval "local SuffixName=\${${StrFuncName}SuffixName:=Debug}" ; 
  eval "local VarName=\${${StrFuncName}VarName:=IsItem}" ; 
  eval "local IsInterpretVar=\${${StrFuncName}InterpretVar:=False}" ; 
  eval "local DefaultValue=\${${StrFuncName}DefaultValue:=False}" ; 
  eval "local IsBase64=\${${StrFuncName}Base64:=False}" ; 
  if [ "${IsInterpretVar}" == "True" ] ; then 
		#echo -ne "IsInterpretVar set to transfert variable between ${DefaultValue} and \${${DefaultValue}} \n" > /dev/stderr ; 
		if [ ${IsBase64:=False} == "True" ] ; then 
      eval "DefaultValue=\"\\\${${DefaultValue}}\"" ;
      eval "DefaultValue=\"$( echo \"${DefaultValue}\" | base64 --wrap=0 -d )\"";
    else
      eval "DefaultValue=\"\\\${${DefaultValue}}\"" ;
      eval "DefaultValue=\"\\\${${DefaultValue}}\"" ;
    fi
  else
    if [ ${IsBase64:=False} == "True" ] ; then 
      eval "DefaultValue=\"$( echo \"${DefaultValue}\" | base64 --wrap=0 -d )\"";
    else
      eval "DefaultValue=\"${DefaultValue}\"";
    fi
	fi
  eval "local StrArrayHelperName=ArrayHelper${StrFuncNameOut}" ;
  eval "local HelperIncrementInArray=\${${StrFuncNameOut}HelperIncrementInArray:=True}" ;
  
  eval "local IntNextItemAHelper=\${#${StrArrayHelperName}[@]}" ;
  
  ### ArrayDetection Test. 
  ### It's unusual, but stacking information in Tree-Function disposition with same Prefix 
  ### Handler can be used for many purposes... And Instead of overwriting the variable, it
  ### simply add it to the end... The other advantage is using the same AddHelper and ListHelper
  ### in Tree function. unlike DOM and SGML, they similary work in same fashion...
  ### 
  ### Note: 
  ### There is an FParamHelperIncrementInArray which is set to True by default, having
  ### consequence to add has many as __fnctCreateLocalityFuncParam is called with same 
  ### FParamVarName, excepted we should work with adding in Helper in manner it's The
  ### FParamSuffixName ':' IntLength pair is added instead, giving idea when the Array
  ### reach it's state, before or after using __fnctCreateLocalityFuncParam... 
  ### 
  eval "local IntLength=\${#${VarName}[@]}" ;
  if [ ${IntLength:=0} -eq 0 ] ; then 
		echo -ne "eval \"local ${VarName}=\${${StrFuncNameOut}${SuffixName}:=$( echo ${DefaultValue} )}\"\n" ; 
		echo -ne "eval \${StrFuncNameHelperAdd} ${SuffixName};" ;
  else
		eval "local NextItem=\${#${VarName}[@]}" ;
		echo -ne "eval \"${VarName}[${NextItem}]=\${${StrFuncNameOut}${SuffixName}:=$( echo ${DefaultValue} )}\"\n" ; 
		if [ "${HelperIncrementInArray:=True}" == "False" ] ; then
			echo -ne "eval \${StrFuncNameHelperAdd} ${SuffixName}:${IntLength};" ;
		fi 
  fi
  echo -ne "eval \${StrFuncNameHelperList};\n" ;
}


### Function : __in_for ()
### Function to Loop Process f(x) from Array in loop
### Noted : eval $( __in_for <|ArrayContent|> f() x
### where :
###   <|ArrayContent|> : is an Array. The Holder-Name can be a Global or local Array
###   f() : is a function or program with __call_locality ability or parse_newvar or even __InitFunc
###   x : Is the variable, can be fixed result from query or variable assignation like, var=value
###
###   Content of f() must:
###     Having support for ${ArrayArg[0]} or ${<|ArrayContent|>[int<|ArrayContent|>]} is the internal
###     form and both of them are working, but ${<|ArrayContent|>[int<|ArrayContent|>]} will be Array-named
###     dependent.
###
###     ex :
###     function __test_internal_form()
###     {
###       eval $( __InitFunc __test_internal_form ) ;
###       if [ ${InternalForm:=full} == "full" ] ; then
###           echo "${ArrayTest[${intArrayTest}]}" ;
###       elif [ ${InternalForm:=full} == "ArrayArg" ] ; then
###           echo "${ArrayArg[0]}" ;
###       fi
###    }
###
###   while, ArrayTest=( 1 2 3 ) ;while, ArrayTest1=( 3 2 1 ) ;
###   calling : eval $( __in_for ArrayTest __test_internal_form )
###    ---> will pass, displaying 1\n 2\n 3\n ...
###   calling : eval $( __in_for ArrayTest1 __test_internal_form )
###    ---> Will Fail...
###     Because ArrayTest1 is involved in looping and looking for ${ArrayTest1[${inArrayTest1}]} and not
###     ${ArrayTest[${intArrayTest}]}, but
###   calling : eval $( __in_for ArrayTest1 __test_internal_form InternalForm=ArrayArg )
###   ---> will pass, displaying 3\n 2\n 1\n ...
###
###   But this function can not perform everything if :
###   eval $( __InitFunc __test_internal_form ) ;
###       Thank to evolution of ArrayBashCmd...
###   Note: Base64 is not supported.
###
###

ForBase64Encode()
{
 eval $( __call_localityLocalName=ForBase64Encode __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
 local Result=$( echo "${ArrayArg[@]}" | base64 --wrap=0 ) ;
 echo "BASE64:${Result[@]}" ;
}

ForBase64Decode()
{
 eval $( __call_localityLocalName=ForBase64Decode __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
 local Result=( ${ArrayArg[@]//:/ } ) ;
 if [ ${Result[0]:=none} == "BASE64"  ] ; then
   echo "${Result[1]}" | base64 --wrap=0 -d ;
 fi
}

__in_for ()
{
  eval $( __call_localityLocalName=For __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
  #eval $( parse_newvar ${EFunctionTypeDecl} ${TypeDebugKey[${EParamNoDebugDecl}]} ${ArrayArg[@]} ) ;
  ### parse_newvar is removed, time-saving arguments and FParam is more versatile...
  ###
  ###

  local IntUsingEgrepScanLoop=${IntUsingEgrepScanLoop:=0} ;
  local IntUsingArgModLimitation=${IntUsingArgModLimitation:=1} ;
  local IntTransmitArgModbase64=${IntTransmitArgModbase64:=0} ;
  local ParseTagArray="__ARRAY__" ;
  local ArrayArgMod;
  local ArrayName=${ArrayArg[0]};
  ArrayName=${ArrayName:=Array} ;
  local FunctionName=${ArrayArg[1]};
  local FunctionNameArg=${ArrayArg[2]};
  local CurrentIncType="int" ;
  local StrUUID=$( uuidgen -r ) ;
  StrUUID=${StrUUID//-/} ;
  local ArrayOptFParam=() ;
  ArrayOptFParam[0]="""eval \$( FParamFuncName=ForOpt FParamSuffixName=Debug     FParamVarName=IsDebug         FParamDefaultValue=True     __fnctCreateLocalityFuncParam ) ;""" ;
  ArrayOptFParam[1]="""eval \$( FParamFuncName=ForOpt FParamSuffixName=Try       FParamVarName=TryFunc         FParamDefaultValue=None     __fnctCreateLocalityFuncParam ) ;""" ;
  ArrayOptFParam[2]="""eval \$( FParamFuncName=ForOpt FParamSuffixName=Main      FParamVarName=MainFunc        FParamDefaultValue=${FunctionName:=echo}     __fnctCreateLocalityFuncParam ) ;""" ;
  ArrayOptFParam[3]="""eval \$( FParamFuncName=ForOpt FParamSuffixName=Except    FParamVarName=ExceptFunc      FParamDefaultValue=None     __fnctCreateLocalityFuncParam ) ;""" ;
  ArrayOptFParam[4]="""eval \$( FParamFuncName=ForOpt FParamSuffixName=Else      FParamVarName=ElseFunc        FParamDefaultValue=None     __fnctCreateLocalityFuncParam ) ;""" ;
  ArrayOptFParam[5]="""eval \$( FParamFuncName=ForOpt FParamSuffixName=Finalize  FParamVarName=FinalizeFunc    FParamDefaultValue=None     __fnctCreateLocalityFuncParam ) ;""" ;
  ArraySubFunc=( "function" "this_loop_${StrUUID}()    " "{" "; }" ) ;
  local ArrayTryCatchFunc=( "local TryErrorState=\$? ;" "if [ \"\${TryFunc:=None}\" != \"None\" ] ; then local TryFunc=\${TryErrorState} ; if [ \${ExceptFunc:=None} != \"None\" ] ; then eval \${ExceptFunc:=None} ; fi  ;  if [ \${FinalizeFunc:=None} != \"None\" ] ; then eval \${FinalizeFunc:=None} ; fi ; else if [ \${ElseFunc:=None} != \"None\" ] ; then eval \${ElseFunc:=None} ; fi ; fi" ) ;
  local ArrayInFor=( "${ArraySubFunc[@]:0:3} eval \$( __call_localityLocalName=${StrUUID} __call_locality ) ; ${ArrayOptFParam[@]}" "local ArrayName=${ArrayArg[0]}" ";" "for" "((" "${CurrentIncType}${ParseTagArray}=0" ";" "${CurrentIncType}${ParseTagArray}" "<=" "\${#${ParseTagArray}[@]}-1" ";" "${CurrentIncType}${ParseTagArray}++" "))" ";" "do" "local value=\"\${${ParseTagArray}[\$((int${ParseTagArray}))]}\" ; local type=\"Default\"; eval local IntPos=\${${CurrentIncType}${ParseTagArray}}" ";" "eval ${FunctionName:=${MainFunc:=echo}} ${FunctionNameArg} \${value}" "${ArrayArgMod[@]/#/;}" ";" ${ArrayTryCatchFunc[@]]} ";" "done" "${ArraySubFunc[3]}" ";" "${ArraySubFunc[1]/\(\)/}" ";" "unset ${ArraySubFunc[1]/\(\)/}" ) ;
  local StrRegExpParse=0;

  function Base64Handler()
  {
    if [ ${IntUsingArgModLimitation} -eq 1 ] ; then
      if [ ${IntTransmitArgModbase64} -eq 1 ] ; then
        ArrayArgMod=( $( echo ${ArrayArg[@]:4} | ForBase64Encode ) ) ;
      else
        ArrayArgMod=( ${ArrayArg[@]:4} ) ;
      fi
    else
      if [ ${IntTransmitArgModbase64} -eq 1 ] ; then
        ArrayArgMod=( $( echo ${ArrayArg[@]} | ForBase64Encode ) ) ;
      else
        ArrayArgMod=( ${ArrayArg[@]} ) ;
      fi
    fi
  }
  function RegExpLoopParse()
  {
    local IntRegExpParse=0;
    for(( IntY=0 ; intY <= ${#ArrayInFor[@]}-1 ;intY++ )) ; do
     local IntLengthArgInit=${#ArrayInFor[${IntY}]};
     local StrCopyArg=${ArrayInFor[${IntY}]/${ParseTagArray}/} ;
     local IntCopyArgLength=${#StrCopyArg} ;
     if [ "${IntLengthArgInit}" -ne "${IntCopyArgLength}" ] ; then
       IntRegExpParse=1 ;
       break 1 ;
     fi
    done
  }
  function ScanLoop()
  { ### By default using egrep is not a problems, may
    ### be slow with an excessive amount of Item in an
    ### Array, or if the limitation from ArrayArgMod is removed...
    ###
    if [ ${IntUsingEgrepScanLoop:=0} -eq 1 ] ; then
      local StrRegExpParse=$( echo "${ArrayInFor[@]}" | egrep -ic "${ParseTagArray}" ) ;
    else
      RegExpLoopParse ;
    fi
    echo "${IntRegExpParse:=0}" ;
    #echo "${StrRegExpParse:=0}" ;
  }

  Base64Handler ;

  local IntNeedParse=$( ScanLoop ${ArrayInFor[@]} ) ;
  	ArrayInFor=( $( echo ${ArrayInFor[@]//__ARRAY__/$ArrayName} ) ) ;
  echo "${ArrayInFor[@]}" ;
}

### Specialization of __in_for
###
###
__for()
{
  eval $( __call_localityLocalName=For __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
  local CmdEval=( "eval" "$(" "__in_for" "${ArrayArg[@]}" ")" )  ;
  eval "${CmdEval[@]}"  ;
}

### Unset GetSpacer ;
### Unset this function is quite problematic in user display experience.
unset GetSpacer ;
function GetSpacer()
{
  eval $( __call_localityLocalName=GetSpacer __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
  unset PreProcess ShowVarDebug InitCharSpacer AttributeCharSpacer ArrayInit ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ProcessShowVarDebug           FParamVarName=IsShowVarDebug         FParamDefaultValue="False"   __fnctCreateLocalityFuncParam   ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ProcessAttributeCharSpacer    FParamVarName=IsAttributeCharSpacer  FParamDefaultValue="True"   __fnctCreateLocalityFuncParam   ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ProcessCharSpacer             FParamVarName=IsCharSpacer           FParamDefaultValue="True"   __fnctCreateLocalityFuncParam   ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Char                          FParamVarName=StrCharSpace           FParamDefaultValue=Star   __fnctCreateLocalityFuncParam   ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=CharId                        FParamVarName=IntCharSpaceId         FParamDefaultValue=None   __fnctCreateLocalityFuncParam   ) ; 
  
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=StarChar                      FParamVarName=StrStartChar           FParamDefaultValue=None   __fnctCreateLocalityFuncParam   ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=EndChar                       FParamVarName=StrEndChar             FParamDefaultValue=None   __fnctCreateLocalityFuncParam   ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Stream                        FParamVarName=StrStream              FParamDefaultValue=None   __fnctCreateLocalityFuncParam   ) ; 
  
  local ArrayInit=( CharSpacer AttributeCharSpacer ) ; 
  local StrChr="" ;
  local IntSpacer=${ArrayArg[0]} ;
  local IsCharFound=0 ;
  IntSpacer=${IntSpacer:=0} ;
  local StrCharOut="" ;
  local IntProcessEntity="False" ;
  
  function PreProcess( )
  {
    eval $( __call_localityLocalName=PreProcess __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
    eval "IntProcessEntity=\${Is${ArrayArg[0]}}" ;
    if [ "${IntProcessEntity:=False}" == "True" ] ; then 
     eval ${ArrayArg[0]} ;
    fi
  }
  
  function ShowVarDebug()
  {
    eval $( __call_localityLocalName=ShowVarDebug __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
    local StreamDisplay="""Variable IntCharSpaceId,        Value : ${IntCharSpaceId}
Variable IsShowVarDebug,        Value : ${IsShowVarDebug}
Variable IsCharSpacer,          Value : ${IsCharSpacer}
Variable IsAttributeCharSpacer  Value : ${IsAttributeCharSpacer}
Variable StrStartChar,          Value : ${StrStartChar}
Variable StrEndChar,            Value : ${StrEndChar}
Variable StrStream,             Value : ${StrStream}
Default Char Used : <Char; ${StrCharSpace}>\nSpacer Length:${IntSpacer}\n""" ;
  echo -ne "${StreamDisplay}" > /dev/stderr ;
  }

  
  function InitCharSpacer()
  {
    eval $( __call_localityLocalName=InitCharSpacer __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
    if [ ${IsCharFound:=0} -ne 1 ] ; then 
     if [ "${StrCharSpace:=Star}" == "${ArrayCharSpacerName[${intArrayCharSpacerName}]}" ] ; then 
       StrChr="${ArrayCharSpacerConv[${intArrayCharSpacerName}]}" ; 
       IsCharFound=1 ;
     fi
    fi
  }
  
  function AttributeCharSpacer()
  {
    eval $( __call_localityLocalName=AttributeCharSpacer __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
    if [ ${IntSpacer:=0} -gt 0 ] ; then
      for (( intx=0 ; intx <= $(( ${IntSpacer}-1 )) ; intx++ )) ; do 
        StrCharOut="${StrCharOut}${StrChr}"
      done ;
    else
      StrCharOut="" ; 
    fi
  }
  
  function CharSpacer()
  {
    eval $( __call_localityLocalName=CharSpacer __call_localityDisplayFunctionEntry=0 __call_locality ) ; 
    if [ "${IntCharSpaceId:=None}" == "None" ]; then 
     eval $( __in_for ArrayCharSpacerName InitCharSpacer ) ; 
    else
     StrChr=${ArrayCharSpacerConv[${IntCharSpaceId}]} ;
    fi
  }
  
 
  eval $( __in_for ArrayInit PreProcess ) ;
  echo -ne "${StrCharOut}" ;
  
}


function FileLoadScript()
{
  
  eval $( __call_localityLocalName=FileLoadScript __call_locality ) ; 
  local StrSpaceSize ;
  local SizeMaxHead=40 ;
  local IntDiffSize=$(( ${SizeMaxHead} - ${#ArrayArg[1]} )) ;
  local StrSpaceSize=$( GetSpacerCharId=1 GetSpacer ${IntDiffSize} ) ;

  function __OK()
  {
    eval $( __call_localityLocalName=CmdOK __call_locality ) ; 
    echo -ne "\t${ArraySubFuncCall[${intArraySubFuncCall}]}${StrSpaceSize}\t[ OK ]\n" ;  
  }
  
  function __Fail()
  {
    eval $( __call_localityLocalName=CmdFail __call_locality ) ; 
    echo -ne "\t${ArraySubFuncCall[${intArraySubFuncCall}]}${StrSpaceSize}\t[ Fail ]\n" ;
  }

  . ${ArrayArg[0]}/${ArrayArg[1]} ;
  local IntErrorLoading=$? ;
  local CmdEval=( """
   if [ \${IntErrorLoading:=1} -eq 0 ] ; then 
    __OK ; 
   else 
    __Fail ; 
   fi ; """ )  ;
  eval "${CmdEval[@]}" ;
}

function StartLoading()
{
  local ArrayArg=( $* ) ;
  echo -ne "Loading Script Sub Function\n"; 
  eval $( __in_for ArraySubFuncCall FileLoadScript ${ABaseRoot} ) ;
  unset StartLoading FileLoadScript ArraySubFuncCall ABaseRoot ;
}


unset __unset ;
__unset()
{
  eval $( __InitFunc __unset ) ;
  local StrFuncName=( __unset );
  function __functor_unset()
  {
    eval $( __InitFunc __functor_unset );
    local CmdEval=( "unset" \"${ArrayArg[${IntDefaultItemValue}]}\" ) ;
    eval "${CmdEval}" ;
  }
  eval $( __in_for ArrayArg __functor_unset ) ;
}

__get_background_jobs()
{
  local ArrayArg=( $* ) ;
  local IntJob=( $( jobs -p | tr '[:cntrl:]' ' ' ) ) ;
  local StrFuncName=( ) ;
  IntJob="${#IntJob[@]}" ;
  local StrTaskType=${ArrayArg[${IntDefaultItemValue}]} ;
  if [ "${StrTaskType:=number}" == "number" ] ; then
    echo "${IntJob:=0}" ;
   elif [ "${StrTaskType:=number}" == "id" ] ; then
    if [ "${IntJob:=0}" -gt 0 ] ; then
       echo "${IntJob[${ArrayArg[1]}]}" ;
    fi
   elif [ "${StrTaskType:=number}" == "kill" ] ; then
    if [ "${IntJob:=0}" -gt 0 ] ; then
       echo "kill -9 ${IntJob[${ArrayArg[1]}]}" ;
    fi
   fi
}

__init_time_var()
{
    local ArrayArg=( $* ) ;
    local StrFuncName=( ) ;
    local IntNbArg=${#ArrayArg[@]}
    if [ ${IntNbArg:=0} -gt 1 ] ; then
      echo "local ${ArrayArg[${IntDefaultItemValue}]}=$(( ${ArrayArg[1]}-${ArrayArg[2]} )) ;" ;
    else
      echo "local ${ArrayArg[${IntDefaultItemValue}]}=$( date +\"%s\" ) ;" ;
    fi
}
function __InitFunc()
{
  ### Warning __InitFunc() does not support base64 wrapping information in this version, so refer to
  ### . /etc/init.d/fnct.d/fnct_lib for Initial Function and note :
  ### Any Function from the main . /etc/init.d/fnct.d/fnct_lib can be re-handled by re-writing same function_name
  ### in any sub call_file, so beware ...
  ###
  ### This information was provided for regression-test feasibility and energy-times saving in somes cases...
  ###
  ###
  #. /etc/init.d/fnct.d/fnct_lib ;
  eval $( __call_locality ) ;
  ### echo > temp ; 
  function __functor_call_push_action()
  {
    echo "${ArrayCondPushArg[${IntCx}]}" ;
    ### echo "${ArrayCondPushArg[${IntCx}]}" >> temp ;
  }  
  function __fuctor_loop_recall_arg()
  {
    #echo "AllArg:[${ArrayCondPushArg[@]}]" >> temp ;  
    for(( IntCx=0 ; IntCx <= ${#ArrayCondPushArg[@]} ; IntCx++ )) ; do 
      __functor_call_push_action  ; 
    done 
  }
  
  local ArrayCondPushArg ;
  echo "eval \$( __call_locality )" ; 
  echo "eval \$( __prompt_var_extraction )" ; 
  local IntArgCount=${#ArrayArg[@]} ;
  if (( ${IntArgCount} >= 1 )) ; then 
    echo "local IntArrayItemValue=\$((\${#ArrayArg[@]}+1)) ; " ;
    echo "local __STR_LOOP_VALUE__=\"\${ArrayArg[\${IntArrayItemValue}]}\"" ;
  else
    echo "local IntArrayItemValue=\$((\${#ArrayArg[@]})) ; " ;
    echo "local __STR_LOOP_VALUE__=\"${ArrayArg[\${IntArrayItemValue}]}\"" ;
  fi 
  local IntFuncNameInspect=${#StrFuncName} ;
  if (( ${IntFuncNameInspect:=0} == 0 )) ; then 
    eval "echo \"local StrFuncName=\${ArrayArg[0]}\"" ; 
  else
    eval "echo \"local StrFuncName=\${StrFuncName}.\${ArrayArg[0]}\"" ; 
  fi 
  #__fuctor_loop_recall_arg
}


__get_lib_symbols()
{
  eval $( __InitFunc __get_lib_symbols ) ;
  local StrFuncName=( ) ;
  echo -ne "\n\n-------------------\n\tExtracted Symbols: ${ArrayArg[${IntArrayItemValue}]}\n\tArrayObjDumpOptionType:${IntOptionType}, List:[${ArrayObjDumpOptionType[${IntOptionType:=0}]}]\n-------------------\n\n" ;
  local CmdEval=( ${Program:=objdump} ${ProgramOptions:=${ArrayObjDumpOptionType[${IntOptionType:=0}]} ${ArrayArg[${IntArrayItemValue}]}} ${ProgramQuery:=${ObjLibName:=/usr/lib/libots-1.so.0.5.0}} ) ;
  eval "${CmdEval[@]}" ;
  eval ${CmdEval[@]} ;
}

__fnctInitType()
{
  local ArrayArg=( $* ) ;
  local IntNbArg=${#ArrayArg[@]} ;
  local IntParseEmbeded=$( echo ${ArrayInitType[${ArrayArg[0]}]} | egrep -ic "__[a-zA-Z0-9]+__" ) ;
  if [ ${IntParseEmbeded:=0} -gt 0 ] ; then
    if [ ${IntNbArg} -gt 1 ] ; then
     echo "${ArrayInitType[${ArrayArg[0]}]//__${ArrayArg[1]}__/${ArrayArg[2]}}" ;
    else
      echo "echo \"Problems of pasing, no argument passed and TAG exist inside query.\";" ;
      return 1 ;
    fi
  else
    echo "${ArrayInitType[${ArrayArg[0]}]}" ;
  fi
}

PythonPackage()
{
  local ArrayArg=( $* ) ;
  local ArrayPipEventTrigger=( "Successfully installed" "Requirement already satisfied" ) ;
  local ArrayPipEventCondition=( "pip install __PACKAGE__ " "pip install --upgrade __PACKAGE__ " ) ;
  local OnTrueExit=1;
  local OnFalseExit=1;
  local ArrayPipEventContitionStatement=( ${OnTrueExit} ${OnTrueExit} ) ;

  local ArrayBase=( ${ArrayArg[0]/_// } ) ;
  declare EvalStatementMaster=( "if" "[" "\${IntAnswer:=0}" "-eq" "0" "]" ";" "then" "IntAnswer=\$(" "__0" "|"  "__1" ")" ";" "if" "[" "\${IntAnswer:=0}" "-eq" "__2" "]" ";" "return 1" ";" "fi" ";" "fi" ) ;

  function PipInstallQueue()
  {
    local ArrayArg=( $* ) ;
    local IterPos=${intArrayPipEventContitionStatement} ;
    local ArrayFormatProcess=( ${ArrayPipEventCondition[${IterPos}]/__PACKAGE__/${ArrayBase[${intArrayBase}]}} ${ArrayPipEventTrigger[${IterPos}]} ${ArrayPipEventContitionStatement[${IterPos}]} )
    declare IntAnswer=0 ;
    declare -a Template=( ${EvalStatementMaster[@]} ) ;
    function __ProcesControl()
    {

      function __0()
      {
        echo "${ArrayFormatProcess[${intArrayFormatProcess}]}" ;
      }
      function __1()
      {
        echo "egrep -ic ${ArrayFormatProcess[${intArrayFormatProcess}]}" ;
      }
      function __2()
      {
        echo "${ArrayFormatProcess[${intArrayFormatProcess}]}" ;
      }
      Template=( ${Template[@]//__TAG__/__${intArrayFormatProcess} | __TAG__} ) ;
    }
    eval $( __in_for __ProcesControl ArrayFormatProcess )
    local IterFuncPos=${intArrayPipEventContitionStatement} ;
    local CmdEval=( ${Template[@]//__${IterFuncPos}/$( __${IterFuncPos} )} ) ;
    echo "CmdLine:[${CmdEval[@]}]" ;
    eval "${CmdEval[@]}" ;
  }
  eval $( __in_for ArrayPipEventContitionStatement PipInstallQueue )

  function PythonPackageInstallerPipe()
  {
    local ArrayArg=( $* ) ;

    function CatchEvent()
    {
      local ArrayArg=( $* ) ;
      local IsTriggered=$( echo "${TriggerStatement[${intTriggerStatement}]}" | egrep -ic "${ArrayArg[0]}" )  ;
      if [ ${IsTriggered:=0} -gt 0 ] ; then
        echo "" ;
      fi
    }

    function Trigger()
    {
      local ArrayArg=( $* ) ;
      local TriggerStatement=( $( pip install ${ArrayPythonPackage[${intArrayPythonPackage}]} ) ) ;
      local ErrorStatement=$? ;
      if [ ${ErrorStatement:=0} -eq 1  ] ; then
        echo -ne "\n\n\tError Installing thru PIP.\n\tModule:${ArrayArg[0]}\n\n" ;
      else
         eval $( __in_for TriggerStatement CatchEvent )
      fi

    }
    eval $( __in_for ArrayPipEventTrigger Trigger ) ;

  } ;
  declare -a ArrayPythonPackage=( ${ArrayArg[@]} ) ;
  eval $( __in_for ArrayPythonPackage PythonPackageInstallerPipe ) ;
} 

SCSIUnpoolerDisk()
{
  eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=Device_unpool_test2 __call_locality );

  local FileName=( /etc/mtab /home/maxiste/mtab.temp mtab )
  local DeviceUnpoolBase64=( L2Rldi9zZGMxIC9tZWRpYS9DSEtORk1HVzMyIHZmYXQgcncsbm9zdWlkLG5vZGV2LHVoZWxwZXI9ZGV2a2l0LHVpZD0xMDAwLGdpZD0xMDAwLHNob3J0bmFtZT1taXhlZCxkbWFzaz0wMDc3LHV0Zjg9MSxmbHVzaCAwIDAK );
  local DeviceUnpoolable=( /dev/sdc1 ) ;
  local DeviceUnpoolDecoded=$( Base64Decode ${DeviceUnpoolBase64[0]} ) ;
  echo "Based Unpooled segment:${DeviceUnpoolDecoded}" ;
  local ArrayTimeSleep=();

  function TestScsi()
  {
    eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=TestScsi __call_locality );
    function __fnct_scsi_ready()
    {
     eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=__fnct_scsi_ready __call_locality );
     local ReturnInfo=$( scsi_ready ${ArrayArg[0]} | tr '[:cntrl:]' '|' | sed 's/\(sg_turs\)/|\1/g' ) ;
     echo "${ReturnInfo}" > /dev/stderr ;
    }

    local ArraySCSI=( $( scsiinfo -l ) ) ;
    eval $( __in_for ArraySCSI __fnct_scsi_ready  ) ;
  } ;

  function Base64Decode()
  {
   eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=Base64Decode __call_locality );
   echo "${ArrayArg[0]}" | base64 --wrap=0 -d ;
  }

  function SleepProcess()
  {
   eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=SleepProcess __call_locality );
   echo "Sleeping for ${ArrayArg[0]} sec. " > /dev/stderr ;
   sleep ${ArrayArg[0]} ;
  }

  function UnmountPooledDevice()
  {
   eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=UnmountPooledDevice __call_locality );
   local ErrorStatementUmount=1;
   local IntCount=0;
   local ArrayUnmountOption=( -f -l ) ;
   while [ ${ErrorStatementUmount:=0} -ne 0 ] ; do
    local CmdEval=( "umount" "${ArrayUnmountOption[${IntCount}]}" "${ArrayArg[0]}"  );
    echo -ne "\n\tCmdLine:[${CmdEval[@]}]\n" ;
    eval "${CmdEval[@]}" ;
    ErrorStatementUmount=$? ;
    (( IntCount+=1 )) ;
   done
  }
  function CheckFileDevice()
  {
   eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=CheckFileDevice __call_locality );
   local IntMtabFree=1;
   while [ ${IntMtabFree:=1} -ne 0 ] ; do
     echo "${ArrayArg[0]} not free" ;
     IntMtabFree=$( lsof -w | egrep -ic --no-filename "${ArrayArg[0]}" 2> /dev/null ) ;
     echo "IntMtabFree State:[${IntMtabFree}]" ;
     sleep 1 ;
   done
  }
  function SetRandom()
  {
   eval $(  __call_localityDisplayFunctionEntry=1 __call_localityLocalName=SetRandom __call_locality );
   local ArrayRandomName=${ArrayArg[2]};
   ArrayRandomName=${ArrayRandomName:=ArrayTimerSleep} ;
   for(( intx=0;intx<=${ArrayArg[0]}-1;intx++));do
    local IntRandom=$(( (${RANDOM} % ${ArrayArg[1]})+1 )) ;
    echo -ne "Adding random number:${IntRandom} in List\n" > /dev/stderr ;
    local CmdEval=( "${ArrayRandomName}[${intx}]=${IntRandom}" ) ;
    echo -ne "\n\tCmdLine:[${CmdEval[@]}]\n" > /dev/stderr ;
    eval "${CmdEval[@]}" ;
   done
  }

  local IntSleepCount=0;
  local IntMaxSleep=100 ;
  while [ 1 ] ; do

   if [ ${IntSleepCount:=0} -eq 0 ] ; then
     SetRandom ${IntMaxSleep} 20 ArrayTimeSleep ;
   fi
   echo "Array ArrayTimeSleep:[${ArrayTimeSleep[@]}]" ;

   eval $( __in_for FileName CheckFileDevice )
   echo "${DeviceUnpoolDecoded}" >> ${FileName[0]} ;
   TestScsi ;
   SleepProcess ${ArrayTimeSleep[0]} ;

   eval $( __in_for FileName CheckFileDevice )
   egrep -iv "${DeviceUnpoolDecoded}" ${FileName[0]} > ${FileName[1]} ;

   eval $( __in_for FileName CheckFileDevice )
   cat ${FileName[1]} > ${FileName[0]} ;

   eval $( __in_for FileName CheckFileDevice )
   SleepProcess ${ArrayTimeSleep[1]} ;

   #eval $( __in_for DeviceUnpoolable UnmountPooledDevice ) ;

   if [ ${IntSleepCount:=0} -gt ${IntMaxSleep} ] ; then
     IntSleepCount=0;
   else
     ((IntSleepCount+=1)) ;
   fi

  done

}

### This one can only be acheived if you download 2C from ( cl2cru, or I.P.Pelletier  )
### http://code.google.com/p/2c-python/downloads/list.
### Uncompress the content in you Python 2.x( mostly /usr/local/lib/python2.x/dist-packages path )
###
###
CompilePythonFile()
{
 eval $( __call_localityLocalName=CompilePythonFile __call_locality );

 function get_file_list()
 {
  eval $( __call_localityLocalName=get_file_list __call_locality );
  local DefaultPath=${ArrayArg[0]};
  DefaultPath=${DefaultPath:=./} ;
  local CmdEval=( "find ${DefaultPath} -maxdepth 1 -type f -iname \"*.py\" -printf \"%p \"" "|" "sed 's/\.\///g'"  ) ;
  echo -ne "CmdLine:${CmdEval[@]}\n" > /dev/stderr ;
  eval "${CmdEval[@]}" ;
 }

 function CompilePython2C()
 {
  eval $( __call_locality ) ;
  local CmdEval=( "python${ArrayPythonVer[1]}" "${ArrayPython26Path[1]}/2C.py" "${ArrayArg[0]}" ) ;
  echo -ne "CmdLine:[ ${CmdEval[@]} ]\n" ;
  eval "${CmdEval[@]}" ;
 } ;

 local ArrayPyCompile=( $( get_file_list ${ArrayArg[@]} ) ) ;

 eval $( __in_for ArrayPyCompile CompilePython2C ) ;
}

unset ZenityLdConfig ;
function ZenityLdConfig()
{
  eval $( __call_localityLocalName=COMMAND __call_localityDisplayFunctionEntry=1 __call_locality ) ;

  local ArrayArgMaster=( ${ArrayArg} ) ;

  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DisplayFrameProg     FParamVarName=StrDisplayFrameProg    FParamDefaultValue=zenity                __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Width                FParamVarName=IntWidth               FParamDefaultValue=800                   __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=WidthProgress        FParamVarName=IntWidthProgress       FParamDefaultValue=600                   __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Height               FParamVarName=IntHeight              FParamDefaultValue=600                   __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Title                FParamVarName=StrTitle               FParamDefaultValue="LdConfig Dependency" __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Text                 FParamVarName=StrText                FParamDefaultValue="Updated Lib"         __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Col1                 FParamVarName=ArrayCol[0]            FParamDefaultValue="Updated"             __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Col2                 FParamVarName=ArrayCol[1]            FParamDefaultValue="__OFFICIAL__"        __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Col3                 FParamVarName=ArrayCol[2]            FParamDefaultValue="__VERSION__"         __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=WithProgress         FParamVarName=IsProgresShow          FParamDefaultValue=False                 __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DefaultLibState      FParamVarName=LibStateStr            FParamDefaultValue=FALSE                 __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DefaultScriptLoader  FParamVarName=StrDefaultScriptLoader FParamDefaultValue=Zenity_OTS_Resume __fnctCreateLocalityFuncParam ) ;

  local LoaderLocalTitle="Loading ${StrDefaultScriptLoader} " ;
  local StrLibName="Lib's Official Name" ;
  local StrLibSubVersion="Lib's SubVersion Name" ;
  local ClassicTitle="Ldconfig update lib dependency" ;

  unset ZenityProgress ZenityLdConfigList ListAwkFilter VerboseLdConfig IDLEPython ;

  function ZenityProgress()
  {
    eval $( __call_localityLocalName=ZenityProgress __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Title FParamVarName=StrTitle FParamDefaultValue=ClassicTitle FParamIsInterpretVar=True __fnctCreateLocalityFuncParam ) ;
    local IntRand=$(( ${RANDOM} % 25 )) ;
    echo -ne "Title : ${StrTitle}\n" > /dev/stderr ;
    eval "zenity --progress --pulsate --width=${IntWidthProgress} --text=\"${StrTitle}\" --percentage=$(( 75 + ${IntRand} ))  --auto-close " ;
  }

  function ZenityLdConfigList()
  {
    eval $( __call_localityLocalName=ZenityLdConfigList __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    ${StrDisplayFrameProg} --width=${IntWidth} --height=${IntHeight} --title "${StrTitle}" --text "${StrText}" --list --checklist --column "${ArrayCol[0]}" --column "${ArrayCol[1]/__OFFICIAL__/${StrLibName}}" --column "${ArrayCol[2]/__VERSION__/${StrLibSubVersion}}" ${ArrayLibConfigList[@]} ;
  }

  function ListAwkFilter()
  {
    eval $( __call_localityLocalName=ListAwkFilter __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    awk -vLibState=${LibStateStr} 'BEGIN{}{ Xret="False" ; Ares="" ; for( intx=1 ; intx <= NF ; intx++ ){ if( $(intx) ~ /^lib/ ){ Xret="True" ; Ares=sprintf("%s %s ",Ares,$(intx) ) ; } ; } ; if( Xret == "True" ){ printf("%s %s ",LibState,Ares ) ; } ; }END{}'
  }

  function VerboseLdConfig()
  {
    eval $( __call_localityLocalName=VerboseLdConfig __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    sudo -s ldconfig -vf /etc/ld.so.conf
  }

  function Loader()
  {
    eval $( __call_localityLocalName=VerboseLdConfig __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    eval "${StrDefaultScriptLoader}" ;
  }

  local ArrayLibConfigList=( $( VerboseLdConfig | ListAwkFilter ) );
  local ArrayProg=( ZenityLdConfigList Loader ) ;
  local ArrayProgOption=( ZenityProgressTitle=ClassicTitle ZenityProgressTitle=LoaderLocalTitle ) ;
  function ConfigLoad()
  {
    eval $( __call_localityLocalName=VerboseLdConfig __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    if [ "${IsProgresShow}" == "True" ] ; then
      eval "${ArrayProg[${intArrayProg}]} | ${ArrayProgOption[${intArrayProgOption}]} ${ArrayArg[0]}"
    else
      eval "${ArrayProg[${intArrayProg}]} " ;
    fi
  }
  eval $( __in_for ArrayProg ConfigLoad ZenityProgress ) ;
}

function CondEvalParamPretest()
{
  eval $( __call_locality __call_localityLocalName=CondEvalParamPretest __call_localityDisplayFunctionEntry=1 ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=PathArrayExecRestriction   FParamVarName=StrExecRestriction        FParamDefaultValue=ArrayEnableAction __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=CommandEvalArrayName  FParamVarName=StrCmdEvalName        FParamDefaultValue=CmdEval __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=MemberTrue            FParamVarName=StrMemberTrue         FParamDefaultValue=True __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DeviceOutCmd          FParamVarName=StrDeviceOutCmd[0]    FParamDefaultValue=/dev/stderr __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DeviceOutCmd1         FParamVarName=StrDeviceOutCmd[1]    FParamDefaultValue=echo __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DeviceRedirAction     FParamVarName=StrDeviceRedirAction  FParamDefaultValue=GreaterThan __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DeviceHandlerIsOS     FParamVarName=IsDeviceHandlerOS     ParamDefaultValue=True __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Action0               FParamVarName=ArrayAction[0]        FParamDefaultValue=DeviceOutRedirection __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Action1               FParamVarName=ArrayAction[1]        FParamDefaultValue=EvaluationInit __fnctCreateLocalityFuncParam ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Action2               FParamVarName=ArrayAction[2]        FParamDefaultValue=ParseLoader __fnctCreateLocalityFuncParam ) ;

  ### Tweak Within redirection way...
  ### By default, all redirection are set to /dev/stderr. Producing an '> /dev/stderr' at the end of designed
  ### StreamOut sequence of code. Exception is when netcat, or NC or any other program can be involved...
  ### Most of the time, program like netcat, nc can support Pipe instruction from stdin... like echo "__Stream__" | nc ...
  ### To activate this you need to specify ${StrFuncName}DeviceHandlerIsOS=False, ${StrFuncName}DeviceRedirAction=Pipe
  ### like Array in ArrayCharSpacerName, from fnct_var_decl, and defining something else than echo in
  ### ${StrFuncName}DeviceOutCmd1. like ${StrFuncName}DeviceOutCmd1=__fnct_nc ( it's better to assign a script, because )
  ### passing space here is not likely to love chained-mechanism...
  ### so It produce : echo "__Stream__" | __fnct_nc and can send you out information on paired-network.

  local IntDeviceOut=0 ;
  local CharCtrl="" ;
  local StrHardwareRedir="" ;
  local StrActionTest="" ;
  local StrEvalAction="" ;
  local StrEvalFailAction="" ;
  local StrDevOut="" ;
  local Template="" ;
  local ArrayRegVar=( StrActionTest StrMemberTrue StrEvalAction StrEvalFailAction StrDevOut ) ;
  local ArrayNoQuoteParse=( StrDevOut );
  local MasterTemplate=( "if" "[" "__StrActionTest__" "==" "__StrMemberTrue__" "] ;" "then" "eval" "__StrEvalAction__" ";" "else" "echo" "-ne" "__StrEvalFailAction__" "__StrDevOut__" ";" "fi"  ) ;
  function Parse()
  {
    eval $( __call_locality __call_localityLocalName=ParseAction __call_localityDisplayFunctionEntry=1 ) ;
    local IsQuotable=$( echo "${ArrayNoQuoteParse[@]}" | egrep -c --no-filename "${ArrayArg[0]}" ) ;
    if [ ${IsQuotable:=0} -gt 0 ] ; then
      eval "local ValueEval=\${${ArrayArg[0]}}" ;
    else
      eval "local ValueEval=\"\${${ArrayArg[0]}}\"" ;
    fi
    echo -ne "Testing Value ${ArrayArg[0]}, Value: ${ValueEval}\n" ${StrHardwareRedir} ;
    Template=( ${Template[@]//__${ArrayArg[0]}__/${ValueEval}} ) ;
  }

  function DeviceOutRedirection()
  {
    eval $( __call_locality __call_localityLocalName=DeviceOutRedirection __call_localityDisplayFunctionEntry=1 ) ;
    if [ ${IsDeviceHandlerOS} == "True" ] ; then
      IntDeviceOut=0 ;
    else
      IntDeviceOut=1 ;
    fi
    CharCtrl=$( GetSpacerChar=${StrDeviceRedirAction} GetSpacer 1 ) ;
    StrHardwareRedir="${CharCtrl} ${StrDeviceOutCmd[${IntDeviceOut}]}" ;
  }

  function EvaluationInit()
  {
    eval $( __call_locality __call_localityLocalName=EvaluationInit __call_localityDisplayFunctionEntry=1 ) ;
    eval "StrActionTest=\"\${${StrExecRestriction}[\${int${StrExecRestriction}}]}\"" ;
    eval "StrEvalAction=\${${StrCmdEvalName}[@]}" ;
    StrEvalFailAction="Following Action where disabled:\n\t CmdLine:[ \${StrEvalAction} ]" ;
    StrDevOut="> ${StrDeviceOutCmd}" ;
    Template=( ${MasterTemplate[@]} ) ;
  }

  function ParseLoader()
  {
    eval $( __call_locality __call_localityLocalName=ParseLoader __call_localityDisplayFunctionEntry=1 ) ;
    eval $( __in_for ArrayRegVar Parse ) ;
    echo -ne "Template: [ ${Template[@]} ]\n" > /dev/stderr ;
    echo -ne "${Template[@]}" ;
  }

  function __exec()
  {
    eval $( __call_locality __call_localityLocalName=ExecStatement __call_localityDisplayFunctionEntry=1 ) ;
    ${ArrayArg[0]} ;
  }

  function MainAction()
  {
    eval $( __call_locality __call_localityLocalName=MainAction __call_localityDisplayFunctionEntry=1 ) ;
    eval $( __in_for ArrayAction __exec ) ;
  }

  echo -ne "Registry: ArrayAction:[ ${ArrayAction[@]} ]\n" > /dev/stderr ;
  echo -ne "Registry: ArrayEnableAction:[ ${ArrayEnableAction[@]} ]\n" > /dev/stderr ;
  echo -ne "Registry: ArrayCompressorOption:[ ${ArrayCompressorOption[@]} ]\n" > /dev/stderr ;

  MainAction ;
}

### Inline Array ReDeclaration :
### This tiny method allow inserting a position-0, an array Name and create a new one from 
### listed element from Element[1] to ${#Element[@]} 
### 
function ArrayInlineRedecl()
{
  eval $( __call_localityLocalName=Redecl  __call_locality ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName FParamVarName=StrArrayName FParamDefaultValue=CmdEval __fnctCreateLocalityFuncParam     )  ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Debug FParamVarName=IsDebug FParamDefaultValue=False __fnctCreateLocalityFuncParam     ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DeclType FParamVarName=StrDeclType FParamDefaultValue=local __fnctCreateLocalityFuncParam     ) ; 
  
  local ArrayEvalDecl=( "local" "declare -a" ) ;
  
  local EnumIntArrayEvalDecl=0 ;
  
  function GetDeclType()
  {
   eval $( __call_localityLocalName=GetDeclType  __call_locality ) ;
   eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DeclStub FParamVarName=StrDeclStub FParamDefaultValue=process __fnctCreateLocalityFuncParam     )  ; 
   
   function ArrayDeclCreate()
   {
     echo -ne """local ArrayEvalDecl=( \"local\" \"declare -a\" ) ;""" ;
   }
   
   function EnumDeclCreate()
   {
     echo -ne """ local EnumIntArrayEvalDecl=0 ; """ ;
   }
   
   function Action()
   {
    case ${StrDeclType} in
     "local" )
      EnumIntArrayEvalDecl=0;
     ;;
     "global" )
      EnumIntArrayEvalDecl=1;
     ;;
    esac
   }
   
   case ${StrDeclStub} in
    "process" )
    Action ;
    ;;
    "array" )
    ArrayDeclCreate ;
    ;;
    "enum" )
    EnumDeclCreate ;
    ;;
    
   esac 
  }
  
  eval "local StrNameArray=\${${StrArrayName}[0]}" ;
  local CmdLineEval=( """__DECLTYPE__${StrNameArray}=( \${${StrArrayName}[@]:2}  );"""  ) ;
  if [ "${IsDebug}" == "True" ] ; then 
   echo -ne "CmdLine:\n\t${CmdLineEval[@]}\n" > /dev/stderr ; 
  fi 
  eval "${CmdLineEval[@]}" ;
}


### Inline Array Content Insertion :
### This tiny method allow to insert an array name inside a Parsed __ARRAY__ Tag
### and re-evaluate the content within the declaration.
### 
function ArrayInlineCmdParser()
{
  eval $( __call_localityLocalName=Redecl  __call_locality ) ;
  #eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName FParamVarName=StrArrayName FParamDefaultValue=CmdEval __fnctCreateLocalityFuncParam     )  ; 
  #eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Debug FParamVarName=IsDebug FParamDefaultValue=False __fnctCreateLocalityFuncParam     ) ; 
  
  eval "local StrNameArray=\${${StrArrayName}[0]}" ;
  local CmdLineEval=( """__DECLTYPE__${StrNameArray}=( \${${StrArrayName}[@]:2}  );"""  ) ;
  if [ "${IsDebug}" == "True" ] ; then 
   echo -ne "CmdLine:\n\t${CmdLineEval[@]}\n" > /dev/stderr ; 
  fi 
  eval "${CmdLineEval[@]}" ;
}
