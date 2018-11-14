package test;

public class Bank_Card {
	
	/**
	 * we use the amount of money in the bank card, the owner (subscriber), and the id
	 * to define a bank card
	 */
	private double money;
	private User owner;
	private int id;
	
	/**
	 * constructor: bank card are used to activate a bike and pay for the trip
	 * @param money
	 * @param owner
	 * @param id
	 */
	public Bank_Card(double money, User owner, int id){
		this.money = money;
		this.owner = owner;
		this.id = id;
	}
	
	/**
	 * the function check is used to check whether there is enough to pay for the trip in the account
	 * @param m
	 */
	public void check(double m) throws Exception{
		if(this.money<=m){System.out.println("No enough money!");throw new Exception("NO MONEY");}
	}

	/**
	 * getters and setters
	 */
	public double getMoney() {
		return money;
	}

	public void setMoney(double money) {
		this.money = money;
	}

	public User getOwner() {
		return owner;
	}

	public void setOwner(User owner) {
		this.owner = owner;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

}
