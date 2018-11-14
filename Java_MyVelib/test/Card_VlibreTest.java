package test;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

public class Card_VlibreTest {
	Card card = new Card_Vlibre();
	
	@Before
	public void setUp() throws Exception {
	}

	@Test
	public void testPrice() throws Exception{
		Station s1 = new Station_Standard(1,0,0,5,5);
		Station s2 = new Station_Plus(2,30,40,10,10);
		Routine routine = new Routine(0,0,30,50,s1,s2);
		assertEquals(9.0,card.price(routine, new Bicycle_Elec(0)),0.001);
	}

}
