#constants
AppDomain = System::AppDomain
Console   = System::Console
#caption of table
Console.WriteLine('{0, 5} {1}', 'GAC', 'AssemblyName')
Console.WriteLine('{0, 5} {1}', '---', '------------')
#print table of loaded assemblies
AppDomain.CurrentDomain.GetAssemblies().each do |i|
  Console.WriteLine('{0, 5} {1}', i.GlobalAssemblyCache, i.GetName().Name)
end
