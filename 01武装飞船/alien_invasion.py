import sys
import pygame
import settings

pygame.init()

'主窗口'
screen_image = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen_image.get_rect()

'标题栏'
pygame.display.set_caption('Alien Invasion')

'飞船'
ship_image = pygame.image.load('images/ship.bmp')
ship_rect = ship_image.get_rect()
ship_rect.midbottom = screen_rect.midbottom
moving_left = False
moving_right = False

'子弹'
bullets = pygame.sprite.Group()

'死循环'
while True:
    '捕捉所有操作'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()

            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True

            if event.key == pygame.K_SPACE:
                if len(bullets) < settings.bullets_allowed:
                    new_bullet = pygame.sprite.Sprite()
                    new_bullet.rect = pygame.Rect(0, 0, 3, 15)
                    new_bullet.rect.midbottom = ship_rect.midtop
                    bullets.add(new_bullet)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
    
    '飞船随开关移动'
    if moving_left and ship_rect.left > 0:
        ship_rect.x -= settings.ship_speed
    if moving_right and ship_rect.right < screen_rect.right:
        ship_rect.x += settings.ship_speed

    '绘制图像'
    screen_image.fill(settings.bg_color1)
    screen_image.blit(ship_image, ship_rect)

    for bullet in bullets:
        pygame.draw.rect(screen_image, settings.bg_color2, bullet.rect)
        bullet.rect.y -= 1
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    pygame.display.flip()
