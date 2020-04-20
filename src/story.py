import pygame
import time
"""
def story():
  surface = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption('James Bomb')
	clock = pygame.time.Clock()

  stories = [pygame.image.load('../story/story1.1.jpg'),
            pygame.image.load('../story/story1.2.jpg'),
            pygame.image.load('../story/story1.3.jpg'),
            pygame.image.load('../story/story1.4.jpg'),
            pygame.image.load('../story/story1.5.jpg'),
            pygame.image.load('../story/story1.6.jpg'),
            pygame.image.load('../story/story1.7.jpg'),
            pygame.image.load('../story/story1.8.jpg'),
            pygame.image.load('../story/story1.9.jpg'),
            pygame.image.load('../story/story1.10.jpg')]
"""

pygame.init()


display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
stories = [pygame.image.load('story/story1.1.jpg'),
            pygame.image.load('story/story1.2.jpg'),
            pygame.image.load('story/story1.3.jpg'),
            pygame.image.load('story/story1.4.jpg'),
            pygame.image.load('story/story1.5.jpg'),
            pygame.image.load('story/story1.6.jpg'),
            pygame.image.load('story/story1.7.jpg'),
            pygame.image.load('story/story1.8.jpg'),
            pygame.image.load('story/story1.9.jpg'),
            pygame.image.load('story/story1.10.jpg')]
  

def story1(index):
  if index<10 :
    gameDisplay.blit(stories[index], (display_width/2, display_height/2))
  else :
    gameDisplay.blit(stories[9])


nbStory = 0;

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    story1(nbStory)
    time.sleep(3)
    nbStory=nbStory+1
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()