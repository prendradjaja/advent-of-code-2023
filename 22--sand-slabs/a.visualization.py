import a
import sys
import ast
from a import X, Y, Z, CollisionWorld, Brick


def main():
    world = CollisionWorld()
    for line in open(sys.argv[1]).read().splitlines():
        start, end = line.split('~')
        start = ast.literal_eval(start)
        end = ast.literal_eval(end)
        world.add_brick(Brick(start, end))

    print('X axis is left-to-right:')
    show(world, X, 0, 9)

    print('\nY axis is left-to-right:')
    show(world, Y, 0, 9)


def show(world, ltr_axis, z_min, z_max):
    assert ltr_axis in [X, Y]

    # Names:
    # - A (or a) is the ltr_axis
    # - B (or b) is the other axis (neither A nor Z, but the other one)

    A = ltr_axis
    B = int(not A)

    foo = {
        (cube[A], cube[Z])
        for brick in world.bricks
        for cube in brick.cubes
    }

    for z in range(z_max, z_min-1, -1):
        for a in range(3):
            if (a, z) in foo:
                ch = '#'
            else:
                ch = '.'
            print(ch, end='')
        print('', z)


if __name__ == '__main__':
    main()
