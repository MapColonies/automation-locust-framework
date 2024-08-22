import random

def generate_random_points(data, num_points_per_item):
  """
  This function generates random X, Y values for each item in the provided data structure.

  Args:
      data: A list of sublists, where each sublist contains items with "startX", "startY",
            "endX", and "endY" properties.
      num_points_per_item: An integer specifying the desired number of random points
                            to generate for each item in the data.

  Returns:
      None. It prints the results in the format "[index, x, y]".
  """

  for index, sublist in enumerate(data):
    # Check if sublist is empty
    if sublist:
      for item in sublist:
        # Calculate the actual number of points to generate (capped by range size)
        num_points = min(num_points_per_item, (item["endX"] - item["startX"] + 1) * (item["endY"] - item["startY"] + 1))

        # Use a set to avoid duplicates
        points = set()
        while len(points) < num_points:
          # Generate random X and Y values within the range
          x = random.randint(item["startX"], item["endX"])
          y = random.randint(item["startY"], item["endY"])
          points.add((x, y))  # Add unique (x, y) pair to the set

        # Print the results
        for x, y in points:
          print(f"[ {index}, {x}, {y} ]")

# Example usage with configurable number of points
num_points_per_item = 10  # You can change this value
data = [  # Your data structure here (omitted for brevity)]
generate_random_points(data, num_points_per_item)
