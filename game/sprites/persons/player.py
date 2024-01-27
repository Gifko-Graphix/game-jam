from game.defs import Direction
from game.sprites.persons.person import Person
from utils.loader import load_image

walkUpFiles = ["PlayerB1.png", "PlayerB2.png", "PlayerB3.png", "PlayerB4.png", "PlayerB5.png", "PlayerB6.png", "PlayerB7.png", "PlayerB8.png"]
walkDownFiles = ["PlayerF1.png", "PlayerF2.png", "PlayerF3.png", "PlayerF4.png", "PlayerF5.png", "PlayerF6.png", "PlayerF7.png", "PlayerF8.png"]
walkLeftFiles = ["PlayerL1.png", "PlayerL2.png", "PlayerL3.png", "PlayerL4.png", "PlayerL5.png", "PlayerL6.png", "PlayerL7.png", "PlayerL8.png"]
walkRightFiles = ["PlayerR1.png", "PlayerR2.png", "PlayerR3.png", "PlayerR4.png", "PlayerR5.png", "PlayerR6.png", "PlayerR7.png", "PlayerR8.png"]



class Player(Person):
    def __init__(self):
        Person.__init__(self)
        self.surface, self.rect = load_image("PlayerL.png", -1, scale=1)
        self.walkUpAnim = [load_image(file, -1, 1) for file in walkUpFiles]
        self.walkDownAnim = [load_image(file, -1, 1) for file in walkDownFiles]
        self.walkLeftnAnim = [load_image(file, -1, 1) for file in walkLeftFiles]
        self.walkRightAnim = [load_image(file, -1, 1) for file in walkRightFiles]


        self.idleUp = load_image("PlayerB.png", -1, 1)
        self.idleDown = load_image("PlayerF.png", -1, 1)
        self.idleLeft = load_image("PlayerL.png", -1, 1)
        self.idleRight = load_image("PlayerR.png", -1, 1)
        self.isWalking = False
        self.walkCount = 9
        self.isCaught = False
        self.velocity = 5
        self.direction = Direction.up
        self.rect.topleft = 10, 90
    
    def walkLeft(self):
        self.isWalking = True
        self.direction = Direction.left
        self.surface = self.walkLeftnAnim[self.walkCount // 9][0]
        self.walkCount -= 1
        if self.rect.left > self.area.left:
            self.rect.move_ip(-self.velocity, 0)

    def walkRight(self):
        self.isWalking = True
        self.direction = Direction.right
        self.surface = self.walkRightAnim[self.walkCount // 9][0]
        self.walkCount -= 1
        if self.rect.right < self.area.right:
            self.rect.move_ip(self.velocity, 0)

    def walkUp(self):
        self.isWalking = True
        self.direction = Direction.up
        self.surface = self.walkUpAnim[self.walkCount // 9][0]
        self.walkCount -= 1
        if self.rect.top < self.area.top:
            self.rect.move_ip(0, self.velocity)
        if self.rect.top > self.area.top:
            self.rect.move_ip(0, -self.velocity)

    def walkDown(self):
        self.isWalking = True
        self.direction = Direction.down
        self.surface = self.walkDownAnim[self.walkCount // 9][0]
        self.walkCount -= 1
        if self.rect.bottom < self.area.bottom:
            self.rect.move_ip(0, self.velocity)
    
    def update(self):
        if self.isWalking:
            if self.walkCount == 0:
                self.walkCount = 9
        else:
            if self.direction == Direction.up:
                self.surface = self.idleUp[0]
            if self.direction == Direction.down:
                self.surface = self.idleDown[0]
            if self.direction == Direction.left:
                self.surface = self.idleLeft[0]
            if self.direction == Direction.right:
                self.surface = self.idleRight[0]
        super().update()


    def interact(self, allInteractables):
      for sprite in allInteractables:
        if sprite.canInteract:
            sprite.foo_action()
