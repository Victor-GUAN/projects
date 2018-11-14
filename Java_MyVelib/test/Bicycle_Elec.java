package test;

public class Bicycle_Elec extends Bicycle{

	/**
	 * Bicycle_Elec represents the electronic bikes which is a subclass of Bicycle
	 * which is defined by the id and the speed.
	 */
	private int id;
	private final double speed = 20;
	
	/**
	 * constructor: Bicycle_Elec is instantiate by the id. 
	 * @param id
	 */
	public Bicycle_Elec(int id){
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
