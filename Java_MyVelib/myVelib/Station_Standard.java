package myVelib;

public class Station_Standard extends Station{
	
	/**
	 * Station_Standard represents the station of type standard which is a subclass of Station
	 * and which is specialized by its type.
	 */
	private String type;
	
	/**
	 * constructor: Station_Standard is instantiate by its id, its position, the places for mech bikes, and the places for elec bikes 
	 * type is standard
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
	public Station_Standard(int id, double x, double y, int N, int M) throws Exception{
		super(id,x,y,N,M);
		this.type = "standard";
	}
	
	/**
	 * getters and setters
	 */
	@Override
	public String getType() {
		return type;
	}
	@Override
	public void setType(String type){
		this.type = type;
	}
	
}
