####################################################################
# List Servers 
###################################################################

set cells [$AdminConfig list Cell ] 

foreach cell $cells {

   set nodes [$AdminConfig list Node $cell ]

   foreach node $nodes {
      set cname [$AdminConfig showAttribute $cell name ]
      set nname [$AdminConfig showAttribute $node name ]
      set servs [$AdminControl queryNames type=Server,cell=$cname,node=$nname,*]

      puts "\nNumber of running servers on node $nname:[llength $servs ]\n"

      foreach server $servs {
         set sname [$AdminControl getAttribute $server name ]
         set ptype [$AdminControl getAttribute $server processType ]
         set pid   [$AdminControl getAttribute $server pid ]
         set state [$AdminControl getAttribute $server state ]
         set jvm   [$AdminControl queryNames type=JVM,cell=$cname,node=$nname,process=$sname,*]
         set osname [$AdminControl invoke $jvm getProperty os.name ]

         puts "\n   $sname ($ptype)has pid $pid; state:$state;on $osname\n"

         set apps  [$AdminControl queryNames type=Application,cell=$cname,node=$nname,process=$sname,*]

         puts "\n     Number of applications running on $sname:[llength $apps ]\n"

         foreach app $apps { set aname [$AdminControl getAttribute $app name ]
			     puts "     $aname"
         }
         puts "\n     -------\n"
      }
   }
}
