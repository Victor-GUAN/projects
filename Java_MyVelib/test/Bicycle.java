package test;

public abstract class Bicycle {
	
	/**
	 * The general class Bicycle represent the bikes which is a parent class of Bicycle_Mech and Bicycle_Elec
	 * and which is defined by the id and the speed, the user who uses this bike, the bank card to pay for,
	 * and the statistical parameters number of rides of the total time spent on this bike.
	 */
	private int id;
	private double speed;
	private User user;
	private Bank_Card bank_card_to_use;
	private int number_rides;
	private double total_time_spent;
	
	/**
	 * constructor: Bicycle_Mech is instantiate by the id, and other attributes are instantiate by default.
	 * @param id
	 */
	public Bicycle(int id){
		this.id = id;
		this.number_rides = 0;
		this.total_time_spent = 0;
		this.user = null;
	}
	
	/**
	 * the function count_bike_time is used to calculate the time spent on this bike between two bike stations
	 * @param s
	 * @param e
	 */
	public double count_bike_time(Station s, Station e){
		double i;
		i = Math.sqrt(Math.pow(s.getPosition()[0]-e.getPosition()[0],2) + Math.pow(s.getPosition()[1]-e.getPosition()[1],2)) / this.getSpeed();                          
		this.setTotal_time_spent(this.getTotal_time_spent()+i);
		return i;
	}
	
	/**
	 * getters and setters
	 */
	public int getNumber_rides() {
		return number_rides;
	}

	public void setNumber_rides(int number_rides) {
		this.number_rides = number_rides;
	}

	public double getTotal_time_spent() {
		return total_time_spent;
	}

	public void setTotal_time_spent(double total_time_spent) {
		this.total_time_spent = total_time_spent;
	}

	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public double getSpeed() {
		return speed;
	}
	public void setSpeed(double speed) {
		this.speed = speed;
	}

	public User getUser() {
		return user;
	}

	public void setUser(User user) {
		this.user = user;
	}

	public Bank_Card getBank_card_to_use() {
		return bank_card_to_use;
	}

	public void setBank_card_to_use(Bank_Card bank_card_to_use) {
		this.bank_card_to_use = bank_card_to_use;
	}
	
}
