import pygame
import sys
import random
import json
from pygame.locals import *

def _log_io_error(context, err):
    """セーブ/ロード関連のI/Oエラーはプレイ継続を優先してこれまで黙って
    握りつぶしていたが、原因不明のままだと再現・調査ができないため、
    最低限stderrには残す(プレイヤー向けの画面表示は呼び出し元が別途行う)。"""
    print(f"[dungeon] I/O error in {context}: {err!r}", file=sys.stderr)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLINK = [(224, 255, 255), (192, 240, 255), (128, 224, 255), (64, 192, 255), (128, 224, 255), (192, 240, 255)]

imgTitle = pygame.image.load("image/title2.jpg")
imgWall = pygame.image.load("image/wall.png")
imgWall2 = pygame.image.load("image/wall2.png")
imgWallCrystal = pygame.image.load("image/wall_crystal.png")
imgWallCrystalTop = pygame.image.load("image/wall_crystal_top.png")
imgWallFlame = pygame.image.load("image/wall_flame.png")
imgWallFlameTop = pygame.image.load("image/wall_flame_top.png")
imgDark = pygame.image.load("image/dark.png")
imgPara = pygame.image.load("image/parameter.png")
imgPara2 = pygame.image.load("image/parameter2.png")
# Hero(職業)ごとに左下ステータス欄の顔グラも変える
imgParaSets = {
    "warrior": imgPara,
    "guardian": pygame.image.load("image/parameter_guardian.png"),
    "scholar": pygame.image.load("image/parameter_scholar.png"),
    "scout": pygame.image.load("image/parameter_scout.png"),
}
imgBtlBG = pygame.image.load("image/btlbg.png")
imgBtlBGCrystal = pygame.image.load("image/btlbg_crystal.png")
imgBtlBGFlame = pygame.image.load("image/btlbg_flame.png")
imgEnemy = pygame.image.load("image/enemy0.png")
imgItem = [pygame.image.load("image/potion.png"),
           pygame.image.load("image/blaze_gem.png"),
           pygame.image.load("image/spoiled.png"),
           pygame.image.load("image/apple.png"),
           pygame.image.load("image/meat.png"),
           pygame.image.load("image/sord.png"),
           pygame.image.load("image/shield.png"),
           pygame.image.load("image/ring.png"),
           pygame.image.load("image/amulet.png"),
           pygame.image.load("image/bread.png"),
           pygame.image.load("image/pet_egg.png")]
imgPetEggCrystal = pygame.image.load("image/pet_egg_crystal.png")
imgPetEggFlame = pygame.image.load("image/pet_egg_flame.png")
imgPet = {
    "slime": pygame.image.load("image/pet_slime.png"),
    "sprite": pygame.image.load("image/pet_sprite.png"),
    "cat": pygame.image.load("image/pet_cat.png"),
}
imgPetRev = {
    "slime": pygame.image.load("image/pet_slime_rev.png"),
    "sprite": pygame.image.load("image/pet_sprite_rev.png"),
    "cat": pygame.image.load("image/pet_cat_rev.png"),
}
imgHero = {
    "warrior": pygame.image.load("image/hero_warrior.png"),
    "guardian": pygame.image.load("image/hero_guardian.png"),
    "scholar": pygame.image.load("image/hero_scholar.png"),
    "scout": pygame.image.load("image/hero_scout.png"),
}
imgAchBadge = pygame.image.load("image/achievement_badge.png")
imgDamage = pygame.image.load("image/Damage.png")
imgFloor = [pygame.image.load("image/floor.png"),
            pygame.image.load("image/tbox.png"),
            pygame.image.load("image/cocoon.png"),
            pygame.image.load("image/stairs.png"),
            pygame.image.load("image/floor_trap.png"),
            pygame.image.load("image/floor_warp.png"),
            pygame.image.load("image/floor_healing_spring.png"),
            pygame.image.load("image/floor_curse.png"),
            pygame.image.load("image/floor_ice.png"),
            pygame.image.load("image/merchant.png")]
imgFloorCrystal = pygame.image.load("image/floor_crystal.png")
imgFloorFlame = pygame.image.load("image/floor_flame.png")
imgTboxCrystal = pygame.image.load("image/tbox_crystal.png")
imgTboxFlame = pygame.image.load("image/tbox_flame.png")
imgCocoonCrystal = pygame.image.load("image/cocoon_crystal.png")
imgCocoonFlame = pygame.image.load("image/cocoon_flame.png")
imgHealingSpringCrystal = pygame.image.load("image/floor_healing_spring_crystal.png")
imgHealingSpringFlame = pygame.image.load("image/floor_healing_spring_flame.png")
imgTrapCrystal = pygame.image.load("image/floor_trap_crystal.png")
imgTrapFlame = pygame.image.load("image/floor_trap_flame.png")
imgWarpCrystal = pygame.image.load("image/floor_warp_crystal.png")
imgWarpFlame = pygame.image.load("image/floor_warp_flame.png")
imgIdol = pygame.image.load("image/floor_idol.png")
imgIdolCrystal = pygame.image.load("image/floor_idol_crystal.png")
imgIdolFlame = pygame.image.load("image/floor_idol_flame.png")
imgBoulder = pygame.image.load("image/boulder.png")
imgShrine = pygame.image.load("image/floor_shrine.png")
imgShrineCrystal = pygame.image.load("image/floor_shrine_crystal.png")
imgShrineFlame = pygame.image.load("image/floor_shrine_flame.png")
imgCaptive = pygame.image.load("image/floor_captive.png")
imgCaptiveCrystal = pygame.image.load("image/floor_captive_crystal.png")
imgCaptiveFlame = pygame.image.load("image/floor_captive_flame.png")
imgRift = pygame.image.load("image/floor_rift.png")
imgRiftCrystal = pygame.image.load("image/floor_rift_crystal.png")
imgRiftFlame = pygame.image.load("image/floor_rift_flame.png")
imgAltar = pygame.image.load("image/floor_altar.png")
imgAltarCrystal = pygame.image.load("image/floor_altar_crystal.png")
imgAltarFlame = pygame.image.load("image/floor_altar_flame.png")
imgPressurePlate = pygame.image.load("image/floor_pressure_plate.png")
imgPressurePlateCrystal = pygame.image.load("image/floor_pressure_plate_crystal.png")
imgPressurePlateFlame = pygame.image.load("image/floor_pressure_plate_flame.png")
imgSealedDoor = pygame.image.load("image/floor_sealed_door.png")
imgSealedDoorCrystal = pygame.image.load("image/floor_sealed_door_crystal.png")
imgSealedDoorFlame = pygame.image.load("image/floor_sealed_door_flame.png")
imgSealedDoorOpen = pygame.image.load("image/floor_sealed_door_open.png")
imgSealedDoorOpenCrystal = pygame.image.load("image/floor_sealed_door_open_crystal.png")
imgSealedDoorOpenFlame = pygame.image.load("image/floor_sealed_door_open_flame.png")
imgSpirit = pygame.image.load("image/floor_spirit.png")
imgSpiritCrystal = pygame.image.load("image/floor_spirit_crystal.png")
imgSpiritFlame = pygame.image.load("image/floor_spirit_flame.png")
imgBountyBoard = pygame.image.load("image/floor_bounty_board.png")
imgBountyBoardCrystal = pygame.image.load("image/floor_bounty_board_crystal.png")
imgBountyBoardFlame = pygame.image.load("image/floor_bounty_board_flame.png")
imgTotem = pygame.image.load("image/floor_totem.png")
imgTotemCrystal = pygame.image.load("image/floor_totem_crystal.png")
imgTotemFlame = pygame.image.load("image/floor_totem_flame.png")
imgMirror = pygame.image.load("image/floor_mirror.png")
imgMirrorCrystal = pygame.image.load("image/floor_mirror_crystal.png")
imgMirrorFlame = pygame.image.load("image/floor_mirror_flame.png")
imgMapFragment = pygame.image.load("image/floor_map_fragment.png")
imgMapFragmentCrystal = pygame.image.load("image/floor_map_fragment_crystal.png")
imgMapFragmentFlame = pygame.image.load("image/floor_map_fragment_flame.png")
imgSacredKey = pygame.image.load("image/floor_sacred_key.png")
imgSacredKeyCrystal = pygame.image.load("image/floor_sacred_key_crystal.png")
imgSacredKeyFlame = pygame.image.load("image/floor_sacred_key_flame.png")
imgVault = pygame.image.load("image/floor_vault.png")
imgVaultCrystal = pygame.image.load("image/floor_vault_crystal.png")
imgVaultFlame = pygame.image.load("image/floor_vault_flame.png")
imgStatue = pygame.image.load("image/floor_statue.png")
imgStatueCrystal = pygame.image.load("image/floor_statue_crystal.png")
imgStatueFlame = pygame.image.load("image/floor_statue_flame.png")
imgGamblingDen = pygame.image.load("image/floor_gambling_den.png")
imgGamblingDenCrystal = pygame.image.load("image/floor_gambling_den_crystal.png")
imgGamblingDenFlame = pygame.image.load("image/floor_gambling_den_flame.png")
imgChimeraLair = pygame.image.load("image/floor_chimera_lair.png")
imgChimeraLairCrystal = pygame.image.load("image/floor_chimera_lair_crystal.png")
imgChimeraLairFlame = pygame.image.load("image/floor_chimera_lair_flame.png")
imgPlayer = [pygame.image.load("image/mychr0.png"),
             pygame.image.load("image/mychr1.png"),
             pygame.image.load("image/mychr2.png"),
             pygame.image.load("image/mychr3.png"),
             pygame.image.load("image/mychr4.png"),
             pygame.image.load("image/mychr5.png"),
             pygame.image.load("image/mychr6.png"),
             pygame.image.load("image/mychr7.png"),
             pygame.image.load("image/mychr8.png")]
# Hero(職業)ごとに見た目が変わるダンジョン歩行スプライト。
# warriorは既存のmychr*.pngをそのまま使い、他の職業は専用の配色違い画像を使う。
imgPlayerSets = {
    "warrior": imgPlayer,
    "guardian": [pygame.image.load(f"image/mychr_guardian{i}.png") for i in range(9)],
    "scholar": [pygame.image.load(f"image/mychr_scholar{i}.png") for i in range(9)],
    "scout": [pygame.image.load(f"image/mychr_scout{i}.png") for i in range(9)],
}

imgEffect = [pygame.image.load("image/effect_a.png"),
             pygame.image.load("image/effect_b.png")]

def _convert_loaded_images():
    """起動時に読み込んだimg*系のSurfaceを、画面のピクセルフォーマットに
    一括で変換(convert_alpha)しておく。未変換のSurfaceは毎回blit時に暗黙の
    フォーマット変換が走って遅くなるため、pygame.display.set_mode()の直後に
    一度だけ呼ぶ(display作成前はconvert_alpha()できないのでモジュール読み込み
    時点では行えない)。imgPlayerSetsのようなlist/dictのネストにも対応する。"""
    def conv(obj):
        if isinstance(obj, pygame.Surface):
            return obj.convert_alpha()
        elif isinstance(obj, list):
            return [conv(o) for o in obj]
        elif isinstance(obj, dict):
            return {k: conv(v) for k, v in obj.items()}
        return obj
    g = globals()
    for name in list(g.keys()):
        if name.startswith("img"):
            g[name] = conv(g[name])

speed = 6
idx = 0
tmr = 0
floor = 0
fl_max = 1
welcome = 0

#追加
moving = False
move_dx = 0
move_dy = 0
move_progress = 0.0
# 探索中は高フレームレート(WALK_FPS)で描画するので、
# 1マス移動にかかる実時間が以前と近くなるよう基準速度も合わせて下げてある
base_move_speed = 0.058
MOVE_SPEED = base_move_speed * (1 + (speed - 1) * 0.15)

hold_dir = None
hold_timer = 0.0
hold_delay = 9
hold_interval = 3

# 移動アニメーション中に押された方向キーを覚えておき、アニメーションが
# 終わった瞬間に間を空けず次の移動へつなげるための「先読み入力」
queued_dir = None

pl_x = 0
pl_y = 0
pl_d = 0
pl_a = 0
pl_lifemax = 0
pl_life = 0
pl_str = 0
pl_lv = 1
pl_exp = 0
pl_exp_mult = 1.0
pl_charge = False
pl_poison = 0

# --- 低HP警告 ---
# 残りHPが最大値の一定割合を切ったとき、数値を読まなくても直感的に
# 危険な状態だとわかるよう、画面端を脈打つ赤で縁取る演出を入れる。
LOW_HP_WARNING_RATIO = 0.2

# ステータスパネルのHP数値を、危険度が上がるほど早めに気づけるようにする中間警告。
# 従来はHPが絶対値で10を切った瞬間だけ赤く点滅していたが、最大HPが大きい
# キャラクター(Guardianなど)ではその頃には手遅れに近く、逆に最大HPが低い
# 序盤では過敏に点滅していた。境界を割合(画面端の低HP警告と同じ20%)に揃え、
# その手前の50%からオレンジで予兆を出すようにする。
HP_MID_WARNING_RATIO = 0.5
HP_MID_WARNING_COLOR = (255, 165, 0)

# --- 食料残量の事前警告 ---
# 従来は食料が完全に尽きた(0になった)瞬間しか赤く点滅せず、飢餓による
# ダメージを受けてから慌ててポーション/食料を探すことになりがちだった。
# 0になる前にオレンジ色で点滅させ、余裕を持って食料を確保できるようにする。
FOOD_LOW_WARNING_THRESHOLD = 30
FOOD_LOW_WARNING_COLOR = (255, 165, 0)

# ポーションが尽きた(0本)ことを一目で気づけるようにする表示色。
# 従来は"0"という数字が他の数値と同じ白色で表示されるだけで見落としやすかった。
POTION_EMPTY_COLOR = (140, 140, 140)

# --- ポーション/爆炎石の残り僅か警告 ---
# 従来は0本になった瞬間に灰色化するだけで、「残り1本」の時点では他の数値と
# 同じ白色のままだった。食料の事前警告(FOOD_LOW_WARNING_THRESHOLD)と同じ
# 考え方で、尽きる前にオレンジ色の点滅で気づけるようにする。
POTION_LOW_WARNING_THRESHOLD = 1
POTION_LOW_WARNING_COLOR = (255, 165, 0)

# --- 難易度システム ---
DIFFICULTY_LIST = ["Easy", "Normal", "Hard"]
difficulty = "Normal"
food_acc = 0.0  # 食料消費のペース補正で生じる端数をためておくアキュムレータ
BASE_VISION_RADIUS = 5  # ミニマップの基本可視範囲(ここに難易度補正が乗る)

# --- 音量設定 ---
# これまでBGM/SEの音量調整手段が無く、ユーザーが自分の環境で音量を
# 調整できなかったため設定画面を追加する。デフォルトは1.0(=これまで通り
# set_volume未呼び出しの状態と同じ音量)にして、既存プレイヤーの体感を変えない。
VOLUME_STEP = 0.1
bgm_volume = 1.0
se_volume = 1.0
# 音量スライダーを毎回0にせずとも即座に無音化したい場面(来客対応・夜間プレイ等)
# のためのミュート。ON中もbgm_volume/se_volumeの値自体は保持し、解除時に元の
# 音量へ戻せるようにする。Mキーでいつでもトグル可能。
muted = False
# 被弾やクリティカル演出のたびに画面が揺れる画面シェイクは、乗り物酔いしやすい
# プレイヤーや目が疲れやすい環境では不快に感じることがあるため、設定画面から
# オフにできるようにする(デフォルトはON=これまで通りの挙動)。
screen_shake_enabled = True
# クリティカル/コンボフィニッシャー/レア発見などの画面フラッシュ演出も、
# 画面シェイクと同様に光過敏なプレイヤーには負担になりうるため、
# 個別にオフにできるようにする(デフォルトはON)。
screen_flash_enabled = True
settings_cursor = 0  # 設定画面でのカーソル位置(0=BGM, 1=SE, 2=Mute All, 3=Screen Shake, 4=Screen Flash)

DIFFICULTY_PARAMS = {
    "Easy": dict(
        enemy_str_mult=0.75, enemy_life_mult=0.75,
        exp_mult=1.3,
        item_bonus=15,
        growth_mult=1.3,
        pl_lifemax_bonus=100, pl_str_bonus=20, pl_def_bonus=5,
        maze_step_bonus=-1,
        food_consume_mult=1/3, heal_per_step=2, starve_dmg=3,
        trap_dmg_mult=0.6, trap_rate_mult=0.6,
        poison_decay_per_step=1,
        minimap_enabled=True, minimap_full_reveal=True, vision_radius_bonus=2,
    ),
    "Normal": dict(
        enemy_str_mult=1.0, enemy_life_mult=1.0,
        exp_mult=1.0,
        item_bonus=0,
        growth_mult=1.0,
        pl_lifemax_bonus=0, pl_str_bonus=0, pl_def_bonus=0,
        maze_step_bonus=0,
        food_consume_mult=1/2, heal_per_step=1, starve_dmg=5,
        trap_dmg_mult=1.0, trap_rate_mult=1.0,
        poison_decay_per_step=2,
        minimap_enabled=True, minimap_full_reveal=False, vision_radius_bonus=0,
    ),
    "Hard": dict(
        enemy_str_mult=1.3, enemy_life_mult=1.3,
        exp_mult=0.8,
        item_bonus=-15,
        growth_mult=0.8,
        pl_lifemax_bonus=-50, pl_str_bonus=-10, pl_def_bonus=-3,
        maze_step_bonus=1,
        food_consume_mult=1.0, heal_per_step=1, starve_dmg=8,
        trap_dmg_mult=1.5, trap_rate_mult=2.0,
        poison_decay_per_step=3,
        minimap_enabled=False, minimap_full_reveal=False, vision_radius_bonus=-2,
    ),
}

def diff_params():
    return DIFFICULTY_PARAMS[difficulty]

# --- ボスフロア・実績システム ---
BOSS_FLOOR_INTERVAL = 10
boss_floors_cleared = set()
in_boss_battle = False
battle_took_damage = False
curse_active = False
hidden_treasure_pos = None
pending_bonus_room = False

# --- コンボ(連携攻撃)システム ---
# 通常攻撃[A]を連続で選ぶとコンボ数が増え、攻撃力にボーナスがかかる。
# ポーション/ブレイズジェム/逃げる/防御を選ぶとリセットされる(Focusはリセットしない)。
combo_count = 0
COMBO_MAX_BONUS_STACKS = 5  # これ以上は頭打ち(+50%)
# そのバトル中に「歴代最高コンボ更新」の演出を既に出したかどうか。連続ヒットの
# たびに毎回演出すると煩わしいため、1バトルにつき一度だけに絞る。
combo_record_shown_this_battle = False

def combo_damage_mult():
    return 1.0 + modifier_combo_bonus_per_stack() * min(max(0, combo_count - 1), COMBO_MAX_BONUS_STACKS)

# --- コンボ・フィニッシャー(コンボを高く積み上げた末の大技) ---
# 通常のコンボ補正が頭打ちになった後もコンボを繋ぎ続け、しきい値に達した状態で
# 攻撃を出すと、ひときわ派手な大ダメージの一撃が発動する。発動後はコンボが
# リセットされるので、また一から積み上げて次のフィニッシャーを狙う緊張感が生まれる。
COMBO_FINISHER_THRESHOLD = 8
COMBO_FINISHER_MULT = 2.2
MASSIVE_HIT_THRESHOLD = 500  # 一撃でこのダメージ以上を叩き出すと「MASSIVE HIT!」演出が発生

# --- 逃走(Run)成功率 ---
FLEE_CHANCE_PCT = 60

def flee_chance_pct():
    """基本の逃走成功率にフロア特性(Tranquil Floor)のボーナスを加える"""
    return min(95, FLEE_CHANCE_PCT + modifier_flee_bonus())

# --- ボスの複数フェーズ演出 ---
# ボスのHPが半分を切ると、1度だけ「激怒」して攻撃力が上がる。
boss_phase2 = False
BOSS_PHASE2_STR_MULT = 1.3

# --- ペット(仲間)システム ---
PET_TYPES = {
    "slime": {"name": "Slime Pal", "desc": "10% chance to assist-attack"},
    "sprite": {"name": "Guardian Sprite", "desc": "+3 DEF while active"},
    "cat":    {"name": "Lucky Cat", "desc": "+5 item find while active"},
}
pet_type = None
pet_def_bonus = 0
pet_item_bonus = 0

def hatch_random_pet():
    """卵を拾った瞬間にランダムな仲間が孵る。既に仲間がいる場合は何もしない
    (呼び出し側でポーション等の代替報酬を渡す)"""
    global pet_type, pet_def_bonus, pet_item_bonus
    if pet_type is not None:
        return False
    pet_type = random.choice(list(PET_TYPES.keys()))
    pet_def_bonus = 3 if pet_type == "sprite" else 0
    pet_item_bonus = 5 if pet_type == "cat" else 0
    return True

# --- デイリーチャレンジ(シード固定モード) ---
daily_mode = False
daily_start_requested = False
# ヒーロー選択画面でキャラクターを選んでEnterを押すと、そのままゲームを
# 開始できるようにするフラグ(タイトル画面へ戻ってから改めてSPACEを押す
# 、というわかりにくい2段階の操作を無くすため)
hero_start_requested = False

# --- タイトル画面の階層メニュー ---
# トップ階層: [T]難易度 / [G]ゲームデータ(→ロード・コンティニュー) / [R]記録(→実績・統計)
#            / [Y]デイリー / [H]隠しステージ
# キーボードとマウスクリックの両方から同じ処理を呼べるよう、操作は関数化してある。
title_menu_rects = []  # このフレームで描画したクリック可能領域: (x,y,w,h,action)

def register_menu_rect(x, y, w, h, action):
    title_menu_rects.append((x, y, w, h, action))

def point_in_rect(px, py, rect):
    x, y, w, h = rect
    return x <= px <= x+w and y <= py <= y+h

def hit_test_menu(px, py):
    for (x, y, w, h, action) in title_menu_rects:
        if point_in_rect(px, py, (x, y, w, h)):
            return action
    return None

_btn_surface_cache = {}

def _lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def _clamp_color(c):
    return tuple(max(0, min(255, int(v))) for v in c)

def _build_glossy_button(w, h, color, radius):
    """モバイルゲーム風の『つやのある立体ボタン』画像をその場で描いて返す。
    同じ(サイズ,色,角丸)の組み合わせは初回だけ生成してキャッシュし、
    毎フレーム描き直すコストを避ける。"""
    key = (w, h, color, radius)
    cached = _btn_surface_cache.get(key)
    if cached is not None:
        return cached
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    # 外枠(メタリックなグレーの縁取り)
    pygame.draw.rect(surf, (100, 100, 108), [0, 0, w, h], border_radius=radius)
    pygame.draw.rect(surf, (215, 215, 222), [0, 0, w, h], width=2, border_radius=radius)
    # 内側: 上が明るく下が暗い縦グラデーションの本体(角丸マスクをかけてから乗算する)
    pad = 4
    iw, ih = w - pad*2, h - pad*2
    irad = max(0, radius - pad)
    if iw > 0 and ih > 0:
        top_c = _clamp_color(tuple(c*1.5 + 45 for c in color))
        bot_c = _clamp_color(tuple(c*0.55 for c in color))
        mask = pygame.Surface((iw, ih), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), [0, 0, iw, ih], border_radius=irad)
        grad = pygame.Surface((iw, ih), pygame.SRCALPHA)
        for yy in range(ih):
            t = yy / max(1, ih - 1)
            col = _lerp_color(top_c, bot_c, t)
            pygame.draw.line(grad, (*col, 255), (0, yy), (iw, yy))
        mask.blit(grad, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(mask, (pad, pad))
        # 上部の光沢(半透明の白い楕円)
        gloss_w = int(iw * 0.86)
        gloss_h = max(1, int(ih * 0.42))
        gloss = pygame.Surface((gloss_w, gloss_h), pygame.SRCALPHA)
        pygame.draw.ellipse(gloss, (255, 255, 255, 75), [0, 0, gloss_w, gloss_h])
        surf.blit(gloss, (pad + (iw - gloss_w)//2, pad + int(ih*0.06)))
    _btn_surface_cache[key] = surf
    return surf

def draw_button(screen, font, x, y, w, h, label, action=None,
                 base_color=(90, 120, 200), mouse_pos=None, enabled=True, align="left"):
    """クリック可能なメニュー項目を、つやのある立体的な『ボタン』として描画する。
    マウスカーソルが乗っていれば色を明るくし白い縁取りを足してハイライトし、
    enabled=Falseの場合はクリック領域を登録せずグレーアウト表示のみ行う
    (「ロードデータ無し」など、押せない項目の見た目を揃えるために使う)。
    戻り値はホバー中かどうか(呼び出し側で追加の演出をしたい場合に使える)。"""
    hovered = enabled and mouse_pos is not None and point_in_rect(mouse_pos[0], mouse_pos[1], (x, y, w, h))
    if not enabled:
        color = (92, 92, 98)
    elif hovered:
        color = _clamp_color(tuple(c + 35 for c in base_color))
    else:
        color = base_color
    radius = h // 2
    btn_surf = _build_glossy_button(w, h, color, radius)
    screen.blit(btn_surf, [x, y])
    if hovered:
        pygame.draw.rect(screen, WHITE, [x, y, w, h], width=2, border_radius=radius)
    tw, th = font.size(label)
    ty = y + (h - th)//2 - 1
    tx = x + (w - tw)//2 if align == "center" else x + int(w*0.10)
    text_col = WHITE if enabled else (165, 165, 165)
    draw_text(screen, label, int(tx), ty, font, text_col)
    if enabled and action is not None:
        register_menu_rect(x, y, w, h, action)
    return hovered

def toggle_difficulty():
    global difficulty
    di = (DIFFICULTY_LIST.index(difficulty) + 1) % len(DIFFICULTY_LIST)
    difficulty = DIFFICULTY_LIST[di]

def start_hidden_stage_challenge():
    """タイトル画面から隠しボスへ挑戦する処理(キーボード/マウス共通)。
    全3ステージクリア(game_clear実績)が条件。"""
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_def_buff, def_pill
    global food, food_acc, potion, blazegem, pl_poison, pl_charge, battle_took_damage
    global in_boss_battle, in_hidden_stage, floor, idx, tmr
    dp = diff_params()
    cp = char_params()
    if pl_lifemax <= 0:
        # このセッションでまだキャラクターを作っていない場合、
        # 裏ボス挑戦用にやや強めのステータスで即座に用意する
        pl_lifemax = 300 + dp["pl_lifemax_bonus"] + cp["lifemax"] + 200
        pl_life = pl_lifemax
        pl_str = 100 + dp["pl_str_bonus"] + cp["str"] + 50
        pl_def_base = 0 + dp["pl_def_bonus"] + cp["def"] + 20
        pl_def_buff = 0
        def_pill = 2
        food = 300
        food_acc = 0.0
        potion = 3
        blazegem = 3
    pl_poison = 0
    pl_charge = False
    battle_took_damage = False
    in_boss_battle = True
    in_hidden_stage = True
    floor = HIDDEN_FLOOR
    init_hidden_boss_battle()
    init_message()
    pygame.mixer.music.load("sound/natsuyasuminotanken.mp3")
    pygame.mixer.music.play(-1)
    idx = 40
    tmr = 0

def daily_seed_for_today():
    import datetime, hashlib
    date_str = datetime.date.today().isoformat()
    return int(hashlib.md5(date_str.encode()).hexdigest(), 16) % (2**31)

def load_daily_record():
    try:
        with open("daily.json", "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
    import datetime
    today = datetime.date.today().isoformat()
    history = data.get("history", [])
    if data.get("date") != today:
        # 日付が変わったら、進捗のあった前日分の記録をランキング履歴に積んでおく
        prev_date = data.get("date")
        if prev_date and (data.get("best_floor", 0) > 0 or data.get("cleared", False)):
            history.append({"date": prev_date, "best_floor": data.get("best_floor", 0), "cleared": data.get("cleared", False)})
            history = history[-30:]  # 直近30日分だけ保持する
        data = {"date": today, "best_floor": 0, "cleared": False, "history": history}
    data.setdefault("best_floor", 0)
    data.setdefault("cleared", False)
    data.setdefault("history", history)
    return data

def save_daily_record(data):
    try:
        with open("daily.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        _log_io_error("save_daily_record", e)

def record_daily_result(floor_reached, cleared):
    data = load_daily_record()
    if floor_reached > data.get("best_floor", 0):
        data["best_floor"] = floor_reached
    if cleared:
        data["cleared"] = True
    save_daily_record(data)

# --- ステージシステム ---
# ダンジョンを STAGE_LENGTH(30)階ごとに区切り、全 STAGE_COUNT(3) ステージで1周のゲームとする。
# 各ステージの中では10階・20階・30階(ステージ内の相対階数)ごとにボスが登場し、
# 最終ステージの30階(=global floor 90)のボスを倒すとゲームクリアになる。
STAGE_LENGTH = 30
STAGE_COUNT = 3
MAX_FLOOR = STAGE_LENGTH * STAGE_COUNT

# --- 隠しステージ(裏ボス) ---
# 全3ステージクリア(game_clear実績)後、タイトル画面から挑戦できる特別な一体。
# 通常のダンジョン生成は行わず、専用の強敵といきなり戦う一発勝負のコンテンツ。
HIDDEN_FLOOR = MAX_FLOOR + 1
HIDDEN_BOSS_IMAGE = "enemy20.png"
in_hidden_stage = False

# ステージごとの画面色調(ダンジョン探索中にうっすら重ねる色。Noneなら色調補正なし)
STAGE_TINTS = {
    1: None,
    2: (40, 70, 150),
    3: (140, 20, 20),
}

stage_intro_timer = 0
stage_intro_num = 1

# --- フロア特性(Floor Modifier) ---
# フロアごとに一定確率でランダムな特性が発生し、見た目(背景の色調)と
# プレイ内容(視界・食料消費・回復量・移動速度・罠の出やすさ・宝箱の出やすさ)に
# 軽い変化を与えることで、ダンジョンが単調にならないようにする。
FLOOR_MODIFIERS = {
    "foggy":     {"name": "Foggy Floor",     "desc": "Vision is limited here",      "color": (110, 110, 150)},
    "bountiful": {"name": "Bountiful Floor",  "desc": "Treasure is more common",     "color": (255, 215, 0)},
    "quiet":     {"name": "Quiet Floor",      "desc": "Fewer traps here",            "color": (120, 200, 150)},
    "windy":     {"name": "Windy Floor",      "desc": "You move faster here",        "color": (150, 210, 255)},
    "chilly":    {"name": "Chilly Floor",     "desc": "Food drains faster here",     "color": (120, 170, 220)},
    "blessed":   {"name": "Blessed Floor",    "desc": "Healing is stronger here",    "color": (255, 235, 170)},
    "rocky":     {"name": "Rocky Floor",      "desc": "+3 DEF here, but you move slower", "color": (120, 100, 80)},
    "toxic":     {"name": "Toxic Floor",      "desc": "Enemies poison you more often",  "color": (120, 170, 60)},
    "sparkling": {"name": "Sparkling Floor",  "desc": "EXP gained here is boosted",   "color": (255, 180, 240)},
    "serene":    {"name": "Serene Floor",     "desc": "Poison cannot affect you here", "color": (170, 255, 220)},
    "fortunate": {"name": "Fortunate Floor",  "desc": "Critical hits land more often here", "color": (255, 200, 80)},
    "resonant":  {"name": "Resonant Floor",   "desc": "Combo damage bonus grows faster here", "color": (255, 120, 220)},
    "frostbound": {"name": "Frostbound Floor", "desc": "Enemy attacks hit softer here", "color": (140, 210, 255)},
    "empowered": {"name": "Empowered Floor",  "desc": "Your attacks hit harder here",  "color": (255, 90, 60)},
    "verdant":   {"name": "Verdant Floor",    "desc": "Food drains slower here",       "color": (100, 200, 90)},
    "tranquil":  {"name": "Tranquil Floor",   "desc": "Fleeing succeeds more often here", "color": (180, 230, 210)},
    "cursed":    {"name": "Cursed Floor",     "desc": "Enemies hit harder, but treasure is richer", "color": (170, 30, 110)},
    "veiled":    {"name": "Veiled Floor",     "desc": "Fewer monsters lurk here",      "color": (95, 65, 135)},
    "clear":     {"name": "Clear Floor",      "desc": "The full map is revealed here", "color": (200, 235, 255)},
    "elite_grounds": {"name": "Elite Grounds", "desc": "Elite monsters are far more common here", "color": (255, 150, 30)},
    "opulent":   {"name": "Opulent Floor",   "desc": "Treasure chests are much more common here", "color": (255, 195, 60)},
    "radiant":   {"name": "Radiant Floor",   "desc": "Critical hits deal much more damage here", "color": (255, 245, 180)},
    "merciful":  {"name": "Merciful Floor",  "desc": "Traps hurt much less here",     "color": (200, 255, 210)},
    "warded":    {"name": "Warded Floor",    "desc": "Curse tiles have no effect here", "color": (200, 220, 255)},
    "bazaar":    {"name": "Bazaar Floor",    "desc": "The traveling merchant trades for less here", "color": (255, 225, 140)},
    "genuine":   {"name": "Genuine Floor",   "desc": "Treasure chests are never Mimics here", "color": (210, 240, 200)},
    "fertile":   {"name": "Fertile Floor",   "desc": "Food found here restores 50% more", "color": (160, 220, 90)},
    "volatile":  {"name": "Volatile Floor",  "desc": "Blaze Gems deal much more damage here", "color": (255, 110, 40)},
    "torchlit":  {"name": "Torchlit Floor",  "desc": "Vision is wider here",         "color": (255, 200, 120)},
    "peaceful":  {"name": "Peaceful Floor",  "desc": "No Elite monsters appear here", "color": (180, 255, 200)},
    "barren":    {"name": "Barren Floor",    "desc": "Passive healing is weaker here", "color": (140, 120, 100)},
}
floor_modifier = None  # 現在のフロアの特性id(Noneなら特性なし)

def roll_floor_modifier(fl):
    """フロア2以降、40%の確率でランダムな特性を1つ選ぶ(フロア1は操作に慣れてもらうため無し)"""
    if fl <= 1:
        return None
    if random.randint(0, 99) < 40:
        return random.choice(list(FLOOR_MODIFIERS.keys()))
    return None

def modifier_vision_delta():
    if floor_modifier == "foggy":
        return -2
    if floor_modifier == "torchlit":
        return 2
    return 0

def modifier_item_bonus():
    if floor_modifier == "bountiful":
        return 20
    if floor_modifier == "cursed":
        return 25
    return 0

def modifier_trap_mult():
    return 0.3 if floor_modifier == "quiet" else 1.0

def modifier_speed_mult():
    return 1.3 if floor_modifier == "windy" else 1.0

def modifier_food_mult():
    if floor_modifier == "chilly":
        return 1.5
    if floor_modifier == "verdant":
        return 0.6
    return 1.0

def modifier_heal_mult():
    """Blessed Floorでは歩数ごとの受動回復(heal_per_step)が2倍になる。
    対になる「はずれ」特性のBarren Floorでは、同じ受動回復が半分に弱まる
    (Blessedがこれまで倍増する方向のみだったため、逆方向の特性が無かった
    穴を埋める新しい方向性として追加した)。"""
    if floor_modifier == "blessed":
        return 2.0
    if floor_modifier == "barren":
        return 0.5
    return 1.0

def modifier_def_bonus():
    return 3 if floor_modifier == "rocky" else 0

def modifier_rocky_speed_mult():
    return 0.85 if floor_modifier == "rocky" else 1.0

def modifier_poison_chance_bonus():
    return 25 if floor_modifier == "toxic" else 0

def modifier_exp_mult():
    return 1.3 if floor_modifier == "sparkling" else 1.0

def modifier_poison_immune():
    return floor_modifier == "serene"

def modifier_crit_chance_bonus():
    return 0.15 if floor_modifier == "fortunate" else 0.0

def modifier_combo_bonus_per_stack():
    return 0.15 if floor_modifier == "resonant" else 0.1

def modifier_incoming_dmg_mult():
    if floor_modifier == "frostbound":
        return 0.85
    if floor_modifier == "cursed":
        return 1.15
    return 1.0

def modifier_atk_mult():
    return 1.15 if floor_modifier == "empowered" else 1.0

def modifier_flee_bonus():
    return 20 if floor_modifier == "tranquil" else 0

def modifier_encounter_mult():
    """Veiled Floorではフロア生成時にモンスターの遭遇マス(event_pool内の2)を
    間引き、通常より静かに探索できるようにする倍率。"""
    return 0.5 if floor_modifier == "veiled" else 1.0

def modifier_minimap_full_reveal():
    """Clear Floorでは、そのフロアに限り難易度設定に関係なくミニマップが
    最初から全開放される(Easy専用だった全開放をフロア特性として体験できる)。"""
    return floor_modifier == "clear"

def modifier_elite_chance_bonus():
    """Elite Groundsでは、通常戦闘のエリート化確率(ELITE_CHANCE)に上乗せする
    ボーナス(%pt)を返す。エリートは強い代わりに経験値ボーナスが付くため、
    危険度と引き換えに稼ぎやすくなるハイリスク・ハイリターンの特性。
    対になる「当たり」特性のPeaceful Floorでは、同じ12%ptを差し引いて
    ELITE_CHANCEをちょうど0にし、そのフロアではElite化した敵に遭遇しなくなる
    (Elite Groundsが確率を上乗せする方向のみだったため、逆方向の安全な
    フロア特性が無かった穴を埋める新しい方向性として追加した)。"""
    if floor_modifier == "elite_grounds":
        return 12
    if floor_modifier == "peaceful":
        return -12
    return 0

def modifier_treasure_weight_mult():
    """Opulent Floorでは、フロア生成時の宝箱(event_pool内の1)の出現重みが
    増える。bountiful/cursedは獲得アイテムの「質」を上げる特性だったが、
    こちらは宝箱そのものの「数」を増やす新しい方向性の特性。"""
    return 2.0 if floor_modifier == "opulent" else 1.0

def modifier_crit_dmg_mult():
    """Radiant Floorでは、クリティカルヒットの倍率が通常のx2からx2.5に上がる。
    fortunate(発生率)やempowered(通常攻撃力)はこれまであったが、
    クリティカル自体の「威力」を伸ばす特性が無かったため追加した。"""
    return 2.5 if floor_modifier == "radiant" else 2.0

def modifier_trap_dmg_mult():
    """Merciful Floorでは、罠(通常の罠・罠の宝箱)によるダメージが30%軽減される。
    quiet(遭遇頻度そのものを下げる)とは別の角度で、踏んでしまった罠の
    「痛さ」自体を和らげる、初めての防御寄り特性。"""
    return 0.7 if floor_modifier == "merciful" else 1.0

def modifier_curse_immune():
    """Warded Floorでは、呪いの床(STR/DEFが下がるタイル)を踏んでも
    デバフを受けない。serene(毒を無効化)と同じ「特定の状態異常を
    まるごと防ぐ」方向性を、呪いの床に対しても持たせた特性。"""
    return floor_modifier == "warded"

def modifier_trade_cost_mult():
    """Bazaar Floorでは、フロア探索中に出会う旅の商人(idx==48)との
    取引コストが25%引きになる。これまでのフロア特性は入手量や被ダメージなど
    プレイヤーの戦闘・探索能力に関わるものばかりで、アイテム交換の
    「コスト」自体に関わる経済寄りの特性が無かったため、新しい方向性として
    追加した。"""
    return 0.75 if floor_modifier == "bazaar" else 1.0

def merchant_trade_cost(base):
    """旅の商人での取引コストにmodifier_trade_cost_mult()を適用した実際の
    コストを返す(最低1を保証)。Bazaar Floorでなければbaseのまま。"""
    return max(1, int(base * modifier_trade_cost_mult()))

def modifier_mimic_immune():
    """Genuine Floorでは、宝箱を開けた時にミミックが混ざらなくなる。
    これまでのフロア特性はダメージ・遭遇頻度・コストなどに関わるものばかりで、
    「宝箱の安全性」自体に関わる特性が無かったため、新しい方向性として追加した。"""
    return floor_modifier == "genuine"

def modifier_food_yield_mult():
    """Fertile Floorでは、探索中に見つかる食料アイテムの回復量が1.5倍になる。
    chilly/verdantは食料の「消費速度」に関わる特性だったが、拾った食料自体の
    「量」を増やす特性が無かったため、新しい方向性として追加した。"""
    return 1.5 if floor_modifier == "fertile" else 1.0

def modifier_blaze_dmg_mult():
    """Volatile Floorでは、爆炎石(Blaze Gem)の与えるダメージが1.5倍になる。
    従来のフロア特性は通常攻撃・クリティカル・被ダメージなどには関わっていたが、
    アイテムとして使う爆炎石そのものの威力に関わる特性が無かったため、
    新しい方向性として追加した。"""
    return 1.5 if floor_modifier == "volatile" else 1.0

# --- 床の彩色パッチ(見た目だけの演出) ---
# フロアの一部区画をランダムな色合いに染めて、同じ床タイルの繰り返しでも
# 単調に見えないようにする(ゲームプレイには影響しない純粋な見た目の変化)。
PATCH_COLORS = [
    (90, 130, 70),    # 苔むした緑
    (150, 110, 60),   # 砂っぽい茶色
    (110, 80, 130),   # 紫がかった岩
    (160, 100, 40),   # 錆びたオレンジ
    (80, 100, 110),   # くすんだ青灰色
    (140, 60, 60),    # 赤褐色
    (60, 120, 140),   # 深い水色
    (120, 140, 60),   # 深緑がかった黄
    (150, 90, 130),   # 明るい紫紅色
    (170, 150, 90),   # 明るい黄土色
    (70, 70, 70),     # 灰色
    (60, 140, 120),   # ティール系の緑
    (160, 80, 30),    # 焼けたオレンジ
    (90, 50, 50),     # 暗い赤茶
    (50, 90, 50),     # 暗い森緑
    (120, 120, 170),  # 淡い藤色
    (180, 170, 100),  # 黄ばんだ石灰
    (40, 60, 90),     # 暗い藍色
    (150, 120, 120),  # くすんだローズ
    (100, 90, 150),   # 落ち着いた青紫
]
color_patches = []  # [(cx, cy, radius, color), ...]
_prev_patch_colors = []  # 前のフロアで使った色(次のフロアで繰り返さないようにする)

# --- 壁の色バリエーション ---
# フロアごとに壁の色調を変えて、同じ壁画像がずっと続く単調さを減らす。
WALL_TINTS = [
    None,               # 通常(無地、色補正なし)
    (120, 90, 70),      # 赤茶けた岩肌
    (70, 90, 110),      # 冷たい青灰色の岩肌
    (90, 110, 80),      # 苔むした岩肌
    (110, 80, 120),     # 紫がかった洞窟
    (130, 110, 60),     # 砂岩っぽい黄土色
    (150, 60, 60),      # 赤錆びた岩
    (60, 100, 140),     # 深い青の岩肌
    (100, 130, 60),     # 深緑の岩肌
    (140, 100, 150),    # 明るい紫の洞窟
    (160, 140, 90),     # 明るい砂色
    (80, 80, 80),       # 灰色の石壁
    (60, 130, 130),     # 青緑(ティール)の岩肌
    (150, 90, 40),      # 焼けたオレンジの岩
    (90, 60, 60),       # 暗い赤茶
    (60, 90, 60),       # 暗い森の緑
    (110, 110, 160),    # 淡い藤色
    (170, 170, 100),    # 黄ばんだ石灰岩
    (50, 70, 90),       # 暗い藍色の岩肌
    (140, 120, 120),    # くすんだローズ色
]
wall_tint = None  # 現在のフロアの壁色(Noneなら無地のまま)

def roll_wall_tint(previous=None):
    """次のフロアの壁色を選ぶ。直前のフロアと同じ色が連続しないよう、
    previousに渡した色は候補から除外する。"""
    candidates = [c for c in WALL_TINTS if c != previous]
    if not candidates:
        candidates = WALL_TINTS
    return random.choice(candidates)

# --- 壁/床/戦闘背景の見た目バリエーション(ステージテーマ) ---
# 色調ティントとは別に、壁と床の模様・戦闘背景そのものをステージごとに
# 差し替える: ステージ1=通常, ステージ2=クリスタル洞窟, ステージ3=火山(炎)。
# ランダムではなく現在のステージで一意に決まるので、同じステージの中では
# フロアが変わっても常に同じテーマの見た目になる。
wall_variant = 0    # 0=通常の壁, 1=クリスタル洞窟の壁, 2=炎の壁
floor_variant = 0   # 0=通常の床, 1=クリスタル洞窟の床, 2=炎の床

def stage_theme_variant(fl):
    """フロア番号(1始まり)からステージテーマ番号(0/1/2)を返す"""
    stg = current_stage(fl)
    return {1: 0, 2: 1, 3: 2}.get(stg, 0)

def battle_bg_for_floor(fl):
    """現在のフロアのステージテーマに応じた戦闘背景画像を返す。
    隠しステージ/エコーバトルなどfloorがMAX_FLOORを超える場合はcurrent_stageが
    STAGE_COUNTで頭打ちになるため、最終ステージ(炎)の背景になる。"""
    variant = stage_theme_variant(fl)
    if variant == 1:
        return imgBtlBGCrystal
    elif variant == 2:
        return imgBtlBGFlame
    return imgBtlBG

def bgm_field_for_floor(fl):
    """現在のフロアのステージテーマに応じた探索BGMのファイルパスを返す。
    ステージ1は既存のBGMのまま、ステージ2/3は新しく作成した専用曲を使う。"""
    variant = stage_theme_variant(fl)
    if variant == 1:
        return "sound/ohd_bgm_field_stage2.wav"
    elif variant == 2:
        return "sound/ohd_bgm_field_stage3.wav"
    return "sound/ohd_bgm_field.ogg"

def bgm_battle_for_floor(fl):
    """現在のフロアのステージテーマに応じた通常戦闘BGMのファイルパスを返す。
    ステージ1は既存のBGMのまま、ステージ2/3は新しく作成した専用曲を使う。"""
    variant = stage_theme_variant(fl)
    if variant == 1:
        return "sound/ohd_bgm_battle_stage2.wav"
    elif variant == 2:
        return "sound/ohd_bgm_battle_stage3.wav"
    return "sound/ohd_bgm_battle.ogg"

def generate_color_patches():
    """フロア生成時に0〜2個のランダムな彩色区画を作る。
    前のフロアで使った色は、このフロアでは選ばないようにする(連続を防ぐ)。"""
    global color_patches, _prev_patch_colors
    n = random.randint(0, 2)
    used_this_floor = []
    new_patches = []
    for _ in range(n):
        candidates = [c for c in PATCH_COLORS if c not in _prev_patch_colors and c not in used_this_floor]
        if not candidates:
            candidates = [c for c in PATCH_COLORS if c not in used_this_floor]
        if not candidates:
            candidates = PATCH_COLORS
        cx = random.randint(3, DUNGEON_W-4)
        cy = random.randint(3, DUNGEON_H-4)
        radius = random.randint(2, 4)
        color = random.choice(candidates)
        used_this_floor.append(color)
        new_patches.append((cx, cy, radius, color))
    color_patches = new_patches
    _prev_patch_colors = used_this_floor

def patch_color_at(x, y):
    """(x,y)がどれかの彩色区画に含まれていれば、その色を返す(無ければNone)"""
    for (cx, cy, radius, color) in color_patches:
        if abs(x-cx) <= radius and abs(y-cy) <= radius:
            return color
    return None

def current_stage(fl):
    """フロア番号(1始まり)が何ステージ目に属するかを返す(最大STAGE_COUNT)"""
    return min(STAGE_COUNT, (max(1, fl) - 1) // STAGE_LENGTH + 1)

def stage_local_floor(fl):
    """ステージ内での階数(1〜STAGE_LENGTH)を返す"""
    return (max(1, fl) - 1) % STAGE_LENGTH + 1

ACHIEVEMENT_DEFS = [
    ("game_clear", "Clear all 3 stages"),
    ("boss_defeat", "Defeat a stage boss"),
    ("no_damage_win", "Win a battle without taking damage"),
    ("hard_clear", "Clear all stages on Hard difficulty"),
    ("starve_survive", "Survive starvation (0 food)"),
    ("trap100", "Step on 100 traps"),
    ("hidden_boss_defeat", "Defeat the hidden boss"),
    ("skill_maxed", "Max out any single skill"),
    ("grandmaster", "Unlock the Grandmaster capstone skill"),
    ("echo_hunter", "Defeat an Echo Battle boss"),
    ("echo_master", "Defeat every Echo Battle boss at least once"),
    ("merchant_regular", "Trade with a merchant 5 times"),
    ("elite_hunter", "Defeat an Elite monster"),
    ("explorer", "Fully explore 10 floors"),
    ("golden_catch", "Catch a golden slime"),
    ("vault_escapee", "Escape a collapsing vault"),
    ("den_cleared", "Clear a monster den"),
    ("boulder_dodge", "Outrun a rolling boulder"),
    ("shrine_gambler", "Try your luck at a shrine"),
    ("blood_moon_survivor", "Clear a Blood Moon floor"),
    ("mimic_defeated", "Defeat a Mimic chest"),
    ("ally_rescued", "Rescue a captive ally"),
    ("rift_survivor", "Survive a rift's Elite encounter"),
    ("altar_sacrifice", "Make an offering at a sacrificial altar"),
    ("altar_boon", "Receive a boon from a sacrificial altar"),
    ("door_unlocked", "Trigger a pressure plate to unlock a sealed door"),
    ("spirit_blessed", "Receive a blessing from a wandering spirit"),
    ("bounty_hunter", "Complete a bounty board quest"),
    ("totem_channeled", "Channel an elemental totem's power"),
    ("doppelganger_defeated", "Defeat your own shadow doppelganger"),
    ("cartographer", "Collect a full set of treasure map fragments"),
    ("vault_opener", "Open a sealed vault with a Sacred Key"),
    ("statue_trial_passed", "Pass a Guardian Statue's strength trial"),
    ("combo_finisher", "Unleash a Combo Finisher"),
    ("high_roller", "Win a High Roller bet at the Gambling Den"),
    ("chimera_slain", "Slay the legendary Chimera"),
    ("escape_artist", "Flee from battle 10 times"),
    ("crit_master", "Land 50 Critical Hits"),
    ("alchemist", "Drink 20 Potions"),
    ("floor_whisperer", "Encounter every floor modifier at least once"),
    ("marathoner", "Take 10,000 steps"),
    ("executioner", "Deal 100,000 total damage"),
    ("demolitionist", "Use 30 Blaze Gems in battle"),
    ("veteran", "Defeat 500 enemies in total"),
    ("sharpshooter", "Deal 500+ damage in a single hit"),
    ("treasure_hunter", "Open 150 treasure chests"),
    ("fortified", "Use 25 Defense Pills in battle"),
    ("combo_king", "Reach a 20-hit combo streak in one battle"),
    ("deep_delver", "Reach floor 60"),
    ("chain_reaction", "Unleash 25 Combo Finishers in total"),
    ("master_cartographer", "Fully explore 50 floors in total"),
    ("tactician", "Use Focus 40 times in total"),
    ("elite_slayer", "Defeat 100 Elite monsters in total"),
    ("merchant_baron", "Trade with a merchant 50 times in total"),
]

# --- 実績画面での進捗表示 ---
# 累計値がしきい値に達すると解除される実績について、(対応するstats.jsonのキー, しきい値)
# を紐付ける。実績一覧でまだ解除していない項目の横に「現在値/しきい値」を表示するために使う
# (これまでは"Traps triggered"だけ実績一覧の下に個別表示されていたが、他の累積系実績には
# 進捗を確認する手段が無く、あとどれだけ頑張ればよいか分からなかったため追加した)。
ACHIEVEMENT_PROGRESS = {
    "crit_master": ("critical_hits_landed", 50),
    "alchemist": ("potions_used", 20),
    "marathoner": ("steps_taken", 10000),
    "executioner": ("total_damage_dealt", 100000),
    "demolitionist": ("blazegems_used", 30),
    "veteran": ("total_kills", 500),
    "escape_artist": ("battles_fled", 10),
    "sharpshooter": ("highest_single_hit_damage", 500),
    "treasure_hunter": ("treasures_opened", 150),
    "fortified": ("def_pills_used", 25),
    "combo_king": ("highest_combo_reached", 20),
    "deep_delver": ("deepest_floor_reached", 60),
    "chain_reaction": ("combo_finishers_used", 25),
    "master_cartographer": ("floors_fully_explored", 50),
    "tactician": ("focus_used", 40),
    "elite_slayer": ("elites_defeated", 100),
    "merchant_baron": ("merchant_trades", 50),
}

# --- 実績連動の称号システム ---
# 解除した実績のうち、最も優先度の高いものを称号として表示する。
TITLE_DEFS = [
    # (実績キー, 称号, 優先度が高い順に並べる)
    ("hidden_boss_defeat", "the Unbound Slayer"),
    ("hard_clear",         "the Hardened"),
    ("game_clear",         "the Conqueror"),
    ("no_damage_win",      "the Untouchable"),
    ("trap100",            "the Surefooted"),
    ("starve_survive",     "the Enduring"),
    ("boss_defeat",        "the Boss Slayer"),
    ("grandmaster",        "the Grandmaster"),
    ("skill_maxed",        "the Adept"),
    ("echo_master",        "the Echomaster"),
    ("echo_hunter",        "the Echo Hunter"),
    ("merchant_regular",   "the Regular"),
    ("elite_hunter",       "the Elite Hunter"),
    ("explorer",           "the Explorer"),
    ("golden_catch",       "the Fortune Seeker"),
    ("vault_escapee",      "the Quick-Footed"),
    ("den_cleared",        "the Den Cleanser"),
    ("boulder_dodge",      "the Idol Thief"),
    ("shrine_gambler",     "the Gambler"),
    ("blood_moon_survivor", "the Bloodstained"),
    ("mimic_defeated",     "the Chest Breaker"),
    ("ally_rescued",       "the Liberator"),
    ("rift_survivor",      "the Rift Walker"),
    ("altar_boon",         "the Devout"),
    ("altar_sacrifice",    "the Penitent"),
    ("door_unlocked",      "the Locksmith"),
    ("spirit_blessed",     "the Blessed"),
    ("bounty_hunter",      "the Bounty Hunter"),
    ("totem_channeled",    "the Elementalist"),
    ("doppelganger_defeated", "the Self-Made"),
    ("cartographer",       "the Cartographer"),
    ("vault_opener",       "the Vault Breaker"),
    ("statue_trial_passed", "the Mighty"),
    ("combo_finisher",     "the Chainbreaker"),
    ("high_roller",        "the High Roller"),
    ("chimera_slain",      "the Chimera Slayer"),
    ("escape_artist",      "the Escape Artist"),
    ("crit_master",        "the Deadeye"),
    ("alchemist",          "the Alchemist"),
    ("floor_whisperer",    "the Attuned"),
    ("marathoner",         "the Wanderer"),
    ("executioner",        "the Executioner"),
    ("demolitionist",      "the Demolitionist"),
    ("veteran",            "the Veteran"),
    ("sharpshooter",       "the Sharpshooter"),
    ("treasure_hunter",    "the Treasure Hunter"),
    ("fortified",          "the Fortified"),
    ("combo_king",         "the Combo King"),
    ("deep_delver",        "the Abyssal"),
    ("chain_reaction",     "the Chainmaster"),
    ("master_cartographer", "the Master Cartographer"),
    ("tactician",           "the Tactician"),
    ("elite_slayer",        "the Bane of Elites"),
    ("merchant_baron",      "the Merchant Baron"),
]

_current_title_cache = ""
_current_title_dirty = True

def current_title():
    """解除済みの実績のうち、最も優先度の高い称号を返す(何も無ければ空文字)
    achievements.jsonへのディスクアクセスを避けるため、unlock_achievement()で
    実績が更新された時だけ再計算するキャッシュを使う。"""
    global _current_title_cache, _current_title_dirty
    if _current_title_dirty:
        data = load_achievements()
        _current_title_cache = ""
        for key, title in TITLE_DEFS:
            if data.get(key, False):
                _current_title_cache = title
                break
        _current_title_dirty = False
    return _current_title_cache

# --- スタート時のキャラクター選択 ---
CHARACTER_TYPES = {
    "warrior":  {"name": "Warrior",  "desc": "+20 STR, well-rounded fighter",
                 "str": 20, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0},
    "guardian": {"name": "Guardian", "desc": "+15 DEF, +50 Max HP, tougher",
                 "str": 0, "def": 15, "lifemax": 50, "exp_mult": 1.0, "food_mult": 1.0},
    "scholar":  {"name": "Scholar",  "desc": "+20% EXP gain, but -10 STR",
                 "str": -10, "def": 0, "lifemax": 0, "exp_mult": 1.2, "food_mult": 1.0},
    "scout":    {"name": "Scout",    "desc": "Food lasts 20% longer",
                 "str": 0, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 0.8},
}
CHARACTER_ORDER = ["warrior", "guardian", "scholar", "scout"]
selected_character = "warrior"

def char_params():
    return CHARACTER_TYPES.get(selected_character, CHARACTER_TYPES["warrior"])

def is_boss_floor(fl):
    return fl >= BOSS_FLOOR_INTERVAL and fl % BOSS_FLOOR_INTERVAL == 0

_achievements_cache = None
achievements_scroll = 0
ACHIEVEMENTS_VISIBLE_ROWS = 13
stats_scroll = 0
STATS_VISIBLE_ROWS = 18

def load_achievements():
    """achievements.jsonはタイトル画面や実績一覧など複数の描画箇所から毎フレーム
    呼ばれるため、一度読み込んだらプロセス内キャッシュを使い、save_achievements()
    で書き込む時だけ更新する。呼び出し側が戻り値を書き換えてもキャッシュ自体は
    汚さないようコピーを返す。"""
    global _achievements_cache
    if _achievements_cache is None:
        try:
            with open("achievements.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        for key, _ in ACHIEVEMENT_DEFS:
            data.setdefault(key, False)
        data.setdefault("trap_count", 0)
        data.setdefault("echo_floors_defeated", [])
        data.setdefault("floor_modifiers_seen", [])
        _achievements_cache = data
    return dict(_achievements_cache)

def save_achievements(data):
    global _achievements_cache
    _achievements_cache = dict(data)
    try:
        with open("achievements.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        _log_io_error("save_achievements", e)

ACHIEVEMENT_LABELS = dict(ACHIEVEMENT_DEFS)

def unlock_achievement(key):
    """実績を解除する。以前は解除してもプレイヤーには何の合図もなく、
    後でRecords→Achievements画面を開くまで気づけなかったため、
    新規解除時はinfo_messageでトーストのように知らせていたが、他の雑多な
    メッセージと見分けがつかず地味だった。今は専用のゴールドバナー演出
    (draw_achievement_toast)で目立たせる。さらにバナー表示と同時に
    ジングルを鳴らし(achievement_sound_pending)、視覚だけでなく聴覚でも
    達成の瞬間に気づけるようにする。"""
    global _current_title_dirty, achievement_toast_label, achievement_toast_timer, achievement_sound_pending
    data = load_achievements()
    if not data.get(key, False):
        data[key] = True
        save_achievements(data)
        _current_title_dirty = True
        achievement_toast_label = ACHIEVEMENT_LABELS.get(key, key)
        achievement_toast_timer = ACHIEVEMENT_TOAST_FRAMES
        achievement_sound_pending = True

def register_floor_modifier_seen(mod_id):
    """訪れたフロア特性を記録し、全種類(FLOOR_MODIFIERS)を一度でも踏破したら
    実績「Floor Whisperer」を解除する。echo_floors_defeatedと同じ、
    setで重複を除いてリスト保存するパターンを踏襲。"""
    if not mod_id:
        return
    data = load_achievements()
    seen = set(data.get("floor_modifiers_seen", []))
    if mod_id in seen:
        return
    seen.add(mod_id)
    data["floor_modifiers_seen"] = sorted(seen)
    save_achievements(data)
    if seen.issuperset(FLOOR_MODIFIERS.keys()):
        unlock_achievement("floor_whisperer")

def add_trap_count(n=1):
    data = load_achievements()
    data["trap_count"] = data.get("trap_count", 0) + n
    if data["trap_count"] >= 100 and not data.get("trap100", False):
        data["trap100"] = True
    save_achievements(data)

# --- プレイ統計(実績とは別に、これまでの全プレイを通じた記録を残す) ---
STATS_DEFS = [
    ("total_playtime_ms", "Total play time"),
    ("total_kills", "Enemies defeated"),
    ("bosses_defeated_count", "Bosses defeated"),
    ("treasures_opened", "Treasure chests opened"),
    ("total_deaths", "Deaths"),
    ("total_floors_descended", "Total floors descended"),
    ("runs_completed", "Times game cleared"),
    ("merchant_trades", "Merchant trades made"),
    ("echoes_defeated", "Echo battles won"),
    ("elites_defeated", "Elite monsters defeated"),
    ("floors_fully_explored", "Floors fully explored"),
    ("golden_sprites_caught", "Golden slimes caught"),
    ("vaults_escaped", "Collapsing vaults escaped"),
    ("dens_cleared", "Monster dens cleared"),
    ("boulders_dodged", "Boulders outrun"),
    ("shrines_used", "Shrines gambled at"),
    ("blood_moons_survived", "Blood Moon floors survived"),
    ("mimics_encountered", "Mimic chests encountered"),
    ("mimics_defeated", "Mimic chests defeated"),
    ("allies_rescued", "Captive allies rescued"),
    ("rifts_entered", "Unstable rifts entered"),
    ("rifts_cleared", "Unstable rifts cleared"),
    ("altars_used", "Sacrificial altars used"),
    ("altar_boons", "Altar boons received"),
    ("pressure_plates_triggered", "Pressure plates triggered"),
    ("spirits_encountered", "Wandering spirits encountered"),
    ("bounties_completed", "Bounty quests completed"),
    ("totems_used", "Elemental totems channeled"),
    ("doppelgangers_encountered", "Doppelganger mirrors touched"),
    ("doppelgangers_defeated", "Doppelgangers defeated"),
    ("map_fragment_sets_completed", "Treasure map fragment sets completed"),
    ("sacred_keys_found", "Sacred Keys found"),
    ("vaults_opened", "Sealed vaults opened"),
    ("statue_trials_attempted", "Guardian Statue trials attempted"),
    ("statue_trials_passed", "Guardian Statue trials passed"),
    ("combo_finishers_used", "Combo Finishers unleashed"),
    ("gambles_played", "Gambling Den bets placed"),
    ("gambles_won", "Gambling Den bets won"),
    ("chimeras_encountered", "Chimeras encountered"),
    ("chimeras_defeated", "Chimeras defeated"),
    ("deepest_floor_reached", "Deepest floor ever reached"),
    ("battles_fled", "Battles fled"),
    ("critical_hits_landed", "Critical hits landed"),
    ("potions_used", "Potions drunk"),
    ("highest_combo_reached", "Highest combo streak reached"),
    ("steps_taken", "Steps taken"),
    ("total_damage_dealt", "Total damage dealt"),
    ("blazegems_used", "Blaze Gems used in battle"),
    ("highest_single_hit_damage", "Hardest single hit dealt"),
    ("def_pills_used", "Defense Pills used in battle"),
    ("focus_used", "Focus used in battle"),
]

playtime_ms_accum = 0
steps_taken_accum = 0

SETTINGS_FILE = "settings.json"

def load_settings():
    """settings.jsonからBGM/SE音量とミュート状態を読み込む。ファイルが無い/
    壊れている場合はデフォルト(1.0=フル音量、ミュートOFF)のまま何もしない。"""
    global bgm_volume, se_volume, muted, screen_shake_enabled, screen_flash_enabled
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        bgm_volume = max(0.0, min(1.0, float(data.get("bgm_volume", 1.0))))
        se_volume = max(0.0, min(1.0, float(data.get("se_volume", 1.0))))
        muted = bool(data.get("muted", False))
        screen_shake_enabled = bool(data.get("screen_shake_enabled", True))
        screen_flash_enabled = bool(data.get("screen_flash_enabled", True))
    except Exception:
        pass

def save_settings():
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"bgm_volume": bgm_volume, "se_volume": se_volume, "muted": muted,
                       "screen_shake_enabled": screen_shake_enabled,
                       "screen_flash_enabled": screen_flash_enabled}, f)
    except Exception as e:
        _log_io_error("save_settings", e)

def trigger_screen_shake(timer, mag):
    """screen_shake_enabledがOFFの場合は何もしない、共通の画面シェイク発火口。"""
    global screen_shake_timer, screen_shake_mag
    if not screen_shake_enabled:
        return
    screen_shake_timer = timer
    screen_shake_mag = mag

def flush_playtime():
    """蓄積したプレイ時間(ms)と歩数をstats.jsonへ書き出し、蓄積分をリセットする。
    歩数は1歩ごとにディスクへ書くと負荷が大きいため、プレイ時間と同じく
    メモリに貯めておいて既存のフラッシュ地点(セーブ・階段・終了時など)で
    まとめて書き込む。"""
    global playtime_ms_accum, steps_taken_accum
    if playtime_ms_accum > 0:
        record_stat("total_playtime_ms", playtime_ms_accum)
        playtime_ms_accum = 0
    if steps_taken_accum > 0:
        record_stat("steps_taken", steps_taken_accum)
        steps_taken_accum = 0
        if load_stats().get("steps_taken", 0) >= 10000:
            unlock_achievement("marathoner")

_stats_cache = None

def load_stats():
    """stats.jsonも記録画面や各種条件チェックから頻繁に呼ばれるので、achievements
    と同じくプロセス内キャッシュ+コピー返却にしてディスクI/Oを1回だけにする。"""
    global _stats_cache
    if _stats_cache is None:
        try:
            with open("stats.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        for key, _ in STATS_DEFS:
            data.setdefault(key, 0)
        _stats_cache = data
    return dict(_stats_cache)

def save_stats(data):
    global _stats_cache
    _stats_cache = dict(data)
    try:
        with open("stats.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        _log_io_error("save_stats", e)

def record_stat(key, amount=1):
    data = load_stats()
    data[key] = data.get(key, 0) + amount
    save_stats(data)

def record_stat_max(key, value):
    """加算ではなく、これまでの最大値のみを記録したい統計(到達最深階層など)用。"""
    data = load_stats()
    if value > data.get(key, 0):
        data[key] = value
        save_stats(data)

def format_playtime(ms):
    total_sec = ms // 1000
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    if h > 0:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"

# --- 発見ログ/図鑑(Bestiary) ---
# 出会った敵・見つけたアイテムを記録し、タイトル画面の記録メニューから確認できる。
_bestiary_cache = None

def load_bestiary():
    """bestiary.jsonも図鑑画面などから毎フレーム呼ばれるので、achievements/statsと
    同じくプロセス内キャッシュ+コピー返却にする(内側のリストはコピーし直して、
    呼び出し側のin-place更新がキャッシュに漏れないようにする)。"""
    global _bestiary_cache
    if _bestiary_cache is None:
        try:
            with open("bestiary.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        data.setdefault("enemies", [False] * len(EMY_NAME))
        data.setdefault("items", [False] * len(TRE_NAME))
        data.setdefault("bosses", [False] * len(BOSS_BESTIARY))
        # 敵/アイテム/ボスの種類が増えた場合に備えて長さを合わせる
        if len(data["enemies"]) < len(EMY_NAME):
            data["enemies"] += [False] * (len(EMY_NAME) - len(data["enemies"]))
        if len(data["items"]) < len(TRE_NAME):
            data["items"] += [False] * (len(TRE_NAME) - len(data["items"]))
        if len(data["bosses"]) < len(BOSS_BESTIARY):
            data["bosses"] += [False] * (len(BOSS_BESTIARY) - len(data["bosses"]))
        _bestiary_cache = data
    return {k: (list(v) if isinstance(v, list) else v) for k, v in _bestiary_cache.items()}

def save_bestiary(data):
    global _bestiary_cache
    _bestiary_cache = {k: (list(v) if isinstance(v, list) else v) for k, v in data.items()}
    try:
        with open("bestiary.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        _log_io_error("save_bestiary", e)

def record_enemy_seen(typ_idx):
    if not (0 <= typ_idx < len(EMY_NAME)):
        return
    data = load_bestiary()
    if not data["enemies"][typ_idx]:
        data["enemies"][typ_idx] = True
        save_bestiary(data)

def record_item_seen(treasure_idx):
    if not (0 <= treasure_idx < len(TRE_NAME)):
        return
    data = load_bestiary()
    if not data["items"][treasure_idx]:
        data["items"][treasure_idx] = True
        save_bestiary(data)

def record_boss_seen(boss_idx):
    if not (0 <= boss_idx < len(BOSS_BESTIARY)):
        return
    data = load_bestiary()
    if not data["bosses"][boss_idx]:
        data["bosses"][boss_idx] = True
        save_bestiary(data)

# 図鑑(Bestiary)の詳細表示画面(idx==47)で、いま選択中のモンスター/ボスを覚えておく状態
bestiary_detail_kind = None   # "enemy" または "boss"
bestiary_detail_index = 0
bestiary_detail_img = None    # 選択中の画像(未発見ならNone)
bestiary_detail_seen = False

# --- スキルツリー(レベルアップで得たポイントで永続強化を購入する) ---
# 5本の枝(body/combat/mind/survival/fortune)、各3段のツリー構造。tier2/tier3
# のスキルは、同じ枝の1つ前の段を1レベル以上習得していないと解放されない。
# 最後に、5枝すべてのtier3を1レベル以上習得すると解放される総仕上げの
# "grandmaster"がある(枝をまたぐ本物のツリー構造)。
# 各スキルは"base"+"growth"を持ち、レベルを上げるごとにその回で得られる効果
# 自体が大きくなっていく(単純な線形の積み上げではなく、後半のレベルほど
# 効果が跳ね上がる右肩上がりの強化曲線にしてある)。
SKILLS = [
    {"id": "tough_skin",    "name": "Toughness",      "branch": "body",     "tier": 1, "requires": None,
     "desc": "DEF grows/lv", "cost": 1, "max_level": 5, "base": 4, "growth": 4},
    {"id": "vital_surge",   "name": "Vital Surge",    "branch": "body",     "tier": 2, "requires": "tough_skin",
     "desc": "Max HP% grows/lv", "cost": 2, "max_level": 5, "base": 0.03, "growth": 0.01},
    {"id": "fortress",      "name": "Fortress",       "branch": "body",     "tier": 3, "requires": "vital_surge",
     "desc": "Trap dmg cut grows/lv", "cost": 3, "max_level": 3, "base": 0.1, "growth": 0.08},
    {"id": "warrior_will",  "name": "Warrior's Will", "branch": "combat",   "tier": 1, "requires": None,
     "desc": "STR grows/lv", "cost": 1, "max_level": 5, "base": 8, "growth": 8},
    {"id": "antidote_body", "name": "Antidote Body",  "branch": "combat",   "tier": 2, "requires": "warrior_will",
     "desc": "Poison res grows/lv", "cost": 1, "max_level": 2, "base": 0.2, "growth": 0.2},
    {"id": "berserker",     "name": "Berserker",      "branch": "combat",   "tier": 3, "requires": "antidote_body",
     "desc": "STR grows/lv (big)", "cost": 3, "max_level": 4, "base": 15, "growth": 15},
    {"id": "scholar_mind",  "name": "Scholar's Mind", "branch": "mind",     "tier": 1, "requires": None,
     "desc": "EXP grows/lv", "cost": 2, "max_level": 3, "base": 0.08, "growth": 0.08},
    {"id": "lucky_find",    "name": "Lucky Find",     "branch": "mind",     "tier": 2, "requires": "scholar_mind",
     "desc": "Item luck grows/lv", "cost": 2, "max_level": 3, "base": 4, "growth": 4},
    {"id": "sage",          "name": "Sage",           "branch": "mind",     "tier": 3, "requires": "lucky_find",
     "desc": "EXP grows/lv (big)", "cost": 3, "max_level": 3, "base": 0.15, "growth": 0.1},
    {"id": "iron_stomach",  "name": "Iron Stomach",   "branch": "survival", "tier": 1, "requires": None,
     "desc": "Food eff grows/lv", "cost": 1, "max_level": 3, "base": 0.12, "growth": 0.12},
    {"id": "forager",       "name": "Forager",        "branch": "survival", "tier": 2, "requires": "iron_stomach",
     "desc": "Food yield grows/lv", "cost": 2, "max_level": 3, "base": 0.15, "growth": 0.1},
    {"id": "survivor",      "name": "Survivor",       "branch": "survival", "tier": 3, "requires": "forager",
     "desc": "Auto-heal on stairs grows/lv", "cost": 3, "max_level": 3, "base": 0.05, "growth": 0.03},
    {"id": "keen_eye",      "name": "Keen Eye",       "branch": "fortune",  "tier": 1, "requires": None,
     "desc": "Vision radius grows/lv", "cost": 1, "max_level": 2, "base": 1, "growth": 0},
    {"id": "swift_feet",    "name": "Swift Feet",     "branch": "fortune",  "tier": 2, "requires": "keen_eye",
     "desc": "Move speed grows/lv", "cost": 2, "max_level": 3, "base": 0.08, "growth": 0.05},
    {"id": "perfect_strike", "name": "Perfect Strike", "branch": "fortune", "tier": 3, "requires": "swift_feet",
     "desc": "Crit chance grows/lv", "cost": 3, "max_level": 3, "base": 0.05, "growth": 0.03},
    {"id": "grandmaster",   "name": "Grandmaster",    "branch": "capstone", "tier": 4,
     "requires": ["fortress", "berserker", "sage", "survivor", "perfect_strike"],
     "desc": "One-time boost to every stat", "cost": 5, "max_level": 1, "base": 0, "growth": 0},
]
SKILLS_BY_ID = {sk["id"]: sk for sk in SKILLS}
SKILL_BRANCH_ORDER = ["body", "combat", "mind", "survival", "fortune"]
SKILL_ICONS = {sk["id"]: pygame.image.load(f"image/skill_{sk['id']}.png") for sk in SKILLS}

def skill_level_contribution(sk, level):
    """そのレベル自身が単独で追加する効果量(線形に増える"のびしろ")"""
    if level <= 0:
        return 0
    return sk["base"] + sk["growth"] * (level - 1)

def skill_cumulative_effect(sk, level):
    """1レベルからlevelまでの効果を全部足した累計値"""
    if level <= 0:
        return 0
    return level * sk["base"] + sk["growth"] * level * (level - 1) / 2

def skill_requirement_ids(sk):
    req = sk.get("requires")
    if req is None:
        return []
    if isinstance(req, list):
        return req
    return [req]

def skill_prereq_met(sk):
    return all(skill_levels.get(r, 0) > 0 for r in skill_requirement_ids(sk))

skill_points = 0
skill_levels = {sk["id"]: 0 for sk in SKILLS}
skill_food_mult = 1.0
skill_poison_mult = 1.0
skill_exp_mult = 1.0
skill_item_bonus = 0
skill_trap_dmg_mult = 1.0
skill_food_yield_mult = 1.0
skill_vision_bonus = 0
skill_move_speed_bonus = 0.0
skill_crit_chance = 0.0
skill_floor_heal_pct = 0.0
skill_cursor_col = 0
skill_cursor_row = 0
skill_cursor_capstone = False

def recompute_skill_percent_effects():
    """割合/加算系スキルの効果を現在のskill_levelsから作り直す(セーブ読込時
    などに使う)。固定値強化(tough_skin/warrior_will/vital_surge/berserker/
    grandmaster)は購入時にステータスへ直接加算済みなので、ここでは
    再計算しない(二重加算を避けるため)。"""
    global skill_food_mult, skill_poison_mult, skill_exp_mult, skill_item_bonus
    global skill_trap_dmg_mult, skill_food_yield_mult, skill_vision_bonus
    global skill_move_speed_bonus, skill_crit_chance, skill_floor_heal_pct

    def cum(skill_id):
        return skill_cumulative_effect(SKILLS_BY_ID[skill_id], skill_levels.get(skill_id, 0))

    skill_food_mult = max(0.2, 1.0 - cum("iron_stomach"))
    skill_poison_mult = max(0.2, 1.0 - cum("antidote_body"))
    skill_exp_mult = 1.0 + cum("scholar_mind") + cum("sage")
    skill_item_bonus = cum("lucky_find")
    skill_trap_dmg_mult = max(0.3, 1.0 - cum("fortress"))
    skill_food_yield_mult = 1.0 + cum("forager")
    skill_vision_bonus = int(round(cum("keen_eye")))
    skill_move_speed_bonus = cum("swift_feet")
    skill_crit_chance = min(0.6, cum("perfect_strike"))
    skill_floor_heal_pct = min(0.6, cum("survivor"))

SKILL_PER_LEVEL_TEXT = {
    "tough_skin":    lambda lv: f"+{int(round(skill_cumulative_effect(SKILLS_BY_ID['tough_skin'], lv)))} DEF",
    "warrior_will":  lambda lv: f"+{int(round(skill_cumulative_effect(SKILLS_BY_ID['warrior_will'], lv)))} STR",
    "iron_stomach":  lambda lv: f"-{skill_cumulative_effect(SKILLS_BY_ID['iron_stomach'], lv)*100:.0f}% food",
    "antidote_body": lambda lv: f"-{skill_cumulative_effect(SKILLS_BY_ID['antidote_body'], lv)*100:.0f}% poison",
    "scholar_mind":  lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['scholar_mind'], lv)*100:.0f}% EXP",
    "lucky_find":    lambda lv: f"+{int(round(skill_cumulative_effect(SKILLS_BY_ID['lucky_find'], lv)))} luck",
    "vital_surge":   lambda lv: f"HP boosted x{lv}",
    "fortress":      lambda lv: f"-{skill_cumulative_effect(SKILLS_BY_ID['fortress'], lv)*100:.0f}% trap dmg",
    "berserker":     lambda lv: f"+{int(round(skill_cumulative_effect(SKILLS_BY_ID['berserker'], lv)))} STR",
    "sage":          lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['sage'], lv)*100:.0f}% EXP",
    "forager":       lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['forager'], lv)*100:.0f}% food",
    "survivor":      lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['survivor'], lv)*100:.0f}% heal/floor",
    "keen_eye":      lambda lv: f"+{int(round(skill_cumulative_effect(SKILLS_BY_ID['keen_eye'], lv)))} vision",
    "swift_feet":    lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['swift_feet'], lv)*100:.0f}% speed",
    "perfect_strike": lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['perfect_strike'], lv)*100:.0f}% crit",
    "grandmaster":   lambda lv: "All stats boosted!",
}
SKILL_NEXT_LEVEL_TEXT = {
    "tough_skin":    lambda lv: f"Next: +{int(round(skill_level_contribution(SKILLS_BY_ID['tough_skin'], lv+1)))} DEF",
    "warrior_will":  lambda lv: f"Next: +{int(round(skill_level_contribution(SKILLS_BY_ID['warrior_will'], lv+1)))} STR",
    "iron_stomach":  lambda lv: f"Next: -{skill_level_contribution(SKILLS_BY_ID['iron_stomach'], lv+1)*100:.0f}% food",
    "antidote_body": lambda lv: f"Next: -{skill_level_contribution(SKILLS_BY_ID['antidote_body'], lv+1)*100:.0f}% poison",
    "scholar_mind":  lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['scholar_mind'], lv+1)*100:.0f}% EXP",
    "lucky_find":    lambda lv: f"Next: +{int(round(skill_level_contribution(SKILLS_BY_ID['lucky_find'], lv+1)))} luck",
    "vital_surge":   lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['vital_surge'], lv+1)*100:.0f}% HP",
    "fortress":      lambda lv: f"Next: -{skill_level_contribution(SKILLS_BY_ID['fortress'], lv+1)*100:.0f}% more",
    "berserker":     lambda lv: f"Next: +{int(round(skill_level_contribution(SKILLS_BY_ID['berserker'], lv+1)))} STR",
    "sage":          lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['sage'], lv+1)*100:.0f}% more",
    "forager":       lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['forager'], lv+1)*100:.0f}% more",
    "survivor":      lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['survivor'], lv+1)*100:.0f}% more",
    "keen_eye":      lambda lv: f"Next: +{int(round(skill_level_contribution(SKILLS_BY_ID['keen_eye'], lv+1)))} vision",
    "swift_feet":    lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['swift_feet'], lv+1)*100:.0f}% more",
    "perfect_strike": lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['perfect_strike'], lv+1)*100:.0f}% more",
    "grandmaster":   lambda lv: "Requires all 5 branches maxed to tier 3",
}

def skill_current_effect_text(skill_id, lv):
    """そのスキルの『今まで習得した分の累計効果』を分かりやすい文章にして返す。
    まだ1つも習得していなければ空文字を返す。"""
    if lv <= 0:
        return ""
    fn = SKILL_PER_LEVEL_TEXT.get(skill_id)
    return fn(lv) if fn else ""

def apply_skill_effect(skill_id):
    """スキルのレベルが1つ上がった直後に呼ぶ(skill_levelsは呼び出し側で
    既に新しいレベルへ更新済み)。固定値強化はここで直接ステータスに加算し、
    割合系の強化はrecompute_skill_percent_effectsで一括反映する。"""
    global pl_def_base, pl_str, pl_lifemax, pl_life
    sk = SKILLS_BY_ID.get(skill_id)
    lv = skill_levels.get(skill_id, 0)
    if sk is not None and skill_id == "tough_skin":
        pl_def_base += int(round(skill_level_contribution(sk, lv)))
    elif sk is not None and skill_id == "warrior_will":
        pl_str += int(round(skill_level_contribution(sk, lv)))
    elif sk is not None and skill_id == "berserker":
        pl_str += int(round(skill_level_contribution(sk, lv)))
    elif sk is not None and skill_id == "vital_surge":
        rate = skill_level_contribution(sk, lv)
        gain = max(1, int(pl_lifemax * rate))
        pl_lifemax += gain
        pl_life += gain
    elif sk is not None and skill_id == "grandmaster":
        pl_def_base += 30
        pl_str += 50
        gain = 100
        pl_lifemax += gain
        pl_life += gain
        unlock_achievement("grandmaster")
    recompute_skill_percent_effects()
    if sk is not None and lv >= sk["max_level"]:
        unlock_achievement("skill_maxed")

food = 0
potion = 0
blazegem = 0
treasure = 0
pl_def_base = 0
pl_def_buff = 0
def_pill = 0
flg_action = False

emy_name=""
emy_lifemax = 0
emy_life = 0
emy_str = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0
emy_lv = 1
typ = 0
is_elite = False

# --- エリートモンスター(見た目バリエーション) ---
# 新しい画像を用意しなくても、通常モンスターに稀な確率で色調ティントと
# 強化ステータスを与えることで「特別な個体」として見た目にバリエーションを出す。
ELITE_CHANCE = 12  # 通常戦闘(ボス以外)でエリート化する確率(%)
ELITE_TINT = (255, 200, 90)  # BLEND_MULTで乗算する色(金色がかった強敵感を出す)
DOPPELGANGER_TINT = (90, 70, 140)  # 分身の鏡の影を暗い紫がかった色にする
ELITE_LIFE_MULT = 1.6
ELITE_STR_MULT = 1.3
ELITE_EXP_MULT = 1.5

def tint_surface(img, color):
    """imgのRGBをcolorで乗算した色調違いのコピーを返す(アルファ/形状はそのまま)。"""
    tinted = img.convert_alpha()
    tinted.fill(color, special_flags=pygame.BLEND_MULT)
    return tinted

# --- ゴールデンスライム(逃げ回るレア遭遇) ---
# フロアに稀に現れ、プレイヤーが近づくと1マスずつ逃げる。追いついて同じマスに
# 乗れば豪華な報酬がもらえるが、一定歩数の間に逃げ切られると消えてしまう。
# 「捕まえられるか、逃げられるか」というその場限りの緊張感を狙った要素。
GOLDEN_SPRITE_CHANCE = 12     # フロアに出現する確率(%)。floor>=3から
GOLDEN_SPRITE_LIFESPAN = 35   # 出現してから逃げ切られるまでのプレイヤーの歩数
GOLDEN_SPRITE_MIN_DIST = 6    # プレイヤーの現在地からこれ以上離れた場所に出現
golden_sprite_pos = None
golden_sprite_timer = 0
_golden_sprite_img_cache = None

def get_golden_sprite_image():
    """金色にティントしたスライム画像を初回だけ作ってキャッシュする
    (pygameのconvert_alpha()はディスプレイ初期化後でないと使えないため、
    モジュール読み込み時ではなく初めて必要になった時に生成する)。"""
    global _golden_sprite_img_cache
    if _golden_sprite_img_cache is None:
        # 乗算だけでは元が緑のスライムなので金色にならず、加算ブレンドで
        # 暖色の輝きを足すことではっきり「金色」に見えるようにする
        img = pygame.image.load("image/enemy0.png").convert_alpha()
        img.fill((255, 235, 120), special_flags=pygame.BLEND_MULT)
        img.fill((70, 50, 0), special_flags=pygame.BLEND_ADD)
        _golden_sprite_img_cache = img
    return _golden_sprite_img_cache

_monster_den_img_cache = None

def get_monster_den_image():
    """モンスターの巣タイル用に、繭画像を赤黒くティントした画像を初回だけ作ってキャッシュする。"""
    global _monster_den_img_cache
    if _monster_den_img_cache is None:
        img = pygame.image.load("image/cocoon.png").convert_alpha()
        img.fill((150, 60, 60), special_flags=pygame.BLEND_MULT)
        img.fill((40, 0, 0), special_flags=pygame.BLEND_ADD)
        _monster_den_img_cache = img
    return _monster_den_img_cache

def roll_golden_sprite():
    """フロアの床が確定した後(put_eventの最後)に呼ぶ。既存のゴールデンスライムは
    フロアが変わったタイミングでリセットする。"""
    global golden_sprite_pos, golden_sprite_timer
    golden_sprite_pos = None
    golden_sprite_timer = 0
    if floor < 3 or random.randint(0, 99) >= GOLDEN_SPRITE_CHANCE:
        return
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] == 0 and abs(x-pl_x) + abs(y-pl_y) >= GOLDEN_SPRITE_MIN_DIST:
                candidates.append((x, y))
    if not candidates:
        return
    golden_sprite_pos = random.choice(candidates)
    golden_sprite_timer = GOLDEN_SPRITE_LIFESPAN

def update_golden_sprite():
    """プレイヤーが1マス移動を終えるたびに呼ぶ。捕獲判定・寿命の消化・
    プレイヤーから離れる方向への1マス移動(遭遇AI)を行う。"""
    global golden_sprite_pos, golden_sprite_timer
    global potion, blazegem, food, def_pill, pl_lifemax, pl_life
    global info_message, info_timer
    if golden_sprite_pos is None:
        return
    if (pl_x, pl_y) == golden_sprite_pos:
        r = random.randint(0, 99)
        if r < 10:
            potion += 3
            blazegem += 2
            def_pill += 1
            food += 100
            reward_txt = "+3 Potion, +2 Blaze gem, +1 Defense Pill, +100 Food"
        elif r < 40:
            pl_lifemax += 50
            pl_life += 50
            reward_txt = "+50 Max HP"
        elif r < 70:
            food += 100
            def_pill += 1
            reward_txt = "+100 Food, +1 Defense Pill"
        else:
            potion += 2
            blazegem += 1
            reward_txt = "+2 Potion, +1 Blaze gem"
        golden_sprite_pos = None
        golden_sprite_timer = 0
        record_stat("golden_sprites_caught")
        unlock_achievement("golden_catch")
        info_message = f"Caught the golden slime! {reward_txt}"
        info_timer = 80
        return
    golden_sprite_timer -= 1
    if golden_sprite_timer <= 0:
        golden_sprite_pos = None
        info_message = "The golden slime slipped away..."
        info_timer = 50
        return
    gx, gy = golden_sprite_pos
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(dirs)
    best = None
    best_dist = -1
    for dxn, dyn in dirs:
        nx, ny = gx+dxn, gy+dyn
        if 0 <= nx < DUNGEON_W and 0 <= ny < DUNGEON_H and dungeon[ny][nx] not in (9, 25):
            dist = abs(nx-pl_x) + abs(ny-pl_y)
            if dist > best_dist:
                best_dist = dist
                best = (nx, ny)
    if best:
        golden_sprite_pos = best

# --- 崩落する古代の宝物庫(脱出チャレンジ) ---
# 稀に生成される特別な宝物庫は、最初の宝箱を開けた瞬間に崩落が始まる。
# 一定歩数以内に部屋(3x3の範囲)の外へ脱出できれば無傷で済むが、
# 間に合わないと生き埋めになって大ダメージを受ける、というリスク/リターンの
# その場限りの緊張感を狙ったギミック。
COLLAPSING_VAULT_CHANCE = 18   # このタイプの宝物庫が生成される確率(%)。floor>=5から
COLLAPSE_COUNTDOWN = 18        # 崩落が始まってから脱出できる猶予歩数
COLLAPSE_DAMAGE_FRACTION = 0.3 # 逃げ遅れた場合に失う最大HPの割合
collapsing_vault_bounds = None  # (x0, y0, x1, y1) の部屋の範囲。Noneなら該当なし
collapse_timer = 0              # 0=まだ崩落していない/既に決着済み

def trigger_vault_collapse():
    """崩落する古代の宝物庫の宝箱を初めて開けた瞬間に呼ぶ。"""
    global collapse_timer, info_message, info_timer
    if collapsing_vault_bounds is None or collapse_timer > 0:
        return
    collapse_timer = COLLAPSE_COUNTDOWN
    info_message = "The ancient vault begins to collapse! Flee!"
    info_timer = 60

def update_collapse_timer():
    """プレイヤーが1マス移動を終えるたびに呼ぶ。崩落中なら歩数を消化し、
    部屋の外に出られたか、間に合わず生き埋めになったかを判定する。"""
    global collapse_timer, collapsing_vault_bounds
    global pl_life, info_message, info_timer, idx, tmr
    if collapse_timer <= 0 or collapsing_vault_bounds is None:
        return
    x0, y0, x1, y1 = collapsing_vault_bounds
    if not (x0 <= pl_x <= x1 and y0 <= pl_y <= y1):
        # 部屋の外に出られたので無事に脱出成功
        collapse_timer = 0
        collapsing_vault_bounds = None
        record_stat("vaults_escaped")
        unlock_achievement("vault_escapee")
        info_message = "You escaped the collapsing vault!"
        info_timer = 50
        return
    collapse_timer -= 1
    if collapse_timer <= 0:
        dmg = max(1, int(pl_lifemax * COLLAPSE_DAMAGE_FRACTION))
        pl_life -= dmg
        collapsing_vault_bounds = None
        info_message = f"The vault caves in! {dmg} damage!"
        info_timer = 60
        if pl_life <= 0:
            pl_life = 0
            pygame.mixer.music.stop()
            idx = 9
            tmr = 0

# --- ミミック(擬態する宝箱) ---
# 宝箱を開けた瞬間、まれに中身ではなく牙の生えたミミックが飛び出してくる。
# 見た目は普通の宝箱と全く同じなので、開けるまでは絶対に分からない。
# 倒せば普通の宝箱より豪華な報酬がもらえるが、油断していると不意打ちを食らう。
MIMIC_CHANCE = 12          # 宝箱がミミックである確率(%)。floor>=6から
MIMIC_LIFE_MULT = 1.35
MIMIC_STR_MULT = 1.2
mimic_battle_active = False

# --- モンスターの巣(連続奇襲)---
# 稀にフロアに現れる特別な床を踏むと、3体の敵と連続で戦う羽目になる
# (敵を倒すたびに間髪入れず次の敵が現れる)。全て倒し切れれば豪華な報酬。
# 途中で戦闘から逃げ出した場合は、そこで奇襲は終わり報酬はもらえない。
MONSTER_DEN_CHANCE = 16      # フロアに出現する確率(%)。floor>=4から
MONSTER_DEN_WAVES = 3        # 連続で戦う敵の数
ambush_battles_remaining = 0  # 0=奇襲中ではない

def resolve_post_battle_transition():
    """通常勝利後、次に何をすべきかを決めてidx/tmrを設定する。
    モンスターの巣での連続奇襲中なら、残りがあれば次の敵とただちに戦わせ、
    ちょうど倒し切ったところなら巣クリアのボーナスを与える。"""
    global idx, tmr, ambush_battles_remaining, mimic_battle_active, in_rift_battle
    global potion, blazegem, food, info_message, info_timer
    global doppelganger_battle_active, pl_exp
    global chimera_battle_active, pl_lifemax, pl_life
    if chimera_battle_active:
        chimera_battle_active = False
        bonus_exp = int(80 * max(1, floor))
        pl_exp += bonus_exp
        pl_lifemax += 30
        pl_life += 30
        potion += 3
        blazegem += 8
        food += 150
        record_stat("chimeras_defeated")
        unlock_achievement("chimera_slain")
        info_message = (f"The Chimera falls! +{bonus_exp} EXP, +30 Max HP, "
                         f"+3 Potion, +8 Blaze gem, +150 Food")
        info_timer = 70
    if doppelganger_battle_active:
        doppelganger_battle_active = False
        bonus_exp = int(20 * max(1, floor))
        pl_exp += bonus_exp
        potion += 1
        food += 50
        record_stat("doppelgangers_defeated")
        unlock_achievement("doppelganger_defeated")
        info_message = f"You overcame your reflection! +{bonus_exp} EXP, +1 Potion, +50 Food"
        info_timer = 60
    if mimic_battle_active:
        mimic_battle_active = False
        potion += 1
        blazegem += 2
        food += 60
        record_stat("mimics_defeated")
        unlock_achievement("mimic_defeated")
        info_message = "It was a Mimic! +1 Potion, +2 Blaze gem, +60 Food"
        info_timer = 60
    if in_rift_battle:
        in_rift_battle = False
        potion += 2
        blazegem += 3
        food += 100
        record_stat("rifts_cleared")
        unlock_achievement("rift_survivor")
        info_message = "Rift closed! +2 Potion, +3 Blaze gem, +100 Food"
        info_timer = 60
    if ambush_battles_remaining > 0:
        ambush_battles_remaining -= 1
        if ambush_battles_remaining > 0:
            idx = 10
            tmr = 0
            return
        potion += 2
        blazegem += 2
        food += 150
        record_stat("dens_cleared")
        unlock_achievement("den_cleared")
        info_message = "Monster den cleared! +2 Potion, +2 Blaze gem, +150 Food"
        info_timer = 70
    idx = 60 if in_echo_battle else (26 if in_boss_battle else 22)
    tmr = 0

# --- 転がる巨石(インディ・ジョーンズ風の逃走ギミック) ---
# 台座の上の黄金の像を持ち上げた瞬間、背後で巨石が転がり出す。プレイヤーと
# 同じ速さ(1歩ごとに1マス)で追いかけてくるので、壁に阻まれて distance を
# 詰められると危険。逃げ切れば無傷で像の報酬だけが手に入るが、追いつかれると
# 押し潰されて大ダメージを受ける。
IDOL_PEDESTAL_CHANCE = 14       # フロアに出現する確率(%)。floor>=4から
BOULDER_CHASE_DURATION = 22    # 巨石が追ってくる歩数の上限
BOULDER_DAMAGE_FRACTION = 0.25 # 追いつかれた場合に失う最大HPの割合
boulder_pos = None
boulder_timer = 0

def update_boulder_chase():
    """プレイヤーが1マス移動を終えるたびに呼ぶ。巨石に追いつかれたかどうかを判定し、
    そうでなければプレイヤーへ1マス近づける(追跡AI)。一定歩数逃げ切れば消える。"""
    global boulder_pos, boulder_timer
    global pl_life, info_message, info_timer, idx, tmr
    if boulder_pos is None:
        return
    if (pl_x, pl_y) == boulder_pos:
        dmg = max(1, int(pl_lifemax * BOULDER_DAMAGE_FRACTION))
        pl_life -= dmg
        boulder_pos = None
        boulder_timer = 0
        info_message = f"The boulder crushes you! {dmg} damage!"
        info_timer = 60
        if pl_life <= 0:
            pl_life = 0
            pygame.mixer.music.stop()
            idx = 9
            tmr = 0
        return
    boulder_timer -= 1
    if boulder_timer <= 0:
        boulder_pos = None
        record_stat("boulders_dodged")
        unlock_achievement("boulder_dodge")
        info_message = "You outran the boulder!"
        info_timer = 50
        return
    bx, by = boulder_pos
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(dirs)
    best = None
    best_dist = 10**9
    for dxn, dyn in dirs:
        nx, ny = bx+dxn, by+dyn
        if 0 <= nx < DUNGEON_W and 0 <= ny < DUNGEON_H and dungeon[ny][nx] not in (9, 25):
            dist = abs(nx-pl_x) + abs(ny-pl_y)
            if dist < best_dist:
                best_dist = dist
                best = (nx, ny)
    if best:
        boulder_pos = best

# --- 囚われの仲間(檻からの救出) ---
# 檻に囚われた仲間を助け出すと、そのフロアの間だけ一緒に戦ってくれる。
# フロアを移動すると仲間はその場に残るので、効果も一緒に切れる。
CAPTIVE_CHANCE = 14        # フロアに出現する確率(%)。floor>=3から
ALLY_STR_BONUS = 25
ALLY_DEF_BONUS = 8
ally_buff_active = False

# --- 不安定な裂け目(ハイリスク・ハイリターンのエリート戦) ---
# 踏むと必ずエリート個体との戦闘になる代わりに、勝てば通常の戦闘より豪華な
# 報酬がもらえる。見るからに危険な見た目にしてあるので、避けるか挑むかは
# プレイヤー次第。
RIFT_CHANCE = 10           # フロアに出現する確率(%)。floor>=5から
RIFT_LIFE_MULT = 1.2
RIFT_STR_MULT = 1.15
in_rift_battle = False

# --- 運命の祠(一発勝負のギャンブル床) ---
# 踏むと一度だけ運試しができる床。結果は大当たりから呪いまで幅広く、
# 良くも悪くも「踏んでみるまで分からない」その場限りのスリルを演出する。
SHRINE_CHANCE = 16  # フロアに出現する確率(%)。floor>=3から
# (重み, 結果名, 説明文)。重みの合計が確率(%)になるようにしてある
SHRINE_OUTCOMES = [
    (10, "JACKPOT!",   "+3 Potion, +3 Blaze gem, +2 Defense Pill, +200 Food"),
    (20, "Blessing",   "Fully healed and food restored!"),
    (20, "Fortune",    "+50 Max HP and +1 Blaze gem"),
    (20, "Quiet",      "Nothing happens..."),
    (15, "Curse",      "-15 STR and -5 DEF until you leave this floor"),
    (15, "Misfortune", "A cloud of poison gas bursts out!"),
]
shrine_result_name = ""
shrine_result_desc = ""

def roll_shrine_outcome():
    """祠の結果を実際に決めて効果を適用する。表示用の結果テキストを返す。"""
    global shrine_result_name, shrine_result_desc
    global potion, blazegem, def_pill, food, pl_life, pl_lifemax
    global curse_active, pl_str, pl_def_base, pl_poison
    r = random.randint(1, 100)
    acc = 0
    chosen = SHRINE_OUTCOMES[-1]
    for weight, name, desc in SHRINE_OUTCOMES:
        acc += weight
        if r <= acc:
            chosen = (weight, name, desc)
            break
    _, name, desc = chosen
    if name == "JACKPOT!":
        potion += 3
        blazegem += 3
        def_pill += 2
        food += 200
    elif name == "Blessing":
        pl_life = pl_lifemax
        food = max(food, 200)
    elif name == "Fortune":
        pl_lifemax += 50
        pl_life += 50
        blazegem += 1
    elif name == "Quiet":
        pass
    elif name == "Curse":
        if not curse_active:
            curse_active = True
            pl_str = max(1, pl_str - 15)
            pl_def_base -= 5
    elif name == "Misfortune":
        pl_poison = max(pl_poison, 50)
    shrine_result_name = name
    shrine_result_desc = desc
    record_stat("shrines_used")
    unlock_achievement("shrine_gambler")

# --- 圧力プレート & 封印された扉(探索パズル) ---
# フロアのどこかに封印された扉(壁と同じく通行不能)が1枚置かれ、
# 離れた場所にある圧力プレートを踏むとフロア中の扉がすべて開く。
# 「見つけた入口の先にどう行けばいいか」を考えさせる、探索型のギミック。
PUZZLE_DOOR_CHANCE = 16   # フロアに出現する確率(%)。floor>=3から

# --- さまよう精霊(3択の永続的な祝福) ---
# 祠や祭壇と違い、こちらは完全にランダムな3つの候補の中から
# プレイヤー自身が1つを選べる。運任せではなく戦略的な選択のギミック。
SPIRIT_CHANCE = 14   # フロアに出現する確率(%)。floor>=3から
SPIRIT_BLESSINGS = [
    ("STR +20",       "str",    20),
    ("DEF +15",       "def",    15),
    ("Max HP +40",    "life",   40),
    ("Food +120",     "food",   120),
    ("Potion +2",     "potion", 2),
    ("Blaze gem +2",  "gem",    2),
]
spirit_choice_options = []

def apply_spirit_blessing(option):
    global pl_str, pl_def_base, pl_lifemax, pl_life, food, potion, blazegem
    _, kind, amount = option
    if kind == "str":
        pl_str += amount
    elif kind == "def":
        pl_def_base += amount
    elif kind == "life":
        pl_lifemax += amount
        pl_life += amount
    elif kind == "food":
        food += amount
    elif kind == "potion":
        potion += amount
    elif kind == "gem":
        blazegem += amount

# --- 賞金首の掲示板(フロア限定のミニ討伐クエスト) ---
# 踏むと「このフロアを出るまでにN体倒す」という賞金首クエストを受注する。
# 目標数に達すればその場で報酬。フロアを出てしまうと失敗として消える
# (ペナルティは無く、単に報酬を逃すだけ)。
BOUNTY_CHANCE = 14   # フロアに出現する確率(%)。floor>=3から
bounty_active = False
bounty_target = 0
bounty_kills = 0

def start_bounty():
    global bounty_active, bounty_target, bounty_kills
    bounty_active = True
    bounty_target = random.randint(3, 5)
    bounty_kills = 0

def register_bounty_kill():
    """通常戦闘で敵を倒した直後に呼ぶ。賞金首クエスト中なら達成判定を行う。"""
    global bounty_active, bounty_kills, potion, blazegem, food, info_message, info_timer
    if not bounty_active:
        return
    bounty_kills += 1
    if bounty_kills >= bounty_target:
        bounty_active = False
        potion += 2
        blazegem += 3
        food += 100
        record_stat("bounties_completed")
        unlock_achievement("bounty_hunter")
        info_message = f"Bounty complete! ({bounty_target} kills) +2 Potion, +3 Blaze gem, +100 Food"
        info_timer = 70

# --- 精霊の祭具(ステージに応じて違う一時強化を与える) ---
# 通常フロアはバランス型、クリスタル洞窟は守り型、溶岩地帯は攻め型と、
# ステージのテーマに合わせて効果が変わる。フロアを出ると効果は切れる。
TOTEM_CHANCE = 13   # フロアに出現する確率(%)。floor>=4から
TOTEM_BUFFS = {
    0: {"str": 15, "def": 5,  "label": "Totem's balance"},
    1: {"str": 5,  "def": 20, "label": "Totem's ward"},
    2: {"str": 25, "def": 0,  "label": "Totem's wrath"},
}
totem_buff_active = False
totem_str_bonus = 0
totem_def_bonus = 0

# --- 分身の鏡(自分自身の力を宿した影と戦う) ---
# 鏡に触れると、その瞬間のプレイヤー自身の力を宿した「影の分身」が現れて戦闘になる。
# 常に自分と同じ強さの相手なので、これまでの成長を実感できる腕試しの機会になる。
MIRROR_CHANCE = 12   # フロアに出現する確率(%)。floor>=5から
doppelganger_battle_active = False
doppelganger_str = 0
doppelganger_lifemax = 0

# --- 宝の地図の切れ端(フロアに散らばる3枚を集めると豪華な報酬) ---
# 1枚だけでは何の役にも立たないが、同じフロアに散らばる3枚すべてを
# 集めきると、その場で埋蔵された財宝がまとめて手に入る。
MAP_FRAGMENT_FLOOR_CHANCE = 20   # このフロアに地図の切れ端一式が出現する確率(%)。floor>=4から
MAP_FRAGMENT_COUNT = 3           # 1フロアに散らばる枚数
map_fragments_active = False
map_fragments_found = 0

def place_map_fragments():
    """既存の床の中からMAP_FRAGMENT_COUNT枚を選び、地図の切れ端(30)を配置する。
    互いに、また他の特殊床とも隣接しない位置を選ぶ。"""
    global map_fragments_active, map_fragments_found
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] == 0 and not has_adjacent_special(x, y):
                candidates.append((x, y))
    if len(candidates) < MAP_FRAGMENT_COUNT:
        return
    random.shuffle(candidates)
    chosen = []
    for cx, cy in candidates:
        if all(abs(cx-ox)+abs(cy-oy) >= 5 for ox, oy in chosen):
            chosen.append((cx, cy))
        if len(chosen) >= MAP_FRAGMENT_COUNT:
            break
    if len(chosen) < MAP_FRAGMENT_COUNT:
        return
    for cx, cy in chosen:
        dungeon[cy][cx] = 30
    map_fragments_active = True
    map_fragments_found = 0

def register_map_fragment_found():
    """地図の切れ端を1枚拾った直後に呼ぶ。全て集まったら豪華な報酬を与える。"""
    global map_fragments_found, map_fragments_active
    global potion, blazegem, food, info_message, info_timer
    map_fragments_found += 1
    if map_fragments_found >= MAP_FRAGMENT_COUNT:
        map_fragments_active = False
        potion += 3
        blazegem += 5
        food += 150
        record_stat("map_fragment_sets_completed")
        unlock_achievement("cartographer")
        info_message = "Treasure map complete! +3 Potion, +5 Blaze gem, +150 Food"
        info_timer = 70
    else:
        info_message = f"Map fragment found! ({map_fragments_found}/{MAP_FRAGMENT_COUNT})"
        info_timer = 45

# --- 聖なる鍵と封印の宝物庫(鍵を持ち運んで扉を開ける) ---
# 圧力プレートと違い、鍵はアイテムとしてプレイヤーが持ち運ぶ。
# 同じフロアのどこかにある宝物庫まで鍵を運んで初めて開けられる。
SACRED_KEY_VAULT_CHANCE = 14   # フロアに鍵と宝物庫の組が出現する確率(%)。floor>=5から
has_sacred_key = False

def place_sacred_key_vault():
    """既存の床2マスに、聖なる鍵(31)と封印の宝物庫(32)を1組配置する。"""
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] == 0 and not has_adjacent_special(x, y):
                candidates.append((x, y))
    if len(candidates) < 2:
        return
    key_pos = random.choice(candidates)
    candidates.remove(key_pos)
    far_candidates = [c for c in candidates
                       if abs(c[0]-key_pos[0]) + abs(c[1]-key_pos[1]) >= 6]
    vault_pos = random.choice(far_candidates) if far_candidates else random.choice(candidates)
    dungeon[key_pos[1]][key_pos[0]] = 31
    dungeon[vault_pos[1]][vault_pos[0]] = 32

def open_sacred_vault():
    """聖なる鍵を持った状態で宝物庫に触れた時に呼ぶ。豪華な報酬を与えて鍵を消費する。"""
    global has_sacred_key, potion, blazegem, food, info_message, info_timer
    has_sacred_key = False
    potion += 2
    blazegem += 6
    food += 120
    record_stat("vaults_opened")
    unlock_achievement("vault_opener")
    info_message = "The vault opens! +2 Potion, +6 Blaze gem, +120 Food"
    info_timer = 70

# --- 守護者の像の試練(運やRNGではなく純粋なSTR判定) ---
# 触れた瞬間のSTRがフロアに応じたしきい値以上なら永続的な力を授かり、
# 届かなければ何も持ち去られることなく、ただ力不足を思い知らされるだけ。
STATUE_CHANCE = 12   # フロアに出現する確率(%)。floor>=5から

def statue_str_threshold(fl):
    """フロアに応じて要求STRを決める(深いフロアほど厳しくなる)。"""
    return int(110 + fl * 7)

def challenge_statue():
    """守護者の像に触れた瞬間に呼ぶ。STRがしきい値以上なら永続強化、届かなければ小さな代償。"""
    global pl_str, food, info_message, info_timer
    threshold = statue_str_threshold(floor)
    record_stat("statue_trials_attempted")
    if pl_str >= threshold:
        bonus = 15
        pl_str += bonus
        record_stat("statue_trials_passed")
        unlock_achievement("statue_trial_passed")
        info_message = f"The statue approves your strength! STR permanently +{bonus}"
        info_timer = 60
    else:
        penalty = 40
        food = max(0, food - penalty)
        info_message = f"The statue judges you unworthy (STR {pl_str}/{threshold}). -{penalty} Food"
        info_timer = 60

# --- 賭博場(ブレイズジェムを賭け金にした自分で選ぶギャンブル) ---
# 運命の祠や犠牲の祭壇と違い、こちらは掛け金と勝率をプレイヤー自身が3段階から選べる。
# ハイリスク・ハイリターンな一撃を選ぶか、手堅い小さな賭けにするか、
# それとも賭けずに立ち去るか -- 資源管理の駆け引きを楽しむギミック。
GAMBLE_DEN_CHANCE = 12   # フロアに出現する確率(%)。floor>=4から
GAMBLE_TIERS = [
    {"label": "Small Bet",   "cost": 2,  "win_chance": 60, "payout_mult": 2},
    {"label": "Medium Bet",  "cost": 5,  "win_chance": 45, "payout_mult": 3},
    {"label": "High Roller", "cost": 10, "win_chance": 30, "payout_mult": 5},
]
gamble_result_name = ""
gamble_result_desc = ""

def resolve_gamble(tier_index):
    """選んだ賭けの階層に応じて勝敗を決め、ブレイズジェムを増減させる。"""
    global blazegem, gamble_result_name, gamble_result_desc
    tier = GAMBLE_TIERS[tier_index]
    blazegem -= tier["cost"]
    record_stat("gambles_played")
    won = random.randint(0, 99) < tier["win_chance"]
    if won:
        payout = tier["cost"] * tier["payout_mult"]
        blazegem += payout
        gamble_result_name = "YOU WIN!"
        gamble_result_desc = f"+{payout} Blaze gem!"
        record_stat("gambles_won")
        if tier_index == len(GAMBLE_TIERS) - 1:
            unlock_achievement("high_roller")
    else:
        gamble_result_name = "YOU LOSE..."
        gamble_result_desc = f"-{tier['cost']} Blaze gem lost."

# --- キメラの巣(まれに出現する規格外の超強敵) ---
# ライオン・山羊・竜が混ざり合った伝説の魔獣。エリートよりもさらに遥かに格上で、
# フロアボスに匹敵するほどの強さを持つ。出現率は非常に低く、遭遇そのものが
# 稀少な体験になるよう作られている。倒せば破格の報酬が手に入る。
CHIMERA_CHANCE = 6    # フロアに出現する確率(%)。floor>=8から
chimera_battle_active = False

# --- 犠牲の祭壇(自分の意思でHPを捧げるギャンブル) ---
# 祠と違い、こちらは強制ではなく「捧げるか、立ち去るか」をプレイヤー自身が選ぶ。
# 成功すれば永続的なささやかな強化、失敗すればただ体力を失うだけ、
# 最悪の場合はさらなる呪いを受ける諸刃の剣。
ALTAR_CHANCE = 12       # フロアに出現する確率(%)。floor>=6から
ALTAR_HP_COST = 60      # 捧げるHP
ALTAR_OUTCOMES = [
    (35, "Boon",       "Permanent +10 Max HP, +5 STR, +3 DEF"),
    (40, "Silence",    "The altar takes your offering and gives nothing back"),
    (25, "Backlash",   "The altar punishes you! Extra HP lost and poisoned"),
]
altar_result_name = ""
altar_result_desc = ""

def roll_altar_outcome():
    """犠牲の祭壇の結果を実際に決めて効果を適用する。"""
    global altar_result_name, altar_result_desc
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_poison
    r = random.randint(1, 100)
    acc = 0
    chosen = ALTAR_OUTCOMES[-1]
    for weight, name, desc in ALTAR_OUTCOMES:
        acc += weight
        if r <= acc:
            chosen = (weight, name, desc)
            break
    _, name, desc = chosen
    if name == "Boon":
        pl_lifemax += 10
        pl_life += 10
        pl_str += 5
        pl_def_base += 3
        record_stat("altar_boons")
        unlock_achievement("altar_boon")
    elif name == "Silence":
        pass
    elif name == "Backlash":
        extra_dmg = max(1, int(pl_lifemax * 0.1))
        pl_life = max(1, pl_life - extra_dmg)
        pl_poison = max(pl_poison, 40)
    altar_result_name = name
    altar_result_desc = desc
    record_stat("altars_used")
    unlock_achievement("altar_sacrifice")

# --- 血の満月フロア(ハイリスク・ハイリターンのフロア全体イベント) ---
# フロア全体が『血の満月』になることがあり、そのフロアでは敵との遭遇が増え、
# 敵も強化されるが、経験値も多くもらえる。無事に階段へたどり着ければ
# 実績・統計にも記録される、危険と隣り合わせの一発挑戦。
BLOOD_MOON_CHANCE = 12       # フロアが血の満月になる確率(%)。floor>=8から
BLOOD_MOON_STR_MULT = 1.4    # 敵のHP/STR倍率
BLOOD_MOON_EXP_MULT = 1.5    # 獲得EXP倍率
BLOOD_MOON_ENCOUNTER_BONUS = 3  # イベント抽選プールに追加する遭遇(2)の重み
is_blood_moon = False

dmg_eff = 0
btl_cmd = 0

CRIT_FLASH_FRAMES = 6
crit_flash_timer = 0
crit_flash_color = (255, 255, 190)
last_atk_special = None  # None / "crit" / "finisher" — 直前の攻撃の演出種別(ダメージポップアップの見た目に使う)

# --- 実績解除トースト演出 ---
# 以前はunlock_achievement()がinfo_message(探索/バトル中の汎用メッセージ欄)を
# 使い回していたため、他のメッセージと表示位置・見た目が同じで地味だった。
# 実績はプレイヤーへの数少ない「ご褒美」演出なので、専用のゴールドバナーを
# 画面上部にスライドインさせ、バッジ画像付きで目立たせるようにする。
ACHIEVEMENT_TOAST_FRAMES = 150   # 表示している総フレーム数
ACHIEVEMENT_TOAST_SLIDE = 12     # 上からスライドインする所要フレーム数
ACHIEVEMENT_TOAST_FADE = 25      # 終了間際にフェードアウトする所要フレーム数
achievement_toast_label = ""
achievement_toast_timer = 0
achievement_sound_pending = False  # トーストと同時に鳴らすジングルの再生待ちフラグ
rare_treasure_sound_pending = False  # 希少な宝箱アイテムを引いた時に鳴らすジングルの再生待ちフラグ

# --- 画面シェイク演出 ---
# 被弾・会心の一撃・コンボフィニッシャーなど「衝撃」のある瞬間に、画面全体を
# 数フレームだけ小さくずらして描画することで打撃の重みを演出する。
# 実装はscreen.scroll()で現フレームの描画内容を数px揺らすだけの軽量な仕掛けで、
# 次フレームには通常通り再描画されるため見た目以外への影響はない。
screen_shake_timer = 0
screen_shake_mag = 0

# --- ダメージポップアップ演出 ---
# 攻撃がヒットした瞬間、命中した対象の頭上にダメージ数値が浮かび上がって
# フェードアウトする。「xxxpts of damage!」のメッセージ欄は画面右側に固定表示
# されるだけなので、実際に何がどこで殴られたのかを視覚的に補強する狙い。
DMG_POPUP_LIFE = 30
damage_popups = []  # [[x, y, text, color, life, big], ...]
_dmg_popup_font_big = None

def spawn_damage_popup(x, y, text, color, big=False):
    damage_popups.append([x, y, text, color, DMG_POPUP_LIFE, big])

def draw_damage_popups(bg, fnt):
    """ダメージポップアップを上へ浮かせつつフェードアウトしながら描画する。
    クリティカル/コンボフィニッシャーで生じたものは一回り大きいフォントで
    強調する。"""
    global _dmg_popup_font_big
    if not damage_popups:
        return
    if _dmg_popup_font_big is None:
        _dmg_popup_font_big = pygame.font.Font(None, 44)
    for p in damage_popups:
        x, y, text, color, life, big = p
        f = _dmg_popup_font_big if big else fnt
        rise = (DMG_POPUP_LIFE - life) * 1.3
        alpha = max(0, min(255, int(255 * life / DMG_POPUP_LIFE)))
        shadow = f.render(text, True, BLACK)
        shadow.set_alpha(alpha)
        bg.blit(shadow, [x + 1, y - rise + 2])
        sur = f.render(text, True, color)
        sur.set_alpha(alpha)
        bg.blit(sur, [x, y - rise])
        p[4] -= 1
    damage_popups[:] = [p for p in damage_popups if p[4] > 0]

info_message = ""
info_timer = 0

COMMAND = ["[A]ttack", "[P]otion","[B]laze gem","[R]un", "[D]efense", "[F]ocus"]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food + 30", "Food + 60", "Sord", "Defense Pill",
            "Ring of Vitality", "Amulet of Wisdom", "Food + 45", "Pet Egg"]
EMY_NAME = ["Green slime", "Red slime", "Axe beast", "Ogre", "Sword man",
            "Death hornet", "Signal slime", "Devil plant", "Twin killer", "Hell",
            "Dragon gear", "Crystal slime", "Shadow wisp", "Iron golem",
            "Venom spider", "Bone reaper", "Molten drake"]

# 通常モンスターの画像ファイル名は基本的に"enemy"+typ番号+".png"だが、
# typ 11以降はボス専用画像(enemy11.png〜enemy19.png)と番号が被ってしまうため、
# 新しく追加するモンスターだけは専用のファイル名で個別に対応させる。
REGULAR_ENEMY_IMAGE_OVERRIDE = {
    11: "enemy_crystal_slime.png",
    12: "enemy_shadow_wisp.png",
    13: "enemy_iron_golem.png",
    14: "enemy_venom_spider.png",
    15: "enemy_bone_reaper.png",
    16: "enemy_molten_drake.png",
}

def enemy_image_file(t):
    return REGULAR_ENEMY_IMAGE_OVERRIDE.get(t, f"enemy{t}.png")

# 敵/ボス画像は種類数が限られているのに、戦闘開始のたびpygame.image.load()で
# ディスクから読み直していたのでキャッシュする(初回だけ読み込んでconvert_alpha)
_enemy_image_cache = {}

def load_enemy_image(relpath):
    img = _enemy_image_cache.get(relpath)
    if img is None:
        img = pygame.image.load("image/" + relpath).convert_alpha()
        _enemy_image_cache[relpath] = img
    return img

_achievement_badge_cache = {}
_bestiary_detail_scale_cache = {}

def get_achievement_badge_image(size):
    """実績バッジ画像は毎フレーム同じ結果になるので、サイズごとにsmoothscale結果を
    キャッシュしておく(実績一覧画面は描画のたびに再スケールしていた)"""
    img = _achievement_badge_cache.get(size)
    if img is None:
        img = pygame.transform.smoothscale(imgAchBadge, (size, size))
        _achievement_badge_cache[size] = img
    return img

# --- ボス撃破後のドロップ演出 ---
# 永続強化とは別に、その場で使えるアイテムを2種類ランダムに授与し、
# 撃破画面の途中でアイコン付きで1つずつ表示する。
BOSS_LOOT_TABLE = [
    {"key": "potion",   "label": "+1 Potion",       "icon": 0},
    {"key": "blazegem", "label": "+1 Blaze gem",     "icon": 1},
    {"key": "defpill",  "label": "+1 Defense Pill",  "icon": 6},
    {"key": "food",     "label": "+50 Food",         "icon": 3},
]
boss_loot_rolled = []

MAZE_W = 11
MAZE_H = 9
maze = []
for y in range(MAZE_H):
    maze.append([0]*MAZE_W)
    
DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3
dungeon = []
for y in range(DUNGEON_H):
    dungeon.append([0]*DUNGEON_W)

# ミニマップ用: プレイヤーが実際に見た場所だけTrueになる
explored = []
for y in range(DUNGEON_H):
    explored.append([False]*DUNGEON_W)

# exploration_percent()を毎フレームのダンジョン全マス走査にしないための集計値。
# make_dungeon()でフロアごとにtotalを出し直し、_mark_explored()でseenを差分更新する。
_exploration_total = 0
_exploration_seen = 0

def _mark_explored(x, y):
    """explored[y][x]をTrueにする。新規に探索済みになったマスだけ_exploration_seenを増やす"""
    global _exploration_seen
    if not (0 <= x < DUNGEON_W and 0 <= y < DUNGEON_H) or explored[y][x]:
        return
    explored[y][x] = True
    if dungeon[y][x] not in (9, 25):
        _exploration_seen += 1

def maze_size_for_floor(fl):
    """フロアが深くなるほどマップを大きくする(3フロアごとに1段階拡張、上限あり)。
    難易度でサイズの伸び方に補正がかかる(Easy=小さめ、Hard=大きめ)"""
    step = min(10, (max(1, fl) - 1) // 3) + diff_params()["maze_step_bonus"]
    step = max(0, min(12, step))
    w = 11 + 2*step
    h = 9 + 2*step
    return w, h

# --- 探索率ボーナス ---
# フロアを去る(階段を上る)前に、そのフロアの歩ける床のうちどれだけ探索したかを
# 集計し、しっかり探索してから進んだプレイヤーに報酬を渡す。
# 「とりあえず階段に直行する」だけでなく寄り道して探索したくなるようにする狙い。
EXPLORATION_BONUS_THRESHOLD = 85   # この%以上でボーナス
EXPLORATION_PERFECT_THRESHOLD = 97  # この%以上でさらに豪華なボーナス

def exploration_percent():
    """現在のフロアで、壁(9)以外の歩ける床のうち探索済み(explored=True)の割合(%)
    毎フレームの全マス走査を避けるため、_exploration_total/_exploration_seenの
    集計値(make_dungeon()で初期化、_mark_explored()で更新)を使う"""
    if _exploration_total == 0:
        return 0
    return int(100 * _exploration_seen / _exploration_total)

def make_dungeon():
    global MAZE_W, MAZE_H, DUNGEON_W, DUNGEON_H, maze, dungeon, explored, hidden_treasure_pos
    global floor_modifier, wall_tint, wall_variant, floor_variant
    global collapsing_vault_bounds, collapse_timer
    global ambush_battles_remaining
    global boulder_pos, boulder_timer
    global is_blood_moon
    global mimic_battle_active
    global in_rift_battle
    global bounty_active
    global doppelganger_battle_active
    global map_fragments_active, map_fragments_found
    global has_sacred_key
    global chimera_battle_active
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    floor_modifier = roll_floor_modifier(floor)
    register_floor_modifier_seen(floor_modifier)
    wall_tint = roll_wall_tint(previous=wall_tint)
    wall_variant = stage_theme_variant(floor)
    floor_variant = stage_theme_variant(floor)
    generate_color_patches()
    hidden_treasure_pos = None
    collapsing_vault_bounds = None
    collapse_timer = 0
    ambush_battles_remaining = 0
    mimic_battle_active = False
    in_rift_battle = False
    bounty_active = False
    doppelganger_battle_active = False
    map_fragments_active = False
    map_fragments_found = 0
    has_sacred_key = False
    chimera_battle_active = False
    is_blood_moon = floor >= 8 and random.randint(0, 99) < BLOOD_MOON_CHANCE
    boulder_pos = None
    boulder_timer = 0
    # フロアに応じてマップサイズを決め直し、配列も新しいサイズで作り直す
    MAZE_W, MAZE_H = maze_size_for_floor(floor)
    DUNGEON_W = MAZE_W * 3
    DUNGEON_H = MAZE_H * 3
    maze = [[0]*MAZE_W for _ in range(MAZE_H)]
    dungeon = [[9]*DUNGEON_W for _ in range(DUNGEON_H)]
    if diff_params()["minimap_full_reveal"] or modifier_minimap_full_reveal():
        explored = [[True]*DUNGEON_W for _ in range(DUNGEON_H)]
    else:
        explored = [[False]*DUNGEON_W for _ in range(DUNGEON_H)]

    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H-1][x] = 1
    for y in range(1, MAZE_H-1):
        maze[y][0] = 1
        maze[y][MAZE_W-1] = 1
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            maze[y][x] = 0
            
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            maze[y][x] = 1
            
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            d = random.randint(0, 3)
            if x > 2:
                d = random.randint(0, 2)
            maze[y+YP[d]][x+XP[d]] = 1
    
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                # 開けた小部屋になる確率を下げて、細い通路中心の入り組んだ構成にする
                if random.randint(0, 99) < 8:
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0
                else:
                    dungeon[dy][dx] = 0
                    if maze[y-1][x] == 0: dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0: dungeon[dy+1][dx] = 0
                    if maze[y][x-1] == 0: dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0: dungeon[dy][dx+1] = 0

    if floor >= 5 and random.randint(0, 99) < COLLAPSING_VAULT_CHANCE:
        carve_collapsing_vault()
    else:
        carve_treasure_vault()
    carve_hidden_room()
    if floor >= 3 and random.randint(0, 99) < 40:
        carve_cursed_room()
    if floor >= 5 and random.randint(0, 99) < 60:
        place_warp_tile()
    if random.randint(0, 99) < 50:
        place_healing_spring()
    if floor >= 4 and random.randint(0, 99) < 50:
        place_ice_patch()
    if floor >= 3 and random.randint(0, 99) < 30:
        place_merchant()
    if floor >= 4 and random.randint(0, 99) < MONSTER_DEN_CHANCE:
        place_monster_den()
    if floor >= 4 and random.randint(0, 99) < IDOL_PEDESTAL_CHANCE:
        place_idol_pedestal()
    if floor >= 3 and random.randint(0, 99) < SHRINE_CHANCE:
        place_shrine()
    if floor >= 3 and random.randint(0, 99) < CAPTIVE_CHANCE:
        place_captive()
    if floor >= 5 and random.randint(0, 99) < RIFT_CHANCE:
        place_rift()
    if floor >= 6 and random.randint(0, 99) < ALTAR_CHANCE:
        place_altar()
    if floor >= 3 and random.randint(0, 99) < PUZZLE_DOOR_CHANCE:
        place_puzzle_door()
    if floor >= 3 and random.randint(0, 99) < SPIRIT_CHANCE:
        place_spirit()
    if floor >= 3 and random.randint(0, 99) < BOUNTY_CHANCE:
        place_bounty_board()
    if floor >= 4 and random.randint(0, 99) < TOTEM_CHANCE:
        place_totem()
    if floor >= 5 and random.randint(0, 99) < MIRROR_CHANCE:
        place_mirror()
    if floor >= 4 and random.randint(0, 99) < MAP_FRAGMENT_FLOOR_CHANCE:
        place_map_fragments()
    if floor >= 5 and random.randint(0, 99) < SACRED_KEY_VAULT_CHANCE:
        place_sacred_key_vault()
    if floor >= 5 and random.randint(0, 99) < STATUE_CHANCE:
        place_statue()
    if floor >= 4 and random.randint(0, 99) < GAMBLE_DEN_CHANCE:
        place_gambling_den()
    if floor >= 8 and random.randint(0, 99) < CHIMERA_CHANCE:
        place_chimera_lair()

    global _reveal_radius_last, _minimap_cache_surface
    _reveal_radius_last = None
    _minimap_cache_surface = None

# ワープ床・回復の泉・呪いの床・罠の床・氷の床・モンスターの巣・黄金の像・祠・
# 囚われの仲間・不安定な裂け目・犠牲の祭壇・圧力プレート・封印された扉は、
# 同じ種類同士・異なる種類同士を問わず隣接マスに並ばないようにする
# (ギミックが密集して分かりにくくなるのを防ぐ)
SPECIAL_FLOOR_TYPES = (4, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35)

def has_adjacent_special(x, y):
    for dxn, dyn in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = x + dxn, y + dyn
        if 0 <= xx < DUNGEON_W and 0 <= yy < DUNGEON_H:
            if dungeon[yy][xx] in SPECIAL_FLOOR_TYPES:
                return True
    return False

def carve_treasure_vault():
    """フロアに1つ、宝箱が複数まとまった特別な部屋を作り、
    その中央に見張り役のモンスター(繭)を置く。
    (put_eventが床マスにしかイベントを置かないので、ここで
    非0の値にしておけば上書きされずに残る)"""
    candidates = []
    for y in range(2, MAZE_H-2):
        for x in range(2, MAZE_W-2):
            if maze[y][x] == 0:
                candidates.append((x, y))
    if not candidates:
        return
    x, y = random.choice(candidates)
    dx = x*3 + 1
    dy = y*3 + 1
    for ry in range(-1, 2):
        for rx in range(-1, 2):
            if 0 <= dy+ry < DUNGEON_H and 0 <= dx+rx < DUNGEON_W:
                dungeon[dy+ry][dx+rx] = 0
    corners = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    random.shuffle(corners)
    for rx, ry in corners[:2]:
        dungeon[dy+ry][dx+rx] = 1
    dungeon[dy][dx] = 2

def carve_collapsing_vault():
    """崩落する古代の宝物庫: 見張りの繭は置かない代わりに、宝箱を4つとも敷き詰める。
    最初の宝箱を開けた瞬間に崩落が始まり、一定歩数以内にこの部屋(3x3の範囲)から
    出ないと生き埋めになってダメージを受ける『脱出チャレンジ』になる。"""
    global collapsing_vault_bounds
    candidates = []
    for y in range(2, MAZE_H-2):
        for x in range(2, MAZE_W-2):
            if maze[y][x] == 0:
                candidates.append((x, y))
    if not candidates:
        return
    x, y = random.choice(candidates)
    dx = x*3 + 1
    dy = y*3 + 1
    for ry in range(-1, 2):
        for rx in range(-1, 2):
            if 0 <= dy+ry < DUNGEON_H and 0 <= dx+rx < DUNGEON_W:
                dungeon[dy+ry][dx+rx] = 0
    for rx, ry in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        dungeon[dy+ry][dx+rx] = 1
    collapsing_vault_bounds = (dx-1, dy-1, dx+1, dy+1)

def carve_hidden_room():
    """既存の壁を1マスだけ『隠し壁』(10)にして、その裏に1マスの隠し部屋(宝箱)を作る。
    壁だったマスしか書き換えないので、通常の通路の繋がりは絶対に壊れない。
    隠し部屋の中身は、隠し壁が見つかるまで壁のまま隠しておき(丸見え防止)、
    プレイヤーが隠し壁に隣接した瞬間に壁と宝箱の両方を一緒に出現させる
    (reveal_hidden_adjacent参照)。"""
    global hidden_treasure_pos
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] not in (9, 25):
                continue
            for dxn, dyn in dirs:
                fx, fy = x-dxn, y-dyn
                bx, by = x+dxn, y+dyn
                if dungeon[fy][fx] == 0 and dungeon[by][bx] == 9:
                    candidates.append((x, y, bx, by))
    if not candidates:
        return
    x, y, bx, by = random.choice(candidates)
    dungeon[y][x] = 10
    # ここではまだ宝箱(1)にせず壁(9)のままにしておき、座標だけ覚えておく
    dungeon[by][bx] = 9
    hidden_treasure_pos = (bx, by)

def carve_cursed_room():
    """既存の床1マスを『呪いの床』(13)にする。他の特殊床とは隣接しない位置を選ぶ
    (以前は3x3の範囲を丸ごと呪いの床にしていたため、床が繋がっている場所では
    複数マスが縦・横に連続して並んでしまう不具合があったので、他の仕掛け
    (ワープ床・回復の泉)と同じ「1マスだけ選ぶ」方式に統一した)"""
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] == 0 and not has_adjacent_special(x, y):
                candidates.append((x, y))
    if not candidates:
        return
    x, y = random.choice(candidates)
    dungeon[y][x] = 13

def _place_single_special_tile(tile_id):
    """『他の特殊床と隣接しない空いている床を1つ選んでtile_idにする』という、
    15個のplace_*関数に共通する処理をまとめた共通ヘルパー。
    候補が無ければ何もしない(元の各関数と同じ)。"""
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] == 0 and not has_adjacent_special(x, y):
                candidates.append((x, y))
    if not candidates:
        return
    x, y = random.choice(candidates)
    dungeon[y][x] = tile_id

def place_warp_tile():
    """既存の床1マスをワープ床(11)にする。他の特殊床とは隣接しない位置を選ぶ"""
    _place_single_special_tile(11)

def place_merchant():
    """既存の床1マスに旅の商人(17)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    踏むと一度だけ簡易な取引ができ、その後タイルは消える。"""
    _place_single_special_tile(17)

def place_monster_den():
    """既存の床1マスにモンスターの巣(18)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    踏むと3体の敵と連続で戦う羽目になる代わりに、全て倒し切れば豪華な報酬がもらえる。"""
    _place_single_special_tile(18)

def place_idol_pedestal():
    """既存の床1マスに黄金の像の台座(19)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    像を持ち上げると即座に報酬が手に入る代わりに、その場から巨石が転がって追いかけてくる。"""
    _place_single_special_tile(19)

def place_shrine():
    """既存の床1マスに運命の祠(20)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    踏むと一度だけ運試しができる、一発勝負のギャンブル床。"""
    _place_single_special_tile(20)

def place_captive():
    """既存の床1マスに囚われの仲間(21)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    檻を壊して助け出すと、そのフロアの間だけ一緒に戦ってくれる仲間の力を借りられる
    (STR/DEFが一時的に上昇する)。"""
    _place_single_special_tile(21)

def place_rift():
    """既存の床1マスに不安定な裂け目(22)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    足を踏み入れると必ず強力な(エリート)敵との戦闘になる代わりに、
    勝てば通常より豪華な報酬がもらえるハイリスク・ハイリターンの床。"""
    _place_single_special_tile(22)

def place_altar():
    """既存の床1マスに犠牲の祭壇(23)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    HPを捧げるかどうかをプレイヤー自身が選べる、任意参加のギャンブル床。"""
    _place_single_special_tile(23)

def place_puzzle_door():
    """既存の床2マスに、圧力プレート(24)と封印された扉(25)を1組配置する。
    扉は壁と同じく通行できず、離れたプレートを踏むとフロア中の扉が開く。"""
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] == 0 and not has_adjacent_special(x, y):
                candidates.append((x, y))
    if len(candidates) < 2:
        return
    plate_pos = random.choice(candidates)
    candidates.remove(plate_pos)
    far_candidates = [c for c in candidates
                       if abs(c[0]-plate_pos[0]) + abs(c[1]-plate_pos[1]) >= 6]
    door_pos = random.choice(far_candidates) if far_candidates else random.choice(candidates)
    dungeon[plate_pos[1]][plate_pos[0]] = 24
    dungeon[door_pos[1]][door_pos[0]] = 25

def place_spirit():
    """既存の床1マスにさまよう精霊(26)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    3つの祝福候補からプレイヤーが1つを選べる。"""
    _place_single_special_tile(26)

def place_bounty_board():
    """既存の床1マスに賞金首の掲示板(27)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(27)

def place_totem():
    """既存の床1マスに精霊の祭具(28)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(28)

def place_mirror():
    """既存の床1マスに分身の鏡(29)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(29)

def place_statue():
    """既存の床1マスに守護者の像(33)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(33)

def place_gambling_den():
    """既存の床1マスに賭博場(34)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(34)

def place_chimera_lair():
    """既存の床1マスにキメラの巣(35)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(35)

def place_healing_spring():
    """既存の床1マスを回復の泉(12)にする。他の特殊床とは隣接しない位置を選ぶ"""
    _place_single_special_tile(12)

def place_ice_patch():
    """氷の床(16)を3〜6マスの直線状にまとめて配置する。氷に乗ると
    その方向へ壁にぶつかるまで自動で滑り続ける(move_player側で処理)。
    起点は他の特殊床と隣接しない位置を選ぶ。"""
    candidates = []
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            if dungeon[y][x] == 0 and not has_adjacent_special(x, y):
                candidates.append((x, y))
    if not candidates:
        return
    random.shuffle(candidates)
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for (sx, sy) in candidates:
        d = random.choice(dirs)
        length = random.randint(3, 6)
        cells = []
        cx, cy = sx, sy
        ok = True
        for i in range(length):
            if not (0 <= cx < DUNGEON_W and 0 <= cy < DUNGEON_H) or dungeon[cy][cx] != 0:
                ok = False
                break
            cells.append((cx, cy))
            cx += d[0]
            cy += d[1]
        # 最低3マス確保できた時点で採用する(壁に当たって短くなるのは許容)
        if len(cells) >= 3:
            for (ix, iy) in cells:
                dungeon[iy][ix] = 16
            return

def draw_dungeon(bg, fnt):
    bg.fill(BLACK)
    # 宝物庫が崩落中は、画面全体を小さく揺らして緊迫感を出す
    shake_x = shake_y = 0
    if collapse_timer > 0:
        shake_x = random.randint(-4, 4)
        shake_y = random.randint(-4, 4)
    for y in range(-4, 6):
        for x in range(-5, 6):
            base_x = (x+5)*80 + shake_x
            base_y = (y+4)*80 + shake_y

            offset_x = 0
            offset_y = 0
            if moving:
                offset_x = -move_dx * int(move_progress * 80)
                offset_y = -move_dy * int(move_progress * 80)
            X = base_x + offset_x
            Y = base_y + offset_y
            dx = pl_x + x
            dy = pl_y + y
            if 0 <= dx < DUNGEON_W and 0 <= dy < DUNGEON_H:
                _mark_explored(dx, dy)
                tv = dungeon[dy][dx]
                if tv <= 4:
                    if tv == 0 and floor_variant == 1:
                        bg.blit(imgFloorCrystal, [X, Y])
                    elif tv == 0 and floor_variant == 2:
                        bg.blit(imgFloorFlame, [X, Y])
                    elif tv == 1 and floor_variant == 1:
                        bg.blit(imgTboxCrystal, [X, Y])
                    elif tv == 1 and floor_variant == 2:
                        bg.blit(imgTboxFlame, [X, Y])
                    elif tv == 2 and floor_variant == 1:
                        bg.blit(imgCocoonCrystal, [X, Y])
                    elif tv == 2 and floor_variant == 2:
                        bg.blit(imgCocoonFlame, [X, Y])
                    elif tv == 4 and floor_variant == 1:
                        bg.blit(imgTrapCrystal, [X, Y])
                    elif tv == 4 and floor_variant == 2:
                        bg.blit(imgTrapFlame, [X, Y])
                    else:
                        bg.blit(imgFloor[tv],[X, Y])
                    if tv == 0:
                        # 何もないただの床だけに彩色パッチを重ねる(宝箱や階段等の目印は塗らない)
                        pc = patch_color_at(dx, dy)
                        if pc:
                            patch_ov = pygame.Surface((80, 80))
                            patch_ov.set_alpha(70)
                            patch_ov.fill(pc)
                            bg.blit(patch_ov, [X, Y])
                elif tv == 11:
                    # ワープ床は専用画像で見た目にわかるようにする(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgWarpCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgWarpFlame, [X, Y])
                    else:
                        bg.blit(imgFloor[5], [X, Y])
                elif tv == 12:
                    # 回復の泉も専用画像で見た目にわかるようにする(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgHealingSpringCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgHealingSpringFlame, [X, Y])
                    else:
                        bg.blit(imgFloor[6], [X, Y])
                elif tv == 13:
                    # 呪いの床も専用画像で見た目にわかるようにする
                    bg.blit(imgFloor[7], [X, Y])
                elif tv == 14:
                    # 罠の宝箱は見た目は普通の宝箱と同じ(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgTboxCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgTboxFlame, [X, Y])
                    else:
                        bg.blit(imgFloor[1], [X, Y])
                elif tv == 15:
                    # 隠しボーナス階段は見た目を通常の階段と全く同じにする(気づかれないように)
                    bg.blit(imgFloor[3], [X, Y])
                elif tv == 16:
                    # 氷の床は専用画像で表示する
                    bg.blit(imgFloor[8], [X, Y])
                elif tv == 17:
                    # 旅の商人は専用画像で表示する
                    bg.blit(imgFloor[9], [X, Y])
                elif tv == 18:
                    # モンスターの巣は繭を赤黒くティントして危険な雰囲気を出す
                    bg.blit(get_monster_den_image(), [X, Y])
                elif tv == 19:
                    # 黄金の像の台座は専用画像で表示する(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgIdolCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgIdolFlame, [X, Y])
                    else:
                        bg.blit(imgIdol, [X, Y])
                elif tv == 20:
                    # 運命の祠も専用画像で表示する(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgShrineCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgShrineFlame, [X, Y])
                    else:
                        bg.blit(imgShrine, [X, Y])
                elif tv == 21:
                    # 囚われの仲間(檻)も専用画像で表示する(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgCaptiveCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgCaptiveFlame, [X, Y])
                    else:
                        bg.blit(imgCaptive, [X, Y])
                elif tv == 22:
                    # 不安定な裂け目(踏むと必ずエリート戦)も専用画像で表示する(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgRiftCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgRiftFlame, [X, Y])
                    else:
                        bg.blit(imgRift, [X, Y])
                elif tv == 23:
                    # 犠牲の祭壇(HPを捧げるか選べる)も専用画像で表示する(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgAltarCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgAltarFlame, [X, Y])
                    else:
                        bg.blit(imgAltar, [X, Y])
                elif tv == 24:
                    # 圧力プレート(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgPressurePlateCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgPressurePlateFlame, [X, Y])
                    else:
                        bg.blit(imgPressurePlate, [X, Y])
                elif tv == 25:
                    # 封印された扉(壁と同じく通行不能。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgSealedDoorCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgSealedDoorFlame, [X, Y])
                    else:
                        bg.blit(imgSealedDoor, [X, Y])
                elif tv == 26:
                    # さまよう精霊(3択の祝福。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgSpiritCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgSpiritFlame, [X, Y])
                    else:
                        bg.blit(imgSpirit, [X, Y])
                elif tv == 27:
                    # 賞金首の掲示板(ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgBountyBoardCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgBountyBoardFlame, [X, Y])
                    else:
                        bg.blit(imgBountyBoard, [X, Y])
                elif tv == 28:
                    # 精霊の祭具(ステージに応じた一時強化。背景もステージテーマに応じて差し替え)
                    if floor_variant == 1:
                        bg.blit(imgTotemCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgTotemFlame, [X, Y])
                    else:
                        bg.blit(imgTotem, [X, Y])
                elif tv == 29:
                    # 分身の鏡(自分自身の力を宿した影と戦う。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgMirrorCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgMirrorFlame, [X, Y])
                    else:
                        bg.blit(imgMirror, [X, Y])
                elif tv == 30:
                    # 宝の地図の切れ端(3枚集めると豪華な報酬。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgMapFragmentCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgMapFragmentFlame, [X, Y])
                    else:
                        bg.blit(imgMapFragment, [X, Y])
                elif tv == 31:
                    # 聖なる鍵(拾って運ぶと宝物庫を開けられる。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgSacredKeyCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgSacredKeyFlame, [X, Y])
                    else:
                        bg.blit(imgSacredKey, [X, Y])
                elif tv == 32:
                    # 封印の宝物庫(鍵を持って触れると開く。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgVaultCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgVaultFlame, [X, Y])
                    else:
                        bg.blit(imgVault, [X, Y])
                elif tv == 33:
                    # 守護者の像(STR判定の試練。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgStatueCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgStatueFlame, [X, Y])
                    else:
                        bg.blit(imgStatue, [X, Y])
                elif tv == 34:
                    # 賭博場(ブレイズジェムを賭ける。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgGamblingDenCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgGamblingDenFlame, [X, Y])
                    else:
                        bg.blit(imgGamblingDen, [X, Y])
                elif tv == 35:
                    # キメラの巣(触れると規格外の超強敵と戦闘になる。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgChimeraLairCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgChimeraLairFlame, [X, Y])
                    else:
                        bg.blit(imgChimeraLair, [X, Y])
                elif tv == 36:
                    # 開いた封印の扉(圧力プレート解放後の見た目。ステージテーマに応じて背景を差し替え)
                    if floor_variant == 1:
                        bg.blit(imgSealedDoorOpenCrystal, [X, Y])
                    elif floor_variant == 2:
                        bg.blit(imgSealedDoorOpenFlame, [X, Y])
                    else:
                        bg.blit(imgSealedDoorOpen, [X, Y])
                if tv == 9 or tv == 10:
                    # 隠し壁(10)は発見されるまで普通の壁と同じ見た目
                    if wall_variant == 1:
                        cur_wall, cur_wall2 = imgWallCrystal, imgWallCrystalTop
                    elif wall_variant == 2:
                        cur_wall, cur_wall2 = imgWallFlame, imgWallFlameTop
                    else:
                        cur_wall, cur_wall2 = imgWall, imgWall2
                    # ランダムな色調ティントは、テーマ差し替えのない通常の壁(ステージ1)にのみ乗せる
                    apply_tint = wall_tint if wall_variant == 0 else None
                    bg.blit(cur_wall, [X, Y-40])
                    if apply_tint:
                        wall_ov = pygame.Surface((cur_wall.get_width(), cur_wall.get_height()))
                        wall_ov.set_alpha(80)
                        wall_ov.fill(apply_tint)
                        bg.blit(wall_ov, [X, Y-40])
                    if dy >= 1 and dungeon[dy-1][dx] in (9, 10):
                        bg.blit(cur_wall2, [X, Y-80])
                        if apply_tint:
                            wall_ov2 = pygame.Surface((cur_wall2.get_width(), cur_wall2.get_height()))
                            wall_ov2.set_alpha(80)
                            wall_ov2.fill(apply_tint)
                            bg.blit(wall_ov2, [X, Y-80])
            if golden_sprite_pos is not None and (dx, dy) == golden_sprite_pos:
                # 見つけやすいよう、脈打つ金色のオーラと上下にふわふわ揺れる動きを付ける
                gimg = get_golden_sprite_image()
                bob = int(6 * abs((tmr % 20) - 10) / 10) - 3
                glow_r = 34 + int(6 * abs((tmr % 16) - 8))
                glow = pygame.Surface((glow_r*2, glow_r*2), pygame.SRCALPHA)
                pygame.draw.ellipse(glow, (255, 220, 90, 90), [0, 0, glow_r*2, glow_r*2])
                bg.blit(glow, [X+40-glow_r, Y+40-glow_r+bob])
                bg.blit(gimg, [X + (80-gimg.get_width())//2, Y + (80-gimg.get_height())//2 + bob])
            if boulder_pos is not None and (dx, dy) == boulder_pos:
                # 巨石は小刻みに震わせて「転がっている」勢いを出す
                jx = random.randint(-3, 3)
                jy = random.randint(-3, 3)
                bg.blit(imgBoulder, [X + (80-imgBoulder.get_width())//2 + jx,
                                     Y + (80-imgBoulder.get_height())//2 + jy])
            if x == 0 and y == 0:
                cur_player_set = imgPlayerSets.get(selected_character, imgPlayer)
                bg.blit(cur_player_set[pl_a], [X, Y-40])
    reveal_hidden_adjacent()
    dp = diff_params()
    reveal_radius(max(1, BASE_VISION_RADIUS + dp["vision_radius_bonus"] + modifier_vision_delta() + skill_vision_bonus))
    stage_tint = STAGE_TINTS.get(current_stage(floor))
    mod_color = FLOOR_MODIFIERS[floor_modifier]["color"] if floor_modifier else None
    if stage_tint or mod_color:
        overlay = pygame.Surface((880, 720))
        overlay.set_alpha(45)
        if stage_tint and mod_color:
            blended = tuple((stage_tint[i] + mod_color[i]) // 2 for i in range(3))
            overlay.fill(blended)
        elif mod_color:
            overlay.fill(mod_color)
        else:
            overlay.fill(stage_tint)
        bg.blit(overlay, [0, 0])
    if is_blood_moon:
        # 血の満月フロアは、常時うっすらと血のような赤いフィルターをかけておく
        moon_overlay = pygame.Surface((880, 720))
        moon_overlay.set_alpha(40)
        moon_overlay.fill((150, 15, 15))
        bg.blit(moon_overlay, [0, 0])
    bg.blit(imgDark, [0, 0])
    if collapse_timer > 0:
        # 崩落中は赤い縁取りを脈打たせて危機感を強める
        pulse = 60 + int(50 * abs((tmr % 20) - 10) / 10)
        vignette = pygame.Surface((880, 720), pygame.SRCALPHA)
        pygame.draw.rect(vignette, (200, 20, 10, pulse), [0, 0, 880, 720], width=26)
        bg.blit(vignette, [0, 0])
    draw_low_hp_warning(bg)
    if dp["minimap_enabled"]:
        draw_minimap(bg)
    draw_para(bg, fnt)
    draw_crit_flash(bg)

    if info_timer > 0 and info_message != "":
        draw_text(bg, info_message, 300, 300, fnt, CYAN)

def reveal_hidden_adjacent():
    """プレイヤーが隠し壁(10)に隣接したら、自動的に通れる床(0)にし、
    その裏に隠していた宝箱も同時に出現させる"""
    global hidden_treasure_pos, _exploration_total, _exploration_seen
    for dxn, dyn in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = pl_x + dxn, pl_y + dyn
        if 0 <= xx < DUNGEON_W and 0 <= yy < DUNGEON_H and dungeon[yy][xx] == 10:
            dungeon[yy][xx] = 0
            if hidden_treasure_pos is not None:
                bx, by = hidden_treasure_pos
                dungeon[by][bx] = 1
                hidden_treasure_pos = None
                # この宝箱マスは今まで壁(9)扱いでexploration_percent()の集計から
                # 除外されていたため、床になった今、集計に組み込む
                _exploration_total += 1
                if explored[by][bx]:
                    _exploration_seen += 1

_reveal_radius_last = None

def reveal_radius(radius):
    """プレイヤー周辺の(見た目の描画範囲とは別に)ミニマップ上の探索済み範囲を広げる。
    難易度のvision_radius_bonusで広さが変わる。プレイヤーが動いていない間は
    同じマス集合を毎フレーム塗り直すだけなので、位置と半径が前回と同じならスキップする"""
    global _reveal_radius_last
    if radius <= 0:
        return
    state = (pl_x, pl_y, radius)
    if state == _reveal_radius_last:
        return
    _reveal_radius_last = state
    for dy in range(-radius, radius+1):
        for dx in range(-radius, radius+1):
            if abs(dx) + abs(dy) > radius:
                continue
            yy = pl_y + dy
            xx = pl_x + dx
            if 0 <= xx < DUNGEON_W and 0 <= yy < DUNGEON_H:
                _mark_explored(xx, yy)
    
MINIMAP_RIGHT = 860
MINIMAP_Y = 95
MINIMAP_MAXW = 220
MINIMAP_MAXH = 460

# ミニマップは毎フレームDUNGEON_W*DUNGEON_H マス分fillし直すと重いので、
# 探索済みマスの絵柄をオフスクリーンSurfaceにキャッシュしておき、数フレームに
# 1回だけ(または新しく探索が進んだ時だけ)描き直す。プレイヤーの現在地マーカーは
# 動き続けるので、キャッシュした地図の上から毎フレーム重ねて描く。
_minimap_cache_surface = None
_minimap_cache_key = None
_minimap_rebuild_interval = 4

def draw_minimap(bg):
    global _minimap_cache_surface, _minimap_cache_key
    # マップが大きくなっても画面からはみ出さないよう、セルサイズを自動で縮小する
    cell = 4
    while DUNGEON_W*cell > MINIMAP_MAXW or DUNGEON_H*cell > MINIMAP_MAXH:
        cell -= 1
        if cell <= 1:
            cell = 1
            break
    x0 = MINIMAP_RIGHT - DUNGEON_W*cell
    y0 = MINIMAP_Y
    w = DUNGEON_W * cell
    h = DUNGEON_H * cell

    cache_key = (DUNGEON_W, DUNGEON_H, cell)
    if (_minimap_cache_surface is None or _minimap_cache_key != cache_key
            or tmr % _minimap_rebuild_interval == 0):
        surf = pygame.Surface((w, h))
        surf.fill(BLACK)
        for y in range(DUNGEON_H):
            for x in range(DUNGEON_W):
                if not explored[y][x]:
                    continue
                v = dungeon[y][x]
                if v == 9 or v == 10:
                    col = (90, 90, 90)
                elif v == 3 or v == 15:
                    col = (255, 255, 0)
                elif v == 1:
                    col = (0, 200, 200)
                elif v == 2:
                    col = (200, 80, 80)
                elif v == 4:
                    col = (255, 140, 0)
                elif v == 16:
                    col = (150, 220, 255)
                elif v == 17:
                    col = (255, 180, 60)
                else:
                    col = (180, 180, 180)
                surf.fill(col, [x*cell, y*cell, cell, cell])
        _minimap_cache_surface = surf
        _minimap_cache_key = cache_key

    pygame.draw.rect(bg, BLACK, [x0-2, y0-2, w+4, h+4])
    pygame.draw.rect(bg, WHITE, [x0-2, y0-2, w+4, h+4], 1)
    bg.blit(_minimap_cache_surface, [x0, y0])
    px = x0 + pl_x*cell
    py = y0 + pl_y*cell
    bg.fill(RED, [px, py, cell, cell])
    
def count_nearby_treasures(x, y, radius=1):
    """(x,y)を中心とした周辺(既定は3x3=1部屋相当)に既にある宝箱(1)の数を数える。
    1部屋あたりの宝箱を2個以下に抑えるための密集チェックに使う。"""
    c = 0
    for dy in range(-radius, radius+1):
        for dx in range(-radius, radius+1):
            yy, xx = y+dy, x+dx
            if 0 <= xx < DUNGEON_W and 0 <= yy < DUNGEON_H and dungeon[yy][xx] == 1:
                c += 1
    return c

def stairs_count_for_floor():
    """マップが大きいほど、選べる階段の数を増やす(小さいフロアは2つ、大きいフロアは3つ)"""
    if min(DUNGEON_W, DUNGEON_H) >= 50:
        return 3
    return 2

def place_stairs(count):
    """階段(3)を互いに離れた位置に複数配置する。各階段は他の階段からできるだけ離し、
    どのルートを通ってもプレイヤーが行き先を選べるようにする(ダンジョンの自由度アップ)。
    階段が2つ以上(=分岐)あるとき、1000分の1の確率でそのうち1つが『隠しボーナス階段』(15)になる。
    見た目は通常の階段と全く同じで、上るまでどちらがアタリかは分からない。"""
    positions = []
    min_dist = max(4, min(DUNGEON_W, DUNGEON_H) // 4)
    attempts = 0
    while len(positions) < count and attempts < 3000:
        attempts += 1
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if dungeon[y][x] != 0:
            continue
        if any(abs(px-x) + abs(py-y) < min_dist for px, py in positions):
            continue
        for ry in range(-1, 2):
            for rx in range(-1, 2):
                yy, xx = y+ry, x+rx
                if 0 <= yy < DUNGEON_H and 0 <= xx < DUNGEON_W:
                    dungeon[yy][xx] = 0
        dungeon[y][x] = 3
        positions.append((x, y))
    if len(positions) >= 2 and random.randint(1, 1000) == 1:
        bx, by = random.choice(positions)
        dungeon[by][bx] = 15
    return positions

def generate_bonus_room():
    """隠しボーナス階段から辿り着く特大部屋。5〜8個の宝箱と、次のフロアへの
    階段だけを置いた特別な一部屋だけのミニフロアにする。通常の
    『1部屋につき宝箱2個まで』という制限はこの部屋には適用しない。"""
    global DUNGEON_W, DUNGEON_H, MAZE_W, MAZE_H, dungeon, explored, pl_x, pl_y, pl_d, pl_a
    global golden_sprite_pos, golden_sprite_timer
    golden_sprite_pos = None
    golden_sprite_timer = 0
    DUNGEON_W = 25
    DUNGEON_H = 19
    MAZE_W = DUNGEON_W // 3
    MAZE_H = DUNGEON_H // 3
    dungeon = [[9]*DUNGEON_W for _ in range(DUNGEON_H)]
    for y in range(1, DUNGEON_H-1):
        for x in range(1, DUNGEON_W-1):
            dungeon[y][x] = 0
    # 特別な部屋なので、最初から全体をミニマップに表示する
    explored = [[True]*DUNGEON_W for _ in range(DUNGEON_H)]

    chest_count = random.randint(5, 8)
    placed = 0
    attempts = 0
    while placed < chest_count and attempts < 500:
        attempts += 1
        x = random.randint(2, DUNGEON_W-3)
        y = random.randint(2, DUNGEON_H-3)
        if dungeon[y][x] == 0:
            dungeon[y][x] = 1
            placed += 1

    pl_x = DUNGEON_W // 2
    pl_y = DUNGEON_H // 2
    dungeon[pl_y][pl_x] = 0
    pl_d = 1
    pl_a = 2

    tries = 0
    while tries < 500:
        x = random.randint(2, DUNGEON_W-3)
        y = random.randint(2, DUNGEON_H-3)
        if dungeon[y][x] == 0 and (x, y) != (pl_x, pl_y):
            dungeon[y][x] = 3
            break
        tries += 1

    # ボーナス部屋も通常フロアと同じくdungeon/explored/サイズを丸ごと作り直すので、
    # exploration_percent()用の集計値もここで出し直す(全マス最初から探索済み扱い)
    global _exploration_total, _exploration_seen, _reveal_radius_last, _minimap_cache_surface
    _exploration_total = sum(1 for row in dungeon for v in row if v not in (9, 25))
    _exploration_seen = sum(
        1 for y in range(DUNGEON_H) for x in range(DUNGEON_W)
        if explored[y][x] and dungeon[y][x] not in (9, 25)
    )
    _reveal_radius_last = None
    _minimap_cache_surface = None

def put_event():
    global pl_x, pl_y, pl_d, pl_a
    place_stairs(stairs_count_for_floor())
    trm = diff_params()["trap_rate_mult"] * modifier_trap_mult()
    trap_weight = max(1, round(2 * trm))
    trapchest_weight = max(0, round(1 * trm)) if floor >= 8 else 0
    monster_weight = max(1, round(6 * modifier_encounter_mult()))
    treasure_weight = max(1, round(2 * modifier_treasure_weight_mult()))
    event_pool = [1]*treasure_weight + [2]*monster_weight + [4]*trap_weight + [14]*trapchest_weight
    if is_blood_moon:
        # 血の満月フロアは、モンスターとの遭遇(2)がぐっと増える
        event_pool += [2]*BLOOD_MOON_ENCOUNTER_BONUS
    for i in range(60):
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if(dungeon[y][x] == 0):
            v = random.choice(event_pool)
            # 罠の床(4)は他の特殊床(ワープ・回復の泉・呪いの床・別の罠)と隣接させない
            if v in SPECIAL_FLOOR_TYPES and has_adjacent_special(x, y):
                continue
            # 宝箱(1)は同じ部屋(周辺5x5=部屋の対角まで)に既に2個あれば、これ以上増やさない
            if v == 1 and count_nearby_treasures(x, y, radius=2) >= 2:
                continue
            dungeon[y][x] = v

    while True:
        pl_x = random.randint(3, DUNGEON_W-4)
        pl_y = random.randint(3, DUNGEON_H-4)
        if(dungeon[pl_y][pl_x] == 0):
            break
    pl_d = 1
    pl_a = 2
    roll_golden_sprite()

    # put_event()まで終わって初めてそのフロアの壁/床レイアウトが確定する
    # (place_stairsが階段周りを強制的に床へ掘り直すため、make_dungeon()直後の
    # 時点ではまだ総マス数が確定しない)。ここでexploration_percent()用の
    # 集計値を出し直す。
    global _exploration_total, _exploration_seen
    _exploration_total = sum(1 for row in dungeon for v in row if v not in (9, 25))
    _exploration_seen = sum(
        1 for y in range(DUNGEON_H) for x in range(DUNGEON_W)
        if explored[y][x] and dungeon[y][x] not in (9, 25)
    )

def move_player(key):
    global idx, tmr, pl_x, pl_y, pl_d, pl_a
    global pl_life, food, potion, blazegem, treasure, floor ,pl_str
    global pl_def_base, pl_def_buff, def_pill, flg_action
    global moving, move_progress, hold_dir, hold_timer
    global pl_lifemax, pl_exp_mult
    global pl_poison, curse_active, info_message, info_timer
    global pending_bonus_room
    global ambush_battles_remaining
    global boulder_pos, boulder_timer
    global mimic_battle_active
    global ally_buff_active
    global in_rift_battle
    global spirit_choice_options
    global totem_buff_active, totem_str_bonus, totem_def_bonus
    global doppelganger_battle_active, doppelganger_str, doppelganger_lifemax
    global has_sacred_key
    global chimera_battle_active
    global steps_taken_accum

    if dungeon[pl_y][pl_x] == 1:
        dungeon[pl_y][pl_x] = 0
        if floor >= 6 and not modifier_mimic_immune() and random.randint(0, 99) < MIMIC_CHANCE:
            mimic_battle_active = True
            record_stat("mimics_encountered")
            info_message = "It's a Mimic!!"
            info_timer = 45
            idx = 10
            tmr = 0
            try:
                moving = False
                move_progress = 0.0
                hold_dir = None
                hold_timer = 0
            except NameError:
                pass
            return
        record_stat("treasures_opened")
        if load_stats().get("treasures_opened", 0) >= 150:
            unlock_achievement("treasure_hunter")
        ib = diff_params()["item_bonus"] + skill_item_bonus + pet_item_bonus + modifier_item_bonus()
        treasure = random.choice([0,0,0,1,1,1,1,1,1,2,6,6])
        if floor >= 10:
            treasure = random.choice([0,0,0,1,1,1,1,1,1,2,5,6,6])
            r = random.randint(0, 99)
            if treasure in (5, 6) and r < max(0, min(99, 30 - ib)):
                treasure = 0
        if floor >= 15:
            # さらに深いフロアでは指輪(最大HP上昇)とアミュレット(EXP倍率上昇)が低確率で出現
            treasure = random.choice([0,0,0,1,1,1,1,1,1,2,5,6,6,7,8])
            r = random.randint(0, 99)
            if treasure in (5, 6, 7, 8) and r < max(0, min(99, 40 - ib)):
                treasure = 0
        if floor >= 5 and pet_type is None and random.randint(0, 99) < 3:
            # まだ仲間がいない場合、低確率(3%)でペットの卵に差し替える
            treasure = 10
        if treasure == 0:
            potion = potion + 1
        if treasure == 1:
            blazegem = blazegem + 1
        if treasure == 2:
            food = int(food/2)
        if treasure == 5:
            pl_str += 30
        if treasure == 6:
            pl_def_base += 5
            def_pill += 1 
        if treasure == 7:
            pl_lifemax += 50
            pl_life += 50
        if treasure == 8:
            pl_exp_mult += 0.1
        if treasure in (5, 6, 7, 8):
            # 指輪/アミュレット等の希少なアイテムを引いた時だけ、達成感を強めるために
            # クリティカルヒットと同じ画面フラッシュ機構を金色で流用し、レベルアップと
            # 同じジングルを鳴らす(通常のポーション/爆炎石とは違う特別感を演出)。
            # seリスト自体はmain()内のローカル変数なのでここから直接は再生できず、
            # achievement_sound_pendingと同じ「再生待ちフラグ」パターンを踏襲する。
            global crit_flash_timer, crit_flash_color, rare_treasure_sound_pending
            crit_flash_color = (255, 215, 90)
            crit_flash_timer = CRIT_FLASH_FRAMES + 2
            rare_treasure_sound_pending = True
        if treasure == 10:
            hatch_random_pet()
            info_message = f"{PET_TYPES[pet_type]['name']} hatched!"
            info_timer = 60
        record_item_seen(treasure)
        if collapsing_vault_bounds is not None:
            x0, y0, x1, y1 = collapsing_vault_bounds
            if x0 <= pl_x <= x1 and y0 <= pl_y <= y1:
                trigger_vault_collapse()
        idx = 3
        tmr = 0
        return
    if dungeon[pl_y][pl_x] == 2:
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 99)
        if r < 45:
            treasure = random.choice([3,3,3,3,4,4,9,9,9])
            fym = skill_food_yield_mult * modifier_food_yield_mult()
            if treasure == 3: food = food + int(30 * fym)
            if treasure == 4: food = food + int(60 * fym)
            if treasure == 9: food = food + int(45 * fym)
            record_item_seen(treasure)
            idx = 3
            tmr = 0
        else:
            idx = 10
            tmr = 0
            try:
                moving = False
                move_progress = 0.0
                hold_dir = None
                hold_timer = 0
            except NameError:
                pass
        return
    if dungeon[pl_y][pl_x] == 3:
        if is_boss_floor(floor) and floor not in boss_floors_cleared:
            idx = 25
            tmr = 0
            try:
                moving = False
                move_progress = 0.0
                hold_dir = None
                hold_timer = 0
            except NameError:
                pass
        elif floor >= MAX_FLOOR:
            # 最終ステージのボスを倒し済みの状態(オートセーブ再開など)で
            # 階段に乗った場合は、フロアを増やさずゲームクリア演出へ直行する
            idx = 27
            tmr = 0
            try:
                moving = False
                move_progress = 0.0
                hold_dir = None
                hold_timer = 0
            except NameError:
                pass
        else:
            idx = 2
            tmr = 0
        return

    if dungeon[pl_y][pl_x] == 15:
        # 隠しボーナス階段(通常の階段と見た目は同じ、1000分の1で発生)
        dungeon[pl_y][pl_x] = 0
        pending_bonus_room = True
        idx = 2
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return
    
    if dungeon[pl_y][pl_x] == 4:
        dungeon[pl_y][pl_x] = 0
        tdm = diff_params()["trap_dmg_mult"] * skill_trap_dmg_mult * modifier_trap_dmg_mult()
        r = random.randint(0, 99)
        if r < 10:
            base_dmg = 50
        elif r < 30:
            base_dmg = 30
        else:
            base_dmg = 10
        pl_life = pl_life - max(1, int(base_dmg * tdm))
        idx = 4
        tmr = 0
        add_trap_count(1)
        
        if pl_life < 0:
            idx = 9
        return

    if dungeon[pl_y][pl_x] == 11:
        # ワープ床: ランダムな床マスへ転送する
        tries = 0
        while tries < 500:
            nx = random.randint(3, DUNGEON_W-4)
            ny = random.randint(3, DUNGEON_H-4)
            if dungeon[ny][nx] == 0 and (nx, ny) != (pl_x, pl_y):
                pl_x, pl_y = nx, ny
                break
            tries += 1
        info_message = "Warped!"
        info_timer = 40
        return

    if dungeon[pl_y][pl_x] == 12:
        # 回復の泉: 1回だけ全回復して床に戻る
        dungeon[pl_y][pl_x] = 0
        pl_life = pl_lifemax
        food += int(30 * skill_food_yield_mult)
        info_message = "Refreshed!"
        info_timer = 40
        return

    if dungeon[pl_y][pl_x] == 13:
        # 呪いの床: このフロアの間だけSTR/DEFが下がる(フロア移動時に解除)
        dungeon[pl_y][pl_x] = 0
        if modifier_curse_immune():
            info_message = "Warded! The curse fades harmlessly."
            info_timer = 45
        elif not curse_active:
            curse_active = True
            pl_str = max(1, pl_str - 20)
            pl_def_base = pl_def_base - 5
            info_message = "Cursed! STR/DEF down!"
            info_timer = 45
        return

    if dungeon[pl_y][pl_x] == 14:
        # 罠の宝箱: 見た目は宝箱だが、爆発か毒ガスが仕掛けられている
        dungeon[pl_y][pl_x] = 0
        tdm = diff_params()["trap_dmg_mult"] * skill_trap_dmg_mult * modifier_trap_dmg_mult()
        add_trap_count(1)
        if random.randint(0, 1) == 0:
            dmg = max(1, int(random.randint(20, 50) * tdm))
            pl_life -= dmg
            info_message = f"Trapped chest! {dmg}dmg!"
            info_timer = 45
            if pl_life < 0:
                idx = 9
                tmr = 0
        else:
            pl_poison = max(pl_poison, 50)
            info_message = "Poison gas!"
            info_timer = 45
        return

    if dungeon[pl_y][pl_x] == 17:
        # 旅の商人: 一度だけ簡易な取引ができる(その後タイルは消える)
        dungeon[pl_y][pl_x] = 0
        idx = 48
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 18:
        # モンスターの巣: 3体の敵と連続で戦う羽目になる
        dungeon[pl_y][pl_x] = 0
        ambush_battles_remaining = MONSTER_DEN_WAVES
        info_message = "You've stumbled into a monster den!"
        info_timer = 45
        idx = 10
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 19:
        # 黄金の像: 持ち上げた瞬間に報酬をもらえるが、背後で巨石が転がり出す
        dungeon[pl_y][pl_x] = 0
        pl_lifemax += 40
        pl_life += 40
        blazegem += 2
        info_message = "You grabbed the idol! Something is rumbling... RUN!"
        info_timer = 55
        boulder_pos = (pl_x, pl_y)
        boulder_timer = BOULDER_CHASE_DURATION
        return

    if dungeon[pl_y][pl_x] == 20:
        # 運命の祠: 一度だけ運試しができる
        dungeon[pl_y][pl_x] = 0
        idx = 54
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 21:
        # 囚われの仲間: 檻を壊して救出すると、このフロアの間だけSTR/DEFが上がる
        dungeon[pl_y][pl_x] = 0
        if not ally_buff_active:
            ally_buff_active = True
            pl_str += ALLY_STR_BONUS
            pl_def_base += ALLY_DEF_BONUS
            record_stat("allies_rescued")
            unlock_achievement("ally_rescued")
            info_message = f"Rescued! +{ALLY_STR_BONUS} STR, +{ALLY_DEF_BONUS} DEF for this floor"
            info_timer = 55
        return

    if dungeon[pl_y][pl_x] == 22:
        # 不安定な裂け目: 必ずエリートとの戦闘になる
        dungeon[pl_y][pl_x] = 0
        in_rift_battle = True
        record_stat("rifts_entered")
        info_message = "The rift pulls you in... an Elite awaits!"
        info_timer = 50
        idx = 10
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 23:
        # 犠牲の祭壇: HPを捧げるかどうかをここで選ばせる(idx==61の専用画面へ)
        dungeon[pl_y][pl_x] = 0
        idx = 61
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 24:
        # 圧力プレート: このフロアにある封印された扉をすべて開く(開いた扉は専用グラフィックに差し替え)
        dungeon[pl_y][pl_x] = 0
        opened = 0
        for yy in range(DUNGEON_H):
            for xx in range(DUNGEON_W):
                if dungeon[yy][xx] == 25:
                    dungeon[yy][xx] = 36
                    opened += 1
        if opened > 0:
            record_stat("pressure_plates_triggered")
            unlock_achievement("door_unlocked")
            info_message = "A door unlocks somewhere on this floor..."
            info_timer = 50
        return

    if dungeon[pl_y][pl_x] == 26:
        # さまよう精霊: 3つの祝福候補から1つをプレイヤーに選ばせる(idx==64へ)
        dungeon[pl_y][pl_x] = 0
        spirit_choice_options = random.sample(SPIRIT_BLESSINGS, 3)
        record_stat("spirits_encountered")
        idx = 64
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 27:
        # 賞金首の掲示板: このフロアを出るまでにN体倒すクエストを受注する
        dungeon[pl_y][pl_x] = 0
        if not bounty_active:
            start_bounty()
            info_message = f"Bounty accepted: defeat {bounty_target} enemies on this floor!"
            info_timer = 55
        return

    if dungeon[pl_y][pl_x] == 28:
        # 精霊の祭具: ステージに応じた一時強化(このフロアの間だけ)
        dungeon[pl_y][pl_x] = 0
        if not totem_buff_active:
            totem_buff_active = True
            buff = TOTEM_BUFFS[floor_variant]
            totem_str_bonus = buff["str"]
            totem_def_bonus = buff["def"]
            pl_str += totem_str_bonus
            pl_def_base += totem_def_bonus
            record_stat("totems_used")
            unlock_achievement("totem_channeled")
            info_message = f"{buff['label']}! +{totem_str_bonus} STR, +{totem_def_bonus} DEF for this floor"
            info_timer = 55
        return

    if dungeon[pl_y][pl_x] == 29:
        # 分身の鏡: 触れた瞬間の自分自身の力を宿した影の分身と戦う
        dungeon[pl_y][pl_x] = 0
        doppelganger_str = pl_str
        doppelganger_lifemax = pl_lifemax
        doppelganger_battle_active = True
        record_stat("doppelgangers_encountered")
        info_message = "Your reflection steps out of the mirror..."
        info_timer = 45
        idx = 10
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 30:
        # 宝の地図の切れ端: 同じフロアの3枚すべて集めると豪華な報酬
        dungeon[pl_y][pl_x] = 0
        register_map_fragment_found()
        return

    if dungeon[pl_y][pl_x] == 31:
        # 聖なる鍵: 拾って持ち運ぶ
        dungeon[pl_y][pl_x] = 0
        has_sacred_key = True
        record_stat("sacred_keys_found")
        info_message = "You found a Sacred Key! Find the vault to unlock it."
        info_timer = 55
        return

    if dungeon[pl_y][pl_x] == 32:
        # 封印の宝物庫: 鍵を持っていれば開く
        if has_sacred_key:
            dungeon[pl_y][pl_x] = 0
            open_sacred_vault()
        else:
            info_message = "The vault is sealed. You need a Sacred Key."
            info_timer = 40
        return

    if dungeon[pl_y][pl_x] == 33:
        # 守護者の像: STRがしきい値以上か問われる試練
        dungeon[pl_y][pl_x] = 0
        challenge_statue()
        return

    if dungeon[pl_y][pl_x] == 34:
        # 賭博場: 掛け金の階層を選んでブレイズジェムを賭ける
        dungeon[pl_y][pl_x] = 0
        idx = 65
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 35:
        # キメラの巣: 規格外の超強敵との戦闘が始まる
        dungeon[pl_y][pl_x] = 0
        chimera_battle_active = True
        record_stat("chimeras_encountered")
        info_message = "A monstrous roar shakes the air... the Chimera awakens!"
        info_timer = 50
        idx = 10
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

def draw_text(bg, txt, x, y, fnt, col):
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def draw_low_hp_warning(bg):
    """HPが最大値の20%を切ると、心拍のように速く脈打つ赤い縁取りを
    画面端に表示する(探索/バトル共通)。崩落演出よりも脈拍を速くして、
    見分けがつくようにしている。"""
    if pl_lifemax <= 0 or pl_life <= 0:
        return
    if pl_life / pl_lifemax > LOW_HP_WARNING_RATIO:
        return
    pulse = 70 + int(60 * abs((tmr % 16) - 8) / 8)
    vignette = pygame.Surface((880, 720), pygame.SRCALPHA)
    pygame.draw.rect(vignette, (255, 0, 30, pulse), [0, 0, 880, 720], width=22)
    bg.blit(vignette, [0, 0])

def draw_crit_flash(bg):
    """クリティカルヒット/コンボフィニッシャー発動時に、画面全体を短く光らせて
    爽快感を演出する。crit_flash_timerが立っている間だけ描画し、フレームが
    進むごとに透明度を下げてすぐ消えるようにする。screen_flash_enabledが
    OFFの場合は光過敏なプレイヤー向けに描画自体をスキップする
    (タイマーは進めておき、設定を戻したときに古い演出が急に出ないようにする)。"""
    global crit_flash_timer
    if crit_flash_timer <= 0:
        return
    if not screen_flash_enabled:
        crit_flash_timer = 0
        return
    # コンボフィニッシャー/自己ベストコンボ更新の演出はcrit_flash_timerを
    # CRIT_FLASH_FRAMES+2/+4という高い初期値でセットするため、クランプしないと
    # alphaが255を超えてpygame.Surface.fill()がValueErrorで落ちる
    # (実際にこのPRのテスト中にコンボフィニッシャー発動でクラッシュを確認した)。
    alpha = max(0, min(255, int(190 * crit_flash_timer / CRIT_FLASH_FRAMES)))
    flash = pygame.Surface((880, 720), pygame.SRCALPHA)
    flash.fill((*crit_flash_color, alpha))
    bg.blit(flash, [0, 0])
    crit_flash_timer -= 1

ACHIEVEMENT_TOAST_W = 420
ACHIEVEMENT_TOAST_H = 66
_achievement_toast_hdr_font = None
_achievement_toast_lbl_font = None

def draw_achievement_toast(bg):
    """実績解除時、画面上部にゴールドのバナーをスライドインさせ、バッジ画像と
    共に『Achievement Unlocked!』を表示する。探索中/バトル中/メニュー中を
    問わずメインループの描画の最後(画面更新の直前)から呼ばれるので、
    どの画面状態でも同じように目立つ。"""
    global achievement_toast_timer, _achievement_toast_hdr_font, _achievement_toast_lbl_font
    if achievement_toast_timer <= 0:
        return
    elapsed = ACHIEVEMENT_TOAST_FRAMES - achievement_toast_timer
    if elapsed < ACHIEVEMENT_TOAST_SLIDE:
        t = elapsed / ACHIEVEMENT_TOAST_SLIDE
        y = int(-ACHIEVEMENT_TOAST_H * (1 - t))
        alpha = int(255 * t)
    elif achievement_toast_timer <= ACHIEVEMENT_TOAST_FADE:
        t = achievement_toast_timer / ACHIEVEMENT_TOAST_FADE
        y = 0
        alpha = int(255 * t)
    else:
        y = 0
        alpha = 255
    x = (880 - ACHIEVEMENT_TOAST_W) // 2
    top = 14 + y
    glow = 140 + int(90 * abs((tmr % 24) - 12) / 12)
    panel = pygame.Surface((ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H), pygame.SRCALPHA)
    panel.fill((25, 20, 5, min(230, alpha)))
    pygame.draw.rect(panel, (255, 210, 60, min(255, alpha)), [0, 0, ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H], width=3)
    pygame.draw.rect(panel, (255, 230, 140, min(glow, alpha)), [0, 0, ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H], width=1)
    bg.blit(panel, [x, top])
    badge = get_achievement_badge_image(46)
    badge_sur = badge.copy()
    badge_sur.set_alpha(alpha)
    bg.blit(badge_sur, [x + 10, top + 10])
    if _achievement_toast_hdr_font is None:
        _achievement_toast_hdr_font = pygame.font.Font(None, 22)
        _achievement_toast_lbl_font = pygame.font.Font(None, 24)
    hdr = _achievement_toast_hdr_font.render("ACHIEVEMENT UNLOCKED!", True, (255, 215, 90))
    hdr.set_alpha(alpha)
    bg.blit(hdr, [x + 66, top + 10])
    lbl = _achievement_toast_lbl_font.render(achievement_toast_label, True, WHITE)
    lbl.set_alpha(alpha)
    bg.blit(lbl, [x + 66, top + 34])
    achievement_toast_timer -= 1

_pet_icon_scaled_cache = {}
_def_pill_warn_icon_cache = {}

def draw_pet_status(bg, x, y, fnt):
    """『Pet: 名前』の左側に小さなアイコンを添えて表示する。
    アイコンはテキストの行の高さに収まるよう自動で縮小する。
    一定間隔でrev画像(左右反転版)と入れ替えて、ペットが生きているように
    ちょこちょこ向きを変える簡単なアイドルアニメーションにする。
    pet_typeが変わらない限りスケール済み画像は同じなので、smoothscale結果を
    キャッシュして毎フレームの再生成を避ける。"""
    rev = (tmr // 40) % 2 != 0
    if rev:
        icon = imgPetRev.get(pet_type, imgPet.get(pet_type))
    else:
        icon = imgPet.get(pet_type)
    label = f"Pet: {PET_TYPES[pet_type]['name']}"
    text_x = x
    if icon is not None:
        line_h = fnt.size(label)[1]
        iw, ih = icon.get_width(), icon.get_height()
        if ih > line_h:
            cache_key = (pet_type, rev, line_h)
            scaled = _pet_icon_scaled_cache.get(cache_key)
            if scaled is None:
                scale = line_h / ih
                scaled = pygame.transform.smoothscale(icon, (max(1, int(iw*scale)), line_h))
                _pet_icon_scaled_cache[cache_key] = scaled
            icon = scaled
        bg.blit(icon, [x, y])
        text_x = x + icon.get_width() + 6
    draw_text(bg, label, text_x, y, fnt, (150, 220, 255))
    
def draw_para(bg, fnt):
    X = 30
    Y = 600
    bg.blit(imgParaSets.get(selected_character, imgPara), [X, Y])
    col = WHITE
    if pl_lifemax > 0 and tmr%2 == 0:
        hp_ratio = pl_life / pl_lifemax
        if hp_ratio <= LOW_HP_WARNING_RATIO:
            col = RED
        elif hp_ratio <= HP_MID_WARNING_RATIO:
            col = HP_MID_WARNING_COLOR
    draw_text(bg, f"{pl_life}/{pl_lifemax}", X+128, Y+6, fnt, col)
    draw_text(bg, str(pl_str), X+128, Y+33, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr%2 == 0:
        col = RED
    elif 0 < food <= FOOD_LOW_WARNING_THRESHOLD and tmr%2 == 0:
        col = FOOD_LOW_WARNING_COLOR
    draw_text(bg, str(food), X+128, Y+60, fnt, col)
    potion_col = WHITE
    if potion == 0:
        potion_col = POTION_EMPTY_COLOR
    elif potion <= POTION_LOW_WARNING_THRESHOLD and tmr%2 == 0:
        potion_col = POTION_LOW_WARNING_COLOR
    draw_text(bg, str(potion), X+266, Y+6, fnt, potion_col)
    # ポーションと同様、爆炎石も0になったら灰色に変えて回復/攻撃札切れに
    # パッと気づけるようにする(従来はポーションのみ灰色化していた)。
    # さらに、残り1個まで減った時点でもオレンジ点滅させ、0になる前に
    # 気づけるようにする(食料の事前警告と同じ考え方)。
    blazegem_col = WHITE
    if blazegem == 0:
        blazegem_col = POTION_EMPTY_COLOR
    elif blazegem <= POTION_LOW_WARNING_THRESHOLD and tmr%2 == 0:
        blazegem_col = POTION_LOW_WARNING_COLOR
    draw_text(bg, str(blazegem), X+266, Y+33, fnt, blazegem_col)
    X2, Y2 = 350, 600
    bg.blit(imgPara2, [X2, Y2])
    draw_text(bg, f"DEF   : {pl_def_base}", X2+10, Y2+6, fnt, WHITE)
    draw_text(bg, f"DEF T: {pl_def_buff}", X2+10, Y2+33, fnt, WHITE)
    shield_img = imgItem[6]
    icon_w = shield_img.get_width()
    icon_h = shield_img.get_height()
    X_icon = X2 + 1
    Y_icon = Y2 + 50

    # ポーション・爆炎石と同様、防御の薬(Defense Pill)も0個/残りわずかで
    # 気づきやすくする。従来はアイコン表示のみで色分けが無く、3種類の消費
    # アイテムの中で防御の薬だけ在庫切れ・残り僅かに気づきにくかったため、
    # 表示ルールを他の2つに揃えて改善した。
    if def_pill == 0:
        draw_text(bg, "0", X_icon, Y_icon + icon_h//4, fnt, POTION_EMPTY_COLOR)
    elif def_pill <= POTION_LOW_WARNING_THRESHOLD:
        warn_icon = _def_pill_warn_icon_cache.get(id(shield_img))
        if warn_icon is None:
            warn_icon = tint_surface(shield_img, POTION_LOW_WARNING_COLOR)
            _def_pill_warn_icon_cache[id(shield_img)] = warn_icon
        bg.blit(warn_icon if tmr%2 == 0 else shield_img, [X_icon, Y_icon])
    elif def_pill <= 3:
        for i in range(def_pill):
            bg.blit(shield_img, [X_icon + i*(icon_w + 1), Y_icon])
    else:
        bg.blit(shield_img, [X_icon, Y_icon])
        draw_text(bg, f"x{def_pill}", X_icon + icon_w + 6, Y_icon + icon_h//4, fnt, WHITE)
    
def exp_threshold(level):
    """そのレベルに到達するために必要な累積EXP。
    ポケモンのMedium Fastグループ相当(lv^3)で、レベルが上がるほど
    必要EXPが積み上がっていく曲線にしている。"""
    if level <= 1:
        return 0
    return level ** 3

def init_battle():
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, typ, emy_lv
    global pl_charge, pl_poison, battle_took_damage
    global combo_count, combo_record_shown_this_battle
    global is_elite
    pl_charge = False
    pl_poison = 0
    battle_took_damage = False
    combo_count = 0
    combo_record_shown_this_battle = False
    if mimic_battle_active:
        is_elite = False
        typ = 0
        lev = max(1, floor)
        emy_lv = lev
        imgEnemy = load_enemy_image("enemy_mimic.png")
        emy_name = "Mimic LV" + str(lev)
        emy_lifemax = int((60 * 3 + (lev - 1) * 10) * MIMIC_LIFE_MULT)
        emy_str = int((emy_lifemax / 8) * MIMIC_STR_MULT)
        dp = diff_params()
        emy_lifemax = max(1, int(emy_lifemax * dp["enemy_life_mult"]))
        emy_str = max(1, int(emy_str * dp["enemy_str_mult"]))
        if is_blood_moon:
            emy_lifemax = int(emy_lifemax * BLOOD_MOON_STR_MULT)
            emy_str = int(emy_str * BLOOD_MOON_STR_MULT)
        emy_life = emy_lifemax
        emy_x = 440 - imgEnemy.get_width() / 2
        emy_y = 560 - imgEnemy.get_height()
        return
    if doppelganger_battle_active:
        is_elite = False
        typ = 0
        emy_lv = max(1, floor)
        src = imgPlayerSets.get(selected_character, imgPlayer)[2]
        shadow = tint_surface(src, DOPPELGANGER_TINT)
        scale = 2.2
        imgEnemy = pygame.transform.smoothscale(
            shadow, (int(shadow.get_width() * scale), int(shadow.get_height() * scale)))
        emy_name = "Shadow " + selected_character.capitalize() + " LV" + str(emy_lv)
        emy_lifemax = max(1, doppelganger_lifemax)
        emy_str = max(1, doppelganger_str)
        emy_life = emy_lifemax
        emy_x = 440 - imgEnemy.get_width() / 2
        emy_y = 560 - imgEnemy.get_height()
        return
    if chimera_battle_active:
        is_elite = False
        typ = 0
        lev = max(1, floor)
        emy_lv = lev
        imgEnemy = load_enemy_image("enemy_chimera.png")
        emy_name = "Chimera LV" + str(lev)
        dp = diff_params()
        emy_lifemax = max(1, int((250 + floor * 45) * dp["enemy_life_mult"]))
        emy_str = max(1, int((40 + floor * 6) * dp["enemy_str_mult"]))
        if is_blood_moon:
            emy_lifemax = int(emy_lifemax * BLOOD_MOON_STR_MULT)
            emy_str = int(emy_str * BLOOD_MOON_STR_MULT)
        emy_life = emy_lifemax
        emy_x = 440 - imgEnemy.get_width() / 2
        emy_y = 560 - imgEnemy.get_height()
        return
    if floor >= 30:
        typ = random.randint(8, 16)
        lev = random.randint(floor - 2, floor)
    elif floor >= 15:
        typ = random.randint(0, 16)
        lev = random.randint(floor - 4, floor)
    elif floor >= 11:
        typ = random.randint(0, 16)
        lev = random.randint(floor - 5, floor)
    else:
        typ = random.randint(0, floor)
        lev = random.randint(1, floor)
    emy_lv = lev
    is_elite = random.randint(0, 99) < (ELITE_CHANCE + modifier_elite_chance_bonus())
    if in_rift_battle:
        is_elite = True  # 裂け目から出てくる敵は必ずエリート
    imgEnemy = load_enemy_image(enemy_image_file(typ))
    if is_elite:
        imgEnemy = tint_surface(imgEnemy, ELITE_TINT)
    emy_name = ("Elite " if is_elite else "") + EMY_NAME[typ]+" LV"+str(lev)
    emy_lifemax = 60*(typ+1)+(lev-1)*10
    emy_str = int(emy_lifemax/8)
    dp = diff_params()
    emy_lifemax = max(1, int(emy_lifemax * dp["enemy_life_mult"]))
    emy_str = max(1, int(emy_str * dp["enemy_str_mult"]))
    if is_elite:
        emy_lifemax = int(emy_lifemax * ELITE_LIFE_MULT)
        emy_str = int(emy_str * ELITE_STR_MULT)
    if in_rift_battle:
        emy_lifemax = int(emy_lifemax * RIFT_LIFE_MULT)
        emy_str = int(emy_str * RIFT_STR_MULT)
    if is_blood_moon:
        emy_lifemax = int(emy_lifemax * BLOOD_MOON_STR_MULT)
        emy_str = int(emy_str * BLOOD_MOON_STR_MULT)
    emy_life = emy_lifemax
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()
    record_enemy_seen(typ)

BOSS_IMAGE_MAP = {
    10: "enemy11.png", 20: "enemy12.png", 30: "enemy13.png",  # ステージ1(10/20/30階)
    40: "enemy14.png", 50: "enemy15.png", 60: "enemy16.png",  # ステージ2(10/20/30階)
    70: "enemy17.png", 80: "enemy18.png", 90: "enemy19.png",  # ステージ3(10/20/30階)
}
BOSS_HIDDEN_IMAGE = "enemy16.png"

def boss_image_file(fl):
    return BOSS_IMAGE_MAP.get(fl, BOSS_HIDDEN_IMAGE)

# --- エコーバトル(撃破済みボスとの再戦) ---
# 通常のボス画像(enemyNN.png)をそのまま使い、対応するボスだけ図鑑から
# 再戦を挑めるようにする。
ECHO_ORI_MAP = {
    10: "enemy11.png", 20: "enemy12.png", 30: "enemy13.png",
    40: "enemy14.png", 50: "enemy15.png", 60: "enemy16.png",
    70: "enemy17.png", 80: "enemy18.png", 90: "enemy19.png",
}
ECHO_ELIGIBLE_FLOORS = sorted(ECHO_ORI_MAP.keys())

def register_echo_boss_defeat(fl):
    """Echo Battle勝利のたびに撃破済みフロアを記録する。全エコーボスを
    1体ずつ撃破し終えたら、称号"Echomaster"と一度きりの永続ボーナスを与える。"""
    global pl_lifemax, pl_life
    data = load_achievements()
    defeated = set(data.get("echo_floors_defeated", []))
    defeated.add(fl)
    data["echo_floors_defeated"] = sorted(defeated)
    already_mastered = data.get("echo_master", False)
    save_achievements(data)
    if not already_mastered and defeated.issuperset(ECHO_ELIGIBLE_FLOORS):
        pl_lifemax += 50
        pl_life += 50
        unlock_achievement("echo_master")

def boss_name_for_floor(fl):
    """ボスの表示名をフロア番号から算出する(init_boss_battleと図鑑の両方から使う共通ロジック)"""
    stg = current_stage(fl)
    lf = stage_local_floor(fl)
    if fl >= MAX_FLOOR:
        return "Final Boss"
    elif lf == STAGE_LENGTH:
        return f"Stage {stg} Boss"
    else:
        return f"Stage {stg} Guardian"

# 図鑑(Bestiary)用: 全ステージボス+隠しボスを1つのリストにまとめる(floor, name, image_file)
BOSS_BESTIARY = [(fl, boss_name_for_floor(fl), BOSS_IMAGE_MAP[fl]) for fl in BOSS_IMAGE_MAP] + \
                [(HIDDEN_FLOOR, "??? The Unbound", HIDDEN_BOSS_IMAGE)]

def boss_bestiary_index_for_floor(fl):
    for i, (bfl, _, _) in enumerate(BOSS_BESTIARY):
        if bfl == fl:
            return i
    return None

def init_boss_battle():
    """各ステージ内の10,20,30階(相対)のボス戦。専用の強さ・名前・見た目で初期化する。
    BGMは専用曲(Tolerance_Deviation.mp3)を使用する。ゲーム全体の最終ボス
    (最終ステージの30階、global floor==MAX_FLOOR)はさらに強化されたパラメータになる。"""
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, typ, emy_lv
    global pl_charge, pl_poison, battle_took_damage
    global combo_count
    global boss_phase2
    global is_elite
    pl_charge = False
    pl_poison = 0
    battle_took_damage = False
    combo_count = 0
    boss_phase2 = False
    is_elite = False
    typ = 12
    emy_lv = floor
    dp = diff_params()
    emy_lifemax = max(1, int((900 + floor*60) * dp["enemy_life_mult"]))
    emy_str = max(1, int((50 + floor*7) * dp["enemy_str_mult"]))
    is_final = floor >= MAX_FLOOR
    if is_final:
        emy_lifemax = int(emy_lifemax * 1.5)
        emy_str = int(emy_str * 1.3)
    emy_life = emy_lifemax
    imgEnemy = load_enemy_image(boss_image_file(floor))
    emy_name = boss_name_for_floor(floor)
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()
    bi = boss_bestiary_index_for_floor(floor)
    if bi is not None:
        record_boss_seen(bi)

def init_hidden_boss_battle():
    """隠しステージの裏ボス。全3ステージクリア後にタイトル画面から挑戦できる、
    通常の最終ボスよりもさらに強い専用の一体。"""
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, typ, emy_lv
    global pl_charge, pl_poison, battle_took_damage
    global combo_count
    global boss_phase2
    global is_elite
    pl_charge = False
    pl_poison = 0
    battle_took_damage = False
    combo_count = 0
    boss_phase2 = False
    is_elite = False
    typ = 12
    emy_lv = HIDDEN_FLOOR
    dp = diff_params()
    emy_lifemax = max(1, int((900 + MAX_FLOOR*60) * 2.0 * dp["enemy_life_mult"]))
    emy_str = max(1, int((50 + MAX_FLOOR*7) * 1.6 * dp["enemy_str_mult"]))
    emy_life = emy_lifemax
    imgEnemy = load_enemy_image(HIDDEN_BOSS_IMAGE)
    emy_name = "??? The Unbound"
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()
    bi = boss_bestiary_index_for_floor(floor)
    if bi is not None:
        record_boss_seen(bi)

# --- エコーバトル用の状態 ---
in_echo_battle = False
echo_target_floor = None

def init_echo_boss_battle(target_floor):
    """図鑑から挑む再戦。ダンジョン進行用のグローバルfloorは一切書き換えず、
    target_floorの数値だけを使って本来のボスと同じ強さを再現する。
    見た目は色反転版の専用画像(ECHO_ORI_MAP)を使う。"""
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, typ, emy_lv
    global pl_charge, pl_poison, battle_took_damage
    global combo_count
    global boss_phase2
    global is_elite
    pl_charge = False
    pl_poison = 0
    battle_took_damage = False
    combo_count = 0
    boss_phase2 = False
    is_elite = False
    typ = 12
    emy_lv = target_floor
    dp = diff_params()
    emy_lifemax = max(1, int((900 + target_floor*60) * dp["enemy_life_mult"]))
    emy_str = max(1, int((50 + target_floor*7) * dp["enemy_str_mult"]))
    emy_life = emy_lifemax
    imgEnemy = load_enemy_image(ECHO_ORI_MAP[target_floor])
    emy_name = "Echo of " + boss_name_for_floor(target_floor)
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()

def start_echo_battle(target_floor):
    """記録メニューのエコーバトル選択画面から呼ぶ。まだ今回のセッションで
    キャラクターを作っていない(タイトルからそのまま記録を見に来た)場合は、
    隠しボス挑戦と同様にそこそこ強めのステータスを即座に用意する。"""
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_def_buff, def_pill
    global food, food_acc, potion, blazegem, pl_poison, pl_charge, battle_took_damage
    global in_echo_battle, echo_target_floor, idx, tmr
    dp = diff_params()
    cp = char_params()
    if pl_lifemax <= 0:
        pl_lifemax = 300 + dp["pl_lifemax_bonus"] + cp["lifemax"] + 100
        pl_life = pl_lifemax
        pl_str = 100 + dp["pl_str_bonus"] + cp["str"] + 30
        pl_def_base = 0 + dp["pl_def_bonus"] + cp["def"] + 10
        pl_def_buff = 0
        def_pill = 1
        food = 300
        food_acc = 0.0
        potion = 2
        blazegem = 2
    pl_poison = 0
    pl_charge = False
    battle_took_damage = False
    in_echo_battle = True
    echo_target_floor = target_floor
    init_echo_boss_battle(target_floor)
    init_message()
    pygame.mixer.music.load("sound/Tolerance_Deviation.mp3")
    pygame.mixer.music.play(-1)
    idx = 51
    tmr = 0

def draw_bar(bg, x, y, w, h, val, max, color=(0, 128, 255)):
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, color, [x, y, w*val/max, h])
        
EXP_BAR_NEAR_LEVELUP_RATIO = 0.9
EXP_BAR_PULSE_COLOR = (255, 215, 0)

def draw_exp_bar(bg, x, y, w, h):
    """現在レベル内でのEXP進捗を横バーで表示する。あと一歩でレベルアップという
    タイミング(残り10%以内)が地味な緑色バーのままだと気づきにくかったため、
    HP/食料などの事前警告と同じ考え方で、90%以上溜まると金色に点滅させて
    「もうすぐレベルアップ」という期待感を煽るようにした。"""
    lo = exp_threshold(pl_lv)
    hi = exp_threshold(pl_lv + 1)
    span = max(1, hi - lo)
    prog = max(0, pl_exp - lo)
    prog = min(prog, span)  # レベルアップ演出が終わるまでは満タン(100%)で止めて表示上あふれさせない
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if prog > 0:
        col = (60, 200, 70)
        if prog / span >= EXP_BAR_NEAR_LEVELUP_RATIO and tmr % 2 == 0:
            col = EXP_BAR_PULSE_COLOR
        pygame.draw.rect(bg, col, [x, y, w*prog/span, h])
        
def draw_level_gauge(bg, x, y, fnt, bar_w=150, bar_h=14):
    """'Lv◯'表示とEXPバーの高さを揃え、バーをテキストのすぐ右に配置する"""
    label = f"Lv{pl_lv}"
    lw, lh = fnt.size(label)
    draw_text(bg, label, x, y, fnt, WHITE)
    bar_y = y + (lh - bar_h)//2
    bar_x = x + lw + 8
    draw_exp_bar(bg, bar_x, bar_y, bar_w, bar_h)
        
def draw_battle(bg, fnt):
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg_floor = echo_target_floor if (in_echo_battle and echo_target_floor is not None) else floor
    bg.blit(battle_bg_for_floor(bg_floor), [bx, by])
    if emy_life > 0 and emy_blink%2 ==0:
        if is_elite:
            # 通常の色調ティントだけでは元の色によって目立ちにくいため、
            # 敵の後ろに脈打つ金色のオーラを描いて『特別な個体』だと一目でわかるようにする
            glow_r = 80 + int(12 * abs((tmr % 24) - 12))
            glow = pygame.Surface((glow_r*2, glow_r*2), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (255, 210, 60, 100), [0, 0, glow_r*2, glow_r*2])
            gx = int(emy_x + imgEnemy.get_width()/2 - glow_r)
            gy = int(emy_y + emy_step + imgEnemy.get_height()/2 - glow_r)
            bg.blit(glow, [gx, gy])
        bg.blit(imgEnemy, [emy_x, emy_y+emy_step])
    boss_enraged = (in_boss_battle or in_echo_battle) and boss_phase2
    if boss_enraged:
        # フェーズ2(HP50%以下)に入ったボスは、HPバーを脈打つ赤に染めて
        # 「怒り状態」であることを常時わかるようにする(一度きりのメッセージだけでは
        # ターンが進むと消えて忘れられてしまうため)。
        pulse = 140 + int(90 * abs((tmr % 20) - 10) / 10)
        draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax, (255, pulse//3, 30))
    else:
        draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax)
        if in_boss_battle or in_echo_battle:
            # ボス・エコーバトルでは、フェーズ2(激怒)へ切り替わる50%ラインに
            # 目印の縦線を常時表示する。従来はHPが50%を切った瞬間に初めて
            # 「激怒」だとわかったが、あとどれだけ削ればフェーズ2に入るのか
            # 戦闘開始時から見通せなかったため、事前に狙いを定められるように追加した。
            mark_x = 340 + 100
            pygame.draw.line(bg, (255, 200, 200), [mark_x, 578], [mark_x, 590], 2)
    if is_elite:
        draw_text(bg, "* ELITE *", 340, 560, fnt, (255, 210, 90))
    if boss_enraged:
        draw_text(bg, "* ENRAGED *", 340, 560, fnt, (255, 90, 40))
    if chimera_battle_active:
        draw_text(bg, "* LEGENDARY CHIMERA *", 240, 560, fnt, (255, 90, 60))
    if emy_blink > 0:
        emy_blink = emy_blink-1
    draw_level_gauge(bg, 60, 34, fnt)
    status_y = 64
    if floor_modifier:
        # 入室時の"Welcome to floor"メッセージは数秒で消えてしまい、バトル中に
        # そのフロアの特性を忘れがちだったため、バトル画面にも常時小さく表示する。
        fm = FLOOR_MODIFIERS[floor_modifier]
        draw_text(bg, fm["name"], 60, status_y, fnt, fm["color"])
        status_y += 24
    if pl_poison > 0:
        draw_text(bg, f"POISON x{pl_poison}", 60, status_y, fnt, (190, 80, 220))
        status_y += 24
    if combo_count >= 2:
        if combo_count >= COMBO_FINISHER_THRESHOLD:
            draw_text(bg, f"COMBO x{combo_count} FINISHER READY!", 60, status_y, fnt, (255, 60, 220))
        else:
            combo_bonus_pct = int(round((combo_damage_mult() - 1.0) * 100))
            draw_text(bg, f"COMBO x{combo_count} (+{combo_bonus_pct}% dmg)", 60, status_y, fnt, (255, 160, 0))
        status_y += 24
    if pet_type is not None:
        draw_pet_status(bg, 60, status_y, fnt)
        status_y += 24
    for i in range(10):
        msg_txt, msg_col = message[i]
        draw_text(bg, msg_txt, 600, 100+i*50, fnt, msg_col)
    draw_low_hp_warning(bg)
    draw_para(bg, fnt)
    draw_damage_popups(bg, fnt)
    draw_crit_flash(bg)


def battle_command(bg, fnt, key):
    global btl_cmd
    ent = False
    if key[K_d]:
        btl_cmd = 4
        ent = True
    if key[K_a]:
        btl_cmd = 0
        ent = True
    if key[K_p]:
        btl_cmd = 1
        ent = True
    if key[K_b]:
        btl_cmd = 2
        ent = True
    if key[K_r]:
        btl_cmd = 3
        ent = True
    if key[K_f]:
        btl_cmd = 5
        ent = True
    if key[K_UP] and btl_cmd > 0:
        btl_cmd -= 1
    if key[K_DOWN] and btl_cmd < len(COMMAND) - 1:
        btl_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(len(COMMAND)):
        c = WHITE
        if btl_cmd == i: c=BLINK[tmr%6]
        draw_text(bg, COMMAND[i], 20, 200+i*60, fnt, c)
        if i == 3 and btl_cmd == 3:
            draw_text(bg, f"(~{flee_chance_pct()}% success)", 170, 200+i*60, fnt, (200, 190, 120))
    return ent

message = [("", WHITE)]*10
def init_message():
    for i in range(10):
        message[i] = ("", WHITE)
    damage_popups.clear()

def set_message(msg, col=WHITE):
    for i in range(10):
        if message[i][0] == "":
            message[i] = (msg, col)
            return
    for i in range(9):
        message[i] = message[i+1]
    message[9] = (msg, col)
    
def get_save_data():
    return{
        "floor": floor,
        "pl_x": pl_x,
        "pl_y": pl_y,
        "pl_d": pl_d,
        "pl_a": pl_a,
        "pl_lifemax": pl_lifemax,
        "pl_life": pl_life,
        "pl_str": pl_str,
        "pl_lv": pl_lv,
        "pl_exp": pl_exp,
        "pl_exp_mult": pl_exp_mult,
        "food": food,
        "potion": potion,
        "blazegem": blazegem,
        "pl_def_base": pl_def_base,
        "pl_def_buff": pl_def_buff,
        "def_pill": def_pill,
        "dungeon": dungeon,
        "explored": explored,
        "difficulty": difficulty,
        "boss_floors_cleared": list(boss_floors_cleared),
        "curse_active": curse_active,
        "skill_points": skill_points,
        "skill_levels": skill_levels,
        "pet_type": pet_type,
        "floor_modifier": floor_modifier,
        "color_patches": color_patches,
        "wall_tint": wall_tint,
        "wall_variant": wall_variant,
        "floor_variant": floor_variant,
        "prev_patch_colors": _prev_patch_colors,
        "selected_character": selected_character
    }
    
def save_game(filename="savefile.json"):
    global info_message, info_timer
    try:
        with open(filename, "w") as f:
            json.dump(get_save_data(), f)
    except Exception as e:
        _log_io_error(f"save_game({filename})", e)
        info_message = "Failed to save game."
        info_timer = 60
        return
    info_message = "Game saved."
    info_timer = 60
    _slot_floor_cache.clear()
    
def load_game(filename="savefile.json"):
    global floor, pl_x, pl_y, pl_d, pl_a, pl_lifemax, pl_life, pl_str, pl_lv, pl_exp, pl_exp_mult
    global food, potion, blazegem, pl_def_base, pl_def_buff, def_pill, dungeon, explored
    global info_message, info_timer, DUNGEON_W, DUNGEON_H, MAZE_W, MAZE_H, difficulty
    global boss_floors_cleared, curse_active, in_boss_battle
    global skill_points, skill_levels
    global pet_type, pet_def_bonus, pet_item_bonus
    global floor_modifier
    global color_patches
    global wall_tint
    global wall_variant, floor_variant
    global _prev_patch_colors
    global selected_character
    global _exploration_total, _exploration_seen, _reveal_radius_last, _minimap_cache_surface
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        difficulty = data.get("difficulty", "Normal")
        if difficulty not in DIFFICULTY_PARAMS:
            difficulty = "Normal"
        floor = data["floor"]
        pl_x = data["pl_x"]
        pl_y = data["pl_y"]
        pl_d = data["pl_d"]
        pl_a = data["pl_a"]
        pl_lifemax = data["pl_lifemax"]
        pl_life = data["pl_life"]
        pl_str = data["pl_str"]
        pl_lv = data["pl_lv"]
        pl_exp = data.get("pl_exp", exp_threshold(pl_lv))
        pl_exp_mult = data.get("pl_exp_mult", 1.0)
        food = data["food"]
        potion = data["potion"]
        blazegem = data["blazegem"]
        pl_def_base = data["pl_def_base"]
        pl_def_buff = data["pl_def_buff"]
        def_pill = data["def_pill"]
        dungeon = data["dungeon"]
        # セーブデータの盤面サイズに合わせてマップサイズも復元する
        DUNGEON_H = len(dungeon)
        DUNGEON_W = len(dungeon[0]) if DUNGEON_H > 0 else DUNGEON_W
        MAZE_H = DUNGEON_H // 3
        MAZE_W = DUNGEON_W // 3
        # 旧セーブデータ(探索情報なし)は全域を探索済み扱いにする
        explored = data.get("explored", [[True]*DUNGEON_W for _ in range(DUNGEON_H)])
        boss_floors_cleared = set(data.get("boss_floors_cleared", []))
        curse_active = data.get("curse_active", False)
        skill_points = data.get("skill_points", 0)
        skill_levels = data.get("skill_levels", {sk["id"]: 0 for sk in SKILLS})
        for sk in SKILLS:
            skill_levels.setdefault(sk["id"], 0)
        recompute_skill_percent_effects()
        pet_type = data.get("pet_type", None)
        if pet_type is not None and pet_type not in PET_TYPES:
            pet_type = None
        pet_def_bonus = 3 if pet_type == "sprite" else 0
        pet_item_bonus = 5 if pet_type == "cat" else 0
        floor_modifier = data.get("floor_modifier", None)
        if floor_modifier is not None and floor_modifier not in FLOOR_MODIFIERS:
            floor_modifier = None
        color_patches = data.get("color_patches", [])
        wt = data.get("wall_tint", None)
        wall_tint = tuple(wt) if wt is not None else None
        wall_variant = data.get("wall_variant", 0)
        floor_variant = data.get("floor_variant", 0)
        _prev_patch_colors = [tuple(c) for c in data.get("prev_patch_colors", [])]
        sc = data.get("selected_character", "warrior")
        selected_character = sc if sc in CHARACTER_TYPES else "warrior"
        in_boss_battle = False
        # ロードでdungeon/exploredを丸ごと差し替えたので、exploration_percent()用の
        # 集計値もセーブデータの内容に合わせて出し直す
        _exploration_total = sum(1 for row in dungeon for v in row if v not in (9, 25))
        _exploration_seen = sum(
            1 for y in range(DUNGEON_H) for x in range(DUNGEON_W)
            if explored[y][x] and dungeon[y][x] not in (9, 25)
        )
        _reveal_radius_last = None
        _minimap_cache_surface = None
        info_message = "Game loaded."
        info_timer = 45
    except Exception as e:
        _log_io_error("load_game", e)
        info_message = "Failed to load game."
        info_timer = 45

def autosave():
    """フロア移動時などに自動でオートセーブ枠へ保存する。ディスク書き込みに
    失敗しても(ディスク満杯・権限エラー等)ゲーム進行中の他の処理を巻き込んで
    クラッシュさせないよう、ここで例外を吸収してユーザーに知らせるだけにする。"""
    global info_message, info_timer, _autosave_floor_cache
    try:
        with open("autosave.json", "w") as f:
            json.dump(get_save_data(), f)
    except Exception as e:
        _log_io_error("autosave()", e)
        info_message = "Auto save failed."
        info_timer = 40
        return
    info_message = "Auto saved."
    info_timer = 40
    _autosave_floor_cache = _UNSET

# get_autosave_floor/get_slot_floor はセーブ/ロード/継続メニューが開いている間、
# 毎フレーム(idx==0/30/31/44の描画やイベント判定)呼ばれる。ファイルの中身は
# save_game()/autosave()が書き込んだ時しか変わらないので、結果をキャッシュして
# 保存直後だけ無効化する(ディスクからの毎フレームJSON読み込みを避ける)。
_UNSET = object()
_autosave_floor_cache = _UNSET
_slot_floor_cache = {}

def get_autosave_floor():
    global _autosave_floor_cache
    if _autosave_floor_cache is _UNSET:
        try:
            with open("autosave.json", "r") as f:
                data = json.load(f)
            _autosave_floor_cache = data.get("floor")
        except Exception:
            _autosave_floor_cache = None
    return _autosave_floor_cache

SAVE_SLOTS = 3

def slot_filename(slot):
    return f"savefile{slot}.json"

def get_slot_floor(slot):
    """指定スロットのセーブデータのフロア数を返す。存在しない/壊れている場合はNone"""
    if slot not in _slot_floor_cache:
        try:
            with open(slot_filename(slot), "r") as f:
                data = json.load(f)
            _slot_floor_cache[slot] = data.get("floor")
        except Exception:
            _slot_floor_cache[slot] = None
    return _slot_floor_cache[slot]

def main():
    global speed, idx, tmr, floor, fl_max, welcome
    global pl_x, pl_y, pl_a, pl_lifemax, pl_life, pl_str, food, potion, blazegem, pl_lv, pl_exp
    global pl_exp_mult, pl_charge, pl_poison
    global pl_def_base, pl_def_buff, def_pill
    global emy_life, emy_step, emy_blink, dmg_eff, typ, emy_lv
    global emy_str
    global boss_phase2
    global moving, move_dx, move_dy, move_progress, MOVE_SPEED, base_move_speed
    global hold_dir, hold_timer, hold_delay, hold_interval
    global queued_dir
    global ambush_battles_remaining
    global mimic_battle_active
    global ally_buff_active
    global in_rift_battle
    global doppelganger_battle_active
    global chimera_battle_active
    global shrine_result_name
    global info_message, info_timer
    global difficulty, food_acc
    global boss_floors_cleared, in_boss_battle, battle_took_damage, curse_active
    global in_echo_battle, echo_target_floor
    global boss_loot_rolled
    global stage_intro_timer, stage_intro_num
    global in_hidden_stage
    global combo_count
    global combo_record_shown_this_battle
    global crit_flash_timer, crit_flash_color, last_atk_special
    global screen_shake_timer, screen_shake_mag
    global pet_type, pet_def_bonus, pet_item_bonus
    global daily_mode
    global daily_start_requested
    global hero_start_requested
    global achievements_scroll
    global stats_scroll
    global selected_character
    global pending_bonus_room
    global playtime_ms_accum
    global skill_points, skill_levels, skill_food_mult, skill_poison_mult, skill_exp_mult, skill_item_bonus
    global skill_cursor_col, skill_cursor_row, skill_cursor_capstone
    global bounty_active
    global totem_buff_active, totem_str_bonus, totem_def_bonus
    global bestiary_detail_kind, bestiary_detail_index, bestiary_detail_img, bestiary_detail_seen
    global bgm_volume, se_volume, settings_cursor, muted, screen_shake_enabled, screen_flash_enabled
    global achievement_sound_pending
    global rare_treasure_sound_pending
    dmg = 0
    lif_p = 0
    str_p = 0
    def_inc = 0
    exp_gain = 0
    
    pygame.init()
    pygame.display.set_caption("Dungeon")
    screen = pygame.display.set_mode((880, 720))
    _convert_loaded_images()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    fontS = pygame.font.Font(None, 30)
    fontXS = pygame.font.Font(None, 21)
    
    se = [pygame.mixer.Sound("sound/ohd_se_attack.ogg"),
          pygame.mixer.Sound("sound/ohd_se_blaze.ogg"),
          pygame.mixer.Sound("sound/ohd_se_potion.ogg"),
          pygame.mixer.Sound("sound/ohd_jin_gameover.ogg"),
          pygame.mixer.Sound("sound/ohd_jin_levup.ogg"),
          pygame.mixer.Sound("sound/ohd_jin_win.ogg")]

    def apply_bgm_volume():
        pygame.mixer.music.set_volume(0.0 if muted else bgm_volume)

    def apply_se_volume():
        vol = 0.0 if muted else se_volume
        for s in se:
            s.set_volume(vol)

    load_settings()
    apply_bgm_volume()
    apply_se_volume()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                flush_playtime()
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # タイトル画面のESCはそのまま終了。ダンジョン探索中は誤操作で
                # 直前のオートセーブ以降の進行を失わないよう、確認画面(idx=55)を挟む
                if event.key == K_ESCAPE and idx == 0:
                    flush_playtime()
                    pygame.quit()
                    sys.exit()
                if event.key == K_ESCAPE and idx == 1:
                    idx = 55
                    tmr = 0
                if idx == 55:
                    if event.key == K_y:
                        flush_playtime()
                        pygame.quit()
                        sys.exit()
                    elif event.key in (K_n, K_ESCAPE):
                        idx = 1
                        tmr = 0
                # Mキーで全音声(BGM/SE)をどの画面からでも即座にミュート/解除できる
                # ようにする(音量設定画面を開かなくても来客対応等ですぐ無音化したい)
                if event.key == K_m:
                    muted = not muted
                    apply_bgm_volume()
                    apply_se_volume()
                    save_settings()
                # ゲーム進行中(ダンジョン探索中)にQキーでセーブメニューを開く
                if event.key == K_q and idx == 1:
                    idx = 30
                    tmr = 0
                # ゲーム進行中(ダンジョン探索中)にKキーでスキル画面を開く
                if event.key == K_k and idx == 1:
                    idx = 42
                    tmr = 0
                # ダンジョン探索中にIキーでポーションを使用する
                if event.key == K_i and idx == 1 and potion > 0:
                    potion -= 1
                    pl_life = pl_lifemax
                    se[2].play()
                    info_message = "Potion used! Fully healed."
                    info_timer = 45
                    record_stat("potions_used")
                    if load_stats().get("potions_used", 0) >= 20:
                        unlock_achievement("alchemist")
                # スキル画面内でのカーソル移動・購入操作(5枝x3段+奥義1つ、
                # 16スキルにもなるため数字キーではなく矢印キーのカーソル選択にする)
                if idx == 42:
                    if event.key in (K_LEFT, K_RIGHT) and not skill_cursor_capstone:
                        delta = -1 if event.key == K_LEFT else 1
                        skill_cursor_col = (skill_cursor_col + delta) % len(SKILL_BRANCH_ORDER)
                    elif event.key == K_UP:
                        if skill_cursor_capstone:
                            skill_cursor_capstone = False
                            skill_cursor_row = 2
                        else:
                            skill_cursor_row = max(0, skill_cursor_row - 1)
                    elif event.key == K_DOWN:
                        if not skill_cursor_capstone:
                            if skill_cursor_row >= 2:
                                skill_cursor_capstone = True
                            else:
                                skill_cursor_row += 1
                    elif event.key in (K_RETURN, K_SPACE):
                        if skill_cursor_capstone:
                            sk = SKILLS_BY_ID["grandmaster"]
                        else:
                            branch = SKILL_BRANCH_ORDER[skill_cursor_col]
                            sk = next((s for s in SKILLS if s["branch"] == branch and s["tier"] == skill_cursor_row + 1), None)
                        if sk is not None:
                            cur_lv = skill_levels.get(sk["id"], 0)
                            if not skill_prereq_met(sk):
                                req_names = ", ".join(SKILLS_BY_ID[r]["name"] for r in skill_requirement_ids(sk))
                                info_message = f"Requires {req_names} first!"
                                info_timer = 40
                            elif skill_points >= sk["cost"] and cur_lv < sk["max_level"]:
                                skill_points -= sk["cost"]
                                skill_levels[sk["id"]] = cur_lv + 1
                                apply_skill_effect(sk["id"])
                                info_message = f"{sk['name']} Lv{cur_lv+1}!"
                            info_timer = 40
                    elif event.key == K_ESCAPE:
                        idx = 1
                        tmr = 0
                # タイトル画面でTキーにより難易度を切り替える
                if event.key == K_t and idx == 0:
                    toggle_difficulty()
                # タイトル画面でNキーによりキャラクター選択画面を開く
                if event.key == K_n and idx == 0:
                    idx = 49
                    tmr = 0
                if idx == 49:
                    char_key_map = {K_1: 0, K_2: 1, K_3: 2, K_4: 3}
                    if event.key in char_key_map and char_key_map[event.key] < len(CHARACTER_ORDER):
                        selected_character = CHARACTER_ORDER[char_key_map[event.key]]
                    elif event.key in (K_RETURN, K_SPACE):
                        # 選んだヒーローでそのままゲームを開始する(タイトルに戻って
                        # 改めてSPACEを押す、という分かりにくい手順を省く)
                        hero_start_requested = True
                        idx = 0
                        tmr = 0
                    elif event.key == K_ESCAPE:
                        idx = 0
                        tmr = 0
                # タイトル画面でGキーによりゲームデータメニュー(ロード/コンティニュー)を開く
                if event.key == K_g and idx == 0:
                    idx = 44
                    tmr = 0
                if event.key == K_ESCAPE and idx == 44:
                    idx = 0
                    tmr = 0
                # タイトル画面でRキーにより記録メニュー(実績/統計)を開く
                if event.key == K_r and idx == 0:
                    idx = 45
                    tmr = 0
                if event.key == K_ESCAPE and idx == 45:
                    idx = 0
                    tmr = 0
                # タイトル画面でF1キーによりヘルプ(操作方法一覧)画面を開く
                if event.key == K_F1 and idx == 0:
                    idx = 57
                    tmr = 0
                if event.key == K_ESCAPE and idx == 57:
                    idx = 0
                    tmr = 0
                # ゲームデータメニュー内でLキーによりロードメニューを開く
                if event.key == K_l and idx == 44:
                    idx = 31
                    tmr = 0
                # 記録メニュー内でVキーにより実績一覧を開く
                if event.key == K_v and idx == 45:
                    idx = 33
                    tmr = 0
                    achievements_scroll = 0
                if event.key == K_ESCAPE and idx == 33:
                    idx = 45
                    tmr = 0
                # 実績一覧が画面に収まらないため、Up/Downでスクロールする
                if idx == 33 and event.key in (K_UP, K_DOWN):
                    max_scroll = max(0, len(ACHIEVEMENT_DEFS) - ACHIEVEMENTS_VISIBLE_ROWS)
                    step = -1 if event.key == K_UP else 1
                    achievements_scroll = min(max_scroll, max(0, achievements_scroll + step))
                # 記録メニュー内でXキーによりプレイ統計を開く
                if event.key == K_x and idx == 45:
                    idx = 43
                    tmr = 0
                    stats_scroll = 0
                if event.key == K_ESCAPE and idx == 43:
                    idx = 45
                    tmr = 0
                # プレイ統計一覧が画面に収まらないため、Up/Downでスクロールする
                if idx == 43 and event.key in (K_UP, K_DOWN):
                    max_scroll = max(0, len(STATS_DEFS) + 1 - STATS_VISIBLE_ROWS)
                    step = -1 if event.key == K_UP else 1
                    stats_scroll = min(max_scroll, max(0, stats_scroll + step))
                # 記録メニュー内でBキーにより図鑑(Bestiary)を開く
                if event.key == K_b and idx == 45:
                    idx = 46
                    tmr = 0
                if event.key == K_ESCAPE and idx == 46:
                    idx = 45
                    tmr = 0
                # 記録メニュー内でEキーによりエコーバトル選択画面を開く
                if event.key == K_e and idx == 45:
                    idx = 52
                    tmr = 0
                if idx == 52:
                    echo_key_map = {K_1: 0, K_2: 1, K_3: 2, K_4: 3, K_5: 4, K_6: 5, K_7: 6, K_8: 7, K_9: 8}
                    if event.key in echo_key_map and echo_key_map[event.key] < len(ECHO_ELIGIBLE_FLOORS):
                        target_fl = ECHO_ELIGIBLE_FLOORS[echo_key_map[event.key]]
                        bi = boss_bestiary_index_for_floor(target_fl)
                        bdata = load_bestiary()
                        if bi is not None and bdata["bosses"][bi]:
                            start_echo_battle(target_fl)
                    elif event.key == K_ESCAPE:
                        idx = 45
                        tmr = 0
                # 記録メニュー内でDキーによりデイリーランキング画面を開く
                if event.key == K_d and idx == 45:
                    idx = 53
                    tmr = 0
                if event.key == K_ESCAPE and idx == 53:
                    idx = 45
                    tmr = 0
                # 図鑑の詳細表示(モンスター/ボスの画像)内でEscで図鑑一覧に戻る
                if event.key == K_ESCAPE and idx == 47:
                    idx = 46
                    tmr = 0
                # ゲームデータメニュー内でCキーによりオートセーブから再開
                if event.key == K_c and idx == 44 and get_autosave_floor() is not None:
                    load_game("autosave.json")
                    idx = 1
                    tmr = 0
                    welcome = 0
                    pygame.mixer.music.load(bgm_field_for_floor(floor))
                    pygame.mixer.music.play(-1)
                # タイトル画面でHキーにより隠しステージ(裏ボス)へ挑戦する
                # (全3ステージクリア=game_clear実績が解除済みの場合のみ)
                if event.key == K_h and idx == 0 and load_achievements().get("game_clear", False):
                    start_hidden_stage_challenge()
                # タイトル画面でYキーによりデイリーチャレンジ(今日の固定シード)を開始する
                if event.key == K_y and idx == 0:
                    daily_start_requested = True
                # ゲームデータメニュー内でOキーにより音量設定画面を開く
                if event.key == K_o and idx == 44:
                    idx = 56
                    tmr = 0
                    settings_cursor = 0
                if idx == 56:
                    if event.key == K_ESCAPE:
                        idx = 44
                        tmr = 0
                    elif event.key in (K_UP, K_DOWN):
                        delta_row = 1 if event.key == K_DOWN else -1
                        settings_cursor = (settings_cursor + delta_row) % 5
                    elif event.key in (K_LEFT, K_RIGHT, K_RETURN, K_SPACE) and settings_cursor == 2:
                        muted = not muted
                        apply_bgm_volume()
                        apply_se_volume()
                        save_settings()
                    elif event.key in (K_LEFT, K_RIGHT, K_RETURN, K_SPACE) and settings_cursor == 3:
                        screen_shake_enabled = not screen_shake_enabled
                        save_settings()
                    elif event.key in (K_LEFT, K_RIGHT, K_RETURN, K_SPACE) and settings_cursor == 4:
                        screen_flash_enabled = not screen_flash_enabled
                        save_settings()
                    elif event.key in (K_LEFT, K_RIGHT):
                        delta = VOLUME_STEP if event.key == K_RIGHT else -VOLUME_STEP
                        if settings_cursor == 0:
                            bgm_volume = round(max(0.0, min(1.0, bgm_volume + delta)), 2)
                            apply_bgm_volume()
                        else:
                            se_volume = round(max(0.0, min(1.0, se_volume + delta)), 2)
                            apply_se_volume()
                        save_settings()
                # 拠点(サンクチュア)でのアイテム交換
                if idx == 28:
                    if event.key == K_p and potion >= 2:
                        potion -= 2
                        def_pill += 1
                        info_message = "Exchanged for Defense Pill!"
                        info_timer = 40
                    elif event.key == K_b and blazegem >= 1:
                        blazegem -= 1
                        food += 100
                        info_message = "Exchanged for Food!"
                        info_timer = 40
                    elif event.key == K_f and food >= 60:
                        food -= 60
                        potion += 1
                        info_message = "Exchanged for Potion!"
                        info_timer = 40
                    elif event.key == K_w and potion >= 1:
                        potion -= 1
                        if random.randint(0, 1) == 0:
                            potion += 2
                            info_message = "Gamble win! Potion doubled!"
                        else:
                            info_message = "Gamble lost... the Potion is gone."
                        info_timer = 45
                # 旅の商人(idx==48)での取引。Bazaar Floorではコストが割引される。
                if idx == 48:
                    mc_potion = merchant_trade_cost(80)
                    mc_blaze = merchant_trade_cost(2)
                    mc_defpill = merchant_trade_cost(2)
                    mc_pet = merchant_trade_cost(150)
                    if event.key == K_1 and food >= mc_potion:
                        food -= mc_potion
                        potion += 1
                        info_message = "Bought a Potion!"
                        info_timer = 40
                        record_stat("merchant_trades")
                    elif event.key == K_2 and potion >= mc_blaze:
                        potion -= mc_blaze
                        blazegem += 1
                        info_message = "Traded for a Blaze gem!"
                        info_timer = 40
                        record_stat("merchant_trades")
                    elif event.key == K_3 and blazegem >= mc_defpill:
                        blazegem -= mc_defpill
                        def_pill += 1
                        info_message = "Traded for a Defense Pill!"
                        info_timer = 40
                        record_stat("merchant_trades")
                    elif event.key == K_4 and pet_type is None and food >= mc_pet:
                        food -= mc_pet
                        hatch_random_pet()
                        info_message = f"{PET_TYPES[pet_type]['name']} hatched!"
                        info_timer = 40
                        record_stat("merchant_trades")
                    elif event.key == K_ESCAPE:
                        idx = 1
                        tmr = 0
                    if load_stats().get("merchant_trades", 0) >= 5:
                        unlock_achievement("merchant_regular")
                    # Merchant Regular(5回)の上位版。Elite Hunter->Elite Slayerや
                    # Combo Finisher->Chain Reactionと同じく、繰り返し取引し続ける
                    # ことを評価する累積目標が無かったため、既存の記録
                    # (merchant_trades)をそのまま活かして追加した。
                    if load_stats().get("merchant_trades", 0) >= 50:
                        unlock_achievement("merchant_baron")
                # 犠牲の祭壇(idx==61)での選択
                if idx == 61:
                    if event.key == K_y:
                        if pl_life > ALTAR_HP_COST:
                            pl_life -= ALTAR_HP_COST
                            roll_altar_outcome()
                            idx = 62
                            tmr = 0
                        else:
                            info_message = "Not enough HP to make an offering."
                            info_timer = 40
                            idx = 1
                            tmr = 0
                    elif event.key in (K_n, K_ESCAPE):
                        idx = 1
                        tmr = 0
                # さまよう精霊(idx==64)での3択選択
                if idx == 64:
                    choice_map = {K_1: 0, K_2: 1, K_3: 2}
                    if event.key in choice_map and choice_map[event.key] < len(spirit_choice_options):
                        chosen = spirit_choice_options[choice_map[event.key]]
                        apply_spirit_blessing(chosen)
                        unlock_achievement("spirit_blessed")
                        info_message = f"Blessed with {chosen[0]}!"
                        info_timer = 45
                        idx = 1
                        tmr = 0
                # 賭博場(idx==65)での掛け金選択
                if idx == 65:
                    tier_map = {K_1: 0, K_2: 1, K_3: 2}
                    if event.key in tier_map:
                        t = GAMBLE_TIERS[tier_map[event.key]]
                        if blazegem >= t["cost"]:
                            resolve_gamble(tier_map[event.key])
                            idx = 66
                            tmr = 0
                        else:
                            info_message = "Not enough Blaze gems for that bet."
                            info_timer = 40
                    elif event.key in (K_4, K_ESCAPE):
                        idx = 1
                        tmr = 0
                # セーブメニュー内での操作
                if idx == 30:
                    if event.key in (K_1, K_2, K_3):
                        slot = {K_1: 1, K_2: 2, K_3: 3}[event.key]
                        save_game(slot_filename(slot))
                        idx = 1
                        tmr = 0
                    elif event.key == K_ESCAPE:
                        idx = 1
                        tmr = 0
                # ロードメニュー内での操作
                if idx == 31:
                    if event.key in (K_1, K_2, K_3):
                        slot = {K_1: 1, K_2: 2, K_3: 3}[event.key]
                        if get_slot_floor(slot) is not None:
                            load_game(slot_filename(slot))
                            idx = 1
                            tmr = 0
                            welcome = 0
                            pygame.mixer.music.load(bgm_field_for_floor(floor))
                            pygame.mixer.music.play(-1)
                    elif event.key == K_ESCAPE:
                        idx = 44
                        tmr = 0
                if event.key == K_s:
                    speed = (speed%7) + 1
                    
                    old_move_speed = MOVE_SPEED
                    MOVE_SPEED = base_move_speed * (1 + (speed - 1) * 0.15)
                    try:
                        if old_move_speed > 0:
                            move_progress = move_progress * (old_move_speed/ MOVE_SPEED)
                    except NameError:
                        pass
                #プレーヤー移動
                if idx == 1:
                    dir_key_map = {K_UP: "up", K_DOWN: "down", K_LEFT: "left", K_RIGHT: "right"}
                    if event.key in dir_key_map:
                        pressed_dir = dir_key_map[event.key]
                        if not moving:
                            if pressed_dir == "up" and dungeon[pl_y-1][pl_x] not in (9, 25):
                                move_dx, move_dy = 0, -1
                                moving = True
                                move_progress = 0.0
                                pl_d = 0
                                pl_a = pl_d * 2
                            elif pressed_dir == "down" and dungeon[pl_y+1][pl_x] not in (9, 25):
                                move_dx, move_dy = 0, 1
                                moving = True
                                move_progress = 0.0
                                pl_d = 1
                                pl_a = pl_d * 2
                            elif pressed_dir == "left" and dungeon[pl_y][pl_x-1] not in (9, 25):
                                move_dx, move_dy = -1, 0
                                moving = True
                                move_progress = 0.0
                                pl_d = 2
                                pl_a = pl_d * 2
                            elif pressed_dir == "right" and dungeon[pl_y][pl_x+1] not in (9, 25):
                                move_dx, move_dy = 1, 0
                                moving = True
                                move_progress = 0.0
                                pl_d = 3
                                pl_a = pl_d * 2
                        else:
                            # 移動アニメーション中の入力は捨てず、先読み(queued_dir)として
                            # 覚えておき、アニメーション完了時に間を空けず即座につなげる
                            queued_dir = pressed_dir
                        hold_dir = pressed_dir
                        hold_timer = hold_delay

            if event.type == KEYUP:
                if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    hold_dir = None
                    hold_timer = 0.0

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # タイトル画面の階層メニュー(トップ/ゲームデータ/記録)はクリックでも操作できる
                mx, my = event.pos
                action = hit_test_menu(mx, my)
                if action == "difficulty":
                    toggle_difficulty()
                elif action == "open_game_data":
                    idx = 44
                    tmr = 0
                elif action == "open_records":
                    idx = 45
                    tmr = 0
                elif action == "daily":
                    daily_start_requested = True
                elif action == "hidden" and load_achievements().get("game_clear", False):
                    start_hidden_stage_challenge()
                elif action == "back_to_title":
                    idx = 0
                    tmr = 0
                elif action == "back_to_game_data":
                    idx = 44
                    tmr = 0
                elif action == "back_to_records":
                    idx = 45
                    tmr = 0
                elif action == "open_load":
                    idx = 31
                    tmr = 0
                elif action is not None and action.startswith("load_slot_"):
                    slot = int(action.rsplit("_", 1)[1])
                    if get_slot_floor(slot) is not None:
                        load_game(slot_filename(slot))
                        idx = 1
                        tmr = 0
                        welcome = 0
                        pygame.mixer.music.load(bgm_field_for_floor(floor))
                        pygame.mixer.music.play(-1)
                elif action == "continue" and get_autosave_floor() is not None:
                    load_game("autosave.json")
                    idx = 1
                    tmr = 0
                    welcome = 0
                    pygame.mixer.music.load(bgm_field_for_floor(floor))
                    pygame.mixer.music.play(-1)
                elif action == "open_achievements":
                    idx = 33
                    tmr = 0
                elif action == "open_stats":
                    idx = 43
                    tmr = 0
                elif action == "open_bestiary":
                    idx = 46
                    tmr = 0
                elif action == "open_echo":
                    idx = 52
                    tmr = 0
                elif action == "open_daily_ranking":
                    idx = 53
                    tmr = 0
                elif action and action.startswith("view_enemy_"):
                    vi = int(action.rsplit("_", 1)[1])
                    if 0 <= vi < len(EMY_NAME):
                        bdata = load_bestiary()
                        bestiary_detail_kind = "enemy"
                        bestiary_detail_index = vi
                        bestiary_detail_seen = bdata["enemies"][vi]
                        # 8bitパレット画像などがあるとsmoothscaleが例外を出すため、
                        # 表示前に必ず32bit(アルファ付き)Surfaceへ変換しておく
                        bestiary_detail_img = pygame.image.load("image/" + enemy_image_file(vi)).convert_alpha() if bestiary_detail_seen else None
                        idx = 47
                        tmr = 0
                elif action and action.startswith("view_boss_"):
                    vi = int(action.rsplit("_", 1)[1])
                    if 0 <= vi < len(BOSS_BESTIARY):
                        bdata = load_bestiary()
                        bestiary_detail_kind = "boss"
                        bestiary_detail_index = vi
                        bestiary_detail_seen = bdata["bosses"][vi]
                        _, _, bimg_file = BOSS_BESTIARY[vi]
                        bestiary_detail_img = pygame.image.load("image/" + bimg_file).convert_alpha() if bestiary_detail_seen else None
                        idx = 47
                        tmr = 0
                elif action == "back_to_bestiary":
                    idx = 46
                    tmr = 0
                elif action == "open_hero_select":
                    idx = 49
                    tmr = 0
                elif action == "open_settings":
                    idx = 56
                    tmr = 0
                    settings_cursor = 0
                elif action == "open_help":
                    idx = 57
                    tmr = 0
                elif action == "bgm_vol_down":
                    bgm_volume = round(max(0.0, bgm_volume - VOLUME_STEP), 2)
                    apply_bgm_volume()
                    save_settings()
                elif action == "bgm_vol_up":
                    bgm_volume = round(min(1.0, bgm_volume + VOLUME_STEP), 2)
                    apply_bgm_volume()
                    save_settings()
                elif action == "se_vol_down":
                    se_volume = round(max(0.0, se_volume - VOLUME_STEP), 2)
                    apply_se_volume()
                    save_settings()
                elif action == "se_vol_up":
                    se_volume = round(min(1.0, se_volume + VOLUME_STEP), 2)
                    apply_se_volume()
                    save_settings()
                elif action == "mute_toggle":
                    muted = not muted
                    apply_bgm_volume()
                    apply_se_volume()
                    save_settings()
                elif action == "shake_toggle":
                    screen_shake_enabled = not screen_shake_enabled
                    save_settings()
                elif action == "flash_toggle":
                    screen_flash_enabled = not screen_flash_enabled
                    save_settings()

        tmr = tmr +1
        if info_timer > 0:
            info_timer -= 1
            
        if idx == 1 and moving:
            move_progress += MOVE_SPEED * modifier_speed_mult() * modifier_rocky_speed_mult() * (1.0 + skill_move_speed_bonus)
            
            pl_a = pl_d * 2 + (int(move_progress * 4) % 2)
            if move_progress >=  1.0 :
                moving = False
                move_progress = 0.0
                pl_x += move_dx
                pl_y += move_dy
                steps_taken_accum += 1
                dp = diff_params()
                food_acc += dp["food_consume_mult"] * skill_food_mult * modifier_food_mult() * char_params()["food_mult"]
                consume = int(food_acc)
                food_acc -= consume
                if food > 0:
                    food = max(0, food - max(consume, 0))
                    if pl_life < pl_lifemax:
                        pl_life = min(pl_lifemax, pl_life + int(dp["heal_per_step"] * modifier_heal_mult()))
                else:
                    pl_life -= dp["starve_dmg"]
                    if pl_life <= 0:
                        pl_life = 0
                        pygame.mixer.music.stop()
                        idx = 9
                        tmr = 0
                    else:
                        unlock_achievement("starve_survive")
                
                if pl_poison > 0 and idx == 1:
                    pdmg = max(1, int(pl_lifemax // 20 * skill_poison_mult))
                    pl_life -= pdmg
                    pl_poison = max(0, pl_poison - diff_params()["poison_decay_per_step"])
                    info_message = f"Poison {pdmg}dmg!"
                    info_timer = 30
                    if pl_life <= 0:
                        pl_life = 0
                        pygame.mixer.music.stop()
                        idx = 9
                        tmr = 0
                
                move_player([0]*10)
                update_golden_sprite()
                update_collapse_timer()
                update_boulder_chase()

                # 氷の床(16)に乗った場合、そのまま同じ方向へ自動で滑り続ける
                # (次のマスが壁でなければ継続。階段や宝箱などの特別な地形に
                #  乗ってidxが変わった場合はそこでスライドを止める)
                if idx == 1 and dungeon[pl_y][pl_x] == 16:
                    ny, nx = pl_y + move_dy, pl_x + move_dx
                    if 0 <= nx < DUNGEON_W and 0 <= ny < DUNGEON_H and dungeon[ny][nx] not in (9, 25):
                        moving = True
                        move_progress = 0.0
        # 移動中に先読みされた方向(queued_dir)があれば、間を空けずただちに
        # 次の1マス移動へつなげる(サクサクした操作感のため)。moveが完了した
        # フレームに限らず毎フレームチェックすることで、入力のタイミングに
        # 関わらず取りこぼさないようにする。
        if idx == 1 and not moving and queued_dir is not None:
            qd = queued_dir
            queued_dir = None
            if qd == "up" and dungeon[pl_y-1][pl_x] not in (9, 25):
                move_dx, move_dy = 0, -1
                moving = True
                move_progress = 0.0
                pl_d = 0
                pl_a = pl_d * 2
            elif qd == "down" and dungeon[pl_y+1][pl_x] not in (9, 25):
                move_dx, move_dy = 0, 1
                moving = True
                move_progress = 0.0
                pl_d = 1
                pl_a = pl_d * 2
            elif qd == "left" and dungeon[pl_y][pl_x-1] not in (9, 25):
                move_dx, move_dy = -1, 0
                moving = True
                move_progress = 0.0
                pl_d = 2
                pl_a = pl_d * 2
            elif qd == "right" and dungeon[pl_y][pl_x+1] not in (9, 25):
                move_dx, move_dy = 1, 0
                moving = True
                move_progress = 0.0
                pl_d = 3
                pl_a = pl_d * 2
        key = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if idx == 1 and hold_dir is not None:
            # フレーム単位でデクリメント
            hold_timer -= 1
            if hold_timer <= 0:
                # moving していなければ自動で1マス移動を開始する
                if not moving:
                    if hold_dir == "up":
                        if dungeon[pl_y-1][pl_x] not in (9, 25):
                            move_dx, move_dy = 0, -1
                            moving = True
                            move_progress = 0.0
                            pl_d = 0
                            pl_a = pl_d * 2
                    elif hold_dir == "down":
                        if dungeon[pl_y+1][pl_x] not in (9, 25):
                            move_dx, move_dy = 0, 1
                            moving = True
                            move_progress = 0.0
                            pl_d = 1
                            pl_a = pl_d * 2
                    elif hold_dir == "left":
                        if dungeon[pl_y][pl_x-1] not in (9, 25):
                            move_dx, move_dy = -1, 0
                            moving = True
                            move_progress = 0.0
                            pl_d = 2
                            pl_a = pl_d * 2
                    elif hold_dir == "right":
                        if dungeon[pl_y][pl_x+1] not in (9, 25):
                            move_dx, move_dy = 1, 0
                            moving = True
                            move_progress = 0.0
                            pl_d = 3
                            pl_a = pl_d * 2
                # 初回は hold_delay、以降は hold_interval を使う
                hold_timer = hold_interval
        
        if idx == 0:
            title_menu_rects.clear()
            if tmr == 1:
                pygame.mixer.music.load("sound/ohd_bgm_title.ogg")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            # 操作方法が分からず迷うプレイヤー向けに、常時表示のヘルプボタンを
            # 右上の余白(絵柄がまだ被らない領域)に置く
            help_label = "[F1] Help"
            help_w = fontS.size(help_label)[0] + 30
            draw_button(screen, fontS, 880 - help_w - 16, 12, help_w, 26, help_label, "open_help",
                        base_color=(90, 150, 200), mouse_pos=mouse_pos)
            # 背景の絵柄と文字が被って読みにくいので、文字の後ろに半透明の帯を敷く
            panel = pygame.Surface((880, 370))
            panel.set_alpha(150)
            panel.fill(BLACK)
            screen.blit(panel, [0, 350])
            MENU_X = 215      # メニュー項目のラベルはすべてこのX座標で揃える(ボタン幅450を画面中央に揃えた値)
            ARROW_X = 635     # サブメニューへの「>」矢印はすべてこのX座標で揃える
            title_text = current_title()
            if title_text:
                draw_text(screen, f"You are known as {title_text}", 260, 365, fontS, (255, 215, 0))
            if fl_max >= 2:
                draw_text(screen, f"You reached floor {fl_max} (Stage {current_stage(fl_max)}/{STAGE_COUNT}).", 260, 400, font, CYAN)
            draw_button(screen, font, MENU_X, 435, ARROW_X - MENU_X + 30, 36,
                        "Press SPACE to start", None, base_color=(50, 190, 90),
                        mouse_pos=mouse_pos, align="center")
            pygame.draw.rect(screen, (90, 90, 90), [MENU_X, 481, 480, 2])
            ROW_H = 38        # 行の高さ(6項目に増えたため少し詰める)
            BTN_W = ARROW_X - MENU_X + 30
            y = 488
            # [T] 難易度(直接切り替え、サブメニューなし)
            label = f"[T] Difficulty: {difficulty}"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "difficulty",
                        base_color=(225, 150, 40), mouse_pos=mouse_pos)
            y += ROW_H
            # [N] キャラクター選択(サブメニューへ)
            label = f"[N] Hero: {CHARACTER_TYPES[selected_character]['name']}"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_hero_select",
                        base_color=(40, 165, 130), mouse_pos=mouse_pos)
            draw_text(screen, ">", MENU_X+BTN_W-28, y+4, font, WHITE)
            y += ROW_H
            # [G] ゲームデータ(ロード/コンティニューへのサブメニュー)
            label = "[G] Game Data"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_game_data",
                        base_color=(50, 110, 210), mouse_pos=mouse_pos)
            draw_text(screen, ">", MENU_X+BTN_W-28, y+4, font, WHITE)
            y += ROW_H
            # [R] 記録(実績/統計へのサブメニュー)
            label = "[R] Records"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_records",
                        base_color=(130, 80, 205), mouse_pos=mouse_pos)
            draw_text(screen, ">", MENU_X+BTN_W-28, y+4, font, WHITE)
            # 実績の解除数をタイトル画面から一目で確認できるように、Recordsボタンの
            # 右側に「X/Y」形式で進捗を表示する(従来はRecords画面を開くまで
            # わからなかった)。
            _ach_data = load_achievements()
            _ach_unlocked = sum(1 for _k, _ in ACHIEVEMENT_DEFS if _ach_data.get(_k, False))
            draw_text(screen, f"{_ach_unlocked}/{len(ACHIEVEMENT_DEFS)}", MENU_X+BTN_W+10, y+8, fontXS, (210, 190, 255))
            y += ROW_H
            # [Y] デイリーチャレンジ(直接開始)
            daily_rec = load_daily_record()
            daily_hint = "[Y] Daily Challenge"
            if daily_rec.get("cleared"):
                daily_hint += " (Cleared today!)"
            elif daily_rec.get("best_floor", 0) > 0:
                daily_hint += f" (Best today: floor {daily_rec['best_floor']})"
            draw_button(screen, fontS, MENU_X, y, fontS.size(daily_hint)[0] + 30, 26, daily_hint, "daily",
                        base_color=(60, 170, 90), mouse_pos=mouse_pos)
            y += ROW_H - 8
            # [H] 隠しステージ(全クリア後のみ、直接開始)
            if load_achievements().get("game_clear", False):
                label = "[H] Hidden Stage"
                draw_button(screen, fontS, MENU_X, y, fontS.size(label)[0] + 30, 26, label, "hidden",
                            base_color=(190, 50, 170), mouse_pos=mouse_pos)
            if key[K_SPACE] == 1 or daily_start_requested or hero_start_requested:
                is_daily = daily_start_requested
                daily_start_requested = False
                hero_start_requested = False
                if is_daily:
                    random.seed(daily_seed_for_today())
                    daily_mode = True
                else:
                    random.seed()
                    daily_mode = False
                dp = diff_params()
                cp = char_params()
                floor = 1
                make_dungeon()
                put_event()
                welcome = 15
                pl_lifemax = 300 + dp["pl_lifemax_bonus"] + cp["lifemax"]
                pl_life = pl_lifemax
                pl_str = 100 + dp["pl_str_bonus"] + cp["str"]
                pl_def_base = 0 + dp["pl_def_bonus"] + cp["def"]
                pl_def_buff = 0
                def_pill = 0
                food = 300
                food_acc = 0.0
                potion = 0
                blazegem = 0
                pl_lv = 1
                pl_exp = 0
                pl_exp_mult = 1.0
                boss_floors_cleared = set()
                curse_active = False
                ally_buff_active = False
                in_rift_battle = False
                bounty_active = False
                totem_buff_active = False
                in_boss_battle = False
                battle_took_damage = False
                in_hidden_stage = False
                pl_poison = 0
                pl_charge = False
                stage_intro_timer = 90
                stage_intro_num = 1
                skill_points = 0
                skill_levels = {sk["id"]: 0 for sk in SKILLS}
                skill_food_mult = 1.0
                skill_poison_mult = 1.0
                skill_exp_mult = 1.0
                skill_item_bonus = 0
                combo_count = 0
                pet_type = None
                pet_def_bonus = 0
                pet_item_bonus = 0
                idx = 1
                pygame.mixer.music.load(bgm_field_for_floor(floor))
                pygame.mixer.music.play(-1)

        elif idx == 44:
            # ゲームデータメニュー(タイトル画面に重ねて表示)
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 300])
            MENU_X = 230      # ボタン幅420を画面中央に揃えた値
            draw_text(screen, "Game Data", MENU_X, 320, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [MENU_X, 365, 480, 2])
            BTN_W = 420
            y = 383
            has_slot = any(get_slot_floor(i) is not None for i in range(1, SAVE_SLOTS+1))
            if has_slot:
                label = "[L] Load Game"
                draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_load",
                            base_color=(50, 110, 210), mouse_pos=mouse_pos)
            else:
                draw_button(screen, font, MENU_X, y, BTN_W, 34, "No saved slots yet",
                            mouse_pos=mouse_pos, enabled=False)
            y += 45
            auto_fl = get_autosave_floor()
            if auto_fl is not None:
                label = f"[C] Continue (floor {auto_fl})"
                draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "continue",
                            base_color=(60, 170, 90), mouse_pos=mouse_pos)
            else:
                draw_button(screen, font, MENU_X, y, BTN_W, 34, "No autosave yet",
                            mouse_pos=mouse_pos, enabled=False)
            y += 45
            label = "[O] Settings (BGM/SE volume)"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_settings",
                        base_color=(90, 90, 100), mouse_pos=mouse_pos)
            y += 60
            label = "[Esc] Back"
            draw_button(screen, fontS, MENU_X, y, fontS.size(label)[0] + 30, 28, label, "back_to_title",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 56:
            # 音量設定画面(ゲームデータメニューから開く)。BGM/SE音量を個別に
            # 0-100%で調整でき、変更は即座に反映されsettings.jsonへ保存される。
            # Mute Allは音量値はそのまま残して一時的に無音化するトグル(Mキーと連動)。
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 440))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 280])
            MENU_X = 230
            draw_text(screen, "Settings", MENU_X, 310, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [MENU_X, 355, 480, 2])
            BAR_X = MENU_X + 190
            BAR_W = 200
            rows = [
                ("BGM Volume", bgm_volume, 0, "bgm_vol_down", "bgm_vol_up"),
                ("SE Volume", se_volume, 1, "se_vol_down", "se_vol_up"),
            ]
            y = 385
            for label, vol, row_i, act_down, act_up in rows:
                selected = settings_cursor == row_i
                col = (255, 215, 0) if selected else WHITE
                cursor = "> " if selected else "  "
                draw_text(screen, cursor + label, MENU_X, y, fontS, col)
                draw_bar(screen, BAR_X, y + 32, BAR_W, 16, vol * 100, 100)
                draw_text(screen, f"{int(round(vol * 100))}%", BAR_X + BAR_W + 15, y + 27, fontS, WHITE)
                draw_button(screen, font, BAR_X - 46, y + 24, 34, 30, "-", act_down,
                            base_color=(90, 90, 90), mouse_pos=mouse_pos, align="center")
                draw_button(screen, font, BAR_X + BAR_W + 70, y + 24, 34, 30, "+", act_up,
                            base_color=(90, 90, 90), mouse_pos=mouse_pos, align="center")
                y += 70
            mute_selected = settings_cursor == 2
            mcol = (255, 215, 0) if mute_selected else WHITE
            mcursor = "> " if mute_selected else "  "
            draw_text(screen, mcursor + "Mute All", MENU_X, y, fontS, mcol)
            status_text = "ON" if muted else "OFF"
            status_col = (255, 120, 120) if muted else (150, 255, 150)
            draw_text(screen, status_text, BAR_X + 78, y + 2, fontS, status_col)
            toggle_label = "Toggle"
            draw_button(screen, fontS, BAR_X - 46, y - 2, fontS.size(toggle_label)[0] + 24, 30, toggle_label,
                        "mute_toggle", base_color=(90, 90, 90), mouse_pos=mouse_pos, align="center")
            y += 55
            shake_selected = settings_cursor == 3
            scol = (255, 215, 0) if shake_selected else WHITE
            scursor = "> " if shake_selected else "  "
            draw_text(screen, scursor + "Screen Shake", MENU_X, y, fontS, scol)
            shake_status_text = "ON" if screen_shake_enabled else "OFF"
            shake_status_col = (150, 255, 150) if screen_shake_enabled else (255, 120, 120)
            draw_text(screen, shake_status_text, BAR_X + 78, y + 2, fontS, shake_status_col)
            shake_toggle_label = "Toggle"
            draw_button(screen, fontS, BAR_X - 46, y - 2, fontS.size(shake_toggle_label)[0] + 24, 30, shake_toggle_label,
                        "shake_toggle", base_color=(90, 90, 90), mouse_pos=mouse_pos, align="center")
            y += 40
            flash_selected = settings_cursor == 4
            flcol = (255, 215, 0) if flash_selected else WHITE
            flcursor = "> " if flash_selected else "  "
            draw_text(screen, flcursor + "Screen Flash", MENU_X, y, fontS, flcol)
            flash_status_text = "ON" if screen_flash_enabled else "OFF"
            flash_status_col = (150, 255, 150) if screen_flash_enabled else (255, 120, 120)
            draw_text(screen, flash_status_text, BAR_X + 78, y + 2, fontS, flash_status_col)
            flash_toggle_label = "Toggle"
            draw_button(screen, fontS, BAR_X - 46, y - 2, fontS.size(flash_toggle_label)[0] + 24, 30, flash_toggle_label,
                        "flash_toggle", base_color=(90, 90, 90), mouse_pos=mouse_pos, align="center")
            y += 40
            draw_text(screen, "[Up/Down] Select  [Left/Right] Adjust  [M] Mute  [Esc] Back", MENU_X, y + 5, fontXS, CYAN)
            y += 25
            label = "[Esc] Back"
            draw_button(screen, fontS, MENU_X, y, fontS.size(label)[0] + 30, 28, label, "back_to_game_data",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 57:
            # ヘルプ(操作方法一覧)画面。初めて遊ぶ人がキー操作で迷わないよう、
            # タイトル/ダンジョン探索/バトルの3場面ごとにキー割り当てをまとめて表示する。
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 600))
            panel.set_alpha(190)
            panel.fill(BLACK)
            screen.blit(panel, [0, 90])
            MENU_X = 60
            draw_text(screen, "Help / Controls", MENU_X, 105, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [MENU_X, 145, 760, 2])
            y = 160
            sections = [
                ("Title Screen", (200, 200, 255), [
                    "Arrow Keys : Move cursor        [Space] : Start game",
                    "[T] Difficulty   [N] Hero select   [G] Game data",
                    "[R] Records (achievements/stats/bestiary/echo/ranking)",
                    "[Y] Daily challenge   [H] Hidden stage (after full clear)",
                    "[F1] This help screen   [Esc] Quit game",
                ]),
                ("Dungeon Exploration", (200, 255, 200), [
                    "Arrow Keys : Move   [Q] Save menu   [K] Skill tree",
                    "[I] Use potion   [Esc] Quit confirmation",
                ]),
                ("Battle", (255, 200, 160), [
                    "[A] Attack   [P] Potion   [B] Blaze gem",
                    "[R] Run   [D] Defense   [F] Focus",
                    "[Up/Down] Select command   [Space/Enter] Confirm",
                ]),
                ("Anytime", (220, 220, 220), [
                    "[M] Toggle mute (BGM+SE, works on any screen)",
                ]),
            ]
            for title, col, lines in sections:
                draw_text(screen, title, MENU_X, y, fontS, col)
                y += 30
                for line in lines:
                    draw_text(screen, line, MENU_X + 20, y, fontXS, WHITE)
                    y += 26
                y += 14
            label = "[Esc] Back"
            draw_button(screen, fontS, MENU_X, y, fontS.size(label)[0] + 30, 28, label, "back_to_title",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 45:
            # 記録メニュー(タイトル画面に重ねて表示)
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 380))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 300])
            MENU_X = 230      # ボタン幅420を画面中央に揃えた値
            draw_text(screen, "Records", MENU_X, 320, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [MENU_X, 365, 480, 2])
            BTN_W = 420
            y = 383
            label = "[V] Achievements"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_achievements",
                        base_color=(90, 100, 210), mouse_pos=mouse_pos)
            y += 45
            label = "[X] Stats"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_stats",
                        base_color=(40, 155, 150), mouse_pos=mouse_pos)
            y += 45
            label = "[B] Bestiary"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_bestiary",
                        base_color=(215, 130, 40), mouse_pos=mouse_pos)
            y += 45
            label = "[E] Echo Battles"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_echo",
                        base_color=(50, 140, 210), mouse_pos=mouse_pos)
            y += 45
            label = "[D] Daily Ranking"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_daily_ranking",
                        base_color=(60, 175, 95), mouse_pos=mouse_pos)
            y += 60
            label = "[Esc] Back"
            draw_button(screen, fontS, MENU_X, y, fontS.size(label)[0] + 30, 28, label, "back_to_title",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 46:
            # 図鑑(Bestiary): 出会った敵・ボス・見つけたアイテムを一覧表示。
            # モンスター/ボスの名前をクリックすると詳細画面(idx==47)でその姿を確認できる。
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 560))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 90])
            draw_text(screen, "Bestiary", 340, 105, font, (255, 215, 0))
            bdata = load_bestiary()
            ROW_H = 24
            COL_ENEMY_X = 40
            COL_BOSS_X = 260
            COL_ITEM_X = 480
            draw_text(screen, "Monsters", COL_ENEMY_X, 150, fontS, (200, 200, 255))
            for i, name in enumerate(EMY_NAME):
                seen = bdata["enemies"][i]
                label = name if seen else "???"
                bcol = (100, 90, 190) if seen else (70, 70, 78)
                y = 178 + i*ROW_H
                draw_button(screen, fontS, COL_ENEMY_X, y, max(fontS.size(label)[0]+16, 76), ROW_H-2,
                            label, f"view_enemy_{i}", base_color=bcol, mouse_pos=mouse_pos)
            draw_text(screen, "Bosses", COL_BOSS_X, 150, fontS, (255, 170, 120))
            for i, (bfl, bname, bimg) in enumerate(BOSS_BESTIARY):
                seen = bdata["bosses"][i]
                label = bname if seen else "???"
                bcol = (200, 80, 55) if seen else (70, 70, 78)
                y = 178 + i*ROW_H
                draw_button(screen, fontS, COL_BOSS_X, y, max(fontS.size(label)[0]+16, 76), ROW_H-2,
                            label, f"view_boss_{i}", base_color=bcol, mouse_pos=mouse_pos)
            draw_text(screen, "Items", COL_ITEM_X, 150, fontS, (200, 255, 200))
            for i, name in enumerate(TRE_NAME):
                seen = bdata["items"][i]
                label = name if seen else "???"
                col = WHITE if seen else (110, 110, 110)
                draw_text(screen, label, COL_ITEM_X, 180 + i*ROW_H, fontS, col)
            ecount = sum(bdata["enemies"])
            bcount = sum(bdata["bosses"])
            icount = sum(bdata["items"])
            draw_text(screen, f"Monsters: {ecount}/{len(EMY_NAME)}   Bosses: {bcount}/{len(BOSS_BESTIARY)}   Items: {icount}/{len(TRE_NAME)}", 150, 610, fontS, (150, 220, 255))
            label = "[Esc] Back"
            draw_button(screen, fontS, 340, 640, fontS.size(label)[0] + 30, 28, label, "back_to_records",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 47:
            # 図鑑の詳細表示: クリックしたモンスター/ボスの姿を大きく表示する。
            # まだ遭遇していない場合は黒塗りにしてシークレット状態のままにする。
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 560))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 90])
            if bestiary_detail_kind == "boss":
                bfl, bname, bimg_file = BOSS_BESTIARY[bestiary_detail_index]
                display_name = bname if bestiary_detail_seen else "???"
                subtitle = f"Boss - Floor {bfl}" if bestiary_detail_seen else "Not yet encountered"
                name_col = (255, 170, 120) if bestiary_detail_seen else (110, 110, 110)
            else:
                display_name = EMY_NAME[bestiary_detail_index] if bestiary_detail_seen else "???"
                subtitle = "Monster" if bestiary_detail_seen else "Not yet encountered"
                name_col = (255, 215, 0) if bestiary_detail_seen else (110, 110, 110)
            draw_text(screen, display_name, 340, 110, font, name_col)
            draw_text(screen, subtitle, 340, 150, fontS, (200, 200, 200))
            frame_x, frame_y, frame_w, frame_h = 290, 210, 300, 300
            pygame.draw.rect(screen, (40, 40, 40), [frame_x, frame_y, frame_w, frame_h])
            pygame.draw.rect(screen, WHITE, [frame_x, frame_y, frame_w, frame_h], 2)
            if bestiary_detail_seen and bestiary_detail_img is not None:
                img = bestiary_detail_img
                # このスケール結果はbestiary_detail_imgが変わる(=別のモンスターを
                # 選び直す)まで同じなので、id(img)をキーにキャッシュして
                # smoothscaleの毎フレーム再実行を避ける
                cache_key = (id(img), frame_w, frame_h)
                disp_img = _bestiary_detail_scale_cache.get(cache_key)
                if disp_img is None:
                    iw, ih = img.get_width(), img.get_height()
                    scale = min((frame_w-20)/iw, (frame_h-20)/ih) if iw > 0 and ih > 0 else 1.0
                    scale = min(max(scale, 0.1), 3.0)
                    disp_img = pygame.transform.smoothscale(img, (max(1, int(iw*scale)), max(1, int(ih*scale))))
                    _bestiary_detail_scale_cache.clear()
                    _bestiary_detail_scale_cache[cache_key] = disp_img
                ix = frame_x + (frame_w - disp_img.get_width())//2
                iy = frame_y + (frame_h - disp_img.get_height())//2
                screen.blit(disp_img, [ix, iy])
            else:
                # 未発見: 黒塗りのシークレット表示
                pygame.draw.rect(screen, BLACK, [frame_x+4, frame_y+4, frame_w-8, frame_h-8])
                mark = "???"
                mw, mh = font.size(mark)
                draw_text(screen, mark, frame_x + (frame_w-mw)//2, frame_y + (frame_h-mh)//2, font, (80, 80, 80))
            label = "[Esc] Back"
            draw_button(screen, fontS, 340, 640, fontS.size(label)[0] + 30, 28, label, "back_to_bestiary",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 49:
            # キャラクター選択画面(タイトル画面に重ねて表示)
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 420))
            panel.set_alpha(180)
            panel.fill(BLACK)
            screen.blit(panel, [0, 150])
            draw_text(screen, "Choose your Hero", 300, 165, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [80, 205, 720, 2])
            PORTRAIT_BOX = 64
            for i, cid in enumerate(CHARACTER_ORDER):
                c = CHARACTER_TYPES[cid]
                y0 = 225 + i*80
                is_sel = (cid == selected_character)
                col = (255, 215, 0) if is_sel else WHITE
                mark = "-> " if is_sel else "   "
                portrait = imgHero.get(cid)
                if portrait is not None:
                    pw, ph = portrait.get_width(), portrait.get_height()
                    scale = min(PORTRAIT_BOX/pw, PORTRAIT_BOX/ph) if pw > 0 and ph > 0 else 1.0
                    disp = pygame.transform.smoothscale(portrait, (max(1, int(pw*scale)), max(1, int(ph*scale))))
                    frame_rect = [90, y0-6, PORTRAIT_BOX, PORTRAIT_BOX]
                    if is_sel:
                        pygame.draw.rect(screen, (255, 215, 0), [frame_rect[0]-2, frame_rect[1]-2, PORTRAIT_BOX+4, PORTRAIT_BOX+4], 2)
                    screen.blit(disp, [90 + (PORTRAIT_BOX-disp.get_width())//2, y0-6 + (PORTRAIT_BOX-disp.get_height())//2])
                draw_text(screen, f"{mark}[{i+1}] {c['name']}", 170, y0, font, col)
                draw_text(screen, c["desc"], 200, y0+32, fontS, (200, 200, 200))
            draw_text(screen, "[1-4] Choose   [Esc] Back", 260, 545, fontS, WHITE)

        elif idx == 1:
            move_player(key)
            draw_dungeon(screen, fontS)
            title_suffix = f"  - {current_title()}" if current_title() else ""
            draw_text(screen, f"Stage {current_stage(floor)}  Floor {stage_local_floor(floor)}/{STAGE_LENGTH} ({pl_x} {pl_y}){title_suffix}", 60, 40, fontS, WHITE)
            draw_level_gauge(screen, 60, 62, fontS)
            status_y = 88
            if floor_modifier:
                # 入室時の"Welcome to floor"メッセージが消えた後もフロア特性を
                # 忘れないよう、探索中は常時小さく表示し続ける。
                fm = FLOOR_MODIFIERS[floor_modifier]
                draw_text(screen, fm["name"], 60, status_y, fontS, fm["color"])
                status_y += 26
            if is_blood_moon:
                draw_text(screen, "BLOOD MOON FLOOR (danger & reward both higher)", 60, status_y, fontS, (230, 50, 50))
                status_y += 26
            if not is_boss_floor(floor):
                # ボス階に入った瞬間の警告だけだと不意打ち感が強いため、近づいて
                # いる間(残り3階以内)から前もって心構えできるようにヒントを出す。
                floors_to_boss = BOSS_FLOOR_INTERVAL - (floor % BOSS_FLOOR_INTERVAL)
                if floors_to_boss <= 3:
                    draw_text(screen, f"Boss floor in {floors_to_boss}", 60, status_y, fontS, (255, 160, 90))
                    status_y += 26
            exp_pct = exploration_percent()
            if exp_pct >= EXPLORATION_PERFECT_THRESHOLD:
                exp_col = (255, 215, 60)
            elif exp_pct >= EXPLORATION_BONUS_THRESHOLD:
                exp_col = (120, 255, 150)
            else:
                exp_col = WHITE
            draw_text(screen, f"Explored: {exp_pct}%", 60, status_y, fontS, exp_col)
            status_y += 26
            if golden_sprite_pos is not None:
                draw_text(screen, f"Golden slime nearby! ({golden_sprite_timer} steps)", 60, status_y, fontS, (255, 215, 60))
                status_y += 26
            if collapse_timer > 0:
                warn_col = (255, 70, 40) if tmr % 10 < 5 else (255, 200, 60)
                draw_text(screen, f"VAULT COLLAPSING! FLEE! ({collapse_timer})", 60, status_y, fontS, warn_col)
                status_y += 26
            if boulder_pos is not None:
                warn_col = (255, 70, 40) if tmr % 10 < 5 else (255, 200, 60)
                draw_text(screen, f"A BOULDER IS CHASING YOU! ({boulder_timer})", 60, status_y, fontS, warn_col)
                status_y += 26
            draw_text(screen, "[Q] Save", 60, status_y, fontS, WHITE)
            status_y += 26
            if skill_points > 0:
                draw_text(screen, f"[K] Skills ({skill_points}pt)", 60, status_y, fontS, (255, 215, 0))
                status_y += 26
            if potion > 0:
                draw_text(screen, "[I] Potion", 60, status_y, fontS, WHITE)
                status_y += 26
            if pl_poison > 0:
                draw_text(screen, f"POISON x{pl_poison}", 60, status_y, fontS, (190, 80, 220))
                status_y += 26
            if curse_active:
                draw_text(screen, "CURSED (STR/DEF down)", 60, status_y, fontS, (170, 40, 200))
                status_y += 26
            if ally_buff_active:
                draw_text(screen, "ALLY AIDING YOU (STR/DEF up)", 60, status_y, fontS, (120, 200, 255))
                status_y += 26
            if bounty_active:
                draw_text(screen, f"BOUNTY: {bounty_kills}/{bounty_target} defeated", 60, status_y, fontS, (230, 190, 90))
                status_y += 26
            if totem_buff_active:
                draw_text(screen, f"TOTEM BLESSING (+{totem_str_bonus} STR, +{totem_def_bonus} DEF)", 60, status_y, fontS, (230, 140, 60))
                status_y += 26
            if map_fragments_active:
                draw_text(screen, f"MAP FRAGMENTS: {map_fragments_found}/{MAP_FRAGMENT_COUNT} found", 60, status_y, fontS, (210, 180, 130))
                status_y += 26
            if has_sacred_key:
                draw_text(screen, "CARRYING SACRED KEY", 60, status_y, fontS, (230, 200, 90))
                status_y += 26
            if pet_type is not None:
                draw_pet_status(screen, 60, status_y, fontS)
                status_y += 26
            if daily_mode:
                draw_text(screen, "[Daily Challenge]", 60, status_y, fontS, (120, 255, 150))
                status_y += 26
            if welcome > 0:
                welcome = welcome - 1
                draw_text(screen, f"Welcome to floor {floor}", 300, 180, font, CYAN)
                if floor_modifier:
                    fm = FLOOR_MODIFIERS[floor_modifier]
                    draw_text(screen, f"{fm['name']}: {fm['desc']}", 220, 225, fontS, fm["color"])
                if is_boss_floor(floor) and floor not in boss_floors_cleared:
                    # ボス階に足を踏み入れたことを警告し、緊張感と身構える猶予を与える
                    # (静かに階段まで歩いて不意打ちされるより、事前に分かった方が
                    # ポーションの準備などができて楽しい)
                    pulse = 140 + int(90 * abs((tmr % 20) - 10) / 10)
                    draw_text(screen, "! A powerful presence lurks on this floor !", 130, 250, fontS, (255, pulse//3, 30))
            if stage_intro_timer > 0:
                stage_intro_timer = stage_intro_timer - 1
                draw_text(screen, f"STAGE {stage_intro_num}", 330, 260, font, BLINK[tmr%6])

        elif idx == 55:
            # ダンジョン探索中にEscを押した時の終了確認(誤操作で未セーブの進行を
            # 失わないようにするための確認ダイアログ)
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Quit to desktop?", 300, 320, font, WHITE)
            draw_text(screen, "Unsaved progress since the last save/autosave will be lost.", 130, 370, fontS, (220, 180, 100))
            draw_text(screen, "[Y] Quit   [N/Esc] Cancel", 310, 420, fontS, WHITE)

        elif idx == 30:
            # セーブメニュー(ダンジョン画面に重ねて表示)
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Save Game", 340, 200, font, WHITE)
            for i in range(1, SAVE_SLOTS+1):
                fl = get_slot_floor(i)
                label = f"Slot {i}: floor {fl}" if fl is not None else f"Slot {i}: Empty"
                draw_text(screen, label, 340, 200+i*60, font, WHITE)
            draw_text(screen, "[1-3] Save   [Esc] Cancel", 310, 500, fontS, WHITE)

        elif idx == 31:
            # ロードメニュー(タイトル画面に重ねて表示)
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            # 背景の絵柄とボタンが被って読みにくいので、後ろに半透明の帯を敷く
            panel = pygame.Surface((880, 340))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 220])
            draw_text(screen, "Load Game", 340, 240, font, WHITE)
            BTN_X, BTN_W = 240, 400
            y = 300
            for i in range(1, SAVE_SLOTS+1):
                fl = get_slot_floor(i)
                has_save = fl is not None
                label = f"Slot {i}: floor {fl}" if has_save else f"Slot {i}: Empty"
                draw_button(screen, font, BTN_X, y, BTN_W, 40, label,
                            f"load_slot_{i}" if has_save else None,
                            base_color=(50, 110, 210), mouse_pos=mouse_pos,
                            enabled=has_save, align="center")
                y += 54
            draw_text(screen, "[1-3] Load   [Esc] Back", 340, y+8, fontS, WHITE)

        elif idx == 33:
            # 実績一覧(タイトル画面に重ねて表示)
            # 実績数が画面の縦幅に収まらないため、Up/Downで縦スクロールするページ表示にする。
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 560))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 140])
            ach = load_achievements()
            total_c = len(ACHIEVEMENT_DEFS)
            earned_c = sum(1 for key_name, _ in ACHIEVEMENT_DEFS if ach.get(key_name, False))
            draw_text(screen, "Achievements", 320, 155, font, WHITE)
            draw_text(screen, f"{earned_c}/{total_c} earned", 600, 162, fontS, (150, 220, 255))
            BADGE_SIZE = 26
            ROW_H = 32
            START_Y = 195
            badge_disp = get_achievement_badge_image(BADGE_SIZE)
            stats_snapshot = load_stats()
            visible = ACHIEVEMENT_DEFS[achievements_scroll:achievements_scroll + ACHIEVEMENTS_VISIBLE_ROWS]
            for i, (key_name, label) in enumerate(visible):
                done = ach.get(key_name, False)
                row_y = START_Y + i*ROW_H
                if done:
                    screen.blit(badge_disp, [130, row_y-2])
                else:
                    pygame.draw.rect(screen, (90, 90, 90), [130, row_y-2, BADGE_SIZE, BADGE_SIZE], 1)
                col = (255, 215, 0) if done else (150, 150, 150)
                draw_text(screen, label, 130 + BADGE_SIZE + 10, row_y, fontS, col)
                if not done and key_name in ACHIEVEMENT_PROGRESS:
                    stat_key, goal = ACHIEVEMENT_PROGRESS[key_name]
                    cur = min(goal, stats_snapshot.get(stat_key, 0))
                    draw_text(screen, f"({cur}/{goal})", 700, row_y, fontS, (110, 110, 110))
            trap_c = ach.get("trap_count", 0)
            list_bottom_y = START_Y + ACHIEVEMENTS_VISIBLE_ROWS*ROW_H + 10
            draw_text(screen, f"Traps triggered: {trap_c}", 130, list_bottom_y, fontS, WHITE)
            if total_c > ACHIEVEMENTS_VISIBLE_ROWS:
                shown_to = min(achievements_scroll + ACHIEVEMENTS_VISIBLE_ROWS, total_c)
                draw_text(screen, f"{achievements_scroll+1}-{shown_to} of {total_c}   [Up/Down] Scroll   [Esc] Back",
                          130, 660, fontS, WHITE)
            else:
                draw_text(screen, "[Esc] Back", 340, 660, fontS, WHITE)

        elif idx == 2:
            draw_dungeon(screen, fontS)
            if 1 <= tmr <= 5:
                h = 80*tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 5:
                if pending_bonus_room:
                    pending_bonus_room = False
                    generate_bonus_room()
                    welcome = 15
                    info_message = "Bonus Room!"
                    info_timer = 60
                    autosave()
                    flush_playtime()
                else:
                    if curse_active:
                        pl_str += 20
                        pl_def_base += 5
                        curse_active = False
                    if ally_buff_active:
                        pl_str -= ALLY_STR_BONUS
                        pl_def_base -= ALLY_DEF_BONUS
                        ally_buff_active = False
                    if totem_buff_active:
                        pl_str -= totem_str_bonus
                        pl_def_base -= totem_def_bonus
                        totem_buff_active = False
                    if skill_floor_heal_pct > 0:
                        heal = int(pl_lifemax * skill_floor_heal_pct)
                        pl_life = min(pl_lifemax, pl_life + heal)
                    # 次のフロアを生成する前に、このフロアをどれだけ探索したかを集計し、
                    # しっかり探索していたプレイヤーにボーナスを渡す
                    explore_pct = exploration_percent()
                    if explore_pct >= EXPLORATION_PERFECT_THRESHOLD:
                        potion += 1
                        blazegem += 1
                        food += 30
                        record_stat("floors_fully_explored")
                        fully_explored_total = load_stats().get("floors_fully_explored", 0)
                        if fully_explored_total >= 10:
                            unlock_achievement("explorer")
                        if fully_explored_total >= 50:
                            unlock_achievement("master_cartographer")
                        info_message = f"Perfect exploration ({explore_pct}%)! +1 Potion, +1 Blaze gem, +30 Food"
                        info_timer = 70
                    elif explore_pct >= EXPLORATION_BONUS_THRESHOLD:
                        potion += 1
                        food += 20
                        record_stat("floors_fully_explored")
                        fully_explored_total = load_stats().get("floors_fully_explored", 0)
                        if fully_explored_total >= 10:
                            unlock_achievement("explorer")
                        if fully_explored_total >= 50:
                            unlock_achievement("master_cartographer")
                        info_message = f"Thorough exploration ({explore_pct}%)! +1 Potion, +20 Food"
                        info_timer = 70
                    if is_blood_moon:
                        record_stat("blood_moons_survived")
                        unlock_achievement("blood_moon_survivor")
                    floor = floor + 1
                    if floor > fl_max:
                        fl_max = floor
                    record_stat("total_floors_descended")
                    record_stat_max("deepest_floor_reached", floor)
                    if load_stats().get("deepest_floor_reached", 0) >= 60:
                        unlock_achievement("deep_delver")
                    if difficulty == "Hard" and floor >= MAX_FLOOR:
                        unlock_achievement("hard_clear")
                    welcome = 15
                    if stage_local_floor(floor) == 1:
                        stage_intro_timer = 90
                        stage_intro_num = current_stage(floor)
                    make_dungeon()
                    put_event()
                    autosave()
                    flush_playtime()
            if 6 <= tmr <=9:
                h = 80*(10-tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 10:
                idx = 1
        
        elif idx == 3:
            draw_dungeon(screen, fontS)
            if treasure == 10 and floor_variant == 1:
                # ペットの卵も、そのフロアのステージテーマ(クリスタル/炎)に合わせた見た目にする
                screen.blit(imgPetEggCrystal, [320, 220])
            elif treasure == 10 and floor_variant == 2:
                screen.blit(imgPetEggFlame, [320, 220])
            else:
                screen.blit(imgItem[treasure], [320, 220])
            draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)
            if tmr == 24:
                idx = 1
        
        elif idx == 4:
            draw_dungeon(screen, fontS)
            screen.blit(imgDamage, [320, 220])
            if tmr == 25:
                idx = 1
        
        elif idx == 9:
            if tmr <= 30:
                PL_TURN = [2, 4, 0, 6]
                pl_a = PL_TURN[tmr%4]
                if tmr == 30: pl_a = 8
                draw_dungeon(screen, fontS)
            elif tmr == 31:
                se[3].play()
                draw_text(screen, "You died.", 360, 240, font, RED)
                draw_text(screen, "Game over.", 360, 380, font, RED)
                record_stat("total_deaths")
                flush_playtime()
                if daily_mode:
                    record_daily_result(floor, cleared=False)
            elif tmr == 100:
                idx = 0
                tmr = 0
                
        elif idx == 10:
            if tmr == 1:
                try:
                    moving = False
                    move_progress = 0.0
                    hold_dir = None
                    hold_timer = 0
                except NameError:
                    pass
                init_battle()
                init_message()
                # 通常戦闘ではボス専用曲(Tolerance_Deviation.mp3/natsuyasuminotanken.mp3)を
                # 流さないようにする(typ==11/12はもうボス専用画像なので通常戦闘には出現しない)
                pygame.mixer.music.load(bgm_battle_for_floor(floor))
                pygame.mixer.music.play(-1)
                    
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(battle_bg_for_floor(floor), [bx, by])
                draw_text(screen, "Encounter!", 350, 200, font, WHITE)
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" appear!", 300, 200, font, WHITE)
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                
        elif idx == 11:
            draw_battle(screen, fontS)
            if tmr == 1 and not turn_msg_shown: 
                if pl_poison > 0:
                    pdmg = max(1, int(pl_lifemax // 20 * skill_poison_mult))
                    pl_life -= pdmg
                    pl_poison = max(0, pl_poison - 30)
                    battle_took_damage = True
                    set_message(f"Poison {pdmg}dmg!", (190, 80, 220))
                    if pl_life <= 0:
                        pl_life = 0
                set_message("Your turn.", (150, 220, 255))
                turn_msg_shown = True
                if pl_life <= 0:
                    idx = 15
                    tmr = 0
            if idx == 11 and battle_command(screen, font, key):
                if not flg_action:
                    if btl_cmd == 0:
                        idx = 12
                        tmr = 0
                        flg_action = True
                    elif btl_cmd == 1:
                        if potion > 0:
                            idx = 20
                            tmr = 0
                            flg_action = True
                        else:
                            if not no_potion_shown:
                                set_message("No Potion!", (200, 90, 90))
                                no_potion_shown = True
                    elif btl_cmd == 2: 
                        if blazegem > 0:
                            idx = 21
                            tmr = 0
                            flg_action = True
                        else:
                            if not no_blazegem_shown:
                                set_message("No Blaze gem!", (200, 90, 90))
                                no_blazegem_shown = True
                    elif btl_cmd == 3:
                        idx = 14
                        tmr = 0
                        flg_action = True
                    elif btl_cmd == 4:
                        if def_pill > 0:
                            idx = 23
                            tmr = 0
                            flg_action = True
                        else:
                            if not no_defensepill_shown:
                                set_message("No Defense Pill!", (200, 90, 90))
                                no_defensepill_shown = True
                    elif btl_cmd == 5:
                        idx = 24
                        tmr = 0
                        flg_action = True
                                        
        elif idx == 12:
            draw_battle(screen, fontS)
            if tmr ==1:
                set_message("You attack!", (255, 230, 150))
                se[0].play()
                last_atk_special = None
                combo_count += 1
                prev_best_combo = load_stats().get("highest_combo_reached", 0)
                record_stat_max("highest_combo_reached", combo_count)
                if combo_count >= 20:
                    unlock_achievement("combo_king")
                if (combo_count > prev_best_combo and prev_best_combo > 0
                        and not combo_record_shown_this_battle):
                    # 自己ベストのコンボ数を更新した瞬間、既存のクリティカル演出と
                    # 同じ画面フラッシュ機構を金色で流用して達成感を出す
                    # (1バトルにつき一度だけ。連続ヒットのたびに出ると煩わしいため)。
                    combo_record_shown_this_battle = True
                    set_message(f"New best combo! x{combo_count}", (255, 215, 90))
                    crit_flash_color = (255, 215, 90)
                    crit_flash_timer = CRIT_FLASH_FRAMES + 2
                if pl_str >= 500:
                    dmg = pl_str + random.randint(0, 200)
                elif pl_str >= 300:
                    dmg = pl_str + random.randint(0, 50)
                else:
                    dmg = pl_str + random.randint(0, 15)
                dmg = int(dmg * modifier_atk_mult())
                if pl_charge:
                    dmg = int(dmg * 1.5)
                    pl_charge = False
                    set_message("Focus attack!", (255, 160, 60))
                cmult = combo_damage_mult()
                if cmult > 1.0:
                    dmg = int(dmg * cmult)
                    set_message(f"Combo x{combo_count}!", (255, 160, 0))
                is_finisher = combo_count >= COMBO_FINISHER_THRESHOLD
                if is_finisher:
                    dmg = int(dmg * COMBO_FINISHER_MULT)
                    se[4].play()
                    set_message("COMBO FINISHER!!", (255, 60, 220))
                    record_stat("combo_finishers_used")
                    unlock_achievement("combo_finisher")
                    if load_stats().get("combo_finishers_used", 0) >= 25:
                        unlock_achievement("chain_reaction")
                    combo_count = 0
                    crit_flash_color = (255, 90, 220)
                    crit_flash_timer = CRIT_FLASH_FRAMES + 4
                    trigger_screen_shake(10, 6)
                    last_atk_special = "finisher"
                total_crit_chance = skill_crit_chance + modifier_crit_chance_bonus()
                if total_crit_chance > 0 and random.random() < total_crit_chance:
                    dmg = int(dmg * modifier_crit_dmg_mult())
                    set_message("CRITICAL HIT!", (255, 60, 60))
                    crit_flash_color = (255, 255, 190)
                    crit_flash_timer = CRIT_FLASH_FRAMES
                    trigger_screen_shake(6, 4)
                    if last_atk_special is None:
                        last_atk_special = "crit"
                    record_stat("critical_hits_landed")
                    if load_stats().get("critical_hits_landed", 0) >= 50:
                        unlock_achievement("crit_master")
                record_stat_max("highest_single_hit_damage", dmg)
                if dmg >= MASSIVE_HIT_THRESHOLD:
                    # コンボ/会心/Focus攻撃が重なった一撃だけの特別演出。
                    # 既存のクリティカル/フィニッシャー演出より一段強調して、
                    # 大ダメージを叩き出せた瞬間の爽快感をさらに際立たせる。
                    set_message("MASSIVE HIT!", (255, 215, 60))
                    crit_flash_color = (255, 215, 60)
                    crit_flash_timer = CRIT_FLASH_FRAMES + 6
                    trigger_screen_shake(14, 8)
                    last_atk_special = "massive"
                    unlock_achievement("sharpshooter")
            if 2 <= tmr <= 4:
                screen.blit(imgEffect[0], [700-tmr*120, -100+tmr*120])
            if tmr == 5:
                emy_blink = 5
                set_message(str(dmg)+"pts of damage!", (255, 100, 100))
                if last_atk_special == "massive":
                    popup_color = (255, 215, 60)
                elif last_atk_special == "finisher":
                    popup_color = (255, 90, 220)
                elif last_atk_special == "crit":
                    popup_color = (255, 230, 90)
                else:
                    popup_color = (255, 140, 90)
                popup_x = emy_x + imgEnemy.get_width()/2 - 16
                popup_y = emy_y + emy_step - 6
                spawn_damage_popup(popup_x, popup_y, str(dmg), popup_color, big=last_atk_special is not None)
            if tmr == 11:
                emy_life = emy_life - dmg
                record_stat("total_damage_dealt", dmg)
                if load_stats().get("total_damage_dealt", 0) >= 100000:
                    unlock_achievement("executioner")
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
                elif pet_type == "slime" and random.randint(0, 99) < 10:
                    assist_dmg = max(1, int(dmg * 0.3))
                    emy_life = max(0, emy_life - assist_dmg)
                    set_message(f"Slime Pal assists! {assist_dmg}dmg!", (150, 220, 255))
                    if emy_life <= 0:
                        idx = 16
                        tmr = 0
                if ((in_boss_battle or in_echo_battle) and not boss_phase2 and emy_life > 0
                        and emy_life <= emy_lifemax * 0.5):
                    boss_phase2 = True
                    emy_str = int(emy_str * BOSS_PHASE2_STR_MULT)
                    emy_blink = 12
                    dmg_eff = 8
                    se[1].play()
                    set_message(f"{emy_name} grows furious!!", (255, 80, 40))
            if tmr == 16:
                idx = 13
                tmr = 0
                
        elif idx == 13:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Enemy turn.", (255, 150, 150))
            if tmr == 5:
                set_message(emy_name+" attack!", (255, 150, 150))
                se[0].play()
                emy_step = 30
            if tmr == 9:
                dmg_reduction = pl_def_base + pl_def_buff + pet_def_bonus + modifier_def_bonus()
                dmg = max(1, int(((emy_str + random.randint(0, emy_str)) - dmg_reduction) * modifier_incoming_dmg_mult()))
                set_message(str(dmg)+"pts of damage!", (255, 100, 100))
                spawn_damage_popup(190, 585, str(dmg), (255, 90, 90), big=boss_phase2)
                dmg_eff = 5
                emy_step = 0
                trigger_screen_shake(8 if boss_phase2 else 5, 5 if boss_phase2 else 3)
                if typ in (5, 7, 14) and pl_poison == 0 and not modifier_poison_immune() and random.randint(0, 99) < 30 + modifier_poison_chance_bonus():
                    pl_poison = 50
                    set_message("Poisoned!", (190, 80, 220))
            if tmr == 15:
                pl_life = pl_life - dmg
                battle_took_damage = True
                if pl_life < 0:
                    pl_life = 0
                    idx = 15
                    tmr = 0
            if tmr == 20:
                pl_def_buff = max(0, pl_def_buff -5)
                
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                
                idx = 11
                tmr = 0
                
        elif idx == 14:
            draw_battle(screen, fontS)
            if tmr == 1:
                combo_count = 0
                set_message("...", (180, 180, 180))
            if tmr == 2: set_message(".....", (180, 180, 180))
            if tmr == 3: set_message(".......", (180, 180, 180))
            if tmr == 4: set_message(".........", (180, 180, 180))
            if tmr == 5:
                if random.randint(0, 99) < flee_chance_pct():
                    idx = 22
                    ambush_battles_remaining = 0
                    mimic_battle_active = False
                    in_rift_battle = False
                    doppelganger_battle_active = False
                    chimera_battle_active = False
                    record_stat("battles_fled")
                    if load_stats().get("battles_fled", 0) >= 10:
                        unlock_achievement("escape_artist")
                else:
                    set_message("You failed to flee.", (200, 90, 90))
            if tmr == 10:
                idx = 13
                tmr = 0
                
        elif idx == 15:
            draw_battle(screen, fontS)
            if tmr == 1:
                pygame.mixer.music.stop()
                set_message("You lose.", (220, 60, 60))
            if tmr == 11:
                idx = 9
                tmr = 29
        
        elif idx == 16:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You win!", (255, 215, 0))
                pygame.mixer.music.stop()
                se[5].play()
                record_stat("total_kills")
                if load_stats().get("total_kills", 0) >= 500:
                    unlock_achievement("veteran")
                register_bounty_kill()
                if not battle_took_damage:
                    unlock_achievement("no_damage_win")
                exp_gain = int(max(1, (typ + 1) * emy_lv * 3) * pl_exp_mult * diff_params()["exp_mult"] * skill_exp_mult * char_params()["exp_mult"] * modifier_exp_mult())
                if is_elite:
                    exp_gain = int(exp_gain * ELITE_EXP_MULT)
                    unlock_achievement("elite_hunter")
                    record_stat("elites_defeated")
                    if load_stats().get("elites_defeated", 0) >= 100:
                        unlock_achievement("elite_slayer")
                if is_blood_moon:
                    exp_gain = int(exp_gain * BLOOD_MOON_EXP_MULT)
                pl_exp += exp_gain
                set_message(f"EXP +{exp_gain}!", (60, 200, 70))
            if tmr == 28:
                if pl_exp >= exp_threshold(pl_lv + 1):
                    idx = 17
                    tmr = 0
                else:
                    resolve_post_battle_transition()

        elif idx == 17:
            draw_battle(screen, fontS)
            if tmr == 1:
                lif_p = 0
                str_p = 0
                def_inc = 0
                gm = diff_params()["growth_mult"]
                while pl_exp >= exp_threshold(pl_lv + 1):
                    pl_lv += 1
                    lif_p += int(random.randint(10, 20) * gm)
                    str_p += int(random.randint(5, 10) * gm)
                    def_inc += int(random.randint(1, 5) * gm)
                    skill_points += 1
                set_message(f"Level up! Lv{pl_lv}", (255, 215, 0))
                se[4].play()
            if tmr == 21:
                set_message(f"Max life +{lif_p}", (60, 200, 70))
                pl_lifemax += lif_p
                pl_life += lif_p
            if tmr == 26:
                set_message(f"Str +{str_p}", (255, 140, 60))
                pl_str += str_p
            if tmr == 31:
                set_message(f"Def+{def_inc}", (120, 180, 255))
                pl_def_base += def_inc
            if tmr == 50:
                resolve_post_battle_transition()
                
        elif idx == 20:
            draw_battle(screen, fontS)
            if tmr == 1:
                combo_count = 0
                set_message("Potion!", (60, 200, 70))
                se[2].play()
            if tmr == 6:
                pl_life = pl_lifemax
                potion -= 1
                record_stat("potions_used")
                if load_stats().get("potions_used", 0) >= 20:
                    unlock_achievement("alchemist")
            if tmr == 11:
                idx = 13
                tmr = 0
        elif idx == 21:
            draw_battle(screen, fontS)
            img_rz = pygame.transform.rotozoom(imgEffect[1], 30*tmr, (12-tmr)/8)
            X = 440-img_rz.get_width()/2
            Y = 360-img_rz.get_height()/2
            screen.blit(img_rz, [X, Y])
            if tmr == 1:
                combo_count = 0
                set_message("Blaze gem!", (255, 140, 40))
                se[1].play()
            if tmr == 6:
                blazegem -= 1
                record_stat("blazegems_used")
                if load_stats().get("blazegems_used", 0) >= 30:
                    unlock_achievement("demolitionist")
            if tmr == 11:
                dmg = int(1000 * modifier_blaze_dmg_mult())
                idx = 12
                tmr = 4
                
        elif idx == 22:
            pygame.mixer.music.load(bgm_field_for_floor(floor))
            pygame.mixer.music.play(-1)
            idx = 1
            
        elif idx == 23:
            draw_battle(screen, fontS)
            if tmr == 1:
                combo_count = 0
                set_message("Defense Pill!", (120, 180, 255))
            if tmr == 6:
                buff_amount = random.randint(5, 15)
                pl_def_buff += buff_amount
                def_pill -= 1
                set_message(f"Buff Def +{buff_amount}", (120, 180, 255))
                record_stat("def_pills_used")
                if load_stats().get("def_pills_used", 0) >= 25:
                    unlock_achievement("fortified")
            if tmr == 20:
                idx = 13
                tmr = 0
                
        elif idx == 24:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Focus!", (255, 160, 60))
                pl_charge = True
                record_stat("focus_used")
                if load_stats().get("focus_used", 0) >= 40:
                    unlock_achievement("tactician")
            if tmr == 15:
                idx = 13
                tmr = 0
                
        elif idx == 25:
            if tmr == 1:
                try:
                    moving = False
                    move_progress = 0.0
                    hold_dir = None
                    hold_timer = 0
                except NameError:
                    pass
                in_boss_battle = True
                init_boss_battle()
                init_message()
                pygame.mixer.music.load("sound/Tolerance_Deviation.mp3")
                pygame.mixer.music.play(-1)
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(battle_bg_for_floor(floor), [bx, by])
                draw_text(screen, "Boss Battle!", 320, 200, font, RED)
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" appear!", 280, 200, font, RED)
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                
        elif idx == 26:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Boss defeated!", (255, 215, 0))
                boss_floors_cleared.add(floor)
                unlock_achievement("boss_defeat")
                record_stat("bosses_defeated_count")
                if difficulty == "Hard" and floor >= MAX_FLOOR:
                    unlock_achievement("hard_clear")
                pl_lifemax += 100
                pl_life += 100
                pl_str += 30
                pl_def_base += 10
                pl_exp_mult += 0.1
                boss_loot_rolled = random.sample(BOSS_LOOT_TABLE, k=2)
                for entry in boss_loot_rolled:
                    if entry["key"] == "potion":
                        potion += 1
                    elif entry["key"] == "blazegem":
                        blazegem += 1
                    elif entry["key"] == "defpill":
                        def_pill += 1
                    elif entry["key"] == "food":
                        food += 50
            if tmr == 20:
                set_message("Permanent power up!", (255, 215, 0))
            if 32 <= tmr <= 74:
                # ドロップしたアイテムを1つずつアイコン付きで表示する
                panel_w, panel_h = 380, 150
                px, py = 440 - panel_w//2, 380
                loot_panel = pygame.Surface((panel_w, panel_h))
                loot_panel.set_alpha(190)
                loot_panel.fill((20, 20, 30))
                screen.blit(loot_panel, [px, py])
                pygame.draw.rect(screen, (255, 215, 0), [px, py, panel_w, panel_h], 2)
                draw_text(screen, "Loot!", px + 16, py + 10, font, (255, 215, 0))
                for i, entry in enumerate(boss_loot_rolled):
                    if tmr >= 36 + i*18:
                        icon = imgItem[entry["icon"]]
                        ix = px + 30 + i*170
                        iy = py + 50
                        screen.blit(icon, [ix, iy])
                        draw_text(screen, entry["label"], ix - 10, iy + 70, fontS, (120, 255, 150))
            if tmr == 75:
                in_boss_battle = False
                if in_hidden_stage:
                    unlock_achievement("hidden_boss_defeat")
                    in_hidden_stage = False
                    idx = 41
                    tmr = 0
                elif floor >= MAX_FLOOR:
                    unlock_achievement("game_clear")
                    idx = 27
                    tmr = 0
                elif stage_local_floor(floor) == STAGE_LENGTH:
                    # ステージクリア: 次のステージへ進む前に拠点(サンクチュア)を挟む
                    idx = 28
                    tmr = 0
                else:
                    pygame.mixer.music.load(bgm_field_for_floor(floor))
                    pygame.mixer.music.play(-1)
                    idx = 2
                    tmr = 0

        elif idx == 27:
            # 全3ステージクリア(ゲームクリア)演出
            if tmr == 1:
                pygame.mixer.music.stop()
                se[5].play()
                record_stat("runs_completed")
                flush_playtime()
                if daily_mode:
                    record_daily_result(floor, cleared=True)
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, "GAME CLEAR!", 280, 300, font, (255, 215, 0))
            draw_text(screen, "You cleared all 3 stages!", 250, 360, font, WHITE)
            draw_text(screen, f"Difficulty: {difficulty}", 320, 420, fontS, WHITE)
            if tmr > 90:
                draw_text(screen, "Press space key", 320, 480, font, BLINK[tmr%6])
            if tmr > 90 and key[K_SPACE] == 1:
                idx = 0
                tmr = 0

        elif idx == 28:
            # ステージ間の拠点(サンクチュア): 全回復・食料補給・アイテム交換ができる安全地帯
            if tmr == 1:
                pl_life = pl_lifemax
                food = max(food, 150)
                pygame.mixer.music.load("sound/ohd_bgm_title.ogg")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 470))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 190])
            draw_text(screen, f"Stage {current_stage(floor)} Cleared!", 260, 210, font, (255, 215, 0))
            draw_text(screen, "Sanctuary - rest and prepare", 250, 260, fontS, WHITE)
            draw_text(screen, f"HP: {pl_life}/{pl_lifemax}   Food: {food}", 250, 300, fontS, CYAN)
            col_p = WHITE if potion >= 2 else (110, 110, 110)
            col_b = WHITE if blazegem >= 1 else (110, 110, 110)
            col_f = WHITE if food >= 60 else (110, 110, 110)
            col_w = (255, 215, 0) if potion >= 1 else (110, 110, 110)
            draw_text(screen, "[P] Exchange: 2 Potion -> 1 Defense Pill", 130, 350, fontS, col_p)
            draw_text(screen, "[B] Exchange: 1 Blaze gem -> Food +100", 130, 390, fontS, col_b)
            draw_text(screen, "[F] Exchange: Food 60 -> 1 Potion", 130, 430, fontS, col_f)
            draw_text(screen, "[W] Gamble: wager 1 Potion (50/50 double or lose)", 130, 470, fontS, col_w)
            if info_timer > 0 and info_message != "":
                draw_text(screen, info_message, 250, 510, fontS, CYAN)
            draw_text(screen, "[Space] Proceed to next stage", 250, 590, font, BLINK[tmr%6])
            if tmr > 5 and key[K_SPACE] == 1:
                idx = 2
                tmr = 0

        elif idx == 48:
            # 旅の商人: ダンジョン探索中に出会う一度限りの簡易な取引所
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(190)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "A traveling merchant!", 260, 160, font, (255, 180, 60))
            draw_text(screen, f"Food: {food}   Potion: {potion}   Blaze gem: {blazegem}", 190, 210, fontS, CYAN)
            mc_potion = merchant_trade_cost(80)
            mc_blaze = merchant_trade_cost(2)
            mc_defpill = merchant_trade_cost(2)
            mc_pet = merchant_trade_cost(150)
            col1 = WHITE if food >= mc_potion else (110, 110, 110)
            col2 = WHITE if potion >= mc_blaze else (110, 110, 110)
            col3 = WHITE if blazegem >= mc_defpill else (110, 110, 110)
            draw_text(screen, f"[1] {mc_potion} Food -> 1 Potion", 200, 280, fontS, col1)
            draw_text(screen, f"[2] {mc_blaze} Potion -> 1 Blaze gem", 200, 320, fontS, col2)
            draw_text(screen, f"[3] {mc_defpill} Blaze gem -> 1 Defense Pill", 200, 360, fontS, col3)
            if pet_type is None:
                col4 = WHITE if food >= mc_pet else (110, 110, 110)
                draw_text(screen, f"[4] {mc_pet} Food -> Pet Egg", 200, 400, fontS, col4)
            if floor_modifier == "bazaar":
                draw_text(screen, "Bazaar Floor: prices reduced!", 250, 250, fontS, (255, 225, 140))
            if info_timer > 0 and info_message != "":
                draw_text(screen, info_message, 250, 440, fontS, (120, 255, 150))
            draw_text(screen, "[Esc] Leave", 300, 480, fontS, WHITE)

        elif idx == 40:
            # 隠しボス登場演出(通常のボス戦idx==25と同様の流れ)
            if tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(battle_bg_for_floor(floor), [bx, by])
                draw_text(screen, "Hidden Boss Battle!", 220, 200, font, (200, 60, 220))
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" appear!", 260, 200, font, (200, 60, 220))
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False

        elif idx == 41:
            # 隠しボス撃破(真エンディング)演出
            if tmr == 1:
                pygame.mixer.music.stop()
                se[5].play()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, "TRUE ENDING", 300, 300, font, (200, 60, 220))
            draw_text(screen, "You defeated the hidden boss!", 210, 360, font, WHITE)
            draw_text(screen, f"Difficulty: {difficulty}", 320, 420, fontS, WHITE)
            if tmr > 90:
                draw_text(screen, "Press space key", 320, 480, font, BLINK[tmr%6])
            if tmr > 90 and key[K_SPACE] == 1:
                idx = 0
                tmr = 0

        elif idx == 51:
            # エコーバトル登場演出(通常のボス戦idx==25と同様の流れ)
            if tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(battle_bg_for_floor(echo_target_floor), [bx, by])
                draw_text(screen, "Echo Battle!", 300, 200, font, (120, 200, 255))
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" appear!", 260, 200, font, (120, 200, 255))
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False

        elif idx == 52:
            # エコーバトル選択画面(記録メニューから開く)
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 470))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 150])
            draw_text(screen, "Echo Battles", 300, 170, font, (120, 200, 255))
            draw_text(screen, "Refight a defeated boss's echo for a small permanent reward.", 100, 210, fontS, (200, 200, 200))
            bdata = load_bestiary()
            y = 250
            for i, fl in enumerate(ECHO_ELIGIBLE_FLOORS):
                bi = boss_bestiary_index_for_floor(fl)
                seen = bdata["bosses"][bi] if bi is not None else False
                bname = boss_name_for_floor(fl)
                label = f"[{i+1}] {bname} (Floor {fl})" if seen else f"[{i+1}] ??? (Floor {fl})"
                col = (120, 200, 255) if seen else (110, 110, 110)
                draw_text(screen, label, 130, y, fontS, col)
                y += 32
            draw_text(screen, "[1-9] Challenge   [Esc] Back", 250, 590, fontS, WHITE)

        elif idx == 53:
            # デイリーチャレンジのランキング(自己ベストの履歴を日付順ではなく
            # フロア到達数の多い順に並べた、ローカル限定のパーソナルランキング)
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 470))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 150])
            draw_text(screen, "Daily Ranking", 300, 170, font, (120, 255, 150))
            draw_text(screen, "Your best floor reached per daily challenge (local record).", 150, 210, fontS, (200, 200, 200))
            drec = load_daily_record()
            entries = list(drec.get("history", []))
            if drec.get("best_floor", 0) > 0 or drec.get("cleared", False):
                entries = entries + [{"date": drec["date"], "best_floor": drec.get("best_floor", 0),
                                       "cleared": drec.get("cleared", False), "today": True}]
            entries.sort(key=lambda r: r.get("best_floor", 0), reverse=True)
            top = entries[:10]
            if not top:
                draw_text(screen, "No daily runs recorded yet.", 150, 260, fontS, (150, 150, 150))
            for i, rec in enumerate(top):
                tag = "  (today)" if rec.get("today") else ""
                cleared_mark = "  [CLEARED]" if rec.get("cleared") else ""
                label = f"{i+1}. {rec['date']}   Floor {rec.get('best_floor', 0)}{cleared_mark}{tag}"
                col = (255, 215, 0) if i == 0 else ((120, 255, 150) if rec.get("today") else WHITE)
                draw_text(screen, label, 150, 250 + i*32, fontS, col)
            draw_text(screen, "[Esc] Back", 340, 590, fontS, WHITE)

        elif idx == 54:
            # 運命の祠: 一発勝負のギャンブル演出(スロットのように候補を高速で切り替えた後、結果を出す)
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Shrine of Fortune", 290, 160, font, (200, 150, 255))
            if tmr <= 24:
                if tmr % 3 == 0:
                    spin_name = random.choice(SHRINE_OUTCOMES)[1]
                    shrine_result_name = spin_name
                draw_text(screen, shrine_result_name, 330, 330, font, (220, 200, 255))
            elif tmr == 25:
                roll_shrine_outcome()
            else:
                good = shrine_result_name in ("JACKPOT!", "Blessing", "Fortune")
                bad = shrine_result_name in ("Curse", "Misfortune")
                col = (255, 215, 0) if good else ((220, 60, 60) if bad else (200, 200, 200))
                draw_text(screen, shrine_result_name, 330, 300, font, col)
                draw_text(screen, shrine_result_desc, 440-fontS.size(shrine_result_desc)[0]//2, 350, fontS, WHITE)
            if tmr > 75:
                idx = 1
                tmr = 0

        elif idx == 61:
            # 犠牲の祭壇: HPを捧げるかどうかをプレイヤーに選ばせる
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Altar of Sacrifice", 280, 160, font, (230, 120, 60))
            draw_text(screen, f"Offer {ALTAR_HP_COST} HP for a chance at a permanent boon?", 130, 260, fontS, WHITE)
            draw_text(screen, f"Current HP: {pl_life}/{pl_lifemax}", 320, 300, fontS, (200, 200, 200))
            draw_text(screen, "[Y] Offer HP    [N] Walk away", 280, 360, fontS, (255, 215, 0))

        elif idx == 62:
            # 犠牲の祭壇: 結果表示
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Altar of Sacrifice", 280, 160, font, (230, 120, 60))
            good = altar_result_name == "Boon"
            bad = altar_result_name == "Backlash"
            col = (255, 215, 0) if good else ((220, 60, 60) if bad else (200, 200, 200))
            draw_text(screen, altar_result_name, 330, 280, font, col)
            draw_text(screen, altar_result_desc, 440 - fontS.size(altar_result_desc)[0]//2, 330, fontS, WHITE)
            if tmr > 60:
                idx = 1
                tmr = 0

        elif idx == 64:
            # さまよう精霊: 3択の祝福から1つを選ばせる
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Wandering Spirit", 270, 130, font, (150, 220, 235))
            draw_text(screen, "Choose one blessing:", 300, 190, fontS, WHITE)
            for i, opt in enumerate(spirit_choice_options):
                y0 = 240 + i * 70
                band = pygame.Surface((520, 56))
                band.set_alpha(120)
                band.fill((40, 70, 80))
                screen.blit(band, [180, y0])
                pygame.draw.rect(screen, (140, 210, 225), [180, y0, 520, 56], 2)
                draw_text(screen, f"[{i+1}] {opt[0]}", 200, y0 + 16, fontS, (255, 215, 0))
            draw_text(screen, "Press 1, 2, or 3 to choose", 290, 460, fontS, WHITE)

        elif idx == 65:
            # 賭博場: 掛け金の階層を選ばせる
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Gambling Den", 300, 110, font, (230, 190, 90))
            draw_text(screen, f"Blaze Gems: {blazegem}", 340, 165, fontS, (200, 200, 200))
            for i, t in enumerate(GAMBLE_TIERS):
                y0 = 210 + i * 70
                band = pygame.Surface((640, 56))
                band.set_alpha(120)
                band.fill((70, 55, 25))
                screen.blit(band, [120, y0])
                pygame.draw.rect(screen, (210, 170, 80), [120, y0, 640, 56], 2)
                label = (f"[{i+1}] {t['label']}: wager {t['cost']} gems, "
                         f"{t['win_chance']}% win, payout x{t['payout_mult']}")
                draw_text(screen, label, 140, y0 + 16, fontS, (255, 215, 0))
            draw_text(screen, "Press 1-3 to bet, or [4]/ESC to walk away", 210, 440, fontS, WHITE)

        elif idx == 66:
            # 賭博場: 結果表示
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(160)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Gambling Den", 300, 160, font, (230, 190, 90))
            good = gamble_result_name == "YOU WIN!"
            col = (255, 215, 0) if good else (220, 60, 60)
            draw_text(screen, gamble_result_name, 330, 280, font, col)
            draw_text(screen, gamble_result_desc, 440 - fontS.size(gamble_result_desc)[0]//2, 330, fontS, WHITE)
            if tmr > 60:
                idx = 1
                tmr = 0

        elif idx == 60:
            # エコーバトル撃破: 小さな永続強化を得て記録メニューに戻る
            if tmr == 1:
                pygame.mixer.music.stop()
                se[5].play()
                pl_lifemax += 25
                pl_life += 25
                pl_str += 8
                pl_def_base += 3
                unlock_achievement("echo_hunter")
                record_stat("echoes_defeated")
                register_echo_boss_defeat(echo_target_floor)
                in_echo_battle = False
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 260))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 280])
            draw_text(screen, "Echo Defeated!", 300, 310, font, (120, 200, 255))
            draw_text(screen, "A faint permanent power lingers...", 200, 360, fontS, WHITE)
            draw_text(screen, "+25 Max HP   +8 STR   +3 DEF", 280, 400, fontS, (120, 255, 150))
            if tmr > 60:
                draw_text(screen, "Press space key", 320, 460, font, BLINK[tmr%6])
            if tmr > 60 and key[K_SPACE] == 1:
                idx = 45
                tmr = 0

        elif idx == 42:
            # スキルツリー画面(ダンジョン画面に重ねて表示)
            # 5本の枝(body/combat/mind/survival/fortune)を横に並べ、tier1→2→3
            # を線でつないでツリーらしく見せる。さらに5枝すべてのtier3を
            # 1レベル以上習得すると、下段中央の奥義"Grandmaster"が解放される。
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(190)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Skill Tree", 60, 18, font, (255, 215, 0))
            draw_text(screen, f"Points: {skill_points}", 400, 24, fontS, (150, 220, 255))

            BRANCH_LABEL = {"body": "Body", "combat": "Combat", "mind": "Mind",
                            "survival": "Survival", "fortune": "Fortune"}
            BOX_W, BOX_H = 150, 145
            COL_GAP = 12
            START_X = 30
            BRANCH_COL_X = {br: START_X + i * (BOX_W + COL_GAP) for i, br in enumerate(SKILL_BRANCH_ORDER)}
            TIER_ROW_Y = {1: 66, 2: 220, 3: 374}
            CAP_W, CAP_H = 260, 118
            CAP_X = 440 - CAP_W // 2
            CAP_Y = 540

            for br in SKILL_BRANCH_ORDER:
                draw_text(screen, BRANCH_LABEL[br], BRANCH_COL_X[br], 50, fontXS, (150, 150, 170))

            # 先に枝の接続線を描いてから箱を上に重ねる(線が箱の裏に隠れるように)
            for sk in SKILLS:
                reqs = skill_requirement_ids(sk)
                if not reqs:
                    continue
                if sk["id"] == "grandmaster":
                    x1, y1 = CAP_X + CAP_W // 2, CAP_Y
                    for r in reqs:
                        rsk = SKILLS_BY_ID[r]
                        x0 = BRANCH_COL_X[rsk["branch"]] + BOX_W // 2
                        y0 = TIER_ROW_Y[rsk["tier"]] + BOX_H
                        col = (255, 215, 0) if skill_levels.get(r, 0) > 0 else (90, 90, 90)
                        pygame.draw.line(screen, col, [x0, y0], [x1, y1], 2)
                else:
                    x = BRANCH_COL_X[sk["branch"]] + BOX_W // 2
                    y0 = TIER_ROW_Y[sk["tier"] - 1] + BOX_H
                    y1 = TIER_ROW_Y[sk["tier"]]
                    col = (120, 255, 150) if skill_levels.get(reqs[0], 0) > 0 else (90, 90, 90)
                    pygame.draw.line(screen, col, [x, y0], [x, y1], 3)

            def box_colors(maxed, locked, affordable):
                if maxed:
                    return (70, 58, 10), (255, 215, 0), (255, 215, 0)
                if locked:
                    return (35, 35, 35), (90, 90, 90), (110, 110, 110)
                if affordable:
                    return (10, 55, 40), (120, 255, 150), WHITE
                return (45, 45, 45), (110, 110, 110), (170, 170, 170)

            def draw_skill_box(sk, x0, y0, w, h, selected):
                lv = skill_levels.get(sk["id"], 0)
                maxed = lv >= sk["max_level"]
                locked = not skill_prereq_met(sk)
                affordable = (not locked) and skill_points >= sk["cost"] and not maxed
                fill_col, border_col, name_col = box_colors(maxed, locked, affordable)
                box = pygame.Surface((w, h))
                box.set_alpha(215)
                box.fill(fill_col)
                screen.blit(box, [x0, y0])
                pygame.draw.rect(screen, border_col, [x0, y0, w, h], 4 if selected else 2)
                icon = SKILL_ICONS.get(sk["id"])
                if icon is not None:
                    isize = 30
                    icon_s = pygame.transform.smoothscale(icon, (isize, isize))
                    if locked:
                        icon_s = icon_s.copy()
                        icon_s.set_alpha(90)
                    screen.blit(icon_s, [x0 + w - isize - 6, y0 + 6])
                draw_text(screen, sk["name"], x0 + 6, y0 + 6, fontXS, name_col)
                if locked:
                    req_names = "+".join(SKILLS_BY_ID[r]["name"] for r in skill_requirement_ids(sk))
                    draw_text(screen, "LOCKED", x0 + 6, y0 + 30, fontXS, (200, 80, 80))
                    draw_text(screen, f"Needs {req_names}", x0 + 6, y0 + 50, fontXS, (150, 150, 150))
                else:
                    lv_txt = "MAX" if maxed else f"Lv {lv}/{sk['max_level']}  {sk['cost']}pt"
                    draw_text(screen, lv_txt, x0 + 6, y0 + 30, fontXS, (200, 200, 200))
                    draw_text(screen, sk["desc"], x0 + 6, y0 + 50, fontXS, (190, 190, 190))
                    cur_txt = skill_current_effect_text(sk["id"], lv)
                    if cur_txt:
                        draw_text(screen, f"Now: {cur_txt}", x0 + 6, y0 + h - 40, fontXS, (120, 255, 150))
                    if not maxed:
                        next_txt = SKILL_NEXT_LEVEL_TEXT[sk["id"]](lv)
                        draw_text(screen, next_txt, x0 + 6, y0 + h - 20, fontXS, (255, 200, 120))

            for sk in SKILLS:
                if sk["id"] == "grandmaster":
                    continue
                x0 = BRANCH_COL_X[sk["branch"]]
                y0 = TIER_ROW_Y[sk["tier"]]
                selected = (not skill_cursor_capstone and SKILL_BRANCH_ORDER[skill_cursor_col] == sk["branch"]
                            and skill_cursor_row + 1 == sk["tier"])
                draw_skill_box(sk, x0, y0, BOX_W, BOX_H, selected)

            draw_skill_box(SKILLS_BY_ID["grandmaster"], CAP_X, CAP_Y, CAP_W, CAP_H, skill_cursor_capstone)

            bottom_y = CAP_Y + CAP_H + 14
            if info_timer > 0 and info_message != "":
                draw_text(screen, info_message, 260, bottom_y, fontS, CYAN)
            draw_text(screen, "Arrows: move   Enter: learn   Esc: back", 210, bottom_y + 26, fontS, WHITE)

        elif idx == 43:
            # プレイ統計(タイトル画面に重ねて表示)
            # STATS_DEFS全項目(+トラップ数)を表示する。項目数が画面に収まらないため、
            # 実績一覧と同じくUp/Downでスクロールするページ表示にする。
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 520))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 150])
            draw_text(screen, "Play Statistics", 300, 163, font, WHITE)
            st = load_stats()
            ach_for_traps = load_achievements()
            rows = [(label, (format_playtime(st.get(key, 0)) if key == "total_playtime_ms" else str(st.get(key, 0))))
                    for key, label in STATS_DEFS]
            rows.append(("Traps triggered", str(ach_for_traps.get("trap_count", 0))))
            total_c = len(rows)
            visible = rows[stats_scroll:stats_scroll + STATS_VISIBLE_ROWS]
            for i, (label, value) in enumerate(visible):
                draw_text(screen, f"{label}: {value}", 130, 190 + i*24, fontS, WHITE)
            if total_c > STATS_VISIBLE_ROWS:
                shown_to = min(stats_scroll + STATS_VISIBLE_ROWS, total_c)
                draw_text(screen, f"{stats_scroll+1}-{shown_to} of {total_c}   [Up/Down] Scroll   [Esc] Back",
                          130, 630, fontS, WHITE)
            else:
                draw_text(screen, "[Esc] Back", 340, 630, fontS, WHITE)

        draw_text(screen, "[S]peed" + str(speed), 740, 40, fontS, WHITE)
        if idx != 1:
            try:
                hold_dir = None
                hold_timer = 0
            except NameError:
                pass
        if screen_shake_timer > 0:
            dx = random.randint(-screen_shake_mag, screen_shake_mag)
            dy = random.randint(-screen_shake_mag, screen_shake_mag)
            if dx or dy:
                screen.scroll(dx, dy)
            screen_shake_timer -= 1
        if achievement_sound_pending:
            se[4].play()
            achievement_sound_pending = False
        if rare_treasure_sound_pending:
            se[4].play()
            rare_treasure_sound_pending = False
        draw_achievement_toast(screen)
        pygame.display.update()
        if idx in (1, 3, 4):
            # 移動をなめらかにするため、探索中だけ高フレームレートで描画する
            # (アイテム取得/被ダメージのポップアップも探索の一部なので同じ扱いにし、
            #  低フレームレートへの急な切り替わりによる「カクつき」を防ぐ)
            # (戦闘演出やメッセージ送りなど他の画面のテンポは変えない)
            fps = max(35, 30 + 5 * int(speed))
        else:
            fps = max(1, 4 + 2 *int(speed))
        playtime_ms_accum += clock.tick(fps)
        
if __name__ == "__main__":
    main()
