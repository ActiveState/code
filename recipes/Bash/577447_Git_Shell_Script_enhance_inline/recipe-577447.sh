function __GitBranch( )
{
 eval $( __call_localityLocalName=BrOpt __call_locality ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Action FParamVarName=StrActionBranch FParamDefaultValue=change     __fnctCreateLocalityFuncParam ); 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Name FParamVarName=StrBranchName FParamDefaultValue=master     __fnctCreateLocalityFuncParam ); 

  function CaseBranchingGit()
  {
    function __GitCheckOut()
    {
      local CmdEval=( git checkout -f ${StrBranchName} ); 
      echo -ne "CmdLine:[ ${CmdEval[@]} ]\n" ;
      eval "${CmdEval[@]}";
    }
    function __GitCreateBranch()
    {
      local CmdEval=( git branch -l ${StrBranchName} --color );
      echo -ne "CmdLine:[ ${CmdEval[@]} ]\n" ;
      ###
      ### The '''eval "${CmdEval[@]}" ;''' Tend to be a good __finalize, or __closure...
      eval "${CmdEval[@]}" ;
    }
    eval $( __call_localityLocalName=CBGit __call_locality ) ;
    function __BinaryCase()
    {
      case "${StrActionBranch}" in 
        "change" )
        __GitCheckOut
        ;;
        "create" )
        __GitCreateBranch
        ;;
      esac
    }
    __BinaryCase ;
  }
  CaseBranchingGit;
}

function GitBranchList()
{
  eval $( __call_localityLocalName=GBL __call_locality ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName    FParamVarName=StrArrayName    FParamDefaultValue=ArrayGitBranch     __fnctCreateLocalityFuncParam );
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=VariableMode FParamVarName=StrVariableMode FParamDefaultValue=local              __fnctCreateLocalityFuncParam );
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Action       FParamVarName=StrAction       FParamDefaultValue=ArrayCreation      __fnctCreateLocalityFuncParam );
 
  GitBranchList.Property.N() 
  {
   eval $( __call_localityLocalName=${StrFuncName}.Property.N __call_localityDisplayFunctionEntry=1 __call_locality );
   #local IntID=(${StrFuncName/./ });
   #IntID=${IntID[${#IntID[@]}]};
   local IntArrayArg=${#ArrayArg[@]} ;
   local ArrayFuncProperty=( ${StrFuncName/Property/Getter} ${StrFuncName/Property/Setter} ) ;
   if [ ${IntArrayArg:=0} -gt 0 ] ; then 
    eval "${ArrayFuncProperty[1]/\.N/\.${IntPos}} ${ArrayArg[@]}" ;
   else
    eval "${ArrayFuncProperty[0]/\.N/\.${IntPos}} ${ArrayArg[@]}" ;
   fi 
  }
  
  GitBranchList.Getter.N() 
  { 
      eval $( __call_localityLocalName=${StrFuncName}.Getter.N __call_localityDisplayFunctionEntry=1 __call_locality );
      local IntID=(${StrFuncName/./ });
      IntID=${IntID[${#IntID[@]}]};
      echo "${__META__[${IntID}]}"
  }
  
  GitBranchList.Setter.N() 
  { 
      eval $( __call_localityLocalName=${StrFuncName}.Setter.N __call_localityDisplayFunctionEntry=1 __call_locality );
      local IntID=(${StrFuncName/./ });
      IntID=${IntID[${#IntID[@]}]};
      echo "__META__[${IntID}]=${ArrayArg[@]}" ;
  }
  
  function ActionArrayProperty()
  {
    eval $( __call_localityLocalName=Property __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    echo -ne "\nFunc: ${StrFuncName}, NameArrayID : ${ArrayArg[0]}\n" ;
    eval """$( declare -f GitBranchList.Property.N | sed 's/__META__/${ArrayName}/g;s/\.N/\.${IntPos}/g;s/\.${StrFuncName}//g')""" ;
  }
  
  function ActionArrayGetter()
  {
    eval $( __call_localityLocalName=Getter __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    eval """$( declare -f GitBranchList.Getter.N | sed 's/__META__/${ArrayName}/g;s/\.N/\.${IntPos}/g;s/\.${StrFuncName}//g')""" ;
  }

  function ActionArraySetter()
  {
    eval $( __call_localityLocalName=Setter __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    eval """$( declare -f GitBranchList.Setter.N | sed 's/__META__/${ArrayName}/g;s/\.N/\.${IntPos}/g;s/\.${StrFuncName}//g')""" ;
  }
  
  function VarDeclHandler()
  {
    eval $( __call_localityLocalName=VDecl __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    eval $( FParamFuncName=${StrFuncName} FParamSuffixName=CreateVar    FParamVarName=StrCreateVar    FParamDefaultValue=StrDeclVar     __fnctCreateLocalityFuncParam );
    function __Case0()
    {
      echo -ne "${StrCreateVar}=\"local \";\n" ;
    }
    function __Case1()
    {
      echo -ne "${StrCreateVar}=\"declare -a \";\n" ;
    }
      
    function __BinaryCase()
    {
      echo -ne "Creating Array : ${StrArrayName }\n" > /dev/stderr ; 
      case "${StrVariableMode}" in 
        "local" )
        __Case0
        ;;
        "global" )
        __Case1 
        ;;
      esac
    }
    __BinaryCase ;
  }

  function AwkFilter()
  {
    eval $( __call_localityLocalName=AwkFilter __call_locality ) ;
    awk -f ${ArrayAwkScriptPath[0]}/GitBranchList.awk
  }

  function GitCmd()
  {
    eval $( __call_localityLocalName=GCmd __call_locality ) ;
    eval $( FParamFuncName=${StrFuncName} FParamSuffixName=GitCommand0 FParamVarName=ArrayGitCommand[0] FParamDefaultValue=branch   __fnctCreateLocalityFuncParam );
    eval $( FParamFuncName=${StrFuncName} FParamSuffixName=GitCommand1 FParamVarName=ArrayGitCommand[1] FParamDefaultValue=-l       __fnctCreateLocalityFuncParam );
    eval "git ${ArrayGitCommand[@]}" ; 
  }
    
  function ActionArrayCreation()
  {
    eval $( __call_localityLocalName=ActionArrayCreation __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    GitBranch=$( ( GitCmd | AwkFilter ) );
    StrDeclVar="";
    eval $( VDeclCreateVar=StrDeclVar VarDeclHandler ) ;
    echo -ne "${StrDeclVar}${StrArrayName}=( ${GitBranch} )" ;
  }
  
  function ActionArrayPropertyLoader()
  {
    eval $( __call_localityLocalName=ActionArrayPropertyLoader __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    ActionArrayProperty ${ArrayArg[0]} ;
    ActionArrayGetter ${ArrayArg[0]} ;
    ActionArraySetter ${ArrayArg[0]} ;
  }
  
  case ${StrAction} in
   "ArrayCreation" )
   ActionArrayCreation ;
   ;;
   "Property" )
   eval $( __in_for ${StrArrayName} ActionArrayPropertyLoader ) ;
   ;;
  esac 
}

function git_add_reflection()
{
  eval $( __call_localityLocalName=GitMeth __call_localityDisplayFunctionEntry=1 __call_locality ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Dcommand FParamVarName=StrDcommand FParamDefaultValue=AddRepository __fnctCreateLocalityFuncParam     ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=CommitMessage FParamVarName=StrCommitMessage FParamDefaultValue=StrMsgGitCommit FParamInterpretVar=True __fnctCreateLocalityFuncParam     ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=GitRepository FParamVarName=StrGitRepository FParamDefaultValue=Montreal-Olympic-Statium-kml-python.git  __fnctCreateLocalityFuncParam     ) ;
  local CmdEval=() ;
  
  function RemoveDbVarLog()
  {
   if [ -e db_parse_newvar ] ; then 
    rm -f db_parse_newvar ;
   fi
  }
  
  function DisplayEvalCmd()
  {
    eval $( __call_localityLocalName=DisplayEvalCmd __call_localityDisplayFunctionEntry=1 __call_locality ) ;
    echo -ne "\n\t\tCommand Eval:[ ${CmdEval[${intCmdEval}]} ]\n" ;
    RemoveDbVarLog ;
    eval "${CmdEval[${intCmdEval}]}" ;
  }
  
  function SingleAdd()
  {
   eval $( __call_localityLocalName=SingleAdd __call_localityDisplayFunctionEntry=0 __call_locality ) ;
   CmdEval[0]="git add ${ArrayArg[0]} "  ;
   eval $( __in_for CmdEval DisplayEvalCmd  );
  }
  
  function SinglePushOrigin()
  {
   eval $( __call_localityLocalName=SingleAdd __call_localityDisplayFunctionEntry=0 __call_locality ) ;
   
   eval """CmdEval[0]=\"git push origin master \" """  ;
   eval $( __in_for CmdEval DisplayEvalCmd  );
  }

  function SingleAddOrigin()
  {
   eval $( __call_localityLocalName=SingleAdd __call_localityDisplayFunctionEntry=0 __call_locality ) ;
   
   eval """CmdEval[0]=\"git remote add origin git@github.com:priendeau/${StrGitRepository} \" """  ;
   eval $( __in_for CmdEval DisplayEvalCmd  );
  }
  
  function SingleCommit()
  {
   eval $( __call_localityLocalName=SingleAdd __call_localityDisplayFunctionEntry=0 __call_locality ) ;
   eval """CmdEval[0]=\"git commit -m '\${${StrCommitMessage}}' \" """  ;
   eval $( __in_for CmdEval DisplayEvalCmd  );
  }
  
  function AddRepository()
  {
   eval $( __call_localityLocalName=AddRepository __call_localityDisplayFunctionEntry=0 __call_locality ) ;
   CmdEval[0]="git add ${ArrayArg[0]} "  ;
   eval """CmdEval[1]=\"git commit -m '\${${StrCommitMessage}}' \" """  ;
   CmdEval[2]="git remote add origin git@github.com:priendeau/${ArrayArg[0]}"  ;
   CmdEval[3]="git push origin master" ;
   
   eval $( __in_for CmdEval DisplayEvalCmd  );
  
  }
  echo -ne "Command Git :[ ${StrDcommand} ]\n" ;
  eval ${StrDcommand} ${ArrayArg[@]} ;
}

function GitAddFile()    
{  
 eval $( __call_localityLocalName=GitAdd __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=FileName FParamVarName=StrFileName FParamDefaultValue=None __fnctCreateLocalityFuncParam     ) ;
 
 function SubEval()
 {
   eval $( __call_localityLocalName=GitSE __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
   if [ "${StrFileName}" == "None" ] ; then 
    echo "No file-name to add to Git Repository: File=${StrFileName}\n" ;
   else
    local CmdEval=( git add ${StrFileName} );
    echo -ne "CmdLine:[ ${CmdEval[@]} ]\n" > /dev/stderr ;
    eval "${CmdEval[@]}" ;
   fi
 }
 StrFileName=${ArrayArg[0]} SubEval ;
} ; 

function start_git_add_file()
{
 eval $( __call_localityLocalName=SGaf __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
 eval $( GBLVariableMode=local GitBranchList )
 eval $( GitCreateLocalQueue ) ;
 eval $( __in_for ArrayGitQueue GitAddFile ) ;
 git commit -m "updated:UUID:$( uuidgen -r )" -a ; 
}


function GitCommitMsg()    
{  
 eval $( __call_localityLocalName=Add __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=TagMsg FParamVarName=StrTagMsg FParamDefaultValue=pocdedu __fnctCreateLocalityFuncParam     ) ;
 local StrMsg="v.$( uuidgen -r )${StrTagMsg}/${RANDOM}" ; 
 echo -ne "\nCommit Section Name:[ ${StrMsg} ]\n" ; 
 git commit -m "${StrMsg}" ;

}


function CleanDbParseNewVar()
{
  eval $( __call_localityLocalName=CLDPNV __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
  echo -ne """if [ -e db_parse_newvar ] ; then rm -f db_parse_newvar ; fi ; """ ;
}

function GitCreateLocalQueue()
{
 eval $( __call_localityLocalName=GCLQ __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName FParamVarName=StrArrayName FParamDefaultValue=ArrayGitQueue __fnctCreateLocalityFuncParam     ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DefaultPath FParamVarName=StrDefaultPath FParamDefaultValue=./ __fnctCreateLocalityFuncParam     ) ;
 
 function EgrepFilter()
 {
   eval $( __call_localityLocalName=EgrepFilter __call_localityDisplayFunctionEntry=0 __call_locality  ) ; 
   egrep -iv ".passogva|.commit-msg|git-password|README.encode|.git|.decode|.encode|.gitfs|.avfs-git|.avfs_git|.passwd|.password|.htpasswd|.htconf|db_parse_newvar" ;
   
 }
 
 function TrailRemove()
 {
  eval $( __call_localityLocalName=EgrepFilter __call_localityDisplayFunctionEntry=0 __call_locality  ) ; 
  tr '[:cntrl:]' ' ' ;
 }
 
 function LocalFind()
 {
   eval $( __call_localityLocalName=LocalFind __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
   find ${StrDefaultPath} -type f | sed 's/\.\///g'| EgrepFilter  | TrailRemove ;
 }
 eval $( CleanDbParseNewVar );
 local CmdEval=( "declare -a ${StrArrayName}=( $( LocalFind ) )" ) ; 
 echo -ne "CmdLine : CmdEval length: ${#CmdEval} bytes\n" > /dev/stderr ;
 eval "echo \"${CmdEval[@]}\"" ;
 echo -ne "Array with Git Local File are stored inside Array:[ ${StrArrayName} ]\n" > /dev/stderr ;
}

function GitCmdFileArray()    
{  
 eval $( __call_localityLocalName=Git __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName FParamVarName=StrArrayName FParamDefaultValue=ArrayArg __fnctCreateLocalityFuncParam     ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Cmd FParamVarName=StrCmd FParamDefaultValue=add __fnctCreateLocalityFuncParam     ) ;
 eval "eval $( __in_for ${StrArrayName} \"${StrCmd}\" )" ;

}

function GitAddFileArray()    
{  
 eval $( __call_localityLocalName=GitAddFileArray __call_localityDisplayFunctionEntry=1 __call_locality  ) ; 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName FParamVarName=StrArrayName FParamDefaultValue=ArrayArg __fnctCreateLocalityFuncParam     ) ;
 eval $( CleanDbParseNewVar );
 eval "eval $( __in_for ${StrArrayName} GitAddFile )" ;
 
}

#declare -a ArrayFileRm=( WebServiceStudio.pidb WebServiceStudio.mdp WebServiceStudio.mds WebServiceStudio.mdp WebServiceStudio.userprefs ComponentSysWinFormTranslation.cs WebServiceStudio.exe.encode WebServiceStudio.exe.mdb.encode ) ; 

function find_git_rm()    
{ 
  eval $( __call_localityLocalName=FGRM __call_locality ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName FParamVarName=StrArrayName FParamDefaultValue=ArrayFileRm __fnctCreateLocalityFuncParam     ) ;
  eval "find ./ -type f -iname \"\${${StrArrayName}[\${int${StrArrayName}}]}\" -exec git rm {} \; ;" 
} 

function start_find_rm()
{
  eval $( __call_localityLocalName=SFR __call_locality ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=ArrayName FParamVarName=StrArrayName FParamDefaultValue=ArrayFileRm __fnctCreateLocalityFuncParam     ) ;
  FGRMArrayName=${StrArrayName} eval $( __in_for ArrayFileRm find_git_rm ) ;
}

function GetPassogva( )
{
  eval $( __call_localityLocalName=GetPassogva __call_locality ); 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=MinLen FParamVarName=IntMinLen FParamDefaultValue=10 __fnctCreateLocalityFuncParam     ) ;
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=MaxLen FParamVarName=IntMaxLen FParamDefaultValue=20 __fnctCreateLocalityFuncParam     ) ;
  /etc/init.d/fnct.d/GetPassogva.py
  
}

function encode_git_add()
{ 
 eval $( __call_localityLocalName=gitadd __call_locality ); 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=PasswdFile FParamVarName=StrPasswdFile FParamDefaultValue=/home/ubuntu/git/priendeau/.passwd __fnctCreateLocalityFuncParam     ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=DefaultGitHeadFile FParamVarName=StrDefaultGitHeadFile FParamDefaultValue=.git/logs/HEAD __fnctCreateLocalityFuncParam     ) ;
 
 local FileNameGit="${ArrayGitQueue[${intArrayGitQueue}]}" ; 
 local StrRealFileName=${FileNameGit} ;
 local PASSOGVA
 GetPassogva ;
 local UUID=$( uuidgen -r );
 local ShaValue=( $( sha1sum --binary ${StrRealFileName} ) );
 local NewMsg=${StrMsgCommit/__FILENAME__/${StrRealFileName}}; 
 NewMsg=${NewMsg/__SHA__/${ShaValue[0]}}; 
 NewMsg=${NewMsg/__UUID__/${UUID}} ;
 NewMsg=${NewMsg/__PASSOGVA__/${PASSOGVA}} ;
 local IsEncoded=False ;
 
 
 if [ -e ${StrPasswdFile} ] ; then
  IsEncoded=True ;
  local CmdEval=( openssl enc -e -base64 -cast5-cbc -kfile ${StrPasswdFile} -in ${StrRealFileName} -out ${FileNameGit}.encode ) ;
  echo -ne "CmdEval: ${CmdEval[@]}\n" ;
  eval "${CmdEval[@]}" ;
  FileNameGit="${FileNameGit}.encode" ;
  NewMsg=${NewMsg/__ENCODING__/BASE64:CAST5-CBC} ;
  if [ -e ${StrRealFileName} ]; then 
   if [ -e ${FileNameGit} ] ; then 
    git rm ${StrRealFileName} ; 
   fi
  fi

 else
  IsEncoded=False ;
  NewMsg=${NewMsg/__ENCODING__/NONE} ;
 fi 

 local IntAddFound=$( egrep -ic --no-filename "${FileNameGit}" ${StrDefaultGitHeadFile} ) ;
 if [ ${IntAddFound:=0} -eq 0 ] ; then 
  
  if [ "${IsEncoded:=False}" == "True" ] ; then 
    local IsEncodedProduct=$( echo "${FileNameGit}" | egrep -ic --no-filename "\.encode"  ) ;
    if [ ${IsEncodedProduct:=0} -gt 0 ] ; then 
     git add "${FileNameGit}" ; 
    fi
  else
   git add "${StrRealFileName}" ; 
  fi 
  
 fi
 git commit -m "${NewMsg}" ${FileNameGit} ; 

} ; 

function encode_start_git_add()
{
 local StrMsgCommit="__MSG__:__FILENAME__: SHA:__SHA__, UUID:__UUID__ ENCODING:__ENCODING__" ;
 if [ -e .passogva ]; then 
  rm -f .passogva 
 fi
 eval $( GitCreateLocalQueue ) ;
 eval $( __in_for ArrayGitQueue encode_git_add ) ;
 git remote add origin git@github.com:priendeau/MonoWebServicesStudio.git
 git push origin master ;
 
}

function GitDailyWorkUpdate()
{
 eval $( __call_localityLocalName=GDWU __call_locality ); 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=AddNewFileHolder FParamVarName=StrAddNewFileHolder FParamDefaultValue=.file-add __fnctCreateLocalityFuncParam     ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=BranchName FParamVarName=StrBranchName FParamDefaultValue=master __fnctCreateLocalityFuncParam     ) ;
 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=MimeTypeCleanUp FParamVarName=StrMimeTypeCleanUp FParamDefaultValue=pyc __fnctCreateLocalityFuncParam     ) ;
 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=Interpreter FParamVarName=StrInterpreter FParamDefaultValue=python __fnctCreateLocalityFuncParam     ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=VersionName FParamVarName=StrVersionName FParamDefaultValue=2.6 __fnctCreateLocalityFuncParam     ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=SetupInstallName FParamVarName=StrSetupInstallName FParamDefaultValue=setup.py __fnctCreateLocalityFuncParam     ) ;
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=SetupInstallOption FParamVarName=StrSetupInstallOption FParamDefaultValue=clean,build,bdist,bdist_dumb,sdist,upload __fnctCreateLocalityFuncParam     ) ;

 function ShowRegisteredStep()
 {
  eval $( __call_localityLocalName=ShowRS __call_locality ); 
  echo -ne "\n\tAdding ${ArrayOption[${intArrayOption}]} has step to process.\n" ; 
 }
 
 local ArrayOption=( ${StrSetupInstallOption//,/ } ) ;
 
 eval $( __in_for ArrayOption ShowRegisteredStep ) ;
 
 function __fnct_git_add()
 {
  eval $( __call_localityLocalName=MGAF __call_locality ); 
  local StrFileName=${ArrayFileAdd[${intArrayFileAdd}]} ;
  local StrUUID=$( uuidgen -r );
  local Sha1Sum=( $( sha1sum -b ${StrFileName} ) );
  Sha1Sum=${Sha1Sum[0]} ;
  git add ${StrFileName} ;
  git commit -m "Adding new file: ${StrFileName}, UUID:${StrUUID}, SHA1SUM: ${Sha1Sum}" ${StrFileName} ;
  
 }
 
 function main_git_add_file()    
 {
   eval $( __call_localityLocalName=MGAF __call_locality ); 
   if [ -e ${StrAddNewFileHolder} ] ; then
    local IntNbLine=( $( wc -l ${StrAddNewFileHolder} ) ) ;
    IntNbLine=${IntNbLine[0]} ;
    if [ ${IntNbLine:=0} -gt 0 ] ; then 
     local ArrayFileAdd=( $( cat ${StrAddNewFileHolder} ) ) ;
     eval $( __in_for ArrayFileAdd __fnct_git_add ) ;
     echo > ${StrAddNewFileHolder} ;
    fi
   else
    echo > ${StrAddNewFileHolder} ;
   fi
 }
 
 function main_git_commit_update()    
 { 
   eval $( __call_localityLocalName=MGCU __call_locality ); 
   
   local UUID=$( uuidgen -r ) ;
   find ./ -type f -iname "*.${StrMimeTypeCleanUp}" -exec rm -f {} \; 
   git commit -m "UUID:${UUID}" -a ; 
   git push origin ${StrBranchName} ; 
 } ; 
 
 function install_pymodule()    
 { 
   eval $( __call_localityLocalName=IPymodule __call_locality ); 
   function install_py()    
   { 
     eval $( __call_localityLocalName=IPy __call_locality ); 
     local CmdEval=( ${StrInterpreter}${StrVersionName} ${StrSetupInstallName} ${ArrayArg[0]} ) ;  
     local strcmd="${ArrayOption[${intArrayOption}]}"; 
     eval "${CmdEval[@]}" ;
     if [ "${strcmd}" == "sdist" ] ; then 
      echo -ne "\n\n\tCreating Source with tag : ${strcmd}\n\n" ; 
     fi ; 
   } ; 
   eval $( __in_for ArrayOption install_py ); 
 } ; 
 
  main_git_commit_update ; 
  install_pymodule 
}

#~ function GitAutoUpdate()
#~ {
 #~ eval $( __call_localityLocalName=GitUpdate __call_locality ); 
 #~ #eval $( FParamFuncName=${StrFuncName} FParamSuffixName= FParamVarName= FParamDefaultValue= __fnctCreateLocalityFuncParam     ) ;
 #~ eval $( FParamFuncName=${StrFuncName} FParamSuffixName=TimeSlicing FParamVarName=IntTimeSlicing FParamDefaultValue=60 __fnctCreateLocalityFuncParam     ) ;
 #~ 
 #~ local IntFactorSlice=$(( IntTimeSlicing ))
  #~ 
#~ }

Git_Branch_Handler()  
{ 
 eval $( __call_localityLocalName=GBH __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
 eval $( FParamFuncName=${StrFuncName} FParamSuffixName=BranchName FParamVarName=StrBranchName FParamDefaultValue=master __fnctCreateLocalityFuncParam )  ; 
 
 local intSleep=0;
 local TestSleep=40 ; 
 local TotalTestTime=$(( ${TestSleep} + 10 )) ;
 local ArrayPushBranch=( git push origin ${StrBranchName} ) ;
 local ArrayDateFormatReport=( "date" "+\"%c, UnixTimeStamp:%s\"" ) ;
 
 function BranchLocking()
 {
  eval $( __call_localityLocalName=BL __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  BrOptAction=change BrOptName=${StrBranchName} __GitBranch   ; 
 }
 
 function RandomInstance()
 {
   eval $( __call_localityLocalName=RI __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
   intSleep=$(( ${RANDOM} % 90 )) ;
   DecalSleep=$(( ${RANDOM} % 20 )) ;
 }
 
 function SetRandomTime()
 {
  eval $( __call_localityLocalName=GBHSRT __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  while [ ${intSleep} -lt ${TotalTestTime} ] ; do 
   RandomInstance ;
   TotalTestTime=$(( ${TestSleep} + ${DecalSleep:=10} )) ; 
  done ; 
 }
 
 function DisplayInfo()
 {
   eval $( __call_localityLocalName=DisplayInfo __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
   echo -ne "\n\tSleeping for ${intSleep} seconds.\n\tTest was done with TimeTrigger=${TotalTestTime} ,Average +-${DecalSleep}\n" ; 
 }

 function ContentLoop()
 {
  eval $( __call_localityLocalName=CL __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
 }
 
 function TimerSleep()
 {
  eval $( __call_localityLocalName=TS __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  sleep ${intSleep} ; 
 }
 
 function DateReport()
 {
  eval $( __call_localityLocalName=DateR __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  eval "${ArrayDateFormatReport[@]}" ;
 }
 
 function __fnct_uuidgen()
 {
   eval $( __call_localityLocalName=__fnct_UUID __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
   StrUUID=$( uuidgen -r ) ;
 } 
 
 function UUIDGenerator()
 {
  eval $( __call_localityLocalName=UUID __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  local StrUUID=None ;

  git commit -m "updated:UUID( ${StrUUID} )" -a ; 
 }
 
 function git_push()
 {
  eval $( __call_localityLocalName=GitP __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  eval "${ArrayPushBranch[@]}" ; 
 } 
 
 function __fnct_while_ArrayProc()
 {
  echo """local ArrayFuncLoop=( ${ListFuncProcList//,/ } ); while [ 1 ] ; do eval \$( __in_for ArrayFuncLoop eval ) ; done""" ;
 }
 
 function __fnct_ArrayProc()
 {
  echo """local ArrayFuncLoop=( ${ListFuncProcList//,/ } ); eval \$( __in_for ArrayFuncLoop eval )""" ;
 } 
 
 function ContentLoop()
 {
  eval $( __call_localityLocalName=GBHCL __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=FuncProcList FParamVarName=ListFuncProcList FParamDefaultValue=SetRandomTime,DisplayInfo,TimerSleep,DateReport,UUIDGenerator,git_push FParamTypeVar=Array __fnctCreateLocalityFuncParam )  ; 
  
  eval $( __fnct_while_ArrayProc ) ; 
  #local ArrayFuncLoop=( ${ListFuncProcList//,/ } );
  
  #while [ 1 ] ; do 
  # eval $( __in_for ArrayFuncLoop eval )
  #done
  
 }
 
 function MainLoop()
 {
  eval $( __call_localityLocalName=MainWhileLoop __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=FuncLoop FParamVarName=ListFuncProcList FParamDefaultValue=ContentLoop __fnctCreateLocalityFuncParam )  ; 

  eval $( __fnct_while_ArrayProc ) ;  
  #local ArrayFuncLoop=( ${ListFuncProcList//,/ } );
  
  #while [ 1 ] ; do 
  # eval $( __in_for ArrayFuncLoop eval ) ; 
  #done
 }
 
 function LoopInit()
 {
  eval $( __call_localityLocalName=LoopInit __call_localityDisplayFunctionEntry=1 __call_locality ) ; 
  eval $( FParamFuncName=${StrFuncName} FParamSuffixName=LoopInit FParamVarName=ListFuncProcList FParamDefaultValue=BranchLocking,MainLoop __fnctCreateLocalityFuncParam )  ; 

  eval $( __fnct_ArrayProc ) ;
  #local ArrayFuncLoop=( ${ListFuncLoop//,/ } );
  #eval $( __in_for ArrayFuncLoop eval ) ; 
 }
 LoopInit ;
 

}
