package test;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.TreeMap;


public abstract class Station {
	
	/**
	 * Station class represents a station of bikes which is a parent class of Station_Plus and Station_Standard
	 */
	/**
	 * places_mech: HashMap for the collections of mech bikes parked in this station
	 * places_elec: HashMap for the collections of elec bikes parked in this station
	 * users: collection of users added to this station (user is added when he is going to take a bike at this station, or to park his bike at this station).                                 
	 * position: the coordinates of this station
	 * state: offline or not for this station
	 * id: id of this station
	 * type: type of this station (plus or standard, determined by its subclass)
	 * rent_times: number of renting at this station
	 * return_times: number of dropping bikes at this station
	 * states_list_mech: treemap to store the states of the station's places for mech bikes at different moments (at each moment in this treemap, there is an action of taking or parking)
	 *					 key: time moment; value: HashMap for the collections of mech bikes parked in this station
	 * states_list_elec: treemap to store the states of the station's places for elec bikes at different moments (at each moment in this treemap, there is an action of taking or parking)
	 *					 key: time moment; value: HashMap for the collections of elec bikes parked in this station
	 */
	private HashMap<Slot,Bicycle_Mech> places_mech;
	private HashMap<Slot,Bicycle_Elec> places_elec;
	private HashSet<User> users;
	private double[] position;
	private boolean state;
	private int id;
	private String type;
	private int rent_times;
	private int return_times;
	private TreeMap<Double,HashMap<Slot,Bicycle_Mech>> states_list_mech;
	private TreeMap<Double,HashMap<Slot,Bicycle_Elec>> states_list_elec;
	
	/**
	 * constructor: Station is instantiate by its id, its position, the places for mech bikes, and the places for elec bikes
	 * x: the first coordinate of its position
	 * y: the second coordinate of its position
	 * N: the number of places for mech bikes
	 * M: the number of places for elec bikes
	 * @param id
	 * @param x
	 * @param y
	 * @param N
	 * @param M
	 */
	public Station(int id, double x, double y, int N, int M) throws Exception{
		super();
		this.id = id;
		this.position = new double[]{x,y};
		this.places_mech = new HashMap<Slot,Bicycle_Mech>();
		this.places_elec = new HashMap<Slot,Bicycle_Elec>();
		for(int i=1;i<=N;i++){this.places_mech.put(new Slot(i), null);}
		for(int j=1;j<=M;j++){this.places_elec.put(new Slot(j), null);}
		this.state = true;
		this.type = null;
		this.users = new HashSet<User>();
		this.notify_users();
		this.rent_times = 0;
		this.return_times = 0;
		this.states_list_mech = new TreeMap<Double,HashMap<Slot,Bicycle_Mech>>();
		this.states_list_elec = new TreeMap<Double,HashMap<Slot,Bicycle_Elec>>();
	}
	
	/**
	 * the function occupation_rate_mech() is used to calculate the occupation for its mech bike slots during a certain period.   
	 * it works after a certain thread of operation where some actions of the user are defined.
	 * @param t1
	 * @param t2
	 */
	public double occupation_rate_mech(double t1, double t2) throws Exception{
		if(t2 < t1){System.out.println("WRONG INTERVAL");throw new Exception("WRONG INTERVAL");}
		double de = (t2 - t1)*this.places_mech.size();
		
		double occupation = 0;
		Double[] key_array = this.states_list_mech.keySet().toArray(new Double[this.states_list_mech.keySet().size()]); 
		for(Slot slot: this.places_mech.keySet()){
			for(int j=0;j<=key_array.length-2;j++){
				if(key_array[j].doubleValue() >= t1 && key_array[j+1].doubleValue() <= t2){
					if(this.states_list_mech.get(key_array[j]).get(slot)!=null){occupation += key_array[j+1].doubleValue() - key_array[j].doubleValue();}                                 
				}
				if(key_array[j].doubleValue() < t1 && key_array[j+1].doubleValue() > t1){
					if(this.states_list_mech.get(key_array[j]).get(slot)!=null){occupation += key_array[j+1].doubleValue() - t1;}
				}
				if(key_array[j].doubleValue() < t2 && key_array[j+1].doubleValue() > t2){
					if(this.states_list_mech.get(key_array[j]).get(slot)!=null){occupation += t2 - key_array[j].doubleValue();}
				}
			}
		}
		return occupation / de;
	}
	
	/**
	 * the function occupation_rate_elec() is used to calculate the occupation for its elec bike slots during a certain period.   
	 * it works after a certain thread of operation where some actions of the user are defined.
	 * @param t1
	 * @param t2
	 */
	public double occupation_rate_elec(double t1, double t2) throws Exception{
		if(t2 < t1){System.out.println("WRONG INTERVAL");throw new Exception("WRONG INTERVAL");}
		double de = (t2 - t1)*this.places_elec.size();
		
		double occupation = 0;
		//System.out.println(this.getStates_list_elec());
		Double[] key_array = this.getStates_list_elec().keySet().toArray(new Double[this.getStates_list_elec().keySet().size()]); 
		for(Slot slot: this.places_elec.keySet()){
			for(int j=0;j<=key_array.length-2;j++){
				if(key_array[j].doubleValue() >= t1 && key_array[j+1].doubleValue() <= t2){
					if(this.states_list_elec.get(key_array[j]).get(slot)!=null){occupation += key_array[j+1].doubleValue() - key_array[j].doubleValue();}                                 
				}
				if(key_array[j].doubleValue() < t1 && key_array[j+1].doubleValue() > t1){
					if(this.states_list_elec.get(key_array[j]).get(slot)!=null){occupation += key_array[j+1].doubleValue() - t1;}
				}
				if(key_array[j].doubleValue() < t2 && key_array[j+1].doubleValue() > t2){
					if(this.states_list_elec.get(key_array[j]).get(slot)!=null){occupation += t2 - key_array[j].doubleValue();}
				}
			}
		}
		return occupation / de;
	}
	
	/**
	 * the observable function notify_users() is used to notify all its added users the modification info
	 */
	public void notify_users() throws Exception{
		for(User u: this.users){
			u.check_station(this);
		}
	}
	
	/**
	 * the function add_user is used to register users to this station (user is added when he is going to take a bike at this station, or to park his bike at this station).
	 * @param user
	 */
	public void add_user(User user) throws Exception{
		if(!this.state){System.out.println("offline - out of order!");throw new Exception("OFFLINE");}
		this.users.add(user);
		System.out.println("Station "+ this.getType() + " " + this.id +" successfully added the user " + user.getUserName() + " " + user.getUserId());
	}
	
	/**
	 * the function remove_user is used to remove users from this station (user is removed when he has taken a bike at this station, or has parked his bike at this station).
	 * @param user
	 */
	public void remove_user(User user) throws Exception{
		if(!this.state){System.out.println("offline - out of order!");throw new Exception("OFFLINE");}
		if(this.users.contains(user)){
			this.users.remove(user);
			System.out.println("Station "+ this.getType() + " " + this.id +" successfully removed the user " + user.getUserName() + " " + user.getUserId());
		}
	}
	
	/**
	 * the function count_elec is used to count the number of available elec bikes at this station.
	 */
	public int count_elec() throws Exception{
		if(!this.state){System.out.println("offline - out of order!");throw new Exception("OFFLINE");}
		int i = 0;
		for(Bicycle_Elec be: this.places_elec.values()){if(be!=null){i+=1;}}
		return i;
	}
	
	/**
	 * the function count_mech is used to count the number of available mech bikes at this station.
	 */
	public int count_mech() throws Exception{
		if(!this.state){System.out.println("offline - out of order!");throw new Exception("OFFLINE");}
		int j = 0;
		for(Bicycle_Mech bm: this.places_mech.values()){if(bm!=null){j+=1;}}
		return j;
	}
	
	/**
	 * getters and setters
	 */
	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public Map<Slot, Bicycle_Mech> getPlaces_mech() {
		return places_mech;
	}

	public void setPlaces_mech(HashMap<Slot, Bicycle_Mech> places_mech) throws Exception {
		this.places_mech = places_mech;
		this.notify_users();
	}

	public Map<Slot, Bicycle_Elec> getPlaces_elec() {
		return places_elec;
	}

	public void setPlaces_elec(HashMap<Slot, Bicycle_Elec> places_elec) throws Exception {
		this.places_elec = places_elec;
		this.notify_users();
	}

	public double[] getPosition() {
		return position;
	}

	public void setPosition(double[] position) throws Exception {
		this.position = position;
		this.notify_users();
	}

	public boolean isState() {
		return state;
	}

	public void setState(boolean state) throws Exception {
		this.state = state;
		this.notify_users();
	}

	public int getId() {
		return id;
	}

	public void setId(int id) throws Exception {
		this.id = id;
		this.notify_users();
	}

	public int getRent_times() {
		return rent_times;
	}

	public void setRent_times(int rent_times) {
		this.rent_times = rent_times;
	}

	public int getReturn_times() {
		return return_times;
	}

	public void setReturn_times(int return_times) {
		this.return_times = return_times;
	}

	public TreeMap<Double, HashMap<Slot, Bicycle_Mech>> getStates_list_mech() {
		return states_list_mech;
	}

	public void setStates_list_mech(
			TreeMap<Double, HashMap<Slot, Bicycle_Mech>> states_list_mech) {
		this.states_list_mech = states_list_mech;
	}

	public TreeMap<Double, HashMap<Slot, Bicycle_Elec>> getStates_list_elec() {
		return states_list_elec;
	}

	public void setStates_list_elec(
			TreeMap<Double, HashMap<Slot, Bicycle_Elec>> states_list_elec) {
		this.states_list_elec = states_list_elec;
	}

	@Override
	public String toString() {
		return "Station [position=" + Arrays.toString(position) + ", state="
				+ state + ", id=" + id + ", type=" + this.getType() + "]";
	}
	
}
