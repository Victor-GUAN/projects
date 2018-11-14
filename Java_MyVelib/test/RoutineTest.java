package test;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

public class RoutineTest {

	@Before
	public void setUp() throws Exception {
	}

	@Test
	public void testCount_time() throws Exception{
		Station s1 = new Station_Standard(1,0,0,5,5);
		Station s2 = new Station_Plus(2,30,40,10,10);
		Routine routine = new Routine(0,0,30,50,s1,s2);

		assertEquals(5.833,routine.count_time(new Bicycle_Mech(0)),0.01);
	}

}
