package test;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.TreeMap;

public class Plan {
	
	/**
	 * Plan class represent the plan in the map there several stations are distributed.
	 * It provides several functions to calculate some statistics of the system, as well as the methods for the routine.
	 */
	/**
	 * stations: stations arranged in the plan.
	 * routine: the routine to be chosen with respect to a certain principle ("shortest" for example)
	 * map_1: the treemap to collect the stations by order of distance to a certain point.
	 * map_2: the treemap to collect the stations by order of distance to another point.
	 * map_3: the treemap to collect the routines by order of distance in a certain principle.
	 */
	private ArrayList<Station> stations;
	private Routine routine;
	private TreeMap<Double,Station> map_1;
	private TreeMap<Double,Station> map_2;
	private TreeMap<Double, Routine> map_3;
	
	/**
	 * constructor: Plan is instantiated by a list of stations in the map. 
	 */
	public Plan(ArrayList<Station> stations){
		this.stations = stations;
	}
	
	/**
	 * the function most_used_station() is used to order the stations which are sorted by the total number of renting + dropping operations.    
	 * it works after a certain thread of operation where some actions of the user are defined.
	 */
	public HashSet<Station> most_used_station(){
		double m = 0;
		HashSet<Station> ss = new HashSet<Station>();
		for(Station s: this.stations){
			if(s.getRent_times() + s.getReturn_times() >= m){m = s.getRent_times() + s.getReturn_times();}
		}
		for(Station e: this.stations){if(e.getRent_times() + e.getReturn_times() == m){ss.add(e);}}
		return ss;
	}
	
	/**
	 * the function least_occupied_station_mech is used to order the stations by the rate of occupation for the mech bikes (ratio
     * between free time over occupied time of parking bays)   
	 * it works after a certain thread of operation where some actions of the user are defined.
	 * @param t1
	 * @param t2
	 */
	public HashSet<Station> least_occupied_station_mech(double t1, double t2) throws Exception{
		double m = 1;
		HashSet<Station> ss = new HashSet<Station>();
		for(Station s: this.stations){
			if(s.occupation_rate_mech(t1,t2) <= m){m = s.occupation_rate_mech(t1,t2);}
		}
		for(Station e: this.stations){if(e.occupation_rate_mech(t1,t2) == m){ss.add(e);}}
		return ss;
	}
	
	/**
	 * the function least_occupied_station_elec is used to order the stations by the rate of occupation for the elec bikes (ratio
     * between free time over occupied time of parking bays)   
	 * it works after a certain thread of operation where some actions of the user are defined.
	 * @param t1
	 * @param t2
	 */
	public HashSet<Station> least_occupied_station_elec(double t1, double t2) throws Exception{
		double m = 1;
		HashSet<Station> ss = new HashSet<Station>();
		for(Station s: this.stations){
			if(s.occupation_rate_elec(t1,t2) <= m){m = s.occupation_rate_elec(t1,t2);}
		}
		for(Station e: this.stations){if(e.occupation_rate_elec(t1,t2) == m){ss.add(e);}}
		return ss;
	}
	
	/**
	 * the function find_routine_shortest is used to find the best routine with respect to the shortest path policy.
	 * @param start
	 * @param end
	 */
	public Routine find_routine_shortest(double[] start, double[] end){
		
		map_1 = new TreeMap<Double,Station>(); map_2 = new TreeMap<Double,Station>();
		for(Station s:this.stations){map_1.put(Math.pow(start[0]-s.getPosition()[0],2) + Math.pow(start[1]-s.getPosition()[1],2),s);}
		for(Station e:this.stations){map_2.put(Math.pow(end[0]-e.getPosition()[0],2) + Math.pow(end[1]-e.getPosition()[1],2),e);}
		
		routine = new Routine(start[0],start[1],end[0],end[1],map_1.get(map_1.firstKey()),map_2.get(map_2.firstKey()));
		return routine;
	}
	
	/**
	 * the function find_routine_fastest is used to find the best routine with respect to the fastest path policy.
	 * @param start
	 * @param end
	 * @param b
	 */
	public Routine find_routine_fastest(double[] start, double[] end, Bicycle b){
		map_3 = new TreeMap<Double, Routine>();
		for(Station s: stations){
			for(Station e:stations){
				Routine r = new Routine(start[0],start[1],end[0],end[1],s,e);
				map_3.put(r.count_time(b),r);
			}
		}		
		routine = map_3.get(map_3.firstKey());		
		return routine;
	}
	
	/**
	 * the function find_routine_avoid_plus is used to find the best routine with respect to the avoid ¡°plus¡± stations policy.
	 * @param start
	 * @param end
	 */
	public Routine find_routine_avoid_plus(double[] start, double[] end){
		
		this.find_routine_shortest(start, end);
		Station s = map_1.get(map_1.firstKey());
		for(Station e:map_2.values()){
			if(!e.getType().equals("plus")){routine = new Routine(start[0],start[1],end[0],end[1],s,e);break;}
		};
		return routine;
	}
	
	/**
	 * the function find_routine_prefer_plus is used to find the best routine with respect to the prefer ¡°plus¡± stations policy.
	 * @param start
	 * @param end
	 */
	public Routine find_routine_prefer_plus(double[] start, double[] end){
		
		routine = null;		
		this.find_routine_shortest(start, end);
		Station s = map_1.get(map_1.firstKey());
		Station ss = map_2.get(map_2.firstKey());
		for(Station e:map_2.values()){
			if(e.getType().equals("plus")
					&& (Math.pow(end[0]-e.getPosition()[0],2) + Math.pow(end[1]-e.getPosition()[1],2) <= 1.1*1.1*(Math.pow(end[0]-ss.getPosition()[0],2) + Math.pow(end[1]-ss.getPosition()[1],2)))){                                                                
				routine = new Routine(start[0],start[1],end[0],end[1],s,e);
				break;
				}
		};
		if(routine==null){routine = new Routine(start[0],start[1],end[0],end[1],s,ss);}
		return routine;
	}
	
	/**
	 * the function find_routine_uniform is used to find the best routine with respect to the preservation of uniformity of bicycles distribution amongst stations policy.
	 * @param start
	 * @param end
	 * @param b
	 */
	public Routine find_routine_uniform(double[] start, double[] end, Bicycle b) throws Exception{
		
		routine = null;		
		this.find_routine_shortest(start, end);
		Station so=null; Station sd=null; Station soo=null; Station sdd=null;
		
		OUT_1: for(Station s: map_1.values()){
			if(b instanceof Bicycle_Mech){for(Bicycle_Mech bm: s.getPlaces_mech().values()){if(bm!=null){so = s;break OUT_1;}}}
			if(b instanceof Bicycle_Elec){for(Bicycle_Elec be: s.getPlaces_elec().values()){if(be!=null){so = s;break OUT_1;}}}
		}
		
		OUT_2: for(Station e: map_2.values()){
			if(b instanceof Bicycle_Mech){if(e.getPlaces_mech().values().contains(null)){sd = e;break OUT_2;}}
			if(b instanceof Bicycle_Elec){if(e.getPlaces_elec().values().contains(null)){sd = e;break OUT_2;}}
		}
		
		OUT_3: for(Station ss: map_1.values()){
			if(b instanceof Bicycle_Mech){
				if(ss.count_mech()>=so.count_mech()&&
						(Math.pow(start[0]-ss.getPosition()[0],2) + Math.pow(start[1]-ss.getPosition()[1],2) <= 1.05*1.05*(Math.pow(start[0]-so.getPosition()[0],2) + Math.pow(start[1]-so.getPosition()[1],2)))){
					soo = ss;
					break OUT_3;
				}
			}
			if(b instanceof Bicycle_Elec){
				if(ss.count_elec()>=so.count_elec()&&
						(Math.pow(start[0]-ss.getPosition()[0],2) + Math.pow(start[1]-ss.getPosition()[1],2) <= 1.05*1.05*(Math.pow(start[0]-so.getPosition()[0],2) + Math.pow(start[1]-so.getPosition()[1],2)))){
					soo = ss;
					break;
				}
			}
		}
		
		OUT_4: for(Station ee: map_2.values()){
			if(b instanceof Bicycle_Mech){
				if(ee.getPlaces_mech().size()-ee.count_mech() >= sd.getPlaces_mech().size()-sd.count_mech() &&
						(Math.pow(end[0]-ee.getPosition()[0],2) + Math.pow(end[1]-ee.getPosition()[1],2) <= 1.05*1.05*(Math.pow(end[0]-sd.getPosition()[0],2) + Math.pow(end[1]-sd.getPosition()[1],2)))){
					sdd = ee;
					break OUT_4;
				}
			}
			if(b instanceof Bicycle_Elec){
				if(ee.getPlaces_elec().size()-ee.count_elec() >= sd.getPlaces_elec().size()-sd.count_elec() &&
						(Math.pow(end[0]-ee.getPosition()[0],2) + Math.pow(end[1]-ee.getPosition()[1],2) <= 1.05*1.05*(Math.pow(end[0]-sd.getPosition()[0],2) + Math.pow(end[1]-sd.getPosition()[1],2)))){
					sdd = ee;
					break;
				}
			}
		}
		
		if(sd==null || so==null){return null;}
		else{
			if(sdd==null || soo==null){routine = new Routine(start[0],start[1],end[0],end[1],so,sd);}
			else{routine = new Routine(start[0],start[1],end[0],end[1],soo,sdd);}
		}
		
		return routine;
	}

	/**
	 * getters and setters
	 */
	public ArrayList<Station> getStations() {
		return stations;
	}

	public void setStations(ArrayList<Station> stations) {
		this.stations = stations;
	}
	
}
