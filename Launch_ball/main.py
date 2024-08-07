import pygame, pymunk, math
import pymunk.pygame_util

from pygame.time import get_ticks

pygame.init()

width, height = 1200, 700
radius = 30

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Launch_ball")

collide_sound = pygame.mixer.Sound('collide.wav')

duration = 5

def collision(shape):
    if shape.body.position.x >= width-radius or shape.body.position.x <= 0+radius or shape.body.position.y <= 0+radius or shape.body.position.y >= height-radius:
        collide_sound.play()
        print("Collision")
        print(shape.body.position)



def calc_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def calc_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 +(p2[0] - p1[0])**2)


def draw(space, screen, draw_options, line):
    screen.fill("white")

    if line:
        pygame.draw.line(screen, "black", line[0], line[1],3)

    space.debug_draw(draw_options)

    pygame.display.update()

def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type= pymunk.Body.STATIC)
    body.position = pos

    shape = pymunk.Circle(body,radius)
    shape.mass = mass
    shape.color = (255,0,0,100)

    shape.elasticity = 1.4
    shape.friction = 0.4

    space.add(body, shape)
    return shape

def create_rect(space, width, height, mass, color, pos):
    body = pymunk.Body(body_type= pymunk.Body.DYNAMIC)
    body.position = pos

    shape = pymunk.Poly.create_box(body,([width, height]))
    shape.mass = mass
    shape.color = color

    shape.elasticity = 0.8
    shape.friction = 0.8

    space.add(body, shape)
    return shape

def create_boudaries(space,width, height):
    rects = [
        [(width / 2, height+49), (width, 100)],
        [(width / 2, -49), (width, 100)],
        [(width+49, height / 2), (100, height)],
        [(-49, height / 2), (100, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        space.add(body,shape)
        shape.elasticity = 0.5
        shape.friction = 0.8

def run(screen, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0, 981)


    rect1 = create_rect(space, 50, 50, 20, (0, 255, 0, 100), (720, 400))

    rect2 = create_rect(space, 30, 120, 80, (100, 50, 10, 100), (800, height-60))

    rect3 = create_rect(space, 30, 120, 80, (100, 50, 10, 100), (650, height - 60))

    rect4= create_rect(space, 200, 30, 80, (100, 50, 10, 100), (720, height - 140))

    create_boudaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    press_pos = None
    ball = None

    while run:

        line = None
        if ball and press_pos:
            line = [press_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    press_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, radius,10, press_pos)
                start_time = 0

            if event.type == pygame.MOUSEBUTTONUP:
                if press_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calc_angle(*line)

                    force = calc_distance(*line)*50

                    print(force)

                    if force < 28000:
                        act_force = force
                    else:
                        act_force = 28000

                    print(act_force)

                    fx = math.cos(angle) * act_force
                    fy = math.sin(angle) * act_force

                    ball.body.apply_impulse_at_local_point((-fx,-fy),(0,0))
                    press_pos = None


                    #current_time = get_ticks()
                    #if current_time - start_time >= duration:


                else:
                    space.remove(ball, ball.body)
                    ball = None

        draw(space, screen, draw_options, line)

        if ball:
            #print(ball.body.position)
            collision(ball)

        space.step(dt)
        clock.tick(fps)


if __name__ == "__main__":
    run(screen, width, height)