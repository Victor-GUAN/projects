package myVelib;

import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class RunMe extends OutputStream{
	
	OutputStream output1;
	OutputStream output2;
	
	private static Scanner sc;
	
	public RunMe(OutputStream output1, OutputStream output2){this.output1 = output1;this.output2 = output2;}
	
	@Override
	public void write(int b) throws IOException {
		output1.write(b);
		output2.write(b);
	}
	
	public static void clui(String s, Plan plan, ArrayList<User> users, ArrayList<Bank_Card> bank_cards) throws Exception{
		String[] list;
		list = s.split("\\s+");
		switch (list[0]){
    		case "setup":
    			ArrayList<Station> stations = new ArrayList<Station>();

    			if(list.length == 2){
    				String com = list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">"));
    				int id_number = 1;
    				for(int i=1;i<=3;i++){
    					for(int j=1;j<=3;j++){
    						if(id_number % 2 == 0){
    							Station sta_st = new Station_Standard(id_number,(i-1)*4,(j-1)*4,10,10);
    							for(Slot sl: sta_st.getPlaces_mech().keySet())
    							{for(int m=1;m<=7;m++){if(sl.getId()==m){sta_st.getPlaces_mech().put(sl, new Bicycle_Mech(m));break;}}}          
    							for(Slot sl: sta_st.getPlaces_elec().keySet())
    							{for(int n=1;n<=7;n++){if(sl.getId()==n){sta_st.getPlaces_elec().put(sl, new Bicycle_Elec(n));break;}}}
    							stations.add(sta_st);
    						}
    						else if(id_number % 2 == 1){
    							Station sta_pl = new Station_Plus(id_number,(i-1)*4,(j-1)*4,10,10);
    							for(Slot sl: sta_pl.getPlaces_mech().keySet())
    							{for(int m=1;m<=7;m++){if(sl.getId()==m){sta_pl.getPlaces_mech().put(sl, new Bicycle_Mech(m));break;}}}          
    							for(Slot sl: sta_pl.getPlaces_elec().keySet())
    							{for(int n=1;n<=7;n++){if(sl.getId()==n){sta_pl.getPlaces_elec().put(sl, new Bicycle_Elec(n));break;}}}
    							stations.add(sta_pl);
    						}
    						id_number += 1;
    					}
    				}
    				
    				plan.setStations(stations);
    				plan.setName(com);

    				System.out.println("A plan has been constructed, which has name \"" + com + "\" and consists of 9 stations each of which has 10 electronic and 10 mechanical parking slots and such that stations are arranged on a square grid whose of side 4km and initially populated with a 70% bikes randomly distributed over the 9 stations.");                                     
    			}
    			else if(list.length == 6){
    				String name = list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">"));
    				int nstations = Integer.parseInt(list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">")));
    				int nslots = Integer.parseInt(list[3].substring(list[3].indexOf("<")+1,list[3].lastIndexOf(">")));
    				double side = Double.parseDouble(list[4].substring(list[4].indexOf("<")+1,list[4].lastIndexOf(">")));
    				int nbikes = Integer.parseInt(list[5].substring(list[5].indexOf("<")+1,list[5].lastIndexOf(">")));
    			
    				if(nbikes > nslots){throw new Exception("nbikes > nslots");}      			
    				int nsquare = (int)Math.sqrt(nstations);
    			
    				int id_number = 1;
    				for(int i=1;i<=nsquare;i++){
    					for(int j=1;j<=nsquare;j++){
    						if(id_number % 2 == 0){
    							Station sta_st = new Station_Standard(id_number,(i-1)*side,(j-1)*side,nslots,nslots);
    							for(Slot sl: sta_st.getPlaces_mech().keySet())
    							{for(int m=1;m<=nbikes;m++){if(sl.getId()==m){sta_st.getPlaces_mech().put(sl, new Bicycle_Mech(m));break;}}}          
    							for(Slot sl: sta_st.getPlaces_elec().keySet())
    							{for(int n=1;n<=nbikes;n++){if(sl.getId()==n){sta_st.getPlaces_elec().put(sl, new Bicycle_Elec(n));break;}}}
    							stations.add(sta_st);
    						}
    						else if(id_number % 2 == 1){
    							Station sta_pl = new Station_Plus(id_number,(i-1)*side,(j-1)*side,nslots,nslots);
    							for(Slot sl: sta_pl.getPlaces_mech().keySet())
    							{for(int m=1;m<=nbikes;m++){if(sl.getId()==m){sta_pl.getPlaces_mech().put(sl, new Bicycle_Mech(m));break;}}}          
    							for(Slot sl: sta_pl.getPlaces_elec().keySet())
    							{for(int n=1;n<=nbikes;n++){if(sl.getId()==n){sta_pl.getPlaces_elec().put(sl, new Bicycle_Elec(n));break;}}}
    							stations.add(sta_pl);
    						}
    						id_number += 1;
    					}
    				}
    			
    				for(int p = nsquare*nsquare+1;p<=nstations;p++){
    					if(p % 2 == 0){
    						Station sta_st = new Station_Standard(p,nsquare*side,(p-nsquare*nsquare-1)*side,nslots,nslots);
    						for(Slot sl: sta_st.getPlaces_mech().keySet())
    						{for(int m=1;m<=nbikes;m++){if(sl.getId()==m){sta_st.getPlaces_mech().put(sl, new Bicycle_Mech(m));break;}}}          
    						for(Slot sl: sta_st.getPlaces_elec().keySet())
    						{for(int n=1;n<=nbikes;n++){if(sl.getId()==n){sta_st.getPlaces_elec().put(sl, new Bicycle_Elec(n));break;}}}
    						stations.add(sta_st);
    					}
    					if(p % 2 == 1){
    						Station sta_pl = new Station_Plus(p,nsquare*side,(p-nsquare*nsquare-1)*side,nslots,nslots);
    						for(Slot sl: sta_pl.getPlaces_mech().keySet())
    						{for(int m=1;m<=nbikes;m++){if(sl.getId()==m){sta_pl.getPlaces_mech().put(sl, new Bicycle_Mech(m));break;}}}          
    						for(Slot sl: sta_pl.getPlaces_elec().keySet())
    						{for(int n=1;n<=nbikes;n++){if(sl.getId()==n){sta_pl.getPlaces_elec().put(sl, new Bicycle_Elec(n));break;}}}
    						stations.add(sta_pl);
    					}			
    				}
    			
    				plan.setStations(stations);
    				plan.setName(name);        	
    				
    				System.out.println("A plan has been constructed, which has name \"" + name + "\" and consists of "+nstations+" stations each of which has "+nslots+" electronic and "+nslots+" mechanical parking slots and such that stations are arranged on a square grid whose of side "+side+"km and initially populated with a "+(nbikes/nslots)*100+"% bikes randomly distributed over the "+nstations+" stations.");
    			}
    			else{throw new Exception("Wrong Command Format");}
    		
    			for(Station station: plan.getStations()){
    				station.getStates_list_mech().put((double)0, (HashMap<Slot,Bicycle_Mech>)station.getPlaces_mech());
    				station.getStates_list_elec().put((double)0, (HashMap<Slot,Bicycle_Elec>)station.getPlaces_elec());
    			}		
    		
    			break;
    		case "addUser":
    			if(list.length == 6){
    				String userName = list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">"));
    				String cardType = list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">"));
    				String planName = list[3].substring(list[3].indexOf("<")+1,list[3].lastIndexOf(">"));
    				double x = Double.parseDouble(list[4].substring(list[4].indexOf("<")+1,list[4].lastIndexOf(">")));
    				double y = Double.parseDouble(list[5].substring(list[5].indexOf("<")+1,list[5].lastIndexOf(">")));
    			
    			
    				Card velo_card;
    				if(cardType.equals("vmax")||cardType.equals("Vmax")||cardType.equals("VMax")||cardType.equals("VMAX")){
    					velo_card = new Card_Vmax();
    				}
    				else if(cardType.equals("vlibre")||cardType.equals("Vlibre")||cardType.equals("VLibre")||cardType.equals("VLIBRE")){
    					velo_card = new Card_Vlibre();
    				}
    				else if(cardType.equals("null")){velo_card = null;}
    				else{velo_card = null;}
    			
    				User user = new User(userName,users.size()+1,x,y,velo_card);
    				Bank_Card bank_card = new Bank_Card(10000,user,user.getUserId());
    			
    				users.add(user);
    				bank_cards.add(bank_card);

    				plan.setName(planName);
    				
    				System.out.println("A user named" +userName+ "has been added to the plan "+planName+". They holds a velib card of type "+cardType+", and their location is x:"+x+", y: "+y);
    			
    			}
    			else{throw new Exception("Wrong Command Format");}
    		
    			break;
    		case "offline":
    			if(list.length == 4){
    				String planName = list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">"));
    				int stationID = Integer.parseInt(list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">")));
    				double time = Double.parseDouble(list[3].substring(list[3].indexOf("<")+1,list[3].lastIndexOf(">")));
    			
    				plan.setName(planName);
    				for(Station sta: plan.getStations()){if(sta.getId()==stationID){sta.setState(false);break;}}
    				for(Station station: plan.getStations()){
    					station.getStates_list_mech().put((double)time, (HashMap<Slot,Bicycle_Mech>)station.getPlaces_mech());
    					station.getStates_list_elec().put((double)time, (HashMap<Slot,Bicycle_Elec>)station.getPlaces_elec());
    				}
    				
    				System.out.println("The station of ID: "+stationID+" in the plan "+planName+" has been set offline at time unit: "+time);
    			
    			}
    			else{throw new Exception("Wrong Command Format");}	
    		
    			break;
    		case "online":
    			if(list.length == 4){
    				String planName = list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">"));
    				int stationID = Integer.parseInt(list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">")));
    				double time = Double.parseDouble(list[3].substring(list[3].indexOf("<")+1,list[3].lastIndexOf(">")));
    			
    				plan.setName(planName);
    				for(Station sta: plan.getStations()){if(sta.getId()==stationID){sta.setState(true);break;}}
    				for(Station station: plan.getStations()){
    					station.getStates_list_mech().put((double)time, (HashMap<Slot,Bicycle_Mech>)station.getPlaces_mech());
    					station.getStates_list_elec().put((double)time, (HashMap<Slot,Bicycle_Elec>)station.getPlaces_elec());
    				}
    				
    				System.out.println("The station of ID: "+stationID+" in the plan "+planName+" has been set online at time unit: "+time);
    			}
    			else{throw new Exception("Wrong Command Format");}	
         
    			break;
    		case "rentBike":
    			if(list.length == 4){
    				int userID = Integer.parseInt(list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">")));
    				int stationID = Integer.parseInt(list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">")));
    				String bikeType = list[3].substring(list[3].indexOf("<")+1,list[3].lastIndexOf(">"));
    			
    				Station sta = null;
    				User user = null;
    				Bank_Card bc = null;
    				for(Station station: plan.getStations()){if(station.getId()==stationID){sta = station;break;}}
    				for(User u: users){if(u.getUserId()==userID){user = u;break;}}
    				for(Bank_Card bank_card: bank_cards){if(bank_card.getId()==userID){bc = bank_card;break;}}
    			
    				sta.add_user(user);
    				user.setLast_routine(new Routine(user.getPosition()[0],user.getPosition()[1],sta.getPosition()[0],sta.getPosition()[1],sta,null));
    			
    				double time = user.count_walk_time(sta.getPosition()[0], sta.getPosition()[1]);
    			
    				if(bikeType.equals("mechanical")){user.take(sta, new Bicycle_Mech(0), bc);}
    				else if(bikeType.equals("electronic")){user.take(sta, new Bicycle_Elec(0), bc);}
    				else{throw new Exception("Wrong Command Format");}
    			
    				for(Station station: plan.getStations()){
    					station.getStates_list_mech().put((double)time, (HashMap<Slot,Bicycle_Mech>)station.getPlaces_mech());
    					station.getStates_list_elec().put((double)time, (HashMap<Slot,Bicycle_Elec>)station.getPlaces_elec());
    				}
    				
    				System.out.println("A bike of type: "+bikeType+" has been successfully rent by the user of ID: "+userID+" at the station of ID: "+stationID);
    			
    			}
    			else{throw new Exception("Wrong Command Format");}	

    			break;
    		case "returnBike":
    			if(list.length == 4){
    				int userID = Integer.parseInt(list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">")));
    				int stationID = Integer.parseInt(list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">")));
    				double time = Double.parseDouble(list[3].substring(list[3].indexOf("<")+1,list[3].lastIndexOf(">")));
    			
    				Station sta = null;
    				User user = null;

    				for(Station station: plan.getStations()){if(station.getId()==stationID){sta = station;break;}}
    				for(User u: users){if(u.getUserId()==userID){user = u;break;}}
    			
    				sta.add_user(user);
    				user.getLast_routine().setDestination(sta);
    				user.getLast_routine().setEnd(new double[]{sta.getPosition()[0],sta.getPosition()[1]});
    				//user.setLast_routine(new Routine(user.getPosition()[0],user.getPosition()[1],sta.getPosition()[0],sta.getPosition()[1],null,sta));
    			
    				user.park(sta);
    			
    				for(Station station: plan.getStations()){
    					station.getStates_list_mech().put((double)time, (HashMap<Slot,Bicycle_Mech>)station.getPlaces_mech());
    					station.getStates_list_elec().put((double)time, (HashMap<Slot,Bicycle_Elec>)station.getPlaces_elec());
    				}
    				
    				System.out.println("The bike used by the user of ID: "+userID+" has been successfully returned at the station of ID: "+stationID+", at the time unit: "+time);
    				System.out.println("The payment has been automatically taken above");
    			
    			}
    			else{throw new Exception("Wrong Command Format");}	
    			
    			break;
    		case "displayStation":
    			if(list.length == 3){
    				int stationID = Integer.parseInt(list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">")));
    				double time = Double.parseDouble(list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">")));
    			
    				Station sta = null;
    				for(Station station: plan.getStations()){if(station.getId()==stationID){sta = station;break;}}
    			
    				users.get(0).check_station(sta);
    				System.out.println("The occupation rate of elec bikes for Station " + sta.getId()+": "+sta.occupation_rate_elec(0, time));
    				System.out.println("The occupation rate of mech bikes for Station " + sta.getId()+": "+sta.occupation_rate_mech(0, time));       
		
    			}
    			else{throw new Exception("Wrong Command Format");}	

    			break;
    		case "findRoutine":
    			if(list.length == 6){
    				double x = Double.parseDouble(list[1].substring(list[1].indexOf("<")+1,list[1].lastIndexOf(">")));
    				double y = Double.parseDouble(list[2].substring(list[2].indexOf("<")+1,list[2].lastIndexOf(">")));
    				String sortPolicy = list[3].substring(list[3].indexOf("<")+1,list[3].lastIndexOf(">"));
    				String bikeType = list[4].substring(list[4].indexOf("<")+1,list[4].lastIndexOf(">"));
    				int userID = Integer.parseInt(list[5].substring(list[5].indexOf("<")+1,list[5].lastIndexOf(">")));
    			
    				User user = null;
    				for(User u: users){if(u.getUserId()==userID){user = u;break;}}
    			
    				if(bikeType.equals("mechanical")){user.find_routine(x, y, plan, sortPolicy, new Bicycle_Mech(0));}
    				else if(bikeType.equals("electronic")){user.find_routine(x, y, plan, sortPolicy, new Bicycle_Elec(0));}
    				else{throw new Exception("Wrong Command Format");}
    			
    				user.choose_routine(user.getLast_routine());
    			
    				System.out.println("The routine best suited to the sort policy and the chosen destination: "+user.getLast_routine());
    				System.out.println(plan.getMap_1());
    				System.out.println(plan.getMap_2());
    				System.out.println(plan.getMap_3());	
    			
    			}
    			else{throw new Exception("Wrong Command Format");}	

    			break;
    		case "display":
    			
    			System.out.println("The info in the network");
    			for(Station sta: plan.getStations()){
    				users.get(0).check_station(sta);
    			}
    		
    			break; 
    		
    		case "runtest":
    			if(list.length == 2){
    				String fileName = list[1];
    				FileReader file = null;
    				BufferedReader reader = null;
    				FileOutputStream propFile = null;
    				RunMe multi = null;
    				
    			
    				try{
    					file = new FileReader(fileName);
    					
    					propFile = new FileOutputStream(fileName.split("\\.")[0]+"output.txt");
    					multi = new RunMe(new PrintStream(propFile),System.out);
    					System.setOut(new PrintStream(multi));
    					
    					reader = new BufferedReader(file);
    					String line = reader.readLine();
    					
    					while(line!=null && !line.isEmpty()){
    						clui(line,plan,users,bank_cards);
    						line = reader.readLine();
    					}
    					
    					System.out.println("Reading of the file: "+fileName+" and Writing of the file: "+fileName.split("\\.")[0]+"output.txt"+" have been finished!");
    					
    				}catch (Exception e){
    					e.printStackTrace();
    					throw new RuntimeException(e);
    				}finally{
    					if(reader!=null){try{reader.close();}catch(IOException e){}}
    					if(file!=null){try{file.close();}catch(IOException e){}}
    					if(multi!=null){try{multi.close();}catch(IOException e){}}
    					if(propFile!=null){try{propFile.close();}catch(IOException e){}}
    				} 			    			
    			}
    			else{throw new Exception("Wrong Command Format");}		        			        		         	      	       	
    		
    			break;   
    		default:
    			throw new Exception("Wrong Command Format");
		}			
	}

	public static void main(String[] args) throws Exception {
		
		Plan plan = new Plan(null);
		ArrayList<User> users = new ArrayList<User>();
		ArrayList<Bank_Card> bank_cards = new ArrayList<Bank_Card>();
		
		clui("runtest my_velib.ini",plan,users,bank_cards);
		
		System.out.println("Please input your commands: ");
		/*String[] list;*/
		sc = new Scanner(System.in);
		String s = sc.nextLine().trim();	
		
		while(s != null && !s.isEmpty()){
			
			clui(s,plan,users,bank_cards);
			
			System.out.println("Please input your next commands: ");
			
			s = sc.nextLine().trim();
					
		}

	}

}
