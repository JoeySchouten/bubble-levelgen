import levelgen

#TODO: come up with some examples of various usages

def test(output): # Apply this test function to any of the examples below.
    for row in output:
        test_string = " ".join(map(str, row))
        print(test_string.center(20))
    print("Done!")

# Generate the first level in the first world of your game.
levelgen.generate_level(1,1)

# Generate the second level, which is required to only use the 'diagonalR2' fill with the colors 1 and 2.
levelgen.generate_level(1,2, 
                        required=[1, 2, 'diagonalR2'],
                        only_required=True)

# Generate the third level, which excludes all objects with the keywords 'fill' and 'locked'.
levelgen.generate_level(1,2, 
                        excludes=['fill', 'locked'])

# Generate the 7th level of the 4th world, which requires a windmill, a pine tree, and the frame fill, 
# but excludes objects associated with Japan or flags.
levelgen.generate_level(7,2,
                        required=['windmill', 'frame', 'pinetree'],
                        excludes=['japan', 'flag'])