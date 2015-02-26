""" Creates png images of "art" with recursive functions """

import random
import math
from PIL import Image

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if min_depth < 1:
        return 'Error, min_depth must be greater than 1'

    depth = random.randint(min_depth, max_depth)
    function = make_function(depth)
    #clever, I guess this technically works! The wording of the assignment was somewhat ambiguous so I'm not going to take points of for this, but the intention was for every 'x' or 'y' in this function to be randomly nested at a depth somewhere between min_depth and max_depth.
    #currently, in your code, every 'x' or 'y' is nested at the same depth. Can you think of how you would change your code to have that depth be random, between min_depth and max_depth?
    return function

def make_function(depth):
    """ Recursively generates a function for build_random_function"""
    if depth == 0:
        base_case_options = [["x"], ["y"]]
        return random.choice(base_case_options)
    else:
        modifiers = ["prod", "avg", "cos_pi", "sin_pi", "tan_pi", "asin_pi"]
        rand_modifier = random.choice(modifiers)
        # try to avoid using in when comparing strings for equality, as it obscures what you're doing and the intention is not clear. Instead, just do if rand_modifier == "prod", which is more readable.
        if "prod" in rand_modifier:
            return ["prod", make_function(depth-1), make_function(depth-1)]
        if "avg" in rand_modifier:
            return ["avg", make_function(depth-1), make_function(depth-1)]
        if "cos_pi" in rand_modifier:
            return ["cos_pi", make_function(depth-1)]
        if "sin_pi" in rand_modifier:
            return ["sin_pi", make_function(depth-1)]
        if "tan_pi" in rand_modifier:
            return ["tan_pi", make_function(depth-1)]
        if "asin_pi" in rand_modifier:
            return ["asin_pi", make_function(depth-1)]

def evaluate_random_function(function, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value
    """
    if "x" in function[0]:
        return x
    elif "y" in function[0]:
        return y
    elif "prod" in function[0]:
        return evaluate_random_function(function[1], x, y) * evaluate_random_function(function[2], x, y)
    elif "avg" in function[0]:
        return 0.5 * (evaluate_random_function(function[1], x, y) + evaluate_random_function(function[2], x, y))
    elif "cos_pi" in function[0]:
        return math.cos(math.pi * evaluate_random_function(function[1], x, y))
    elif "sin_pi" in function[0]:
        return math.sin(math.pi * evaluate_random_function(function[1], x, y))
    elif "tan_pi" in function[0]:
        return math.tan(math.pi * evaluate_random_function(function[1], x, y))
    elif "asin_pi" in function[0]:
        return math.asin(math.pi * evaluate_random_function(function[1], x, y))
#nice and compact, cool! :)

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_interval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_range = input_interval_end - float(input_interval_start) #turns input_interval_start into a float to prevent integer division problems
    output_range = output_interval_end - output_interval_start
    return (((val - input_interval_start) / input_range) * output_range) + output_interval_start
    #nice, good job choosing variable names too!

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    # red_function = ["x"]
    # green_function = ["y"]
    # blue_function = ["x"]
    red_function = build_random_function(5, 7)
    green_function = build_random_function(5, 7)
    blue_function = build_random_function(5, 7)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    #print build_random_function(7, 10)
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
