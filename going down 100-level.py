import pgzrun
import random

WIDTH = 700
HEIGHT = 900
playerSpeed = 5
brickSpeed = 2
isLoose = False
score = 0
game_started = False  # New variable to track if the game has started

# New variables for jumping
isJumping = False
jumpSpeed = 10
gravity = 1

alien = Actor('alien')
alien.x = WIDTH / 2
alien.y = HEIGHT / 5
lastAlienY = alien.y

bricks = []
for i in range(5):
    brick = Actor('brick')
    brick.pos = 100 * (i + 1), 150 * (i + 1)
    bricks.append(brick)

def draw():
    screen.clear()
    if not game_started:  # Show the start screen if the game hasn't started
        screen.draw.text("Press ESC to Start the Game", center=(WIDTH / 2, HEIGHT / 2),
                         fontsize=50, color="Pink")
    else:
        alien.draw()
        for brick in bricks:
            brick.draw()
        screen.draw.text("Survived for " + str(score) + " levels！",
                         (400, 20), fontsize=25, fontname='s', color='white')
        if isLoose:
            screen.draw.text("Fail！", (80, HEIGHT / 2 - 100),
                             fontsize=100, fontname='s', color='red')

def update():
    global isLoose, playerSpeed, brickSpeed, score, lastAlienY, isJumping, jumpSpeed, game_started

    # Check if ESC is pressed to start the game
    if not game_started and keyboard.escape:  # Use `keyboard.escape` for ESC key
        game_started = True

    if game_started and not isLoose:
        isPlayerOnGround = False
        for brick in bricks:
            # Check if the alien is on a brick
            if abs(alien.bottom - brick.top) < 5 \
                and brick.left - alien.left < alien.width * 2 / 3 \
                and alien.right - brick.right < alien.width * 2 / 3:
                alien.image = 'alien'
                isPlayerOnGround = True
                alien.bottom = brick.top
                isJumping = False  # Reset jumping when on the ground
                if lastAlienY < alien.y:
                    score += 1

                if keyboard.left:
                    alien.x = alien.x - playerSpeed
                if keyboard.right:
                    alien.x = alien.x + playerSpeed

        lastAlienY = alien.y

        # Jumping logic
        if keyboard.space and not isJumping and isPlayerOnGround:
            isJumping = True
            jumpSpeed = 19 # Initial jump speed

        if isJumping:
            alien.image = 'alien_falling'
            alien.y -= jumpSpeed  # Move alien up
            jumpSpeed -= gravity  # Gradually decrease jump speed to simulate gravity

            if jumpSpeed < 0:  # Check if alien starts falling down
                isJumping = False

        elif not isPlayerOnGround:
            alien.image = 'alien_falling'
            alien.y += 5  # Apply gravity when in free fall

        for brick in bricks:
            brick.y -= brickSpeed

        if bricks[0].top < 10:
            del bricks[0]
            brick = Actor('brick')
            brick.x = random.randint(100, 500)
            brick.y = HEIGHT
            bricks.append(brick)

        if alien.top < 0 or alien.bottom > HEIGHT:
            playerSpeed = 0
            brickSpeed = 0
            isLoose = True

pgzrun.go()
