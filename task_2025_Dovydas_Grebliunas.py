"""
# Task:
Implement a route planning algorithm.
# Description:
Write a Python program that calculates the optimal route plan given a fleet of vans to deliver packages.
The program should determine the most fuel efficient route based on distances while considering the capacity of each
van, van fuel consumption and the weight of the packages.
# Constraints:
1. Each van has a specified capacity.
2. Each package has a pickup location, delivery location, and weight.
3. Locations are one dimensional (straight line).
4. Vans can pick up and deliver multiple packages, ensuring their capacity is not exceeded.
5. Vans can drop a package only at destination.
6. All packages must be delivered by the end of the day.
7. All vans start and end the day at central warehouse (0).
8. Max 5 packages might need to be delivered during the day.
9. Max 3 vans might be given as a fleet.
10. In case of multiple best routes, provide any one of them.
11. Do not use any 3rd party libraries. You can use Python standard libraries.
# Goals:
1. [Base] Calculate the most fuel efficient route if only a single van from the fleet would operate during the
   day (others remain parked). You need to determine which van is the most suitable for the day.
2. [Optional - Karma points] Calculate the most fuel efficient routes combination if all vans would be operational
   during the day. You'll need to create a function `find_optimal_route_for_multiple_vans`.
# Input Format:
- van_stats: A list where each element specifies the capacity of a van and fuel units consumed for 1 distance unit
    - van_stats = [(10, 10), (9,8)]
- packages: A list of tuples, where each tuple represents a package with (pickup location, delivery location, weight).
    - packages = [(-1, 5, 4), (6, 2, 9), (-2, 9, 3)]
# Sample Input:
van_stats = [(10, 10), (9,8)]
packages = [(-1, 5, 4), (6, 2, 9), (-2, 9, 3)]
# Sample Output for Base Goal:
- Selected Van: (9, 8)
- Optimal Route: [
      (0, "start"), (-1, "pick"), (-2, "pick"), (5, "drop"), (9, "drop"), (6, "pick"), (2, "drop"), (0, "end")
  ]
- Route Length: 22
- Fuel Consumption: 176
"""

import math
import itertools
from typing import List, Tuple, Dict

def find_optimal_route_for_single_van(
    van_stats: List[Tuple[int, int]], 
    packages: List[Tuple[int, int, int]]
) -> Tuple[Tuple[int, int], List[Tuple[int, str]], int, int]:

    best_solution = None  # (van, route, route_length, fuel_consumption)

    def compute_optimal_route_for_van(capacity: int, packages: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, str]] | None, int]:
        best_distance = float('inf')
        best_route = None

        def backtrack(current_loc: int, remaining: List[Tuple[int, int, int]], 
                      onboard: List[Tuple[int, int, int]], 
                      current_route: List[Tuple[int, str]], 
                      current_load: int, current_distance: int):
            nonlocal best_distance, best_route

            # All packages have been picked up and delivered,
            # return to warehouse
            if not remaining and not onboard:
                total_distance = current_distance + abs(current_loc - 0)
                if total_distance < best_distance:
                    best_distance = total_distance
                    best_route = current_route + [(0, "end")]
                return

            # Pick up packages if capacity let's it
            for i, pkg in enumerate(remaining):
                pickup, delivery, weight = pkg
                if current_load + weight <= capacity:
                    new_loc = pickup
                    step_distance = abs(current_loc - new_loc)
                    new_distance = current_distance + step_distance
                    # Skip if distance if higher than best one
                    if new_distance >= best_distance:
                        continue
                    # Remove this package from remaining and add it to onboard
                    new_remaining = remaining[:i] + remaining[i+1:]
                    new_onboard = onboard + [pkg]
                    backtrack(new_loc, new_remaining, new_onboard, current_route + [(new_loc, "pick")],
                              current_load + weight, new_distance)
            
            # Deliver package that are onboard
            for i, pkg in enumerate(onboard):
                pickup, delivery, weight = pkg
                new_loc = delivery
                step_distance = abs(current_loc - new_loc)
                new_distance = current_distance + step_distance
                if new_distance >= best_distance:
                    continue
                new_onboard = onboard[:i] + onboard[i+1:]
                backtrack(new_loc, remaining, new_onboard, current_route + [(new_loc, "drop")],
                          current_load - weight, new_distance)
        
        # Start the recursion at the warehouse
        backtrack(0, packages, [], [(0, "start")], 0, 0)
        return (best_route, best_distance) if best_route is not None else (None, float('inf'))
    
    # Check van for delivering packages if it's a viable option
    for van in van_stats:
        capacity, fuel_rate = van
        # Skip van if it can't pick up atleast one package
        if any(weight > capacity for (_, _, weight) in packages):
            continue
        route, route_length = compute_optimal_route_for_van(capacity, packages)
        if route is None:
            continue
        fuel_consumption = route_length * fuel_rate
        if best_solution is None or fuel_consumption < best_solution[3]:
            best_solution = (van, route, route_length, fuel_consumption)
    
    if best_solution is None:
        raise ValueError("No van can deliver all packages with the given constraints.")
    
    return best_solution

def find_optimal_route_for_multiple_vans(
    van_stats: List[Tuple[int, int]], 
    packages: List[Tuple[int, int, int]]
) -> Tuple[Dict[int, Tuple[List[Tuple[int, str]], int, int]], int]:

    def compute_optimal_route(capacity: int, pkgs: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, str]] | None, int]:

        best_distance = math.inf
        best_route = None

        def backtrack(current_loc: int,
                      remaining: List[Tuple[int, int, int]],
                      onboard: List[Tuple[int, int, int]],
                      current_route: List[Tuple[int, str]],
                      current_load: int,
                      current_distance: int):
            nonlocal best_distance, best_route

            # All packages have been delivered
            # Van returns to warehouse
            if not remaining and not onboard:
                total_distance = current_distance + abs(current_loc - 0)
                if total_distance < best_distance:
                    best_distance = total_distance
                    best_route = current_route + [(0, "end")]
                return

            # Pick up packages
            for i, pkg in enumerate(remaining):
                pickup, delivery, weight = pkg
                if current_load + weight <= capacity:
                    new_loc = pickup
                    step_distance = abs(current_loc - new_loc)
                    new_distance = current_distance + step_distance
                    # Skip if distance if higher than best one
                    if new_distance >= best_distance:
                        continue
                    new_remaining = remaining[:i] + remaining[i+1:]
                    new_onboard = onboard + [pkg]
                    backtrack(new_loc, new_remaining, new_onboard,
                              current_route + [(new_loc, "pick")],
                              current_load + weight,
                              new_distance)

            # Delivere packages that are already picked up
            for i, pkg in enumerate(onboard):
                pickup, delivery, weight = pkg
                new_loc = delivery
                step_distance = abs(current_loc - new_loc)
                new_distance = current_distance + step_distance
                if new_distance >= best_distance:
                    continue
                new_onboard = onboard[:i] + onboard[i+1:]
                backtrack(new_loc, remaining, new_onboard,
                          current_route + [(new_loc, "drop")],
                          current_load - weight,
                          new_distance)

        backtrack(0, pkgs, [], [(0, "start")], 0, 0)
        return (best_route, best_distance) if best_route is not None else (None, math.inf)

    best_total_fuel = math.inf
    best_assignment_routes = None
    num_vans = len(van_stats)

    # Try every way to assign packages to vans.
    # Each assignment is a list of numbers (one number per package)
    # where each number indicates which van (0 to num_vans-1) will deliver that package.
    for assignment in itertools.product(range(num_vans), repeat=len(packages)):
        # Create a dictionary mapping each van to its list of assigned packages.
        van_to_packages = {i: [] for i in range(num_vans)}
        for pkg_index, van_index in enumerate(assignment):
            van_to_packages[van_index].append(packages[pkg_index])
        
        assignment_valid = True  # boolean to check if the assignment is valid.
        total_fuel = 0
        routes_for_assignment = {}  # route, distance and fuel for each van in this assignment.

        # For every van compute its optimal route based on the packages assigned.
        for i in range(num_vans):
            capacity, fuel_rate = van_stats[i]
            assigned_pkgs = van_to_packages[i]
            # If any assigned package exceeds the van's capacity than this assignment is invalid.
            if any(weight > capacity for (_, _, weight) in assigned_pkgs):
                assignment_valid = False
                break

            # If no packages are assigned to this van it stays at the warehouse.
            if not assigned_pkgs:
                route = [(0, "start"), (0, "end")]
                distance = 0
                fuel = 0
            else:
                # Compute the optimal route for the van with it's assigned packages.
                route, distance = compute_optimal_route(capacity, assigned_pkgs)
                if route is None:
                    assignment_valid = False
                    break
                fuel = distance * fuel_rate

            # Save route details
            routes_for_assignment[i] = (route, distance, fuel)
            total_fuel += fuel

        # If assignment is valid and fuel consumption is better than best one save details
        if assignment_valid and total_fuel < best_total_fuel:
            best_total_fuel = total_fuel
            best_assignment_routes = routes_for_assignment

    if best_assignment_routes is None:
        raise ValueError("No valid assignment found for delivering all packages.")

    return best_assignment_routes, best_total_fuel

if __name__ == "__main__":
    # Tests for a single van operation
    print("=== Single Van Operation ===")
    van_stats_single = [(10, 10), (9, 8)]
    packages_single = [(-1, 5, 4), (6, 2, 9), (-2, 9, 3)]
    
    selected_van, optimal_route, route_length, fuel_consumption = find_optimal_route_for_single_van(van_stats_single, packages_single)
    
    assert selected_van == (9, 8)
    assert optimal_route == [
        (0, 'start'), (-1, 'pick'), (-2, 'pick'), (5, 'drop'), (9, 'drop'), (6, 'pick'), (2, 'drop'), (0, 'end')
    ]
    assert route_length == 22
    assert fuel_consumption == 176

    print("Selected Van:", selected_van)
    print("Optimal Route:", optimal_route)
    print("Route Length:", route_length)
    print("Fuel Consumption:", fuel_consumption)
    
    # Tests for multiple vans operation
    print("\n=== Multiple Vans Operation ===")
    van_stats_multiple = [(10, 9), (18, 10)]
    packages_multiple = [(-10, -5, 9), (5, 10, 9), (4, 15, 9)]
    
    assignment_routes, total_fuel = find_optimal_route_for_multiple_vans(van_stats_multiple, packages_multiple)

    for van_index, (route, distance, fuel) in assignment_routes.items():
        capacity, fuel_rate = van_stats_multiple[van_index]
        print(f"Van {van_index} (capacity={capacity}, fuel_rate={fuel_rate}):")
        print("  Route:", route)
        print("  Route Length:", distance)
        print("  Fuel Consumption:", fuel)
    print("Total Fuel Consumption:", total_fuel)
