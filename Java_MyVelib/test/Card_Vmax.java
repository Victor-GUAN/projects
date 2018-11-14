package test;

public class Card_Vmax extends Card{
	
	/**
	 * Card_Vmax represent the velib card of type Vmax which is a subclass of Card
	 * and which is defined by the credits earned by this card.
	 */
	private double credits;
	
	/**
	 * constructor: Card_Vmax is instantiate by default, and this credits is set 0 at first. 
	 */
	public Card_Vmax(){super();this.credits = 0;}
	
	/**
	 * the function overrode price is used to calculated the price spent on a routine, it's determined by the Routine to take, the type of the bike,
	 * its credits remaining, and the policy of payment for this type of card defined in the subject.
	 * @param routine
	 * @param b
	 */
	@Override
	public double price(Routine routine, Bicycle b){
		double price = 0;
		double time = 0;
		if(routine.count_time(b) <= this.getCredits()/60){time = 0;this.setCredits(this.getCredits()-routine.count_time(b));}                           
		if(routine.count_time(b) > this.getCredits()/60){time = routine.count_time(b) - this.getCredits()/60;this.setCredits(0);}	
		
		if(time <= 1){price = 0;}
		if(time > 1){price = time-1;}
		return price;
	}
	
	/**
	 * getters and setters
	 */
	public double getCredits() {
		return credits;
	}
	public void setCredits(double credits) {
		this.credits = credits;
	};
}
