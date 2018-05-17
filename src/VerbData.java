import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import edu.mit.jverbnet.data.IFrame;
import edu.mit.jverbnet.data.IMember;
import edu.mit.jverbnet.data.IVerbClass;
import edu.mit.jverbnet.data.semantics.IPredicateDesc;
import edu.mit.jverbnet.data.semantics.ISemanticDesc;
import edu.mit.jverbnet.index.IVerbIndex;
import edu.mit.jverbnet.index.VerbIndex;

public class VerbData {
	
	// verb index, members(verbs)
	private Map<String, List<IMember>> indexMemberMap;
	
	// verbs, related verb index (verb class)
	//map<member(verb), verb classes with specific index>
	private Map<String, List<IVerbClass>> memberIndexMap;
	
	/*
	 *  input a verb to get its semantic list, ISemanticDesc = List<String>;
	 */
	public VerbData(String VerbNetPath) throws IOException{
		/*
		 * initial verb index and setting of verbnet folder
		 */
		indexMemberMap = new TreeMap<String, List<IMember>>();
		memberIndexMap = new TreeMap<String, List<IVerbClass>>();
		
		
		URL url = new URL("file", null, VerbNetPath);	
		// construct the index and open it
		IVerbIndex index = new VerbIndex(url);
		index.open();
		
		// get all verb index which are used to represent verbs
		Iterator<IVerbClass> allIndex = index.iterator();

	    //get a index List
		//List<String>
		while(allIndex.hasNext()) {
			IVerbClass currentVerbIndex = allIndex.next();
	        //System.out.println(element.getID());
	         
	        //index: IVerbClass.getID()
	        //member List: IVerbClass.getMembers()
	        //member name: IMember.getName()

			//for each verb index we need their members
			List<IMember> memberList = new ArrayList<IMember>();
	        memberList = currentVerbIndex.getMembers();
	         
	        //store members in map <key: verb index, value: member list>
	        indexMemberMap.put(currentVerbIndex.getID(), memberList);
	        
	        /*
	         * add each member as a verb
	         */
	        for(int i = 0; i < memberList.size(); i++){
	        	/*
	        	 * check whether this verb exist in verb map
	        	 * if not add it to map
	        	 * if exist update related verb index list
	        	 */
	        	String memberName = memberList.get(i).getName();
	        	if(memberIndexMap.get(memberName)!=null){
	        		List<IVerbClass> currentRelatedIndexList = memberIndexMap.get(memberName);
	        		currentRelatedIndexList.add(currentVerbIndex);
	        		memberIndexMap.put(memberName, currentRelatedIndexList);
	        		
	        	}
	        	else{
	        		//add this verb to map
	        		List<IVerbClass> verbRelatedIndexList = new ArrayList<IVerbClass>();
	        		verbRelatedIndexList.add(currentVerbIndex);
	        		memberIndexMap.put(memberName, verbRelatedIndexList);
	        		
	        	}
	        }
	    }		
		
	}
	/*
	 * print input verb's related verb_index list
	 */
	public void printVerbIndexList(String TargetVerb){
		List<IVerbClass> indexList = new ArrayList<IVerbClass>();
		indexList = memberIndexMap.get(TargetVerb);
		for(int i = 0; i < indexList.size(); i++){
			//show verb index
			System.out.println(TargetVerb+", verb index "+(i+1)+" : "+indexList.get(i).getID());
		}
	}
	/*
	 * get related semantic tags for a verb
	 */
	public List<IPredicateDesc> getSemantic(String TargetVerb){
		
		List<IVerbClass> verbIndexList = new ArrayList<IVerbClass>();
		verbIndexList = memberIndexMap.get(TargetVerb);
		
		List<IPredicateDesc> tempSemanticPredicate;
		List<IPredicateDesc> resultSemanticPredicate = new ArrayList<IPredicateDesc>();
		
		for(int i = 0; i < verbIndexList.size(); i++){
			//for each verb index class related to this verb
			IVerbClass currentVerbClass = verbIndexList.get(i);
			IFrame frame = currentVerbClass.getFrames().get(0);
			tempSemanticPredicate = frame.getSemantics().getPredicates();
			
			resultSemanticPredicate.addAll(tempSemanticPredicate);
			
			
		}

		return resultSemanticPredicate;
	}
	/*
	 * print related semantic tags for a verb
	 */
	public void printSemanticPredicateList(String TargetVerb){
		List<IPredicateDesc> semanticPredicateList = new ArrayList<IPredicateDesc>();
		semanticPredicateList = getSemantic(TargetVerb);
		for(int i = 0; i < semanticPredicateList.size(); i++){
			//show verb index
			System.out.println(TargetVerb+", semantic "+(i+1)+" : "+semanticPredicateList.get(i));
		}
	}
	/*
	 * get all related verb class (verb index which are used to describe the verb) 
	 */
	public List<IVerbClass> getRelatedVerbClass(String TargetVerb){
		List<IVerbClass> targetVerbClasses = new ArrayList<IVerbClass>();
		return targetVerbClasses;
	}
	/*
	 * print all members in an input verb index
	 */
	public void printMembersInAnIndex(IVerbClass TargetVerbIndex){
		System.out.println("Related verb index: "+TargetVerbIndex.getID());
		List<IMember> memberList = new ArrayList<IMember>();
        memberList = TargetVerbIndex.getMembers();	
        
        for(int i = 0 ; i < memberList.size(); i++){
    		System.out.println("    Member: "+memberList.get(i).getName());
        }
	}
	/*
	 * print all related verb index with their members for the input verb
	 */
	public void printIndexAndMembers(String TargetVerb){
		List<IVerbClass> indexList = new ArrayList<IVerbClass>();
		indexList = memberIndexMap.get(TargetVerb);
		for(int i = 0; i < indexList.size(); i++){
			//show verb index
			printMembersInAnIndex(indexList.get(i));
		}	
	}
}
