import tkinter as tk

"""

“I confirm that this assignment is my own work.”

Short Report:
This program implements a modified Dijkstra's algorithm to find a path from classroom 'S' to 'F'
while visiting all classes in the graph. The algorithm ensures all classrooms are visited by 
starting from 'S' and using a greedy approach to visit unvisited classrooms with the shortest
available paths, finally reaching 'F'. 

Important:

## The GUI used in this program does not pop up when required so upon choosing to display your graph,
please check your taskbar (The bar at the bottom of your computer.) ##
"""




"""
Function Name: Dijkstra
Function Description: Uses the dijkstra algorithm to work on a map given in the format of dictionaries of dictionaries.
Inputs: graph, start, end
Outputs: The path taken, how long it took
Process: Gets all the classrooms and sets their initial distance to be infinity since they have not been visited yet apart from S
Gets the previous classroom visited before a classroom, then puts it in a dictionary. Initially it will all set to be None
Puts all the unvisited classes in a set. To make sure there is no repition
Checks the next node and neighboring nodes to make sure the path its taking is the shortest one.
Then updates the path list with shortest way to get to from start to end
Returns the path taken and how long it took from start to end
"""
def dijkstra(graph, start, end):
    # Initialize distances and predecessors
    # Set the distance to the start classroom to 0 and all other classrooms to infinity
    distances = dict()
    for classroom in graph:
        distances[classroom] = float('inf')
    # Code starts with the start class == 0 ##
    distances[start] = 0

    # Predecessors dictionary to reconstruct the shortest path
    predecessors = dict()
    for classroom in graph:
        predecessors[classroom] = None
    
    # Set of all classrooms (unvisited)
    unvisited = set(graph.keys())
    
    while unvisited:
        # Find the unvisited classroom with the smallest distance
        min_classroom = None
        for classroom in unvisited:
            if min_classroom is None or distances[classroom] < distances[min_classroom]:
                min_classroom = classroom
        
        ## So this if statement will never execute (This line is a continuation of line 29)
        # If the smallest distance is infinity, there is no connection
        if distances[min_classroom] == float('inf'):
            break
        
        # Remove the classroom from the unvisited set
        unvisited.remove(min_classroom)
        # Update distances to each neighbor of the current classroom
        for neighbor, weight in graph[min_classroom].items():
            new_distance = distances[min_classroom] + weight
            
            # Only update if the new distance is shorter
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = min_classroom
    
    # Backtrack from the last classroom to find the path to the first classroom
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]

    path = path[::-1]
    
    return path, distances[end]




"""
Function Name: createSchoolMap
Function Description: This function creates the map of the classroom that will be used in the dijkstra
function
Inputs: None
Outputs: A dictionary of the classrooms and their connections (Dictionary of dictionaries)
Process: Saves the extra minutes taken to cross pass that area, then adds those values to time taken from a node to a specific neighbour
"""
def create_school_map():
    # delays in mins
    lava = 1000  # Walk through the lava (isnt possible so death (+1000))
    plank = 10 # Takes an extra 3 mins to steadily use a plank to get past
    river = 15 # A flood on the way, you have to swim (but your not the best swimmer)
    gameroom = 90 # You see the gameroom so you go play fifa for some time (Time runs fast when your playing games)
    bathroom = 2 # You need to go to the bathroom
    reception = 10 # The receptionist are giving food for free, you can't miss out on the offer
    girl = 25 # You see your girlfriend that wont stop disturbing you

    # Define the graph as an adjacency list
    graph = {
        'A': {'S': 7+reception, 'H': 21+lava},
        'B': {'S': 8+reception, 'D': 20+plank, 'H': 4, 'L': 19},
        'C': {'L': 5, 'S': 15+reception},
        'D': {'B': 20+river, 'E': 4},
        'E': {'D': 4, 'H': 5},
        'F': {'G': 6, 'K': 12+girl},
        'G': {'H': 4, 'K': 11+bathroom, 'F': 6},
        'H': {'E': 5, 'A': 21+plank, 'B': 4, 'G': 4}, #Plank can only be used one way, the rest has to manage
        'I': {'J': 4+gameroom, 'K': 4+gameroom}, # I,J,K is the game halls (ps4,xbox,nintendo)
        'J': {'I': 4+gameroom, 'L': 3},
        'K': {'I': 4+gameroom, 'G': 11+bathroom, 'F': 12+girl},
        'L': {'J': 3, 'B': 19, 'C': 5},
        'S': {'A': 7+reception, 'B': 8+reception, 'C': 15+reception}
    }
    return graph


"""
Function Name: draw_graph
Function Description: This function creates the graph that was given in the project debrief. Using canvas from tkiner library
Inputs: canvas(where the graph would be displayed), graph(the graph to use to create this visual display), and the paths
Outputs: None
Process: The coordinate of where each node is saved
Loops through the graph given to find the neighbours to a node then make a connection between those 2 nodes making sure the start and end node are both highlighted.
"""
def draw_graph(canvas, graph, path):
    node_coords = {
        'A': (50, 170), 'B': (200, 180), 'C': (280, 110),
        'D': (30, 250), 'E': (50, 350), 'F': (280, 380),
        'G': (200, 350), 'H': (170, 300), 'I': (280, 240),
        'J': (350, 230), 'K': (320, 270), 'L': (320, 200),
        'S': (130, 80)
    }



    for node in graph:
        for neighbor, distance in graph[node].items():
            x1, y1 = node_coords[node]
            x2, y2 = node_coords[neighbor]
            canvas.create_line(x1, y1, x2, y2)


            # # The code below shows the distance, but i put it in comments because it does not look good
            # # Calculate the position for the distance label away from the midpoint
            # mid_x = (x1 + x2) / 2
            # mid_y = (y1 + y2) / 2

            # # Offset the label position to avoid overlapping with the line
            # offset_x = (x2 - x1) * 0.1
            # offset_y = (y2 - y1) * 0.1
            # label_x = mid_x + offset_x
            # label_y = mid_y + offset_y

            # # Display the distance
            # canvas.create_text(label_x, label_y, text=str(distance), fill="blue")

    for node, (x, y) in node_coords.items():
        color = "white"
        if node == 'S':
            color = "purple"
        elif node == 'F':
            color = "green"
        canvas.create_oval(x-10, y-10, x+10, y+10, fill=color)
        canvas.create_text(x, y, text=node)

    for i in range(len(path)-1):
        x1, y1 = node_coords[path[i]]
        x2, y2 = node_coords[path[i+1]]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
    

"""
Function Name: display_gui
Function Description: This function displays the graph that was given in the project debrief. Using tkiner and canvas.
Inputs: None
Outputs: None
Process: A window is created then a canvas is packed unto that window.
The graph is then created and then used in the djikstra function and draw_graph function
the draw_draph function is called with the graph, canvas packed and the path to be used.
All this is displayed with the path taken and the time taken.
"""
def display_gui():
    root = tk.Tk()
    root.title("School Map Path Finder")

    canvas = tk.Canvas(root, width=400, height=500)
    canvas.pack()

    graph = create_school_map()
    path, distance = dijkstra(graph, 'S', 'F')

    draw_graph(canvas, graph, path)

    label = tk.Label(root, text=f"Shortest path from class S to F: {path}\nTotal distance: {distance}")
    label.pack()

    root.mainloop()


"""
Function Name: run
Function Description: This function runs the program and calls the other functions
Inputs: None
Outputs: None
Function Process: Ask's the user if they would prefer to see the graph displayed or not.
If not runs the dijkstra function using the createSchoolMap function, 'S' as the start, and 'F' as then End.
Saves the results of dijkstra into path and distance
Prints the path and distance
If yes, the display_gui function is run
"""

def run():
    user_choice = input("Do you want the graph displayed or not? (y/n): ") # Asks the user if they want the graph displayed
    if user_choice.lower() in ('n', 'no'):
        # Find the shortest path from class S to F
        path, distance = dijkstra(create_school_map(), 'S', 'F')

        # Output the results
        print(f"Shortest path from class S to F: {path}")
        print(f"Total minutes Taken: {distance} Minutes")
    elif user_choice.lower() in ('y', 'yes'):
        display_gui()
    else:
        print("Invalid Input")


run()
