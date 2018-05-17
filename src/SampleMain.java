import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

import edu.mit.jverbnet.data.FrameType;
import edu.mit.jverbnet.data.IFrame;
import edu.mit.jverbnet.data.IMember;
import edu.mit.jverbnet.data.IVerbClass;
import edu.mit.jverbnet.data.semantics.ISemanticDesc;
import edu.mit.jverbnet.index.IVerbIndex;
import edu.mit.jverbnet.index.VerbIndex;


import org.python.core.PyInstance;
import org.python.util.PythonInterpreter;


public class SampleMain {

	private static VerbData v_Data;
	   PythonInterpreter interpreter = null;
	   
	   
   public SampleMain()
   {
      PythonInterpreter.initialize(System.getProperties(),
                                   System.getProperties(), new String[0]);
 
      this.interpreter = new PythonInterpreter();
   }
 
   void execfile( final String fileName )
   {
      this.interpreter.execfile(fileName);
   }
 
   PyInstance createClass( final String className, final String opts )
   {
      return (PyInstance) this.interpreter.eval(className + "(" + opts + ")");
   }
   
	public static void main(String[] args) throws Exception {
	//public void test_function() throws Exception {
		// TODO Auto-generated method stub
		System.out.println("Test JVerbnet");
		v_Data = new VerbData(".\\3rd_party\\verbnet\\");
		
		
		SampleMain ie = new SampleMain();
		 
	    ie.execfile("hello.py");
	 
	    PyInstance hello = ie.createClass("Hello", "None");
	 
	    //hello.invoke("run");		
		
		
		
		String targetVerb = "";

		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		String line = "";

		System.out.println("input new verb: ");
		// call python here
		call_python(hello);
		while (line.equalsIgnoreCase("quit") == false) {
			line = in.readLine();

		    //do something
			//System.out.println(line);
			targetVerb = line;

			System.out.println("\n\n");
			System.out.println("==================================================");
			System.out.println(targetVerb);
			System.out.println("==================================================");
			
			v_Data.printVerbIndexList(targetVerb);
			System.out.println("---------------------------------------");
			v_Data.printSemanticPredicateList(targetVerb);
			System.out.println("---------------------------------------");
			v_Data.printIndexAndMembers(targetVerb);
			System.out.println("\n\n");
			
			//call python here
			call_python(hello);
			
			System.out.println("input new verb: ");
		}

		in.close();		
		
	}
	public static void call_python(PyInstance py_obj) {
		py_obj.invoke("run");
	}
}
