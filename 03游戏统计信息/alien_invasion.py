import sys
import time
import pygame
import settings

pygame.init()

'主窗口'
screen_image = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen_image.get_rect()
screen_image.fill(settings.bg_color1)

'标题栏'
pygame.display.set_caption('Alien Invasion')

'飞船'
ship_image = pygame.image.load('images/ship.bmp')
ship_rect = ship_image.get_rect()
ship_rect.midbottom = screen_rect.midbottom
moving_left = False
moving_right = False
ships_isleft = 0
screen_image.blit(ship_image, ship_rect)

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
aliens.draw(screen_image)

'按钮'
button_rect = pygame.Rect(0, 0, 200, 50)
button_rect.center = screen_rect.center
play_font = pygame.font.SysFont(None, 48)
play_image = play_font.render('Play', True, settings.bg_color2, settings.bg_color4)
play_rect = play_image.get_rect()
play_rect.center = button_rect.center

'统计信息'
score = 0
high_score = 0
level = 1
alien_points = 50

score_str = str(score)
score_font = pygame.font.SysFont(None, 48)
score_image = score_font.render(score_str, True, settings.bg_color2, settings.bg_color3)
score_rect = score_image.get_rect()
score_rect.right = screen_rect.right - 20
score_rect.top = 20
screen_image.blit(score_image, score_rect)

high_score_str = str(high_score)
high_score_font = pygame.font.SysFont(None, 48)
high_score_image = high_score_font.render(high_score_str, True, settings.bg_color2, settings.bg_color3)
high_score_rect = high_score_image.get_rect()
high_score_rect.centerx = screen_rect.centerx
high_score_rect.top = score_rect.top
screen_image.blit(high_score_image, high_score_rect)

level_str = str(level)
level_font = pygame.font.SysFont(None, 48)
level_image = level_font.render(level_str, True, settings.bg_color2, settings.bg_color3)
level_rect = level_image.get_rect()
level_rect.right = score_rect.right
level_rect.top = score_rect.bottom + 10
screen_image.blit(level_image, level_rect)

'可用飞船数量'
ship_group = pygame.sprite.Group()
for ship_number in range(settings.ship_limit - 1):
    ship = pygame.sprite.Sprite()
    ship.image = pygame.image.load('images/ship.bmp')
    ship.rect = ship.image.get_rect()
    ship.rect.x = 10 + (ship.rect.width + 10) * ship_number
    ship.rect.y = 10
    ship_group.add(ship)
ship_group.draw(screen_image)

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                ships_isleft = settings.ship_limit
                pygame.mouse.set_visible(False)
                bullets.empty()

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
        duang = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if duang:
            for item in duang.values():
                score += alien_points * len(item)
        if score > high_score:
            high_score = score

        '统计信息'
        score_str = '{:,}'.format(score)
        score_font = pygame.font.SysFont(None, 48)
        score_image = score_font.render(score_str, True, settings.bg_color2, settings.bg_color3)
        score_rect = score_image.get_rect()
        score_rect.right = screen_rect.right - 20
        score_rect.top = 20
        screen_image.blit(score_image, score_rect)

        high_score_str = '{:,}'.format(high_score)
        high_score_font = pygame.font.SysFont(None, 48)
        high_score_image = high_score_font.render(high_score_str, True, settings.bg_color2, settings.bg_color3)
        high_score_rect = high_score_image.get_rect()
        high_score_rect.centerx = screen_rect.centerx
        high_score_rect.top = score_rect.top
        screen_image.blit(high_score_image, high_score_rect)

        level_str = str(level)
        level_font = pygame.font.SysFont(None, 48)
        level_image = level_font.render(level_str, True, settings.bg_color2, settings.bg_color3)
        level_rect = level_image.get_rect()
        level_rect.right = score_rect.right
        level_rect.top = score_rect.bottom + 10
        screen_image.blit(level_image, level_rect)

        '可用飞船数量'
        ship_group = pygame.sprite.Group()
        for ship_number in range(ships_isleft - 1):
            ship = pygame.sprite.Sprite()
            ship.image = pygame.image.load('images/ship.bmp')
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + (ship.rect.width + 10) * ship_number
            ship.rect.y = 10
            ship_group.add(ship)
        ship_group.draw(screen_image)

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
            settings.ship_speed *= settings.speedup_scale
            settings.bullet_speed *= settings.speedup_scale
            settings.alien_x_speed *= settings.speedup_scale
            level += 1

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

    else:
        pygame.draw.rect(screen_image, settings.bg_color4, button_rect)
        screen_image.blit(play_image, play_rect)
        pygame.mouse.set_visible(True)
        settings.ship_speed, settings.bullet_speed, settings.alien_x_speed = settings.speedlist
        score = 0
        level = 1

    pygame.display.flip()
