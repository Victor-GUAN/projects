package myVelib;

public class Slot {
	
	/**
	 * Slot represent the slot class in a station place which is defined by its id in a relative station
	 */
	private int id;
	
	/**
	 * constructor: Slot is instantiate by its id.
	 * @param id
	 */
	public Slot(int id){
		super();
		this.id = id;
	}

	/**
	 * getters and setters
	 */
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}
}
