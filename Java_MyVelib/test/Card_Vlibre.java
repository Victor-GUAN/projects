package test;

public class Card_Vlibre extends Card{
	
	/**
	 * Card_Vlibre represent the velib card of type Vlibre which is a subclass of Card
	 * and which is defined by the credits earned by this card.
	 */
	private double credits;
	
	/**
	 * constructor: Card_Vlibre is instantiate by default, and this credits is set 0 at first. 
	 */
	public Card_Vlibre(){super();this.credits = 0;}
	
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
		
		if(b instanceof Bicycle_Mech){
			if(time <= 1){price = 0;}
			else{price = time-1;}
		}
		if(b instanceof Bicycle_Elec){
			if(time <= 1){price = time;}
			else{price = 2*(time-1)+1;}
		}
	
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
