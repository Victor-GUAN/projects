package myVelib;

import java.util.ArrayList;
import java.util.HashMap;

public class Demo {
	
	public static void main(String[] args) throws Exception {
		
		/**
		 * this is a test scenario to testify the normal operation of the system
		 */
		/**
		 * instantiate two types of velib card: card_vmax and card_vlibre
		 */
		Card card_vmax = new Card_Vmax();
		Card card_vlibre = new Card_Vlibre();
		
		/**
		 * instantiate several stations of bicycles with different types, which are distributed on the plan.
		 * add some bikes (mech and elec) to each station corresponding to their number of slots.
		 */
		Station s_1_plus = new Station_Plus(1,20,0,5,10);
		for(Slot s: s_1_plus.getPlaces_mech().keySet())
		{for(int i=11;i<=13;i++){if(s.getId()+10==i){s_1_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_1_plus.getPlaces_elec().keySet())
		{for(int i=11;i<=16;i++){if(s.getId()+10==i){s_1_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		Station s_2_plus = new Station_Plus(2,0,20,10,5);
		for(Slot s: s_2_plus.getPlaces_mech().keySet())
		{for(int i=21;i<=25;i++){if(s.getId()+20==i){s_2_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_2_plus.getPlaces_elec().keySet())
		{for(int i=21;i<=24;i++){if(s.getId()+20==i){s_2_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		Station s_3_standard = new Station_Standard(3,20,20,10,10);
		for(Slot s: s_3_standard.getPlaces_mech().keySet())
		{for(int i=31;i<=37;i++){if(s.getId()+30==i){s_3_standard.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_3_standard.getPlaces_elec().keySet())
		{for(int i=31;i<=36;i++){if(s.getId()+30==i){s_3_standard.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		Station s_4_plus = new Station_Plus(4,0,0,5,5);
		for(Slot s: s_4_plus.getPlaces_mech().keySet())
		{for(int i=41;i<=42;i++){if(s.getId()+40==i){s_4_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_4_plus.getPlaces_elec().keySet())
		{for(int i=41;i<=43;i++){if(s.getId()+40==i){s_4_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		/**
		 * create a plan in the map, and add the stations above to the plan
		 */
		ArrayList<Station> stations = new ArrayList<Station>();
		stations.add(s_1_plus);stations.add(s_2_plus);stations.add(s_3_standard);stations.add(s_4_plus);
		final Plan plan = new Plan(stations);
		
		/**
		 * instantiate several users of this system, and arrange different parameters and properties to them.
		 */
        //User admin = new User("admin",0,0,0,null);
        final User user_1 = new User("user_1",1,10,10,card_vmax);
        final User user_2 = new User("user_2",2,10,0,card_vlibre);
        final User user_3 = new User("user_3",3,0,10,null);
        
		/**
		 * instantiate several bank_cards to different users, with some initial amounts of money.
		 */
        //Bank_Card bc_0 = new Bank_Card(1000,admin,0);
        final Bank_Card bc_1 = new Bank_Card(100,user_1,1);
        final Bank_Card bc_2 = new Bank_Card(200,user_2,2);
        final Bank_Card bc_3 = new Bank_Card(300,user_3,3);
        
        /*admin.check_station(s_4_plus);
        admin.find_routine(3,3,plan,"uniform",new Bicycle_Mech(0));
        admin.choose_routine(admin.getLast_routine());*/
           
		/**
		 * create several threads to realize the multi-threading functionality of the system.
		 * In each thread, we define some actions and behaviors of the users (choose_routine, take, park, walk, etc).
		 * after the running of all threads, we can calculate the statistical data during certain period of the operation of the thread.
		 * each thread has different actions in it, and between two actions, thread will sleep some time corresponding to the time spent on the trip in reality.
		 */
        Thread thread_1 = new Thread(new Runnable(){
        	public void run(){
        		try{
        			user_1.find_routine(40, 50, plan, "shortest", new Bicycle_Elec(0));
        			user_1.choose_routine(user_1.getLast_routine());

        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)0, (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)0, (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t1 = 1000*user_1.count_walk_time(user_1.getLast_routine().getSource().getPosition()[0], user_1.getLast_routine().getSource().getPosition()[1]);         
        			Thread.sleep((long)t1);
        			
        			user_1.take(user_1.getLast_routine().getSource(), new Bicycle_Elec(0),bc_1);
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)t1, (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)t1, (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t2 = 1000*user_1.getBicycle().count_bike_time(user_1.getLast_routine().getSource(), user_1.getLast_routine().getDestination());
        			Thread.sleep((long)t2);
        			
        			user_1.park(user_1.getLast_routine().getDestination());
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)(t1+t2), (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)(t1+t2), (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t3 = 1000*user_1.count_walk_time(40, 50);
        			Thread.sleep((long)t3);
        			
        			System.out.println("User_1 Arrived!");
        			
        		}catch(Exception e){};
        	}
        });
        
        Thread thread_2 = new Thread(new Runnable(){
        	public void run(){
        		try{
        			double t0 = 1000*1;
        			Thread.sleep((long)t0);
        			
        			user_2.find_routine(-10, 30, plan, "fastest", new Bicycle_Mech(0));
        			user_2.choose_routine(user_2.getLast_routine());
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)t0, (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)t0, (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t1 = 1000*user_2.count_walk_time(user_2.getLast_routine().getSource().getPosition()[0], user_2.getLast_routine().getSource().getPosition()[1]);         
        			Thread.sleep((long)t1);
        			
        			user_2.take(user_2.getLast_routine().getSource(), new Bicycle_Elec(0),bc_2);
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)(t0+t1), (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)(t0+t1), (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}

        			double t2 = 1000*user_2.getBicycle().count_bike_time(user_2.getLast_routine().getSource(), user_2.getLast_routine().getDestination());
        			Thread.sleep((long)t2);
        			
        			user_2.park(user_2.getLast_routine().getDestination());
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)(t0+t1+t2), (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)(t0+t1+t2), (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t3 = 1000*user_2.count_walk_time(-10, 30);
        			Thread.sleep((long)t3);
        			
        			System.out.println("User_2 Arrived!");
        			
        		}catch(Exception e){};
        	}
        });
        
        Thread thread_3 = new Thread(new Runnable(){
        	public void run(){
        		try{
        			double t0 = 1000*2;
        			Thread.sleep((long)t0);
        			
        			user_3.find_routine(15, 50, plan, "uniform", new Bicycle_Elec(0));
        			user_3.choose_routine(user_3.getLast_routine());
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)(t0), (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)(t0), (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t1 = 1000*user_3.count_walk_time(user_3.getLast_routine().getSource().getPosition()[0], user_3.getLast_routine().getSource().getPosition()[1]);         
        			Thread.sleep((long)t1);
        			
        			user_3.take(user_3.getLast_routine().getSource(), new Bicycle_Elec(0),bc_3);
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)(t0+t1), (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)(t0+t1), (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t2 = 1000*(user_3.getBicycle().count_bike_time(user_3.getLast_routine().getSource(), user_3.getLast_routine().getDestination()));
        			Thread.sleep((long)t2);
        			
        			user_3.park(user_3.getLast_routine().getDestination());
        			
        			for(Station s: plan.getStations()){
        				s.getStates_list_mech().put((double)(t0+t1+t2), (HashMap<Slot,Bicycle_Mech>)s.getPlaces_mech());
        				s.getStates_list_elec().put((double)(t0+t1+t2), (HashMap<Slot,Bicycle_Elec>)s.getPlaces_elec());
        			}
        			
        			double t3 = 1000*user_3.count_walk_time(15, 50);
        			Thread.sleep((long)t3);
        			
        			System.out.println("User_3 Arrived!");
        			
        		}catch(Exception e){};
        	}
        });
        
		/**
		 * all thread starts simultaneously.
		 * the independence is guaranteed by the synchronized function inside.
		 */
        thread_1.start();
        thread_2.start();
        thread_3.start();
        
		/**
		 * wait for all threads finishing.
		 */
        thread_1.join();
        thread_2.join();
        thread_3.join();
        
		/**
		 * show some statistics of the system, like the occupation rate and the most used station.
		 */
        System.out.println("The occupation rate of elec bikes for Station 3: "+s_3_standard.occupation_rate_elec(0.5*1000, 1.5*1000));
        System.out.println("The occupation rate of mech bikes for Station 3: "+s_3_standard.occupation_rate_mech(0.5*1000, 1.5*1000));
        
        System.out.println("Most used station: " + plan.most_used_station());
        System.out.println("Least elec occupied station: " + plan.least_occupied_station_elec(0.5*1000, 1.5*1000));
        System.out.println("Least mech occupied station: " + plan.least_occupied_station_mech(0.5*1000, 1.5*1000));
        System.out.println("FINISHED!!!");
    }  
}
