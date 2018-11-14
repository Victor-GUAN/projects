package test;

import static org.junit.Assert.*;

import java.util.ArrayList;

import org.junit.Before;
import org.junit.Test;

public class UserTest {

	@Before
	public void setUp() throws Exception {
	}

	@Test
	public void testCount_walk_time() {
		User user = new User("user",0,0,0,null);
		assertEquals(1.25,user.count_walk_time(3,4),0.01);
	}

	@Test
	public void testPay() throws Exception{
		Card card_vlibre = new Card_Vlibre();
		User user = new User("user",0,10,0,card_vlibre);
		Bank_Card bc = new Bank_Card(200,user,0);
		Station s1 = new Station_Standard(1,0,0,5,5);
		Station s2 = new Station_Plus(2,30,40,10,10);
		Routine routine = new Routine(0,0,30,50,s1,s2);
		
		assertEquals(9.0,user.pay(routine, new Bicycle_Elec(0), bc),0.01);
	}

	@Test
	public void testTake() throws Exception{
		Station s_1_plus = new Station_Plus(1,2,0,5,10);
		for(Slot s: s_1_plus.getPlaces_mech().keySet())
		{for(int i=11;i<=13;i++){if(s.getId()+10==i){s_1_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_1_plus.getPlaces_elec().keySet())
		{for(int i=11;i<=16;i++){if(s.getId()+10==i){s_1_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		Station s_2_plus = new Station_Plus(2,0,2,10,5);
		for(Slot s: s_2_plus.getPlaces_mech().keySet())
		{for(int i=21;i<=25;i++){if(s.getId()+20==i){s_2_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_2_plus.getPlaces_elec().keySet())
		{for(int i=21;i<=24;i++){if(s.getId()+20==i){s_2_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		Station s_3_standard = new Station_Standard(3,2,2,10,10);
		for(Slot s: s_3_standard.getPlaces_mech().keySet())
		{for(int i=31;i<=37;i++){if(s.getId()+30==i){s_3_standard.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_3_standard.getPlaces_elec().keySet())
		{for(int i=31;i<=36;i++){if(s.getId()+30==i){s_3_standard.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		//reverse order
		Station s_4_plus = new Station_Plus(4,0,0,5,5);
		for(Slot s: s_4_plus.getPlaces_mech().keySet())
		{for(int i=41;i<=42;i++){if(s.getId()+40==i){s_4_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_4_plus.getPlaces_elec().keySet())
		{for(int i=41;i<=43;i++){if(s.getId()+40==i){s_4_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}		

		ArrayList<Station> stations = new ArrayList<Station>();
		stations.add(s_1_plus);stations.add(s_2_plus);stations.add(s_3_standard);stations.add(s_4_plus);
		Plan plan = new Plan(stations);
		
        User admin = new User("admin",0,0,0,null);
        Bank_Card bc_0 = new Bank_Card(1000,admin,0);
        admin.check_station(s_4_plus);
        admin.find_routine(3,3,plan,"uniform",new Bicycle_Mech(10));
        admin.choose_routine(admin.getLast_routine());

        admin.take(s_4_plus, new Bicycle_Mech(10), bc_0);

        assertTrue(admin.getBicycle().getId()- 4*10 > 0);
		
	}

	@Test
	public void testPark() throws Exception{
		Station s_1_plus = new Station_Plus(1,2,0,5,10);
		for(Slot s: s_1_plus.getPlaces_mech().keySet())
		{for(int i=11;i<=13;i++){if(s.getId()+10==i){s_1_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_1_plus.getPlaces_elec().keySet())
		{for(int i=11;i<=16;i++){if(s.getId()+10==i){s_1_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		Station s_2_plus = new Station_Plus(2,0,2,10,5);
		for(Slot s: s_2_plus.getPlaces_mech().keySet())
		{for(int i=21;i<=25;i++){if(s.getId()+20==i){s_2_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_2_plus.getPlaces_elec().keySet())
		{for(int i=21;i<=24;i++){if(s.getId()+20==i){s_2_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		
		Station s_3_standard = new Station_Standard(3,2,2,10,10);
		for(Slot s: s_3_standard.getPlaces_mech().keySet())
		{for(int i=31;i<=37;i++){if(s.getId()+30==i){s_3_standard.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_3_standard.getPlaces_elec().keySet())
		{for(int i=31;i<=36;i++){if(s.getId()+30==i){s_3_standard.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}
		//reverse order
		Station s_4_plus = new Station_Plus(4,0,0,5,5);
		for(Slot s: s_4_plus.getPlaces_mech().keySet())
		{for(int i=41;i<=42;i++){if(s.getId()+40==i){s_4_plus.getPlaces_mech().put(s, new Bicycle_Mech(i));}}}
		for(Slot s: s_4_plus.getPlaces_elec().keySet())
		{for(int i=41;i<=43;i++){if(s.getId()+40==i){s_4_plus.getPlaces_elec().put(s, new Bicycle_Elec(i));}}}		

		ArrayList<Station> stations = new ArrayList<Station>();
		stations.add(s_1_plus);stations.add(s_2_plus);stations.add(s_3_standard);stations.add(s_4_plus);
		Plan plan = new Plan(stations);
		
        User admin = new User("admin",0,0,0,null);
        Bank_Card bc_0 = new Bank_Card(1000,admin,0);
        admin.check_station(s_4_plus);
        admin.find_routine(3,3,plan,"uniform",new Bicycle_Mech(10));
        admin.choose_routine(admin.getLast_routine());
        
        int a = s_3_standard.count_mech();
        admin.take(s_4_plus, new Bicycle_Mech(10), bc_0);
        admin.park(s_3_standard);
        int b = s_3_standard.count_mech();
        assertEquals(1,b-a);
	}

	@Test
	public void testChoose_routine() throws Exception{
		Station s1 = new Station_Standard(1,0,0,5,5);
		Station s2 = new Station_Plus(2,30,40,10,10);
		Routine routine = new Routine(0,0,30,50,s1,s2);
		
		User admin = new User("admin",0,0,0,null);

        admin.choose_routine(routine);
        
        assertEquals(routine,admin.getLast_routine());
		
	}

}
