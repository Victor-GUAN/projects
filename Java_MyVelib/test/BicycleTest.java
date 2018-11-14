package test;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

public class BicycleTest {

	Bicycle b = new Bicycle_Elec(0);
	
	@Before
	public void setUp() throws Exception {
	}

	@Test
	public void testCount_bike_time() throws Exception {
		System.out.println(b.count_bike_time(new Station_Plus(1,0,0,10,5), new Station_Standard(2,30,40,5,5)));
		assertEquals((double)2.5,b.count_bike_time(new Station_Plus(1,0,0,10,5), new Station_Standard(2,30,40,5,5)),0.01);
	}

}
