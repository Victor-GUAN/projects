package test;

public class Bicycle_Mech extends Bicycle{
	
	/**
	 * Bicycle_Mech represents the mechanical bikes which is a subclass of Bicycle
	 * which is defined by the id and the speed.
	 */
	private int id;
	private final double speed = 15;
	
	/**
	 * constructor: Bicycle_Mech is instantiate by the id. 
	 * @param id
	 */
	public Bicycle_Mech(int id){
		super(id);
		this.id = id;
	}
	
	/**
	 * getters and setters
	 */
	@Override
	public int getId() {
		return id;
	}
	@Override
	public void setId(int id) {
		this.id = id;
	}
	@Override
	public double getSpeed() {
		return speed;
	}

}
