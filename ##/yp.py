
from math import pi
def Circle_area(Radius, Pi=3.14):
    """
    Calculate the area of a Circle using Radius .
    
    Formula: Area = pi *Radius**2 
    
    Args:
        Radius (float): The Radius of the Circle
        pi (float):the volue of pi (default is 3.14 )
    Returns:
        float: The area of the Circle
    """
    area =(Pi *(Radius**2))
    return area


# Example usage
if __name__ == "__main__":
    #pass
    #...
    # Get base and height from user input
    try:
        Radius = float(input("Enter the Radius of the Circle: "))        
        # Calculate and display the area
    # ... (הקוד עד שורת ה-print) ...
        area = Circle_area( Radius)
        print(f"Circle with Radius {Radius} has area: {area}")
        
    # שורה קריטית זו חייבת להגיע מיד אחרי ה-try-block
    except ValueError: 
        print("Please enter a valid number for the Radius.")#בבבב8