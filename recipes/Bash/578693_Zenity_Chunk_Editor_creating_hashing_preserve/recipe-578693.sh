unset ZenityShellEval ;
function ZenityShellEval()    
{ 
 local __call_locality=( ZSE ZenityShellEval ) ;
 local ArrayArg=( $* ) ; 
 local Arg0=${ArrayArg[0]}              ;
 local IntSleep=${ZSESleepInterval:=5}  ;
 local IntFontSize=${ZSEFontSize:=12}   ; 
 local IsEditField=${ZSEEditable:=True} ; 
 local IsAddFootPrint=${ZSEAddFootPrint:=True} ; 
 local StrTitle=${ZSEZenityTitle:='Shell Evaluation command'} ;
 local StrFileName=${ZSEFileName:=None} ;
 local StrDateFormat=${ZSEDateFormat:=%Y%m%d-%H:%M:%S,%s}
 local IntDefaultModeExec=${ZSEChmodFileExec:=775} ;
 local StrFilePath=${ZSEPathStorage:=./} ; 
 local IntWidth=${ZSEWindowWidth:=640} ;
 local IntHeight=${ZSEWindowHeight:=400} ;
 local IsLoopOnSucc=${ZSELoopOnSucc:=True} ; 
 local IsCheckSumOnly=${ZSECheckSumTest:=False} ; 
 
 ### Note: f1161962-0ad8-11e3-b166-001b3875b29c 
 ### 
 ### Title : Variable Forwarding Example in BoolVarTestVarCreation & mutation 
 ### of BoolVarTestVarCreation from True/False test into None
 ### 
 ### BoolVarTestVarCreation for substitution of StrFileTmp has unidirectionnaly
 ### a uuid-like file name into Pre-fixed Var ZSEFileName:=None for 
 ### affectation inside StrFileName=None, where if this one != None, will 
 ### get the parameter Name Being passed inside StrFileTmp. 
 ### 
 ### - Had consequence:
 ###  - if the file does not exist, an echo > StrFileTmp will be done . 
 ###  - if the file exist, content will be open by Zenity in text-info --editable
 ###  - Selected filename supplied, content will be overwritted and there is 
 ###  no protection mechanism and no verification against file-permission
 ###    - To this, a workaround will store all code generated from this application
 ###    - into sub-directory being made by the command and store-it inside user
 ###      respective home location which is safe and Pre-fixable into 
 ###      your specification, and not-warrented to be correct but designable. 
 ###  
 ### 
 ### - If the variable ZSEFileName is untouched, the content of StrFileTmp will
 ### hold value 'None' and belong to parsed BoolVarTestVarCreation it should 
 ### get it's uuid-like filename, see generated command from parameter below
 ### 
 ### Command : BVTestVarName=StrFileTmp BVTestVarHold='${StrFileName}' BVTestBoolVarName=\${StrFileName} BVTestBoolCase=None BVTestBoolAssertion='$( uuidgen -t )' BVTestScopeTest=local BoolVarTestVarCreation
 ### 
 ### generated code:
 ### local StrFileTmp="${StrFileName}" ; 
 ### if [ "${StrFileName}" == "None" ] ; then 
 ###  StrFileTmp=$( uuidgen -t ) ; 
 ### fi
 ### 
 ### Which is making sense. 
 ### 
 ### Also Note f1161962-0ad8-11e3-b166-001b3875b29c introduce explanation on mutation of BoolVarTestVarCreation from True/False test into None and moving uuid-file-id variable inside BVTestBoolAssertion
 ### 
 ### 
 eval $( BVTestVarName=StrFileTmp \
         BVTestVarHold='${StrFilePath}/${StrFileName}' \
         BVTestBoolVarName=\${StrFileName} \
         BVTestBoolCase=None \
         BVTestBoolAssertion='${StrFilePath}/$( uuidgen -t )' \
         BVTestScopeTest=local \
         BoolVarTestVarCreation ) ; 
 
 local StrSwitchMessages="${StrSwitchesShow}${StrStartSwitches}\n${StrGetMsgSwitches}\n${StrListMsgSwitches}\n${StrCompWordMsgSwitches}\n" ;
 

 function __main_Editor()
 {
  local __call_locality=( Editor __main_Editor ) ;
  local Arg0=${ArrayArg[0]} ;
  local ArrayArg=( $* ) ;
  test ! -e ${StrFileTmp} && echo "" > ${StrFileTmp} ; 
  
  local res=1 ; 
  local shell_res=0 ; 
  local shell_quit=0 ; 
  eval $( BVTestVarName=StrEditableAttr \
          BVTestVarHold='--editable' \
          BVTestBoolVarName=\${IsEditField} \
          BVTestBoolCase=False \
          BVTestBoolAssertion='' \
          BVTestScopeTest=local \
          BoolVarTestVarCreation ) ; 
  
  
  while [ ${res} -eq 1 -a ${shell_quit} -eq 0 ] ; do 
   CmdEval=$( zenity \
              --text-info ${StrEditableAttr} \
              --font=${IntFontSize} \
              --filename=${StrFileTmp} \
              --title="${StrTitle}" \
              --width=${IntWidth} \
              --height=${IntHeight} ) ; 
   res=$? ; 
   if [ ${res} -ne 1 ] ; then 
    ### 
    ### FootPrint Section
    ###
    ###
      function _NoFootPrint()
      {
        echo -ne "###\n### No FootPrint Added, see Prefixed-Var ZSEAddFootPrint from ZenityShellEval\n###\n###\n###\n###\n###\n###\n###\n###\n###\n" ; 
      }
      function _FootPrint()
      {
        local StrUUID=$( uuidgen -t ) ; 
        local StrSha1Sum=$( echo "${CmdEval}" | sha1sum | cut -d ' ' -f 1)
        local StrSize=$( echo "${CmdEval}" | wc -c ) ; 
        local StrNbWord=$( echo "${CmdEval}" | wc -w ) ; 
        local StrDateConfirm=$( GODFormat='${StrDateFormat}' GetOtherDate )
        echo -ne "###\n### FootPrint Added, see Prefixed-Var ZSEAddFootPrint from ZenityShellEval\n###\n\n###File:${StrFileTmp}\n###UUID-TIME-MARKER:${StrUUID}\n###Date: ${StrDateConfirm}\n###Sha1Sum: ${StrSha1Sum}\n### Size:${StrSize}\n### NbWord: ${StrNbWord}\n\n" ; 
      }
      function _DetectFootPrint()
      {
       local IntFootPrintDetection=$( echo -ne "${CmdEval}" | head -n 11 | egrep -ic "FootPrint" ) ;
       eval $( BVTestVarName=StrFootPrintMark BVTestVarHold='$( StrDateFormat=${StrDateFormat} CmdEval=${CmdEval} _FootPrint )' BVTestBoolVarName=\${IsAddFootPrint} BVTestBoolCase=False BVTestBoolAssertion='$( _NoFootPrint )' BVTestScopeTest=local BoolVarTestVarCreation ) ;
      }
      
      eval $( BVTestVarName=StrFootPrintMark BVTestVarHold='$( StrDateFormat=${StrDateFormat} CmdEval=${CmdEval} _FootPrint )' BVTestBoolVarName=\${IsAddFootPrint} BVTestBoolCase=False BVTestBoolAssertion='$( _NoFootPrint )' BVTestScopeTest=local BoolVarTestVarCreation ) ;       
      
    ###
    ### End FootPrint
    ###
    
    
    echo """${StrFootPrintMark}\n${CmdEval}""" > ${StrFileTmp} ; 
    chmod 775 ${StrFileTmp} ; 
    . ${StrFileTmp} ; 
    shell_res=$?
    if [ ${shell_res} -eq 1 ] ; then 
     echo -ne "\n\n\tUser Shell evaluation reported error\n\n" > /dev/stderr ; 
     res=1 ; 
     shell_res=1 ; 
    fi 
   else 
    echo -ne "\n\n\tUser cancel the test.\n\n" > /dev/stderr ; 
    shell_quit=1 ; 
   fi ; 
   sleep ${IntSleep} ; 
   test ${res} -eq 0 -a ${shell_res} -eq 0 && eval $( BVTestVarName=res BVTestVarHold='0' BVTestBoolVarName=\${IsLoopOnSucc} BVTestBoolCase=False BVTestBoolAssertion='1' BVTestScopeTest=local BoolVarTestVarCreation ) ; 
  done
  echo -ne "\n\tQuitting Function :${__call_locality[1]}\n\n" > /dev/stderr ;  
 }
 function __main_CheckSum()
 {
		local __call_locality=( CheckSum __main_CheckSum ) ;
		local Arg0=${ArrayArg[0]} ;
		local ArrayArg=( $* ) ;
  local CheckSumFile=$( cat ${StrFilePath}/${StrFileName} | grep -v "^###" | sha1sum | cut -d ' ' -f 1  ) ; 
  local CheckSumIdentity=$( cat ${StrFilePath}/${StrFileName} | grep "^###Sha1Sum:" | cut -d ' ' -f 2  | sed 's/[\ \t]//g' ) ;
  echo -ne "File: ${CheckSumFile}\nFootprint: ${CheckSumIdentity}\n" > /dev/stderr ; 
  if [ ${CheckSumFile} == ${CheckSumIdentity} ] ; then 
   echo -ne "file-shasum:${StrFilePath}/${StrFileName}:MATCH\n" ; 
  else
   echo -ne "file-shasum:${StrFilePath}/${StrFileName}:FAILED\n" ; 
  fi 
 }

 function __main_StartServices()
 {
		local __call_locality=( Main __main_StartServices ) ;
		local Arg0=${ArrayArg[0]} ;
		local ArrayArg=( $* ) ; 
  if [ "${IsCheckSumOnly}" == "True" ] ; then 
   StrFilePath=${StrFilePath} StrFileName=${StrFileName} __main_CheckSum ; 
  else
  eval $( VTVValueEntry=StrFileTmp,StrTitle,StrDateFormat,IntSleep,IntFontSize,IsEditField,IntWidth,IntHeight,IntDefaultModeExec,IsEditField,IsAddFootPrint,IsLoopOnSucc,IsCheckSumOnly\
          VTVIsValueReAssign=True \
          VTVIsValueToConvert=False \
          VTVIsArrayStyleInsert=True \
          ValueToVariable ) __main_Editor 
  fi


 }
 
 if [ "${Arg0:=--startservices}" == "--help"	] ; then 
			GetVarReference ${__call_locality[1]} ; 
			echo -ne "${StrSwitchMessages}" > /dev/stderr ; 
	elif [ "${Arg0:=--startservices}" == "--get" ] ; then 
		eval """local ArgGet=\${${ArrayArg[1]}}""" ; 
		echo -ne """${ArgGet}\n""" ;
	elif [ "${Arg0:=--startservices}" == "--list" ] ; then 
		eval $( __GetVarReferenceList ) ;
 elif [ "${Arg0:=--startservices}" == "--compword" ] ; then 
		eval $( __GetVarReferenceCompWord ) ;
 elif [ "${Arg0:=--startservices}" == "--startservices" ] ; then 
  eval $( VTVIsArrayStyleInsert=True \
  VTVValueEntry=StrFileTmp,StrTitle,StrDateFormat,IntSleep,IntFontSize,IsEditField,IntWidth,IntHeight,IntDefaultModeExec,IsAddFootPrint,IsLoopOnSucc,IsCheckSumOnly \
  VTVIsValueReAssign=True \
  VTVIsValueToConvert=False \
  VTVIsArrayStyleInsert=True \
  ValueToVariable ) __main_StartServices
 fi


}
