/*
 * Copyright (C) 2020 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package locationfudger;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import java.util.function.Predicate;

/**
 * A location result representing a list of locations, ordered from earliest to latest.
 *
 * @hide
 */
public final class LocationResult {

    /**
     * Creates a new LocationResult from the given locations, making a copy of each location.
     * Locations must be ordered in the same order they were derived (earliest to latest).
     */
    public static LocationResult create(List<Location> locations) {
        ArrayList<Location> locationsCopy = new ArrayList<>(locations.size());
        for (Location location : locations) {
            locationsCopy.add(new Location(Objects.requireNonNull(location)));
        }
        return new LocationResult(locationsCopy);
    }

    /**
     * Creates a new LocationResult from the given locations, making a copy of each location.
     * Locations must be ordered in the same order they were derived (earliest to latest).
     */
    public static LocationResult create(Location... locations) {
        ArrayList<Location> locationsCopy = new ArrayList<>(locations.length);
        for (Location location : locations) {
            locationsCopy.add(new Location(Objects.requireNonNull(location)));
        }
        return new LocationResult(locationsCopy);
    }

    /**
     * Creates a new LocationResult that takes ownership of the given locations without copying
     * them. Callers must ensure the given locations are never mutated after this method is called.
     * Locations must be ordered in the same order they were derived (earliest to latest).
     */
    public static LocationResult wrap(List<Location> locations) {
        return new LocationResult(new ArrayList<>(locations));
    }

    /**
     * Creates a new LocationResult that takes ownership of the given locations without copying
     * them. Callers must ensure the given locations are never mutated after this method is called.
     * Locations must be ordered in the same order they were derived (earliest to latest).
     */
    public static LocationResult wrap(Location... locations) {
        ArrayList<Location> newLocations = new ArrayList<>(locations.length);
        for (Location location : locations) {
            newLocations.add(Objects.requireNonNull(location));
        }
        return new LocationResult(newLocations);
    }

    private final ArrayList<Location> mLocations;

    private LocationResult(ArrayList<Location> locations) {
        mLocations = locations;
    }

    /**
     * Throws an IllegalArgumentException if the ordering of locations does not appear to generally
     * be from earliest to latest, or if any individual location is incomplete.
     *
     * @hide
     */
    public LocationResult validate() {
        long prevElapsedRealtimeNs = 0;
        final int size = mLocations.size();
        for (int i = 0; i < size; ++i) {
            Location location = mLocations.get(i);
            if (!location.isComplete()) {
                throw new IllegalArgumentException(
                        "incomplete location at index " + i + ": " + mLocations);
            }
            if (location.getElapsedRealtimeNanos() < prevElapsedRealtimeNs) {
                throw new IllegalArgumentException(
                        "incorrectly ordered location at index " + i + ": " + mLocations);
            }
            prevElapsedRealtimeNs = location.getElapsedRealtimeNanos();
        }

        return this;
    }

    /**
     * Returns the latest location in this location result, ie, the location at the highest index.
     */
    public Location getLastLocation() {
        return mLocations.get(mLocations.size() - 1);
    }

    /**
     * Returns the number of locations in this location result.
     */
    public int size() {
        return mLocations.size();
    }

    /**
     * Returns the location at the given index, from 0 to {@link #size()} - 1. Locations at lower
     * indices are from earlier in time than location at higher indices.
     */
    public Location get(int i) {
        return mLocations.get(i);
    }

    /**
     * Returns an unmodifiable list of locations in this location result.
     */
    public List<Location> asList() {
        return Collections.unmodifiableList(mLocations);
    }

    /**
     * Returns a deep copy of this LocationResult.
     *
     * @hide
     */
    public LocationResult deepCopy() {
        final int size = mLocations.size();
        ArrayList<Location> copy = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            copy.add(new Location(mLocations.get(i)));
        }
        return new LocationResult(copy);
    }

    /**
     * Returns a LocationResult with only the last location from this location result.
     *
     * @hide
     */
    public LocationResult asLastLocationResult() {
        if (mLocations.size() == 1) {
            return this;
        } else {
            return LocationResult.wrap(getLastLocation());
        }
    }

    /**
     * Returns a LocationResult with only locations that pass the given predicate. This
     * implementation will avoid allocations when no locations are filtered out. The predicate is
     * guaranteed to be invoked once per location, in order from earliest to latest. If all
     * locations are filtered out a null value is returned.
     *
     * @hide
     */
    public LocationResult filter(Predicate<Location> predicate) {
        ArrayList<Location> filtered = mLocations;
        final int size = mLocations.size();
        for (int i = 0; i < size; ++i) {
            if (!predicate.test(mLocations.get(i))) {
                if (filtered == mLocations) {
                    filtered = new ArrayList<>(mLocations.size() - 1);
                    for (int j = 0; j < i; ++j) {
                        filtered.add(mLocations.get(j));
                    }
                }
            } else if (filtered != mLocations) {
                filtered.add(mLocations.get(i));
            }
        }

        if (filtered == mLocations) {
            return this;
        } else if (filtered.isEmpty()) {
            return null;
        } else {
            return new LocationResult(filtered);
        }
    }

    /**
     * Returns a LocationResult with locations mapped to other locations. This implementation will
     * avoid allocations when all locations are mapped to the same location. The function is
     * guaranteed to be invoked once per location, in order from earliest to latest.
     *
     * @hide
     */
    public LocationResult map(Function<Location, Location> function) {
        ArrayList<Location> mapped = mLocations;
        final int size = mLocations.size();
        for (int i = 0; i < size; ++i) {
            Location location = mLocations.get(i);
            Location newLocation = function.apply(location);
            if (mapped != mLocations) {
                mapped.add(newLocation);
            } else if (newLocation != location) {
                mapped = new ArrayList<>(mLocations.size());
                for (int j = 0; j < i; ++j) {
                    mapped.add(mLocations.get(j));
                }
                mapped.add(newLocation);
            }
        }

        if (mapped == mLocations) {
            return this;
        } else {
            return new LocationResult(mapped);
        }
    }

    public int describeContents() {
        return 0;
    }

    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }

        LocationResult that = (LocationResult) o;
        return mLocations.equals(that.mLocations);
    }

    public int hashCode() {
        return Objects.hash(mLocations);
    }

    public String toString() {
        return mLocations.toString();
    }
}
