import sys
import time
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
ships_isleft = 3

'子弹'
bullets = pygame.sprite.Group()

'数学计算'
an_alien_image = pygame.image.load('images/alien.bmp')
an_alien_image_rect = an_alien_image.get_rect()
an_alien_width = an_alien_image_rect.width
an_alien_height = an_alien_image_rect.height
screen_width, screen_height = screen_rect.size
ship_width, ship_height = ship_rect.size
space_x = screen_width - 2 * an_alien_width
space_y = screen_height - ship_height - 3 * an_alien_height
column_number = space_x // (2 * an_alien_width)
line_number = space_y // (2 * an_alien_height)

'外星人'
aliens = pygame.sprite.Group()
for y_number in range(line_number):
    for x_number in range(column_number):
        alien_sprite = pygame.sprite.Sprite()
        alien_sprite.image = pygame.image.load('images/alien.bmp')
        alien_sprite.rect = alien_sprite.image.get_rect()
        alien_sprite.rect.x = an_alien_width + 2 * an_alien_width * x_number
        alien_sprite.rect.y = an_alien_height + 2 * an_alien_height * y_number
        aliens.add(alien_sprite)
alien_direction = 1

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
                    new_bullet.rect = pygame.Rect(0, 0, 150, 15)
                    new_bullet.rect.midbottom = ship_rect.midtop
                    bullets.add(new_bullet)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    if ships_isleft > 0:

        '飞船随开关移动'
        if moving_left and ship_rect.left > 0:
            ship_rect.x -= settings.ship_speed
        if moving_right and ship_rect.right < screen_rect.right:
            ship_rect.x += settings.ship_speed
        ship_sprite = pygame.sprite.Sprite()
        ship_sprite.image = ship_image
        ship_sprite.rect = ship_rect

        '填充主窗口，绘制飞船'
        screen_image.fill(settings.bg_color1)
        screen_image.blit(ship_image, ship_rect)

        '子弹运动'
        for bullet in bullets:
            pygame.draw.rect(screen_image, settings.bg_color2, bullet.rect)
            bullet.rect.y -= settings.bullet_speed
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        '外星人运动'
        for alien in aliens:
            if alien.rect.right >= screen_rect.right or alien.rect.left <= 0:
                alien_direction *= -1
                for alien in aliens:
                    alien.rect.y += settings.alien_y_speed
                break

        for alien in aliens:
            alien.rect.x += settings.alien_x_speed * alien_direction

        '绘制外星人'
        aliens.draw(screen_image)

        '子弹和外星人碰撞'
        pygame.sprite.groupcollide(bullets, aliens, True, True)

        '外星人没了怎么办？'
        if not aliens:
            bullets.empty()
            for y_number in range(line_number):
                for x_number in range(column_number):
                    alien_sprite = pygame.sprite.Sprite()
                    alien_sprite.image = pygame.image.load('images/alien.bmp')
                    alien_sprite.rect = alien_sprite.image.get_rect()
                    alien_sprite.rect.x = an_alien_width + 2 * an_alien_width * x_number
                    alien_sprite.rect.y = an_alien_height + 2 * an_alien_height * y_number
                    aliens.add(alien_sprite)

        '外星人撞到飞船怎么办？'
        if pygame.sprite.spritecollideany(ship_sprite, aliens):
            ships_isleft -= 1
            aliens.empty()
            bullets.empty()
            for y_number in range(line_number):
                for x_number in range(column_number):
                    alien_sprite = pygame.sprite.Sprite()
                    alien_sprite.image = pygame.image.load('images/alien.bmp')
                    alien_sprite.rect = alien_sprite.image.get_rect()
                    alien_sprite.rect.x = an_alien_width + 2 * an_alien_width * x_number
                    alien_sprite.rect.y = an_alien_height + 2 * an_alien_height * y_number
                    aliens.add(alien_sprite)
            ship_rect.midbottom = screen_rect.midbottom
            time.sleep(0.5)

        '外星人触底怎么办？'
        for alien in aliens:
            if alien.rect.bottom >= screen_rect.bottom:
                ships_isleft -= 1
                aliens.empty()
                bullets.empty()
                for y_number in range(line_number):
                    for x_number in range(column_number):
                        alien_sprite = pygame.sprite.Sprite()
                        alien_sprite.image = pygame.image.load('images/alien.bmp')
                        alien_sprite.rect = alien_sprite.image.get_rect()
                        alien_sprite.rect.x = an_alien_width + 2 * an_alien_width * x_number
                        alien_sprite.rect.y = an_alien_height + 2 * an_alien_height * y_number
                        aliens.add(alien_sprite)
                ship_rect.midbottom = screen_rect.midbottom
                time.sleep(0.5)
                break

        pygame.display.flip()
