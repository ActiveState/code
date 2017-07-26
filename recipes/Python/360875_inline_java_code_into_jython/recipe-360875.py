import jythonc, sys
def java(code, force=0):
	"""compile code snippet and return imported class"""
	codelines=code.split(";")
	for line in codelines:
		if line.find("class")!= -1:
			classname=line[line.find("class"):].split()[1]
			break
	try:
		oldcode=open(classname+".java").readlines()
	except:
		oldcode=""
	print >> open(classname+".java","w") ,code
	code=open(classname+".java").readlines()
	if(oldcode!=code or force!=0):
		retcode,retout,reterr=jythonc.javac.compile([classname+".java",])
		if retcode!=0:
			raise RuntimeError, reterr
	return sys.builtins["__import__"](classname)
		

if __name__=="__main__":
	java("""
	// this is the embedded java code
	public class inlined_java {
		public static void main() {
			System.out.println("Hello World from jython!!!");
		}
	}
	""",force=1).main()
