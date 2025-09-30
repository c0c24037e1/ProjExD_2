import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-5), 
    pg.K_DOWN: (0,+5), 
    pg.K_LEFT: (-5,0), 
    pg.K_RIGHT: (+5,0),
    #最後","を付ける
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen: pg.Surface) -> None: # 課題1:ゲームオーバー画面
    # 1.
    go_img = pg.Surface((WIDTH, HEIGHT))
    go_img.fill((0,0,0))
    # 2.
    go_img.set_alpha(200)
    # 3.
    go_font = pg.font.Font(None, 100)
    txt = go_font.render("Game Over", True,(255,255,255))
    txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    # 4.
    kouka_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kouka2_img = kouka_img
    kouka_rct = kouka_img.get_rect(center=(WIDTH // 2 - 225, HEIGHT // 2 + 50))
    kouka2_rct = kouka_img.get_rect(center=(WIDTH // 2 + 225, HEIGHT // 2 + 50))
    # 5.
    screen.blit(go_img,(0,0))
    screen.blit(txt,txt_rect)
    screen.blit(kouka_img, kouka_rct)
    screen.blit(kouka2_img, kouka2_rct)

    # 6.
    pg.display.update()
    time.sleep(5)





def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向, 縦方向）
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) # 空のsurface(20*20)
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    bb_img.set_colorkey((0,0,0)) #四隅の黒い部分を削除
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH) # 爆弾用横
    bb_rct.centery = random.randint(0,HEIGHT) # 爆弾用縦
    vx, vy = +5, +5 # 爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            gameover(screen)
            return  #ゲームオーバー


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向
                sum_mv[1] += mv[1] #縦方向

#ctrl / で範囲内をすべてコメントアウト
        # if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #   sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx,vy) # 爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 横にはみ出ていたら
            vx *= -1
        if not tate: # 縦にはみ出ていたら
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct) #爆弾を描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
