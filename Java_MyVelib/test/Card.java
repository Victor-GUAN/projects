package test;

public abstract class Card{
	
	/**
	 * Card_Vmax represent the velib card of generic type which is the parent class of Card_Vlibre and Card_Vmax
	 * and which is defined by the credits earned by this card.
	 */
	private double credits;
	
	/**
	 * abstract function price to calculate the money spent on a routine, which is to be overload by its different subclasses.
	 * @param routine
	 * @param b
	 */
	public abstract double price(Routine routine, Bicycle b);
	
	/**
	 * constructor: Card is instantiate by default, and this credits is set 0 at first. 
	 */
	public Card(){
		this.credits = 0;
	}
	
	/**
	 * getters and setters
	 */
	public double getCredits() {
		return credits;
	}
	public void setCredits(double credits) {
		this.credits = credits;
	}
	
	
}
