package myVelib;

import java.util.Map;
import java.util.TreeMap;


public class User extends Thread{
	
	/**
	 * User class represents the users who use this velib system and are as well as observers for all the stations in the plan. 
	 */
	/**
	 * WALK_SPEED: walking speed of user
	 * name: name of the user
	 * bicycle: bike to ride for this user                               
	 * last_routine: the routine this user has decided to take
	 * id: id of this user
	 * position: position of the user
	 * card: the velib card the user possesses
	 * neighbors_of_location: collection of stations around a certain location, which is ordered by the distance to the location. 
	 */
	private final double WALK_SPEED = 4;
	
	private String name;
	private Bicycle bicycle;
	private Routine last_routine;
	private int id;
	private double[] position;
	private Card card;
	private TreeMap<Double,Station> neighbors_of_location;
	
	/**
	 * constructor: User is instantiate by its name, its id, its position, and the velib card he has.
	 * x: the first coordinate of its position
	 * y: the second coordinate of its position
	 * card: velib card
	 * @param name
	 * @param id
	 * @param x: the first coordinate of its position
	 * @param y: the second coordinate of its position
	 * @param card: velib card
	 */
	public User(String name, int id, double x, double y, Card card){
		this.name = name;
		this.id = id;
		this.position = new double[]{x,y};
		this.card = card;
		this.bicycle = null;
		this.last_routine = null;
	}
	
	/**
	 * the function count_walk_time is used to calculate the time spent on walking between the current position of the user and the chosen location.
	 * x: the first coordinate of the chosen location
	 * y: the second coordinate of the chosen location
	 * @param x
	 * @param y
	 */
	public double count_walk_time(double x, double y){
		return Math.sqrt(Math.pow(x-this.getPosition()[0],2) + Math.pow(y-this.getPosition()[1],2)) / this.WALK_SPEED;	
	}
	
	/**
	 * the synchronized function pay is used to realize the functionality of payment and can calculate the price spent on the routine.
	 * routine: the routine to pay for
	 * b: the bike used in the routine to pay for
	 * bank_card: the bank_card used to pay for the money.
	 * @param routine
	 * @param b
	 * @param bank_card
	 */
	public synchronized double pay(Routine routine, Bicycle b, Bank_Card bank_card) throws Exception{
		if(!routine.getDestination().isState()){System.out.println("offline - out of order!");throw new Exception("OFFLINE");}
		double price = 0;
		if(routine.getDestination()==null || routine.getEnd()==null || routine.getSource()==null || routine.getStart()==null){System.out.println("no routine to pay");}          
		if(this.card == null){
			if(b instanceof Bicycle_Mech){price = routine.count_time(b);}
			if(b instanceof Bicycle_Elec){price = 2*routine.count_time(b);}
		}
		if(this.card != null){price = this.card.price(routine, b);}
		if(bank_card.getOwner().equals(this)){bank_card.check(price);bank_card.setMoney(bank_card.getMoney()-price);}
		if(!bank_card.getOwner().equals(this)){System.out.println("choose a right bank card");}
		return price;
	}
	
	/**
	 * the synchronized function take is used to realize the action of taking a bike at certain station for the user, and this user's bicycle attribute will be arranged by this taken bike.
	 * s: the source station to take bikes
	 * b: the type of bike to take
	 * bank_card: the bank_card used to activate of taking action
	 * @param s
	 * @param b
	 * @param bank_card
	 */
	public synchronized void take(Station s, Bicycle b, Bank_Card bank_card) throws Exception{
		if(!s.equals(this.last_routine.getSource())){System.out.println("CHOOSE THE STATION OF YOUR ROUTINE");throw new Exception("WRONG STATION");}
		if(this.bicycle!=null){System.out.println("Already Got a Bicycle");throw new Exception("ALREADY GOT A BIKE");}
		s.remove_user(this);
		if(!s.isState()){System.out.println("offline - out of order!");throw new Exception("OFFLINE");}
		this.setPosition(s.getPosition());
		if(b instanceof Bicycle_Mech){
			if(s.count_mech() == 0){System.out.println("no more mech bicycles available");}
			else{
				for(Map.Entry<Slot,Bicycle_Mech> me:s.getPlaces_mech().entrySet()){
					if(me.getValue()!=null){
						this.bicycle = me.getValue();s.getPlaces_mech().put(me.getKey(), null);
						s.setRent_times(s.getRent_times()+1);s.notify_users();
						this.bicycle.setNumber_rides(this.bicycle.getNumber_rides()+1);
						if(bank_card.getOwner().equals(this)){this.bicycle.setBank_card_to_use(bank_card);}
						if(!bank_card.getOwner().equals(this)){System.out.println("choose a right bank card");throw new Exception("WRONG BANK CARD USER");}	
						this.bicycle.setUser(this);
						this.setPosition(s.getPosition());
						break;
					}
				}
			}
		}
		if(b instanceof Bicycle_Elec){
			if(s.count_elec() == 0){System.out.println("no more elec bicycles available");}
			else{
				for(Map.Entry<Slot,Bicycle_Elec> me:s.getPlaces_elec().entrySet()){
					if(me.getValue()!=null){
						this.bicycle = me.getValue();s.getPlaces_elec().put(me.getKey(), null);
						s.setRent_times(s.getRent_times()+1);s.notify_users();
						this.bicycle.setNumber_rides(this.bicycle.getNumber_rides()+1);
						if(bank_card.getOwner().equals(this)){this.bicycle.setBank_card_to_use(bank_card);}
						if(!bank_card.getOwner().equals(this)){System.out.println("choose a right bank card");throw new Exception("WRONG BANK CARD USER");}	
						this.bicycle.setUser(this);
						this.setPosition(s.getPosition());
						break;
					}
				}
			}
		}
	}
	
	/**
	 * the synchronized function park is used to realize the action of parking a bike at certain station for the user, 
	 * and this user's bicycle attribute will be removed after parking action,
	 * and the payment action will be executed automatically while parking.
	 * s: the destination station to park bikes
	 * @param s
	 */
	public synchronized void park(Station s) throws Exception{
		if(!s.equals(this.last_routine.getDestination())){System.out.println("CHOOSE THE STATION OF YOUR ROUTINE");throw new Exception("WRONG STATION");}
		s.remove_user(this);
		if(!s.isState()){System.out.println("offline - out of order!");throw new Exception("OFFLINE");}
		if(this.bicycle == null){System.out.println("no bicycle to park");}
		this.bicycle.setTotal_time_spent(this.bicycle.getTotal_time_spent()+this.bicycle.count_bike_time(this.last_routine.getSource(), this.last_routine.getDestination()));
		this.setPosition(s.getPosition());
		if(this.bicycle instanceof Bicycle_Mech){
			if(s.getPlaces_mech().size()-s.count_mech() == 0){System.out.println("no more mech bicycle slots available");}
			else{
				if(s instanceof Station_Plus && this.card!=null){this.card.setCredits(this.card.getCredits()+5);}
				for(Map.Entry<Slot,Bicycle_Mech> me:s.getPlaces_mech().entrySet()){
					if(me.getValue()==null){
						s.getPlaces_mech().put(me.getKey(), (Bicycle_Mech)this.bicycle);s.setReturn_times(s.getReturn_times()+1);
						if(this.card!=null){System.out.println(this.getUserName() + " Credits remaining: " + this.getCard().getCredits());}
						System.out.println(this.getUserName() + " PAY: " + this.pay(this.last_routine, this.bicycle, this.bicycle.getBank_card_to_use()));
						this.last_routine = null;
						s.notify_users();
						this.bicycle.setUser(null);
						this.bicycle.setBank_card_to_use(null);
						this.bicycle = null;
						this.setPosition(s.getPosition());
						break;
					}    
				}
			}
		}
		if(this.bicycle instanceof Bicycle_Elec){
			if(s.getPlaces_elec().size()-s.count_elec() == 0){System.out.println("no more elec bicycle slots available");}
			else{
				if(s instanceof Station_Plus && this.card!=null){this.card.setCredits(this.card.getCredits()+5);}
				for(Map.Entry<Slot,Bicycle_Elec> me:s.getPlaces_elec().entrySet()){
					if(me.getValue()==null){
						s.getPlaces_elec().put(me.getKey(), (Bicycle_Elec)this.bicycle);s.setReturn_times(s.getReturn_times()+1);
						if(this.card!=null){System.out.println(this.getUserName() + " Credits remaining: " + this.getCard().getCredits());}
						System.out.println(this.getUserName() + " PAY: " + this.pay(this.last_routine, this.bicycle,this.bicycle.getBank_card_to_use()));
						this.last_routine = null;
						s.notify_users();
						this.bicycle.setUser(null);
						this.bicycle.setBank_card_to_use(null);
						this.bicycle = null;
						this.setPosition(s.getPosition());
						break;
					}    
				}
			}
		}
	}
	
	/**
	 * the synchronized function find_routine is used to find out the best suited routine between the current location and the chosen location, with respect to a certain policy for ride planning
	 * the user can choose the policies of shortest path, fastest path, avoid ¡°plus¡± stations, prefer ¡°plus¡± stations, and preservation of uniformity of bicycles distribution amongst stations.       
	 * x: the first coordinate the chosen location
	 * y: the second coordinate the chosen location
	 * plan: the plan in which to find the best suited routine
	 * path: the policy for ride planning
	 * b: the type of bicycle to take for this routine
	 * @param x
	 * @param y
	 * @param plan
	 * @param path
	 * @param b
	 */
	public synchronized Routine find_routine(double x, double y, Plan plan, String path, Bicycle b) throws Exception{
		if(path.equals("shortest")){this.last_routine = plan.find_routine_shortest(this.position, new double[]{x,y});}
		else if(path.equals("fastest")){this.last_routine = plan.find_routine_fastest(this.position, new double[]{x,y},b);}                         
		else if(path.equals("avoid_plus")){this.last_routine = plan.find_routine_avoid_plus(this.position, new double[]{x,y});}
		else if(path.equals("prefer_plus")){this.last_routine = plan.find_routine_prefer_plus(this.position, new double[]{x,y});}
		else if(path.equals("uniform")){this.last_routine = plan.find_routine_uniform(this.position, new double[]{x,y},b);}
		else{System.out.println("choose the right way of path");return null;}
		System.out.println(this.getUserName() + " - the routine shown: "+ this.last_routine.toString());
		return this.last_routine;
	}
	
	/**
	 * the synchronized function choose_routine is used to decide which routine to take for the trip.
	 * the user's last_routine attribute will be arranged by this routine variable.
	 * routine: the decided taken routine
	 * @param routine
	 */
	public synchronized void choose_routine(Routine routine) throws Exception{
		routine.getSource().add_user(this);
		routine.getDestination().add_user(this);
		this.last_routine = routine;
	}
	
	/**
	 * the function check_plan is used to obtain the collection of stations around a certain location, which is ordered by the distance to the location. 
	 * the user's neighbors_of_location attribute will be arranged by this collection
	 * plan: the plan in which to find out the collection
	 * x: the first coordinate the chosen location
	 * y: the second coordinate the chosen location
	 * @param plan
	 * @param x
	 * @param y
	 */
	public void check_plan(Plan plan, double x, double y){
		this.neighbors_of_location = new TreeMap<Double,Station>();
		for(Station s: plan.getStations()){
			this.neighbors_of_location.put(Math.sqrt(Math.pow(x-s.getPosition()[0],2) + Math.pow(y-s.getPosition()[1],2)),s);
		}
		System.out.println("Neighbors of the location ["+x+", "+y+"]: " + this.neighbors_of_location.toString());
	}
	
	/**
	 * the function check_station is used to check out the current detailed info of a chosen station
	 * s: the station to check out the situation
	 * @param s
	 */
	public void check_station(Station s) throws Exception{
		s.add_user(this);
		System.out.println("Station State: " + s.isState());
		System.out.println("Station Id: " + s.getId());
		System.out.println("Station Type: " + s.getType());
		System.out.println("Station Position: " + s.getPosition()[0] + " " + s.getPosition()[1]);
		System.out.println("Mech Slots Available: " + (s.getPlaces_mech().size()-s.count_mech()));
		System.out.println("Elec Slots Available: " + (s.getPlaces_elec().size()-s.count_elec()));
		System.out.println("Mech Bicycles Available: " + (s.count_mech()));
		System.out.println("Elec Bicycles Available: " + (s.count_elec()));
	}
	
	/**
	 * the function deconnect_station is used to cut off connections to a certain station
	 * s: the station to cut off connections.
	 * @param s
	 */
	public void deconnect_station(Station s) throws Exception{
		s.remove_user(this);
	}

	/**
	 * getters and setters
	 */
	public String getUserName() {
		return name;
	}

	public void setUserName(String name) {
		this.name = name;
	}

	public Bicycle getBicycle() {
		return bicycle;
	}

	public void setBicycle(Bicycle bicycle) {
		this.bicycle = bicycle;
	}

	public Routine getLast_routine() {
		return last_routine;
	}

	public void setLast_routine(Routine last_routine) {
		this.last_routine = last_routine;
	}

	public int getUserId() {
		return id;
	}

	public void setUserId(int id) {
		this.id = id;
	}

	public double[] getPosition() {
		return position;
	}

	public void setPosition(double[] position) {
		this.position = position;
	}

	public Card getCard() {
		return card;
	}

	public void setCard(Card card) {
		this.card = card;
	}
	
}
