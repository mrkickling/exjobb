package locationfudger;

import java.util.Random;
import java.util.concurrent.*;
import java.time.Clock;

public class Test {
	private static final double MIN_LATITUDE = -90D;
	private static final double MAX_LATITUDE = 90D;
	private static final double MIN_LONGITUDE = -180D;
	private static final double MAX_LONGITUDE = 180D;

	private static final float MIN_ACCURACY = 1;
	private static final float MAX_ACCURACY = 100;

	private Random mRandom;

	public static Location move(Location location) {
		location.setLatitude(location.getLatitude() + (1 + 1 * Math.random() - 1) / 100);
		location.setLongitude(location.getLongitude() + (1 + 1 * Math.random() - 1) / 100);
		return location;
	}

	public static Location moveFront(Location location) {
		location.setLatitude(location.getLatitude() + 1 / 1000);
		location.setLongitude(location.getLongitude() + 1 / 1000);
		return location;
	}

	public static Location moveBack(Location location) {
		location.setLatitude(location.getLatitude() - 1 / 1000);
		location.setLongitude(location.getLongitude() - 1 / 1000);
		return location;
	}

	public static Location createLocation(String provider, double latitude, double longitude,
	        float accuracy) {
	    Location location = new Location(provider);
	    location.setLatitude(latitude);
	    location.setLongitude(longitude);
	    location.setAccuracy(accuracy);
	    location.setTime(System.currentTimeMillis());
	    location.setElapsedRealtimeNanos(Clock.systemDefaultZone().instant().getNano());
	    return location;
	}

	public static Location createLocation(String provider, Random random) {
		return createLocation(provider,
		        MIN_LATITUDE + random.nextDouble() * (MAX_LATITUDE - MIN_LATITUDE),
		        MIN_LONGITUDE + random.nextDouble() * (MAX_LONGITUDE - MIN_LONGITUDE),
		        2000.0f);
	}


	public static void main(String[] args) {
		moveAround(1000);
	}

	public static void moveAround(int x) {
		Location fine = createLocation("test", new Random());
		LocationFudger lf = new LocationFudger(2000.0f);
		Location coarse = lf.createCoarse(fine);
		// System.out.println(fine.getLatitude() + ": " + lf.roundLat(fine.getLatitude()));

		for (int i = 0; i < x; i++) {
			fine = createLocation("test", fine.getLatitude(), fine.getLongitude(), 2000.0f);
			fine = move(fine);
			coarse = lf.createCoarse(fine);
			System.out.println(fine.getLatitude() + ";" + fine.getLongitude() +
				";" + coarse.getLatitude() + ";" + coarse.getLongitude());
		}

	}

	public static void standStillForXMilliSeconds(int x) {
		Location fine = createLocation("test", new Random());
		LocationFudger lf = new LocationFudger(2000.0f);
		Location coarse = lf.createCoarse(fine);

		for (int i = 0; i < x; i++) {
			try{
				Thread.sleep(1);
			} catch(InterruptedException e) {
				System.out.println("Time Error!");
			}
			fine = createLocation("test", fine.getLatitude(), fine.getLongitude(), 2000.0f);
			coarse = lf.createCoarse(fine);
			System.out.println(fine.getLatitude() + ";" + fine.getLongitude() +
				";" + coarse.getLatitude() + ";" + coarse.getLongitude());
		}

	}

	public static void showRandomOffset(int x) {
		Location fine = createLocation("test", new Random());
		LocationFudger lf = new LocationFudger(2000.0f);
		Location coarse = lf.createCoarse(fine);

		for (int i = 0; i < x; i++) {
			try{
				Thread.sleep(1);
			} catch(InterruptedException e) {
				System.out.println("Time Error!");
			}
			fine = createLocation("test", fine.getLatitude(), fine.getLongitude(), 2000.0f);
			coarse = lf.createCoarse(fine);
			double offset[] = lf.getOffset(fine);
			System.out.println(fine.getLatitude() + ";" + fine.getLongitude() +
				";" + offset[0] + ";" + offset[1]);
		}

	}


}