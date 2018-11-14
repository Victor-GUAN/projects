package myVelib;

import java.util.Arrays;

public class Routine {
	
	/**
	 * Routine class represent the routine to choose with respect to a certain distance policy
	 * It is represented by the start point, the source station, the destination station, and the end point.
	 */
	/**
	 * WALK_SPEED: speed of the walker
	 * start: the start position of the routine
	 * end: the end position of the routine
	 * source: the source station to take the bike
	 * destination: the destination station to park the bike
	 */
	private final double WALK_SPEED = 4;
	
	private double[] start;
	private double[] end;
	private Station source;
	private Station destination;
	
	/**
	 * the function count_time is used to calculate the whole time spent on this routine with a certain type of bicycle.
	 * it includes the time of walking from start to source, the time of biking from source to destination, and the time of walking from destination to end.
	 * @param b
	 */
	public double count_time(Bicycle b){
		double s = Math.sqrt(Math.pow(this.start[0]-this.source.getPosition()[0],2) + Math.pow(this.start[1]-this.source.getPosition()[1],2)) / WALK_SPEED;
		double e = Math.sqrt(Math.pow(this.end[0]-this.destination.getPosition()[0],2) + Math.pow(this.end[1]-this.destination.getPosition()[1],2)) / WALK_SPEED;
		double i = Math.sqrt(Math.pow(this.source.getPosition()[0]-this.destination.getPosition()[0],2) + Math.pow(this.source.getPosition()[1]-this.destination.getPosition()[1],2)) / b.getSpeed();              
		
		return s+e+i;
	}
	
	/**
	 * the toString() function overrode.
	 */
	@Override
	public String toString() {
		return "Routine [start=" + Arrays.toString(start) + ", end="
				+ Arrays.toString(end) + ", source=" + source.toString()
				+ ", destination=" + destination.toString() + "]";
	}

	/**
	 * constructor: Routine is instantiate by the start point, the source station, the destination station, and the end point.
	 * @param x1
	 * @param y1
	 * @param x2
	 * @param y2
	 * @param source
	 * @param destination
	 */
	public Routine(double x1, double y1, double x2, double y2, Station source, Station destination){
		this.start = new double[]{x1,y1};
		this.end = new double[]{x2,y2};
		this.source = source;
		this.destination = destination;
	}

	/**
	 * getters and setters
	 */
	public double[] getStart() {
		return start;
	}

	public void setStart(double[] start) {
		this.start = start;
	}

	public double[] getEnd() {
		return end;
	}

	public void setEnd(double[] end) {
		this.end = end;
	}

	public Station getSource() {
		return source;
	}

	public void setSource(Station source) {
		this.source = source;
	}

	public Station getDestination() {
		return destination;
	}

	public void setDestination(Station destination) {
		this.destination = destination;
	}

	public double getWALK_SPEED() {
		return WALK_SPEED;
	}
	
	
}
