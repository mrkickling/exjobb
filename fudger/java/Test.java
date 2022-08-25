package locationfudger;

import java.util.Random;
import java.util.concurrent.*;
import java.io.*;  
import java.time.Clock;

public class Test {
	private static final double MIN_LATITUDE = -90D;
	private static final double MAX_LATITUDE = 90D;
	private static final double MIN_LONGITUDE = -180D;
	private static final double MAX_LONGITUDE = 180D;

	private static final float MIN_ACCURACY = 1;
	private static final float MAX_ACCURACY = 100;
	private static final int APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR = 111_000;

	private Random mRandom;

	private static double metersToDegreesLatitude(double distance) {
	    return distance / APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR;
	}

	// requires latitude since longitudinal distances change with distance from equator.
	private static double metersToDegreesLongitude(double distance, double lat) {
	    return distance / APPROXIMATE_METERS_PER_DEGREE_AT_EQUATOR / Math.cos(Math.toRadians(lat));
	}


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


	public static void main(String[] args) throws IOException {
		double lat;
		double lon;

		switch(args[0]) {
			case "preciseToApprox": // Converts a directories precise locations to approximate
				convertAllInDirectoryToApprox("/Users/joakimloxdal/GoogleDrive/KTH/exjobb/exjobb/results/simulated");
				break;
			case "moveAround": // Moves around randomly for x seconds and records approx loc
				moveAround(new Integer(args[1]));
				break;
			case "standStill": // Stands still for x seconds and records approx loc
				standStillForXMilliSeconds(new Integer(args[1]));
				break;
			case "generateGrid": // For diagram in the thesis
				lat = new Double(args[1]);
				lon = new Double(args[2]);
				generateGrid(lat, lon);
				break;
			case "showRandomOffset": // For diagram in the thesis
				lat = new Double(args[1]);
				lon = new Double(args[2]);
				int x = new Integer(args[3]);
				showRandomOffset(lat, lon, x);
				break;
			default:
				break;
		}
	}

	public static Location preciseLocToApprox(double lat, double lon, LocationFudger lf) {
		Location fine = createLocation("test", lat, lon, 2000.0f);
		Location coarse = lf.createCoarse(fine);
		return coarse;
	}

	public static String preciseRouteToApprox(String filepath) throws IOException {
		LocationFudger lf = new LocationFudger(2000.0f);
		FileReader fr = new FileReader(new File(filepath));  
		BufferedReader br = new BufferedReader(fr);
		String line = br.readLine();
		String result = "";
		while (line != null && !line.isEmpty()) {
		    String[] loc = line.split(",");
		    double lat = Double.parseDouble(loc[2]);
		    double lon = Double.parseDouble(loc[3]);
		    Location coarse = preciseLocToApprox(lat, lon, lf);
			result += loc[0] + "," + loc[1] + "," + coarse.getLatitude() + "," + coarse.getLongitude() + "\n";
			line = br.readLine();
		}
		return result;
	}

	public static void convertAllInDirectoryToApprox(String dirname) throws IOException {
		File folder = new File(dirname + "/precise");
		File[] preciseFiles = folder.listFiles();
		System.out.println(preciseFiles.length);

		for (int i = 0; i < preciseFiles.length; i++) {
		  if (preciseFiles[i].isFile()) {
		  	String filename = preciseFiles[i].getName();
		  	String filepath = dirname + "/precise/" + filename;
		    String approx = preciseRouteToApprox(filepath);
		    System.out.println("Writing..");
		    File file = new File(dirname + "/approximate/" + filename);
		    FileOutputStream fos = new FileOutputStream(file);
		    BufferedOutputStream bos = new BufferedOutputStream(fos);
		    byte[] bytes = approx.getBytes();
		    bos.write(bytes);
		    bos.close();
		    fos.close();
		  }
		}
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
				Thread.sleep(1); // sleep 1ms to update the random offset
			} catch(InterruptedException e) {
				System.out.println("Time Error!");
			}
			fine = createLocation("test", fine.getLatitude(), fine.getLongitude(), 2000.0f);
			coarse = lf.createCoarse(fine);
			System.out.println(fine.getLatitude() + ";" + fine.getLongitude() +
				";" + coarse.getLatitude() + ";" + coarse.getLongitude());
		}

	}

	/*
	** Used to generate approximate locations to show how the grid looks like
	** for a diagram in the report.
	*/
	public static void generateGrid(double lat, double lon) {
		LocationFudger lf = new LocationFudger(2000.0f);
		Location start = createLocation("test", lat, lon, 2000.0f);
		for (int i = 0; i < 50; i++) {
			for (int j = 0; j < 50; j++) {
				Location fine = createLocation("test", 
					start.getLatitude() + i * metersToDegreesLatitude(2000.0f), 
					start.getLongitude() + j * metersToDegreesLongitude(2000.0f, start.getLatitude()), 
					2000.0f);
				Location coarse = lf.createCoarse(fine);
				System.out.println(coarse.getLatitude() + "," + coarse.getLongitude());
			}

		}
	}

	public static void showRandomOffset(double lat, double lon, int x) {
		Location fine = createLocation("test", lat, lon, 2000.0f);
		LocationFudger lf = new LocationFudger(2000.0f);
		Location coarse = lf.createCoarse(fine);
		System.out.println(fine.getLatitude() + "," + fine.getLongitude());

		for (int i = 0; i < x; i++) {
			try{
				Thread.sleep(1);
			} catch(InterruptedException e) {
				System.out.println("Time Error!");
			}
			fine = createLocation("test", fine.getLatitude(), fine.getLongitude(), 2000.0f);
			coarse = lf.createCoarse(fine);
			double offset[] = lf.getOffset(fine);
			System.out.println(offset[0] + "," + offset[1]);
		}

	}


}