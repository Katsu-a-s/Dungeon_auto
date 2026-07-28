import pygame
import sys
import random
import json
import os
import colorsys
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
    "ember": pygame.image.load("image/pet_ember.png"),
}
imgPetRev = {
    "slime": pygame.image.load("image/pet_slime_rev.png"),
    "sprite": pygame.image.load("image/pet_sprite_rev.png"),
    "cat": pygame.image.load("image/pet_cat_rev.png"),
    "ember": pygame.image.load("image/pet_ember_rev.png"),
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

# --- プレイヤーの状態異常(出血) ---
# 毒(pl_poison)は歩数・スキル(Antidote Body)・フロア特性(Festering/Cleansing)
# のいずれからも軽減・短縮できる「対策のある」持続ダメージだったが、どんな
# 手段を積んでも一切軽減できない持続ダメージがまだ無かった。出血(pl_bleed)は
# 「あと何回ダメージが発生するか」という残り回数そのものを直接カウントし、
# 減衰量・ダメージ量のどちらもskill_poison_mult/modifier_poison_decay_mult()の
# 影響を受けない(詳しくはBLOODTHORN_BLEED_TICKS定義のコメントを参照)。
pl_bleed = 0

# --- プレイヤーの状態異常(凍結) ---
# 毒(pl_poison)・出血(pl_bleed)はどちらも「じわじわ削る」持続ダメージ型の
# 状態異常で、ダメージを伴わずプレイヤーの行動そのものを封じるタイプは
# まだ無かった(気絶emy_stunは逆方向、プレイヤーが敵の手番を封じるだけ)。
# 凍結(pl_frozen)は新しいPermafrost Wyrm(typ42)の攻撃が命中すると付与され、
# 1の間だけプレイヤーの次の手番をまるごと1回封じる(付与時にpl_frozen=1を
# 立て、プレイヤーの手番の頭で消費して0に戻す単純な1ターン限定のフラグ。
# emy_stunと対称の実装だが、封じる対象が敵側ではなくプレイヤー側という
# 初めての方向性)。ダメージを伴わないためpl_lifemaxやskill_poison_mult
# などの軽減倍率は一切関係しない。
pl_frozen = 0

# --- 敵の状態異常(毒) ---
# これまで状態異常(毒/呪い)はすべて「敵がプレイヤーに与える」一方通行だった。
# 秘宝Serpent's Fangを手に入れると、プレイヤーの攻撃側からも初めて敵に
# 状態異常を与えられるようになる(emy_poisonはpl_poisonと同じ「スタック値が
# 毎ターン減衰しつつダメージを与える」パターンを敵側に反転させたもの)。
emy_poison = 0
emy_poisoned_this_battle = False  # このバトル中に一度でも敵を毒にしたか(実績判定用)

# --- 敵の状態異常(気絶) ---
# rev202で追加。毒(emy_poison)は「じわじわ削る」持続ダメージ型の状態異常
# だったが、状態異常はこれで2種類目でも仕組みはまだ同じ「毎ターン減衰する
# ダメージ」の一種のみだった。気絶(emy_stun)は初めてダメージを伴わない
# 「敵の行動そのものを封じる」タイプの状態異常で、emy_stun>0の間だけ
# 敵は攻撃せずに1ターン行動不能になる(付与時にemy_stun=1を立て、
# 敵の手番の頭で消費して0に戻す単純な1ターン限定のフラグ)。
emy_stun = 0
emy_stunned_this_battle = False  # このバトル中に一度でも敵を気絶させたか(実績判定用)

# --- 低HP警告 ---
# 残りHPが最大値の一定割合を切ったとき、数値を読まなくても直感的に
# 危険な状態だとわかるよう、画面端を脈打つ赤で縁取る演出を入れる。
LOW_HP_WARNING_RATIO = 0.2

SECOND_WIND_HEAL_RATIO = 0.15  # Second Wind Floorが発動した際、最大HPの何割を回復するか
second_wind_used_this_floor = False  # このフロアで既にSecond Windを消費したか
floor_chest_guarantee_used = False  # Bonanza/Clouded Floorで「このフロア最初の宝箱」の保証を既に消費したか

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

# ステータスパネルのHP数値(HP_MID_WARNING_RATIO/LOW_HP_WARNING_RATIO)と同様、
# 食料も0になる直前だけでなく、さらに深刻な残量になった時点で一段強い赤色の
# 点滅に切り替える中間警告を追加する。従来はオレンジ(30以下)と0の2段階しか
# 無く、「あと何歩で尽きるか」の緊急度がオレンジのまま変わらなかったため、
# 本当に危険な残量(10以下)ではより目立つ赤色で区別できるようにした。
FOOD_CRITICAL_WARNING_THRESHOLD = 10
FOOD_CRITICAL_WARNING_COLOR = (255, 60, 40)

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
# Nightmareは玄人向けの最上位難易度。いきなり選べると初見殺しになるため、
# Hardクリア実績(hard_clear)を解除するまではtoggle_difficulty()の
# サイクルから除外される(実績解除後に初めて選択肢に現れるアンロック制)。
# Abyssはさらにその上、Nightmareクリア実績(nightmare_clear)を解除して
# 初めて選べるようになる最上位難易度。単なる数値の底上げではなく、
# 「死んだらそのオートセーブが消える(続きからやり直せない)」という
# 真のパーマデス制約を持つ、玄人向けモードの決定版。
DIFFICULTY_LIST = ["Easy", "Normal", "Hard", "Nightmare", "Abyss"]
difficulty = "Normal"
# 難易度ボタン/表示テキストの色分け。Easy=安心の緑、Normal=標準の橙、
# Hard=警戒の赤橙、Nightmare=脈打つ深紅、Abyss=漆黒に近い紫
# (パーマデスの緊張感を、他のどの難易度よりも重い色で示す)。
DIFFICULTY_COLORS = {
    "Easy": (70, 190, 90),
    "Normal": (225, 150, 40),
    "Hard": (220, 90, 40),
    "Nightmare": (200, 20, 30),
    "Abyss": (130, 20, 200),
}
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
# 低HP時に画面端が速く脈打つ赤い縁取り警告も、Screen Shake/Screen Flashと
# 同様に光過敏なプレイヤーには負担になりうるため、個別にオフにできる
# ようにする(デフォルトはON)。
low_hp_pulse_enabled = True
settings_cursor = 0  # 設定画面でのカーソル位置(0=BGM, 1=SE, 2=Mute All, 3=Screen Shake, 4=Screen Flash, 5=Low HP Pulse)

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
    "Nightmare": dict(
        # Hardをさらに上回る玄人向けの最上位難易度。歩数ごとの受動回復を
        # 0にする(heal_per_step=0)のが最大の違いで、ポーションや回復床
        # (Blessed Floor等)を計画的に頼らないと立ち行かなくなる。
        enemy_str_mult=1.6, enemy_life_mult=1.6,
        exp_mult=0.65,
        item_bonus=-30,
        growth_mult=0.65,
        pl_lifemax_bonus=-100, pl_str_bonus=-20, pl_def_bonus=-6,
        maze_step_bonus=2,
        food_consume_mult=1.3, heal_per_step=0, starve_dmg=12,
        trap_dmg_mult=2.0, trap_rate_mult=3.0,
        poison_decay_per_step=4,
        minimap_enabled=False, minimap_full_reveal=False, vision_radius_bonus=-3,
    ),
    "Abyss": dict(
        # Nightmareのさらに上。ただし「もっと数値を悪化させる」だけの積み増しでは
        # 玄人にとっての報酬感が無いため、戦闘の脅威(enemy_*_mult)はNightmareより
        # さらに上げつつ、経験値/アイテム運はむしろNightmare未満まで削らずNormal
        # 相当まで戻す(パーマデス自体が最大のリスクなので、進行速度まで
        # 二重に罰する必要は無いという設計)。プレイヤー基礎ステータス・迷路の
        # 厳しさ・食料/罠周りはNightmareと同水準のまま据え置く。
        enemy_str_mult=1.8, enemy_life_mult=1.8,
        exp_mult=1.0,
        item_bonus=10,
        growth_mult=1.0,
        pl_lifemax_bonus=-100, pl_str_bonus=-20, pl_def_bonus=-6,
        maze_step_bonus=2,
        food_consume_mult=1.3, heal_per_step=0, starve_dmg=12,
        trap_dmg_mult=2.0, trap_rate_mult=3.0,
        poison_decay_per_step=4,
        minimap_enabled=False, minimap_full_reveal=False, vision_radius_bonus=-3,
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
hidden_treasure_positions = []
# 隠し壁の奥から出現した宝箱の座標。move_playerで開けた瞬間に
# item_sparkle演出を出すかどうかの判定に使う(通常の宝箱と区別するため)
hidden_chest_cells = set()
pending_bonus_room = False
# 近道(分岐ルート)。隠し壁(10)と同じ「壁を1マスだけ書き換える」方式で
# 見つかる隠し通路だが、見つけた先は宝箱ではなく細い一本道の小さな
# エリア(generate_branch_route_area)で、そこを抜けるとフロアを1つ余分に
# 飛ばして深層へ進める(探索・経験値・宝箱を犠牲にする代わりに、確実な
# 報酬とともに素早く進めるハイリスク・ハイリターンな近道)。
pending_branch_route = False
branch_route_floor_skip_pending = False

# --- Escでの終了確認(ダンジョン中に呼び出せる範囲を拡張) ---
# 以前は素の探索中(idx==1)でEscを押した時しか終了確認(idx=55)を
# 開けなかった。バトルのコマンド選択中(11)・拠点/サンクチュア(28)・
# さまよう精霊の選択中(64)は、いずれもプレイヤーの入力待ちで
# 演出の途中ではない安全なタイミングなので、ここでもEscから終了確認を
# 開けるようにする。キャンセル時は元にいた画面へ戻す必要があるため、
# 呼び出し元のidxをpre_quit_confirm_idxに控えておく。
QUIT_CONFIRM_TRIGGER_IDX = (1, 11, 28, 64)
pre_quit_confirm_idx = 1

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

# --- 反撃(Counter)コマンド ---
# 従来の防御的な選択肢は「防御の薬を消費してDEFを底上げする」Defenseのみで、
# 消費アイテムに頼らずその場で攻防を両立させる純粋な戦術コマンドが無かった。
# Counterは、あえて敵の攻撃を受け止めて被ダメージを軽減しつつ、受けた直後に
# こちらから反撃する「守ってから殴る」新しい駆け引きのコマンド。通常のAttackより
# 反撃の威力は控えめだが、同時に防御も得られるため、被弾を抑えたい場面で
# Attackの代わりに選ぶ理由になる。
COUNTER_DEF_BONUS = 15    # Counter中に追加される防御力(Defense Pillの平均バフ相当)
COUNTER_DMG_MULT = 0.65   # 反撃ダメージは通常攻撃の基礎威力のこの倍率

# --- 逃走(Run)成功率 ---
FLEE_CHANCE_PCT = 60

def flee_chance_pct():
    """基本の逃走成功率にフロア特性(Tranquil Floor)・キャラクター(Vagabond)・
    秘宝(Featherlight Cloak)・護符(Charm of the Wanderer)のボーナスを加える"""
    return min(95, FLEE_CHANCE_PCT + modifier_flee_bonus() + char_params().get("flee_bonus", 0) + relic_flee_bonus() + charm_flee_bonus())

# --- ボスの複数フェーズ演出 ---
# ボスのHPが半分を切ると、1度だけ「激怒」して攻撃力が上がる。
boss_phase2 = False
BOSS_PHASE2_STR_MULT = 1.3

# --- ペット(仲間)システム ---
PET_TYPES = {
    "slime": {"name": "Slime Pal", "desc": "10% chance to assist-attack"},
    "sprite": {"name": "Guardian Sprite", "desc": "+3 DEF while active"},
    "cat":    {"name": "Lucky Cat", "desc": "+5 item find while active"},
    "ember":  {"name": "Ember Whelp", "desc": "+3 STR while active"},
    # Owl(rev186で5種目として追加)。既存4種はDEF/アイテム発見率/STR/
    # 追撃確率のいずれかに関わる効果だったが、会心率(クリティカル発生率)は
    # フロア特性(Fortunate/Unlucky)・キャラクター(Rogue)・秘宝・護符では
    # 既に触れられていたのに、仲間(ペット)の枠からはまだ触れられていなかった。
    # PET_TYPESに新しいキーを足すだけでハッチング(hatch_random_pet)・
    # 吟遊詩人での交換(Traveling Bard)にも自動的に組み込まれる既存の仕組みを
    # そのまま使い、pet_crit_bonusという新しいフィールドで穴を埋めた。
    "owl":    {"name": "Wise Owl", "desc": "+10%pt crit chance while active"},
    # Beetle(rev192で6種目として追加)。既存5種はDEF/アイテム発見率/STR/
    # 追撃確率/会心率のいずれかに関わる効果だったが、被ダメージそのものを
    # 直接軽くする「盾役」の仲間がまだいなかった(sprite/owlのpet_def_bonusは
    # 被ダメージ計算前のDEF値に足されるだけで、モンスターのSTRが高いほど
    # 効果が薄れていく)。新しいpet_dmg_reduction_multフィールドで、DEF値に
    # 依らず被ダメージそのものに一定割合を掛けて減らす、Frostbound Floor
    # (modifier_incoming_dmg_mult)と同じ軸をペット側からも初めて触れるように
    # した。
    "beetle": {"name": "Iron Beetle", "desc": "Incoming damage 8% weaker while active"},
    # Fox(rev209で7種目として追加)。既存6種はDEF/アイテム発見率/STR/
    # 追撃確率/会心率/被ダメージ軽減のいずれかに関わる効果だったが、経験値
    # (EXP)は難易度・スキル・フロア特性(Sparkling/Drab)・キャラクター
    # (Scholar)・秘宝・護符ではすでに触れられていたのに、仲間(ペット)の枠
    # からはまだ触れられていなかった。pet_exp_mult(EXP計算箇所で乗算参照、
    # 他ペットはデフォルト1.0のため無影響)という新しいフィールドで穴を
    # 埋めた。
    "fox":    {"name": "Lucky Fox", "desc": "+15% EXP gained while active"},
}
pet_type = None
pet_def_bonus = 0
pet_item_bonus = 0
pet_str_bonus = 0
pet_slime_assist_chance = 0
pet_crit_bonus = 0.0
pet_dmg_reduction_mult = 1.0
pet_exp_mult = 1.0
# --- 仲間の絆(Pet Bond) ---
# これまで仲間の効果はどのpet_typeでも孵化した瞬間から一切変化しない固定値
# だったため、同じ仲間と長く一緒に潜っても数値上は何も変わらなかった。
# 一定フロア数(PET_BOND_FLOOR_THRESHOLD)を同じ仲間と一緒に生き延びると
# 「絆」が生まれ、効果が一段強くなるようにした。pet_hatched_floorは
# その仲間が孵った時点のフロア番号で、floor - pet_hatched_floorが
# しきい値以上になったかどうかで絆の有無を判定する。
PET_BOND_FLOOR_THRESHOLD = 20
pet_hatched_floor = 0
# 絆が今回のプレイでまだ実績として記録されていないかどうかのフラグ。
# apply_pet_bonuses()は絆が結ばれた後もフロア移動のたびに繰り返し呼ばれるため、
# ここでガードしないと絆達成の実績・累計スタッツが呼び出されるたびに何度も
# 加算されてしまう(セーブ読み込み時は既に絆済みの状態を復元できるよう、
# get_save_data/load側でこのフラグ自体も保存・復元する)。
pet_bond_achieved_this_run = False

def modifier_pet_bond_floor_requirement():
    """Bonded Floorは仲間の卵の出現率、という「絆が始まるまで」の軸には
    既に関わっていたが、絆(Pet Bond)そのものが結ばれるまでの「速さ」に
    関わる特性はまだ無かった。Kinship Floorは、そのフロアにいる間だけ
    絆に必要なフロア数を通常20から半分の10に短縮する新しい軸として
    追加した(floor_modifierは1フロアごとに再抽選されるため、Kinship
    Floorを抜けると通常の20フロアに戻る)。"""
    if floor_modifier == "kinship":
        return max(1, PET_BOND_FLOOR_THRESHOLD // 2)
    return PET_BOND_FLOOR_THRESHOLD

def pet_is_bonded():
    return pet_type is not None and (floor - pet_hatched_floor) >= modifier_pet_bond_floor_requirement()

def apply_pet_bonuses():
    """現在のpet_type・絆の有無に応じてpet_*_bonus/pet_slime_assist_chanceを
    再計算する。仲間が孵った直後・セーブデータ読み込み後・フロア移動のたびに
    呼び出し、絆のしきい値を跨いだ瞬間に効果が自動的に強化されるようにする。
    絆が初めて形成された瞬間だけ実績・累計スタッツを記録する(この関数は絆が
    結ばれた後もフロア移動のたびに繰り返し呼ばれるため、pet_bond_achieved_this_run
    で二重加算を防ぐ)。"""
    global pet_def_bonus, pet_item_bonus, pet_str_bonus, pet_slime_assist_chance, pet_crit_bonus
    global pet_bond_achieved_this_run, pet_dmg_reduction_mult, pet_exp_mult
    bonded = pet_is_bonded()
    pet_def_bonus = (5 if bonded else 3) if pet_type == "sprite" else 0
    pet_item_bonus = (8 if bonded else 5) if pet_type == "cat" else 0
    pet_str_bonus = (5 if bonded else 3) if pet_type == "ember" else 0
    pet_slime_assist_chance = (15 if bonded else 10) if pet_type == "slime" else 0
    pet_crit_bonus = (0.15 if bonded else 0.10) if pet_type == "owl" else 0.0
    pet_dmg_reduction_mult = (0.88 if bonded else 0.92) if pet_type == "beetle" else 1.0
    pet_exp_mult = (1.20 if bonded else 1.15) if pet_type == "fox" else 1.0
    if bonded and not pet_bond_achieved_this_run:
        pet_bond_achieved_this_run = True
        record_stat("pet_bonds_formed")
        unlock_achievement("pet_bond_formed")
        if load_stats().get("pet_bonds_formed", 0) >= 5:
            unlock_achievement("bond_keeper")

def hatch_random_pet():
    """卵を拾った瞬間にランダムな仲間が孵る。既に仲間がいる場合は何もしない
    (呼び出し側でポーション等の代替報酬を渡す)"""
    global pet_type, pet_hatched_floor, pet_bond_achieved_this_run
    if pet_type is not None:
        return False
    pet_type = random.choice(list(PET_TYPES.keys()))
    pet_hatched_floor = floor
    pet_bond_achieved_this_run = False
    apply_pet_bonuses()
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
    """Easy→Normal→Hard→(Nightmare)→(Abyss)→Easyの順に切り替える。Nightmareは
    hard_clear実績を、Abyssはさらにnightmare_clear実績を解除するまで
    サイクルから除外し、いきなり選べて面食らわないようにする
    (それぞれ一段下の難易度をクリアして初めて選択肢に現れるアンロック制)。"""
    global difficulty, info_message, info_timer
    achv = load_achievements()
    nightmare_unlocked = achv.get("hard_clear", False)
    abyss_unlocked = achv.get("nightmare_clear", False)
    cycle = [d for d in DIFFICULTY_LIST
             if (d != "Nightmare" or nightmare_unlocked)
             and (d != "Abyss" or abyss_unlocked)]
    di = (cycle.index(difficulty) + 1) % len(cycle) if difficulty in cycle else 0
    difficulty = cycle[di]
    # 【UI改善】これまでNightmare/Abyssは、実績を解除するまでサイクルに
    # 何の説明も無く現れなかった(「なぜHardの次がEasyに戻るのか」が
    # プレイヤーに伝わらなかった)。今アンロック済みの中で一番上の難易度を
    # 選んだ瞬間だけ、次の難易度をどうすれば解放できるかヒント表示する。
    if difficulty == "Hard" and not nightmare_unlocked:
        info_message = "Clear all stages on Hard to unlock Nightmare!"
        info_timer = 90
    elif difficulty == "Nightmare" and not abyss_unlocked:
        info_message = "Clear all stages on Nightmare to unlock Abyss (permadeath)!"
        info_timer = 90

def start_hidden_stage_challenge():
    """タイトル画面から隠しボスへ挑戦する処理(キーボード/マウス共通)。
    全3ステージクリア(game_clear実績)が条件。"""
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_def_buff, def_pill
    global food, food_acc, potion, blazegem, pl_poison, pl_bleed, pl_frozen, pl_charge, battle_took_damage
    global in_boss_battle, in_hidden_stage, floor, idx, tmr, in_endless_mode
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
    pl_bleed = 0
    pl_frozen = 0
    pl_charge = False
    battle_took_damage = False
    in_boss_battle = True
    in_hidden_stage = True
    in_endless_mode = False
    floor = HIDDEN_FLOOR
    init_hidden_boss_battle()
    init_message()
    pygame.mixer.music.load("sound/natsuyasuminotanken.mp3")
    pygame.mixer.music.play(-1)
    idx = 40
    tmr = 0

def start_true_hidden_stage_challenge():
    """タイトル画面から「真の隠しボス」??? The Voidcrownedへ挑戦する処理。
    ??? The Unboundを通算TRUE_HIDDEN_UNLOCK_DEFEATS回倒していることが条件
    (呼び出し側でも確認するが、念のため関数内でも確認する)。"""
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_def_buff, def_pill
    global food, food_acc, potion, blazegem, pl_poison, pl_bleed, pl_frozen, pl_charge, battle_took_damage
    global in_boss_battle, in_hidden_stage, in_true_hidden_stage, floor, idx, tmr, in_endless_mode
    if load_stats().get("hidden_boss_defeats", 0) < TRUE_HIDDEN_UNLOCK_DEFEATS:
        return
    dp = diff_params()
    cp = char_params()
    if pl_lifemax <= 0:
        # このセッションでまだキャラクターを作っていない場合、
        # 裏ボス挑戦用にやや強めのステータスで即座に用意する(既存の
        # start_hidden_stage_challengeと同じ即席ステータス)
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
    pl_bleed = 0
    pl_frozen = 0
    pl_charge = False
    battle_took_damage = False
    in_boss_battle = True
    in_hidden_stage = True
    in_true_hidden_stage = True
    in_endless_mode = False
    floor = TRUE_HIDDEN_FLOOR
    init_true_hidden_boss_battle()
    init_message()
    pygame.mixer.music.load("sound/natsuyasuminotanken.mp3")
    pygame.mixer.music.play(-1)
    idx = 40
    tmr = 0

def start_arena_challenge():
    """タイトル画面から闘技場(Arena of Trials)へ挑戦する処理。全クリア等の
    条件は無く、いつでも挑戦できる。現在のセーブキャラのステータスをそのまま
    持ち込む(start_hidden_stage_challengeと同じ、未作成時の即席ステータス)。"""
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_def_buff, def_pill
    global food, food_acc, potion, blazegem, pl_poison, pl_bleed, pl_frozen, pl_charge, battle_took_damage
    global in_boss_battle, in_hidden_stage, in_arena_mode, arena_round, floor, idx, tmr, in_endless_mode
    dp = diff_params()
    cp = char_params()
    if pl_lifemax <= 0:
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
    # 直前にダンジョンや別の闘技場ランで力尽きた直後(pl_life==0)のまま
    # タイトルから即座に再挑戦されると、1ターン目から即敗北してしまう。
    # 闘技場は「新しい挑戦の始まり」として、いつ呼んでも必ず満タンで
    # 開始できるようにする。
    pl_life = pl_lifemax
    pl_poison = 0
    pl_bleed = 0
    pl_frozen = 0
    pl_charge = False
    battle_took_damage = False
    in_boss_battle = False
    in_hidden_stage = False
    in_arena_mode = True
    arena_round = 1
    in_endless_mode = False
    record_stat("arena_runs")
    floor = ARENA_BASE_FLOOR
    init_battle()
    init_message()
    pygame.mixer.music.load("sound/Tolerance_Deviation.mp3")
    pygame.mixer.music.play(-1)
    idx = 72
    tmr = 0

def start_boss_rush():
    """タイトル画面から挑む新しいサイドコンテンツ「ボスラッシュ」。全9体の
    ステージボス(フロア10/20/.../90)を、間に軽い回復を挟みながら順番に
    連戦する。現在のセーブキャラのステータス(未作成なら他の即席コンテンツと
    同じ即席ステータス)を持ち込む。ダンジョン進行用のグローバルfloorは
    ボスごとの見た目・強さの計算にそのまま使い、init_boss_battle()を
    闘技場のinit_battle()と同じ要領で使い回す(通常のボス戦と全く同じ
    強さ・見た目になる)。"""
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_def_buff, def_pill
    global food, food_acc, potion, blazegem, pl_poison, pl_bleed, pl_frozen, pl_charge, battle_took_damage
    global in_boss_battle, in_hidden_stage, in_arena_mode, in_boss_rush_mode, boss_rush_index
    global floor, idx, tmr, in_endless_mode
    dp = diff_params()
    cp = char_params()
    if pl_lifemax <= 0:
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
    pl_life = pl_lifemax
    pl_poison = 0
    pl_bleed = 0
    pl_frozen = 0
    pl_charge = False
    battle_took_damage = False
    in_boss_battle = True
    in_hidden_stage = False
    in_arena_mode = False
    in_boss_rush_mode = True
    boss_rush_index = 0
    in_endless_mode = False
    record_stat("boss_rush_runs")
    floor = BOSS_RUSH_FLOORS[boss_rush_index]
    init_boss_battle()
    init_message()
    pygame.mixer.music.load("sound/Tolerance_Deviation.mp3")
    pygame.mixer.music.play(-1)
    idx = 76
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
    """デイリーチャレンジの結果を記録する。これまでデイリーチャレンジは
    daily.json内の「今日の記録」だけで完結しており、実績システムと
    一切連動していなかった(全127種の実績のどれもデイリーに触れていない
    穴だった)。今日まだクリアしていなかった場合に限り、通算のクリア日数
    (stats.json、日をまたいでも失われない永続記録)を1つ進める。"""
    data = load_daily_record()
    if floor_reached > data.get("best_floor", 0):
        data["best_floor"] = floor_reached
    if cleared and not data.get("cleared", False):
        data["cleared"] = True
        unlock_achievement("daily_challenger")
        record_stat("daily_challenges_cleared")
        if load_stats().get("daily_challenges_cleared", 0) >= 7:
            unlock_achievement("daily_devotee")
    elif cleared:
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
HIDDEN_BOSS_IMAGE = "enemy_hidden_boss.png"
in_hidden_stage = False

# --- 真の隠しステージ(??? The Voidcrowned) ---
# ??? The Unbound(既存の隠しボス)を通算TRUE_HIDDEN_UNLOCK_DEFEATS回倒すと
# タイトル画面に挑戦の入り口が現れる、隠しステージのさらに奥にいる一体。
# これまで隠しステージは倒して終わりの一発ネタで、真エンディングを見た後の
# 目標が何も無かった。既存の隠しボス戦の仕組み(一発勝負・専用BGM)をそのまま
# 流用し、挑戦条件と強さだけを積み増した「隠しボスのそのまた奥」を追加した。
TRUE_HIDDEN_FLOOR = HIDDEN_FLOOR + 1
TRUE_HIDDEN_UNLOCK_DEFEATS = 3
TRUE_HIDDEN_BOSS_TINT = (150, 40, 190)  # Unboundよりもさらに深い紫(禍々しさを強調)
in_true_hidden_stage = False

# --- 闘技場(Arena of Trials) ---
# タイトル画面からいつでも挑戦できる、連戦サバイバル形式の新しいサイドコンテンツ。
# 隠しステージ/真の隠しステージが「全クリア後にしか挑めない一発勝負のご褒美戦」
# だったのに対し、こちらは全クリア前のプレイヤーでも遊べる、腕試しの場として
# 新設した。現在のセーブキャラのステータス(未作成なら隠しステージ挑戦と同じ
# 即席ステータス)を持ち込み、ラウンドを重ねるごとに敵を強くしながら
# 通常のダンジョン敵(init_battle()の抽選)と連戦する。1ラウンド倒すごとに
# 「次のラウンドに挑む(ハイリスク)」か「ここで退いて報酬を持ち帰る
# (ローリスク)」かを選べる、いわゆる「攻めるか、退くか」のプッシュユア
# ラック型の駆け引きを持つ。
ARENA_BASE_FLOOR = 3      # ラウンド1で敵を生成する際に使う仮想フロア値(init_battle()にそのまま渡す)
ARENA_FLOOR_STEP = 4      # ラウンドが1つ進むごとに仮想フロアを何段上げるか
ARENA_HEAL_PCT_PER_ROUND = 0.12  # ラウンドクリアごとに回復する最大HP割合
in_arena_mode = False
arena_round = 1

# --- ボスラッシュ(Boss Rush) ---
# rev203の闘技場(Arena of Trials)以来、プレイの幅を広げる新しいゲームモードが
# しばらく追加されていなかったため、今回新設した新しいサイドコンテンツ。
# 闘技場が「同じ雑魚敵をどんどん強くしながら削る持久戦」で、退くか攻めるかの
# 駆け引きを持つのに対し、ボスラッシュは全9体のステージボス(フロア
# 10/20/.../90)を、間に軽い回復を挟みながら一体ずつ連戦する「格上の敵と
# 立て続けに戦う瞬発力型」の挑戦として性格を分けた。押し引きの選択は無く、
# 全員倒すか、力尽きるまで進むだけのシンプルな構成。
BOSS_RUSH_FLOORS = list(range(BOSS_FLOOR_INTERVAL, MAX_FLOOR + 1, BOSS_FLOOR_INTERVAL))  # [10, 20, ..., 90] 全9体を順番に連戦する
BOSS_RUSH_HEAL_PCT_PER_BOSS = 0.35  # 1体倒すごとに回復する最大HP割合(相手が毎回ボス級のため、
                                    # 闘技場のARENA_HEAL_PCT_PER_ROUNDより高めに設定している)
in_boss_rush_mode = False
boss_rush_index = 0  # 次に挑むBOSS_RUSH_FLOORSのインデックス(0-8)

# --- エンドレス・ディープス(周回後の無限探索モード) ---
# 全3ステージクリア(game_clear実績)後、タイトル画面から挑戦できる新しいゲーム
# モード。通常のダンジョン生成(make_dungeon/put_event)をそのまま流用し、
# フロア91以降も終わりなく潜り続けられる。current_stage()がSTAGE_COUNTで
# 頭打ちになる・is_boss_floor()が10階ごとの剰余判定のみで上限が無い、といった
# 既存のステージ計算がもともとMAX_FLOORを超えるフロア番号にも対応できる作りに
# なっていたため、通常の周回ロジックにほぼ手を入れずに「終わらない周回」を
# 追加できた(敵の強さもfloor値に比例する既存の式でそのまま際限なく上昇する)。
ENDLESS_START_FLOOR = MAX_FLOOR + 1
in_endless_mode = False

# 【新ゲームシステム】エンドレス・ディープス「深淵の祝福(Depths Blessing)」
# これまでエンドレス・ディープスは、フロア100/150到達の実績(endless_delver/
# endless_legend)を除けば潜るほど敵が強くなるだけで、長い潜行そのものに
# 報酬が無かった。25階進むごと(100/125/150/175...と、既存の実績しきい値
# 100/150ともきれいに重なる間隔)に、永続的な小さなステータス上昇を
# 一度だけ贈ることで、エンドレス・ディープスに「潜り続ける理由」を追加した。
ENDLESS_BLESSING_INTERVAL = 25
ENDLESS_BLESSING_STR = 2
ENDLESS_BLESSING_DEF = 2
endless_blessing_floor = 0  # 直近で祝福を受け取ったフロア番号(二重付与を防ぐ)

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
    # 【UI改善】各特性の効果説明(desc)に、これまで「much more」「far more」
    # などの曖昧な表現だった箇所を、実際の数値(modifier_*()の戻り値)に
    # 揃えて明記した。効果の大きさが実績一覧やヘルプと同じように一目で
    # わかるように、新規追加のSnared Floorも含めて全36種類で表記を統一している。
    "foggy":     {"name": "Foggy Floor",     "desc": "Vision range is 2 tiles smaller here",      "color": (110, 110, 150)},
    "bountiful": {"name": "Bountiful Floor",  "desc": "+20%pt item find rate here",     "color": (255, 215, 0)},
    "scarce":    {"name": "Scarce Floor",     "desc": "-20%pt item find rate here",     "color": (120, 110, 95)},
    "quiet":     {"name": "Quiet Floor",      "desc": "Traps are 70% less common here",            "color": (120, 200, 150)},
    "windy":     {"name": "Windy Floor",      "desc": "+30% movement speed here",        "color": (150, 210, 255)},
    "sluggish":  {"name": "Sluggish Floor",  "desc": "-30% movement speed here", "color": (90, 80, 70)},
    "chilly":    {"name": "Chilly Floor",     "desc": "Food drains 50% faster here",     "color": (120, 170, 220)},
    "blessed":   {"name": "Blessed Floor",    "desc": "Passive healing is doubled here",    "color": (255, 235, 170)},
    "rocky":     {"name": "Rocky Floor",      "desc": "+3 DEF here, but you move slower", "color": (120, 100, 80)},
    "toxic":     {"name": "Toxic Floor",      "desc": "+25%pt poison chance here",  "color": (120, 170, 60)},
    "sparkling": {"name": "Sparkling Floor",  "desc": "+30% EXP gained here",   "color": (255, 180, 240)},
    "serene":    {"name": "Serene Floor",     "desc": "Poison cannot affect you here", "color": (170, 255, 220)},
    "fortunate": {"name": "Fortunate Floor",  "desc": "+15%pt critical hit chance here", "color": (255, 200, 80)},
    "resonant":  {"name": "Resonant Floor",   "desc": "Combo damage grows 50% faster per stack here", "color": (255, 120, 220)},
    "frostbound": {"name": "Frostbound Floor", "desc": "Enemy attack damage is 15% weaker here", "color": (140, 210, 255)},
    "empowered": {"name": "Empowered Floor",  "desc": "+15% attack damage here",  "color": (255, 90, 60)},
    "verdant":   {"name": "Verdant Floor",    "desc": "Food drains 40% slower here",       "color": (100, 200, 90)},
    "tranquil":  {"name": "Tranquil Floor",   "desc": "+20%pt flee success rate here", "color": (180, 230, 210)},
    "cursed":    {"name": "Cursed Floor",     "desc": "+15% enemy damage, +25%pt item find here", "color": (170, 30, 110)},
    "veiled":    {"name": "Veiled Floor",     "desc": "50% fewer monster encounters here",      "color": (95, 65, 135)},
    "clear":     {"name": "Clear Floor",      "desc": "The full map is revealed here", "color": (200, 235, 255)},
    "elite_grounds": {"name": "Elite Grounds", "desc": "+12%pt Elite monster chance here", "color": (255, 150, 30)},
    "opulent":   {"name": "Opulent Floor",   "desc": "Treasure chest weight is doubled here", "color": (255, 195, 60)},
    "radiant":   {"name": "Radiant Floor",   "desc": "Critical hits deal x2.5 damage here (vs. x2)", "color": (255, 245, 180)},
    "merciful":  {"name": "Merciful Floor",  "desc": "Trap damage is 30% weaker here",     "color": (200, 255, 210)},
    "warded":    {"name": "Warded Floor",    "desc": "Curse tiles have no effect here", "color": (200, 220, 255)},
    "bazaar":    {"name": "Bazaar Floor",    "desc": "Merchant prices are 25% cheaper here", "color": (255, 225, 140)},
    "genuine":   {"name": "Genuine Floor",   "desc": "Treasure chests are never Mimics here", "color": (210, 240, 200)},
    "fertile":   {"name": "Fertile Floor",   "desc": "Food found here restores 50% more", "color": (160, 220, 90)},
    "volatile":  {"name": "Volatile Floor",  "desc": "Blaze Gems deal 50% more damage here", "color": (255, 110, 40)},
    "torchlit":  {"name": "Torchlit Floor",  "desc": "Vision range is 2 tiles larger here",         "color": (255, 200, 120)},
    "peaceful":  {"name": "Peaceful Floor",  "desc": "No Elite monsters appear here", "color": (180, 255, 200)},
    "bastion":   {"name": "Bastion Floor",   "desc": "Defense Pills grant 50% more DEF here", "color": (150, 190, 255)},
    "frail":     {"name": "Frail Floor",     "desc": "Monsters here have 20% less HP", "color": (190, 205, 175)},
    "swarming":  {"name": "Swarming Floor",  "desc": "+60% monster encounters here", "color": (150, 40, 60)},
    "weakened":  {"name": "Weakened Floor",  "desc": "-15% attack damage here", "color": (140, 140, 150)},
    "barren":    {"name": "Barren Floor",    "desc": "Passive healing is halved here", "color": (140, 120, 100)},
    "hardened":  {"name": "Hardened Floor",  "desc": "Monsters here have 20% more HP", "color": (130, 140, 160)},
    "snared":    {"name": "Snared Floor",    "desc": "-20%pt flee success rate here", "color": (90, 60, 50)},
    "hazardous": {"name": "Hazardous Floor", "desc": "Traps are 100% more common here", "color": (210, 90, 20)},
    "ruinous":   {"name": "Ruinous Floor",   "desc": "Trap damage is 30% stronger here", "color": (150, 40, 20)},
    "meager":    {"name": "Meager Floor",    "desc": "Treasure chest weight is halved here", "color": (110, 100, 90)},
    "drab":      {"name": "Drab Floor",      "desc": "-20% EXP gained here", "color": (100, 95, 90)},
    "unlucky":   {"name": "Unlucky Floor",   "desc": "-15%pt critical hit chance here", "color": (80, 75, 100)},
    "withered":  {"name": "Withered Floor",  "desc": "Food found here restores 30% less", "color": (110, 95, 60)},
    "costly":    {"name": "Costly Floor",    "desc": "Merchant prices are 25% pricier here", "color": (150, 110, 40)},
    "damp":      {"name": "Damp Floor",      "desc": "Blaze Gems deal 30% less damage here", "color": (80, 110, 130)},
    "dim":       {"name": "Dim Floor",       "desc": "Critical hits deal x1.5 damage here (vs. x2)", "color": (90, 85, 100)},
    "corroded":  {"name": "Corroded Floor",  "desc": "Defense Pills grant 25% less DEF here", "color": (110, 130, 95)},
    "muffled":   {"name": "Muffled Floor",   "desc": "Combo damage grows 50% slower per stack here", "color": (200, 140, 190)},
    "antiseptic": {"name": "Antiseptic Floor", "desc": "-15%pt poison chance here", "color": (190, 230, 190)},
    "frenzied":  {"name": "Frenzied Floor",  "desc": "-3 DEF here, but you move faster", "color": (200, 60, 50)},
    "venomous":  {"name": "Venomous Floor",  "desc": "Poison-capable enemies always poison you here", "color": (110, 200, 40)},
    "focused":   {"name": "Focused Floor",   "desc": "Focus attacks deal x2.0 damage here (vs. x1.5)", "color": (255, 170, 60)},
    "vampiric":  {"name": "Vampiric Floor",  "desc": "Attacks heal you for 15% of damage dealt here", "color": (180, 20, 60)},
    "sanctuary": {"name": "Sanctuary Floor", "desc": "Defeating an enemy fully restores your HP here", "color": (150, 255, 190)},
    "echoing":   {"name": "Echoing Floor",   "desc": "Attacks have a 25% chance to strike again here", "color": (190, 140, 255)},
    "overcharged": {"name": "Overcharged Floor", "desc": "Ultimate needs only 3 combo here (vs. 5)", "color": (255, 60, 180)},
    "treacherous": {"name": "Treacherous Floor", "desc": "Treasure chests are twice as likely to be Mimics here", "color": (130, 45, 35)},
    # 既存のフロア特性はどれも毒の「発生確率」(toxic/venomous/antiseptic/serene)
    # にしか関わっておらず、一度かかった毒が「どれくらい長引くか」という持続時間側の
    # 軸に触れる特性が無かった。Festering Floor/Cleansing Floorはpoison_decay_per_step
    # (歩数ごとに毒がどれだけ減るか)を直接変化させる、新しい方向性の特性として追加した。
    "festering": {"name": "Festering Floor", "desc": "Poison drains 50% slower here", "color": (90, 130, 40)},
    "cleansing": {"name": "Cleansing Floor", "desc": "Poison drains 50% faster here", "color": (200, 255, 230)},
    # 特定のバトルコマンド専用のフロア特性は、Focused Floor(Focus専用)・
    # Overcharged Floor(Ultimate専用)に続いて3つ目。新しく追加したCounter
    # コマンドの被ダメージ軽減・反撃ダメージを両方1.5倍にする、コマンドごとに
    # 得意なフロアを作るという方向性を踏襲した特性。
    "bulwark":   {"name": "Bulwark Floor",   "desc": "Counter mitigates & retaliates 50% harder here", "color": (80, 140, 220)},
    # これまでのフロア特性はボス戦のフェーズ2(激怒、HP50%で発動固定)自体には
    # 一切触れておらず、ボス・エコーバトルという最も緊張感のある戦闘の「山場が
    # いつ来るか」を左右する特性が無かった。Simmering Floorはそのフェーズ2の
    # 発動しきい値をHP65%まで前倒しする、ボス/エコーバトル専用の新しい方向性の
    # 特性として追加した(通常戦闘には影響しない)。
    "simmering": {"name": "Simmering Floor", "desc": "Bosses/Echo Battles enrage at 65% HP here (vs. 50%)", "color": (255, 120, 60)},
    # 既存のBountiful/Scarce/Cursed等は宝箱の「中身の質」(item_bonus)に関わる
    # 特性、Fertile/Witheredは食料の「量」に関わる特性だったが、宝箱がまれに
    # 化ける仲間(ペット)の卵の出現率そのものに関わる特性は今まで無かった。
    # 新しい軸として、ペットの卵の出現確率(通常3%)を2倍にするFortune寄りの
    # 「当たり」特性を追加した(まだ仲間がいない場合のみ意味を持つ)。
    "bonded":    {"name": "Bonded Floor",    "desc": "Pet egg chance is doubled here (~6%)", "color": (255, 170, 190)},
    # 既存のSanctuary Floor(敵撃破時に全回復)・Vampiric Floor(攻撃ヒット時に
    # 回復)はどちらも「プレイヤーが攻撃した結果」が引き金の回復だった。
    # Second Wind Floorは、そのフロアで初めてHPが低HP警告と同じ20%を切った
    # 瞬間に一度だけ最大HPの15%を回復する、「体力がピンチに陥ったこと自体」が
    # 引き金になる今までに無かった発動条件の安全網として追加した。
    "second_wind": {"name": "Second Wind Floor", "desc": "First time HP drops below 20% here, instantly heal 15% max HP (once)", "color": (150, 255, 190)},
    # 既存のBonded Floorはペットの卵の出現率(絆が始まるまで)の軸にしか
    # 関わっておらず、絆(Pet Bond)そのものが結ばれるまでの「速さ」に関わる
    # 特性が無かった。Kinship Floorは、そのフロアにいる間だけ絆に必要な
    # フロア数を半分(20→10)に短縮する新しい軸として追加した。
    "kinship":   {"name": "Kinship Floor",   "desc": "Pet Bond forms in half the floors here (10 vs. 20)", "color": (255, 200, 220)},
    # これまでのBountiful/Scarce/Opulent/Meager等は宝箱の「質」に関わる特性
    # だったが、どれも確率(item_bonus/重み)をずらすだけで、実際に何が出るかは
    # 依然として運任せだった。Bonanza Floor/Clouded Floorは、そのフロアで
    # 最初に開けた宝箱の中身を「確率ではなく確定」で決めるという、今までに
    # 無かった新しい軸として追加した(2個目以降の宝箱は通常通り確率で決まる)。
    "bonanza":   {"name": "Bonanza Floor",   "desc": "The first treasure chest here is guaranteed to be rare", "color": (255, 225, 90)},
    "clouded":   {"name": "Clouded Floor",   "desc": "The first treasure chest here is guaranteed to be a plain Potion", "color": (130, 125, 115)},
    # 護符の祠(Charm Shrine)は通常フロア6以降に約10%の確率でしか出現しない
    # ため、護符をまだ持っていないプレイヤーが何十階も見つけられずにいる
    # ことがあった。Bonanza/Clouded Floorと同じ「確率ではなく確定にする」軸を、
    # 宝箱の中身ではなく特殊な部屋そのものの出現に適用した新しい特性として、
    # このフロアでは護符の祠が必ず1つ出現するようにした。
    "charmed":   {"name": "Charmed Floor",   "desc": "A Charm Shrine is guaranteed to appear here", "color": (200, 160, 255)},
    # Focused Floor(Focus専用)・Overcharged Floor(Ultimateのコンボ必要数)・
    # Bulwark Floor(Counter専用)と、バトルコマンドごとに得意なフロアはすでに
    # 揃っていたが、Overcharged Floorは必殺技(Ultimate)の「発動しやすさ」
    # (コンボ必要数)にしか関わっておらず、Ultimate自体の「威力」を伸ばす
    # 特性はまだ無かった。Focused FloorがFocusの一撃倍率を伸ばすのと同じ
    # 考え方を、必殺技の威力そのものに新しく適用した。
    "devastation": {"name": "Devastation Floor", "desc": "Ultimate attacks deal 25% more damage here", "color": (255, 90, 190)},
    # 既存のフロア特性は宝箱・遭遇率・取引コストなど様々な軸に関わってきたが、
    # 拠点(サンクチュア)でポーションを賭けて増やすギャンブル(Wキー)の勝率だけは
    # 常に50%固定で、フロア特性から一切影響を受けない数少ない一点だった。この
    # フロアではその勝率を65%まで引き上げる、賭け事運という新しい軸を追加した。
    "wagered":   {"name": "Wagered Floor",   "desc": "Sanctuary potion gamble win chance is 65% here (vs. 50%)", "color": (255, 205, 60)},
    # 守護者の像(Guardian Statue)の試練は、statue_str_threshold(floor)で決まる
    # 必要STRを満たすかどうかの一発判定で、これまでどのフロア特性からも
    # 一切影響を受けない数少ない一点だった(Charmed/Wagered Floorが埋めてきた
    # 「フロア特性が及んでいない一点」の穴を、今回は守護者の像に適用した)。
    # このフロアでは必要STRが20下がり、永続的なSTR+15という報酬にわずかに
    # 手が届きやすくなる「当たり」特性として追加した。
    "hallowed":  {"name": "Hallowed Floor",  "desc": "Guardian Statue trials require 20 less STR here", "color": (255, 245, 210)},
    # 秘宝(Relic)はボス撃破時にRELIC_DROP_CHANCE(30%固定)で1つ手に入るが、
    # これまでどのフロア特性からも一切影響を受けない数少ない一点だった
    # (Charmed/Wagered/Hallowed Floorが埋めてきた「フロア特性が及んでいない
    # 一点」の穴を、今回は秘宝ドロップに適用した)。このフロアで倒したボスは
    # ドロップ率が15%pt上乗せされ、未所持の秘宝に手が届きやすくなる。
    "fated":     {"name": "Fated Floor",     "desc": "+15%pt Relic drop chance from bosses here", "color": (230, 195, 255)},
    # Simmering Floorはボス・エコーバトルのフェーズ2(激怒)発動しきい値をHP65%まで
    # 前倒しする「当たり(緊張感が増す)」方向の特性だったが、その逆に発動を
    # 遅らせて激怒状態と戦う時間を短くする「はずれ寄り(気楽に戦える)」特性が
    # 無かった。Frail⇔Hardenedと同じ「既存修飾子の符号を反転させる」パターンで、
    # modifier_boss_phase2_threshold()にHP35%の分岐を1つ足すだけで対になる特性を
    # 安全に追加した。
    "placid":    {"name": "Placid Floor",    "desc": "Bosses/Echo Battles enrage at 35% HP here (vs. 50%)", "color": (140, 205, 190)},
    # 灯火の鍛冶場(Ember Forge)は所持しているブレイズジェムを永続STRに変える
    # 仕掛けだが、EMBER_FORGE_STR_PER_GEM(ジェム1個につき+3STR)は固定値で、
    # これまでどのフロア特性からも一切影響を受けない数少ない一点だった(Charmed/
    # Wagered/Hallowed/Fated Floorが埋めてきた「フロア特性が及んでいない一点」の
    # 穴を、今回は灯火の鍛冶場の変換レートに適用した)。このフロアの鍛冶場は
    # 変換レートが1.5倍になり、同じ数のブレイズジェムでより多くの永続STRが手に入る。
    "molten":    {"name": "Molten Floor",    "desc": "Ember Forge STR conversion is x1.5 here", "color": (255, 140, 70)},
    # 隠し壁(carve_hidden_room)の奥がもう1マス深く続き、宝箱2つの「秘密の
    # 宝物庫(Secret Vault)」になる確率は、フロア8以降ずっと15%固定で、
    # これまでどのフロア特性からも一切影響を受けない数少ない一点だった
    # (Charmed/Wagered/Hallowed/Fated/Molten Floorが埋めてきた「フロア特性が
    # 及んでいない一点」の穴を、今回は秘密の宝物庫の出現確率に適用した)。
    # このフロアでは確率が30%(2倍)まで引き上がり、隠し部屋を見つけた時に
    # 豪華な宝物庫だった時の嬉しさに出会いやすくなる。
    "buried":    {"name": "Buried Floor",    "desc": "Secret Vault chance is doubled here (15% -> 30%)", "color": (150, 110, 60)},
    # rev198で新設した秘宝Serpent's Fang(攻撃が敵を毒にする)は、フロア特性
    # からは一切影響を受けない状態のまま追加すると、Charmed/Wagered/Hallowed/
    # Fated/Molten/Buried Floorが埋めてきた「フロア特性が及んでいない一点」の
    # 穴が新設した瞬間からすぐにできてしまう。今回は新システム導入と同じrevで
    # その穴を埋め、Serpent's Fangの毒付与確率を+20%pt上乗せする特性を用意した。
    "venomfang": {"name": "Venomfang Floor", "desc": "Serpent's Fang poison chance +20%pt here", "color": (140, 200, 90)},
    # rev202で新設した秘宝Thunderclap Idol(攻撃が敵を気絶させる)も、
    # venomfangの時と同じく新システム導入と同じrevでフロア特性側の穴を
    # 埋めておく。気絶付与確率を+15%pt上乗せする専用の特性。
    "stormbound": {"name": "Stormbound Floor", "desc": "Thunderclap Idol stun chance +15%pt here", "color": (235, 210, 90)},
    # 灯火の鍛冶場(Ember Forge)は、Molten Floorのおかげで変換レート
    # (STR化効率)には既に触れられていたが、その鍛冶場そのものが出現する
    # かどうか(通常floor>=6で12%固定)には、Charmed Floorが護符の祠に
    # 適用したのと同じ「確率ではなく確定にする」軸がまだ及んでいなかった。
    # このフロアでは灯火の鍛冶場が必ず1つ出現するようにした。
    "forgefire": {"name": "Forgefire Floor", "desc": "An Ember Forge is guaranteed to appear here", "color": (255, 170, 80)},
    # rev205で新設した新モンスターBloodthorn Revenant(通常攻撃が出血を与える)
    # も、venomfang/stormboundの時と同じく新システム導入と同じrevでフロア
    # 特性側の穴を埋めておく。出血付与確率を+20%pt上乗せする専用の特性。
    "bloodslick": {"name": "Bloodslick Floor", "desc": "Bloodthorn Revenant bleed chance +20%pt here", "color": (150, 10, 15)},
    # 今回新設した新モンスターPermafrost Wyrm(通常攻撃が凍結を与える)も、
    # bloodslickの時と同じく新システム導入と同じrevでフロア特性側の穴を
    # 埋めておく。凍結付与確率を+20%pt上乗せする専用の特性(既存の
    # "frostbound"キーはFrostbound Floor(敵の攻撃力-15%)で既に使われていた
    # ため、辞書キーの衝突を避けて"frostgrip"という新しいキーにした)。
    "frostgrip": {"name": "Frostgrip Floor", "desc": "Permafrost Wyrm freeze chance +20%pt here", "color": (150, 220, 255)},
    # 転がる巨石(黄金の像を持ち上げると追ってくるBOULDER_CHASE_DURATION歩の
    # 逃走ギミック)は、これまでどのフロア特性からも一切影響を受けない数少ない
    # 一点だった。既存修飾子の符号反転ではなく、新しい方向として追跡時間
    # そのものを短くする「当たり」特性を追加した(modifier_boulder_chase_duration_bonus()を新設)。
    "fleeting": {"name": "Fleeting Floor", "desc": "Rolling boulder chases are 8 steps shorter here", "color": (255, 205, 130)},
    # 秘宝Slayer's Emblem(rev208追加、ボス戦ダメージ+15%)は、これまで
    # どのフロア特性からも一切影響を受けない数少ない一点だった
    # (Venomfang/Stormbound/Bloodslick/Frostgripが新システム導入と同じrevで
    # 埋めてきた「フロア特性が及んでいない一点」の穴と同じパターンを、今回は
    # ボス戦ダメージに適用した)。このフロアで挑むボス級の相手(通常のステージ
    # ボス・エコーバトル・ボスラッシュ)には、ダメージがさらに+15%pt上乗せされる。
    "warbound": {"name": "Warbound Floor", "desc": "+15%pt bonus damage against bosses here", "color": (200, 50, 50)},
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
    """Bountiful Floorはアイテム発見率を+20%pt上乗せする「当たり」特性だったが、
    逆に下げる方向の対になる特性が無かったため、Scarce Floorとして
    -20%ptを返す分岐を追加した(Fortunate⇔Unluckyと同じ、既存修飾子の符号を
    反転させるパターン)。呼び出し側は max(0, min(99, ...)) でクランプしてから
    判定するため、マイナスになってもレアアイテムが出にくくなるだけで安全。"""
    if floor_modifier == "bountiful":
        return 20
    if floor_modifier == "cursed":
        return 25
    if floor_modifier == "scarce":
        return -20
    return 0

def modifier_poison_decay_mult():
    """既存の毒関連特性(toxic/venomous/antiseptic/serene)はすべて毒の「発生確率」に
    関わるものばかりで、一度かかった毒が抜けるまでの「速さ」に関わる特性が無かった。
    Festering Floorは歩数ごとの毒減少量(poison_decay_per_step)を半分に鈍らせて
    毒を長引かせ、対になるCleansing Floorは1.5倍速く抜けるようにした。呼び出し側で
    最低1は減るようクランプするため、0倍になって毒が永久に抜けなくなる心配は無い。"""
    if floor_modifier == "festering":
        return 0.5
    if floor_modifier == "cleansing":
        return 1.5
    return 1.0

def modifier_trap_mult():
    """Quiet Floorは罠の出現重みを0.3倍に間引く「当たり」特性だったが、
    逆に増やす方向の対になる特性が無かったため、Hazardous Floorとして
    2.0倍を返す分岐を追加した(Frail⇔Hardened、Tranquil⇔Snaredと同じ、
    既存修飾子の符号を反転させるパターン)。"""
    if floor_modifier == "quiet":
        return 0.3
    if floor_modifier == "hazardous":
        return 2.0
    return 1.0

def modifier_speed_mult():
    """Windy Floorは移動速度を1.3倍にする「当たり」特性だったが、逆に遅くする
    方向の対になる特性が無かったため、Sluggish Floorとして0.7倍を返す分岐を
    追加した(Empowered⇔Weakenedと同じ、既存修飾子の符号を反転させる
    パターン)。"""
    if floor_modifier == "windy":
        return 1.3
    if floor_modifier == "sluggish":
        return 0.7
    return 1.0

def modifier_food_mult():
    if floor_modifier == "chilly":
        return 1.5
    if floor_modifier == "verdant":
        return 0.6
    return 1.0

def modifier_gamble_win_chance():
    """拠点(サンクチュア)のポーション倍増ギャンブルは常に50%固定の勝率だった。
    Wagered Floorでは、このフロアにいる間だけ勝率を65%まで引き上げる。"""
    if floor_modifier == "wagered":
        return 65
    return 50

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
    """Rocky Floorは+3 DEFの代わりに移動速度が落ちる「守り」寄りの特性
    だったが、逆にDEFを削って速く動ける「攻め」寄りの対になる特性が
    無かったため、Frenzied Floorとして-3 DEFを返す分岐を追加した
    (Frail⇔Hardenedなどと同じ、既存修飾子の符号を反転させるパターン)。"""
    if floor_modifier == "rocky":
        return 3
    if floor_modifier == "frenzied":
        return -3
    return 0

def modifier_rocky_speed_mult():
    """Rocky Floor(-15%速度)の逆で、Frenzied Floorでは+15%速度になる。
    modifier_def_bonus()とセットで、DEF↔速度のトレードオフを両方向に
    体験できる対になる特性として追加した。"""
    if floor_modifier == "rocky":
        return 0.85
    if floor_modifier == "frenzied":
        return 1.15
    return 1.0

def modifier_poison_chance_bonus():
    """Toxic Floorは毒の発生確率が+25%pt上乗せされる「はずれ」特性だったが、
    逆に下げる方向の対になる特性が無かったため、Antiseptic Floorとして
    -15%ptを返す分岐を追加した(Fortunate⇔Unluckyと同じ、既存修飾子の符号を
    反転させるパターン)。呼び出し側は 30 + この戻り値 をrandint(0,99)との
    比較にそのまま使うため、マイナスになっても発生確率が下がるだけで安全。"""
    if floor_modifier == "toxic":
        return 25
    if floor_modifier == "antiseptic":
        return -15
    if floor_modifier == "venomous":
        # Serene Floorは毒を完全無効化する「当たり」特性だったが、その逆に
        # 毒を確実に発生させる方向の特性が無かったため、Venomous Floorとして
        # 呼び出し側の 30 + この戻り値 が必ず99を超えるだけの大きな値(70)を
        # 返す分岐を追加した。toxic/antisepticのような発生率の微調整ではなく、
        # 「毒を出せる敵(typ in (5,7,14))なら必ず刺さる」という新しい方向性。
        return 70
    return 0

def modifier_exp_mult():
    """Sparkling Floorは獲得EXPが1.3倍になる「当たり」特性だったが、
    逆に弱める方向の対になる特性が無かったため、Drab Floorとして
    0.8倍を返す分岐を追加した(Empowered⇔Weakenedと同じ、既存修飾子の
    符号を反転させるパターン)。"""
    if floor_modifier == "sparkling":
        return 1.3
    if floor_modifier == "drab":
        return 0.8
    return 1.0

def modifier_poison_immune():
    return floor_modifier == "serene"

def modifier_enemy_poison_chance_bonus():
    """Serpent's Fangの敵への毒付与確率(relic_enemy_poison_chance())に
    上乗せする、%pt単位のフロア特性ボーナス。呼び出し側はrelicの値と
    合算してからrandint(0,99)と比較するだけなので、秘宝を持っていない間は
    このフロアにいてもボーナスが乗るだけで実際には何も起きない。"""
    if floor_modifier == "venomfang":
        return 20
    return 0

def modifier_enemy_stun_chance_bonus():
    """Thunderclap Idolの敵への気絶付与確率(relic_enemy_stun_chance())に
    上乗せする、%pt単位のフロア特性ボーナス。modifier_enemy_poison_chance_bonus()
    と同じく、秘宝を持っていない間はこのフロアにいてもボーナスが乗るだけで
    実際には何も起きない。"""
    if floor_modifier == "stormbound":
        return 15
    return 0

def modifier_bleed_chance_bonus():
    """Bloodthorn Revenant(typ41)の出血付与確率(BLOODTHORN_BLEED_CHANCE)に
    上乗せする、%pt単位のフロア特性ボーナス。modifier_enemy_stun_chance_bonus()
    と同じく、Bloodthorn Revenantに遭遇していない間はこのフロアにいても
    ボーナスが乗るだけで実際には何も起きない。"""
    if floor_modifier == "bloodslick":
        return 20
    return 0

def modifier_freeze_chance_bonus():
    """Permafrost Wyrm(typ42)の凍結付与確率(PERMAFROST_FREEZE_CHANCE)に
    上乗せする、%pt単位のフロア特性ボーナス。modifier_bleed_chance_bonus()と
    同じく、Permafrost Wyrmに遭遇していない間はこのフロアにいてもボーナスが
    乗るだけで実際には何も起きない。"""
    if floor_modifier == "frostgrip":
        return 20
    return 0

def modifier_crit_chance_bonus():
    """Fortunate Floorはクリティカル発生率を+15%pt上乗せする「当たり」特性
    だったが、逆に下げる方向の対になる特性が無かったため、Unlucky Floorとして
    -15%ptを返す分岐を追加した(Tranquil⇔Snaredと同じ、既存修飾子の符号を
    反転させるパターン)。呼び出し側は total_crit_chance > 0 の判定を
    通してから乱数判定するため、マイナスになってもクリティカルが発生しなく
    なるだけで安全。"""
    if floor_modifier == "fortunate":
        return 0.15
    if floor_modifier == "unlucky":
        return -0.15
    return 0.0

def modifier_combo_bonus_per_stack():
    """Resonant Floorはコンボ倍率の伸びが1スタックあたり+15%になる「当たり」
    特性だったが、逆に伸びを鈍らせる方向の対になる特性が無かったため、
    Muffled Floorとして+5%(通常の半分)を返す分岐を追加した
    (Empowered⇔Weakenedと同じ、既存修飾子の符号を反転させるパターン)。"""
    if floor_modifier == "resonant":
        return 0.15
    if floor_modifier == "muffled":
        return 0.05
    return 0.1

def modifier_incoming_dmg_mult():
    if floor_modifier == "frostbound":
        return 0.85
    if floor_modifier == "cursed":
        return 1.15
    return 1.0

def modifier_atk_mult():
    """Empowered Floorは通常攻撃力を1.15倍にする「当たり」特性だったが、
    逆に弱める方向の対になる特性が無かったため、Weakened Floorとして
    0.85倍を返す分岐を追加した(Veiled⇔Swarming、Elite Grounds⇔Peacefulと
    同じ、既存修飾子の符号を反転させるパターン)。"""
    if floor_modifier == "empowered":
        return 1.15
    if floor_modifier == "weakened":
        return 0.85
    return 1.0

def modifier_flee_bonus():
    """Tranquil Floorは逃走成功率を+20%pt上乗せする「当たり」特性だったが、
    逆に下げる方向の対になる特性が無かったため、Snared Floorとして
    -20%ptを返す分岐を追加した(Frail⇔Hardenedと同じ、既存修飾子の符号を
    反転させるパターン)。"""
    if floor_modifier == "tranquil":
        return 20
    if floor_modifier == "snared":
        return -20
    return 0

def modifier_encounter_mult():
    """Veiled Floorではフロア生成時にモンスターの遭遇マス(event_pool内の2)を
    間引き、通常より静かに探索できるようにする倍率。対になるSwarming Floorは
    逆に遭遇マスを大幅に増やし、危険度と引き換えに戦闘・撃破数を稼ぎやすい
    ハイリスク・ハイリターンの特性(既存のmodifier_*()の符号を反転させる
    パターンで、Veiled Floorの「逆」として追加した)。"""
    if floor_modifier == "veiled":
        return 0.5
    if floor_modifier == "swarming":
        return 1.6
    return 1.0

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
    こちらは宝箱そのものの「数」を増やす新しい方向性の特性。
    Meager Floorはその逆で、宝箱の出現重みを半分に減らす(呼び出し側の
    treasure_weight = max(1, round(2 * この戻り値))が下限1でクランプ
    しているため、0.5を返しても数式が壊れない)。"""
    if floor_modifier == "opulent":
        return 2.0
    if floor_modifier == "meager":
        return 0.5
    return 1.0

def modifier_crit_dmg_mult():
    """Radiant Floorでは、クリティカルヒットの倍率が通常のx2からx2.5に上がる。
    fortunate(発生率)やempowered(通常攻撃力)はこれまであったが、
    クリティカル自体の「威力」を伸ばす特性が無かったため追加した。
    Dim Floorはその逆で、クリティカル倍率がx2からx1.5に下がる(Radiant Floorが
    伸ばす方向のみだったため、既存修飾子の符号を反転させるパターンで対になる
    「はずれ」特性を追加した)。"""
    if floor_modifier == "radiant":
        return 2.5
    if floor_modifier == "dim":
        return 1.5
    return 2.0

def modifier_lifesteal_pct():
    """Vampiric Floor:通常攻撃(Attack)がヒットするたび、与えたダメージの
    15%を自分のHPとして回復する新しいフロア特性。これまでの特性は
    「ダメージ・確率・移動速度などの数値を上下させる」ものばかりで、
    攻撃した結果プレイヤー自身が回復するという方向の仕掛けが無かったため、
    既存修飾子の符号反転ではない新しいカテゴリの特性として追加した。"""
    if floor_modifier == "vampiric":
        return 0.15
    return 0.0

def modifier_full_heal_on_kill():
    """Sanctuary Floor:敵を倒すたびにHPが全回復する新しいフロア特性。
    Vampiric Floorが「攻撃した瞬間」に少しずつ回復する(オンヒット型)のに対し、
    こちらは「敵を倒しきった瞬間」に全回復する(オンキル型)という、これまで
    無かった発動タイミングの新しい方向性の特性として追加した。"""
    return floor_modifier == "sanctuary"

def modifier_second_wind():
    """Second Wind Floor:このフロアで初めてHPが20%を切った瞬間、一度だけ
    最大HPの15%を自動回復する安全網。Sanctuary/Vampiricが「攻撃した結果」の
    回復なのに対し、こちらは「ピンチに陥ったこと自体」が引き金になる。"""
    return floor_modifier == "second_wind"

def modifier_focus_mult():
    """集中(Focusコマンド)は次の一撃のダメージを通常x1.5倍にするが、
    クリティカル(modifier_crit_dmg_mult)やコンボフィニッシャーには専用の
    倍率強化フロア特性(radiant/dim)があるのに対し、Focus自体の威力を
    伸ばす特性が無かった。新しいFocused Floorでは、この一撃倍率がx2.0に
    上がり、集中してから攻める立ち回りがより効果的になる。"""
    if floor_modifier == "focused":
        return 2.0
    return 1.5

def modifier_ultimate_mult():
    """Overcharged Floorは必殺技(Ultimate)の発動に必要なコンボ数(発動しやすさ)
    にしか関わっておらず、発動した後の一撃の威力を伸ばす特性がまだ無かった。
    Devastation Floorでは、Focused FloorがFocusの一撃倍率を伸ばすのと同じ
    考え方で、Ultimateのダメージそのものを+25%する。"""
    if floor_modifier == "devastation":
        return 1.25
    return 1.0

def modifier_counter_bonus():
    """Bulwark Floorでは、Counterコマンドの被ダメージ軽減量・反撃ダメージが
    ともに1.5倍になる。Focused FloorがFocus専用、Overcharged FloorがUltimate
    専用の強化特性であるのと同じ考え方で、Counter専用の強化特性として追加した。
    rev182で追加したMonk(counter_mult)はこの戻り値にさらに掛け算される
    キャラクター側の倍率で、Bulwark Floor + Monkを組み合わせると両方が
    重なってさらに強力なCounterになる。"""
    if floor_modifier == "bulwark":
        return 1.5
    return 1.0

def modifier_boss_phase2_threshold():
    """ボス・エコーバトルのフェーズ2(激怒)は、従来どこの階でもHPが50%を切った
    瞬間に固定で発動していた。Simmering Floorではその発動しきい値をHP65%まで
    前倒しし、通常のボス戦より早く・長くフェーズ2の激怒状態と戦うことになる
    ハイテンションな一戦にする。"""
    if floor_modifier == "simmering":
        return 0.65
    if floor_modifier == "placid":
        return 0.35
    return 0.5

def modifier_trap_dmg_mult():
    """Merciful Floorでは、罠(通常の罠・罠の宝箱)によるダメージが30%軽減される。
    quiet(遭遇頻度そのものを下げる)とは別の角度で、踏んでしまった罠の
    「痛さ」自体を和らげる、初めての防御寄り特性。
    Ruinous Floorは、Frail⇔HardenedやQuiet⇔Hazardousと同じ「既存修飾子の
    符号を反転させる」パターンで、Mercifulの逆(罠ダメージが30%増える)
    ハイリスクな特性として追加した。"""
    if floor_modifier == "merciful":
        return 0.7
    if floor_modifier == "ruinous":
        return 1.3
    return 1.0

def modifier_curse_immune():
    """Warded Floorでは、呪いの床(STR/DEFが下がるタイル)を踏んでも
    デバフを受けない。serene(毒を無効化)と同じ「特定の状態異常を
    まるごと防ぐ」方向性を、呪いの床に対しても持たせた特性。"""
    return floor_modifier == "warded"

def modifier_enemy_life_mult():
    """Frail Floorでは、出現する通常モンスターの最大HPが20%減る。従来の
    フロア特性はプレイヤー側の攻守やアイテムの効果に関わるものが中心で、
    敵そのものの強さを直接弱める特性が無かったため、新しい方向性として
    追加した(ボス・ミミック・キメラ・ドッペルゲンガーなどの特殊な敵には
    適用されない。elite_chance_bonusが通常戦闘限定なのと同じ扱い)。
    対になるHardened Floorでは、逆に通常モンスターの最大HPが20%増える
    (Frail Floorが弱める方向のみだったため、Veiled⇔Swarmingと同じ
    「既存修飾子の符号を反転させる」パターンで、ハイリスク・ハイリターンの
    対になる特性を追加した)。"""
    if floor_modifier == "frail":
        return 0.8
    if floor_modifier == "hardened":
        return 1.2
    return 1.0

def modifier_trade_cost_mult():
    """Bazaar Floorでは、フロア探索中に出会う旅の商人(idx==48)との
    取引コストが25%引きになる。これまでのフロア特性は入手量や被ダメージなど
    プレイヤーの戦闘・探索能力に関わるものばかりで、アイテム交換の
    「コスト」自体に関わる経済寄りの特性が無かったため、新しい方向性として
    追加した。
    Costly Floorはその逆で、取引コストが25%割高になる(Bazaar Floorが
    安くする方向のみだったため、既存修飾子の符号を反転させるパターンで
    対になる「はずれ」特性を追加した)。"""
    if floor_modifier == "bazaar":
        return 0.75
    if floor_modifier == "costly":
        return 1.25
    return 1.0

def merchant_trade_cost(base):
    """旅の商人での取引コストにmodifier_trade_cost_mult()とTraderのtrade_mult
    (該当キャラ以外は.get()のデフォルト1.0で無影響)を適用した実際の
    コストを返す(最低1を保証)。Bazaar Floorでなければbaseのまま。"""
    return max(1, int(base * modifier_trade_cost_mult() * char_params().get("trade_mult", 1.0)))

def modifier_mimic_immune():
    """Genuine Floorでは、宝箱を開けた時にミミックが混ざらなくなる。
    これまでのフロア特性はダメージ・遭遇頻度・コストなどに関わるものばかりで、
    「宝箱の安全性」自体に関わる特性が無かったため、新しい方向性として追加した。"""
    return floor_modifier == "genuine"

def modifier_mimic_chance_mult():
    """Genuine Floorはミミックの混入を完全に無効化する「当たり」特性だったが、
    逆に混入率を上げる対になる特性が無かったため、Treacherous Floorとして
    ミミック出現率を2倍にする分岐を追加した(Frail⇔Hardenedなどと同じ、
    既存修飾子の符号を反転させるパターン)。呼び出し側はmodifier_mimic_immune()
    を先にチェックしているため、genuineとtreacherousが同時に効くことはない。"""
    if floor_modifier == "treacherous":
        return 2.0
    return 1.0

def modifier_pet_egg_chance_mult():
    """宝箱がまれに(通常3%)仲間(ペット)の卵に化ける確率を、Bonded Floorでは
    2倍にする。既存のフロア特性は宝箱の「中身の質」(item_bonus系)や食料の
    「量」には関わっていたが、ペットの卵という別枠の抽選そのものを動かす
    特性が無かったため、新しい軸として追加した。"""
    if floor_modifier == "bonded":
        return 2.0
    return 1.0

def modifier_food_yield_mult():
    """Fertile Floorでは、探索中に見つかる食料アイテムの回復量が1.5倍になる。
    chilly/verdantは食料の「消費速度」に関わる特性だったが、拾った食料自体の
    「量」を増やす特性が無かったため、新しい方向性として追加した。
    Withered Floorはその逆で、食料の回復量が30%減る(Fertile Floorが増やす
    方向のみだったため、既存修飾子の符号を反転させるパターンで対になる
    「はずれ」特性を追加した)。"""
    if floor_modifier == "fertile":
        return 1.5
    if floor_modifier == "withered":
        return 0.7
    return 1.0

def modifier_blaze_dmg_mult():
    """Volatile Floorでは、爆炎石(Blaze Gem)の与えるダメージが1.5倍になる。
    従来のフロア特性は通常攻撃・クリティカル・被ダメージなどには関わっていたが、
    アイテムとして使う爆炎石そのものの威力に関わる特性が無かったため、
    新しい方向性として追加した。
    Damp Floorでは、その逆に爆炎石のダメージが30%弱まる。Volatile Floorは
    爆炎石を強める方向のみの特性だったため、Frail⇔Hardenedなどと同じ
    「既存修飾子の符号を反転させる」パターンで対になる「はずれ」特性を追加した。"""
    if floor_modifier == "volatile":
        return 1.5
    if floor_modifier == "damp":
        return 0.7
    return 1.0

def modifier_defpill_mult():
    """Bastion Floorでは、防御の薬(Defense Pill)が付与するDEFバフ量が1.5倍になる。
    Volatile Floor(爆炎石の威力)・Fertile Floor(食料の回復量)と同じ発想で、
    3種類ある消費アイテムのうち防御の薬だけ、フロア特性で威力が伸びる
    仕組みが無かったため、同じ枠組みで抜けを埋める新しい方向性として追加した。
    Corroded Floorはその逆で、防御の薬のDEFバフ量が25%減る(Bastion Floorが
    伸ばす方向のみだったため、既存修飾子の符号を反転させるパターンで対になる
    「はずれ」特性を追加した)。"""
    if floor_modifier == "bastion":
        return 1.5
    if floor_modifier == "corroded":
        return 0.75
    return 1.0

def modifier_echo_chance():
    """Echoing Floorでは、通常攻撃(Attack)がヒットした際に25%の確率で
    追加の一撃(ダメージは半分)が即座に連続してもう1回入る。既存の特性は
    いずれも1回の攻撃の威力・回復量・確率などの「数値」を上下させるだけ
    だったが、これは「攻撃という行動そのものがもう1回起こるかもしれない」
    という、今までに無かった発動タイミングの特性(Sanctuary Floorの
    オンキル型と同じ発想で、今回は「オン攻撃・確率追撃型」)。"""
    if floor_modifier == "echoing":
        return 25
    return 0

def modifier_ultimate_combo_requirement():
    """Overcharged Floor:必殺技(Ultimate)の発動に必要なコンボ数がULTIMATE_
    COMBO_REQUIREMENT(5)から3に下がる。これまでのフロア特性はダメージ・
    確率・移動速度などパラメータの数値を上下させるだけだったが、バトル
    コマンドそのものの「解放条件」を変える特性が無かったため、新しい
    方向性として追加した(コンボを3まで積めば以降は毎ターンでもUltimateを
    連発しやすくなる、テンポ重視の「当たり」特性)。"""
    if floor_modifier == "overcharged":
        return 3
    return ULTIMATE_COMBO_REQUIREMENT

def modifier_charm_shrine_guaranteed():
    """Charmed Floor:このフロアでは護符の祠(Charm Shrine)が確率ではなく
    必ず1つ出現する(make_dungeon側でCHARM_SHRINE_CHANCEの代わりにこの
    真偽値を参照する)。"""
    return floor_modifier == "charmed"

def modifier_statue_threshold_bonus():
    """Hallowed Floor:守護者の像(Guardian Statue)の試練に必要なSTRが
    20下がる(statue_str_threshold()側でこの戻り値を差し引く)。"""
    if floor_modifier == "hallowed":
        return -20
    return 0

def modifier_relic_drop_bonus():
    """Fated Floor:このフロアでボスを倒したときの秘宝(Relic)ドロップ率が
    15%pt上乗せされる(RELIC_DROP_CHANCEに加算して使う)。"""
    if floor_modifier == "fated":
        return 15
    return 0

def modifier_boss_dmg_bonus():
    """Warbound Floor:このフロアで挑むボス級の相手(通常のステージボス・
    エコーバトル・ボスラッシュ)へのダメージが+0.15上乗せされる
    (relic_boss_dmg_mult()の戻り値に加算して使う、他フロアは0.0で無影響)。"""
    if floor_modifier == "warbound":
        return 0.15
    return 0.0

def modifier_ember_forge_str_mult():
    """Molten Floor:このフロアの灯火の鍛冶場(Ember Forge)は、ブレイズジェムを
    永続STRに変える変換レートが1.5倍になる(EMBER_FORGE_STR_PER_GEMに掛けて使う)。"""
    if floor_modifier == "molten":
        return 1.5
    return 1.0

def modifier_ember_forge_guaranteed():
    """Forgefire Floor:このフロアには灯火の鍛冶場(Ember Forge)が確率ではなく
    必ず1つ出現する(place_ember_forge()呼び出し側でEMBER_FORGE_CHANCEの
    代わりにこの真偽値を参照する。charmed FloorのCharm Shrineと同じパターン)。"""
    return floor_modifier == "forgefire"

def modifier_secret_vault_chance_bonus():
    """Buried Floor:carve_hidden_room()が隠し部屋を『秘密の宝物庫(Secret Vault)』
    (宝箱2つ連なり)にする確率(通常15%pt固定)に加算する上乗せ分(%pt)。"""
    if floor_modifier == "buried":
        return 15
    return 0

def modifier_boulder_chase_duration_bonus():
    """Fleeting Floor:黄金の像を持ち上げた後に追ってくる巨石の逃走猶予
    (BOULDER_CHASE_DURATION歩)に加算する分(負の値なら短縮=当たり特性)。
    呼び出し側はmax(8, ...)でクランプしてから使うため、0以下になっても
    最低限の緊張感は残る。"""
    if floor_modifier == "fleeting":
        return -8
    return 0

def effective_ultimate_combo_requirement():
    """Ultimateの発動に必要なコンボ数の実効値。フロア特性(Overcharged Floor)に
    加え、スキルツリーの新しい枝「Tactics」の3段目「Combo Adept」でも短縮できる
    ようにした。両方を素直に足し引きすると0以下になり得てコマンド自体が
    無意味化してしまうため、下限をmax(2, ...)でクランプしている。"""
    return max(2, modifier_ultimate_combo_requirement() - skill_ultimate_req_reduction)

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
    """フロア番号(1始まり)から探索/戦闘BGM・戦闘背景のテーマ番号(0/1/2)を返す。
    current_stage()はゲームバランス用にSTAGE_COUNTで頭打ちになるため、91階以降の
    エンドレス・ディープスはこれまでずっとテーマ2(ステージ3の炎)のBGM・背景が
    固定で流れ続けていた(場面に合わないBGMが延々ループする不具合)。ゲーム
    バランス(敵の強さなど)には手を触れず、見た目・音だけのテーマ番号を
    STAGE_LENGTHごとに0→1→2→0…と巡回させることで、潜り続けても飽きの来ない
    テーマの移り変わりを付けた。"""
    if fl > MAX_FLOOR:
        return ((fl - MAX_FLOOR - 1) // STAGE_LENGTH) % STAGE_COUNT
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
    ("nightmare_clear", "Clear all stages on Nightmare difficulty"),
    ("abyss_clear", "Clear all stages on Abyss difficulty (permadeath)"),
    ("starve_survive", "Survive starvation (0 food)"),
    ("trap100", "Step on 100 traps"),
    ("hidden_boss_defeat", "Defeat the hidden boss"),
    ("true_hidden_boss_defeat", "Defeat the true hidden boss (??? The Voidcrowned)"),
    ("skill_maxed", "Max out any single skill"),
    ("grandmaster", "Unlock the Grandmaster capstone skill"),
    ("combat_sage", "Max out every skill in the Tactics branch"),
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
    ("spirit_whisperer", "Encounter 10 wandering spirits in total"),
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
    ("totemic", "Channel elemental totems 15 times in total"),
    ("card_shark", "Win 20 Gambling Den bets in total"),
    ("master_trader", "Trade with a merchant 50 times in total"),
    ("dungeon_warden", "Clear 15 monster dens in total"),
    ("boss_vanquisher", "Defeat 20 stage bosses in total"),
    ("mimic_hunter", "Defeat 15 Mimic chests in total"),
    ("chimera_bane", "Defeat the Chimera 10 times in total"),
    ("guardian_angel", "Rescue 20 captive allies in total"),
    ("shadow_reaper", "Defeat your own shadow doppelganger 10 times in total"),
    ("crimson_survivor", "Survive 5 Blood Moon floors in total"),
    ("bounty_master", "Complete 10 bounty board quests in total"),
    ("golden_hunter", "Catch 10 golden slimes in total"),
    ("rift_master", "Survive 10 rift Elite encounters in total"),
    ("boulder_master", "Outrun 15 rolling boulders in total"),
    ("altar_devotee", "Receive 10 altar boons in total"),
    ("master_smith", "Convert Blaze Gems into permanent STR at an Ember Forge 10 times in total"),
    ("voidforged_slain", "Defeat a Voidforged Golem"),
    ("voidforged_bane", "Defeat 10 Voidforged Golems in total"),
    ("legendary_hero", "Reach character level 40"),
    ("mirror_wraith_slain", "Defeat a Mirror Wraith"),
    ("mirror_wraith_bane", "Defeat 10 Mirror Wraiths in total"),
    ("ultimate_unleashed", "Unleash your character's Ultimate move"),
    ("ultimate_master", "Use your character's Ultimate move 20 times in total"),
    ("endless_delver", "Reach floor 100 in Endless Depths"),
    ("endless_legend", "Reach floor 150 in Endless Depths"),
    ("endless_myth", "Reach floor 200 in Endless Depths"),
    ("counter_master", "Land 30 Counter attacks in total"),
    ("hollow_widow_slain", "Defeat a Hollow Widow"),
    ("hollow_widow_bane", "Defeat 10 Hollow Widows in total"),
    ("chain_warden_slain", "Defeat a Chain Warden"),
    ("chain_warden_bane", "Defeat 10 Chain Wardens in total"),
    ("frenzied_revenant_slain", "Defeat a Frenzied Revenant"),
    ("frenzied_revenant_bane", "Defeat 10 Frenzied Revenants in total"),
    ("abyssal_warden_slain", "Defeat an Abyssal Warden"),
    ("abyssal_warden_bane", "Defeat 10 Abyssal Wardens in total"),
    ("pet_bond_formed", "Form a Pet Bond with your companion"),
    ("bond_keeper", "Form a Pet Bond 5 times in total"),
    ("relic_finder", "Find your first Relic"),
    ("relic_collector", "Collect every Relic"),
    ("secret_vault_finder", "Find your first Secret Vault"),
    ("secret_vault_hoarder", "Find 5 Secret Vaults in total"),
    ("warbreaker_wight_slain", "Defeat a Warbreaker Wight"),
    ("warbreaker_wight_bane", "Defeat 10 Warbreaker Wights in total"),
    ("charm_seeker", "Find your first Charm"),
    ("charm_collector", "Collect every Charm"),
    ("close_call", "Win a battle with less than 15% HP remaining"),
    ("iron_will", "Win 10 battles with less than 15% HP remaining, in total"),
    ("gloom_sprite_slain", "Defeat a Gloom Sprite"),
    ("gloom_sprite_bane", "Defeat 10 Gloom Sprites in total"),
    ("vault_survivor", "Escape 10 collapsing vaults in total"),
    ("treasure_keykeeper", "Open 10 sealed vaults with a Sacred Key in total"),
    ("statue_champion", "Pass a Guardian Statue's strength trial 10 times in total"),
    ("locksmith_master", "Trigger 10 pressure plates to unlock sealed doors in total"),
    ("hungry_rat_slain", "Defeat a Hungry Rat"),
    ("hungry_rat_bane", "Defeat 10 Hungry Rats in total"),
    ("cinder_ward_slain", "Defeat a Cinder Ward"),
    ("cinder_ward_bane", "Defeat 10 Cinder Wards in total"),
    ("numbing_hornet_slain", "Defeat a Numbing Hornet"),
    ("numbing_hornet_bane", "Defeat 10 Numbing Hornets in total"),
    ("flawless_victor", "Win 10 battles without taking damage, in total"),
    ("bestiary_complete", "Discover every monster, boss, and item in the Bestiary"),
    ("grand_champion", "Clear the game 5 times in total"),
    ("ashbound_titan_slain", "Defeat an Ashbound Titan"),
    ("ashbound_titan_bane", "Defeat 10 Ashbound Titans in total"),
    ("shrine_regular", "Try your luck at a shrine 10 times in total"),
    ("bloodbound", "Heal 5,000 total HP via lifesteal"),
    ("silence_wisp_slain", "Defeat a Silence Wisp"),
    ("silence_wisp_bane", "Defeat 10 Silence Wisps in total"),
    ("altar_regular", "Make an offering at a sacrificial altar 10 times in total"),
    ("venomtouch", "Poison an enemy with Serpent's Fang"),
    ("serpent_charmer", "Defeat 10 poisoned enemies in total"),
    ("daily_challenger", "Clear the Daily Challenge"),
    ("daily_devotee", "Clear the Daily Challenge on 7 different days in total"),
    ("vengeful_wraith_slain", "Defeat a Vengeful Wraith"),
    ("vengeful_wraith_bane", "Defeat 10 Vengeful Wraiths in total"),
    # High Roller(high_roller、Gambling Denの最高額の賭けに勝つ)は初回実績は
    # あるのに繰り返し達成し続けることを評価する累積実績が無く、Golden
    # Hunter/Rift Master/Bounty Masterなどと同じ「初回はあるが繰り返し系が
    # 無かった」穴が残っていたため、新しい記録(high_roller_wins)を追加して
    # 累積実績を用意した。
    ("high_roller_veteran", "Win 10 High Roller bets in total"),
    # 新しい「近道(分岐ルート)」システム(carve_branch_route参照)の発見実績。
    # secret_vault_finder/hoarderと同じ「初回」+「累積」の2段構成にする。
    ("branch_route_finder", "Discover a hidden shortcut passage"),
    ("branch_route_veteran", "Discover 5 shortcut passages in total"),
    # 新ヒーローApothecary(rev201追加)により、Serpent's Fangを持たなくても
    # 敵を毒にできるようになったため、その双方の入口を持つ実績として
    # enemies_poisoned_totalの累積実績を新設した。
    ("venom_adept", "Poison 25 enemies in total"),
    # 新秘宝Thunderclap Idol(rev202追加)による気絶実績。venomtouch/venom_adept
    # と同じ「初回」+「累積25回」の2段構成。
    ("shocktouch", "Stun an enemy with Thunderclap Idol"),
    ("stun_master", "Stun 25 enemies in total"),
    # 新しい闘技場(Arena of Trials)システムの実績。他の新システム(Shortcut
    # Passage、Serpent's Fang等)と同じく、システム導入と同じrevで実績側の
    # 入口も用意する。
    ("arena_novice", "Clear a round in the Arena of Trials"),
    ("arena_gladiator", "Reach round 10 in a single Arena of Trials run"),
    # Arena of Trials(rev203追加)はarena_novice(初回クリア)・arena_gladiator
    # (1回の挑戦でラウンド10到達)の2つはあったが、shrine_regular/altar_regular/
    # branch_route_veteranなどと同じ「初回はあるが繰り返し系が無かった」穴が
    # ここにも残っていた。全挑戦を通算したクリアラウンド数(arena_total_rounds_cleared、
    # 継続・退却・敗北のいずれで区切っても、クリアした分は必ず加算される)を
    # 新設し、通算50ラウンドクリアで解除する累積実績を追加した。
    ("arena_veteran", "Clear 50 rounds in the Arena of Trials in total"),
    # 新モンスターBloodthorn Revenant(typ41、出血を与える新モンスター)の
    # 実績。Vengeful Wraith/Silence Wispと同じ「初回」+「累積10体」の2段構成。
    ("bloodthorn_revenant_slain", "Defeat a Bloodthorn Revenant"),
    ("bloodthorn_revenant_bane", "Defeat 10 Bloodthorn Revenants in total"),
    # 新システム「ヒーロー覚醒(Hero Awakening)」の実績。ボスを倒した瞬間、
    # そのキャラクターで初めてボスを倒したなら永久に覚醒し、以後そのキャラを
    # 選ぶたび常時ステータスボーナスを得る(awaken_character()参照)。
    # hero_awakened(初回覚醒)・full_ascension(全18人覚醒)の2段構成は
    # 他の「初回+累積(全種)」実績と同じパターン。rev211でVanguardが
    # 18人目として加わったため、判定はlen(CHARACTER_ORDER)を参照しており
    # 表記のみ17→18に更新した。
    ("hero_awakened", "Awaken your first Hero"),
    ("full_ascension", "Awaken all 18 Heroes"),
    # 新モンスターPermafrost Wyrm(typ42、凍結を与える新モンスター)の実績。
    # Bloodthorn Revenantと同じ「初回」+「累積10体」の2段構成。
    ("permafrost_wyrm_slain", "Defeat a Permafrost Wyrm"),
    ("permafrost_wyrm_bane", "Defeat 10 Permafrost Wyrms in total"),
    # 新モード「ボスラッシュ」の実績。arena_novice/arena_gladiatorと同じ
    # 「初回の一歩」+「完全達成」の2段構成。
    ("boss_rush_starter", "Defeat your first boss in the Boss Rush"),
    ("boss_rush_champion", "Clear the Boss Rush (defeat all 9 stage bosses in a row)"),
    # boss_rush_champion(初回全クリア)は、Arena Novice/Gladiatorや
    # Trial Survivor/Masterと同じ「初回はあるが繰り返し系が無かった」穴が
    # ここにも残っていた。既存の記録(boss_rush_clears、全クリアのたびに
    # record_stat()で加算済み)をそのまま活かし、通算5回の全クリアで
    # 解除する累積実績を追加した。
    ("boss_rush_veteran", "Clear the Boss Rush 5 times in total"),
    # 新実績「Critical Veteran」:crit_master(通算50回)はすでにあったが、
    # Boulder Master/Altar Devotee/Fortune Chaserなどと同様に、初回実績
    # (crit_master)より一段上の繰り返し目標が無かった穴を埋めた。既存の記録
    # (critical_hits_landed)をそのまま活かし、通算200回で解除する。
    ("critical_veteran", "Land 200 Critical Hits in total"),
    # 聖なる鍵(sacred_keys_found)は拾った回数を記録していながら、これまで
    # どの実績からも一切参照されていなかった穴だった(鍵と封印の宝物庫は
    # 別々に抽選されるため、鍵だけ見つけて宝物庫に出会えないことも多い)。
    # 既存の記録をそのまま活かし、Boulder Master/Altar Devoteeと同じ
    # 累積目標として追加した。
    ("key_collector", "Find 20 Sacred Keys in total"),
    # 新しい特殊床「試練の石碑(Trial Post)」の実績。rift_survivor/rift_masterと
    # 同じ「初回」+「累積10回」の2段構成。
    ("trial_survivor", "Defeat the Elite guardian of a Trial Post"),
    ("trial_master", "Clear 10 Trial Posts in total"),
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
    "totemic": ("totems_used", 15),
    "card_shark": ("gambles_won", 20),
    "master_trader": ("merchant_trades", 50),
    "dungeon_warden": ("dens_cleared", 15),
    "boss_vanquisher": ("bosses_defeated_count", 20),
    "mimic_hunter": ("mimics_defeated", 15),
    "chimera_bane": ("chimeras_defeated", 10),
    "guardian_angel": ("allies_rescued", 20),
    "shadow_reaper": ("doppelgangers_defeated", 10),
    "crimson_survivor": ("blood_moons_survived", 5),
    "bounty_master": ("bounties_completed", 10),
    "golden_hunter": ("golden_sprites_caught", 10),
    "rift_master": ("rifts_cleared", 10),
    "boulder_master": ("boulders_dodged", 15),
    "altar_devotee": ("altar_boons", 10),
    "master_smith": ("ember_forges_used", 10),
    "voidforged_bane": ("voidforged_golems_defeated", 10),
    "mirror_wraith_bane": ("mirror_wraiths_defeated", 10),
    "ultimate_master": ("ultimates_used", 20),
    # endless_delver/endless_legendはrev170のEndless Depths追加時に実績自体は
    # 用意されていたが、他の累積系実績と同じ進捗表示(現在値/しきい値)への
    # 登録が漏れていたため、既存の記録(deepest_endless_floor)を使って追加した。
    "endless_delver": ("deepest_endless_floor", 100),
    "endless_legend": ("deepest_endless_floor", 150),
    "endless_myth": ("deepest_endless_floor", 200),
    "counter_master": ("counters_used", 30),
    "hollow_widow_bane": ("hollow_widows_defeated", 10),
    "chain_warden_bane": ("chain_wardens_defeated", 10),
    # さまよう精霊(Wandering Spirit)は初回遭遇の実績「spirit_blessed」しか
    # 無く、Golden Hunter/Rift Master/Bounty Masterなどと同じ「初回はあるが
    # 繰り返し系が無かった」穴が残っていたため、既存の記録
    # (spirits_encountered)をそのまま使って累積実績を追加した。
    "spirit_whisperer": ("spirits_encountered", 10),
    "frenzied_revenant_bane": ("frenzied_revenants_defeated", 10),
    "abyssal_warden_bane": ("abyssal_wardens_defeated", 10),
    # Pet Bond(仲間との絆)は初回形成の実績「pet_bond_formed」しか無く、
    # Golden Hunter/Rift Master/Bounty Masterなどと同じ「初回はあるが繰り返し系が
    # 無かった」穴が残っていたため、新しい記録(pet_bonds_formed)を使って
    # 累積実績を追加した。
    "bond_keeper": ("pet_bonds_formed", 5),
    "secret_vault_hoarder": ("secret_vaults_found", 5),
    "warbreaker_wight_bane": ("warbreaker_wights_defeated", 10),
    "iron_will": ("close_calls", 10),
    "gloom_sprite_bane": ("gloom_sprites_defeated", 10),
    "hungry_rat_bane": ("hungry_rats_defeated", 10),
    "cinder_ward_bane": ("cinder_wards_defeated", 10),
    "numbing_hornet_bane": ("numbing_hornets_defeated", 10),
    # 無傷勝利(no_damage_win)は初回実績はあるのに繰り返し達成し続けることを
    # 評価する累積実績が無く、Golden Hunter/Rift Masterと同じ「初回はあるが
    # 繰り返し系が無かった」穴が残っていたため、新しい記録(no_damage_wins)を
    # 使って累積実績を追加した。
    "flawless_victor": ("no_damage_wins", 10),
    # 秘密の宝物庫からの脱出(vault_escapee)・聖なる鍵での宝物庫開放(vault_opener)・
    # 守護者の像の試練突破(statue_trial_passed)・圧力プレートでの扉解錠
    # (door_unlocked)は、いずれも初回実績はあるのに繰り返し達成し続けることを
    # 評価する累積実績が無く、Golden Hunter/Rift Master/Bounty Masterと同じ
    # 「初回はあるが繰り返し系が無かった」穴が残っていたため、既存の記録
    # (vaults_escaped/vaults_opened/statue_trials_passed/pressure_plates_triggered)
    # をそのまま活かして4つまとめて追加した。
    "vault_survivor": ("vaults_escaped", 10),
    "treasure_keykeeper": ("vaults_opened", 10),
    "statue_champion": ("statue_trials_passed", 10),
    "locksmith_master": ("pressure_plates_triggered", 10),
    "grand_champion": ("runs_completed", 5),
    "ashbound_titan_bane": ("ashbound_titans_defeated", 10),
    # 祠の運試し(shrine_gambler)は初回実績はあるのに繰り返し達成し続けることを
    # 評価する累積実績が無く、Golden Hunter/Rift Master/Bounty Masterと同じ
    # 「初回はあるが繰り返し系が無かった」穴が残っていたため、既存の記録
    # (shrines_used)をそのまま活かして累積実績を追加した。
    "shrine_regular": ("shrines_used", 10),
    "bloodbound": ("total_lifesteal_healed", 5000),
    "silence_wisp_bane": ("silence_wisps_defeated", 10),
    # 生贄の祭壇での献上(altar_sacrifice)は初回実績はあるのに繰り返し達成し
    # 続けることを評価する累積実績が無く、Golden Hunter/Rift Master/Bounty
    # Masterなどと同じ「初回はあるが繰り返し系が無かった」穴が残っていた。
    # 既存の記録(altars_used、結果がBoon/Silence/Backlashのいずれでも
    # 加算される)をそのまま活かして累積実績を追加した。
    "altar_regular": ("altars_used", 10),
    "serpent_charmer": ("poisoned_enemies_defeated", 10),
    # デイリーチャレンジ(daily.json)はこれまで実績と一切連動していなかった穴を
    # 埋めた新しい記録。何日クリアしたか(distinct日数)をstats.jsonに記録する。
    "daily_devotee": ("daily_challenges_cleared", 7),
    "vengeful_wraith_bane": ("vengeful_wraiths_defeated", 10),
    "high_roller_veteran": ("high_roller_wins", 10),
    "branch_route_veteran": ("branch_routes_found", 5),
    "venom_adept": ("enemies_poisoned_total", 25),
    "stun_master": ("enemies_stunned_total", 25),
    "arena_gladiator": ("arena_best_round", 10),
    "arena_veteran": ("arena_total_rounds_cleared", 50),
    "bloodthorn_revenant_bane": ("bloodthorn_revenants_defeated", 10),
    "full_ascension": ("characters_awakened_count", 18),
    "permafrost_wyrm_bane": ("permafrost_wyrms_defeated", 10),
    "critical_veteran": ("critical_hits_landed", 200),
    "key_collector": ("sacred_keys_found", 20),
    "trial_master": ("trial_posts_cleared", 10),
    "boss_rush_veteran": ("boss_rush_clears", 5),
}

# --- 実績連動の称号システム ---
# 解除した実績のうち、最も優先度の高いものを称号として表示する。
TITLE_DEFS = [
    # (実績キー, 称号, 優先度が高い順に並べる)
    ("abyss_clear",        "the Abysswalker"),
    ("true_hidden_boss_defeat", "the Voidcrowned Slayer"),
    ("hidden_boss_defeat", "the Unbound Slayer"),
    ("endless_myth",       "the Unfathomable"),
    ("endless_legend",     "the Depthless"),
    ("nightmare_clear",    "the Nightmare Breaker"),
    ("hard_clear",         "the Hardened"),
    ("grand_champion",     "the Grand Champion"),
    ("game_clear",         "the Conqueror"),
    ("no_damage_win",      "the Untouchable"),
    ("trap100",            "the Surefooted"),
    ("starve_survive",     "the Enduring"),
    ("boss_defeat",        "the Boss Slayer"),
    ("grandmaster",        "the Grandmaster"),
    ("skill_maxed",        "the Adept"),
    ("combat_sage",        "the Combat Sage"),
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
    ("spirit_whisperer",   "the Spirit Whisperer"),
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
    ("critical_veteran",   "the Marksman"),
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
    ("totemic",              "the Totemkeeper"),
    ("card_shark",           "the Card Shark"),
    ("master_trader",        "the Master Trader"),
    ("dungeon_warden",       "the Dungeon Warden"),
    ("boss_vanquisher",     "the Boss Vanquisher"),
    ("mimic_hunter",        "the Mimic Hunter"),
    ("chimera_bane",        "the Chimera Bane"),
    ("guardian_angel",      "the Guardian Angel"),
    ("shadow_reaper",       "the Shadow Reaper"),
    ("crimson_survivor",    "the Crimson Veteran"),
    ("bounty_master",       "the Bounty Master"),
    ("golden_hunter",       "the Golden Hunter"),
    ("rift_master",         "the Rift Master"),
    ("boulder_master",      "the Boulder Master"),
    ("altar_devotee",       "the Favored"),
    ("master_smith",        "the Master Smith"),
    ("legendary_hero",      "the Legend"),
    ("voidforged_bane",     "the Voidbane"),
    ("voidforged_slain",    "the Void Breaker"),
    ("mirror_wraith_bane",  "the Wraithbane"),
    ("mirror_wraith_slain", "the Reflection Breaker"),
    ("hollow_widow_bane",   "the Widowbane"),
    ("hollow_widow_slain",  "the Drainbreaker"),
    ("chain_warden_bane",   "the Unshackled"),
    ("chain_warden_slain",  "the Warden Slayer"),
    ("frenzied_revenant_bane",  "the Ashbound"),
    ("frenzied_revenant_slain", "the Emberreaper"),
    ("ultimate_master",     "the Ultimate"),
    ("ultimate_unleashed",  "the Awakened"),
    ("endless_delver",      "the Depth Seeker"),
    ("counter_master",      "the Counterstriker"),
    ("abyssal_warden_bane",  "the Depthbane"),
    ("abyssal_warden_slain", "the Warden Breaker"),
    ("bond_keeper",         "the Faithful"),
    ("pet_bond_formed",     "the Companion"),
    ("warbreaker_wight_bane",  "the Wightbane"),
    ("warbreaker_wight_slain", "the Guardbreaker"),
    ("gloom_sprite_bane",      "the Sprite Bane"),
    ("gloom_sprite_slain",     "the Sprite Hunter"),
    ("vault_survivor",         "the Vault Survivor"),
    ("treasure_keykeeper",     "the Keykeeper"),
    ("statue_champion",        "the Statue Champion"),
    ("locksmith_master",       "the Master Locksmith"),
    ("hungry_rat_bane",        "the Rat Catcher"),
    ("hungry_rat_slain",       "the Pest Controller"),
    ("bestiary_complete",      "the Bestiary Master"),
    ("cinder_ward_bane",       "the Cinderbane"),
    ("cinder_ward_slain",      "the Warden Quencher"),
    ("numbing_hornet_bane",    "the Hornet's Bane"),
    ("numbing_hornet_slain",   "the Sting Survivor"),
    ("flawless_victor",        "the Immaculate"),
    ("ashbound_titan_bane",    "the Ashbreaker"),
    ("ashbound_titan_slain",   "the Titan Tamer"),
    ("shrine_regular",         "the Fortune Chaser"),
    ("bloodbound",             "the Bloodbound"),
    ("silence_wisp_bane",      "the Wispbane"),
    ("silence_wisp_slain",     "the Unsilenced"),
    ("altar_regular",          "the Faithful"),
    ("vengeful_wraith_bane",   "the Unforgiven"),
    ("vengeful_wraith_slain",  "the Vengeance Breaker"),
    ("high_roller_veteran",    "the High Stakes Veteran"),
    ("branch_route_veteran",   "the Pathfinder"),
    ("venom_adept",            "the Venom Adept"),
    ("stun_master",            "the Stormbound"),
    ("arena_gladiator",        "the Gladiator"),
    ("arena_veteran",          "the Arena Veteran"),
    ("bloodthorn_revenant_bane",   "the Bloodletter"),
    ("bloodthorn_revenant_slain",  "the Bleeding Edge"),
    ("full_ascension",         "the Ascended"),
    ("hero_awakened",          "the Awakened"),
    ("permafrost_wyrm_bane",   "the Frostbane"),
    ("permafrost_wyrm_slain",  "the Ice Breaker"),
    ("boss_rush_veteran",      "the Undefeated"),
    ("boss_rush_champion",     "the Boss Slayer"),
    ("key_collector",          "the Keymaster"),
    ("trial_master",           "the Trialbreaker"),
    ("trial_survivor",         "the Trial Seeker"),
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
# rev165で5人目のRogueを追加。既存4種はいずれもSTR/DEF/HP/EXP/食料という
# 「安定した数値強化」の枠に収まっていたため、Rogueは新フィールド
# crit_bonus(会心率への上乗せ)を持つ最初のキャラクターとし、代わりにDEFを
# 下げるハイリスク・ハイリターンの選択肢にした(既存4種はcrit_bonus=0.0)。
# rev168で6人目のBerserkerを追加。既存5種はDEF/EXP/食料/会心率のいずれかを
# 犠牲にする構成だったが、最大HPそのものを削って攻撃力に全振りする
# 「ガラスの大砲」構成が無かったため、lifemaxをマイナスにする最初の
# キャラクターとして追加した(基礎HP300から-30されても270残るため、
# 装備ボーナスなしの初期状態でも即詰みにはならない)。
# rev171で7人目のProspectorを追加。既存6種はSTR/DEF/HP/EXP/食料/会心率
# のいずれかを犠牲にする構成だったが、アイテム発見率(item_bonus)は
# フロア特性(Bountiful/Scarce)・仲間(Lucky Cat)・スキル(Lucky Find)には
# 既にあるのに、キャラクター自身の個性としては誰も持っていなかった。
# 戦闘力を削って宝探しに全振りする「トレジャーハンター」構成として、
# item_bonusフィールドを新設した最初のキャラクターにした。
CHARACTER_TYPES = {
    "warrior":  {"name": "Warrior",  "desc": "+20 STR, well-rounded fighter",
                 "str": 20, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0},
    "guardian": {"name": "Guardian", "desc": "+15 DEF, +50 Max HP, tougher",
                 "str": 0, "def": 15, "lifemax": 50, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0},
    "scholar":  {"name": "Scholar",  "desc": "+20% EXP gain, but -10 STR",
                 "str": -10, "def": 0, "lifemax": 0, "exp_mult": 1.2, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0},
    "scout":    {"name": "Scout",    "desc": "Food lasts 20% longer",
                 "str": 0, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 0.8, "crit_bonus": 0.0, "item_bonus": 0},
    "rogue":    {"name": "Rogue",    "desc": "+12%pt crit chance, but -5 DEF",
                 "str": 0, "def": -5, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.12, "item_bonus": 0},
    "berserker": {"name": "Berserker", "desc": "+35 STR, but -30 Max HP",
                 "str": 35, "def": 0, "lifemax": -30, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0},
    "prospector": {"name": "Prospector", "desc": "+15%pt item find rate, but -15 STR",
                 "str": -15, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 15},
    # Trader: 既存7種は攻撃/防御/経験値/食料/会心率/アイテム発見率のいずれかに
    # 手を出す構成ばかりで、旅の商人(idx==48)との取引コストという経済寄りの
    # 数値には誰も触れていなかった。trade_mult(merchant_trade_cost()側で
    # .get()経由で参照、他キャラはデフォルト1.0のため無影響)で取引を大幅に
    # 有利にする代わり、既存のfood_multを使って食料の減りを早める弱点を
    # 持たせた(新しいキーを追加せず既存フィールドの再利用で済ませている)。
    "trader":   {"name": "Trader",   "desc": "-30% trades, food -20% faster",
                 "str": 0, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.2, "crit_bonus": 0.0, "item_bonus": 0,
                 "trade_mult": 0.7},
    # Monk(rev182で9人目として追加)。rev174で新設したCounter(反撃)コマンドは
    # 全ヒーロー共通の威力のままで、キャラクター側からCounterを強化する構成が
    # 無かった(Bulwark Floorのようなフロア特性側の強化はあった)。既存8種と
    # 違う新フィールドcounter_mult(counter_def_bonus/cdmgの計算式で
    # .get()経由で参照、他キャラはデフォルト1.0のため無影響)を新設し、
    # 「守ってから殴る」戦い方に全振りする構成にした。
    "monk":     {"name": "Monk",     "desc": "+8 DEF, Counter 50% stronger, but -10 STR",
                 "str": -10, "def": 8, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "counter_mult": 1.5},
    # Cleric(rev186で10人目として追加)。既存9種はSTR/DEF/HP上限/経験値/食料/
    # 会心率/アイテム発見率/取引コスト/Counter倍率のいずれかに手を出す構成
    # ばかりで、歩数ごとの受動回復(heal_per_step、modifier_heal_mult()で
    # Blessed/Barren Floorが既に増減させている値)をキャラクター側から
    # 底上げする構成が無かった。heal_mult(char_params().get()経由で参照、
    # 他キャラはデフォルト1.0のため無影響)を新設し、探索中じわじわ長引く
    # 消耗戦に強い「回復役」の個性を持たせた。
    "cleric":   {"name": "Cleric",   "desc": "+50% passive healing, but -15 STR",
                 "str": -15, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "heal_mult": 1.5},
    # Pyromancer(rev190で11人目として追加)。既存10種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復のいずれかに
    # 手を出す構成ばかりで、消費アイテムの中でも一発逆転力を持つ爆炎石
    # (Blaze Gem、modifier_blaze_dmg_mult()でVolatile/Damp Floorが既に増減
    # させている値)そのものの威力をキャラクター側から底上げする構成が無かった。
    # blaze_mult(爆炎石ダメージ計算箇所で.get()経由で参照、他キャラはデフォルト
    # 1.0のため無影響)を新設し、爆炎石を主軸に据えるハイリスク・ハイリターンな
    # 「爆撃役」の個性を持たせた。
    "pyromancer": {"name": "Pyromancer", "desc": "+30% Blaze gem damage, but -10 STR",
                 "str": -10, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "blaze_mult": 1.3},
    # Duelist(rev192で12人目として追加)。既存11種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復/爆炎石倍率の
    # いずれかに手を出す構成ばかりで、バトルコマンド「集中(Focus)」の一撃倍率
    # (modifier_focus_mult()でFocused Floorが既に増減させている値)を
    # キャラクター側から底上げする構成が無かった。focus_mult(Focus発動時の
    # ダメージ計算箇所で.get()経由で参照、他キャラはデフォルト1.0のため無影響)
    # を新設し、隙を見て一撃に賭ける「決闘者」の個性を持たせた。これで
    # 2列×6行のグリッドがちょうど12/12で埋まっていた。
    "duelist":  {"name": "Duelist",  "desc": "+45% Focus attack damage, but -8 DEF",
                 "str": 0, "def": -8, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "focus_mult": 1.45},
    # Reaver(rev195で13人目として追加)。既存12種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復/爆炎石倍率/
    # Focus倍率のいずれかに手を出す構成ばかりで、Vampiric Floor
    # (modifier_lifesteal_pct()、通常攻撃ヒット時にダメージの一部を回復する
    # フロア限定の特性)と同じ「攻撃した結果プレイヤー自身が回復する」効果を
    # キャラクター側から常時持たせる構成が無かった。lifesteal_pct(通常攻撃の
    # ダメージ計算箇所でmodifier_lifesteal_pct()の戻り値に加算、他キャラは
    # デフォルト0.0のため無影響)を新設し、Vampiric Floorでなくても常に
    # 攻撃のたびに出血で相手を削りながら自分は回復する「血を啜る者」の
    # 個性を持たせた(代償として最大HPを大きく削る)。これで2列×7行の
    # グリッドに13/14人目まで埋まる(あと1枠は将来の増員用に空けてある)。
    "reaver":   {"name": "Reaver",   "desc": "+10% lifesteal on Attack, but -20 Max HP",
                 "str": 0, "def": -6, "lifemax": -20, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "lifesteal_pct": 0.10},
    # Vagabond(rev197で14人目として追加)。既存13種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復/爆炎石倍率/
    # Focus倍率/吸血率のいずれかに手を出す構成ばかりで、逃走成功率
    # (flee_chance_pct()、これまでTranquil/Snared Floorというフロア特性側
    # からしか触れられてこなかった値)をキャラクター側から底上げする構成が
    # 無かった。flee_bonus(flee_chance_pct()で.get()経由で参照、他キャラは
    # デフォルト0のため無影響)を新設し、危険を感じたら迷わず逃げて生き延びる
    # 「旅の渡り者」の個性を持たせた(代償として守りの薄さをDEFで表現)。
    # これで2列×7行のグリッドがちょうど14/14で埋まる。
    "vagabond": {"name": "Vagabond", "desc": "+25%pt flee success chance, but -8 DEF",
                 "str": 0, "def": -8, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "flee_bonus": 25},
    # Apothecary(rev201で15人目として追加)。既存14種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復/爆炎石倍率/
    # Focus倍率/吸血率/逃走成功率のいずれかに手を出す構成ばかりで、秘宝
    # Serpent's Fang(rev198追加)を手に入れるまで敵を毒にする手段が一切
    # 無かった(敵への毒付与は relic_enemy_poison_chance() が100%担っており、
    # キャラクター側から触れる軸が無かった)。poison_bonus(敵への毒付与判定
    # idx==12/67で.get()経由で参照、他キャラはデフォルト0のため無影響)を
    # 新設し、Serpent's Fangを持たない序盤から敵を毒にできる「毒使い」の
    # 個性を持たせた(代償として通常攻撃力を削っている)。これで2列×7行の
    # グリッドが埋まりきったため、2列×8行に拡張した。
    "apothecary": {"name": "Apothecary", "desc": "+18%pt chance to poison enemies, but -12 STR",
                 "str": -12, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "poison_bonus": 18},
    # Marshal(rev204で16人目として追加)。既存15種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復/爆炎石倍率/
    # Focus倍率/吸血率/逃走成功率/毒付与のいずれかに手を出す構成ばかりで、
    # 秘宝Thunderclap Idol(rev202追加)を手に入れるまで敵を気絶させる手段が
    # 一切無かった(敵への気絶付与はrelic_enemy_stun_chance()が100%担っており、
    # キャラクター側から触れる軸が無かった。Apothecaryがpoison_bonusで
    # Serpent's Fangに対して行ったのと同じパターン)。stun_bonus(敵への気絶
    # 付与判定idx==12/67で.get()経由で参照、他キャラはデフォルト0のため無影響)を
    # 新設し、Thunderclap Idolを持たない序盤から敵を気絶させられる「治安官」の
    # 個性を持たせた(代償としてDEFを削っている)。これで2列×8行のグリッドが
    # ちょうど16/16枠で埋まる。
    "marshal":  {"name": "Marshal",  "desc": "+16%pt chance to stun enemies on Attack, but -10 DEF",
                 "str": 0, "def": -10, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "stun_bonus": 16},
    # Ranger(rev209で17人目として追加)。既存16種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復/爆炎石倍率/
    # Focus倍率/吸血率/逃走成功率/毒付与/気絶付与のいずれかに手を出す構成
    # ばかりで、クリティカルヒットの「発生率」(crit_bonus、Rogueが既に採用)
    # ではなく「威力」そのものをキャラクター側から底上げする構成が無かった
    # (modifier_crit_dmg_mult()はこれまでRadiant/Dim Floorという環境要因
    # からしか触れられていなかった)。crit_dmg_bonus(通常攻撃のクリティカル
    # ダメージ計算idx==12で.get()経由で加算参照、他キャラはデフォルト0.0の
    # ため無影響)を新設し、当たれば一撃が跳ね上がる代わりに地力(STR)を
    # 削ったハイリスク・ハイリターンな「一撃必殺」の個性を持たせた。これで
    # 2列×8行のグリッドが埋まりきったため、2列×9行に拡張した。
    "ranger":   {"name": "Ranger",   "desc": "+0.8x critical hit damage multiplier, but -12 STR",
                 "str": -12, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "crit_dmg_bonus": 0.8},
    # Vanguard(rev211で18人目として追加)。既存17種はSTR/DEF/HP上限/経験値/
    # 食料/会心率/アイテム発見率/取引コスト/Counter倍率/受動回復/爆炎石倍率/
    # Focus倍率/吸血率/逃走成功率/毒付与/気絶付与/クリティカルダメージ倍率の
    # いずれかに手を出す構成ばかりで、秘宝Slayer's Emblem(rev208追加)が
    # 通常のステージボス・エコーバトル・ボスラッシュにだけ効かせている
    # 「相手を選ぶ」ダメージボーナス軸(relic_boss_dmg_mult())にキャラクター
    # 側から触れる構成が無かった。boss_dmg_bonus(idx==12/tmr==5の
    # relic_boss_dmg_mult()と同じ箇所で.get()経由で加算参照、他キャラは
    # デフォルト0.0のため無影響。雑魚戦では一切効果が無い代わりに、通常攻撃力
    # そのものを削っている)を新設し、Boss Rush・Arenaのボス級の相手にこそ
    # 本領を発揮する「対ボス特化」の個性を持たせた。これで2列×9行の
    # グリッドがちょうど18/18枠で埋まる。
    "vanguard": {"name": "Vanguard", "desc": "+20% damage against bosses, but -12 STR",
                 "str": -12, "def": 0, "lifemax": 0, "exp_mult": 1.0, "food_mult": 1.0, "crit_bonus": 0.0, "item_bonus": 0,
                 "boss_dmg_bonus": 0.20},
}
CHARACTER_ORDER = ["warrior", "guardian", "scholar", "scout", "rogue", "berserker", "prospector", "trader", "monk", "cleric", "pyromancer", "duelist", "reaver", "vagabond", "apothecary", "marshal", "ranger", "vanguard"]
HERO_GRID_ROWS = 9  # キャラクター選択画面(idx==49)のグリッド行数。2列×9行=18枠。rev204のMarshal追加で2列×8行(16枠)が埋まりきった後、rev209のRanger追加で2列×9行に拡張し、rev211のVanguard追加でちょうど18/18枠が埋まった(次の増員では行の追加が必要)。
selected_character = "warrior"

# --- 主人公専用の必殺技(Ultimate) ---
# バトルコマンドに新設した「Ultimate」で発動する、キャラクターごとに全く異なる
# 一撃。既存キャラクターの個性(Warriorは万能、Guardianは頑丈、Scholarは
# 知識、Scoutは身軽さ、Rogueはハイリスク・ハイリターン)をそのまま必殺技の
# 演出にも反映させ、5人それぞれ「使ってみたい」と思える固有ムーブになるように
# した。mult/bonus_randは通常攻撃(pl_str + 乱数)よりずっと大きい一撃を作るための
# 倍率・加算乱数の上限。heal_pctを持つキャラは追加でHPも回復する。
ULTIMATE_DEFS = {
    "warrior":  {"name": "Rampage",         "mult": 3.2, "bonus_rand": 150},
    "guardian": {"name": "Guardian's Wrath", "mult": 1.8, "bonus_rand": 60, "heal_pct": 0.15},
    "scholar":  {"name": "Arcane Overload",  "mult": 1.6, "bonus_rand": 40, "lv_bonus": 10},
    "scout":    {"name": "Piercing Shot",    "mult": 2.4, "bonus_rand": 80},
    "rogue":    {"name": "Assassinate",      "mult": 2.6, "bonus_rand": 120},
    # BerserkerはHPを削って攻撃力に全振りする構成なので、必殺技も5人の中で
    # 最大の倍率にして「ハイリスク・ハイリターン」を一撃の重さにも反映させた。
    "berserker": {"name": "Bloodrage",      "mult": 3.8, "bonus_rand": 170},
    # ProspectorはSTRを削っているため必殺技倍率は控えめだが、一発逆転の
    # 「大穴」感を出すためbonus_randの振れ幅を大きくした(最低保証は低いが、
    # 運が良ければ他キャラのUltimateに匹敵する一撃になる)。
    "prospector": {"name": "Fortune's Gambit", "mult": 2.0, "bonus_rand": 180},
    # Traderは攻守どちらも底上げしていないため必殺技の倍率もScout同様の中堅
    # 水準に留め、代わりに命中打点のブレ(bonus_rand)をやや大きめにしている。
    "trader":   {"name": "Windfall Strike",  "mult": 2.2, "bonus_rand": 90},
    # MonkはCounter特化で通常のSTRを削っている分、必殺技は堅実な中堅倍率に
    # 留め、代わりに瞑想による回復(heal_pct)でGuardianと同じ「守り」の
    # 個性を必殺技側にも反映させた。
    "monk":     {"name": "Iron Palm",        "mult": 2.0, "bonus_rand": 70, "heal_pct": 0.12},
    # Clericは通常攻撃に振っていない分、必殺技はGuardian/Monkと同じ「守り」
    # 寄りの控えめな倍率に留め、代わりにheal_pctを5人の中で最大にして
    # 「回復役」の個性を必殺技側にも反映させた。
    "cleric":   {"name": "Divine Restoration", "mult": 1.5, "bonus_rand": 50, "heal_pct": 0.25},
    # Pyromancerは爆炎石特化で通常のSTRを削っている分、必殺技は他キャラより
    # 高めの倍率にして「攻めに全振り」の個性を必殺技側にも反映させた。
    "pyromancer": {"name": "Cinderburst",   "mult": 2.4, "bonus_rand": 100},
    # DuelistはFocus特化でDEFを削っている分、必殺技は一撃離脱のハイリスク・
    # ハイリターンな高めの倍率にした。
    "duelist":  {"name": "Riposte Flourish", "mult": 2.7, "bonus_rand": 130},
    # Reaverは通常攻撃の吸血が持ち味なので、必殺技も同じ吸血のテーマを
    # 一撃に凝縮し、Cleric/Guardian/Monkに次ぐ高めのheal_pctを持たせた
    # (削った最大HPを必殺技一発でまとめて取り戻せる、攻めながら守る個性)。
    "reaver":   {"name": "Crimson Feast",   "mult": 2.3, "bonus_rand": 90, "heal_pct": 0.20},
    # Vagabondは守りを削って逃げ足の速さに全振りする構成なので、必殺技は
    # 一撃離脱で隙を突く読みにくさをbonus_randの大きな振れ幅で表現した。
    "vagabond": {"name": "Vanishing Strike", "mult": 2.2, "bonus_rand": 140},
    # Apothecaryは通常攻撃力(STR)を削って毒付与に全振りする構成なので、
    # 必殺技も他キャラより控えめな中堅倍率に留めている(この一撃自体も
    # idx==12に合流するため、poison_bonusによる毒付与判定はUltimateでも
    # 同じように働く)。
    "apothecary": {"name": "Toxic Brew",    "mult": 2.1, "bonus_rand": 80},
    # Marshalは通常攻撃のDEFを削って気絶付与に全振りする構成なので、
    # 必殺技も他キャラより控えめな中堅倍率に留めている(この一撃自体も
    # idx==12に合流するため、stun_bonusによる気絶付与判定はUltimateでも
    # 同じように働く)。
    "marshal":  {"name": "Iron Verdict",    "mult": 2.0, "bonus_rand": 80},
    # Rangerは通常攻撃のクリティカルダメージ倍率が持ち味だが、必殺技
    # (idx==12/tmr=4に合流)自体はクリティカル判定を経由しないため、その分を
    # 補うようDuelist/Reaverに次ぐ高めの倍率にして「一撃必殺」の個性を
    # 必殺技側にも反映させた。
    "ranger":   {"name": "Kill Shot",       "mult": 2.6, "bonus_rand": 100},
    # Vanguardは通常のSTRを削って対ボス特化にした構成なので、必殺技も
    # 雑魚戦では他キャラよりやや控えめな中堅倍率に留めているが、この一撃自体も
    # idx==12に合流するため、boss_dmg_bonusによるボス戦ダメージ底上げは
    # Ultimateでも同じように働き、ボス級の相手にだけ真価を発揮する。
    "vanguard": {"name": "Giant's Bane",    "mult": 2.1, "bonus_rand": 80},
}
ULTIMATE_COMBO_REQUIREMENT = 5  # このコンボ数に達すると[U]ltimateが解放される

def ultimate_def():
    return ULTIMATE_DEFS.get(selected_character, ULTIMATE_DEFS["warrior"])


# --- 新システム「ヒーロー覚醒(Hero Awakening)」(rev206追加) ---
# これまで16人のヒーローは選ぶ個性(STR/DEF/crit_bonus等)が固定のままで、
# 「主人公をどんどんかっこよくしていく」方針に対して、キャラクター自身が
# 育っていく手応えが無かった(スキルツリー・秘宝・護符はすべてセーブデータ
# 側の成長で、キャラクター自体は初日からずっと同じ性能のまま)。ボスを
# 倒した瞬間、そのキャラクターでの初めてのボス撃退なら永久に「覚醒」し、
# 以後(このセーブに限らず、そのキャラクターIDを選ぶたび毎回)常時
# +6 STR/+4 DEF/+20 Max HPの永続ボーナスを得る。achievements.jsonに
# 覚醒済みキャラのリストを保存するため、achievements/statsと同じ
# 「解除したら二度と失われない」永続要素として扱う。
AWAKENING_STR_BONUS = 6
AWAKENING_DEF_BONUS = 4
AWAKENING_LIFEMAX_BONUS = 20

def is_character_awakened(char_id=None):
    char_id = char_id if char_id is not None else selected_character
    return char_id in load_achievements().get("awakened_characters", [])

def awaken_character(char_id):
    """ボス撃破(idx==26)で呼ばれる。そのキャラクターが初めてボスを倒したなら
    覚醒させ、専用トースト(既存の実績トーストキューを流用し、表示中なら
    順番待ちにする)とジングルで気づかせる。既に覚醒済みなら何もしない。"""
    global achievement_toast_label, achievement_toast_timer, achievement_sound_pending
    global _current_title_dirty
    data = load_achievements()
    awakened = list(data.get("awakened_characters", []))
    if char_id in awakened:
        return
    awakened.append(char_id)
    data["awakened_characters"] = awakened
    save_achievements(data)
    record_stat("characters_awakened_count")
    _current_title_dirty = True
    hero_name = CHARACTER_TYPES.get(char_id, {}).get("name", char_id)
    label = f"{hero_name} has Awakened!"
    if achievement_toast_timer > 0:
        achievement_toast_queue.append(label)
    else:
        achievement_toast_label = label
        achievement_toast_timer = ACHIEVEMENT_TOAST_FRAMES
    achievement_sound_pending = True
    unlock_achievement("hero_awakened")
    if len(awakened) >= len(CHARACTER_ORDER):
        unlock_achievement("full_ascension")

def char_params():
    base = dict(CHARACTER_TYPES.get(selected_character, CHARACTER_TYPES["warrior"]))
    if is_character_awakened():
        base["str"] = base.get("str", 0) + AWAKENING_STR_BONUS
        base["def"] = base.get("def", 0) + AWAKENING_DEF_BONUS
        base["lifemax"] = base.get("lifemax", 0) + AWAKENING_LIFEMAX_BONUS
    return base

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
        data.setdefault("awakened_characters", [])
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
    (draw_achievement_toast)で目立たせる。
    【バグ修正】従来はバナー表示中に別の実績が解除されると、ラベルと
    タイマーを即座に上書きしてしまい、表示中だった実績の名前が画面に
    出ることなく消えていた(例えば同フレームで複数の累積実績のしきい値を
    同時にまたいだ場合に発生しうる)。表示中はachievement_toast_queueに
    積んでおき、draw_achievement_toast側で現在のバナーが終わるたびに
    次のラベルを取り出して表示するようにし、複数解除時も1つずつ
    順番に見られるようにした。
    【バグ修正】READMEには「実績解除トースト表示の瞬間にレベルアップジングルを
    再生する」と記載されていたが、実際にはどこもse[]を再生しておらず記載と
    実装が食い違っていたため、achievement_sound_pendingを新規解除時に
    立てるようにした(main()側でse[4]を再生して消費する)。"""
    global _current_title_dirty, achievement_toast_label, achievement_toast_timer
    global achievement_sound_pending
    data = load_achievements()
    if not data.get(key, False):
        data[key] = True
        save_achievements(data)
        _current_title_dirty = True
        label = ACHIEVEMENT_LABELS.get(key, key)
        if achievement_toast_timer > 0:
            achievement_toast_queue.append(label)
        else:
            achievement_toast_label = label
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

# --- 秘宝(Relic)システム ---
# これまでプレイヤーの永続的な強化は「ボス撃破時の固定ボーナス」「装備アイテム
# (指輪/アミュレット)」しか無く、探索を重ねるごとに増えていく所持品・収集要素が
# 無かった。ボス撃破時にまれに手に入る「秘宝」を新設し、集めるほど恒久的なパッシブ
# ボーナス(クリティカル率/アイテム発見率/獲得EXP)が積み重なるようにする
# (エコーバトル(idx==60)は周回可能な練習戦のため対象外。通常のボス撃破(idx==26)
# だけで手に入る特別な報酬にしている)。
RELIC_DROP_CHANCE = 30  # ボス撃破時に未所持の秘宝を1つ手に入れる確率(%)
RELIC_DEFS = [
    {"key": "ember_charm",    "name": "Ember Charm",    "desc": "+6%pt critical hit chance",  "effect": "crit", "value": 0.06},
    {"key": "phantom_lens",   "name": "Phantom Lens",   "desc": "+10%pt critical hit chance", "effect": "crit", "value": 0.10},
    {"key": "lucky_clover",   "name": "Lucky Clover",   "desc": "+8%pt item find rate",       "effect": "item", "value": 8},
    {"key": "golden_compass", "name": "Golden Compass", "desc": "+14%pt item find rate",      "effect": "item", "value": 14},
    {"key": "sages_quill",    "name": "Sage's Quill",   "desc": "+15% EXP gained",            "effect": "exp",  "value": 0.15},
    {"key": "ancient_tome",   "name": "Ancient Tome",   "desc": "+25% EXP gained",             "effect": "exp",  "value": 0.25},
    # rev182で追加。既存の秘宝はcrit/item/expの3軸がそれぞれ2種類ずつと
    # いう「同じ軸を数値違いで増やすだけ」の構成が続いていたため、今回は
    # まだどの秘宝も触れていなかった探索中の移動速度という新しい軸を追加した。
    {"key": "swift_sandals",  "name": "Swift Sandals",  "desc": "+8% move speed",             "effect": "speed", "value": 0.08},
    {"key": "windwalker_charm", "name": "Windwalker Charm", "desc": "+14% move speed",         "effect": "speed", "value": 0.14},
    # rev197で追加。既存の秘宝はcrit/item/exp/speedの4軸だったが、
    # 逃走成功率(flee_chance_pct()、これまでフロア特性(Tranquil/Snared)と
    # 今回追加のキャラクター(Vagabond)しか触れていなかった値)を秘宝側から
    # 底上げする構成がまだ無かった。まだ誰も触れていなかった軸として追加した。
    {"key": "featherlight_cloak", "name": "Featherlight Cloak", "desc": "+12%pt flee success chance", "effect": "flee", "value": 12},
    # rev198で追加。秘宝はcrit/item/exp/speed/fleeの5軸すべてが「プレイヤー
    # 自身を強くする」自己バフで、これまで秘宝側から敵に影響を及ぼす軸が
    # 一つも無かった。毒(poison)はこれまでモンスターがプレイヤーに与える
    # 一方通行の状態異常だったが、この秘宝で初めてプレイヤーの攻撃が敵を
    # 毒にできるようになる、これまでと逆方向の新しい軸。
    {"key": "serpents_fang", "name": "Serpent's Fang", "desc": "Attacks have a 20%pt chance to poison the enemy", "effect": "poison", "value": 20},
    # rev199で追加。秘宝はcrit/item/exp/speed/flee/poisonの6軸すべてが通常攻撃
    # (Attack)・逃走・探索など既存コマンドの底上げで、rev174で追加した反撃
    # (Counter)コマンドにはフロア特性(Bulwark Floor)しか触れておらず、秘宝側
    # から強化する軸がまだ無かった。Bulwark Floorと同じ被ダメージ軽減量・
    # 反撃ダメージの両方を底上げする軸として追加し、Bulwark Floor+この秘宝を
    # 組み合わせるとさらに強力なCounterになる(Monk固有のcounter_multとも
    # 重複して掛け算される)。
    {"key": "wardens_bulwark", "name": "Warden's Bulwark", "desc": "+25% Counter's damage reduction and retaliation damage", "effect": "counter", "value": 0.25},
    # rev200で追加。秘宝はcrit/item/exp/speed/flee/poison/counterの7軸すべてが
    # 探索・逃走・戦闘のいずれかを底上げする軸で、歩数ごとの受動回復
    # (heal_per_step)はこれまでフロア特性(Blessed/Barren Floor)にしか
    # 触れられておらず、秘宝側から底上げする軸がまだ無かった。まだ誰も
    # 触れていなかった軸として追加した。
    {"key": "vital_charm", "name": "Vital Charm", "desc": "+40% passive healing from steps", "effect": "heal", "value": 0.40},
    # rev202で追加。秘宝はcrit/item/exp/speed/flee/poison/counter/healの8軸すべてが
    # 「ダメージ量・確率・回復量」のどれかを底上げする軸で、状態異常は毒(poison)
    # しか無く、しかも毒は「じわじわ削る」持続ダメージ型のみだった。気絶(stun)は
    # ダメージを一切伴わない初めての「敵の行動そのものを1ターン封じる」軸で、
    # 毒と違い数値を強めるほど嬉しい系統ではなく、じわじわ削るビルドとは別の
    # 「安全に被弾を減らす」プレイスタイルを提示する新しい状態異常。
    {"key": "thunderclap_idol", "name": "Thunderclap Idol", "desc": "Attacks have a 18%pt chance to stun the enemy for 1 turn", "effect": "stun", "value": 18},
    # rev203で追加。秘宝はcrit/item/exp/speed/flee/poison/counter/heal/stunの9軸
    # すべてが戦闘・逃走・回復のいずれかを底上げする軸で、put_event()が
    # 宝箱タイル自体の出現しやすさ(treasure_weight、Opulent/Meager Floorだけが
    # 触れていた軸)を底上げする秘宝側の手段がまだ無かった。まだ誰も
    # 触れていなかった軸として追加した。
    {"key": "prospectors_ledger", "name": "Prospector's Ledger", "desc": "+20% treasure chest frequency", "effect": "treasure", "value": 0.20},
    # rev204で追加。秘宝はcrit/item/exp/speed/flee/poison/counter/heal/stun/treasureの
    # 10軸すべてが探索・戦闘・回復・宝箱のいずれかを底上げする軸で、消費アイテムの
    # 中でも一発逆転力を持つ爆炎石(Blaze Gem、キャラクターPyromancerの
    # blaze_multやフロア特性Volatile/Damp Floorが既に増減させている値)そのものの
    # 威力を秘宝側から底上げする手段がまだ無かった。まだ誰も触れていなかった軸として
    # 追加した。
    {"key": "cinder_idol", "name": "Cinder Idol", "desc": "+25% Blaze Gem damage", "effect": "blaze", "value": 0.25},
    # rev206で追加。秘宝はcrit/item/exp/speed/flee/poison/counter/heal/stun/
    # treasure/blazeの11軸すべてがプレイヤーを強くする・敵を弱くする一方通行の
    # 軸で、プレイヤー自身が受ける状態異常を軽減する軸は、スキル(Antidote Body、
    # skill_poison_mult)にしか無かった(秘宝側からはまだ触れられていなかった)。
    # 出血(pl_bleed)は「どんな対策を積んでも一切軽減できない」新設計の持続
    # ダメージとして意図的に据え置き(rev205のBloodthorn Revenant導入時の設計
    # 意図)、代わりに元から軽減可能な毒(pl_poison)側にAntidote Bodyと同じ
    # 掛け算式で乗る新しい軸として追加した。
    {"key": "serpents_ward", "name": "Serpent's Ward", "desc": "-25% self-poison damage taken", "effect": "poison_resist", "value": 0.25},
    # rev208で追加。秘宝はcrit/item/exp/speed/flee/poison/counter/heal/stun/
    # treasure/blaze/poison_resistの12軸すべてがフロア道中の雑魚戦にも等しく
    # 効く汎用強化で、新設した「ボスラッシュ」を含むボス級の相手だけにさらに
    # 効く軸がまだ無かった。通常攻撃・爆炎石・必殺技のダメージがボス戦
    # (通常のステージボス・エコーバトル・ボスラッシュ)の間だけ底上げされる、
    # 初めての「相手を選ぶ」秘宝として追加した。
    {"key": "slayers_emblem", "name": "Slayer's Emblem", "desc": "+15% damage against bosses", "effect": "boss_dmg", "value": 0.15},
]
RELIC_LABELS = {r["key"]: r["name"] for r in RELIC_DEFS}
_relics_cache = None

def load_relics():
    """achievements.jsonのload_achievements()と同じ、プロセス内キャッシュ+
    書き込み時だけ更新するパターン。"""
    global _relics_cache
    if _relics_cache is None:
        try:
            with open("relics.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        for relic in RELIC_DEFS:
            data.setdefault(relic["key"], False)
        _relics_cache = data
    return dict(_relics_cache)

def save_relics(data):
    global _relics_cache
    _relics_cache = dict(data)
    try:
        with open("relics.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        _log_io_error("save_relics", e)

def unlock_relic(key):
    """新しい秘宝を手に入れた時に呼ぶ。実績のトースト演出(draw_achievement_toast)
    と同じ表示中キュー(relic_toast_queue)パターンで、複数同時取得時も
    1つずつ順番に表示する。戻り値は今回新規に手に入れたかどうか。"""
    global relic_toast_label, relic_toast_timer, relic_sound_pending
    data = load_relics()
    if data.get(key, False):
        return False
    data[key] = True
    save_relics(data)
    label = RELIC_LABELS.get(key, key)
    if relic_toast_timer > 0:
        relic_toast_queue.append(label)
    else:
        relic_toast_label = label
        relic_toast_timer = RELIC_TOAST_FRAMES
    relic_sound_pending = True
    return True

def relic_crit_bonus():
    data = load_relics()
    return sum(r["value"] for r in RELIC_DEFS if r["effect"] == "crit" and data.get(r["key"], False))

def relic_item_bonus():
    data = load_relics()
    return sum(r["value"] for r in RELIC_DEFS if r["effect"] == "item" and data.get(r["key"], False))

def relic_exp_mult():
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "exp" and data.get(r["key"], False))
    return 1.0 + bonus

def relic_speed_mult():
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "speed" and data.get(r["key"], False))
    return 1.0 + bonus

def relic_flee_bonus():
    """item_bonus/modifier_flee_bonus()と同じく%pt単位の整数を直接返す軸。"""
    data = load_relics()
    return sum(r["value"] for r in RELIC_DEFS if r["effect"] == "flee" and data.get(r["key"], False))

def relic_enemy_poison_chance():
    """flee_bonus同様%pt単位の整数を返す軸。Serpent's Fangを持っていない
    間は0で、敵への毒付与判定(idx==12/67)は常にこの値を参照する。"""
    data = load_relics()
    return sum(r["value"] for r in RELIC_DEFS if r["effect"] == "poison" and data.get(r["key"], False))

def relic_counter_mult():
    """exp_mult/speed_mult同様1.0を基準にした倍率軸。Warden's Bulwarkを
    持っていない間は1.0で、反撃(Counter、idx==67)の被ダメージ軽減量・
    反撃ダメージの計算式にmodifier_counter_bonus()・char_params()の
    counter_multと並んでそのまま掛け算される。"""
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "counter" and data.get(r["key"], False))
    return 1.0 + bonus

def relic_heal_mult():
    """exp_mult/speed_mult同様1.0を基準にした倍率軸。Vital Charmを持っていない
    間は1.0で、歩数ごとの受動回復(heal_per_step)にmodifier_heal_mult()・
    char_params()のheal_multと並んでそのまま掛け算される。"""
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "heal" and data.get(r["key"], False))
    return 1.0 + bonus

def relic_enemy_stun_chance():
    """flee_bonus/enemy_poison_chance同様%pt単位の整数を返す軸。Thunderclap Idolを
    持っていない間は0で、敵への気絶付与判定(idx==12/67)は常にこの値を参照する。"""
    data = load_relics()
    return sum(r["value"] for r in RELIC_DEFS if r["effect"] == "stun" and data.get(r["key"], False))

def relic_treasure_weight_mult():
    """speed_mult/exp_mult同様1.0を基準にした倍率軸。Prospector's Ledgerを
    持っていない間は1.0で、put_event()の宝箱タイル出現weightにmodifier_treasure_weight_mult()
    と並んでそのまま掛け算される。"""
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "treasure" and data.get(r["key"], False))
    return 1.0 + bonus

def relic_blaze_dmg_mult():
    """speed_mult/exp_mult同様1.0を基準にした倍率軸。Cinder Idolを持っていない
    間は1.0で、爆炎石(Blaze Gem)のダメージ計算式にmodifier_blaze_dmg_mult()・
    char_params()のblaze_multと並んでそのまま掛け算される。"""
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "blaze" and data.get(r["key"], False))
    return 1.0 + bonus

def relic_poison_resist_mult():
    """他のrelic_*_multと違い、1.0から減算する軽減倍率軸。Serpent's Wardを
    持っていない間は1.0で、プレイヤー自身が毒状態(pl_poison)から受ける
    ダメージ計算式(探索中の歩数ダメージ・バトルターンダメージの両方)に
    skill_poison_mult(Antidote Body)と並んでそのまま掛け算される。
    skill_poison_mult同様、下限0.2でクランプし毒ダメージが0になる事故を防ぐ。"""
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "poison_resist" and data.get(r["key"], False))
    return max(0.2, 1.0 - bonus)

def relic_boss_dmg_mult():
    """exp_mult/speed_mult同様1.0を基準にした倍率軸。Slayer's Emblemを持って
    いない間は1.0で、通常攻撃・爆炎石・必殺技のダメージ計算式(idx==12)に
    in_boss_battle/in_echo_battleのいずれかがTrueの時だけ掛け算される
    (ボスラッシュはstart_boss_rush()でin_boss_battleを流用しているため個別の
    判定は不要。雑魚戦では効果が無い、初めて相手を選ぶ秘宝)。"""
    data = load_relics()
    bonus = sum(r["value"] for r in RELIC_DEFS if r["effect"] == "boss_dmg" and data.get(r["key"], False))
    return 1.0 + bonus

# --- 護符(Charm)システム ---
# 秘宝(Relic)は見つけたものが全部自動で恒久的に積み重なる「集めるほど強くなる」
# コレクションだったが、プレイヤー自身が選んで組み合わせを変える「装備」の
# 要素がまだ無かった。護符はダンジョンの中にまれに現れる「護符の祠」に
# 触れることで手に入り(秘宝のようなボス撃破報酬とは別の入手経路)、
# 一度に1つだけ身につけられる。どれを身につけるかはRecordsメニューの
# 新しい画面(`[C] Charms`)からいつでも無料で切り替えられ、いずれも
# 一方の数値を強めるかわりにもう一方を弱める「一長一短」の組み合わせなので、
# 秘宝の「持っているだけ良くなる」設計とは違う、プレイスタイルを選ぶ
# 駆け引きになる(効果の軸自体は安全に検証済みのcrit/item/exp/speedの
# 4種類を流用し、複数個所に散らばる計算式を新設せずに済むようにした)。
CHARM_DEFS = [
    {"key": "charm_fury",     "name": "Charm of Fury",     "desc": "+10%pt crit chance, -10%pt item find",
     "crit": 0.10, "item": -10, "exp": 0.0, "speed": 0.0},
    {"key": "charm_fortune",  "name": "Charm of Fortune",  "desc": "+16%pt item find, -6%pt crit chance",
     "crit": -0.06, "item": 16, "exp": 0.0, "speed": 0.0},
    {"key": "charm_haste",    "name": "Charm of Haste",    "desc": "+18% move speed, -10% EXP gained",
     "crit": 0.0, "item": 0, "exp": -0.10, "speed": 0.18},
    {"key": "charm_wisdom",   "name": "Charm of Wisdom",   "desc": "+20% EXP gained, -12% move speed",
     "crit": 0.0, "item": 0, "exp": 0.20, "speed": -0.12},
    # 既存4種はcrit/item/exp/speedの2軸ずつの組み合わせに留まっており、
    # flee_chance_pct()(フロア特性Tranquil/Snared・キャラクターVagabond・
    # 秘宝Featherlight Cloakがすでに絡む軸)には護符側からまだ触れられて
    # いなかった。「攻めるか、逃げの保険を持つか」という新しい一長一短として、
    # 逃走成功率を強めるかわりに宝箱の中身の質を犠牲にする組み合わせを追加した
    # (既存関数と同じ.get()経由の参照にして、"flee"キーを持たない旧3種の
    # 護符でも安全に0扱いされるようにした)。
    {"key": "charm_wanderer", "name": "Charm of the Wanderer", "desc": "+14%pt flee success, -8%pt item find",
     "crit": 0.0, "item": -8, "exp": 0.0, "speed": 0.0, "flee": 14},
    # 今回新設した状態異常「凍結(pl_frozen、Permafrost Wyrmが与えてくる)」は
    # どんなスキル・フロア特性でも軽減できない設計(出血と同じ「対策の無い」
    # 駆け引き)にしたが、Bloodslick Floorが出血に対して行ったのと同じ
    # 「専用のフロア特性で確率を上乗せする」ハイリスク側だけでは、凍結を
    # 軽減したいプレイヤー側の選択肢が一切無くなってしまう。護符側から
    # 初めて状態異常の付与確率そのものを軽減する新しい軸として追加した
    # (charm_wanderer同様、"freeze_resist"キーを持たない旧5種の護符でも
    # .get()で安全に0扱いされる)。重い氷結対策の代償として、移動速度を
    # 落とすトレードオフを選んだ(charm_haste/charm_wisdomと同じspeed軸だが、
    # 逆方向の組み合わせ)。
    {"key": "charm_frostward", "name": "Charm of Frost Ward", "desc": "+20%pt freeze resist, -10% move speed",
     "crit": 0.0, "item": 0, "exp": 0.0, "speed": -0.10, "freeze_resist": 20},
]
CHARM_LABELS = {c["key"]: c["name"] for c in CHARM_DEFS}
_charms_cache = None

def load_charms():
    """load_relics()と同じ、プロセス内キャッシュ+書き込み時だけ更新するパターン。
    "found"は所持している護符の辞書、"equipped"は現在装備中の護符キー(Noneなら未装備)。"""
    global _charms_cache
    if _charms_cache is None:
        try:
            with open("charms.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        data.setdefault("found", {})
        for charm in CHARM_DEFS:
            data["found"].setdefault(charm["key"], False)
        data.setdefault("equipped", None)
        if data["equipped"] is not None and not data["found"].get(data["equipped"], False):
            data["equipped"] = None
        _charms_cache = data
    return {"found": dict(_charms_cache["found"]), "equipped": _charms_cache["equipped"]}

def save_charms(data):
    global _charms_cache
    _charms_cache = {"found": dict(data["found"]), "equipped": data["equipped"]}
    try:
        with open("charms.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        _log_io_error("save_charms", e)

def unlock_charm(key):
    """護符の祠で新しい護符を手に入れた時に呼ぶ。unlock_relicと同じトースト
    キューパターンで、見つけた瞬間に自動で装備はしない(既に別の護符を
    使い込んでいる場合に、勝手に組み合わせを変えられて困らないようにするため)。
    戻り値は今回新規に手に入れたかどうか。"""
    global charm_toast_label, charm_toast_timer, charm_sound_pending
    data = load_charms()
    if data["found"].get(key, False):
        return False
    data["found"][key] = True
    save_charms(data)
    label = CHARM_LABELS.get(key, key)
    if charm_toast_timer > 0:
        charm_toast_queue.append(label)
    else:
        charm_toast_label = label
        charm_toast_timer = CHARM_TOAST_FRAMES
    charm_sound_pending = True
    return True

def equip_charm(key):
    """keyがNoneなら装備解除、そうでなければ所持している護符に限り装備を切り替える。
    切り替え自体はいつでも無料・即座に反映される(ペナルティなし)。"""
    data = load_charms()
    if key is not None and not data["found"].get(key, False):
        return
    data["equipped"] = key
    save_charms(data)

def get_equipped_charm():
    """現在装備中の護符の定義(dict)を返す。未装備ならNone。"""
    key = load_charms()["equipped"]
    if key is None:
        return None
    for c in CHARM_DEFS:
        if c["key"] == key:
            return c
    return None

def charm_crit_bonus():
    c = get_equipped_charm()
    return c["crit"] if c else 0.0

def charm_item_bonus():
    c = get_equipped_charm()
    return c["item"] if c else 0

def charm_exp_mult():
    c = get_equipped_charm()
    return 1.0 + (c["exp"] if c else 0.0)

def charm_speed_mult():
    c = get_equipped_charm()
    return 1.0 + (c["speed"] if c else 0.0)

def charm_flee_bonus():
    """flee_bonus同様%pt単位の整数を返す軸。"flee"キーを持たない旧護符
    (Fury/Fortune/Haste/Wisdom)を装備している間や未装備の間は.get()で
    安全に0を返す。"""
    c = get_equipped_charm()
    return c.get("flee", 0) if c else 0

def charm_freeze_resist_bonus():
    """modifier_freeze_chance_bonus()と加算される、護符側の凍結軽減%pt。
    charm_flee_bonus同様"freeze_resist"キーを持たない旧6種の護符を
    装備している間や未装備の間は.get()で安全に0を返す。"""
    c = get_equipped_charm()
    return c.get("freeze_resist", 0) if c else 0

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
    ("ember_forges_used", "Ember Forges used"),
    ("hidden_boss_defeats", "Hidden Boss (??? The Unbound) defeats"),
    ("true_hidden_boss_defeats", "True Hidden Boss (??? The Voidcrowned) defeats"),
    ("voidforged_golems_defeated", "Voidforged Golems defeated"),
    ("mirror_wraiths_defeated", "Mirror Wraiths defeated"),
    ("hollow_widows_defeated", "Hollow Widows defeated"),
    ("chain_wardens_defeated", "Chain Wardens defeated"),
    ("ultimates_used", "Ultimate moves used"),
    ("deepest_endless_floor", "Deepest floor reached in Endless Depths"),
    ("counters_used", "Counter attacks landed"),
    ("secret_vaults_found", "Secret vaults found"),
    ("close_calls", "Battles won with less than 15% HP remaining"),
    ("no_damage_wins", "Battles won without taking damage"),
    ("total_lifesteal_healed", "Total HP healed via lifesteal"),
    ("poisoned_enemies_defeated", "Poisoned enemies defeated"),
    ("daily_challenges_cleared", "Daily Challenges cleared (distinct days)"),
    ("branch_routes_found", "Shortcut passages found"),
    ("arena_runs", "Arena of Trials runs played"),
    ("arena_best_round", "Arena of Trials best round reached"),
    ("arena_total_rounds_cleared", "Arena of Trials rounds cleared (all runs combined)"),
    ("characters_awakened_count", "Heroes Awakened"),
    ("trial_posts_entered", "Trial Posts entered"),
    ("trial_posts_cleared", "Trial Posts cleared"),
]

playtime_ms_accum = 0
steps_taken_accum = 0
# 今回の1回のプレイ(ゲームオーバー画面のリキャップ表示用)だけの通算値。
# 通算記録(total_kills/total_damage_dealt)とは別に、新しくゲームを始める
# たびに0へリセットされる。
run_kills = 0
run_damage_dealt = 0

SETTINGS_FILE = "settings.json"

def load_settings():
    """settings.jsonからBGM/SE音量とミュート状態を読み込む。ファイルが無い/
    壊れている場合はデフォルト(1.0=フル音量、ミュートOFF)のまま何もしない。"""
    global bgm_volume, se_volume, muted, screen_shake_enabled, screen_flash_enabled, low_hp_pulse_enabled
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        bgm_volume = max(0.0, min(1.0, float(data.get("bgm_volume", 1.0))))
        se_volume = max(0.0, min(1.0, float(data.get("se_volume", 1.0))))
        muted = bool(data.get("muted", False))
        screen_shake_enabled = bool(data.get("screen_shake_enabled", True))
        screen_flash_enabled = bool(data.get("screen_flash_enabled", True))
        low_hp_pulse_enabled = bool(data.get("low_hp_pulse_enabled", True))
    except Exception:
        pass

def save_settings():
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"bgm_volume": bgm_volume, "se_volume": se_volume, "muted": muted,
                       "screen_shake_enabled": screen_shake_enabled,
                       "screen_flash_enabled": screen_flash_enabled,
                       "low_hp_pulse_enabled": low_hp_pulse_enabled}, f)
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

def check_bestiary_complete():
    """図鑑(Bestiary)の敵・ボス・アイテムを1種類でも欠かさず全種発見したかどうかを
    確認し、揃っていれば実績「Bestiary Master」を解除する。record_enemy_seen/
    record_item_seen/record_boss_seenのいずれかで新規発見があった直後にだけ
    呼ばれるため、毎フレームは走らず、既に解除済みならunlock_achievement側で
    何もしないので二重解除の心配もない。"""
    data = load_bestiary()
    if all(data["enemies"]) and all(data["items"]) and all(data["bosses"]):
        unlock_achievement("bestiary_complete")

def record_enemy_seen(typ_idx):
    if not (0 <= typ_idx < len(EMY_NAME)):
        return
    data = load_bestiary()
    if not data["enemies"][typ_idx]:
        data["enemies"][typ_idx] = True
        save_bestiary(data)
        check_bestiary_complete()

def record_item_seen(treasure_idx):
    if not (0 <= treasure_idx < len(TRE_NAME)):
        return
    data = load_bestiary()
    if not data["items"][treasure_idx]:
        data["items"][treasure_idx] = True
        save_bestiary(data)
        check_bestiary_complete()

def record_boss_seen(boss_idx):
    if not (0 <= boss_idx < len(BOSS_BESTIARY)):
        return
    data = load_bestiary()
    if not data["bosses"][boss_idx]:
        data["bosses"][boss_idx] = True
        save_bestiary(data)
        check_bestiary_complete()

# 図鑑(Bestiary)の詳細表示画面(idx==47)で、いま選択中のモンスター/ボスを覚えておく状態
bestiary_detail_kind = None   # "enemy" または "boss"
bestiary_detail_index = 0
bestiary_detail_img = None    # 選択中の画像(未発見ならNone)
bestiary_detail_seen = False

# --- スキルツリー(レベルアップで得たポイントで永続強化を購入する) ---
# 6本の枝(body/combat/mind/survival/fortune/tactics)、各3段のツリー構造。
# tier2/tier3のスキルは、同じ枝の1つ前の段を1レベル以上習得していないと
# 解放されない。最後に、最初の5枝(body/combat/mind/survival/fortune)すべての
# tier3を1レベル以上習得すると解放される総仕上げの"grandmaster"がある
# (枝をまたぐ本物のツリー構造)。6本目のtactics枝は、そこに合流せず
# 単独で完結する専門特化の枝(Counter/Focus/Ultimateを育てる)として追加した。
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
    # 6本目の枝「Tactics」(今回追加分)。反撃(Counter)/集中(Focus)/必殺技(Ultimate)は
    # rev166〜174で追加された比較的新しいバトルコマンドだが、他5枝(body/combat/mind/
    # survival/fortune)がどれも基礎ステータス(DEF/STR/EXP/食料/視界など)の強化に
    # 特化しているのに対し、これら新コマンドをスキルツリーで直接育てる枝が無かった。
    # 新しいスプライト画像は用意していないため、既存のskill_*.pngアイコンを
    # "icon"フィールドで指定して使い回している(新モンスター/新キャラの色替え
    # パターンと同じ、既存アセット流用の考え方)。
    {"id": "battle_instinct", "name": "Battle Instinct", "branch": "tactics", "tier": 1, "requires": None,
     "desc": "Counter dmg grows/lv", "cost": 1, "max_level": 5, "base": 0.03, "growth": 0.02, "icon": "tough_skin"},
    {"id": "focus_training", "name": "Focus Training", "branch": "tactics", "tier": 2, "requires": "battle_instinct",
     "desc": "Focus dmg grows/lv", "cost": 2, "max_level": 4, "base": 0.03, "growth": 0.02, "icon": "perfect_strike"},
    {"id": "combo_adept",   "name": "Combo Adept",     "branch": "tactics", "tier": 3, "requires": "focus_training",
     "desc": "Ultimate req -1/lv", "cost": 3, "max_level": 2, "base": 1, "growth": 0, "icon": "swift_feet"},
    {"id": "grandmaster",   "name": "Grandmaster",    "branch": "capstone", "tier": 4,
     "requires": ["fortress", "berserker", "sage", "survivor", "perfect_strike"],
     "desc": "One-time boost to every stat", "cost": 5, "max_level": 1, "base": 0, "growth": 0},
]
SKILLS_BY_ID = {sk["id"]: sk for sk in SKILLS}
SKILL_BRANCH_ORDER = ["body", "combat", "mind", "survival", "fortune", "tactics"]
SKILL_ICONS = {sk["id"]: pygame.image.load(f"image/skill_{sk.get('icon', sk['id'])}.png") for sk in SKILLS}

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
# Tacticsの枝(今回追加分)。Counter/Focus/Ultimateはmodifier_*()のフロア特性
# 強化と同じ「加算ボーナス」方式にし、フロア特性(Bulwark/Focused/Overcharged)
# とスキルの伸びを両方同時に載せられるようにしている。
skill_counter_bonus = 0.0
skill_focus_bonus = 0.0
skill_ultimate_req_reduction = 0
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
    global skill_counter_bonus, skill_focus_bonus, skill_ultimate_req_reduction

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
    skill_counter_bonus = cum("battle_instinct")
    skill_focus_bonus = cum("focus_training")
    skill_ultimate_req_reduction = int(round(cum("combo_adept")))

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
    "battle_instinct": lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['battle_instinct'], lv)*100:.0f}% counter",
    "focus_training": lambda lv: f"+{skill_cumulative_effect(SKILLS_BY_ID['focus_training'], lv)*100:.0f}% focus",
    "combo_adept":   lambda lv: f"-{int(round(skill_cumulative_effect(SKILLS_BY_ID['combo_adept'], lv)))} combo req",
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
    "battle_instinct": lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['battle_instinct'], lv+1)*100:.0f}% more",
    "focus_training": lambda lv: f"Next: +{skill_level_contribution(SKILLS_BY_ID['focus_training'], lv+1)*100:.0f}% more",
    "combo_adept":   lambda lv: f"Next: -{int(round(skill_level_contribution(SKILLS_BY_ID['combo_adept'], lv+1)))} more",
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
    # 新しい枝「Tactics」の3スキルを全部カンストさせると専用実績が解除される。
    # 既存の「Grandmaster」(全5枝tier3を1Lv以上)とは別に、1つの枝を
    # 極めきることを評価する初めての実績。
    tactics_ids = ("battle_instinct", "focus_training", "combo_adept")
    if skill_id in tactics_ids and all(
            skill_levels.get(tid, 0) >= SKILLS_BY_ID[tid]["max_level"] for tid in tactics_ids):
        unlock_achievement("combat_sage")

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
VOID_GOLEM_TINT = (150, 120, 215)  # Voidforged Golem(typ27)をIron Golemと
                                    # 見分けられるよう乗算する紫の"void"カラー
MIRROR_WRAITH_TINT = (225, 235, 255)  # Mirror Wraith(typ28)をShadow Wispと
                                       # 見分けられるよう乗算する銀白色の"鏡"カラー
MIRROR_WRAITH_REFLECT_MULT = 0.2  # Mirror Wraithが通常攻撃(Attack)を受けた際、
                                   # 与えたダメージの何割をプレイヤーへ跳ね返すか
HOLLOW_WIDOW_TINT = (245, 245, 235)  # Hollow Widow(typ29)をVenom Spiderと
                                      # 見分けられるよう乗算する病的に白い"生命吸収"カラー
HOLLOW_WIDOW_DRAIN_MULT = 0.35  # Hollow Widowがプレイヤーに攻撃を当てた際、
                                 # 与えたダメージの何割を自分のHPとして吸収するか
CHAIN_WARDEN_TINT = (100, 110, 150)  # Chain Warden(typ30)をBone Reaperと
                                      # 見分けられるよう乗算する鈍い鎖色の"束縛"カラー
CHAIN_WARDEN_BREAK_CHANCE = 40  # Chain Wardenの攻撃がプレイヤーのコンボを
                                 # 断ち切る確率(%)
FRENZIED_REVENANT_TINT = (200, 40, 40)  # Frenzied Revenant(typ31)をCrystal Slimeと
                                          # 見分けられるよう乗算する血のような赤の"狂乱"カラー
FRENZIED_REVENANT_STR_GROWTH = 1.12  # Frenzied Revenantが攻撃するたびにSTRへ
                                       # かかる成長倍率(戦闘が長引くほど危険になる)
ABYSSAL_WARDEN_TINT = (70, 30, 110)  # Abyssal Warden(typ32)をMolten Drakeと
                                      # 見分けられるよう乗算する深い紫黒の"深淵"カラー
ABYSSAL_WARDEN_HEAL_HP_PCT = 0.30    # このHP割合以下になった瞬間に緊急回復が発動
ABYSSAL_WARDEN_HEAL_TARGET_PCT = 0.60  # 緊急回復で回復する先の最大HP割合
WARBREAKER_TINT = (195, 140, 80)  # Warbreaker Wight(typ33)をGlacier Knightと
                                    # 見分けられるよう乗算する鈍い金属的な銅色の"破砕"カラー
GLOOM_SPRITE_TINT = (150, 210, 140)  # Gloom Sprite(typ34)をShadow Wispと
                                       # 見分けられるよう乗算する病的な緑がかった"幻惑"カラー
GLOOM_SPRITE_MIN_FLOOR = 6  # このフロア以降でのみ出現する(フロア1-5は出さない)
# typ35「Hungry Rat」。typ27-34の深層〜中盤専用モンスターとは逆に、フロア1-5
# (GLOOM_SPRITE_MIN_FLOOR未満の帯)には「仕組み持ち」の敵が1体も居らず、
# 一番最初にプレイヤーが出会うのはステータス違いのモンスターだけだった。
# 攻撃を受けると食料(food)を1つかじり取ってくる「空腹」持ちの敵を、初めての
# プレイヤーでも安全に体験できる最序盤帯に追加した。foodは0になると歩数ごとに
# HPが減り始める(starve_dmg)実際に意味のある資源のため、無視して長居すると
# じわじわ損をする一方、倒せば齧られた分を埋め合わせる食料を落とすため、
# 早めに仕留める理由にもなる。
HUNGRY_RAT_TINT = (150, 110, 60)  # Hungry Rat(typ35)をRed Slimeと見分けられる
                                    # よう乗算する薄汚れた鼠色の"空腹"カラー
HUNGRY_RAT_STEAL_CHANCE = 35  # Hungry Ratの攻撃が命中した際、食料を1つ
                                # かじり取る確率(%)
HUNGRY_RAT_BONUS_FOOD = 2  # Hungry Rat討伐時にお返しとして得られる食料の数

# typ36「Cinder Ward」。typ27-35はいずれも「反射」「生命吸収」「コンボ破壊」
# 「時間経過で強化」「緊急回復」「防御無視」「集中泥棒」「食料かじり取り」という、
# 通常攻撃(Attack)・反撃(Counter)を軸にした駆け引きばかりで、消費アイテムである
# 爆炎石(Blaze Gem、固定1000ダメージのため強敵への切り札になりがち)そのものを
# 弱める敵がまだ居なかった。フロア70以降(Voidforged Golem以降と同じ深層専用帯)に
# 混ざる新しい深層モンスターとして、爆炎石で受けるダメージがCINDER_WARD_BLAZE_RESIST_MULT
# 倍(60%軽減)になる「業火の加護」を持たせた。爆炎石だけに頼り切る一発逆転の
# 立ち回りが通用しない初めての敵として、通常攻撃・反撃・集中を織り交ぜた戦い方を
# 選ばせる駆け引きを狙った。新規スプライトはこれまでの深層モンスターと同じく
# Hugging Face MCP経由の生成を試みたが、生成画像のホスト(hf.space)への接続が
# この実行環境のネットワーク制限でブロックされ、手元に保存できなかったため、
# 既存のWar Mech(enemy20.png)をCINDER_WARD_TINTで灼けたような橙色に染め直した
# 色違いとして使い回した。
CINDER_WARD_TINT = (255, 130, 40)  # War Mechと見分けられる、灼熱の"業火"カラー
CINDER_WARD_BLAZE_RESIST_MULT = 0.4  # 爆炎石ダメージ倍率(60%軽減)

# typ37「Numbing Hornet」(rev191で追加)。typ27-36はいずれも「一撃が命中した
# 瞬間」だけに効く駆け引き(反射・生命吸収・コンボ破壊・食料略奪・防御無視
# など)で、戦闘が続いている間ずっと効き続ける"場に居るだけの妨害"を持つ敵が
# まだ居なかった。フロア6以降・フロア30未満(Gloom Spriteと同じ序盤〜中盤の
# 帯)に混ざる新モンスターとして、この敵と戦闘中は羽音が集中を乱し、
# NUMBING_HORNET_CRIT_MULT倍(50%減)まで会心率が下がる「痺れの霧」を持たせた。
# コンボ・Focus・秘宝/護符など既存の会心率上昇手段をどれだけ積んでいても、
# この敵が生きている間は帳消しにされてしまうため、会心頼みの立ち回りから
# 一時的に切り替えさせる駆け引きを狙った。新規スプライトはHugging Face MCP
# 経由の生成自体には成功した(gr1_z_image_turbo_generate)が、生成画像の
# ホスト(hf.space)への接続がこの実行環境のネットワーク制限で403拒否され、
# これまでの深層モンスターと同じく手元に保存できなかったため、既存の
# Death hornet(enemy5.png)をNUMBING_HORNET_TINTで薄紫の"痺れ"カラーに
# 染め直した色違いとして使い回した。
NUMBING_HORNET_TINT = (150, 130, 220)  # Death hornetと見分けられる、痺れるような薄紫カラー
NUMBING_HORNET_CRIT_MULT = 0.5  # 戦闘中の会心率倍率(50%減)

# typ38「Ashbound Titan」(今回追加分)。typ27-37はいずれも「反射」「生命吸収」
# 「コンボ破壊」「会心率半減」など、通常攻撃の当たり方や確率に関わる駆け引き
# ばかりで、通常攻撃(Attack)そのものの威力を直接鈍らせてくる敵がまだ居なかった。
# フロア30以降(Chain Warden/Frenzied Revenant/Warbreaker Wightと同じ中盤〜深層の
# 帯)に混ざる新モンスターとして、この敵と戦っている間はのしかかる灰の重みで
# 通常攻撃のダメージがASHBOUND_TITAN_ATK_MULT倍(20%減)になる「灰塵の重圧」を
# 持たせた(Focus攻撃はAttackコマンドの延長として同じ倍率がかかるが、爆炎石・
# 必殺技・反撃には影響しない)。コンボや会心率をどれだけ積んでいても通常攻撃の
# 地力そのものが削がれるため、爆炎石や必殺技など別の攻め手を混ぜる理由になる。
# 新規スプライトはHugging Face MCP経由の生成を検討したが、このセッションの
# プロキシポリシーがhuggingface.co/hf.spaceへの接続を403で拒否することを
# __agentproxy/status で事前に確認できたため、これまでの深層モンスターと同じく
# 既存のFrost Colossus(enemy21.png、typ18)をASHBOUND_TITAN_TINTで灰色に
# 染め直した色違いとして使い回した。
ASHBOUND_TITAN_TINT = (150, 140, 130)  # Frost Colossusと見分けられる、灰塵の"灰色"カラー
ASHBOUND_TITAN_ATK_MULT = 0.8  # 通常攻撃(Attack)ダメージ倍率(20%減)

# typ39「Silence Wisp」(今回追加分)。typ27-38はいずれも「一撃ごとの駆け引き」
# または「戦闘中ずっと効き続ける確率・威力の妨害」(Numbing Hornetの会心率
# 半減、Ashbound Titanの通常攻撃威力ダウンなど)だったが、プレイヤーが積み
# 上げる「コンボ」というリソースそのものを封じてくる敵がまだ居なかった。
# フロア30以降(Chain Warden/Frenzied Revenant/Warbreaker Wight/Ashbound
# Titanと同じ中盤〜深層の帯)に混ざる新モンスターとして、この敵と戦闘中は
# 静寂の霧が集中を乱し、通常攻撃(Focus攻撃を含む)を当ててもコンボが
# 一切たまらない「静寂の霧」を持たせた。Numbing Hornet/Ashbound Titanと
# 同じ「戦闘中ずっと効き続ける、居るだけの妨害」パターンを踏襲しつつ、
# 対象を会心率・威力ではなく初めてコンボの蓄積そのものに広げた。コンボが
# ULTIMATE_COMBO_REQUIREMENT分たまらないと使えない必殺技(Ultimate)も
# 同時に封じられるため、この敵に対しては爆炎石・防御・反撃・集中など
# コンボに頼らない他のコマンドを織り交ぜる立ち回りが必須になる(戦闘が
# 終わればコンボはまた通常通り積み上げられるようになる、あくまでこの敵と
# 戦っている間だけの一時的な妨害)。新規スプライトはプロキシの接続状態
# (`__agentproxy/status`)でhuggingface.co/hf.spaceへの接続がこの実行環境の
# ポリシーで403拒否されることを今回も確認できたため、これまでの深層
# モンスターと同じく既存のVoid Fiend(enemy24.png、typ21)をSILENCE_WISP_TINTで
# 静寂を思わせる薄い青灰色に染め直した色違いとして使い回した。
SILENCE_WISP_TINT = (90, 150, 175)  # Void Fiendと見分けられる、静寂の薄い青灰色カラー

# typ40「Vengeful Wraith」(rev199で追加)。typ27-39はいずれも「一撃ごとの
# 駆け引き」(反射・生命吸収・コンボ破壊・食料略奪など)か「戦闘中ずっと
# 効き続ける確率・威力の妨害」(会心率半減・通常攻撃威力ダウン・コンボ封じ)
# だったが、プレイヤーが会心(クリティカル)を「出したこと」自体を咎めて
# くる敵がまだ居なかった。フロア70以降(Voidforged Golem/Mirror Wraith/
# Hollow Widow/Cinder Wardと同じ深層専用帯)に混ざる新モンスターとして、
# 通常攻撃(Focus攻撃を含む)でクリティカルヒットを与えると、直後に
# VENGEFUL_WRAITH_RETALIATE_MULT分のダメージで報復してくる「血讐の加護」を
# 持たせた。Mirror Wraith(typ28)の反射は命中したすべての攻撃が対象なのに
# 対し、これは会心時だけに絞った初めての駆け引きで、会心率を積みすぎる
# ほど分の悪い相手になる(反撃(Counter)は現状クリティカルが発生しない
# コマンドのため、この敵に対してはCounterで安全に立ち回るという新しい
# 選択肢も生まれる)。新規スプライトはHugging Face MCP経由の生成自体には
# 成功したが、生成画像のホスト(hf.space)への接続がこれまでの深層モンスター
# と同じくこの実行環境のプロキシポリシーで403拒否されローカルに保存できな
# かったため、既存のVanguard Trooper(enemy26.png)を復讐を思わせる深紅色に
# 染め直した色違いとして使い回した。
VENGEFUL_WRAITH_TINT = (170, 15, 30)  # Vanguard Trooperと見分けられる、復讐の深紅色カラー
VENGEFUL_WRAITH_RETALIATE_MULT = 0.35  # 会心ダメージのうち何割をそのまま報復として受けるか

# typ41「Bloodthorn Revenant」(今回追加分)。typ27-40はいずれも状態異常だと
# しても毒(emy_poison)/気絶(emy_stun)のようにスキル(Antidote Body)や
# フロア特性(Festering/Cleansing/Serene)で軽減・無効化できる「対策のある」
# 駆け引きだったが、どんな対策を積んでも一切軽減できない持続ダメージを
# 与えてくる敵がまだ居なかった。フロア30以降(Chain Warden/Frenzied Revenant/
# Warbreaker Wightと同じ中盤〜深層の帯)に混ざる新モンスターとして、通常攻撃が
# 命中すると新しい状態異常「出血(pl_bleed)」を与える。出血はpl_poisonと違い
# 歩数・戦闘ターンで一定回数(BLOODTHORN_BLEED_TICKS)だけ必ず一定ダメージ
# (最大HPのBLOODTHORN_BLEED_DIVISOR分の1)を与え続け、Apothecary/Antidote Body
# スキルやFestering/Cleansing/Serene Floorの影響を一切受けない(唯一の対策は
# ポーションによる直接回復、または出血が自然に切れるまで耐えること)。新規
# スプライトはVengeful Wraith以降と同じくHugging Face MCP経由の生成を試みたが、
# 生成画像のホスト(hf.space)への接続がこの実行環境のプロキシポリシーで403
# 拒否されローカルに保存できないことを`__agentproxy/status`で再確認したため、
# 既存のBone Reaper(enemy_bone_reaper.png、typ15)の画像を使い回し、
# init_battle()側でBLOODTHORN_REVENANT_TINTを乗算して見た目を血を思わせる
# 深い紅黒色に変える。
BLOODTHORN_REVENANT_TINT = (150, 10, 15)  # Bone Reaperと見分けられる、出血を思わせる深紅黒色カラー
BLOODTHORN_BLEED_CHANCE = 35     # 通常攻撃(反撃を含む)命中時に出血を付与する確率(%pt)
BLOODTHORN_BLEED_TICKS = 3       # 出血が持続する回数(歩数/戦闘ターンごとに1回消費)
BLOODTHORN_BLEED_DIVISOR = 15    # 1回のダメージ = 最大HP // この値(poisonの20よりダメージ密度が高い)

# typ42「Permafrost Wyrm」(今回追加分)。typ27-41はいずれも状態異常だとしても
# ダメージを伴うもの(毒/出血)か、敵の手番を封じるもの(気絶、ただしプレイヤー
# →敵の一方通行)ばかりで、「プレイヤー自身の手番を1回丸ごと封じる」という
# 敵側から仕掛けてくる行動封じがまだ無かった。フロア30以降(Bloodthorn
# Revenantと同じ中盤〜深層の帯)に混ざる新モンスターとして、通常攻撃
# (反撃を含む)が命中すると新しい状態異常「凍結(pl_frozen)」を与える。
# 凍結はダメージを一切与えない代わりに、次のプレイヤーの手番をまるごと
# 1回スキップさせる(コマンド入力自体を受け付けない)。出血と同じく
# どんなスキル・フロア特性でも無効化はできない「対策の無い」駆け引きだが、
# Bloodslick FloorがBloodthorn Revenantに対して行ったのと同じ「専用の
# フロア特性で確率を上乗せする/護符で軽減する」という両サイドの拡張余地を
# 今回のrevで併せて埋めた(modifier_freeze_chance_bonus()/
# charm_freeze_resist_bonus()を参照)。新規スプライトはこれまでの深層
# モンスターと同じくHugging Face MCP経由の生成を試みたが、`__agentproxy/status`
# で生成画像のホスト(hf.space)への接続がこの実行環境のプロキシポリシーで
# 403拒否されることを再確認したため、まだ色違いとして使い回されていなかった
# Plague Reaper(enemy25.png、typ22の元画像)を氷のような水色に染め直した
# 色違いとして使い回す。
PERMAFROST_WYRM_TINT = (150, 220, 255)  # Plague Reaperと見分けられる、氷を思わせる淡い水色カラー
PERMAFROST_FREEZE_CHANCE = 30    # 通常攻撃(反撃を含む)命中時に凍結を付与する確率(%pt)

ELITE_LIFE_MULT = 1.6
ELITE_STR_MULT = 1.3
ELITE_EXP_MULT = 1.5

def tint_surface(img, color):
    """imgのRGBをcolorで乗算した色調違いのコピーを返す(アルファ/形状はそのまま)。"""
    tinted = img.convert_alpha()
    tinted.fill(color, special_flags=pygame.BLEND_MULT)
    return tinted

# --- ヒーロー別の色分けスプライト(Rogue/Berserker/Prospector/Trader/Monk) ---
# rev171(Prospector)以降、Guardian/Scholar/Scoutのような専用スプライト
# (mychr_*.png/hero_*.png)が用意されないまま、Rogue以降4人+今回のMonkの
# 計5人はキャラクター選択画面で肖像画が表示されず、ダンジョン内の見た目も
# Warriorの使い回しのままになっていた(README「主人公をどんどんかっこよく」
# の方針にも反する)。深層モンスター(Voidforged Golemなど)がこの実行環境の
# ネットワーク制限でスプライト生成できない時に使っているtint_surface()の
# 色調変更パターンを、新規画像を用意できないヒーロー側にもそのまま流用する。
_HERO_TINT_COLORS = {
    "rogue":      (110, 90, 170),   # 闇に紛れる紫(ステルス)
    "berserker":  (220, 60, 40),    # 血のような赤(激昂)
    "prospector": (210, 175, 60),   # 金銀財宝の黄土色(幸運)
    "trader":     (60, 170, 130),   # 商いの緑がかった青緑(堅実)
    "monk":       (90, 190, 210),   # 静謐な空色(修行僧)
    "cleric":     (190, 215, 255),  # 癒やしの光を思わせる淡い水色がかった白(聖職者)
    "pyromancer": (255, 120, 40),   # 爆炎石を思わせる燃え盛る橙色(爆撃役)
    "duelist":    (215, 60, 110),   # 舞台衣装のような華やかな紅色(決闘者)
    "reaver":     (140, 15, 45),    # 吸った血を思わせる深い葡萄色(吸血鬼)
    "vagabond":   (150, 130, 90),   # 旅埃を思わせる土色がかったベージュ(渡り者)
    "apothecary": (170, 70, 190),   # 怪しい毒薬を思わせる紫がかったマゼンタ(毒使い)
    "marshal":    (80, 120, 150),   # 治安を思わせる鈍い鋼色がかった青(治安官)
    "ranger":     (90, 170, 70),    # 森に紛れる狩人らしい深緑(一撃必殺)
    "vanguard":   (170, 70, 60),    # 先陣を切る戦士の甲冑を思わせる鈍い赤茶色(対ボス特化)
}

def _build_recolored_hero_assets():
    """imgPlayerSets/imgParaSets/imgHeroに、専用画像を持たないヒーローの
    tint_surface版を追加登録する。tint_surface()はconvert_alpha()を
    使うためpygame.display.set_mode()より前には呼べず、
    _convert_loaded_images()の直後(main()内)から呼ぶ。既にキーがある
    ヒーロー(将来専用画像が追加された場合)は上書きしない。"""
    for hid, tint in _HERO_TINT_COLORS.items():
        if hid not in imgPlayerSets:
            imgPlayerSets[hid] = [tint_surface(img, tint) for img in imgPlayer]
        if hid not in imgParaSets:
            imgParaSets[hid] = tint_surface(imgPara, tint)
        if hid not in imgHero:
            imgHero[hid] = tint_surface(imgHero["warrior"], tint)

# --- 仲間(Pet)の色分けスプライト(Owl) ---
# rev186で追加したOwl(Wise Owl)には専用画像が無く、ヒーロー側と同じく
# この実行環境のネットワーク制限でHugging Face MCP経由のスプライト生成
# アセットを手元に保存できない前提のため、_build_recolored_hero_assets()と
# 同じtint_surface()の色調変更パターンを仲間画像にもそのまま流用する。
_PET_TINT_COLORS = {
    "owl": (215, 180, 120),  # 知恵の象徴であるフクロウらしい茶褐色の羽色
    "beetle": (140, 150, 165),  # 鋼の甲殻を思わせる鈍い鉄灰色(盾役)
    "fox": (230, 130, 50),  # 幸運を運ぶキツネらしい鮮やかな橙色
}

imgBranchRoute = None  # 近道(分岐ルート)入り口の見た目。tint_surface()はpygame.display.set_mode()より前には呼べないため、main()内で_build_branch_route_assets()により生成する

def _build_branch_route_assets():
    """近道(分岐ルート)入り口の見た目を、既存のワープ床画像(氷結晶)を琥珀色に
    染め直して用意する。新規スプライトはこの実行環境のネットワーク制限で
    Hugging Face MCP経由の生成画像を保存できないため、ヒーロー/仲間と同じ
    tint_surface()の色調変更パターンをそのまま流用する。"""
    global imgBranchRoute
    imgBranchRoute = tint_surface(imgWarpCrystal, (230, 175, 60))

def _build_recolored_pet_assets():
    """imgPet/imgPetRevに、専用画像を持たない仲間のtint_surface版を追加登録する。
    _build_recolored_hero_assets()と同じく、pygame.display.set_mode()より
    後(main()内)から呼ぶ必要がある。"""
    for pid, tint in _PET_TINT_COLORS.items():
        if pid not in imgPet:
            imgPet[pid] = tint_surface(imgPet["sprite"], tint)
        if pid not in imgPetRev:
            imgPetRev[pid] = tint_surface(imgPetRev["sprite"], tint)

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
        if load_stats().get("golden_sprites_caught", 0) >= 10:
            unlock_achievement("golden_hunter")
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
        if load_stats().get("vaults_escaped", 0) >= 10:
            unlock_achievement("vault_survivor")
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
    global in_trial_post_battle
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
        if load_stats().get("chimeras_defeated", 0) >= 10:
            unlock_achievement("chimera_bane")
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
        if load_stats().get("doppelgangers_defeated", 0) >= 10:
            unlock_achievement("shadow_reaper")
        info_message = f"You overcame your reflection! +{bonus_exp} EXP, +1 Potion, +50 Food"
        info_timer = 60
    if mimic_battle_active:
        mimic_battle_active = False
        potion += 1
        blazegem += 2
        food += 60
        record_stat("mimics_defeated")
        unlock_achievement("mimic_defeated")
        if load_stats().get("mimics_defeated", 0) >= 15:
            unlock_achievement("mimic_hunter")
        info_message = "It was a Mimic! +1 Potion, +2 Blaze gem, +60 Food"
        info_timer = 60
    if in_rift_battle:
        in_rift_battle = False
        potion += 2
        blazegem += 3
        food += 100
        record_stat("rifts_cleared")
        unlock_achievement("rift_survivor")
        if load_stats().get("rifts_cleared", 0) >= 10:
            unlock_achievement("rift_master")
        info_message = "Rift closed! +2 Potion, +3 Blaze gem, +100 Food"
        info_timer = 60
    if in_trial_post_battle:
        in_trial_post_battle = False
        relic_pool = [r for r in RELIC_DEFS if not load_relics().get(r["key"], False)]
        new_relic = random.choice(relic_pool) if relic_pool else None
        if new_relic and unlock_relic(new_relic["key"]):
            unlock_achievement("relic_finder")
            if all(load_relics().get(r["key"], False) for r in RELIC_DEFS):
                unlock_achievement("relic_collector")
            info_message = f"Trial cleared! Relic acquired: {new_relic['name']}"
        else:
            potion += 3
            blazegem += 5
            food += 150
            info_message = "Trial cleared! +3 Potion, +5 Blaze gem, +150 Food"
        info_timer = 70
        record_stat("trial_posts_cleared")
        unlock_achievement("trial_survivor")
        if load_stats().get("trial_posts_cleared", 0) >= 10:
            unlock_achievement("trial_master")
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
        if load_stats().get("dens_cleared", 0) >= 15:
            unlock_achievement("dungeon_warden")
        info_message = "Monster den cleared! +2 Potion, +2 Blaze gem, +150 Food"
        info_timer = 70
    if in_boss_rush_mode:
        # ボスラッシュは通常勝利(idx==22)・ボス勝利(idx==26)・エコー勝利(idx==60)・
        # 闘技場勝利(idx==73)のどれとも異なる専用の「ボス撃破」演出(idx==77)を挟み、
        # 回復してから次のボスへ進める。
        idx = 77
        tmr = 0
        return
    if in_arena_mode:
        # 闘技場は通常勝利(idx==22)・ボス勝利(idx==26)・エコー勝利(idx==60)の
        # どれとも異なる専用の「ラウンドクリア」演出(idx==73)を挟み、
        # 次のラウンドに挑むか退くかをプレイヤーに選ばせる。
        idx = 73
        tmr = 0
        return
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
        if load_stats().get("boulders_dodged", 0) >= 15:
            unlock_achievement("boulder_master")
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

# --- 試練の石碑(Trial Post): 確実に未所持の秘宝が手に入るエリート戦 ---
# 不安定な裂け目(Rift)と同じ「踏むと必ずエリート戦になる」ハイリスクな
# 特殊床だが、裂け目の報酬がポーション/爆炎石/食料という消費アイテムに
# 留まるのに対し、こちらは勝利すると持っていない秘宝(Relic)を1つ確実に
# 入手できる(通常のボス撃破時の秘宝ドロップは確率任せなのに対し、この
# 石碑は挑む代わりに結果を確定させる、新しい「腕試し」の仕掛け)。
# 全17種の秘宝をすでに集め切っている場合は、代わりにまとまった消費
# アイテムを渡す(resolve_post_battle_transition参照)。
TRIAL_POST_CHANCE = 10       # フロアに出現する確率(%)。floor>=6から
TRIAL_POST_LIFE_MULT = 1.3
TRIAL_POST_STR_MULT = 1.2
in_trial_post_battle = False

_trial_post_img_cache = None

def get_trial_post_image():
    """試練の石碑用に、守護者の像の画像を紅蓮色にティントした画像を初回だけ
    作ってキャッシュする(get_bard_image/get_monster_den_imageと同じ、
    新規スプライトをこの実行環境のネットワーク制限で用意できないため、
    既存素材をtint_surfaceで色調違いにするパターンを踏襲)。"""
    global _trial_post_img_cache
    if _trial_post_img_cache is None:
        _trial_post_img_cache = tint_surface(imgStatue, (225, 60, 40))
    return _trial_post_img_cache

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
    if load_stats().get("shrines_used", 0) >= 10:
        unlock_achievement("shrine_regular")

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
        if load_stats().get("bounties_completed", 0) >= 10:
            unlock_achievement("bounty_master")
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
    if load_stats().get("vaults_opened", 0) >= 10:
        unlock_achievement("treasure_keykeeper")
    info_message = "The vault opens! +2 Potion, +6 Blaze gem, +120 Food"
    info_timer = 70

# --- 守護者の像の試練(運やRNGではなく純粋なSTR判定) ---
# 触れた瞬間のSTRがフロアに応じたしきい値以上なら永続的な力を授かり、
# 届かなければ何も持ち去られることなく、ただ力不足を思い知らされるだけ。
STATUE_CHANCE = 12   # フロアに出現する確率(%)。floor>=5から

def statue_str_threshold(fl):
    """フロアに応じて要求STRを決める(深いフロアほど厳しくなる)。
    Hallowed Floorでは modifier_statue_threshold_bonus() 分だけ必要STRが下がる
    (下限を1でクランプし、極端に浅いフロアでも0以下にならないようにする)。"""
    return max(1, int(110 + fl * 7) + modifier_statue_threshold_bonus())

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
        if load_stats().get("statue_trials_passed", 0) >= 10:
            unlock_achievement("statue_champion")
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
        if load_stats().get("gambles_won", 0) >= 20:
            unlock_achievement("card_shark")
        if tier_index == len(GAMBLE_TIERS) - 1:
            unlock_achievement("high_roller")
            record_stat("high_roller_wins")
            if load_stats().get("high_roller_wins", 0) >= 10:
                unlock_achievement("high_roller_veteran")
    else:
        gamble_result_name = "YOU LOSE..."
        gamble_result_desc = f"-{tier['cost']} Blaze gem lost."

# --- キメラの巣(まれに出現する規格外の超強敵) ---
# ライオン・山羊・竜が混ざり合った伝説の魔獣。エリートよりもさらに遥かに格上で、
# フロアボスに匹敵するほどの強さを持つ。出現率は非常に低く、遭遇そのものが
# 稀少な体験になるよう作られている。倒せば破格の報酬が手に入る。
CHIMERA_CHANCE = 6    # フロアに出現する確率(%)。floor>=8から
chimera_battle_active = False

# --- 灯火の鍛冶場(Ember Forge。ブレイズジェムを永続強化に変える鍛冶台) ---
# 従来の消費アイテム系の床仕掛け(精霊の祭具=一時強化、犠牲の祭壇=HPを賭けた
# ランダムな恩恵)はいずれも「その場で何が起きるか運任せ」だったが、この床は
# 完全に確定した効果で、かつプレイヤー自身の所持品(ブレイズジェム)を
# 燃料として使う経済的な選択を迫る新しい方向性の仕掛け。踏んだ時点で
# ブレイズジェムを1個も持っていなければ何も起きず(床はそのまま残る)、
# 1個以上持っていれば全て消費してSTRを永続的に押し上げる。「一撃必殺の
# ブレイズジェムを温存するか、ここで攻撃力そのものに変えてしまうか」という
# 駆け引きが生まれる。
EMBER_FORGE_CHANCE = 12     # フロアに出現する確率(%)。floor>=6から
EMBER_FORGE_STR_PER_GEM = 3 # 消費したブレイズジェム1個につき得られる永続STR

_ember_forge_img_cache = {}

def get_ember_forge_image(floor_variant):
    """既存の祭壇(Altar)画像を炎のような暖色にティントした画像を、
    ステージテーマ(floor_variant)ごとに初回だけ作ってキャッシュする
    (get_monster_den_imageと同じ、新規画像を用意せず既存素材を
    tint_surfaceで色調違いにするパターン)。"""
    global _ember_forge_img_cache
    img = _ember_forge_img_cache.get(floor_variant)
    if img is None:
        base = {1: imgAltarCrystal, 2: imgAltarFlame}.get(floor_variant, imgAltar)
        img = base.convert_alpha()
        img.fill((255, 150, 60), special_flags=pygame.BLEND_MULT)
        img.fill((90, 30, 0), special_flags=pygame.BLEND_ADD)
        _ember_forge_img_cache[floor_variant] = img
    return img

# --- 護符の祠(Charm Shrine。護符(Charm)を1つ授けてくれる祠) ---
# 灯火の鍛冶場(所持品を消費して確定の強化に変える)とは逆に、こちらは
# プレイヤーの所持品を何も要求しない代わりに、まだ持っていない護符を
# ランダムに1つ授けてくれる。全種類集めた後に踏んでも祠は静かに消えるだけ
# (何も起きない)。
CHARM_SHRINE_CHANCE = 10   # フロアに出現する確率(%)。floor>=6から

_charm_shrine_img_cache = {}

def get_charm_shrine_image(floor_variant):
    """既存の祭壇(Altar)画像を神秘的な紫がかった色にティントした画像を、
    ステージテーマ(floor_variant)ごとに初回だけ作ってキャッシュする
    (get_ember_forge_imageと同じ、既存素材をtint済みにして見分けるパターン)。"""
    global _charm_shrine_img_cache
    img = _charm_shrine_img_cache.get(floor_variant)
    if img is None:
        base = {1: imgAltarCrystal, 2: imgAltarFlame}.get(floor_variant, imgAltar)
        img = base.convert_alpha()
        img.fill((180, 140, 255), special_flags=pygame.BLEND_MULT)
        img.fill((40, 0, 70), special_flags=pygame.BLEND_ADD)
        _charm_shrine_img_cache[floor_variant] = img
    return img

# --- 旅の吟遊詩人(Traveling Bard。仲間の生まれ変わりを持ちかけてくる) ---
# ペット(仲間)は孵化以降ずっとpet_type固定で、一度気に入らない仲間が
# 孵ってしまうとその周回中ずっと付き合うしかなかった。今回追加した
# 「仲間の絆」(同じ仲間と長く潜るほど効果が強まる)によって、この
# 「固定である」という性質がより重要になった(絆を積む前提でどの仲間と
# 長く付き合うか選び直したい場面が増える)ため、旅の商人とは別に、
# ダンジョンで稀に出会う吟遊詩人が「今の仲間を新しい仲間と交換する」
# 一度きりの機会を提供するようにした。仲間がいない場合は何も起こらない。
BARD_CHANCE = 10   # フロアに出現する確率(%)。floor>=6から

_bard_img_cache = None

def get_bard_image():
    """旅の商人画像(imgFloor[9])を紫がかった色にティントした画像を、
    初回だけ作ってキャッシュする(get_monster_den_imageと同じ、既存素材を
    tint_surfaceで色調違いにして新規画像なしで見分けをつけるパターン)。"""
    global _bard_img_cache
    if _bard_img_cache is None:
        _bard_img_cache = tint_surface(imgFloor[9], (190, 150, 255))
    return _bard_img_cache

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
        if load_stats().get("altar_boons", 0) >= 10:
            unlock_achievement("altar_devotee")
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
    # 生贄の祭壇での献上(altar_sacrifice)は初回実績はあるのに、結果が
    # Boon/Silence/Backlashのいずれであっても献上した回数そのものを評価する
    # 累積実績が無く、Golden Hunter/Rift Master/Bounty Masterなどと同じ
    # 「初回はあるが繰り返し系が無かった」穴が残っていたため、既存の記録
    # (altars_used)をそのまま活かして通算10回の累積実績を新設した。
    if load_stats().get("altars_used", 0) >= 10:
        unlock_achievement("altar_regular")

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

# --- アイテム入手時の光の粒(sparkle)演出 ---
# rev172でアイテム入手時の画面フラッシュ/ジングルを廃止したが、その代わりの
# 演出が一切無いままだったため、画面全体を光らせず足元だけで完結する控えめな
# 演出を新設する(希少アイテム、および隠し部屋・秘密の宝物庫の宝箱で発動)。
ITEM_SPARKLE_FRAMES = 26
item_sparkle_timer = 0
ITEM_SPARKLE_OFFSETS = [(-24, -50), (24, -50), (-30, -20), (30, -20), (-14, -74), (14, -74)]

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
achievement_toast_queue = []  # 表示中に別の実績が解除された場合、後から順番に表示するための待ち行列
# 【バグ修正】READMEの「サウンド・アセット」節には「実績解除トーストが表示される
# 瞬間、レベルアップジングルを再生して音でも達成に気づけるように」という記述が
# あったが、実際にはunlock_achievement()はトースト表示の状態(グローバル変数)を
# 更新するだけで、どこからもse[]を再生していなかった(記載と実装が食い違って
# いた)。rare_treasure_sound_pendingと同じ「main()の外でフラグを立て、main()側で
# 消費して再生する」パターンで、実績を新規解除した瞬間だけレベルアップジングル
# (se[4])を1回鳴らすようにし、記載通りの挙動にする。
achievement_sound_pending = False  # 実績を新規解除した瞬間のジングル再生待ちフラグ(se[4]を流用)
rare_treasure_sound_pending = False  # 希少な宝箱アイテムを引いた時に鳴らすジングルの再生待ちフラグ
# 隠し壁の発見・宝箱を開けた瞬間は、これまで見た目の変化だけで効果音が
# 何も鳴らなかった(視覚障害者には気づきにくい上、健常者にも「今何か
# 起きた」という手応えが薄かった)。rare_treasure_sound_pendingと同じ、
# 「main()の外(移動処理・隠し壁判定)でフラグを立て、main()側で消費して
# 再生する」パターンで、既存のse[]をそのまま流用する(新規音源ファイルは
# 追加せず、既存の短い効果音を別の発見演出にも使い回す)。
hidden_wall_sound_pending = False  # 隠し壁を見つけた瞬間の再生待ちフラグ(se[0]を流用)
# 低HP警告(画面端の脈打つ赤い縁取り)は、これまで見た目だけの演出で音が無く、
# 画面外に目をやっていたり画面に集中していないと気づきにくかった。同じ
# 「main()の外でフラグを立て、main()側で消費して再生する」パターンで、
# HPが閾値を下回った瞬間(既に警告中の間は鳴らし続けない)だけse[0]を1回
# 再生して気づきやすくする。
low_hp_warning_sound_pending = False  # 低HP警告に入った瞬間の再生待ちフラグ(se[0]を流用)
low_hp_warning_active = False  # 現在低HP警告の表示中かどうか(閾値をまたいだ瞬間だけ音を鳴らすための状態管理)
branch_route_sound_pending = False  # 近道(分岐ルート)の入り口を見つけた瞬間の再生待ちフラグ(隠し壁と同じse[0]を流用)

# --- 秘宝発見トースト演出 ---
# 実績解除トースト(draw_achievement_toast)と同じゴールドバナー方式だが、
# 同じ場所に重ねて出すと文字が重なって読めなくなるため、実績トーストの
# 表示中はその真下に(表示していない時は詰めて画面上端に)ずらして表示する。
RELIC_TOAST_FRAMES = 150
RELIC_TOAST_SLIDE = 12
RELIC_TOAST_FADE = 25
RELIC_TOAST_GAP = 10  # 実績トーストが同時に出ている場合の隙間(px)
relic_toast_label = ""
relic_toast_timer = 0
relic_toast_queue = []
relic_sound_pending = False  # 秘宝を新規入手した瞬間のジングル再生待ちフラグ(se[4]を流用)

# --- 護符発見トースト演出 ---
# 秘宝発見トースト(draw_relic_toast)と同じ方式。実績・秘宝どちらのトーストとも
# 同じ場所に重ねると文字が重なって読めなくなるため、両方の表示中かどうかを
# 見て、その分だけさらに下にずらして表示する。
CHARM_TOAST_FRAMES = 150
CHARM_TOAST_SLIDE = 12
CHARM_TOAST_FADE = 25
CHARM_TOAST_GAP = 10
charm_toast_label = ""
charm_toast_timer = 0
charm_toast_queue = []
charm_sound_pending = False  # 護符を新規入手した瞬間のジングル再生待ちフラグ(se[4]を流用)

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

COMMAND = ["[A]ttack", "[P]otion","[B]laze gem","[R]un", "[D]efense", "[F]ocus", "[U]ltimate", "[C]ounter"]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food + 30", "Food + 60", "Sord", "Defense Pill",
            "Ring of Vitality", "Amulet of Wisdom", "Food + 45", "Pet Egg"]
EMY_NAME = ["Green slime", "Red slime", "Axe beast", "Ogre", "Sword man",
            "Death hornet", "Signal slime", "Devil plant", "Twin killer", "Hell",
            "Dragon gear", "Crystal slime", "Shadow wisp", "Iron golem",
            "Venom spider", "Bone reaper", "Molten drake",
            "War Mech", "Frost Colossus", "Inferno Warlord", "Glacier Knight",
            "Void Fiend", "Plague Reaper", "Vanguard Trooper", "Inferno Trooper",
            "Juggernaut Trooper", "Shadow Ranger",
            # typ 27(2026-07-25追加分)。フロア70以降にのみ出現する新しい深層専用の敵。
            # 新規スプライトはHugging Face MCP経由で生成を試みたが、生成画像の
            # ホスト(hf.space)がこのセッションのプロキシポリシーで403拒否され
            # ローカルに取得できなかったため、Elite/Doppelgangerと同じ既存の
            # tint_surface()による色調変更の使い回しパターン(enemy_iron_golem.png
            # を紫の"void"カラーで乗算)で新モンスターとして成立させた。
            "Voidforged Golem",
            # typ 28(今回追加分)。Voidforged Golemと同じくフロア70以降にのみ
            # 混ざる深層専用の敵だが、単なるステータス違いではなく「通常攻撃
            # (Attack)を当てるとダメージの一部を跳ね返してくる」という今までに
            # 無い戦術性を持つ。爆炎石(Blaze Gem)による一撃なら跳ね返しを受けずに
            # 突破できるため、消費アイテムの使いどころを考えさせる新しい駆け引き
            # を狙った。新規スプライトはHugging Face MCP経由の生成自体は成功した
            # (gr1_z_image_turbo_generate)が、Voidforged Golemの時と同じく生成
            # 画像のホスト(hf.space)がこのセッションのプロキシポリシーで403
            # 拒否されローカル保存できなかったため、既存のShadow Wisp
            # (enemy_shadow_wisp.png)をMIRROR_WRAITH_TINTで銀白色に染めて
            # 使い回した。
            "Mirror Wraith",
            # typ 29(今回追加分)。Voidforged Golem/Mirror Wraithと同じくフロア70以降にのみ
            # 混ざる深層専用の敵で、Mirror Wraithの「反射」とは違う新しい戦術性を持つ:
            # 通常攻撃・反撃どちらでプレイヤーを殴っても、与えたダメージの一部で自分のHPを
            # 回復する「生命吸収」を持つ。じわじわ削るだけでは回復に追いつかれてしまうため、
            # 一気に押し切るか、爆炎石で削り切るかの判断を迫られる。新規スプライトは
            # Hugging Face MCP経由の生成を試みたが、Voidforged Golem/Mirror Wraithの時と
            # 同じくこの実行環境のネットワーク制限で生成画像のホスト(hf.space)へ接続
            # できなかったため、既存のVenom Spider(enemy_venom_spider.png)を
            # 病的に白っぽい色に染め直した色違いとして使い回した。
            "Hollow Widow",
            # typ 30(今回追加分)。Voidforged Golem/Mirror Wraith/Hollow Widowは
            # いずれもフロア70以降専用だったため、フロア30〜69(ステージ2以降)
            # だけずっとtyp8-26の顔ぶれが使い回され続けていた中盤の遭遇マンネリを
            # 崩すための新モンスター。新しい戦術性は「束縛」:通常攻撃・反撃で
            # プレイヤーに命中すると、確率(CHAIN_WARDEN_BREAK_CHANCE)でコンボ
            # ストリークを0に断ち切ってくる。コンボを積む戦い方に対する初めての
            # 「敵側からの妨害」で、コンボに頼りきらない立ち回りも選択肢に
            # 入れさせる駆け引きを狙った。新規スプライトはHugging Face MCP経由の
            # 生成を試みたが、Voidforged Golem以降と同じくこの実行環境の
            # ネットワーク制限で生成画像のホスト(hf.space)へ接続できなかった
            # ため、既存のBone Reaper(enemy_bone_reaper.png)をCHAIN_WARDEN_TINT
            # で鈍い鎖色に染め直した色違いとして使い回した。
            "Chain Warden",
            # typ 31(今回追加分)。Voidforged Golem/Mirror Wraith/Hollow Widow/
            # Chain Wardenはいずれも「その場で」効く駆け引き(スタット違い・反射・
            # 生命吸収・コンボ破壊)だったが、「時間の経過で強くなる」という発動
            # タイミングの特性がまだ無かった。攻撃するたびにSTRが伸びていく
            # (FRENZIED_REVENANT_STR_GROWTH)ため、じわじわ削る長期戦を選ぶほど
            # 危険になり、爆炎石などで早期決着をつける動機になる。フロア30以降
            # (Chain Wardenと同じ帯)に混ざる。新規スプライトはHugging Face MCP
            # 経由の生成を試みたが、これまでの深層モンスターと同じくこの実行
            # 環境のネットワーク制限で生成画像のホスト(hf.space)へ接続できな
            # かったため、既存のCrystal Slime(enemy_crystal_slime.png)を
            # FRENZIED_REVENANT_TINTで血のような赤に染め直した色違いとして
            # 使い回した。
            "Frenzied Revenant",
            # typ 32(今回追加分)。既存の深層専用モンスター(typ27-31)は
            # すべてフロア70〜90の通常ダンジョンにも混ざる一方、新設した
            # 「エンドレス・ディープス」(91階以降)には専用の敵が1体もおらず、
            # 潜り続けても既存の顔ぶれの使い回しのままだった。フロア90超の
            # エンドレス・ディープス限定で混ざる新しい深層専用モンスターとして、
            # Second Wind Floor(プレイヤーがピンチで自動回復する特性)を
            # 敵側の視点に置き換えた「一度だけの緊急回復」を持たせた:HPが
            # ABYSSAL_WARDEN_HEAL_HP_PCT(30%)以下になった瞬間、1バトルにつき
            # 一度だけABYSSAL_WARDEN_HEAL_TARGET_PCT(60%)まで自己回復する。
            # じわじわ削るだけでは息を吹き返されるため、一気に押し切るか、
            # 爆炎石で一撃のうちに仕留めるかの判断を迫られる。新規スプライトは
            # これまでの深層モンスターと同じくこの実行環境のネットワーク制限で
            # 生成画像のホスト(hf.space)へ接続できなかったため、既存の
            # Molten Drake(enemy_molten_drake.png)をABYSSAL_WARDEN_TINTで
            # 深い紫黒の"深淵"カラーに染め直した色違いとして使い回した。
            "Abyssal Warden",
            # typ 33(今回追加分)。typ27-32はいずれも「反射」「生命吸収」
            # 「コンボ破壊」「時間経過で強化」「緊急回復」というプレイヤーへの
            # 妨害・自己強化系の駆け引きだったが、プレイヤー側の防御コマンド
            # (Defend)そのものを逆手に取る敵がまだいなかった。Defendは
            # これまでどの敵に対しても純粋な安全策だったが、この敵は攻撃時に
            # プレイヤーがDefend中(pl_def_buff>0)だと、その防御ボーナス分を
            # 無視して素通りさせる「ガードブレイク」を持つ。Defend連打が
            # 通用しない初めての敵として、Potion/Flee/Counter(反撃)など
            # 他の選択肢を選ばせる駆け引きを狙った。フロア30以降(Chain
            # Warden/Frenzied Revenantと同じ帯)に混ざる。新規スプライトは
            # これまでの深層モンスターと同じくこの実行環境のネットワーク制限で
            # 生成画像のホスト(hf.space)へ接続できなかったため、既存の
            # Glacier Knight(enemy23.png)をWARBREAKER_TINTで鈍い金属的な
            # 銅色に染め直した色違いとして使い回した。
            "Warbreaker Wight",
            # typ 34(今回追加分)。typ27-33はすべてフロア30以降専用の深層
            # モンスターで、フロア1-29(typ0-16の帯)は今まで一度も「駆け引き」
            # 持ちの敵が出現せず、ステータス違いのモンスターだけがずっと使い回されて
            # いた。序盤〜中盤にも初めて仕組み持ちの敵を混ぜるため、フロア6以降・
            # フロア30未満の帯限定で出現する「集中(Focus)泥棒」を追加した。
            # プレイヤーが集中(Focus)コマンドで次の一撃を強化した状態(pl_charge)の
            # ときにこの敵から攻撃を受けると、その強化状態を攻撃と同時に奪い取って
            # しまう。Warbreaker Wightの「Defendを咎める」と同じ発想を、序盤で
            # 覚える最初のバトルコマンドの1つであるFocusに対して適用した。新規
            # スプライトはこれまでの深層モンスターと同じくこの実行環境のネットワーク
            # 制限でHugging Face MCP経由の生成画像ホスト(hf.space)へ接続できな
            # かったため、既存のShadow Wisp(enemy_shadow_wisp.png)を
            # GLOOM_SPRITE_TINTで病的な緑がかった"幻惑"カラーに染め直した色違いとして
            # 使い回した。
            "Gloom Sprite",
            # typ 35(今回追加分)。typ27-34はいずれもフロア30以降・6以降専用の
            # 深層〜中盤モンスターで、フロア1-5には「仕組み持ち」の敵が一体も
            # 居らず、一番最初の出会いはステータス違いのモンスターだけだった。
            # フロア1-5限定で出現する、攻撃が命中するたびに食料(food)を1つ
            # かじり取ってくる「空腹」持ちの敵を追加した。新規スプライトは
            # これまでの深層モンスターと同じくこの実行環境のネットワーク制限で
            # Hugging Face MCP経由の生成画像ホスト(hf.space)へ接続できなかった
            # ため、既存のRed Slime(enemy1.png)をHUNGRY_RAT_TINTで薄汚れた
            # 鼠色に染め直した色違いとして使い回した。
            "Hungry Rat",
            # typ 36。フロア70以降の深層専用帯に混ざる、爆炎石の
            # ダメージを軽減する「業火の加護」持ち。詳細はCINDER_WARD_TINT定義の
            # コメントを参照。
            "Cinder Ward",
            # typ 37(rev191で追加)。typ27-36はいずれも「一撃ごとの駆け引き」
            # (反射・生命吸収・コンボ破壊・食料略奪など)で、戦闘中ずっと効き
            # 続ける"場に居るだけの妨害"を持つ敵がまだ居なかった。フロア6以降・
            # フロア30未満(Gloom Spriteと同じ序盤〜中盤の帯)に混ざる新モンス
            # ターとして、この敵と戦っている間は羽音が集中力を乱し、会心率が
            # ずっと半減する「痺れの霧」を持たせた。詳細はNUMBING_HORNET_TINT
            # 定義のコメントを参照。
            "Numbing Hornet",
            # typ 38(今回追加分)。typ27-37はいずれも「一撃が命中した瞬間」や
            # 「戦闘中ずっと効き続ける確率・会心率の妨害」で、通常攻撃(Attack)
            # そのものの威力を直接鈍らせてくる敵がまだ居なかった。フロア30以降
            # (Chain Warden/Frenzied Revenant/Warbreaker Wightと同じ中盤〜深層の
            # 帯)に混ざる新モンスターとして、この敵と戦っている間はのしかかる
            # 灰の重みで通常攻撃のダメージが20%下がる「灰塵の重圧」を持たせた。
            # 詳細はASHBOUND_TITAN_TINT定義のコメントを参照。
            "Ashbound Titan",
            # typ 39(今回追加分)。typ27-38はいずれも確率・威力に関わる駆け引きで、
            # プレイヤーの「コンボ」リソースそのものを封じる敵がまだ居なかった。
            # 詳細はSILENCE_WISP_TINT定義のコメントを参照。
            "Silence Wisp",
            # typ 40(rev199で追加)。typ27-39はいずれも「一撃ごとの駆け引き」か
            # 「戦闘中ずっと効き続ける確率・威力の妨害」で、プレイヤーが会心
            # (クリティカル)を出したこと自体を咎めてくる敵がまだ居なかった。
            # フロア70以降(Voidforged Golem以降と同じ深層専用帯)に混ざる新
            # モンスターとして、この敵に通常攻撃(Focus攻撃を含む)でクリティカル
            # ヒットを与えると、直後にVENGEFUL_WRAITH_RETALIATE_MULT分の
            # ダメージで報復してくる「血讐の加護」を持たせた。Mirror Wraith
            # (typ28)の反射は命中したすべての攻撃が対象なのに対し、これは
            # 会心時だけに絞った初めての駆け引きで、会心率を積む秘宝
            # (Ember Charm/Phantom Lens)やフロア特性(Radiant/Fortunate)を
            # 積みすぎると逆にこの敵との相性が悪くなる、という新しい判断材料に
            # なる。詳細はVENGEFUL_WRAITH_TINT定義のコメントを参照。
            "Vengeful Wraith",
            # typ 41(今回追加分)。詳細はBLOODTHORN_REVENANT_TINT定義の
            # コメントを参照。
            "Bloodthorn Revenant",
            # typ 42(今回追加分)。詳細はPERMAFROST_WYRM_TINT定義の
            # コメントを参照。
            "Permafrost Wyrm"]

# 【UI改善】特殊な戦闘ギミックを持つ深層モンスター(Mirror Wraith/Hollow Widow/
# Chain Warden)は、これまでバトル中の一度きりの注意書きでしか仕組みを確認できず、
# 図鑑(Bestiary)で見返しても「ただの敵の一覧」にしか見えなかった。図鑑の詳細画面にも
# 同じ説明を常設表示することで、再戦前に予習したり見た目で仕組みを思い出せるようにした。
BESTIARY_ABILITY_HINTS = {
    28: "Reflects damage from Attacks",
    29: "Drains life from its attacks",
    30: "Can shatter your combo streak",
    31: "Grows stronger the longer the fight lasts",
    32: "Heals itself once when critically wounded",
    33: "Ignores your Defend bonus when it strikes",
    34: "Steals your Focus charge when it attacks",
    35: "Nibbles away 1 food when it hits you",
    36: "Resists damage from Blaze gems",
    37: "Halves your critical hit chance while it's alive",
    38: "Weakens your Attack damage by 20% while it's alive",
    39: "Your attacks won't build Combo while it's alive",
    40: "Retaliates hard whenever you land a Critical Hit",
    41: "Its attacks cause Bleed, a damage-over-time no skill or floor trait can lessen",
}

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
    # typ 17以降(2026-07-25追加分)。enemy20.pngは隠しボス専用画像
    # (enemy_hidden_boss.png)に切り出したので、typ 17から改めて
    # enemy20.png〜enemy29.pngを使う。
    17: "enemy20.png",
    18: "enemy21.png",
    19: "enemy22.png",
    20: "enemy23.png",
    21: "enemy24.png",
    22: "enemy25.png",
    23: "enemy26.png",
    24: "enemy27.png",
    25: "enemy28.png",
    26: "enemy29.png",
    # typ 27「Voidforged Golem」は新規画像を用意せず、既存のIron Golem
    # (typ13)の画像を使い回し、init_battle()側でVOID_GOLEM_TINTを
    # 乗算して見た目を紫の"void"カラーに変える(Eliteの色替えと同じ手法)。
    27: "enemy_iron_golem.png",
    # typ 28「Mirror Wraith」も同じ理由で新規画像を用意せず、既存のShadow Wisp
    # (typ12)の画像を使い回し、init_battle()側でMIRROR_WRAITH_TINTを乗算して
    # 見た目を銀白色に変える。
    28: "enemy_shadow_wisp.png",
    # typ 29「Hollow Widow」も同じ理由で新規画像を用意せず、既存のVenom Spider
    # (typ14)の画像を使い回し、init_battle()側でHOLLOW_WIDOW_TINTを乗算して
    # 見た目を病的に白っぽい色に変える。
    29: "enemy_venom_spider.png",
    # typ 30「Chain Warden」も同じ理由で新規画像を用意せず、既存のBone Reaper
    # (typ15)の画像を使い回し、init_battle()側でCHAIN_WARDEN_TINTを乗算して
    # 見た目を鈍い鎖色に変える。
    30: "enemy_bone_reaper.png",
    # typ 31「Frenzied Revenant」も同じ理由で新規画像を用意せず、既存のCrystal
    # Slime(typ11)の画像を使い回し、init_battle()側でFRENZIED_REVENANT_TINTを
    # 乗算して見た目を血のような赤色に変える。
    31: "enemy_crystal_slime.png",
    # typ 32「Abyssal Warden」も同じ理由で新規画像を用意せず、既存のMolten
    # Drake(typ16)の画像を使い回し、init_battle()側でABYSSAL_WARDEN_TINTを
    # 乗算して見た目を深い紫黒色に変える。
    32: "enemy_molten_drake.png",
    # typ 33「Warbreaker Wight」も同じ理由で新規画像を用意せず、既存のGlacier
    # Knight(typ20)の画像を使い回し、init_battle()側でWARBREAKER_TINTを乗算して
    # 見た目を鈍い金属的な銅色に変える。
    33: "enemy23.png",
    # typ 34「Gloom Sprite」も同じ理由で新規画像を用意せず、既存のShadow Wisp
    # (typ12)の画像を使い回し、init_battle()側でGLOOM_SPRITE_TINTを乗算して
    # 見た目を病的な緑がかった色に変える。
    34: "enemy_shadow_wisp.png",
    # typ 35「Hungry Rat」も同じ理由で新規画像を用意せず、既存のRed Slime
    # (typ1)の画像を使い回し、init_battle()側でHUNGRY_RAT_TINTを乗算して
    # 見た目を薄汚れた鼠色に変える。
    35: "enemy1.png",
    # typ 36「Cinder Ward」も同じ理由で新規画像を用意せず、既存のWar Mech
    # (typ17)の画像を使い回し、init_battle()側でCINDER_WARD_TINTを乗算して
    # 見た目を灼熱の橙色に変える。
    36: "enemy20.png",
    # typ 37「Numbing Hornet」も同じ理由で新規画像を用意せず、既存のDeath
    # Hornet(typ5)の画像を使い回し、init_battle()側でNUMBING_HORNET_TINTを
    # 乗算して見た目を薄紫の"痺れ"カラーに変える。
    37: "enemy5.png",
    # typ 38「Ashbound Titan」も同じ理由で新規画像を用意せず、既存のFrost
    # Colossus(typ18)の画像を使い回し、init_battle()側でASHBOUND_TITAN_TINTを
    # 乗算して見た目を灰塵の灰色に変える。
    38: "enemy21.png",
    # typ 39「Silence Wisp」も同じ理由で新規画像を用意せず、既存のVoid Fiend
    # (typ21)の画像を使い回し、init_battle()側でSILENCE_WISP_TINTを乗算して
    # 見た目を静寂を思わせる薄い青灰色に変える。
    39: "enemy24.png",
    # typ 40「Vengeful Wraith」(rev199で追加)も同じ理由で新規画像を用意せず、
    # 既存のVanguard Trooper(enemy26.png、typ23)の画像を使い回し、
    # init_battle()側でVENGEFUL_WRAITH_TINTを乗算して見た目を復讐を思わせる
    # 深紅色に変える。新規スプライトはHugging Face MCP経由の生成自体には
    # 成功した(gr1_z_image_turbo_generate)が、生成画像のホスト(hf.space)への
    # 接続がこれまでの深層モンスターと同じくこの実行環境のプロキシポリシーで
    # 403拒否されローカルに保存できなかったことを`__agentproxy/status`と
    # 実際のcurlで再確認したため、既存画像の色替えを使い回した。
    40: "enemy26.png",
    # typ 41「Bloodthorn Revenant」(今回追加分)も同じ理由で新規画像を用意せず、
    # 既存のBone Reaper(enemy_bone_reaper.png、typ15)の画像を使い回し、
    # init_battle()側でBLOODTHORN_REVENANT_TINTを乗算して見た目を血を思わせる
    # 深紅黒色に変える。詳細はBLOODTHORN_REVENANT_TINT定義のコメントを参照。
    41: "enemy_bone_reaper.png",
    # typ 42「Permafrost Wyrm」(今回追加分)も同じ理由で新規画像を用意せず、
    # まだ色違いとして使い回されていなかったPlague Reaper(enemy25.png、typ22の
    # 元画像)を使い回し、init_battle()側でPERMAFROST_WYRM_TINTを乗算して
    # 見た目を氷を思わせる淡い水色に変える。詳細はPERMAFROST_WYRM_TINT定義の
    # コメントを参照。
    42: "enemy25.png",
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
    global MAZE_W, MAZE_H, DUNGEON_W, DUNGEON_H, maze, dungeon, explored, hidden_treasure_positions
    global hidden_chest_cells
    global floor_modifier, wall_tint, wall_variant, floor_variant
    global collapsing_vault_bounds, collapse_timer
    global ambush_battles_remaining
    global boulder_pos, boulder_timer
    global is_blood_moon
    global mimic_battle_active
    global in_rift_battle
    global in_trial_post_battle
    global bounty_active
    global doppelganger_battle_active
    global map_fragments_active, map_fragments_found
    global has_sacred_key
    global chimera_battle_active
    global second_wind_used_this_floor
    global floor_chest_guarantee_used
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    second_wind_used_this_floor = False
    floor_chest_guarantee_used = False
    floor_modifier = roll_floor_modifier(floor)
    register_floor_modifier_seen(floor_modifier)
    wall_tint = roll_wall_tint(previous=wall_tint)
    wall_variant = stage_theme_variant(floor)
    floor_variant = stage_theme_variant(floor)
    generate_color_patches()
    hidden_treasure_positions = []
    hidden_chest_cells = set()
    collapsing_vault_bounds = None
    collapse_timer = 0
    ambush_battles_remaining = 0
    mimic_battle_active = False
    in_rift_battle = False
    in_trial_post_battle = False
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
    if floor >= 5 and random.randint(0, 99) < 12:
        carve_branch_route()
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
    if floor >= 6 and random.randint(0, 99) < TRIAL_POST_CHANCE:
        place_trial_post()
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
    if floor >= 6 and (modifier_ember_forge_guaranteed() or random.randint(0, 99) < EMBER_FORGE_CHANCE):
        place_ember_forge()
    if floor >= 6 and random.randint(0, 99) < BARD_CHANCE:
        place_bard()
    if floor >= 6 and (modifier_charm_shrine_guaranteed() or random.randint(0, 99) < CHARM_SHRINE_CHANCE):
        place_charm_shrine()

    global _reveal_radius_last, _minimap_cache_surface
    _reveal_radius_last = None
    _minimap_cache_surface = None

# ワープ床・回復の泉・呪いの床・罠の床・氷の床・モンスターの巣・黄金の像・祠・
# 囚われの仲間・不安定な裂け目・犠牲の祭壇・圧力プレート・封印された扉・
# 試練の石碑は、同じ種類同士・異なる種類同士を問わず隣接マスに並ばないようにする
# (ギミックが密集して分かりにくくなるのを防ぐ)
SPECIAL_FLOOR_TYPES = (4, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 42)

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
    (reveal_hidden_adjacent参照)。
    フロア8以降は低確率(15%、Buried Floorでは30%)で、隠し壁の奥がさらに1マス
    深く続く『秘密の宝物庫(Secret Vault)』になり、宝箱が2つ連なって隠される
    ようになる(通常の隠し部屋よりも壁2マス分の奥行きが必要なので、見つからなければ
    普通の1マスの隠し部屋にフォールバックする)。"""
    global hidden_treasure_positions
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if floor >= 8 and random.randint(0, 99) < min(99, 15 + modifier_secret_vault_chance_bonus()):
        vault_candidates = []
        for y in range(2, DUNGEON_H-2):
            for x in range(2, DUNGEON_W-2):
                if dungeon[y][x] not in (9, 25):
                    continue
                for dxn, dyn in dirs:
                    fx, fy = x-dxn, y-dyn
                    bx, by = x+dxn, y+dyn
                    b2x, b2y = x+2*dxn, y+2*dyn
                    if not (0 <= b2x < DUNGEON_W and 0 <= b2y < DUNGEON_H):
                        continue
                    if dungeon[fy][fx] == 0 and dungeon[by][bx] == 9 and dungeon[b2y][b2x] == 9:
                        vault_candidates.append((x, y, bx, by, b2x, b2y))
        if vault_candidates:
            x, y, bx, by, b2x, b2y = random.choice(vault_candidates)
            dungeon[y][x] = 10
            dungeon[by][bx] = 9
            dungeon[b2y][b2x] = 9
            hidden_treasure_positions = [(bx, by), (b2x, b2y)]
            return
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
    hidden_treasure_positions = [(bx, by)]

def carve_branch_route():
    """既存の壁を1マスだけ『近道(分岐ルート)の入り口』(40)にする。
    carve_hidden_room()と同じ『隣接候補を探して壁を1マスだけ書き換える』
    方式だが、裏に隠すのは宝箱ではなく、細い一本道の小さな隠しエリア
    (generate_branch_route_area参照)。そのエリアの階段を使うと、次の
    フロアをまるごと1つ飛ばして深層へ進める『近道』になる(そのフロアの
    探索・経験値・宝箱を犠牲にする代わりに、確実な報酬とともに素早く
    進められるハイリスク・ハイリターンな駆け引き)。ボス階(is_boss_floor)
    と、使うとボス階そのものを飛び越えてしまう1つ手前の階には出現させない
    (ボス戦を飛ばして進行が壊れるのを防ぐため)。"""
    if is_boss_floor(floor) or is_boss_floor(floor + 1):
        return
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
                    candidates.append((x, y))
    if not candidates:
        return
    x, y = random.choice(candidates)
    dungeon[y][x] = 40

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

def place_trial_post():
    """既存の床1マスに試練の石碑(42)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    踏むと不安定な裂け目と同じく必ずエリート戦になるが、勝てば未所持の秘宝が
    1つ確実に手に入る。"""
    _place_single_special_tile(42)

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

def place_ember_forge():
    """既存の床1マスに灯火の鍛冶場(37)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(37)

def place_bard():
    """既存の床1マスに旅の吟遊詩人(38)を配置する。他の特殊床とは隣接しない位置を選ぶ。
    踏むと一度だけ、今の仲間を新しい仲間と交換できる(仲間がいなければ何も起きない)。"""
    _place_single_special_tile(38)

def place_charm_shrine():
    """既存の床1マスに護符の祠(39)を配置する。他の特殊床とは隣接しない位置を選ぶ。"""
    _place_single_special_tile(39)

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

HERO_AURA_TIERS = [(40, "rainbow"), (30, (255, 215, 60)), (20, (215, 220, 235)), (10, (205, 130, 60))]

def hero_aura_color(lv, tmr=0):
    """レベルが上がるほど主人公の見た目が少しずつ「かっこよく」なるよう、
    節目のレベルに達したら背後に光るオーラをまとわせる演出用の色を返す
    (新しいスプライト画像を用意しなくても、既存のgolden_sprite演出と同じ
    半透明の楕円グロー描画を流用するだけで見た目の成長を表現できる)。
    しきい値未満はオーラなし(None)。
    Lv30の金色オーラが最上位の節目のままだったため、さらに上のLv40には
    「伝説」の節目として、時間経過で虹色に色相が回り続けるオーラを追加した
    (固定色ではなく"rainbow"を特別扱いし、tmrを使って毎フレーム色相を
    ずらすことで、金より格上だと一目でわかる特別感を出している)。"""
    for threshold, color in HERO_AURA_TIERS:
        if lv >= threshold:
            if color == "rainbow":
                hue = (tmr % 240) / 240.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
                return (int(r * 255), int(g * 255), int(b * 255))
            return color
    return None

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
                elif tv == 37:
                    # 灯火の鍛冶場(祭壇の画像を炎色にティントして見た目を差別化)
                    bg.blit(get_ember_forge_image(floor_variant), [X, Y])
                elif tv == 38:
                    # 旅の吟遊詩人(商人の画像を紫にティントして見た目を差別化)
                    bg.blit(get_bard_image(), [X, Y])
                elif tv == 39:
                    # 護符の祠(祭壇の画像を神秘的な紫色にティントして見た目を差別化)
                    bg.blit(get_charm_shrine_image(floor_variant), [X, Y])
                elif tv == 41:
                    # 開けた近道(分岐ルート)の入り口。見つけたその場ですぐ分かるよう、
                    # 通常の床とは違う琥珀色のきらめきで目立たせる(imgBranchRoute参照)
                    bg.blit(imgBranchRoute, [X, Y])
                elif tv == 42:
                    # 試練の石碑(守護者の像の画像を紅蓮色にティントして見分けをつける)
                    bg.blit(get_trial_post_image(), [X, Y])
                if tv == 9 or tv == 10 or tv == 40:
                    # 隠し壁(10)・近道の入り口(40)は発見されるまで普通の壁と同じ見た目
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
                    if dy >= 1 and dungeon[dy-1][dx] in (9, 10, 40):
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
                aura_color = hero_aura_color(pl_lv, tmr)
                if aura_color:
                    aura_img = cur_player_set[pl_a]
                    glow_r = 44 + int(5 * abs((tmr % 20) - 10))
                    glow = pygame.Surface((glow_r*2, glow_r*2), pygame.SRCALPHA)
                    pygame.draw.ellipse(glow, (*aura_color, 90), [0, 0, glow_r*2, glow_r*2])
                    cx = X + aura_img.get_width()//2
                    cy = Y - 40 + aura_img.get_height()//2
                    bg.blit(glow, [cx-glow_r, cy-glow_r])
                bg.blit(cur_player_set[pl_a], [X, Y-40])
                draw_item_sparkle(bg, X, Y-40)
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
    apply_second_wind_if_needed()
    draw_low_hp_warning(bg)
    if dp["minimap_enabled"]:
        draw_minimap(bg)
    draw_para(bg, fnt)
    draw_crit_flash(bg)

    if info_timer > 0 and info_message != "":
        draw_text(bg, info_message, 300, 300, fnt, CYAN)

def reveal_hidden_adjacent():
    """プレイヤーが隠し壁(10)に隣接したら、自動的に通れる床(0)にし、
    その裏に隠していた宝箱(1〜2個)も同時に出現させる。宝箱が2つ連なって
    いた場合は『秘密の宝物庫(Secret Vault)』として専用のメッセージ・実績を
    出す(carve_hidden_room参照)。"""
    global hidden_treasure_positions, hidden_chest_cells, _exploration_total, _exploration_seen
    global hidden_wall_sound_pending, info_message, info_timer
    global branch_route_sound_pending
    for dxn, dyn in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = pl_x + dxn, pl_y + dyn
        if 0 <= xx < DUNGEON_W and 0 <= yy < DUNGEON_H and dungeon[yy][xx] == 10:
            dungeon[yy][xx] = 0
            hidden_wall_sound_pending = True
            if hidden_treasure_positions:
                is_vault = len(hidden_treasure_positions) >= 2
                for bx, by in hidden_treasure_positions:
                    dungeon[by][bx] = 1
                    hidden_chest_cells.add((bx, by))
                    # この宝箱マスは今まで壁(9)扱いでexploration_percent()の集計から
                    # 除外されていたため、床になった今、集計に組み込む
                    _exploration_total += 1
                    if explored[by][bx]:
                        _exploration_seen += 1
                hidden_treasure_positions = []
                if is_vault:
                    record_stat("secret_vaults_found")
                    unlock_achievement("secret_vault_finder")
                    if load_stats().get("secret_vaults_found", 0) >= 5:
                        unlock_achievement("secret_vault_hoarder")
                    info_message = "A secret vault opens before you!"
                    info_timer = 60
        if 0 <= xx < DUNGEON_W and 0 <= yy < DUNGEON_H and dungeon[yy][xx] == 40:
            # 近道(分岐ルート)の入り口を発見。隠し壁(10)と違い裏に宝箱は
            # 無く、この場に直接『開けた近道の入り口』(41)を出現させる
            dungeon[yy][xx] = 41
            branch_route_sound_pending = True
            record_stat("branch_routes_found")
            unlock_achievement("branch_route_finder")
            if load_stats().get("branch_routes_found", 0) >= 5:
                unlock_achievement("branch_route_veteran")
            info_message = "A hidden shortcut passage opens beside you!"
            info_timer = 60

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

def generate_branch_route_area():
    """近道(分岐ルート)の入り口から辿り着く、細い一本道の小さな隠しエリア。
    generate_bonus_room()と同じ『dungeon/exploredを丸ごと作り直す』方式だが、
    宝箱だけの安全な部屋ではなく、一本道の途中に宝箱2つとモンスターとの
    遭遇2箇所を仕込む(何もない安全地帯ではなく、多少の危険もある近道に
    するため)。突き当りの階段を使うと、次のフロアをまるごと1つ飛ばして
    深層へ進める(branch_route_floor_skip_pending、idx==2のelse分岐参照)。"""
    global DUNGEON_W, DUNGEON_H, MAZE_W, MAZE_H, dungeon, explored, pl_x, pl_y, pl_d, pl_a
    global golden_sprite_pos, golden_sprite_timer
    golden_sprite_pos = None
    golden_sprite_timer = 0
    DUNGEON_W = 23
    DUNGEON_H = 7
    MAZE_W = DUNGEON_W // 3
    MAZE_H = DUNGEON_H // 3
    dungeon = [[9]*DUNGEON_W for _ in range(DUNGEON_H)]
    midy = DUNGEON_H // 2
    for x in range(1, DUNGEON_W-1):
        dungeon[midy][x] = 0
    # 特別な部屋なので、最初から全体をミニマップに表示する
    explored = [[True]*DUNGEON_W for _ in range(DUNGEON_H)]

    pl_x = 1
    pl_y = midy
    pl_d = 1
    pl_a = 2

    slots = list(range(4, DUNGEON_W-4))
    random.shuffle(slots)
    for cx in slots[:2]:
        dungeon[midy][cx] = 1
    for cx in slots[2:4]:
        dungeon[midy][cx] = 2

    dungeon[midy][DUNGEON_W-2] = 3

    # 通常フロア・ボーナス部屋と同じく、exploration_percent()用の集計値をここで出し直す
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
    treasure_weight = max(1, round(2 * modifier_treasure_weight_mult() * relic_treasure_weight_mult()))
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
    global pending_branch_route
    global ambush_battles_remaining
    global boulder_pos, boulder_timer
    global mimic_battle_active
    global ally_buff_active
    global in_rift_battle
    global in_trial_post_battle
    global spirit_choice_options
    global totem_buff_active, totem_str_bonus, totem_def_bonus
    global doppelganger_battle_active, doppelganger_str, doppelganger_lifemax
    global has_sacred_key
    global chimera_battle_active
    global steps_taken_accum
    global floor_chest_guarantee_used
    global item_sparkle_timer

    if dungeon[pl_y][pl_x] == 1:
        dungeon[pl_y][pl_x] = 0
        if floor >= 6 and not modifier_mimic_immune() and random.randint(0, 99) < min(99, int(MIMIC_CHANCE * modifier_mimic_chance_mult())):
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
        was_hidden_chest = (pl_x, pl_y) in hidden_chest_cells
        if was_hidden_chest:
            hidden_chest_cells.discard((pl_x, pl_y))
        record_stat("treasures_opened")
        if load_stats().get("treasures_opened", 0) >= 150:
            unlock_achievement("treasure_hunter")
        ib = diff_params()["item_bonus"] + skill_item_bonus + pet_item_bonus + modifier_item_bonus() + char_params()["item_bonus"] + relic_item_bonus() + charm_item_bonus()
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
        if floor >= 5 and pet_type is None and random.randint(0, 99) < int(3 * modifier_pet_egg_chance_mult()):
            # まだ仲間がいない場合、低確率(通常3%、Bonded Floorでは6%)でペットの卵に差し替える
            treasure = 10
        if floor_modifier in ("bonanza", "clouded") and not floor_chest_guarantee_used:
            # このフロアで最初に開けた宝箱だけ、確率ではなく確定で中身を決める
            # (2個目以降は通常通りの確率に戻る)。ペットの卵(10)は特別枠なので上書きしない。
            floor_chest_guarantee_used = True
            if floor_modifier == "bonanza" and treasure not in (5, 6, 7, 8, 10):
                treasure = random.choice([7, 8] if floor >= 15 else ([5, 6] if floor >= 10 else [6]))
                set_message("Bonanza! A guaranteed rare treasure!", (255, 215, 60))
            elif floor_modifier == "clouded" and treasure not in (0, 10):
                treasure = 0
                set_message("Clouded Floor... just a Potion.", (150, 150, 150))
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
        # アイテム入手時の画面フラッシュ/ジングル演出は煩わしいという要望のため廃止した
        # (指輪/防御の薬/アミュレット等の希少アイテムを引いても、通常のポーション等と
        # 同様に無音・無演出で受け取るだけになる)。
        if treasure == 10:
            hatch_random_pet()
            info_message = f"{PET_TYPES[pet_type]['name']} hatched!"
            info_timer = 60
        if was_hidden_chest or treasure in (5, 6, 7, 8):
            # 指輪/防御の薬/アミュレット等の希少アイテムや、隠し部屋・秘密の
            # 宝物庫から見つけた宝箱は、画面全体を光らせる派手なフラッシュ
            # (rev172で煩わしいとの声を受け廃止済み)の代わりに、足元だけで
            # 光の粒がきらめく控えめな演出で気づけるようにする
            # (draw_item_sparkle参照)。
            item_sparkle_timer = ITEM_SPARKLE_FRAMES
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
        elif floor >= MAX_FLOOR and not in_endless_mode:
            # 最終ステージのボスを倒し済みの状態(オートセーブ再開など)で
            # 階段に乗った場合は、フロアを増やさずゲームクリア演出へ直行する
            # (エンドレス・ディープス中はfloorがMAX_FLOORを超え続けるが、
            # ボス未撃破の通常フロアでは階段を踏んでも素直に次の階へ進みたいため
            # in_endless_modeの間はこの分岐を通らないようにしている)
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

    if dungeon[pl_y][pl_x] == 41:
        # 近道(分岐ルート)の開けた入り口。踏むと細い一本道のボーナスエリアへ
        # 移動し、そこを抜けるとフロアを1つ余分に飛ばして深層へ進める
        dungeon[pl_y][pl_x] = 0
        pending_branch_route = True
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
        boulder_timer = max(8, BOULDER_CHASE_DURATION + modifier_boulder_chase_duration_bonus())
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
            if load_stats().get("allies_rescued", 0) >= 20:
                unlock_achievement("guardian_angel")
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

    if dungeon[pl_y][pl_x] == 42:
        # 試練の石碑: 裂け目と同じく必ずエリートとの戦闘になるが、
        # 勝てば未所持の秘宝を1つ確実に入手できる
        dungeon[pl_y][pl_x] = 0
        in_trial_post_battle = True
        record_stat("trial_posts_entered")
        info_message = "The trial post ignites... prove your strength!"
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
            if load_stats().get("pressure_plates_triggered", 0) >= 10:
                unlock_achievement("locksmith_master")
            info_message = "A door unlocks somewhere on this floor..."
            info_timer = 50
        return

    if dungeon[pl_y][pl_x] == 26:
        # さまよう精霊: 3つの祝福候補から1つをプレイヤーに選ばせる(idx==64へ)
        dungeon[pl_y][pl_x] = 0
        spirit_choice_options = random.sample(SPIRIT_BLESSINGS, 3)
        record_stat("spirits_encountered")
        if load_stats().get("spirits_encountered", 0) >= 10:
            unlock_achievement("spirit_whisperer")
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
            if load_stats().get("totems_used", 0) >= 15:
                unlock_achievement("totemic")
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
        if load_stats().get("sacred_keys_found", 0) >= 20:
            unlock_achievement("key_collector")
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

    if dungeon[pl_y][pl_x] == 37:
        # 灯火の鍛冶場: 所持しているブレイズジェムを全て消費し、永続STRに変える。
        # ブレイズジェムを1個も持っていなければ何も起きず、床はそのまま残る
        # (聖なる鍵が無いと開かない封印の宝物庫と同じ「条件を満たすまで居座る」方式)。
        if blazegem > 0:
            dungeon[pl_y][pl_x] = 0
            gems_used = blazegem
            blazegem = 0
            gained_str = int(gems_used * EMBER_FORGE_STR_PER_GEM * modifier_ember_forge_str_mult())
            pl_str += gained_str
            record_stat("ember_forges_used")
            if load_stats().get("ember_forges_used", 0) >= 10:
                unlock_achievement("master_smith")
            info_message = f"The forge consumes {gems_used} Blaze Gem(s)... +{gained_str} STR!"
            info_timer = 55
            # アイテム入手時と同じジングルは煩わしいという要望のため廃止していたが、
            # 画面全体を光らせるフラッシュ演出も同じ理由(演出が煩わしい)で
            # プレイヤーからの指摘対象になり得るため、護符の祠・レアアイテムと
            # 同じ「足元だけの光の粒」演出(item_sparkle)に統一した。
            item_sparkle_timer = ITEM_SPARKLE_FRAMES
        else:
            info_message = "The forge needs Blaze Gems to work its magic."
            info_timer = 40
        return

    if dungeon[pl_y][pl_x] == 38:
        # 旅の吟遊詩人: 一度だけ、今の仲間を新しい仲間と交換できる(その後タイルは消える)
        dungeon[pl_y][pl_x] = 0
        idx = 68
        tmr = 0
        try:
            moving = False
            move_progress = 0.0
            hold_dir = None
            hold_timer = 0
        except NameError:
            pass
        return

    if dungeon[pl_y][pl_x] == 39:
        # 護符の祠: まだ持っていない護符があればランダムに1つ授かる
        # (灯火の鍛冶場と違い、所持品は何も消費しない)。全種類集め終えて
        # いた場合は何も起きず、祠だけがそのまま消える。
        dungeon[pl_y][pl_x] = 0
        charm_pool = [c for c in CHARM_DEFS if not load_charms()["found"].get(c["key"], False)]
        if charm_pool:
            new_charm = random.choice(charm_pool)
            if unlock_charm(new_charm["key"]):
                unlock_achievement("charm_seeker")
                if all(load_charms()["found"].get(c["key"], False) for c in CHARM_DEFS):
                    unlock_achievement("charm_collector")
            item_sparkle_timer = ITEM_SPARKLE_FRAMES
            info_message = f"The shrine grants you the {new_charm['name']}!"
            info_timer = 55
        else:
            info_message = "The shrine hums quietly... you already carry every Charm."
            info_timer = 40
        return

def draw_text(bg, txt, x, y, fnt, col):
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def apply_second_wind_if_needed():
    """Second Wind Floorの発動判定。draw_low_hp_warning()と同じく探索/バトル
    どちらの画面からも毎フレーム呼ばれるため、ダメージの発生源(敵の攻撃/毒/
    罠/飢餓など)を個別に書き換えなくても、HPが20%を切った瞬間を一律に
    検知できる(低HP警告の実装パターンをそのまま踏襲した)。"""
    global second_wind_used_this_floor, pl_life, info_message, info_timer
    if not modifier_second_wind() or second_wind_used_this_floor:
        return
    if pl_lifemax <= 0 or pl_life <= 0:
        return
    if pl_life / pl_lifemax > LOW_HP_WARNING_RATIO:
        return
    second_wind_used_this_floor = True
    heal = max(1, int(pl_lifemax * SECOND_WIND_HEAL_RATIO))
    pl_life = min(pl_lifemax, pl_life + heal)
    msg = f"Second Wind! +{heal}HP"
    set_message(msg, (150, 255, 190))
    info_message = msg
    info_timer = 90

def draw_low_hp_warning(bg):
    """HPが最大値の20%を切ると、心拍のように速く脈打つ赤い縁取りを
    画面端に表示する(探索/バトル共通)。崩落演出よりも脈拍を速くして、
    見分けがつくようにしている。Screen Shake/Screen Flashと同様、光過敏な
    プレイヤー向けにlow_hp_pulse_enabledでオフにできる。
    従来はこの警告が視覚演出のみで、画面外に目をやっていると気づけなかった
    ため、閾値をまたいで警告状態に入った瞬間だけse[0]を1回鳴らすようにした
    (脈打つたびに毎回鳴らすと煩わしいので、警告に入った最初の一度だけ)。"""
    global low_hp_warning_sound_pending, low_hp_warning_active
    if not low_hp_pulse_enabled:
        low_hp_warning_active = False
        return
    if pl_lifemax <= 0 or pl_life <= 0:
        low_hp_warning_active = False
        return
    if pl_life / pl_lifemax > LOW_HP_WARNING_RATIO:
        low_hp_warning_active = False
        return
    if not low_hp_warning_active:
        low_hp_warning_active = True
        low_hp_warning_sound_pending = True
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

def draw_item_sparkle(bg, X, Y):
    """希少アイテム・隠し部屋/秘密の宝物庫の宝箱を手に入れた瞬間、画面全体を
    光らせる代わりに、プレイヤーの足元にだけ光の粒がきらめく演出を入れる
    (draw_crit_flashと同じくscreen_flash_enabledがOFFなら描画をスキップし、
    タイマーだけ進めて古い演出が急に出ないようにする)。alphaは0〜255に
    必ずクランプする(draw_crit_flashの既知の不具合パターンと同じ注意)。"""
    global item_sparkle_timer
    if item_sparkle_timer <= 0:
        return
    if not screen_flash_enabled:
        item_sparkle_timer = 0
        return
    progress = item_sparkle_timer / ITEM_SPARKLE_FRAMES
    alpha = max(0, min(255, int(230 * progress)))
    size = max(1, int(5 * progress))
    cx = X + 40
    for i, (ox, oy) in enumerate(ITEM_SPARKLE_OFFSETS):
        bob = int(4 * abs(((tmr + i * 3) % 12) - 6) / 6) - 2
        spark = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(spark, (255, 235, 150, alpha), (6, 6), size)
        bg.blit(spark, [cx + ox - 6, Y + oy + bob - 6])
    item_sparkle_timer -= 1

ACHIEVEMENT_TOAST_W = 420
ACHIEVEMENT_TOAST_H = 66
_achievement_toast_hdr_font = None
_achievement_toast_lbl_font = None

def draw_achievement_toast(bg):
    """実績解除時、画面上部にゴールドのバナーをスライドインさせ、バッジ画像と
    共に『Achievement Unlocked!』を表示する。探索中/バトル中/メニュー中を
    問わずメインループの描画の最後(画面更新の直前)から呼ばれるので、
    どの画面状態でも同じように目立つ。"""
    global achievement_toast_timer, achievement_toast_label
    global _achievement_toast_hdr_font, _achievement_toast_lbl_font
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
    if achievement_toast_timer <= 0 and achievement_toast_queue:
        achievement_toast_label = achievement_toast_queue.pop(0)
        achievement_toast_timer = ACHIEVEMENT_TOAST_FRAMES

_relic_toast_hdr_font = None
_relic_toast_lbl_font = None

def draw_relic_toast(bg):
    """秘宝入手時、実績解除トーストと同じゴールドバナー方式(ただし配色は
    teal系にして見分けが付くようにした)でスライドインさせる。実績トーストと
    完全に同じY座標に出すと文字が重なって読めなくなるため、実績トーストが
    表示中の間だけその真下(ACHIEVEMENT_TOAST_H + 隙間)にずらし、実績トースト
    が出ていなければ画面上端に詰めて表示する。"""
    global relic_toast_timer, relic_toast_label
    global _relic_toast_hdr_font, _relic_toast_lbl_font
    if relic_toast_timer <= 0:
        return
    elapsed = RELIC_TOAST_FRAMES - relic_toast_timer
    if elapsed < RELIC_TOAST_SLIDE:
        t = elapsed / RELIC_TOAST_SLIDE
        y = int(-ACHIEVEMENT_TOAST_H * (1 - t))
        alpha = int(255 * t)
    elif relic_toast_timer <= RELIC_TOAST_FADE:
        t = relic_toast_timer / RELIC_TOAST_FADE
        y = 0
        alpha = int(255 * t)
    else:
        y = 0
        alpha = 255
    x = (880 - ACHIEVEMENT_TOAST_W) // 2
    base = 14 + (ACHIEVEMENT_TOAST_H + RELIC_TOAST_GAP if achievement_toast_timer > 0 else 0)
    top = base + y
    glow = 140 + int(90 * abs((tmr % 24) - 12) / 12)
    panel = pygame.Surface((ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H), pygame.SRCALPHA)
    panel.fill((5, 22, 22, min(230, alpha)))
    pygame.draw.rect(panel, (90, 220, 200, min(255, alpha)), [0, 0, ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H], width=3)
    pygame.draw.rect(panel, (170, 245, 230, min(glow, alpha)), [0, 0, ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H], width=1)
    bg.blit(panel, [x, top])
    if _relic_toast_hdr_font is None:
        _relic_toast_hdr_font = pygame.font.Font(None, 22)
        _relic_toast_lbl_font = pygame.font.Font(None, 24)
    hdr = _relic_toast_hdr_font.render("RELIC FOUND!", True, (150, 235, 220))
    hdr.set_alpha(alpha)
    bg.blit(hdr, [x + 16, top + 10])
    lbl = _relic_toast_lbl_font.render(relic_toast_label, True, WHITE)
    lbl.set_alpha(alpha)
    bg.blit(lbl, [x + 16, top + 34])
    relic_toast_timer -= 1
    if relic_toast_timer <= 0 and relic_toast_queue:
        relic_toast_label = relic_toast_queue.pop(0)
        relic_toast_timer = RELIC_TOAST_FRAMES

_charm_toast_hdr_font = None
_charm_toast_lbl_font = None

def draw_charm_toast(bg):
    """護符入手時、秘宝発見トーストと同じ方式(紫系の配色で見分けを付ける)で
    スライドインさせる。実績トースト・秘宝トーストのどちらか、または両方が
    表示中の場合はその真下にずらして表示し、3つのトーストが同時に出ても
    文字が重ならないようにする。"""
    global charm_toast_timer, charm_toast_label
    global _charm_toast_hdr_font, _charm_toast_lbl_font
    if charm_toast_timer <= 0:
        return
    elapsed = CHARM_TOAST_FRAMES - charm_toast_timer
    if elapsed < CHARM_TOAST_SLIDE:
        t = elapsed / CHARM_TOAST_SLIDE
        y = int(-ACHIEVEMENT_TOAST_H * (1 - t))
        alpha = int(255 * t)
    elif charm_toast_timer <= CHARM_TOAST_FADE:
        t = charm_toast_timer / CHARM_TOAST_FADE
        y = 0
        alpha = int(255 * t)
    else:
        y = 0
        alpha = 255
    x = (880 - ACHIEVEMENT_TOAST_W) // 2
    base = 14
    if achievement_toast_timer > 0:
        base += ACHIEVEMENT_TOAST_H + CHARM_TOAST_GAP
    if relic_toast_timer > 0:
        base += ACHIEVEMENT_TOAST_H + CHARM_TOAST_GAP
    top = base + y
    glow = 140 + int(90 * abs((tmr % 24) - 12) / 12)
    panel = pygame.Surface((ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H), pygame.SRCALPHA)
    panel.fill((22, 12, 30, min(230, alpha)))
    pygame.draw.rect(panel, (190, 140, 235, min(255, alpha)), [0, 0, ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H], width=3)
    pygame.draw.rect(panel, (225, 195, 250, min(glow, alpha)), [0, 0, ACHIEVEMENT_TOAST_W, ACHIEVEMENT_TOAST_H], width=1)
    bg.blit(panel, [x, top])
    if _charm_toast_hdr_font is None:
        _charm_toast_hdr_font = pygame.font.Font(None, 22)
        _charm_toast_lbl_font = pygame.font.Font(None, 24)
    hdr = _charm_toast_hdr_font.render("CHARM FOUND!", True, (215, 180, 245))
    hdr.set_alpha(alpha)
    bg.blit(hdr, [x + 16, top + 10])
    lbl = _charm_toast_lbl_font.render(charm_toast_label, True, WHITE)
    lbl.set_alpha(alpha)
    bg.blit(lbl, [x + 16, top + 34])
    charm_toast_timer -= 1
    if charm_toast_timer <= 0 and charm_toast_queue:
        charm_toast_label = charm_toast_queue.pop(0)
        charm_toast_timer = CHARM_TOAST_FRAMES

_pet_icon_scaled_cache = {}
_def_pill_warn_icon_cache = {}

def draw_pet_status(bg, x, y, fnt):
    """『Pet: 名前 (効果)』の左側に小さなアイコンを添えて表示する。
    アイコンはテキストの行の高さに収まるよう自動で縮小する。
    一定間隔でrev画像(左右反転版)と入れ替えて、ペットが生きているように
    ちょこちょこ向きを変える簡単なアイドルアニメーションにする。
    pet_typeが変わらない限りスケール済み画像は同じなので、smoothscale結果を
    キャッシュして毎フレームの再生成を避ける。効果(desc)もラベルに含めて、
    ペット画面を別途開かなくても今の仲間が何をしてくれるのか常時わかるようにする。"""
    rev = (tmr // 40) % 2 != 0
    if rev:
        icon = imgPetRev.get(pet_type, imgPet.get(pet_type))
    else:
        icon = imgPet.get(pet_type)
    label = f"Pet: {PET_TYPES[pet_type]['name']} ({PET_TYPES[pet_type]['desc']})"
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
    elif 0 < food <= FOOD_CRITICAL_WARNING_THRESHOLD and tmr%2 == 0:
        col = FOOD_CRITICAL_WARNING_COLOR
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
    global pl_charge, pl_poison, pl_bleed, pl_frozen, battle_took_damage
    global combo_count, combo_record_shown_this_battle
    global is_elite
    global abyssal_warden_healed_this_battle
    global emy_poison, emy_poisoned_this_battle
    global emy_stun, emy_stunned_this_battle
    pl_charge = False
    pl_poison = 0
    pl_bleed = 0
    pl_frozen = 0
    battle_took_damage = False
    combo_count = 0
    combo_record_shown_this_battle = False
    abyssal_warden_healed_this_battle = False
    emy_poison = 0
    emy_poisoned_this_battle = False
    emy_stun = 0
    emy_stunned_this_battle = False
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
    if floor > 90:
        # フロア91以降(エンドレス・ディープス)は、フロア70-90の通常
        # ダンジョンと同じtyp8-31の顔ぶれをそのまま引き継ぐだけで、この
        # 新モードだけの専用モンスターが1体も居なかった。typ32
        # 「Abyssal Warden」だけをエンドレス・ディープス限定で混ぜ、
        # 潜り続けても新鮮味が保たれるようにした。typ33「Warbreaker Wight」
        # (今回追加分)はfloor>=30から出現する敵のため、この帯(floor>90は
        # 独立したelifの分岐で30〜89の帯を引き継がない)にも明示的に含めた。
        # typ36「Cinder Ward」(今回追加分)もfloor>=70の深層専用帯のため、
        # ここでも引き続き出現させる。typ38「Ashbound Titan」もfloor>=30から
        # 混ざる帯としてここでも引き続き出現させる。typ39「Silence Wisp」
        # (今回追加分)もfloor>=30から混ざる帯としてここでも引き続き出現させる。
        # typ40「Vengeful Wraith」(rev199で追加)もfloor>=70の深層専用帯のため、
        # ここでも引き続き出現させる。typ41「Bloodthorn Revenant」・typ42
        # 「Permafrost Wyrm」(今回追加分)もfloor>=30から混ざる帯として
        # ここでも引き続き出現させる。
        typ = random.choice(list(range(8, 32)) + [32, 33, 36, 38, 39, 40, 41, 42])
        lev = random.randint(floor - 2, floor)
    elif floor >= 70:
        # フロア70以降だけ、通算60階(30〜90階)ずっと同じtyp8-26の顔ぶれが
        # 使い回されていた終盤の遭遇マンネリを崩すため、新しいtyp27
        # 「Voidforged Golem」・typ28「Mirror Wraith」・typ29「Hollow Widow」・
        # typ30「Chain Warden」・typ31「Frenzied Revenant」だけが混ざるようにした
        # (それ未満の階には出ない)。typ33「Warbreaker Wight」もfloor>=30から
        # 混ざる帯としてここでも引き続き出現させる。typ36「Cinder Ward」
        # (今回追加分)は、爆炎石を軽減する新しい駆け引きを持つ深層専用の
        # 新モンスターとして、この帯で初めて混ざるようにした。typ38
        # 「Ashbound Titan」(今回追加分)もfloor>=30から混ざる帯として
        # ここでも引き続き出現させる。typ39「Silence Wisp」(今回追加分)も
        # floor>=30から混ざる帯としてここでも引き続き出現させる。typ40
        # 「Vengeful Wraith」(rev199で追加)は、フロア70以降に混ざる新しい
        # 深層専用モンスターとしてここで初めて出現させる。typ41「Bloodthorn
        # Revenant」・typ42「Permafrost Wyrm」(今回追加分)もfloor>=30から
        # 混ざる帯としてここでも引き続き出現させる。
        typ = random.choice(list(range(8, 32)) + [33, 36, 38, 39, 40, 41, 42])
        lev = random.randint(floor - 2, floor)
    elif floor >= 30:
        # フロア30〜69(ステージ2以降、typ27-29の深層専用勢が出ない帯)は
        # ずっとtyp8-26の顔ぶれだけが使い回され続けていたため、typ30
        # 「Chain Warden」・typ31「Frenzied Revenant」はこの中盤の帯にも
        # 混ざるようにした(範囲が8-26と非連続になるため、randintではなく
        # choiceでリストを結合する)。typ33「Warbreaker Wight」(今回追加分)も
        # 同じ中盤の帯からプレイヤーの防御コマンドへの駆け引きとして混ぜる。
        # typ38「Ashbound Titan」(今回追加分)も、通常攻撃の威力を直接鈍らせる
        # 新しい駆け引きとしてこの中盤の帯から混ぜる。typ39「Silence Wisp」
        # (今回追加分)も、コンボの蓄積そのものを封じる新しい駆け引きとして
        # この中盤〜深層の帯から混ぜる。typ41「Bloodthorn Revenant」(今回
        # 追加分)も、どんな対策でも軽減できない持続ダメージ「出血」を
        # 新しく持ち込む敵として、この中盤の帯から混ぜる。typ42
        # 「Permafrost Wyrm」(今回追加分)も、ダメージを伴わずプレイヤーの
        # 手番そのものを封じる新しい状態異常「凍結」を持ち込む敵として、
        # この中盤の帯から混ぜる。
        typ = random.choice(list(range(8, 27)) + [30, 31, 33, 38, 39, 41, 42])
        lev = random.randint(floor - 2, floor)
    elif floor >= 15:
        # typ34「Gloom Sprite」は、フロア30以降の深層専用勢(typ27-33)とは
        # 逆に、フロア6以降・フロア30未満の序盤〜中盤の帯にだけ混ざる初めての
        # 「仕組み持ち」の敵(範囲が0-16と非連続になるため、randintではなく
        # choiceでリストを結合する)。typ37「Numbing Hornet」(今回追加分)も
        # 同じ帯に混ざる、戦闘中ずっと会心率を下げ続ける新モンスター。
        typ = random.choice(list(range(0, 17)) + [34, 37])
        lev = random.randint(floor - 4, floor)
    elif floor >= 11:
        typ = random.choice(list(range(0, 17)) + [34, 37])
        lev = random.randint(floor - 5, floor)
    elif floor >= GLOOM_SPRITE_MIN_FLOOR:
        typ = random.choice(list(range(0, floor + 1)) + [34, 37])
        lev = random.randint(1, floor)
    else:
        # typ35「Hungry Rat」(今回追加分)は、フロア1-5(GLOOM_SPRITE_MIN_FLOOR
        # 未満)限定で混ざる、この帯で初めての「仕組み持ち」の敵(範囲が
        # 0-floorと非連続になるため、randintではなくchoiceでリストを結合する)。
        typ = random.choice(list(range(0, floor + 1)) + [35])
        lev = random.randint(1, floor)
    emy_lv = lev
    is_elite = random.randint(0, 99) < (ELITE_CHANCE + modifier_elite_chance_bonus())
    if in_rift_battle:
        is_elite = True  # 裂け目から出てくる敵は必ずエリート
    if in_trial_post_battle:
        is_elite = True  # 試練の石碑から出てくる敵は必ずエリート
    imgEnemy = load_enemy_image(enemy_image_file(typ))
    if typ == 27:
        imgEnemy = tint_surface(imgEnemy, VOID_GOLEM_TINT)
    elif typ == 28:
        imgEnemy = tint_surface(imgEnemy, MIRROR_WRAITH_TINT)
    elif typ == 29:
        imgEnemy = tint_surface(imgEnemy, HOLLOW_WIDOW_TINT)
    elif typ == 30:
        imgEnemy = tint_surface(imgEnemy, CHAIN_WARDEN_TINT)
    elif typ == 31:
        imgEnemy = tint_surface(imgEnemy, FRENZIED_REVENANT_TINT)
    elif typ == 32:
        imgEnemy = tint_surface(imgEnemy, ABYSSAL_WARDEN_TINT)
    elif typ == 33:
        imgEnemy = tint_surface(imgEnemy, WARBREAKER_TINT)
    elif typ == 34:
        imgEnemy = tint_surface(imgEnemy, GLOOM_SPRITE_TINT)
    elif typ == 35:
        imgEnemy = tint_surface(imgEnemy, HUNGRY_RAT_TINT)
    elif typ == 36:
        imgEnemy = tint_surface(imgEnemy, CINDER_WARD_TINT)
    elif typ == 37:
        imgEnemy = tint_surface(imgEnemy, NUMBING_HORNET_TINT)
    elif typ == 38:
        imgEnemy = tint_surface(imgEnemy, ASHBOUND_TITAN_TINT)
    elif typ == 39:
        imgEnemy = tint_surface(imgEnemy, SILENCE_WISP_TINT)
    elif typ == 40:
        imgEnemy = tint_surface(imgEnemy, VENGEFUL_WRAITH_TINT)
    elif typ == 41:
        imgEnemy = tint_surface(imgEnemy, BLOODTHORN_REVENANT_TINT)
    elif typ == 42:
        imgEnemy = tint_surface(imgEnemy, PERMAFROST_WYRM_TINT)
    if is_elite:
        imgEnemy = tint_surface(imgEnemy, ELITE_TINT)
    emy_name = ("Elite " if is_elite else "") + EMY_NAME[typ]+" LV"+str(lev)
    if typ == 34:
        # Gloom Sprite(typ34)はフロア6-29の序盤〜中盤帯に混ざるため、通常の
        # 計算式(60*(typ+1))をtyp番号34にそのまま当てはめると、同じ帯のtyp0-16
        # (最大でも60*17)よりも桁違いに強くなってしまう。typ8相当(中位)の
        # 強さになるよう基準値を差し替えて、この帯の他の敵と釣り合うようにした。
        emy_lifemax = 60*9+(lev-1)*10
    elif typ == 35:
        # Hungry Rat(typ35)はフロア1-5の最序盤帯に混ざるため、通常の計算式
        # (60*(typ+1))をtyp番号35にそのまま当てはめると桁違いに強くなって
        # しまう。この帯の他の敵(typ0-5)と釣り合うよう、最弱のtyp0(Green
        # slime)と同じ基準値にした。
        emy_lifemax = 60*1+(lev-1)*10
    elif typ == 37:
        # Numbing Hornet(typ37)もGloom Spriteと同じフロア6-29の序盤〜中盤帯に
        # 混ざるため、通常の計算式(60*(typ+1))を桁違いに強くしないよう、
        # Gloom Spriteと同じtyp8相当(中位)の基準値に揃えた。
        emy_lifemax = 60*9+(lev-1)*10
    else:
        emy_lifemax = 60*(typ+1)+(lev-1)*10
    emy_str = int(emy_lifemax/8)
    dp = diff_params()
    emy_lifemax = max(1, int(emy_lifemax * dp["enemy_life_mult"] * modifier_enemy_life_mult()))
    emy_str = max(1, int(emy_str * dp["enemy_str_mult"]))
    if is_elite:
        emy_lifemax = int(emy_lifemax * ELITE_LIFE_MULT)
        emy_str = int(emy_str * ELITE_STR_MULT)
    if in_rift_battle:
        emy_lifemax = int(emy_lifemax * RIFT_LIFE_MULT)
        emy_str = int(emy_str * RIFT_STR_MULT)
    if in_trial_post_battle:
        emy_lifemax = int(emy_lifemax * TRIAL_POST_LIFE_MULT)
        emy_str = int(emy_str * TRIAL_POST_STR_MULT)
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
    """ボスの表示名をフロア番号から算出する(init_boss_battleと図鑑の両方から使う共通ロジック)。
    エンドレス・ディープス(フロア91以降)では毎回「Final Boss」と表示されると
    紛らわしいため、MAX_FLOORちょうど(通常周回の最終ボス)とそれより深い
    エンドレス中のボスとで表示名を分けている。"""
    stg = current_stage(fl)
    lf = stage_local_floor(fl)
    if fl > MAX_FLOOR:
        return f"Depths Boss (Floor {fl})"
    elif fl == MAX_FLOOR:
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
    global pl_charge, pl_poison, pl_bleed, pl_frozen, battle_took_damage
    global combo_count
    global boss_phase2
    global is_elite
    global emy_poison, emy_poisoned_this_battle
    global emy_stun, emy_stunned_this_battle
    pl_charge = False
    pl_poison = 0
    pl_bleed = 0
    pl_frozen = 0
    battle_took_damage = False
    combo_count = 0
    boss_phase2 = False
    is_elite = False
    emy_poison = 0
    emy_poisoned_this_battle = False
    emy_stun = 0
    emy_stunned_this_battle = False
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
    global pl_charge, pl_poison, pl_bleed, pl_frozen, battle_took_damage
    global combo_count
    global boss_phase2
    global is_elite
    global emy_poison, emy_poisoned_this_battle
    global emy_stun, emy_stunned_this_battle
    pl_charge = False
    pl_poison = 0
    pl_bleed = 0
    pl_frozen = 0
    battle_took_damage = False
    combo_count = 0
    boss_phase2 = False
    is_elite = False
    emy_poison = 0
    emy_poisoned_this_battle = False
    emy_stun = 0
    emy_stunned_this_battle = False
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

_true_hidden_boss_img_cache = None

def get_true_hidden_boss_image():
    """??? The Voidcrownedの見た目。新規スプライト生成はプロキシの接続状態
    (`__agentproxy/status`)を確認したところ、huggingface.co/hf.spaceへの
    接続がこの実行環境のポリシーで403拒否されることを今回も確認できたため、
    これまでの深層モンスターと同じく既存の隠しボス画像(enemy_hidden_boss.png)
    を色調変更(tint_surface)した色違いとして使い回す。"""
    global _true_hidden_boss_img_cache
    if _true_hidden_boss_img_cache is None:
        _true_hidden_boss_img_cache = tint_surface(load_enemy_image(HIDDEN_BOSS_IMAGE), TRUE_HIDDEN_BOSS_TINT)
    return _true_hidden_boss_img_cache

def init_true_hidden_boss_battle():
    """真の隠しボス「??? The Voidcrowned」。既存の隠しボス(??? The Unbound)を
    通算3回倒して初めて挑戦できる、隠しステージのさらに奥にいる一体で、
    Unboundよりもさらに強い専用のステータスを持つ。"""
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, typ, emy_lv
    global pl_charge, pl_poison, pl_bleed, pl_frozen, battle_took_damage
    global combo_count
    global boss_phase2
    global is_elite
    global emy_poison, emy_poisoned_this_battle
    global emy_stun, emy_stunned_this_battle
    pl_charge = False
    pl_poison = 0
    pl_bleed = 0
    pl_frozen = 0
    battle_took_damage = False
    combo_count = 0
    boss_phase2 = False
    is_elite = False
    emy_poison = 0
    emy_poisoned_this_battle = False
    emy_stun = 0
    emy_stunned_this_battle = False
    typ = 12
    emy_lv = TRUE_HIDDEN_FLOOR
    dp = diff_params()
    emy_lifemax = max(1, int((900 + MAX_FLOOR*60) * 3.2 * dp["enemy_life_mult"]))
    emy_str = max(1, int((50 + MAX_FLOOR*7) * 2.2 * dp["enemy_str_mult"]))
    emy_life = emy_lifemax
    imgEnemy = get_true_hidden_boss_image()
    emy_name = "??? The Voidcrowned"
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()
    # BOSS_BESTIARYには登録しない(通常の図鑑進捗・Bestiary Master実績の対象外の、
    # 純粋な追加チャレンジとして扱う)ため、record_boss_seenは呼ばない。

# --- エコーバトル用の状態 ---
in_echo_battle = False
echo_target_floor = None

def init_echo_boss_battle(target_floor):
    """図鑑から挑む再戦。ダンジョン進行用のグローバルfloorは一切書き換えず、
    target_floorの数値だけを使って本来のボスと同じ強さを再現する。
    見た目は色反転版の専用画像(ECHO_ORI_MAP)を使う。"""
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, typ, emy_lv
    global pl_charge, pl_poison, pl_bleed, pl_frozen, battle_took_damage
    global combo_count
    global boss_phase2
    global is_elite
    global emy_poison, emy_poisoned_this_battle
    global emy_stun, emy_stunned_this_battle
    pl_charge = False
    pl_poison = 0
    pl_bleed = 0
    pl_frozen = 0
    battle_took_damage = False
    combo_count = 0
    boss_phase2 = False
    is_elite = False
    emy_poison = 0
    emy_poisoned_this_battle = False
    emy_stun = 0
    emy_stunned_this_battle = False
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
    隠しボス挑戦と同様にそこそこ強めのステータスを即座に用意する。
    【バグ修正】BGMは従来、闘技場(Arena of Trials)と全く同じ
    Tolerance_Deviation.mp3を共用していた。エコーバトルは「特定のフロアの
    過去のボス戦を再現する」場面なのに、闘技場の緊張感を煽る専用曲が
    流れるのは場面と噛み合っていなかったため、再現対象のフロア
    (target_floor)に対応する、そのステージ本来の戦闘曲
    (bgm_battle_for_floor)を流すよう変更した。"""
    global pl_lifemax, pl_life, pl_str, pl_def_base, pl_def_buff, def_pill
    global food, food_acc, potion, blazegem, pl_poison, pl_bleed, pl_frozen, pl_charge, battle_took_damage
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
    pl_bleed = 0
    pl_frozen = 0
    pl_charge = False
    battle_took_damage = False
    in_echo_battle = True
    echo_target_floor = target_floor
    init_echo_boss_battle(target_floor)
    init_message()
    pygame.mixer.music.load(bgm_battle_for_floor(target_floor))
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
    """'Lv◯'表示とEXPバーの高さを揃え、バーをテキストのすぐ右に配置する。
    バーの右側には現在レベル内でのEXP進捗を%表示する(従来はバーの塗りを
    目で見比べるしかなく、あと何%でレベルアップかが分かりにくかったため、
    コンボ%表示・逃走成功率表示と同じ考え方で数値化した)。"""
    label = f"Lv{pl_lv}"
    lw, lh = fnt.size(label)
    draw_text(bg, label, x, y, fnt, WHITE)
    bar_y = y + (lh - bar_h)//2
    bar_x = x + lw + 8
    draw_exp_bar(bg, bar_x, bar_y, bar_w, bar_h)
    lo = exp_threshold(pl_lv)
    hi = exp_threshold(pl_lv + 1)
    span = max(1, hi - lo)
    prog = max(0, min(pl_exp - lo, span))
    pct = int(100 * prog / span)
    draw_text(bg, f"{pct}%", bar_x + bar_w + 8, y, fnt, (200, 220, 200))
        
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
    if emy_lifemax > 0:
        # プレイヤー側のHPは"◯/◯"の数値表示があるのに対し、敵側はバーのみで
        # 実数値が見えなかった。バーの目分量だけでは「あと何発で倒せるか」の
        # 判断がしにくかったため、プレイヤーHP表示と同じ書式で敵HPバーの右側にも
        # 数値を添えるようにした。
        draw_text(bg, f"{emy_life}/{emy_lifemax}", 548, 578, fnt, WHITE)
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
    equipped_charm = get_equipped_charm()
    if equipped_charm:
        # 護符はいつでも無料で付け替えられる分、今どれを装備しているか
        # 忘れやすい。フロア特性と同じ常時表示のステータス行に追加し、
        # 一長一短のトレードオフを常にバトル中も意識できるようにした。
        draw_text(bg, f"CHARM: {equipped_charm['name']}", 60, status_y, fnt, (215, 180, 245))
        status_y += 24
    total_crit_frac = skill_crit_chance + modifier_crit_chance_bonus() + char_params()["crit_bonus"] + relic_crit_bonus() + charm_crit_bonus() + pet_crit_bonus
    if typ == 37:
        # Numbing Hornetと戦っている間は会心率が半減しているため、表示上の
        # 数値もidx==12の実際の判定と同じ倍率を反映させ、見た目と実挙動が
        # 食い違わないようにする。
        total_crit_frac *= NUMBING_HORNET_CRIT_MULT
    total_crit_pct = int(round(total_crit_frac * 100))
    if total_crit_pct > 0:
        # 会心率はスキル(Perfect Strike)・フロア特性(Fortunate/Unlucky)・
        # キャラクター(Rogue)の3つが絡み合って決まるため、合計値を確認する
        # 手段がこれまで無かった。EXP%・コンボ%表示と同じ「目安を数値で
        # 明確にする」考え方をバトル画面にも常時表示するようにした。
        crit_label = "CRIT CHANCE (dulled)" if typ == 37 else "CRIT CHANCE"
        draw_text(bg, f"{crit_label} {total_crit_pct}%", 60, status_y, fnt, (255, 210, 90) if typ != 37 else (170, 150, 220))
        status_y += 24
    # 【新要素】Ranger(rev209追加)のcrit_dmg_bonusは、これまでのCRIT CHANCE
    # (発生率)表示と違い「当たった時の威力」を底上げする値のため、同じ
    # 「合計値を数値で明確にする」考え方で専用の行を追加した(0の時は非表示)。
    crit_dmg_bonus_total = char_params().get("crit_dmg_bonus", 0.0)
    if crit_dmg_bonus_total > 0:
        draw_text(bg, f"CRIT DMG +{crit_dmg_bonus_total:.1f}x", 60, status_y, fnt, (255, 140, 90))
        status_y += 24
    if pl_poison > 0:
        draw_text(bg, f"POISON x{pl_poison}", 60, status_y, fnt, (190, 80, 220))
        status_y += 24
    if pl_bleed > 0:
        draw_text(bg, f"BLEED x{pl_bleed}", 60, status_y, fnt, (200, 30, 30))
        status_y += 24
    if emy_poison > 0:
        # Serpent's Fangで敵を毒にした後、あと何ターン効いているか自分の
        # 記憶頼りにならないよう、POISON表示と同じ常時表示のステータス行に
        # 敵側の状態も並べて表示する(色はプレイヤー毒の紫と見分けやすい黄緑)。
        draw_text(bg, f"ENEMY POISONED x{emy_poison}", 60, status_y, fnt, (150, 210, 90))
        status_y += 24
    if emy_stun > 0:
        # 秘宝Thunderclap Idol(rev202追加)で気絶させた敵は、次の敵ターンの頭で
        # 行動不能になる。ENEMY POISONEDと同じ常時表示のステータス行に並べ、
        # 今のバトルで気絶が乗っているかひと目でわかるようにした。
        draw_text(bg, "ENEMY STUNNED", 60, status_y, fnt, (235, 210, 90))
        status_y += 24
    if pl_def_buff > 0:
        # Defend/Counterで得られる被ダメージ軽減(pl_def_buff)は、これまで
        # 画面上に何の表示も無く、あと何ターン軽減が残っているか覚えておく
        # しかなかった。今回追加したWarbreaker Wight(Defend中だとこの軽減を
        # 無視して攻撃してくる敵)への対策としても、軽減が今かかっているか
        # ひと目でわかる必要が出てきたため、POISON/FOCUSEDと同じ常時表示の
        # ステータス行に追加した。
        draw_text(bg, "GUARDING", 60, status_y, fnt, (120, 180, 255))
        status_y += 24
    if pl_charge:
        # Focusコマンド使用後、次の通常攻撃が+50%になる状態(pl_charge)は
        # これまで画面上に何の表示も無く、プレイヤーは使ったこと自体を
        # 覚えておくしかなかった。POISON/COMBOと同じ常時表示のステータス行に
        # 並べ、次の攻撃が強化されていることを常に確認できるようにした。
        draw_text(bg, "FOCUSED! (next attack +50%)", 60, status_y, fnt, (255, 160, 60))
        status_y += 24
    if typ == 39:
        # Silence Wispと戦っている間は通常攻撃を当ててもコンボが一切たまらない
        # ため、POISON/GUARDING/FOCUSEDと同じ常時表示のステータス行に
        # 「COMBO SILENCED」を出し、コンボが積み上がらない理由を常に確認
        # できるようにする(Numbing Hornetの「CRIT CHANCE (dulled)」表示と
        # 同じ考え方)。
        draw_text(bg, "COMBO SILENCED (Attacks won't build Combo)", 60, status_y, fnt, (90, 150, 175))
        status_y += 24
    elif combo_count >= 2:
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
    apply_second_wind_if_needed()
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
    if key[K_u]:
        btl_cmd = 6
        ent = True
    if key[K_c]:
        btl_cmd = 7
        ent = True
    if key[K_UP] and btl_cmd > 0:
        btl_cmd -= 1
    if key[K_DOWN] and btl_cmd < len(COMMAND) - 1:
        btl_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    ultimate_req = effective_ultimate_combo_requirement()
    ultimate_ready = combo_count >= ultimate_req
    # Counter追加でコマンドが7→8個に増えた際、従来の行間(60px)のままだと
    # 8行目(y=200+7*60=620)が左下のステータスパネル(imgParaSets、y=600〜)と
    # 重なってしまう。行間を45pxに詰めて8行目をy=515に収め、パネルと
    # 重ならないようにした(「UIで文字が重なるのを避けて」という要望への対応)。
    row_h = 45
    for i in range(len(COMMAND)):
        c = WHITE
        if i == 6:
            # Ultimateは他コマンドと違い使用条件(コンボ数)があるため、準備が
            # 整うまでは暗い色で「まだ使えない」ことを見た目でも伝え、整った
            # 瞬間に金色の明滅へ切り替えて「音でも気づける」考え方と同じく
            # 視覚だけでも一目で気づけるようにする。
            c = BLINK[tmr%6] if ultimate_ready else (110, 90, 60)
        elif btl_cmd == i:
            c = BLINK[tmr%6]
        draw_text(bg, COMMAND[i], 20, 200+i*row_h, fnt, c)
        if i == 3 and btl_cmd == 3:
            draw_text(bg, f"(~{flee_chance_pct()}% success)", 170, 200+i*row_h, fnt, (200, 190, 120))
        if i == 6:
            # 以前はUltimateの文字の右側(x=190)に並べていたが、右側には敵のHPバー/
            # 名前ラベルがあり、コンボ数の桁が増えると文字列が伸びて重なってしまって
            # いたため、Ultimateの文字の真下に置いて重ならないようにする。
            if ultimate_ready:
                draw_text(bg, "READY!", 20, 200+i*row_h+20, fnt, (255, 215, 60))
            else:
                draw_text(bg, f"({combo_count}/{ultimate_req} combo)", 20, 200+i*row_h+20, fnt, (150, 140, 120))
        if i == 7 and btl_cmd == 7:
            # Runの成功率ヒントと同じ考え方で、Counterを選んだ時だけ効果の
            # 目安を右側に添える(常時表示だと他の行と同様に窮屈になるため)。
            draw_text(bg, "(guard + retaliate)", 170, 200+i*row_h, fnt, (150, 190, 230))
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
        "pet_hatched_floor": pet_hatched_floor,
        "pet_bond_achieved_this_run": pet_bond_achieved_this_run,
        "floor_modifier": floor_modifier,
        "color_patches": color_patches,
        "wall_tint": wall_tint,
        "wall_variant": wall_variant,
        "floor_variant": floor_variant,
        "prev_patch_colors": _prev_patch_colors,
        "selected_character": selected_character,
        "in_endless_mode": in_endless_mode,
        "endless_blessing_floor": endless_blessing_floor
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
    global pet_type, pet_hatched_floor, pet_bond_achieved_this_run
    global floor_modifier
    global color_patches
    global wall_tint
    global wall_variant, floor_variant
    global _prev_patch_colors
    global selected_character
    global _exploration_total, _exploration_seen, _reveal_radius_last, _minimap_cache_surface
    global run_kills, run_damage_dealt
    global in_endless_mode
    global endless_blessing_floor
    global second_wind_used_this_floor
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
        # 旧セーブデータ(pet_hatched_floorなし)はfloorをそのまま入れておくことで
        # floor - pet_hatched_floor == 0となり、絆が未形成の状態として扱われる
        # (いきなり絆済み扱いになって効果が変わってしまう事故を防ぐ)。
        pet_hatched_floor = data.get("pet_hatched_floor", floor)
        pet_bond_achieved_this_run = data.get("pet_bond_achieved_this_run", False)
        apply_pet_bonuses()
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
        in_endless_mode = data.get("in_endless_mode", False)
        endless_blessing_floor = data.get("endless_blessing_floor", 0)
        second_wind_used_this_floor = False
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
        # ロード/コンティニューはこのセーブデータでの続きを新しい「1回のプレイ」と
        # 扱い、ゲームオーバー画面のリキャップ表示(このプレイでの撃破数・与ダメージ)
        # を0から数え直す。
        run_kills = 0
        run_damage_dealt = 0
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
    global pl_exp_mult, pl_charge, pl_poison, pl_bleed, pl_frozen
    global pl_def_base, pl_def_buff, def_pill
    global emy_life, emy_step, emy_blink, dmg_eff, typ, emy_lv
    global emy_poison, emy_poisoned_this_battle
    global emy_stun, emy_stunned_this_battle
    global emy_str
    global boss_phase2
    global moving, move_dx, move_dy, move_progress, MOVE_SPEED, base_move_speed
    global hold_dir, hold_timer, hold_delay, hold_interval
    global queued_dir
    global ambush_battles_remaining
    global mimic_battle_active
    global ally_buff_active
    global in_rift_battle
    global in_trial_post_battle
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
    global in_true_hidden_stage
    global in_arena_mode, arena_round
    global in_boss_rush_mode, boss_rush_index
    global combo_count
    global combo_record_shown_this_battle
    global crit_flash_timer, crit_flash_color, last_atk_special
    global screen_shake_timer, screen_shake_mag
    global pet_type, pet_def_bonus, pet_item_bonus, pet_str_bonus
    global pet_hatched_floor, pet_slime_assist_chance, pet_dmg_reduction_mult
    global pet_bond_achieved_this_run
    global abyssal_warden_healed_this_battle
    global daily_mode
    global daily_start_requested
    global hero_start_requested
    global achievements_scroll
    global stats_scroll
    global selected_character
    global pending_bonus_room
    global pending_branch_route, branch_route_floor_skip_pending
    global playtime_ms_accum, steps_taken_accum
    global skill_points, skill_levels, skill_food_mult, skill_poison_mult, skill_exp_mult, skill_item_bonus
    global skill_cursor_col, skill_cursor_row, skill_cursor_capstone
    global bounty_active
    global totem_buff_active, totem_str_bonus, totem_def_bonus
    global bestiary_detail_kind, bestiary_detail_index, bestiary_detail_img, bestiary_detail_seen
    global bgm_volume, se_volume, settings_cursor, muted, screen_shake_enabled, screen_flash_enabled, low_hp_pulse_enabled
    global rare_treasure_sound_pending
    global hidden_wall_sound_pending
    global branch_route_sound_pending
    global low_hp_warning_sound_pending
    global achievement_sound_pending
    global relic_sound_pending
    global charm_sound_pending
    global _autosave_floor_cache
    global pre_quit_confirm_idx
    global run_kills, run_damage_dealt
    global in_endless_mode
    global endless_blessing_floor
    dmg = 0
    lif_p = 0
    str_p = 0
    def_inc = 0
    exp_gain = 0
    
    pygame.init()
    pygame.display.set_caption("Dungeon")
    screen = pygame.display.set_mode((880, 720))
    _convert_loaded_images()
    _build_recolored_hero_assets()
    _build_recolored_pet_assets()
    _build_branch_route_assets()
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
                # タイトル画面のESCはそのまま終了。ダンジョン探索中/バトルの
                # コマンド選択中/拠点/さまよう精霊の選択中など、入力待ちで
                # 演出の途中ではない画面からは、誤操作で直前のオートセーブ以降の
                # 進行を失わないよう確認画面(idx=55)を挟んでから終了する。
                # 【バグ修正】以前はEscを押した瞬間にidxを55へ切り替えた直後、
                # 同じイベントを続けて「if idx == 55:」ブロックが読んでしまい、
                # (Escはキャンセルのキーでもあるため)開いた直後に自分自身を
                # 即座にキャンセルしてしまい、確認画面が事実上一切開けなかった。
                # 呼び出し元のidx値を1回のイベントにつき1つの分岐でしか
                # 扱わないよう、elifで排他的にする。
                if event.key == K_ESCAPE and idx == 0:
                    flush_playtime()
                    pygame.quit()
                    sys.exit()
                elif idx == 55:
                    if event.key == K_y:
                        flush_playtime()
                        pygame.quit()
                        sys.exit()
                    elif event.key in (K_n, K_ESCAPE):
                        idx = pre_quit_confirm_idx
                        tmr = 0
                elif event.key == K_ESCAPE and idx in QUIT_CONFIRM_TRIGGER_IDX:
                    pre_quit_confirm_idx = idx
                    idx = 55
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
                # ダンジョン探索中にPキーでペット情報画面を開く(ペット未所持なら無視)
                if event.key == K_p and idx == 1 and pet_type is not None:
                    idx = 58
                    tmr = 0
                elif idx == 58 and event.key in (K_p, K_ESCAPE):
                    idx = 1
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
                # スキル画面内でのカーソル移動・購入操作(6枝x3段+奥義1つ、
                # 19スキルにもなるため数字キーではなく矢印キーのカーソル選択にする)
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
                    # rev186で10人目(Cleric)が増え1-9のみでは選びきれなくなったため、
                    # [0]キーを10人目(CHARACTER_ORDER[9])に割り当てた
                    # (idx==70の護符装備解除でもK_0を使うが、そちらは別画面(idx)のため衝突しない)。
                    char_key_map = {K_1: 0, K_2: 1, K_3: 2, K_4: 3, K_5: 4, K_6: 5, K_7: 6, K_8: 7, K_9: 8, K_0: 9}
                    if event.key in char_key_map and char_key_map[event.key] < len(CHARACTER_ORDER):
                        selected_character = CHARACTER_ORDER[char_key_map[event.key]]
                    elif event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                        # rev190で11人目(Pyromancer)が増え、数字キー([1-9][0]の10個)
                        # だけでは選びきれなくなったため、矢印キーでグリッドの
                        # カーソルを動かせるようにした(2列×HERO_GRID_ROWS行の
                        # グリッド構造をそのまま流用し、範囲外には移動しない)。
                        cur_i = CHARACTER_ORDER.index(selected_character) if selected_character in CHARACTER_ORDER else 0
                        col_i, row_i = divmod(cur_i, HERO_GRID_ROWS)
                        if event.key == K_DOWN:
                            row_i = min(row_i + 1, HERO_GRID_ROWS - 1)
                        elif event.key == K_UP:
                            row_i = max(row_i - 1, 0)
                        elif event.key == K_RIGHT:
                            col_i += 1
                        elif event.key == K_LEFT:
                            col_i -= 1
                        new_i = col_i * HERO_GRID_ROWS + row_i
                        if 0 <= new_i < len(CHARACTER_ORDER):
                            selected_character = CHARACTER_ORDER[new_i]
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
                # 記録メニュー内でPキーにより秘宝(Relic)一覧を開く
                if event.key == K_p and idx == 45:
                    idx = 69
                    tmr = 0
                if event.key == K_ESCAPE and idx == 69:
                    idx = 45
                    tmr = 0
                # 記録メニュー内でCキーにより護符(Charm)一覧・装備画面を開く
                if event.key == K_c and idx == 45:
                    idx = 70
                    tmr = 0
                if event.key == K_ESCAPE and idx == 70:
                    idx = 45
                    tmr = 0
                if idx == 70 and event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_0):
                    # Charm of the Wanderer(rev206、5種目)導入時から[1-4]キーの
                    # 表しか対応しておらず、5種目以降はマウスのEquipボタンでしか
                    # 装備できなかった穴が残っていた。Charm of Frost Ward(6種目)
                    # 追加に合わせて、キー操作でも6種すべてに対応させた。
                    charm_key_map = {K_1: 0, K_2: 1, K_3: 2, K_4: 3, K_5: 4, K_6: 5}
                    found = load_charms()["found"]
                    if event.key == K_0:
                        equip_charm(None)
                    else:
                        ci = charm_key_map[event.key]
                        if ci < len(CHARM_DEFS) and found.get(CHARM_DEFS[ci]["key"], False):
                            equip_charm(CHARM_DEFS[ci]["key"])
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
                # タイトル画面でVキーにより真の隠しボス(??? The Voidcrowned)へ
                # 挑戦する(??? The Unboundを通算3回倒している場合のみ)
                if event.key == K_v and idx == 0 and load_achievements().get("game_clear", False) \
                        and load_stats().get("hidden_boss_defeats", 0) >= TRUE_HIDDEN_UNLOCK_DEFEATS:
                    start_true_hidden_stage_challenge()
                # タイトル画面でYキーによりデイリーチャレンジ(今日の固定シード)を開始する
                if event.key == K_y and idx == 0:
                    daily_start_requested = True
                # タイトル画面でAキーにより闘技場(Arena of Trials)へ挑戦する
                # (Hidden Stage/True Depthsと違い、全クリア等の条件は無くいつでも挑戦できる)
                if event.key == K_a and idx == 0:
                    start_arena_challenge()
                # タイトル画面でUキーによりボスラッシュ(全9体のステージボスの連戦)へ挑戦する
                if event.key == K_u and idx == 0:
                    start_boss_rush()
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
                        settings_cursor = (settings_cursor + delta_row) % 6
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
                    elif event.key in (K_LEFT, K_RIGHT, K_RETURN, K_SPACE) and settings_cursor == 5:
                        low_hp_pulse_enabled = not low_hp_pulse_enabled
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
                        if random.randint(0, 99) < modifier_gamble_win_chance():
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
                    if load_stats().get("merchant_trades", 0) >= 50:
                        unlock_achievement("master_trader")
                # 旅の吟遊詩人(idx==68)での仲間交換
                if idx == 68:
                    if event.key == K_y and pet_type is not None:
                        old_name = PET_TYPES[pet_type]["name"]
                        new_type = random.choice([k for k in PET_TYPES if k != pet_type])
                        pet_type = new_type
                        pet_hatched_floor = floor
                        pet_bond_achieved_this_run = False
                        apply_pet_bonuses()
                        info_message = f"{old_name} is gone... {PET_TYPES[new_type]['name']} joins you!"
                        info_timer = 50
                        idx = 1
                        tmr = 0
                    elif event.key in (K_n, K_ESCAPE):
                        idx = 1
                        tmr = 0
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
                        if difficulty == "Abyss":
                            # Abyssはパーマデスが売りの難易度なので、セーブスロットへの
                            # 手動保存で死に戻りを回避できてしまうと骨抜きになる。
                            # オートセーブ(死亡時に消去される)だけが頼りにする。
                            info_message = "Abyss forbids manual saves."
                            info_timer = 45
                        else:
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
                elif action == "arena":
                    start_arena_challenge()
                elif action == "boss_rush":
                    start_boss_rush()
                elif action == "hidden" and load_achievements().get("game_clear", False):
                    start_hidden_stage_challenge()
                elif action == "true_hidden" and load_achievements().get("game_clear", False) \
                        and load_stats().get("hidden_boss_defeats", 0) >= TRUE_HIDDEN_UNLOCK_DEFEATS:
                    start_true_hidden_stage_challenge()
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
                elif action == "open_relics":
                    idx = 69
                    tmr = 0
                elif action == "open_charms":
                    idx = 70
                    tmr = 0
                elif action and action.startswith("equip_charm_"):
                    ckey = action[len("equip_charm_"):]
                    found = load_charms()["found"]
                    if ckey == "none" or found.get(ckey, False):
                        equip_charm(None if ckey == "none" else ckey)
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
                elif action == "low_hp_pulse_toggle":
                    low_hp_pulse_enabled = not low_hp_pulse_enabled
                    save_settings()

        tmr = tmr +1
        if info_timer > 0:
            info_timer -= 1
            
        if idx == 1 and moving:
            move_progress += MOVE_SPEED * modifier_speed_mult() * modifier_rocky_speed_mult() * (1.0 + skill_move_speed_bonus) * relic_speed_mult() * charm_speed_mult()
            
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
                        pl_life = min(pl_lifemax, pl_life + int(dp["heal_per_step"] * modifier_heal_mult() * relic_heal_mult() * char_params().get("heal_mult", 1.0)))
                    if food == 0:
                        # 食料はこれまで数値表示のみで、尽きて初めて歩数ごとの
                        # スタベーションダメージ(下記else節)で気づく形だった。
                        # 低HP警告(low_hp_warning_sound_pending)と同じ「閾値を
                        # またいだ瞬間だけ気づかせる」考え方で、food>0からちょうど
                        # 0になったこの一歩でだけ警告メッセージと効果音を出す
                        # (次の一歩からはfood>0の分岐自体に入らなくなるため、
                        # food>0に戻るまで再度鳴ることはない)。新設のHungry Rat
                        # (typ35)が食料をかじり取ってくる場面でも同様に働く。
                        info_message = "Out of food! You'll lose HP each step until you restock."
                        info_timer = 70
                        se[0].play()
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
                    pdmg = max(1, int(pl_lifemax // 20 * skill_poison_mult * relic_poison_resist_mult()))
                    pl_life -= pdmg
                    # Festering/Cleansing Floorは毒の減り方そのものを速めたり遅めたりするが、
                    # 減少倍率をそのまま掛けるとFestering Floor(0.5倍)の低難易度
                    # (poison_decay_per_step=1)で減少量が0になり、毒が永久に抜けなくなる
                    # 事故が起きうるため、必ず最低1は減るようクランプする。
                    poison_decay = max(1, int(round(diff_params()["poison_decay_per_step"] * modifier_poison_decay_mult())))
                    pl_poison = max(0, pl_poison - poison_decay)
                    info_message = f"Poison {pdmg}dmg!"
                    info_timer = 30
                    if pl_life <= 0:
                        pl_life = 0
                        pygame.mixer.music.stop()
                        idx = 9
                        tmr = 0

                if pl_bleed > 0 and idx == 1:
                    # 出血(pl_bleed)は毒と違い、スキル(skill_poison_mult)にも
                    # フロア特性(modifier_poison_decay_mult())にも一切影響を
                    # 受けない固定ダメージ・固定減衰(BLOODTHORN_REVENANT_TINT
                    # 定義のコメント参照)。
                    bdmg = max(1, int(pl_lifemax // BLOODTHORN_BLEED_DIVISOR))
                    pl_life -= bdmg
                    pl_bleed = max(0, pl_bleed - 1)
                    info_message = f"Bleed {bdmg}dmg!"
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
            # 通算プレイ時間はこれまで記録画面(統計)を開かないと確認できなかった
            # ため、まだ絵柄と被らない左上の余白を使ってタイトル画面にも常時
            # 表示するようにした(現在のセッション分はディスクにまだ書き込まれて
            # いないため、playtime_ms_accumを合算してリアルタイムに近い値を出す)。
            _total_playtime_ms = load_stats().get("total_playtime_ms", 0) + playtime_ms_accum
            draw_text(screen, f"Total play time: {format_playtime(_total_playtime_ms)}", 16, 16, fontXS, (170, 170, 190))
            if info_timer > 0:
                # 難易度アンロックのヒント(toggle_difficulty参照)をここに表示する。
                # 他の画面のように毎フレーム描画され続けるが、info_timerが切れれば
                # 自然に消えるので、常設のUI要素を1つ増やすほどの重さは無い。
                draw_text(screen, info_message, 16, 40, fontXS, (255, 215, 90))
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
            # [T] 難易度(直接切り替え、サブメニューなし)。ボタンの色を難易度に
            # 応じて変え(緑→橙→赤橙→深紅)、数値を読まなくても危険度が一目で
            # 伝わるようにした。
            label = f"[T] Difficulty: {difficulty}"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "difficulty",
                        base_color=DIFFICULTY_COLORS.get(difficulty, (225, 150, 40)), mouse_pos=mouse_pos)
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
            y += 26
            # [A] 闘技場(Arena of Trials)。全クリア等の条件は無く、いつでも
            # 挑戦できる連戦サバイバル。Hidden Stage/True Depths行が下に続いても
            # 画面下端(720px)からはみ出さないよう、この行だけ間隔を26pxに詰めた。
            arena_best = load_stats().get("arena_best_round", 0)
            arena_label = f"[A] Arena of Trials (Best: Round {arena_best})" if arena_best > 0 else "[A] Arena of Trials"
            arena_btn_w = fontS.size(arena_label)[0] + 30
            draw_button(screen, fontS, MENU_X, y, arena_btn_w, 26, arena_label, "arena",
                        base_color=(210, 110, 40), mouse_pos=mouse_pos)
            # 【新要素】[U] ボスラッシュ。Hidden Stage/True Depthsと同じく、新しい
            # 行を増やさず闘技場ボタンの右隣に並べて画面下端(720px)への圧迫を避けた。
            boss_rush_best = load_stats().get("boss_rush_best_streak", 0)
            boss_rush_label = (f"[U] Boss Rush (Best {boss_rush_best}/{len(BOSS_RUSH_FLOORS)})"
                                if boss_rush_best > 0 else "[U] Boss Rush")
            draw_button(screen, fontS, MENU_X + arena_btn_w + 8, y, fontS.size(boss_rush_label)[0] + 30, 26,
                        boss_rush_label, "boss_rush", base_color=(170, 40, 40), mouse_pos=mouse_pos)
            # [H] 隠しステージ(全クリア後のみ、直接開始)
            if load_achievements().get("game_clear", False):
                y += 26
                label = "[H] Hidden Stage"
                hidden_btn_w = fontS.size(label)[0] + 30
                draw_button(screen, fontS, MENU_X, y, hidden_btn_w, 26, label, "hidden",
                            base_color=(190, 50, 170), mouse_pos=mouse_pos)
                # 【新要素】真の隠しボス「??? The Voidcrowned」への入り口。
                # ??? The Unboundを通算3回倒して初めて挑戦できる、隠しステージの
                # さらに奥にいる一体で、隠しボスを倒して終わりだった真エンディング後の
                # 次の目標になる。縦方向の余白がほとんど無いパネルのため、新しい行を
                # 増やさずHidden Stageボタンの右隣に並べて表示する。
                _true_hb_defeats = load_stats().get("hidden_boss_defeats", 0)
                _true_hb_unlocked = _true_hb_defeats >= TRUE_HIDDEN_UNLOCK_DEFEATS
                true_label = "[V] True Depths" if _true_hb_unlocked \
                    else f"[V] True Depths ({_true_hb_defeats}/{TRUE_HIDDEN_UNLOCK_DEFEATS})"
                draw_button(screen, fontS, MENU_X + hidden_btn_w + 12, y, fontS.size(true_label)[0] + 30, 26,
                            true_label, "true_hidden", base_color=(110, 30, 150),
                            mouse_pos=mouse_pos, enabled=_true_hb_unlocked)
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
                in_endless_mode = False
                endless_blessing_floor = 0
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
                in_trial_post_battle = False
                bounty_active = False
                totem_buff_active = False
                in_boss_battle = False
                battle_took_damage = False
                in_hidden_stage = False
                in_arena_mode = False
                pl_poison = 0
                pl_bleed = 0
                pl_frozen = 0
                emy_poison = 0
                emy_poisoned_this_battle = False
                emy_stun = 0
                emy_stunned_this_battle = False
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
                run_kills = 0
                run_damage_dealt = 0
                pet_type = None
                pet_def_bonus = 0
                pet_item_bonus = 0
                pet_str_bonus = 0
                pet_hatched_floor = 0
                pet_slime_assist_chance = 0
                pet_dmg_reduction_mult = 1.0
                pet_bond_achieved_this_run = False
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
            panel = pygame.Surface((880, 480))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 240])
            MENU_X = 230
            draw_text(screen, "Settings", MENU_X, 270, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [MENU_X, 315, 480, 2])
            BAR_X = MENU_X + 190
            BAR_W = 200
            rows = [
                ("BGM Volume", bgm_volume, 0, "bgm_vol_down", "bgm_vol_up"),
                ("SE Volume", se_volume, 1, "se_vol_down", "se_vol_up"),
            ]
            y = 345
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
            pulse_selected = settings_cursor == 5
            pucol = (255, 215, 0) if pulse_selected else WHITE
            pucursor = "> " if pulse_selected else "  "
            draw_text(screen, pucursor + "Low HP Pulse", MENU_X, y, fontS, pucol)
            pulse_status_text = "ON" if low_hp_pulse_enabled else "OFF"
            pulse_status_col = (150, 255, 150) if low_hp_pulse_enabled else (255, 120, 120)
            draw_text(screen, pulse_status_text, BAR_X + 78, y + 2, fontS, pulse_status_col)
            pulse_toggle_label = "Toggle"
            draw_button(screen, fontS, BAR_X - 46, y - 2, fontS.size(pulse_toggle_label)[0] + 24, 30, pulse_toggle_label,
                        "low_hp_pulse_toggle", base_color=(90, 90, 90), mouse_pos=mouse_pos, align="center")
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
                    "[T] Difficulty   [N] Hero select (0-9)   [G] Game data",
                    "[R] Records (achievements/stats/bestiary/echo/relics/charms/ranking)",
                    "[Y] Daily challenge   [A] Arena of Trials (playable anytime)",
                    "[H] Hidden stage (after full clear)   [V] True Depths (after 3 clears)",
                    "[F1] This help screen   [Esc] Quit game",
                ]),
                ("Dungeon Exploration", (200, 255, 200), [
                    "Arrow Keys : Move   [Q] Save menu   [K] Skill tree",
                    "[I] Use potion   [P] Pet info (if you have a pet)",
                    "[Esc] Quit confirmation",
                ]),
                ("Battle", (255, 200, 160), [
                    "[A] Attack   [P] Potion   [B] Blaze gem",
                    "[R] Run   [D] Defense   [F] Focus",
                    "[U] Ultimate (needs a 5-hit combo)",
                    "[C] Counter (guard the hit, then strike back)",
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
            # rev185で護符(Charm)一覧ボタンを追加した際、下端のEscボタンが
            # 画面下端やパネル外へはみ出さないよう、パネル・見出し・区切り線・
            # 先頭ボタンをまとめて45px上へずらした(ボタン間隔・Escとの
            # 隙間はそれまでと同じ間隔のまま、全体を1行分押し上げる形)。
            panel = pygame.Surface((880, 450))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 255])
            MENU_X = 230      # ボタン幅420を画面中央に揃えた値
            draw_text(screen, "Records", MENU_X, 275, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [MENU_X, 320, 480, 2])
            BTN_W = 420
            y = 338
            label = "[V] Achievements"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_achievements",
                        base_color=(90, 100, 210), mouse_pos=mouse_pos)
            y += 45
            label = "[X] Stats"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_stats",
                        base_color=(40, 155, 150), mouse_pos=mouse_pos)
            y += 45
            bdata_summary = load_bestiary()
            bestiary_found = (sum(bdata_summary["enemies"]) + sum(bdata_summary["bosses"])
                               + sum(bdata_summary["items"]))
            bestiary_total = len(EMY_NAME) + len(BOSS_BESTIARY) + len(TRE_NAME)
            label = f"[B] Bestiary ({bestiary_found}/{bestiary_total})"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_bestiary",
                        base_color=(215, 130, 40), mouse_pos=mouse_pos)
            y += 45
            echo_data_summary = load_achievements()
            echo_defeated_count = len(set(echo_data_summary.get("echo_floors_defeated", []))
                                       & set(ECHO_ELIGIBLE_FLOORS))
            label = f"[E] Echo Battles ({echo_defeated_count}/{len(ECHO_ELIGIBLE_FLOORS)})"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_echo",
                        base_color=(50, 140, 210), mouse_pos=mouse_pos)
            y += 45
            label = "[D] Daily Ranking"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_daily_ranking",
                        base_color=(60, 175, 95), mouse_pos=mouse_pos)
            y += 45
            relics_data_summary = load_relics()
            relics_found = sum(1 for r in RELIC_DEFS if relics_data_summary.get(r["key"], False))
            label = f"[P] Relics ({relics_found}/{len(RELIC_DEFS)})"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_relics",
                        base_color=(40, 170, 160), mouse_pos=mouse_pos)
            y += 45
            charms_data_summary = load_charms()["found"]
            charms_found = sum(1 for c in CHARM_DEFS if charms_data_summary.get(c["key"], False))
            label = f"[C] Charms ({charms_found}/{len(CHARM_DEFS)})"
            draw_button(screen, font, MENU_X, y, BTN_W, 34, label, "open_charms",
                        base_color=(150, 90, 200), mouse_pos=mouse_pos)
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
            COL_ENEMY_X = 30
            COL_ENEMY_X2 = 240
            COL_BOSS_X = 450
            COL_ITEM_X = 650
            # モンスターの種類数が増え1列(旧レイアウト)には収まらなくなったため、
            # 前半/後半で2列に分けて表示する(図鑑パネルの縦幅に収める)。
            ENEMY_COL_SPLIT = (len(EMY_NAME) + 1) // 2
            draw_text(screen, "Monsters", COL_ENEMY_X, 150, fontS, (200, 200, 255))
            for i, name in enumerate(EMY_NAME):
                seen = bdata["enemies"][i]
                label = name if seen else "???"
                bcol = (100, 90, 190) if seen else (70, 70, 78)
                if i < ENEMY_COL_SPLIT:
                    cx, row = COL_ENEMY_X, i
                else:
                    cx, row = COL_ENEMY_X2, i - ENEMY_COL_SPLIT
                y = 178 + row*ROW_H
                draw_button(screen, fontS, cx, y, max(fontS.size(label)[0]+16, 76), ROW_H-2,
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
            # 【UI改善】これまでMonsters/Bosses/Itemsの内訳しか見えず、実績
            # 「Bestiary Master」(全種発見)まであとどれくらいかが一目で
            # 分からなかった。新しい行を増やすと下の[Esc] Backボタンと文字が
            # 重なるため、既存の内訳と同じ行の末尾に3カテゴリ合算の発見率(%)を
            # 追記するだけにとどめた。
            _total_found = ecount + bcount + icount
            _total_all = len(EMY_NAME) + len(BOSS_BESTIARY) + len(TRE_NAME)
            _pct = int(_total_found * 100 / _total_all) if _total_all else 0
            draw_text(screen, f"Monsters: {ecount}/{len(EMY_NAME)}   Bosses: {bcount}/{len(BOSS_BESTIARY)}   Items: {icount}/{len(TRE_NAME)}   Overall: {_pct}%", 150, 610, fontS, (150, 220, 255))
            label = "[Esc] Back"
            draw_button(screen, fontS, 340, 640, fontS.size(label)[0] + 30, 28, label, "back_to_records",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 69:
            # 秘宝(Relic)一覧。図鑑(idx==46)と同じ「未所持は???」の一覧表示に、
            # 所持しているものだけ効果(desc)も添えて表示する。
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 560))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 90])
            draw_text(screen, "Relics", 340, 105, font, (255, 215, 0))
            rdata = load_relics()
            # rev182で秘宝が6種から8種(Swift Sandals/Windwalker Charmを追加)に
            # 増えたため、行間を60pxから48pxに詰めて「Relics found」の集計行が
            # 下の[Esc] Backボタン(y=640)と重ならないようにした。
            # rev198でSerpent's Fangが加わり9種→10種になったため、同じ理由で
            # 48pxから44pxにさらに詰めた(詰めないと集計行がEsc行と重なる)。
            # rev199でWarden's Bulwarkが加わり10種→11種になったため、同じ理由で
            # 44pxから40pxにさらに詰めた。
            # rev200でVital Charmが加わり11種→12種になり、40pxのままだと
            # 「Relics found」の集計行がy=640でEsc行とちょうど重なって
            # しまうため、同じ理由で40pxから36pxにさらに詰めた。
            # rev202でThunderclap Idolが加わり12種→13種になり、36pxのままだと
            # 「Relics found」の集計行(y=618)が[Esc] Back行(y=640)にかなり
            # 接近して文字が重なって見えてしまうため、同じ理由で36pxから
            # 32pxにさらに詰めた。
            # rev204でCinder Idolが加わり14種→15種になり、32pxのままだと
            # 「Relics found」の集計行がy=640の[Esc] Back行とちょうど重なって
            # しまうため、同じ理由で32pxから30pxにさらに詰めた。
            ROW_H2 = 30
            for i, relic in enumerate(RELIC_DEFS):
                owned = rdata.get(relic["key"], False)
                y = 150 + i*ROW_H2
                name_label = relic["name"] if owned else "???"
                name_col = (150, 235, 220) if owned else (110, 110, 110)
                draw_text(screen, name_label, 60, y, fontS, name_col)
                if owned:
                    draw_text(screen, relic["desc"], 60, y + 26, fontXS, (200, 220, 210))
                else:
                    draw_text(screen, "Defeat a boss for a chance to find this relic", 60, y + 26, fontXS, (90, 90, 90))
            rcount = sum(1 for r in RELIC_DEFS if rdata.get(r["key"], False))
            draw_text(screen, f"Relics found: {rcount}/{len(RELIC_DEFS)}", 60, 150 + len(RELIC_DEFS)*ROW_H2 + 10, fontS, (150, 220, 255))
            label = "[Esc] Back"
            draw_button(screen, fontS, 340, 640, fontS.size(label)[0] + 30, 28, label, "back_to_records",
                        base_color=(110, 110, 120), mouse_pos=mouse_pos)

        elif idx == 70:
            # 護符(Charm)一覧・装備画面。秘宝(idx==69)と同じ「未所持は???」の
            # 一覧表示に加えて、護符は1つだけ選んで装備する必要があるため、
            # 各行に装備切り替えボタン(数字キー1〜4でも操作可)を添える。
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 560))
            panel.set_alpha(175)
            panel.fill(BLACK)
            screen.blit(panel, [0, 90])
            draw_text(screen, "Charms", 320, 105, font, (255, 215, 0))
            cdata = load_charms()
            cfound = cdata["found"]
            equipped_key = cdata["equipped"]
            # Charm of Frost Ward追加でCHARM_DEFSが5種→6種になり、従来の
            # ROW_H3=85のままだと一覧の最終行+下部の合計数表示が、下部固定
            # 位置の[Esc] Backボタン(y=640)と重なってしまう。行間を詰めて
            # 6種でも重ならないようにした(5種以下なら従来と同じ85のまま)。
            ROW_H3 = 85 if len(CHARM_DEFS) <= 5 else 73
            for i, charm in enumerate(CHARM_DEFS):
                owned = cfound.get(charm["key"], False)
                y = 145 + i * ROW_H3
                is_equipped = owned and equipped_key == charm["key"]
                name_label = f"[{i+1}] " + (charm["name"] if owned else "???")
                if is_equipped:
                    name_col = (255, 215, 0)
                elif owned:
                    name_col = (215, 180, 245)
                else:
                    name_col = (110, 110, 110)
                draw_text(screen, name_label, 60, y, fontS, name_col)
                if is_equipped:
                    draw_text(screen, "(equipped)", 60, y + 24, fontXS, (255, 215, 0))
                if owned:
                    draw_text(screen, charm["desc"], 60, y + 46, fontXS, (210, 200, 220))
                    btn_label = "Equipped" if is_equipped else "Equip"
                    draw_button(screen, fontXS, 660, y, 130, 30, btn_label, f"equip_charm_{charm['key']}",
                                base_color=(90, 60, 130) if not is_equipped else (150, 120, 30), mouse_pos=mouse_pos)
                else:
                    draw_text(screen, "Find a Charm Shrine in the dungeon to receive one", 60, y + 24, fontXS, (90, 90, 90))
            ccount = sum(1 for c in CHARM_DEFS if cfound.get(c["key"], False))
            bottom_y = 145 + len(CHARM_DEFS) * ROW_H3 + 4
            draw_text(screen, f"Charms found: {ccount}/{len(CHARM_DEFS)}", 60, bottom_y, fontS, (150, 220, 255))
            draw_button(screen, fontXS, 660, bottom_y - 2, 130, 30, "Unequip", "equip_charm_none",
                        base_color=(90, 90, 90), mouse_pos=mouse_pos)
            draw_text(screen, "[1-6] Equip  [0] Unequip  [Esc] Back", 60, bottom_y + 30, fontXS, CYAN)
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
            if bestiary_detail_kind != "boss" and bestiary_detail_seen:
                ability_hint = BESTIARY_ABILITY_HINTS.get(bestiary_detail_index)
                if ability_hint:
                    draw_text(screen, ability_hint, 340, 178, fontS, (180, 200, 255))
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
            # rev165でRogue追加により5人目が増えたため、行間80px/パネル420pxの
            # ままだと最終行がパネル外・下の[1-4] Chooseラベルと重なってしまう。
            # パネルを480pxに拡大し行間を66pxに詰めて5人が収まるようにした。
            # rev168で6人目のBerserkerが増えたため、パネルをさらに560pxに拡大し
            # 下の[1-6] Chooseラベルの位置も合わせてずらした(行間66pxは維持)。
            # rev171で7人目のProspectorが増えたため、画面の高さ(720px)内に収まる
            # よう行間を66pxから60pxに詰めて7人分を確保した(パネルサイズ560pxは維持)。
            # rev177で8人目のTraderが増えたため、行間を60pxから54pxに、
            # 肖像画の枠(PORTRAIT_BOX)を58pxから50pxに縮めて8人分を確保した
            # (枠を縮めずに行間だけ詰めると、肖像画のある先頭4人分の枠が
            # 上下でわずかに重なってしまうため、両方を詰めて重なりを防いでいる)。
            # rev182で9人目のMonkが増えるまでは、1列に全員を積み上げて行間・
            # 肖像画の枠を毎回少しずつ詰める場当たり的な対応を繰り返してきたが、
            # 9人分でパネル(590px)がほぼ画面の高さ(720px)ぎりぎりまで埋まって
            # おり、この方式のままでは次にヒーローが増えるたびにまた文字が
            # 重なる不具合を作り込みかねなかった。rev186で10人目のClericを
            # 追加するのに合わせ、1列積み上げ方式をやめて2列×5行のグリッドに
            # 描き直した。名前+肖像画だけをグリッドに並べ、詳細な説明文
            # (基礎ステータスの増減・Ultimate名)は今選んでいる1人分だけを
            # グリッドの下にまとめて表示する方式に変えたことで、今後さらに
            # ヒーローが増えても(3列目を足す/行間を詰めるだけで済み)説明文の
            # 横幅を気にして重なりが起きる心配がなくなった。
            # rev190で11人目のPyromancerが増え、既存の[1-9][0]キーだけでは
            # 全員を選びきれなくなった(数字キーは10個しかない)。行間・パネルを
            # 詰めるその場しのぎではまた次にヒーローが増えた時に同じ問題が
            # 再発するため、2列×6行に拡張してグリッド自体に空きを持たせつつ、
            # 矢印キーでカーソルを動かして[Enter]/[Space]で決定する方式を追加した
            # (数字キーによる[1-9][0]の直接選択は10人目までの互換のためそのまま
            # 残している)。これで今後ヒーローが増えても、数字キーの上限に
            # ぶつかることなく行/列を増やすだけで対応できる。
            # rev195で13人目のReaverが増え、2列×6行(12枠)が埋まりきったため、
            # 2列×7行(14枠、うち1枠は将来の増員用の空き)に拡張した。行間を
            # 68pxのままだと最終行の説明文(Ultimate名・操作案内)が画面下端
            # (720px)からはみ出すため、行間を60pxに詰めて全体を上に収めている。
            # rev201で15人目のApothecaryが増え、2列×7行(14枠)が埋まりきったため、
            # 2列×8行に拡張した。行間60pxのままだと最終行の説明文が画面下端から
            # はみ出すため、行間を52pxにさらに詰めている。
            # rev209で17人目のRangerが増え、2列×8行(16枠)が埋まりきったため、
            # 2列×9行に拡張した。行間52pxのままだと最終行の説明文が画面下端から
            # はみ出すため、行間を48pxにさらに詰めている。
            title_menu_rects.clear()
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 590))
            panel.set_alpha(180)
            panel.fill(BLACK)
            screen.blit(panel, [0, 130])
            draw_text(screen, "Choose your Hero", 300, 145, font, (255, 215, 0))
            pygame.draw.rect(screen, (90, 90, 90), [80, 185, 720, 2])
            PORTRAIT_BOX = 46
            GRID_COLS = [90, 490]     # 各列の肖像画x座標
            GRID_TEXT_DX = 80         # 肖像画から名前テキストまでのx方向オフセット
            GRID_ROW_GAP = 48
            GRID_ROWS = HERO_GRID_ROWS
            GRID_Y0 = 205
            cur_sel = None
            for i, cid in enumerate(CHARACTER_ORDER):
                c = CHARACTER_TYPES[cid]
                col_i, row_i = divmod(i, GRID_ROWS)
                gx = GRID_COLS[col_i] if col_i < len(GRID_COLS) else GRID_COLS[-1]
                y0 = GRID_Y0 + row_i * GRID_ROW_GAP
                is_sel = (cid == selected_character)
                if is_sel:
                    cur_sel = cid
                col = (255, 215, 0) if is_sel else WHITE
                mark = "-> " if is_sel else "   "
                portrait = imgHero.get(cid)
                if portrait is not None:
                    pw, ph = portrait.get_width(), portrait.get_height()
                    scale = min(PORTRAIT_BOX/pw, PORTRAIT_BOX/ph) if pw > 0 and ph > 0 else 1.0
                    disp = pygame.transform.smoothscale(portrait, (max(1, int(pw*scale)), max(1, int(ph*scale))))
                    frame_rect = [gx, y0-6, PORTRAIT_BOX, PORTRAIT_BOX]
                    if is_sel:
                        pygame.draw.rect(screen, (255, 215, 0), [frame_rect[0]-2, frame_rect[1]-2, PORTRAIT_BOX+4, PORTRAIT_BOX+4], 2)
                    screen.blit(disp, [gx + (PORTRAIT_BOX-disp.get_width())//2, y0-6 + (PORTRAIT_BOX-disp.get_height())//2])
                    if is_character_awakened(cid):
                        # ヒーロー覚醒(rev206追加)済みのキャラは、新規スプライトを
                        # 用意せず既存肖像画の右上に金色のバッジを添えるだけで
                        # 「見た目でも分かる」ようにする(Rogue等の色替え流用
                        # スプライトと同じ、追加アセット無しで見た目を変える手法)。
                        badge_cx, badge_cy = frame_rect[0] + PORTRAIT_BOX - 2, frame_rect[1] + 2
                        pygame.draw.circle(screen, (255, 215, 0), [badge_cx, badge_cy], 6)
                        pygame.draw.circle(screen, (120, 80, 0), [badge_cx, badge_cy], 6, 1)
                key_label = i+1 if i < 9 else (0 if i == 9 else None)
                label_prefix = f"[{key_label}] " if key_label is not None else ""
                draw_text(screen, f"{mark}{label_prefix}{c['name']}", gx + GRID_TEXT_DX, y0, fontS, col)
            grid_bottom = GRID_Y0 + GRID_ROWS * GRID_ROW_GAP
            pygame.draw.rect(screen, (90, 90, 90), [80, grid_bottom, 720, 2])
            if cur_sel is not None:
                c = CHARACTER_TYPES[cur_sel]
                # 【UI改善】これまで説明文には基礎ステータスの増減しか書かれておらず、
                # 選ぶ前に各キャラの必殺技(Ultimate)が何かを確認する手段が無かった。
                # 既存の説明文にUltimate名を併記することで、画面を切り替えたり
                # 実際にバトルで使ってみたりしなくても選択の決め手にできるようにした。
                ult_name = ULTIMATE_DEFS.get(cur_sel, {}).get("name", "")
                # 【新要素】ヒーロー覚醒(rev206追加):このキャラで一度でもボスを
                # 倒したことがあれば、以後ずっとこの永続ボーナスが乗ったまま
                # 選べる。まだ覚醒していない場合は説明文を変えず、余計な文字数を
                # 増やして他の行と重ならないようにする。
                awakened_suffix = "  [Awakened +6 STR/+4 DEF/+20 HP]" if is_character_awakened(cur_sel) else ""
                draw_text(screen, f"{c['name']}: {c['desc']}{awakened_suffix}", 90, grid_bottom + 16, fontS, (255, 215, 0))
                draw_text(screen, f"Ultimate: {ult_name}", 90, grid_bottom + 42, fontS, (200, 200, 200))
            draw_text(screen, "Arrows to move, [Enter] Choose   [Esc] Back", 190, grid_bottom + 76, fontS, WHITE)

        elif idx == 1:
            move_player(key)
            draw_dungeon(screen, fontS)
            title_suffix = f"  - {current_title()}" if current_title() else ""
            if in_endless_mode:
                # エンドレス・ディープス中はcurrent_stage()がステージ3で頭打ちになり
                # 「Stage 3 Floor 30/30」のまま止まって見えてしまうため、代わりに
                # 実際のフロア番号(91以降も伸び続ける)をそのまま表示する
                depth_best = max(load_stats().get("deepest_endless_floor", 0), floor)
                draw_text(screen, f"Endless Depths - Floor {floor} (best {depth_best}) ({pl_x} {pl_y}){title_suffix}", 60, 40, fontS, (200, 160, 255))
            else:
                draw_text(screen, f"Stage {current_stage(floor)}  Floor {stage_local_floor(floor)}/{STAGE_LENGTH} ({pl_x} {pl_y}){title_suffix}", 60, 40, fontS, WHITE)
            draw_level_gauge(screen, 60, 62, fontS)
            status_y = 88
            if difficulty == "Nightmare":
                # Nightmare(玄人向け最上位難易度)でプレイ中は、探索中ずっと
                # 脈打つ深紅の警告を出し続ける。歩数ごとの受動回復が無い
                # (heal_per_step=0)という他の難易度との一番大きな違いを、
                # 常に視界の隅で意識させるための表示。
                pulse_col = (200, 20, 30) if tmr % 10 < 5 else (255, 90, 90)
                draw_text(screen, "*** NIGHTMARE MODE ***", 60, status_y, fontS, pulse_col)
                status_y += 26
            if difficulty == "Abyss":
                # Abyss(パーマデスの最上位難易度)は、Nightmareよりさらに重い
                # 紫〜漆黒の警告を出し続け、「死んだらこのオートセーブは消える」
                # という他の難易度には無い一発勝負のプレッシャーを常時思い出させる。
                pulse_col = (130, 20, 200) if tmr % 10 < 5 else (60, 0, 90)
                draw_text(screen, "*** ABYSS MODE (PERMADEATH) ***", 60, status_y, fontS, pulse_col)
                status_y += 26
            if floor_modifier:
                # 入室時の"Welcome to floor"メッセージが消えた後もフロア特性を
                # 忘れないよう、探索中は常時小さく表示し続ける。
                fm = FLOOR_MODIFIERS[floor_modifier]
                draw_text(screen, fm["name"], 60, status_y, fontS, fm["color"])
                status_y += 26
            equipped_charm = get_equipped_charm()
            if equipped_charm:
                draw_text(screen, f"CHARM: {equipped_charm['name']}", 60, status_y, fontS, (215, 180, 245))
                status_y += 26
            # アイテム発見率は難易度・スキル(Lucky Find)・仲間(Lucky Cat)・
            # フロア特性(Bountiful/Scarce/Cursed)・キャラクター(Prospector)の
            # 5つが絡み合って最終的な数値が決まるため、これまでは合計値を
            # 確認する手段が無かった。バトル画面のCRIT CHANCE表示と同じ
            # 「合計値を数値で明確にする」考え方を、探索中のステータス行にも
            # 適用した(0の時は表示しない)。
            item_find_total = diff_params()["item_bonus"] + skill_item_bonus + pet_item_bonus + modifier_item_bonus() + char_params()["item_bonus"] + relic_item_bonus() + charm_item_bonus()
            if item_find_total != 0:
                sign = "+" if item_find_total >= 0 else ""
                item_find_col = (255, 215, 0) if item_find_total > 0 else (200, 90, 90)
                draw_text(screen, f"ITEM FIND {sign}{item_find_total}%pt", 60, status_y, fontS, item_find_col)
                status_y += 26
            # 逃走成功率もITEM FINDと同じくフロア特性(Tranquil/Snared)・
            # キャラクター(Vagabond)・秘宝(Featherlight Cloak)の3箇所が絡み、
            # これまでバトルのRunコマンドを選んで初めて確認できた(合計値を
            # 探索中に事前確認する手段が無かった)。ITEM FIND表示と同じ
            # 「合計値を数値で明確にする」考え方をここにも適用した。
            flee_bonus_total = modifier_flee_bonus() + char_params().get("flee_bonus", 0) + relic_flee_bonus() + charm_flee_bonus()
            if flee_bonus_total != 0:
                fsign = "+" if flee_bonus_total >= 0 else ""
                flee_col = (255, 215, 0) if flee_bonus_total > 0 else (200, 90, 90)
                draw_text(screen, f"FLEE {fsign}{flee_bonus_total}%pt", 60, status_y, fontS, flee_col)
                status_y += 26
            # 【UI改善】敵への毒付与確率(秘宝Serpent's Fang・フロア特性Venomfang・
            # キャラクターApothecaryの3つが絡む)も、ITEM FIND/FLEEと同じく
            # 合計値を確認する手段がバトル中に毒が発生するまで無かったため、
            # 同じ「合計値を数値で明確にする」考え方を適用した(0の時は非表示)。
            poison_chance_total = relic_enemy_poison_chance() + modifier_enemy_poison_chance_bonus() + char_params().get("poison_bonus", 0)
            if poison_chance_total > 0:
                draw_text(screen, f"POISON CHANCE +{poison_chance_total}%pt", 60, status_y, fontS, (150, 210, 90))
                status_y += 26
            # 秘宝Thunderclap Idol・フロア特性Stormbound(rev202追加)・
            # キャラクターMarshal(rev204追加)も、POISON CHANCEと同じ理由で
            # 合計値をダンジョン探索中から確認できるようにした。
            stun_chance_total = relic_enemy_stun_chance() + modifier_enemy_stun_chance_bonus() + char_params().get("stun_bonus", 0)
            if stun_chance_total > 0:
                draw_text(screen, f"STUN CHANCE +{stun_chance_total}%pt", 60, status_y, fontS, (235, 210, 90))
                status_y += 26
            # 【新要素】自分自身が毒状態(pl_poison)から受けるダメージの軽減量
            # (スキルAntidote Body・秘宝Serpent's Wardの2箇所が絡む)も、
            # POISON CHANCE/STUN CHANCEと同じ「合計値を数値で明確にする」考え方を
            # 適用した。軽減が無い(1.0倍のまま)時は表示しない。
            poison_resist_pct = int(round((1.0 - skill_poison_mult * relic_poison_resist_mult()) * 100))
            if poison_resist_pct > 0:
                draw_text(screen, f"POISON RESIST -{poison_resist_pct}%", 60, status_y, fontS, (150, 230, 190))
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
            if pl_bleed > 0:
                draw_text(screen, f"BLEED x{pl_bleed}", 60, status_y, fontS, (200, 30, 30))
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
                # 以前はここに「Pet: 名前 (効果)」を常時1行表示していたが、他の
                # ステータス行と重なって探索中の視界を圧迫するという声があったため、
                # スキル情報(「[K] Skills」)と同じ「短いリマインダー行+ボタンで
                # 詳細画面を開く」方式に変更した。
                draw_text(screen, "[P] Pet Info", 60, status_y, fontS, (150, 220, 255))
                status_y += 26
            if daily_mode:
                draw_text(screen, "[Daily Challenge]", 60, status_y, fontS, (120, 255, 150))
                status_y += 26
            if welcome > 0:
                welcome = welcome - 1
                # 【バグ修正】この「Welcome to floor」バナーは従来y=180/225/250の
                # 固定座標に描いていたが、左側のステータス列(x=60、行ごとに
                # status_y+=26)は有効な特性・実績・バフの数が多いと際限なく
                # 伸び、ちょうどこの固定座標の高さと重なって文字が読めなく
                # なることがあった。ステータス列の描画がここまでにすべて
                # 終わっている(status_yに最終的な高さが入っている)ことを
                # 利用し、バナーの開始位置をstatus_yより必ず下にずらすことで
                # 重なりを防ぐ(ステータス列が短い時は従来通りy=180のまま)。
                banner_y = max(180, min(status_y + 14, 610))
                draw_text(screen, f"Welcome to floor {floor}", 300, banner_y, font, CYAN)
                if floor_modifier:
                    fm = FLOOR_MODIFIERS[floor_modifier]
                    draw_text(screen, f"{fm['name']}: {fm['desc']}", 220, banner_y + 45, fontS, fm["color"])
                if is_boss_floor(floor) and floor not in boss_floors_cleared:
                    # ボス階に足を踏み入れたことを警告し、緊張感と身構える猶予を与える
                    # (静かに階段まで歩いて不意打ちされるより、事前に分かった方が
                    # ポーションの準備などができて楽しい)
                    pulse = 140 + int(90 * abs((tmr % 20) - 10) / 10)
                    draw_text(screen, "! A powerful presence lurks on this floor !", 130, banner_y + 70, fontS, (255, pulse//3, 30))
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
            # Floor Whisperer実績(全フロア特性を一度は踏破する)の進捗は、これまで
            # floor_modifiers_seenを記録するだけで画面上に一切表示されておらず、
            # 中学生には気づきにくかった。Traps triggeredと同じ行に、あと何種類の
            # フロア特性を踏めば良いか一目で分かるようにした。
            traits_seen_c = len(ach.get("floor_modifiers_seen", []))
            traits_total_c = len(FLOOR_MODIFIERS)
            draw_text(screen, f"Floor traits discovered: {traits_seen_c}/{traits_total_c}",
                      430, list_bottom_y, fontS, WHITE)
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
                elif pending_branch_route:
                    pending_branch_route = False
                    generate_branch_route_area()
                    branch_route_floor_skip_pending = True
                    welcome = 15
                    info_message = "Shortcut Passage! Grab the loot and reach the stairs to skip ahead."
                    info_timer = 80
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
                        if load_stats().get("blood_moons_survived", 0) >= 5:
                            unlock_achievement("crimson_survivor")
                    if branch_route_floor_skip_pending:
                        # 近道(分岐ルート)の出口。通常の+1に加えてもう1つ
                        # フロアを飛ばし、代わりにそのフロアの探索・経験値・
                        # 宝箱は手に入らない(carve_branch_route参照)
                        branch_route_floor_skip_pending = False
                        skipped_floor = floor + 1
                        floor = floor + 2
                        if not info_message:
                            info_message = f"Shortcut complete! Floor {skipped_floor} skipped."
                            info_timer = 70
                    else:
                        floor = floor + 1
                    apply_pet_bonuses()
                    if floor > fl_max:
                        fl_max = floor
                    record_stat("total_floors_descended")
                    record_stat_max("deepest_floor_reached", floor)
                    if load_stats().get("deepest_floor_reached", 0) >= 60:
                        unlock_achievement("deep_delver")
                    if in_endless_mode:
                        record_stat_max("deepest_endless_floor", floor)
                        if load_stats().get("deepest_endless_floor", 0) >= 100:
                            unlock_achievement("endless_delver")
                        if load_stats().get("deepest_endless_floor", 0) >= 150:
                            unlock_achievement("endless_legend")
                        if load_stats().get("deepest_endless_floor", 0) >= 200:
                            unlock_achievement("endless_myth")
                        if floor % ENDLESS_BLESSING_INTERVAL == 0 and floor > endless_blessing_floor:
                            # 深淵の祝福:潜るほど敵が強くなるだけだったエンドレス・
                            # ディープスに、25階ごとの永続的な小さな成長を追加した。
                            # これまで画面上のテキストポップアップのみで気づける
                            # 手段が無く、探索に集中していると見逃しやすかったため、
                            # レベルアップと同じジングル音を鳴らして「音でも気づける」
                            # ように改善した(UI/UX方針:視覚演出だけでなく音でも
                            # 気づけるようにする)。
                            endless_blessing_floor = floor
                            pl_str += ENDLESS_BLESSING_STR
                            pl_def_base += ENDLESS_BLESSING_DEF
                            info_message = f"Depths Blessing! +{ENDLESS_BLESSING_STR} STR, +{ENDLESS_BLESSING_DEF} DEF (permanent)"
                            info_timer = 90
                            se[4].play()
                    if difficulty in ("Hard", "Nightmare", "Abyss") and floor >= MAX_FLOOR:
                        unlock_achievement("hard_clear")
                    if difficulty in ("Nightmare", "Abyss") and floor >= MAX_FLOOR:
                        unlock_achievement("nightmare_clear")
                    if difficulty == "Abyss" and floor >= MAX_FLOOR:
                        unlock_achievement("abyss_clear")
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
                # ゲームオーバー画面はこれまで「You died./Game over.」の2行だけで、
                # 今回のプレイでどこまで進んだかはタイトル画面(通算最深フロア)を
                # 見に行かないと分からなかった。死んだその場で「もう一回!」と
                # 思えるように、このプレイ限定の簡単な結果を追加表示する
                # (通算記録total_kills等とは別に、run_kills/run_damage_dealtで
                # 今回のプレイ分だけをカウントしている)。
                draw_text(screen, f"Floor reached: {floor}", 300, 288, fontS, WHITE)
                draw_text(screen, f"Monsters defeated: {run_kills}", 300, 316, fontS, WHITE)
                draw_text(screen, f"Damage dealt: {run_damage_dealt}", 300, 344, fontS, WHITE)
                if difficulty == "Abyss":
                    # Abyssはパーマデス:死んだ瞬間にオートセーブを消し、
                    # 「[C] Continue」でこの続きに戻れないようにする(手動保存も
                    # idx==30で既に禁止済み)。真の一発勝負であることを
                    # ゲームオーバー画面でもはっきり言葉で伝える。
                    try:
                        if os.path.exists("autosave.json"):
                            os.remove("autosave.json")
                    except Exception as e:
                        _log_io_error("abyss autosave wipe", e)
                    _autosave_floor_cache = _UNSET
                    draw_text(screen, "ABYSS RUN ENDED - autosave erased. No continue.", 190, 380, fontS, (180, 60, 220))
                else:
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
                if typ == 28:
                    # Mirror Wraithの「通常攻撃を跳ね返す」という新しい駆け引きは
                    # 見た目だけでは伝わらないため、遭遇直後に一度だけ注意書きを
                    # 出して気づけるようにする(低HP警告などと同じ「音だけでなく
                    # 文字でも気づかせる」考え方)。
                    draw_text(screen, "It reflects damage from Attacks!", 220, 235, fontS, (220, 200, 255))
                elif typ == 29:
                    # Hollow Widowの「攻撃を当てるとHPを吸収してくる」という
                    # 駆け引きもMirror Wraith同様に見た目だけでは伝わらないため、
                    # 遭遇直後に一度だけ注意書きを出す。
                    draw_text(screen, "It drains life from its attacks!", 220, 235, fontS, (230, 230, 210))
                elif typ == 30:
                    # Chain Wardenの「攻撃が当たるとコンボを断ち切ってくる」という
                    # 駆け引きも見た目だけでは伝わらないため、遭遇直後に一度だけ
                    # 注意書きを出す。
                    draw_text(screen, "It can shatter your combo streak!", 220, 235, fontS, (200, 205, 230))
                elif typ == 31:
                    # Frenzied Revenantの「戦闘が長引くほど攻撃力が上がっていく」
                    # という駆け引きも見た目だけでは伝わらないため、遭遇直後に
                    # 一度だけ注意書きを出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "It grows stronger the longer this fight lasts!", 190, 235, fontS, (255, 180, 150))
                elif typ == 32:
                    # Abyssal Wardenの「HPが大きく減ると一度だけ自己回復する」
                    # という駆け引きも見た目だけでは伝わらないため、遭遇直後に
                    # 一度だけ注意書きを出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "It can heal itself once when badly wounded!", 170, 235, fontS, (200, 150, 255))
                elif typ == 33:
                    # Warbreaker Wightの「Defend中でもその防御ボーナスを無視して
                    # 攻撃してくる」という駆け引きも見た目だけでは伝わらないため、
                    # 遭遇直後に一度だけ注意書きを出す(既存の新モンスター注意書きと
                    # 同じ考え方)。
                    draw_text(screen, "It ignores your Defend bonus when it attacks!", 170, 235, fontS, (210, 160, 100))
                elif typ == 34:
                    # Gloom Spriteの「集中(Focus)で強化した状態を攻撃と同時に
                    # 奪い取る」という駆け引きも見た目だけでは伝わらないため、
                    # 遭遇直後に一度だけ注意書きを出す(既存の新モンスター注意書きと
                    # 同じ考え方)。
                    draw_text(screen, "It steals your Focus charge when it attacks!", 170, 235, fontS, (150, 210, 140))
                elif typ == 35:
                    # Hungry Ratの「攻撃が当たると食料をかじり取る」という
                    # 駆け引きも見た目だけでは伝わらないため、遭遇直後に一度だけ
                    # 注意書きを出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "It nibbles away your food when it attacks!", 175, 235, fontS, (200, 170, 110))
                elif typ == 36:
                    # Cinder Wardの「爆炎石のダメージを軽減する」という駆け引きも
                    # 見た目だけでは伝わらないため、遭遇直後に一度だけ注意書きを
                    # 出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "It resists damage from Blaze gems!", 190, 235, fontS, (255, 170, 90))
                elif typ == 37:
                    # Numbing Hornetの「戦闘中ずっと会心率を半減させる」という
                    # 駆け引きも見た目だけでは伝わらないため、遭遇直後に一度だけ
                    # 注意書きを出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "Its buzzing halves your critical hit chance!", 155, 235, fontS, (170, 150, 220))
                elif typ == 38:
                    # Ashbound Titanの「戦闘中ずっと通常攻撃のダメージを鈍らせる」
                    # という駆け引きも見た目だけでは伝わらないため、遭遇直後に
                    # 一度だけ注意書きを出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "Its crushing weight weakens your Attacks!", 175, 235, fontS, (150, 140, 130))
                elif typ == 39:
                    # Silence Wispの「戦闘中ずっとコンボがたまらなくなる」という
                    # 駆け引きも見た目だけでは伝わらないため、遭遇直後に一度だけ
                    # 注意書きを出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "Its silence keeps your Combo from building!", 155, 235, fontS, (90, 150, 175))
                elif typ == 40:
                    # Vengeful Wraithの「クリティカルヒットを与えると報復してくる」
                    # という駆け引きも見た目だけでは伝わらないため、遭遇直後に
                    # 一度だけ注意書きを出す(既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "It strikes back hard when you land a Critical Hit!", 145, 235, fontS, (230, 90, 100))
                elif typ == 41:
                    # Bloodthorn Revenantの「攻撃が命中すると、どんな対策でも
                    # 軽減できない出血を与えてくる」という駆け引きも見た目だけ
                    # では伝わらないため、遭遇直後に一度だけ注意書きを出す
                    # (既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "Its attacks cause Bleed, which no skill or floor trait can lessen!", 60, 235, fontS, (200, 30, 30))
                elif typ == 42:
                    # Permafrost Wyrmの「攻撃が命中すると、次のあなたの手番を
                    # まるごと1回封じてくる」という駆け引きも見た目だけでは
                    # 伝わらないため、遭遇直後に一度だけ注意書きを出す
                    # (既存の新モンスター注意書きと同じ考え方)。
                    draw_text(screen, "Its icy breath can Freeze you, skipping your entire next turn!", 60, 235, fontS, (150, 220, 255))
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                no_ultimate_shown = False
                
        elif idx == 11:
            draw_battle(screen, fontS)
            if tmr == 1 and not turn_msg_shown: 
                if pl_poison > 0:
                    pdmg = max(1, int(pl_lifemax // 20 * skill_poison_mult * relic_poison_resist_mult()))
                    pl_life -= pdmg
                    pl_poison = max(0, pl_poison - 30)
                    battle_took_damage = True
                    set_message(f"Poison {pdmg}dmg!", (190, 80, 220))
                    if pl_life <= 0:
                        pl_life = 0
                if pl_bleed > 0:
                    bdmg = max(1, int(pl_lifemax // BLOODTHORN_BLEED_DIVISOR))
                    pl_life -= bdmg
                    pl_bleed = max(0, pl_bleed - 1)
                    battle_took_damage = True
                    set_message(f"Bleed {bdmg}dmg!", (200, 30, 30))
                    if pl_life <= 0:
                        pl_life = 0
                if pl_life <= 0:
                    idx = 15
                    tmr = 0
                if idx == 11 and pl_frozen > 0:
                    # Permafrost Wyrm(typ42)による凍結。出血・毒と違いダメージは
                    # 伴わないが、emy_stunと対称に「行動そのものを1回封じる」
                    # 状態異常のため、プレイヤーの入力を待たずに直接idx13
                    # (敵の手番)へ進める(コマンド選択そのものをスキップする)。
                    pl_frozen = 0
                    set_message("You are frozen solid and skip your turn!", (150, 220, 255))
                    turn_msg_shown = True
                    idx = 13
                    tmr = 0
                elif idx == 11:
                    set_message("Your turn.", (150, 220, 255))
                    turn_msg_shown = True
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
                    elif btl_cmd == 6:
                        ultimate_req = effective_ultimate_combo_requirement()
                        if combo_count >= ultimate_req:
                            idx = 29
                            tmr = 0
                            flg_action = True
                        else:
                            if not no_ultimate_shown:
                                set_message(f"Ultimate not charged! ({combo_count}/{ultimate_req} combo)", (200, 90, 90))
                                no_ultimate_shown = True
                    elif btl_cmd == 7:
                        idx = 67
                        tmr = 0
                        flg_action = True

        elif idx == 12:
            draw_battle(screen, fontS)
            if tmr ==1:
                set_message("You attack!", (255, 230, 150))
                se[0].play()
                last_atk_special = None
                # Vengeful Wraith(typ40、rev199で追加)の報復判定用フラグ。
                # last_atk_specialはMASSIVE HIT/フィニッシャーで後から上書き
                # されるため「この一撃がクリティカルだったか」を確実に覚えて
                # おけない。tmr==11の報復判定はこの専用フラグを見る。
                last_hit_was_crit = False
                if typ == 39:
                    # Silence Wisp(typ39、今回追加分)と戦っている間は、静寂の
                    # 霧が集中を乱し、通常攻撃(Focus攻撃を含む)を当ててもコンボ
                    # ・必殺技ゲージが一切たまらない「静寂の霧」を持たせた。
                    # Numbing Hornet(会心率半減)・Ashbound Titan(通常攻撃威力
                    # ダウン)と同じ「戦闘中ずっと効き続ける」パターンを、今回は
                    # コンボの蓄積そのものに広げた初めての敵。コンボが貯まらない
                    # ためcombo_damage_mult()やUltimate解放判定は自然に無効化
                    # され、爆炎石・防御・反撃・集中など他のコマンドを織り交ぜる
                    # 立ち回りが必須になる。この敵との戦闘が終われば、次の戦闘
                    # からはコンボは普段通り積み上げられる(init_battle()で
                    # combo_countは毎回0にリセットされるため)。
                    pass
                else:
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
                pl_str_eff = pl_str + pet_str_bonus
                if pl_str_eff >= 500:
                    dmg = pl_str_eff + random.randint(0, 200)
                elif pl_str_eff >= 300:
                    dmg = pl_str_eff + random.randint(0, 50)
                else:
                    dmg = pl_str_eff + random.randint(0, 15)
                dmg = int(dmg * modifier_atk_mult())
                if typ == 38:
                    # Ashbound Titanと戦っている間は、のしかかる灰の重みで
                    # 通常攻撃(Focus攻撃を含む)のダメージがずっと20%下がる
                    # 「灰塵の重圧」。爆炎石・必殺技・反撃には影響しない。
                    dmg = int(dmg * ASHBOUND_TITAN_ATK_MULT)
                if pl_charge:
                    dmg = int(dmg * (modifier_focus_mult() + skill_focus_bonus) * char_params().get("focus_mult", 1.0))
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
                total_crit_chance = skill_crit_chance + modifier_crit_chance_bonus() + char_params()["crit_bonus"] + relic_crit_bonus() + charm_crit_bonus() + pet_crit_bonus
                if typ == 37:
                    # Numbing Hornetと戦闘中は、コンボ・Focus・秘宝/護符などで
                    # どれだけ会心率を積んでいても、羽音が集中を乱してその場で
                    # 半減させられてしまう(戦闘中ずっと効き続ける、初めての
                    # "場に居るだけの妨害")。
                    total_crit_chance *= NUMBING_HORNET_CRIT_MULT
                if total_crit_chance > 0 and random.random() < total_crit_chance:
                    # Ranger(rev209追加)のcrit_dmg_bonusは、Radiant/Dim Floorが
                    # 決めるクリティカル倍率そのものに上乗せする加算ボーナス
                    # (他キャラはデフォルト0.0のため無影響)。
                    dmg = int(dmg * (modifier_crit_dmg_mult() + char_params().get("crit_dmg_bonus", 0.0)))
                    set_message("CRITICAL HIT!", (255, 60, 60))
                    crit_flash_color = (255, 255, 190)
                    crit_flash_timer = CRIT_FLASH_FRAMES
                    trigger_screen_shake(6, 4)
                    if last_atk_special is None:
                        last_atk_special = "crit"
                    last_hit_was_crit = True
                    record_stat("critical_hits_landed")
                    if load_stats().get("critical_hits_landed", 0) >= 50:
                        unlock_achievement("crit_master")
                    if load_stats().get("critical_hits_landed", 0) >= 200:
                        unlock_achievement("critical_veteran")
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
                if in_boss_battle or in_echo_battle:
                    # Slayer's Emblem(秘宝)。ボス級の相手(通常のステージボス・
                    # エコーバトル・ボスラッシュ)にだけ効く初めての秘宝軸のため、
                    # ダメージ表示(このtmr==5)とHP減算(tmr==11)の両方に反映されるよう、
                    # 表示前の一度だけdmgそのものを底上げする。Vanguard(rev211追加)の
                    # boss_dmg_bonus・Warbound Floor(rev211追加)のmodifier_boss_dmg_bonus()も
                    # 同じ軸に加算する(他キャラ/他フロアはどちらも0.0のため無影響)。
                    dmg = int(dmg * (relic_boss_dmg_mult() + char_params().get("boss_dmg_bonus", 0.0) + modifier_boss_dmg_bonus()))
                emy_blink = 5
                set_message(str(dmg)+"pts of damage!", (255, 100, 100))
                if last_atk_special == "massive":
                    popup_color = (255, 215, 60)
                elif last_atk_special == "ultimate":
                    popup_color = (255, 80, 220)
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
                run_damage_dealt += dmg
                if load_stats().get("total_damage_dealt", 0) >= 100000:
                    unlock_achievement("executioner")
                # Reaver(rev195追加)はVampiric Floorが無くても常に攻撃で吸血できる
                # lifesteal_pctを持つため、フロア特性分(modifier_lifesteal_pct())と
                # キャラクター分(char_params()、他キャラはデフォルト0.0)を合算する。
                lifesteal_pct = modifier_lifesteal_pct() + char_params().get("lifesteal_pct", 0.0)
                if lifesteal_pct > 0 and pl_life > 0 and pl_life < pl_lifemax:
                    heal_amt = max(1, int(dmg * lifesteal_pct))
                    heal_amt = min(heal_amt, pl_lifemax - pl_life)
                    pl_life = min(pl_lifemax, pl_life + heal_amt)
                    set_message(f"Lifesteal! +{heal_amt}HP", (220, 60, 100))
                    spawn_damage_popup(190, 585, f"+{heal_amt}", (120, 255, 150), big=False)
                    # 実績「Bloodbound」:吸血で通算5,000HP回復すると解除。
                    record_stat("total_lifesteal_healed", heal_amt)
                    if load_stats().get("total_lifesteal_healed", 0) >= 5000:
                        unlock_achievement("bloodbound")
                echo_chance = modifier_echo_chance()
                if echo_chance > 0 and emy_life > 0 and random.randint(0, 99) < echo_chance:
                    echo_dmg = max(1, int(dmg * 0.5))
                    emy_life = emy_life - echo_dmg
                    record_stat("total_damage_dealt", echo_dmg)
                    run_damage_dealt += echo_dmg
                    set_message(f"Echo strike! +{echo_dmg}dmg!", (190, 140, 255))
                    spawn_damage_popup(popup_x, popup_y - 22, str(echo_dmg), (210, 170, 255), big=False)
                # 秘宝Serpent's Fang(rev198追加):これまでの毒/呪いはすべて
                # 敵からプレイヤーへの一方通行だったが、初めてプレイヤーの攻撃が
                # 敵を毒にできるようにした。emy_poison==0の間だけ判定するのは
                # 既存のpl_poison付与ロジック(idx==13)と同じお作法。rev201で
                # Apothecary(poison_bonus)を追加し、Serpent's Fangが無くても
                # この軸に触れられるようにした。
                enemy_poison_chance = relic_enemy_poison_chance() + modifier_enemy_poison_chance_bonus() + char_params().get("poison_bonus", 0)
                if enemy_poison_chance > 0 and emy_life > 0 and emy_poison == 0 and random.randint(0, 99) < enemy_poison_chance:
                    emy_poison = 40
                    emy_poisoned_this_battle = True
                    set_message("Serpent's Fang poisons the enemy!", (150, 210, 90))
                    unlock_achievement("venomtouch")
                    # 実績「Venom Adept」:通算25回、敵を毒にすると解除。
                    record_stat("enemies_poisoned_total")
                    if load_stats().get("enemies_poisoned_total", 0) >= 25:
                        unlock_achievement("venom_adept")
                # 秘宝Thunderclap Idol(rev202追加):Serpent's Fangと同じ「攻撃側から
                # 敵に状態異常を与える」構図だが、毒のような持続ダメージではなく、
                # emy_stun==0の間だけ判定し敵の次の手番を1回封じる(ダメージを
                # 伴わない状態異常はこれが初めて)。rev204でMarshal(stun_bonus)を
                # 追加し、Thunderclap Idolが無くてもこの軸に触れられるようにした。
                enemy_stun_chance = relic_enemy_stun_chance() + modifier_enemy_stun_chance_bonus() + char_params().get("stun_bonus", 0)
                if enemy_stun_chance > 0 and emy_life > 0 and emy_stun == 0 and random.randint(0, 99) < enemy_stun_chance:
                    emy_stun = 1
                    emy_stunned_this_battle = True
                    set_message("Thunderclap Idol stuns the enemy!", (235, 210, 90))
                    unlock_achievement("shocktouch")
                    # 実績「Stun Master」:通算25回、敵を気絶させると解除。
                    record_stat("enemies_stunned_total")
                    if load_stats().get("enemies_stunned_total", 0) >= 25:
                        unlock_achievement("stun_master")
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
                elif pet_type == "slime" and random.randint(0, 99) < pet_slime_assist_chance:
                    assist_dmg = max(1, int(dmg * 0.3))
                    emy_life = max(0, emy_life - assist_dmg)
                    set_message(f"Slime Pal assists! {assist_dmg}dmg!", (150, 220, 255))
                    if emy_life <= 0:
                        idx = 16
                        tmr = 0
                if (typ == 32 and emy_life > 0 and not abyssal_warden_healed_this_battle
                        and emy_life <= emy_lifemax * ABYSSAL_WARDEN_HEAL_HP_PCT):
                    # Abyssal Wardenは、HPがABYSSAL_WARDEN_HEAL_HP_PCT(30%)以下に
                    # 落ちた瞬間、1バトルにつき一度だけABYSSAL_WARDEN_HEAL_TARGET_PCT
                    # (60%)まで自己回復する。じわじわ削るだけでは息を吹き返される
                    # ため、一気に押し切るか爆炎石で仕留めるかの判断を迫られる。
                    heal_to = int(emy_lifemax * ABYSSAL_WARDEN_HEAL_TARGET_PCT)
                    if heal_to > emy_life:
                        emy_life = heal_to
                        abyssal_warden_healed_this_battle = True
                        set_message("The Abyssal Warden calls upon the depths to heal itself!", (170, 90, 230))
                        se[4].play()
                if ((in_boss_battle or in_echo_battle) and not boss_phase2 and emy_life > 0
                        and emy_life <= emy_lifemax * modifier_boss_phase2_threshold()):
                    boss_phase2 = True
                    emy_str = int(emy_str * BOSS_PHASE2_STR_MULT)
                    emy_blink = 12
                    dmg_eff = 8
                    se[1].play()
                    set_message(f"{emy_name} grows furious!!", (255, 80, 40))
                if typ == 28 and emy_life > 0:
                    # Mirror Wraithは通常攻撃(Attack)で削ると、与えたダメージの
                    # 一部を跳ね返してくる。爆炎石(Blaze gem、idx24の別経路)は
                    # この反射を経由しないため、消費アイテムの使いどころを考える
                    # 駆け引きになる(倒しきれば反射自体が発生しない点も同様)。
                    reflect_dmg = max(1, int(dmg * MIRROR_WRAITH_REFLECT_MULT))
                    dmg_reduction = pl_def_base + pl_def_buff + pet_def_bonus + modifier_def_bonus()
                    reflect_dmg = max(1, int((reflect_dmg - dmg_reduction * 0.3) * modifier_incoming_dmg_mult() * pet_dmg_reduction_mult))
                    pl_life = max(0, pl_life - reflect_dmg)
                    battle_took_damage = True
                    set_message(f"The Mirror Wraith reflects {reflect_dmg}dmg!", (200, 140, 255))
                    spawn_damage_popup(190, 585, str(reflect_dmg), (200, 140, 255), big=False)
                    if pl_life <= 0:
                        idx = 15
                        tmr = 0
                if typ == 40 and emy_life > 0 and last_hit_was_crit:
                    # Vengeful Wraithは、通常攻撃(Focus攻撃を含む)でクリティカル
                    # ヒットを与えた時だけ、そのダメージの一部で報復してくる。
                    # Mirror Wraith(typ28)の反射が命中したすべての攻撃を対象に
                    # するのとは違い、会心が絡んだ一撃だけを咎める初めての駆け引き。
                    retaliate_dmg = max(1, int(dmg * VENGEFUL_WRAITH_RETALIATE_MULT))
                    dmg_reduction = pl_def_base + pl_def_buff + pet_def_bonus + modifier_def_bonus()
                    retaliate_dmg = max(1, int((retaliate_dmg - dmg_reduction * 0.3) * modifier_incoming_dmg_mult() * pet_dmg_reduction_mult))
                    pl_life = max(0, pl_life - retaliate_dmg)
                    battle_took_damage = True
                    set_message(f"The Vengeful Wraith retaliates for {retaliate_dmg}dmg!", (255, 90, 100))
                    spawn_damage_popup(190, 585, str(retaliate_dmg), (255, 90, 100), big=False)
                    if pl_life <= 0:
                        idx = 15
                        tmr = 0
            if tmr == 16:
                idx = 13
                tmr = 0
                
        elif idx == 13:
            draw_battle(screen, fontS)
            if tmr == 1:
                if emy_poison > 0:
                    # 敵の毒(Serpent's Fang)は、プレイヤーの毒(idx==11)と対称に
                    # 「毒にかかっている本人の手番の頭」でダメージが入る。
                    # ここで敵が力尽きた場合は、そのまま攻撃させずidx==16(勝利)へ
                    # 進む(死んだ敵に反撃されるのを防ぐ)。
                    edmg = max(1, int(emy_lifemax // 20))
                    emy_life = max(0, emy_life - edmg)
                    emy_poison = max(0, emy_poison - 20)
                    set_message(f"Enemy poison {edmg}dmg!", (150, 210, 90))
                    if emy_life <= 0:
                        idx = 16
                        tmr = 0
                if idx == 13 and emy_stun > 0:
                    # 秘宝Thunderclap Idolによる気絶(rev202追加)。毒(emy_poison)は
                    # ダメージを与えるだけで敵の手番自体は普通に発生していたが、
                    # 気絶は初めて敵の手番そのものを丸ごと1回封じる状態異常。
                    # tmr==20の通常の手番終了処理と同じ後始末をしてidx==11
                    # (プレイヤーの手番)へ直接戻る。
                    emy_stun = 0
                    set_message(f"{emy_name} is stunned and can't move!", (235, 210, 90))
                    pl_def_buff = max(0, pl_def_buff - 5)
                    flg_action = False
                    turn_msg_shown = False
                    no_potion_shown = False
                    no_blazegem_shown = False
                    no_defensepill_shown = False
                    no_ultimate_shown = False
                    idx = 11
                    tmr = 0
                if idx == 13:
                    set_message("Enemy turn.", (255, 150, 150))
            if tmr == 5:
                set_message(emy_name+" attack!", (255, 150, 150))
                se[0].play()
                emy_step = 30
            if tmr == 9:
                dmg_reduction = pl_def_base + pl_def_buff + pet_def_bonus + modifier_def_bonus()
                # Warbreaker Wight(typ33)は、プレイヤーがDefend中(pl_def_buff>0)
                # に攻撃してくると、その防御ボーナス分だけを無視して素通りさせる
                # 「ガードブレイク」を持つ(ベースDEF・ペット・フロア特性による
                # 軽減は通常通り効く)。Defendがどの敵にも通用する安全策だった
                # 中で、初めて防御コマンドそのものを咎めてくる敵。
                guard_broken = typ == 33 and pl_def_buff > 0
                if guard_broken:
                    dmg_reduction = pl_def_base + pet_def_bonus + modifier_def_bonus()
                dmg = max(1, int(((emy_str + random.randint(0, emy_str)) - dmg_reduction) * modifier_incoming_dmg_mult() * pet_dmg_reduction_mult))
                set_message(str(dmg)+"pts of damage!", (255, 100, 100))
                spawn_damage_popup(190, 585, str(dmg), (255, 90, 90), big=boss_phase2)
                dmg_eff = 5
                emy_step = 0
                trigger_screen_shake(8 if boss_phase2 else 5, 5 if boss_phase2 else 3)
                if typ in (5, 7, 14) and pl_poison == 0 and not modifier_poison_immune() and random.randint(0, 99) < 30 + modifier_poison_chance_bonus():
                    pl_poison = 50
                    set_message("Poisoned!", (190, 80, 220))
                if typ == 41 and pl_bleed == 0 and random.randint(0, 99) < BLOODTHORN_BLEED_CHANCE + modifier_bleed_chance_bonus():
                    pl_bleed = BLOODTHORN_BLEED_TICKS
                    set_message("Bleeding!", (200, 30, 30))
                if typ == 42 and pl_frozen == 0 and random.randint(0, 99) < PERMAFROST_FREEZE_CHANCE + modifier_freeze_chance_bonus() - charm_freeze_resist_bonus():
                    pl_frozen = 1
                    set_message("Frozen solid!", (150, 220, 255))
                if guard_broken:
                    set_message("Warbreaker Wight shatters your guard!", (230, 150, 80))
                if typ == 34 and pl_charge:
                    # Gloom Spriteは、プレイヤーが集中(Focus)で次の一撃を強化した
                    # 状態(pl_charge)のときに攻撃してくると、被ダメージ自体は
                    # 変えずにその強化状態だけを奪い取ってしまう。Warbreaker Wightが
                    # Defendを咎めるのと同じ発想を、より早い段階で覚えるFocus
                    # コマンドに対して適用した新しい駆け引き。
                    pl_charge = False
                    set_message("The Gloom Sprite steals your Focus charge!", (150, 210, 140))
            if tmr == 15:
                pl_life = pl_life - dmg
                battle_took_damage = True
                if typ == 29 and emy_life > 0:
                    # Hollow Widowは通常攻撃(Attack)・反撃(Counter)問わず、プレイヤーに
                    # 与えたダメージの一部で自分のHPを回復する。Mirror Wraithの反射とは
                    # 違い被ダメージは増えないが、じわじわ削るだけでは回復に追いつかれる
                    # ため、一気に押し切るか爆炎石で削り切るかの判断を迫られる。
                    drain_heal = min(emy_lifemax - emy_life, max(1, int(dmg * HOLLOW_WIDOW_DRAIN_MULT)))
                    if drain_heal > 0:
                        emy_life += drain_heal
                        set_message(f"The Hollow Widow drains {drain_heal}HP!", (230, 230, 210))
                if typ == 30 and combo_count > 0 and random.randint(0, 99) < CHAIN_WARDEN_BREAK_CHANCE:
                    # Chain Wardenは通常攻撃(Attack)・反撃(Counter)問わず、命中すると
                    # 確率でプレイヤーのコンボストリークを断ち切る。コンボを積む戦い方に
                    # 対して初めて「敵側からの妨害」を持たせた新しい駆け引き。
                    combo_count = 0
                    set_message("The Chain Warden shatters your combo!", (180, 180, 210))
                if typ == 31 and emy_life > 0:
                    # Frenzied Revenantは攻撃するたびに自分のSTRが伸びていく。
                    # 反射(Mirror Wraith)・生命吸収(Hollow Widow)・コンボ破壊
                    # (Chain Warden)はどれも「その場で」効く駆け引きだったが、
                    # これは「時間が経つほど危険になる」という初めての方向性の
                    # 特性で、長期戦を選ぶプレイヤーに一撃の重みで応える。
                    emy_str = int(emy_str * FRENZIED_REVENANT_STR_GROWTH)
                if typ == 35 and food > 0 and random.randint(0, 99) < HUNGRY_RAT_STEAL_CHANCE:
                    # Hungry Ratは通常攻撃(Attack)・反撃(Counter)問わず、命中すると
                    # 確率で食料(food)を1つかじり取る。foodは0になると歩数ごとに
                    # HPが減り始める実際に意味のある資源のため、放置して長居すると
                    # じわじわ損をする「早めに仕留める理由」になる。
                    food -= 1
                    set_message("The Hungry Rat nibbles away 1 food!", (200, 170, 110))
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
                no_ultimate_shown = False
                
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
                    in_trial_post_battle = False
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
                if in_arena_mode:
                    # 闘技場はdraw_dungeon()が前提とするダンジョン状態(make_dungeon()
                    # 未実行)を持たないため、通常の死亡演出(idx==9)を共用せず、
                    # エコー撃破(idx==60)と同じ「タイトル背景+パネル」形式の
                    # 専用の敗北演出(idx==75)を使う。
                    idx = 75
                    tmr = 0
                elif in_boss_rush_mode:
                    # ボスラッシュも闘技場と同じ理由でidx==9を共用せず、
                    # 専用の敗北演出(idx==79)を使う。
                    idx = 79
                    tmr = 0
                else:
                    idx = 9
                    tmr = 29

        elif idx == 16:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You win!", (255, 215, 0))
                pygame.mixer.music.stop()
                se[5].play()
                record_stat("total_kills")
                run_kills += 1
                if load_stats().get("total_kills", 0) >= 500:
                    unlock_achievement("veteran")
                if typ == 27:
                    record_stat("voidforged_golems_defeated")
                    unlock_achievement("voidforged_slain")
                    if load_stats().get("voidforged_golems_defeated", 0) >= 10:
                        unlock_achievement("voidforged_bane")
                if typ == 28:
                    record_stat("mirror_wraiths_defeated")
                    unlock_achievement("mirror_wraith_slain")
                    if load_stats().get("mirror_wraiths_defeated", 0) >= 10:
                        unlock_achievement("mirror_wraith_bane")
                if typ == 29:
                    record_stat("hollow_widows_defeated")
                    unlock_achievement("hollow_widow_slain")
                    if load_stats().get("hollow_widows_defeated", 0) >= 10:
                        unlock_achievement("hollow_widow_bane")
                if typ == 30:
                    record_stat("chain_wardens_defeated")
                    unlock_achievement("chain_warden_slain")
                    if load_stats().get("chain_wardens_defeated", 0) >= 10:
                        unlock_achievement("chain_warden_bane")
                if typ == 31:
                    record_stat("frenzied_revenants_defeated")
                    unlock_achievement("frenzied_revenant_slain")
                    if load_stats().get("frenzied_revenants_defeated", 0) >= 10:
                        unlock_achievement("frenzied_revenant_bane")
                if typ == 32:
                    record_stat("abyssal_wardens_defeated")
                    unlock_achievement("abyssal_warden_slain")
                    if load_stats().get("abyssal_wardens_defeated", 0) >= 10:
                        unlock_achievement("abyssal_warden_bane")
                if typ == 33:
                    record_stat("warbreaker_wights_defeated")
                    unlock_achievement("warbreaker_wight_slain")
                    if load_stats().get("warbreaker_wights_defeated", 0) >= 10:
                        unlock_achievement("warbreaker_wight_bane")
                if typ == 34:
                    record_stat("gloom_sprites_defeated")
                    unlock_achievement("gloom_sprite_slain")
                    if load_stats().get("gloom_sprites_defeated", 0) >= 10:
                        unlock_achievement("gloom_sprite_bane")
                if typ == 35:
                    record_stat("hungry_rats_defeated")
                    unlock_achievement("hungry_rat_slain")
                    if load_stats().get("hungry_rats_defeated", 0) >= 10:
                        unlock_achievement("hungry_rat_bane")
                    food += HUNGRY_RAT_BONUS_FOOD
                    set_message(f"The Hungry Rat drops {HUNGRY_RAT_BONUS_FOOD} reclaimed food!", (200, 170, 110))
                if typ == 36:
                    record_stat("cinder_wards_defeated")
                    unlock_achievement("cinder_ward_slain")
                    if load_stats().get("cinder_wards_defeated", 0) >= 10:
                        unlock_achievement("cinder_ward_bane")
                if typ == 37:
                    record_stat("numbing_hornets_defeated")
                    unlock_achievement("numbing_hornet_slain")
                    if load_stats().get("numbing_hornets_defeated", 0) >= 10:
                        unlock_achievement("numbing_hornet_bane")
                if typ == 38:
                    record_stat("ashbound_titans_defeated")
                    unlock_achievement("ashbound_titan_slain")
                    if load_stats().get("ashbound_titans_defeated", 0) >= 10:
                        unlock_achievement("ashbound_titan_bane")
                if typ == 39:
                    record_stat("silence_wisps_defeated")
                    unlock_achievement("silence_wisp_slain")
                    if load_stats().get("silence_wisps_defeated", 0) >= 10:
                        unlock_achievement("silence_wisp_bane")
                if typ == 40:
                    record_stat("vengeful_wraiths_defeated")
                    unlock_achievement("vengeful_wraith_slain")
                    if load_stats().get("vengeful_wraiths_defeated", 0) >= 10:
                        unlock_achievement("vengeful_wraith_bane")
                if typ == 41:
                    record_stat("bloodthorn_revenants_defeated")
                    unlock_achievement("bloodthorn_revenant_slain")
                    if load_stats().get("bloodthorn_revenants_defeated", 0) >= 10:
                        unlock_achievement("bloodthorn_revenant_bane")
                if typ == 42:
                    record_stat("permafrost_wyrms_defeated")
                    unlock_achievement("permafrost_wyrm_slain")
                    if load_stats().get("permafrost_wyrms_defeated", 0) >= 10:
                        unlock_achievement("permafrost_wyrm_bane")
                register_bounty_kill()
                if not battle_took_damage:
                    unlock_achievement("no_damage_win")
                    # 「無傷で勝つ」実績(no_damage_win)は初回はあるが、Golden
                    # Hunter/Rift Master/Bounty Masterなどと同じ「初回はあるが
                    # 繰り返し系が無かった」穴が残っていたため、通算10回の
                    # 累積実績を新設した。
                    record_stat("no_damage_wins")
                    if load_stats().get("no_damage_wins", 0) >= 10:
                        unlock_achievement("flawless_victor")
                # 「無傷で勝つ」実績(no_damage_win)とは正反対の、被弾を重ねながら
                # ギリギリのHPで勝ち切ったことを称える実績。Sanctuary Floorの
                # 全回復(下記)が適用される前のpl_life/pl_lifemaxで判定する。
                if pl_lifemax > 0 and 0 < pl_life / pl_lifemax < 0.15:
                    unlock_achievement("close_call")
                    record_stat("close_calls")
                    if load_stats().get("close_calls", 0) >= 10:
                        unlock_achievement("iron_will")
                if emy_poisoned_this_battle:
                    # Serpent's Fangで一度でも敵を毒にしてから倒すと進む累積実績。
                    # 初回付与そのものはidx==12/67のvenomtouchで解除済みなので、
                    # ここでは「その毒を効かせて倒し切った」通算回数だけを数える。
                    record_stat("poisoned_enemies_defeated")
                    if load_stats().get("poisoned_enemies_defeated", 0) >= 10:
                        unlock_achievement("serpent_charmer")
                if modifier_full_heal_on_kill() and pl_life > 0 and pl_life < pl_lifemax:
                    pl_life = pl_lifemax
                    set_message("Sanctuary heals you fully!", (150, 255, 190))
                exp_gain = int(max(1, (typ + 1) * emy_lv * 3) * pl_exp_mult * diff_params()["exp_mult"] * skill_exp_mult * char_params()["exp_mult"] * modifier_exp_mult() * relic_exp_mult() * charm_exp_mult() * pet_exp_mult)
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
                if pl_lv >= 40:
                    unlock_achievement("legendary_hero")
                # レベルアップ時の画面フラッシュ・画面シェイク演出は煩わしいという
                # 要望のため廃止した。メッセージとジングルのみで節目を演出する。
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
                dmg = int(1000 * modifier_blaze_dmg_mult() * char_params().get("blaze_mult", 1.0) * relic_blaze_dmg_mult())
                if typ == 36:
                    dmg = int(dmg * CINDER_WARD_BLAZE_RESIST_MULT)
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
                buff_amount = int(random.randint(5, 15) * modifier_defpill_mult())
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

        elif idx == 67:
            # 反撃(Counter)。既存のDefense Pill(idx23)は防御力だけを底上げし、
            # Focus(idx24)は次のAttackを強化するだけで、どちらも「その場で
            # 攻守を両立する」コマンドではなかった。Counterは、あえて敵の攻撃を
            # 迎え撃って被ダメージを軽減しつつ、直後にこちらから反撃する
            # 単独完結の攻防一体コマンド。反撃ダメージは通常のAttackより
            # 控えめ(COUNTER_DMG_MULT)な代わりに、被ダメージも同時に抑えられる。
            # 敵の攻撃処理そのものはidx13と同じ計算式を使うが、Counter専用の
            # 追加DEF・反撃という後続処理があるため、idx13を共用せず独立した
            # ステートとして実装した(1つのコマンドの不具合が他のコマンドの
            # 挙動に波及しないようにするため)。
            draw_battle(screen, fontS)
            if tmr == 1:
                combo_count = 0
                set_message("Counter stance!", (120, 200, 255))
            if tmr == 5:
                set_message(emy_name+" attack!", (255, 150, 150))
                se[0].play()
                emy_step = 30
            if tmr == 9:
                counter_def_bonus = int(COUNTER_DEF_BONUS * (modifier_counter_bonus() + skill_counter_bonus) * char_params().get("counter_mult", 1.0) * relic_counter_mult())
                dmg_reduction = pl_def_base + pl_def_buff + pet_def_bonus + modifier_def_bonus() + counter_def_bonus
                dmg = max(1, int(((emy_str + random.randint(0, emy_str)) - dmg_reduction) * modifier_incoming_dmg_mult() * pet_dmg_reduction_mult))
                set_message(str(dmg)+"pts of damage!", (255, 100, 100))
                spawn_damage_popup(190, 585, str(dmg), (255, 90, 90), big=boss_phase2)
                emy_step = 0
                trigger_screen_shake(8 if boss_phase2 else 5, 5 if boss_phase2 else 3)
                if typ in (5, 7, 14) and pl_poison == 0 and not modifier_poison_immune() and random.randint(0, 99) < 30 + modifier_poison_chance_bonus():
                    pl_poison = 50
                    set_message("Poisoned!", (190, 80, 220))
                if typ == 41 and pl_bleed == 0 and random.randint(0, 99) < BLOODTHORN_BLEED_CHANCE + modifier_bleed_chance_bonus():
                    pl_bleed = BLOODTHORN_BLEED_TICKS
                    set_message("Bleeding!", (200, 30, 30))
                if typ == 42 and pl_frozen == 0 and random.randint(0, 99) < PERMAFROST_FREEZE_CHANCE + modifier_freeze_chance_bonus() - charm_freeze_resist_bonus():
                    pl_frozen = 1
                    set_message("Frozen solid!", (150, 220, 255))
            if tmr == 15:
                pl_life = pl_life - dmg
                battle_took_damage = True
                if typ == 29 and emy_life > 0:
                    drain_heal = min(emy_lifemax - emy_life, max(1, int(dmg * HOLLOW_WIDOW_DRAIN_MULT)))
                    if drain_heal > 0:
                        emy_life += drain_heal
                        set_message(f"The Hollow Widow drains {drain_heal}HP!", (230, 230, 210))
                if typ == 35 and food > 0 and random.randint(0, 99) < HUNGRY_RAT_STEAL_CHANCE:
                    # Mirror Wraithの反射がCounterだけ抜けていた過去の不具合と
                    # 同じ轍を踏まないよう、Hungry Ratの食料かじり取りも通常攻撃
                    # (idx13)と反撃(Counter)の両方に揃えて実装した。
                    food -= 1
                    set_message("The Hungry Rat nibbles away 1 food!", (200, 170, 110))
                if pl_life < 0:
                    pl_life = 0
                    idx = 15
                    tmr = 0
            if tmr == 20:
                pl_str_eff = pl_str + pet_str_bonus
                cdmg = int(pl_str_eff * COUNTER_DMG_MULT * (modifier_counter_bonus() + skill_counter_bonus) * char_params().get("counter_mult", 1.0) * relic_counter_mult()) + random.randint(0, 10)
                cdmg = int(cdmg * modifier_atk_mult())
                set_message(f"Counter attack! {cdmg}pts of damage!", (120, 200, 255))
                popup_x = emy_x + imgEnemy.get_width()/2 - 16
                popup_y = emy_y + emy_step - 6
                spawn_damage_popup(popup_x, popup_y, str(cdmg), (120, 200, 255), big=False)
                emy_life -= cdmg
                record_stat("total_damage_dealt", cdmg)
                run_damage_dealt += cdmg
                record_stat("counters_used")
                if load_stats().get("total_damage_dealt", 0) >= 100000:
                    unlock_achievement("executioner")
                if load_stats().get("counters_used", 0) >= 30:
                    unlock_achievement("counter_master")
                # Serpent's Fangは通常攻撃(Attack)と同じく反撃(Counter)にも
                # 適用する(Hungry Ratの食料かじり取りと同じ理由で、Attack側だけ
                # 効いてCounter側だけ抜けている、という食い違いを避けるため)。
                # rev201のApothecary(poison_bonus)もAttack側と同じく反映する。
                enemy_poison_chance = relic_enemy_poison_chance() + modifier_enemy_poison_chance_bonus() + char_params().get("poison_bonus", 0)
                if enemy_poison_chance > 0 and emy_life > 0 and emy_poison == 0 and random.randint(0, 99) < enemy_poison_chance:
                    emy_poison = 40
                    emy_poisoned_this_battle = True
                    set_message("Serpent's Fang poisons the enemy!", (150, 210, 90))
                    unlock_achievement("venomtouch")
                    record_stat("enemies_poisoned_total")
                    if load_stats().get("enemies_poisoned_total", 0) >= 25:
                        unlock_achievement("venom_adept")
                # Thunderclap IdolもSerpent's Fangと同じ理由でCounter側にも適用する。
                # rev204のMarshal(stun_bonus)もAttack側と同じく反映する。
                enemy_stun_chance = relic_enemy_stun_chance() + modifier_enemy_stun_chance_bonus() + char_params().get("stun_bonus", 0)
                if enemy_stun_chance > 0 and emy_life > 0 and emy_stun == 0 and random.randint(0, 99) < enemy_stun_chance:
                    emy_stun = 1
                    emy_stunned_this_battle = True
                    set_message("Thunderclap Idol stuns the enemy!", (235, 210, 90))
                    unlock_achievement("shocktouch")
                    record_stat("enemies_stunned_total")
                    if load_stats().get("enemies_stunned_total", 0) >= 25:
                        unlock_achievement("stun_master")
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
                if (typ == 32 and emy_life > 0 and not abyssal_warden_healed_this_battle
                        and emy_life <= emy_lifemax * ABYSSAL_WARDEN_HEAL_HP_PCT):
                    heal_to = int(emy_lifemax * ABYSSAL_WARDEN_HEAL_TARGET_PCT)
                    if heal_to > emy_life:
                        emy_life = heal_to
                        abyssal_warden_healed_this_battle = True
                        set_message("The Abyssal Warden calls upon the depths to heal itself!", (170, 90, 230))
                        se[4].play()
                if typ == 28 and emy_life > 0:
                    # 【バグ修正】Mirror Wraithの反射は通常攻撃(idx12)・必殺技
                    # (idx29、idx12に合流)では発生するのに、反撃(Counter)の
                    # 反撃ダメージ(ここ)だけ他の2コマンドと違って反射処理が
                    # 実装されておらず、Counterで削るとMirror Wraith戦の一番の
                    # 駆け引きを回避できてしまっていた。Hollow Widow(typ29)の
                    # 生命吸収・Abyssal Warden(typ32)の緊急回復はすでにCounter
                    # 側にも実装済みだったため、抜けていたMirror Wraithの反射だけ
                    # idx12と同じ計算式でここにも揃えた。
                    reflect_dmg = max(1, int(cdmg * MIRROR_WRAITH_REFLECT_MULT))
                    reflect_dmg_reduction = pl_def_base + pl_def_buff + pet_def_bonus + modifier_def_bonus()
                    reflect_dmg = max(1, int((reflect_dmg - reflect_dmg_reduction * 0.3) * modifier_incoming_dmg_mult() * pet_dmg_reduction_mult))
                    pl_life = max(0, pl_life - reflect_dmg)
                    battle_took_damage = True
                    set_message(f"The Mirror Wraith reflects {reflect_dmg}dmg!", (200, 140, 255))
                    spawn_damage_popup(190, 585, str(reflect_dmg), (200, 140, 255), big=False)
                    if pl_life <= 0:
                        idx = 15
                        tmr = 0
            if tmr == 30:
                pl_def_buff = max(0, pl_def_buff - 5)
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                no_ultimate_shown = False
                idx = 11
                tmr = 0

        elif idx == 29:
            # 必殺技(Ultimate)。コンボをULTIMATE_COMBO_REQUIREMENT分ためて解放する
            # 新しいバトルコマンドで、キャラクターごとに全く異なる一撃になる
            # (ULTIMATE_DEFS参照)。ダメージ演出そのものは既存のAttack処理
            # (idx==12)を、爆炎石(idx==21)と同じ「dmgを自前で計算してから
            # idx=12・tmr=4へ合流する」手法で再利用し、ヒット判定・ミラー
            # ウレイスの反射・撃破判定などを重複実装しない。
            draw_battle(screen, fontS)
            ud = ultimate_def()
            if tmr == 1:
                combo_count = 0
                set_message(f"{ud['name']}!", (255, 80, 220))
                se[4].play()
                trigger_screen_shake(10, 6)
                record_stat("ultimates_used")
                unlock_achievement("ultimate_unleashed")
                if load_stats().get("ultimates_used", 0) >= 20:
                    unlock_achievement("ultimate_master")
                heal_pct = ud.get("heal_pct", 0)
                if heal_pct > 0 and pl_life > 0:
                    heal_amt = min(int(pl_lifemax * heal_pct), pl_lifemax - pl_life)
                    if heal_amt > 0:
                        pl_life += heal_amt
                        set_message(f"{ud['name']} heals +{heal_amt}HP!", (150, 255, 190))
            if tmr == 11:
                dmg = int((pl_str + pet_str_bonus) * ud["mult"]) + random.randint(0, ud["bonus_rand"])
                dmg += ud.get("lv_bonus", 0) * pl_lv
                dmg = int(dmg * modifier_atk_mult() * modifier_ultimate_mult())
                last_atk_special = "ultimate"
                idx = 12
                tmr = 4

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
                no_ultimate_shown = False
                
        elif idx == 26:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Boss defeated!", (255, 215, 0))
                boss_floors_cleared.add(floor)
                unlock_achievement("boss_defeat")
                record_stat("bosses_defeated_count")
                # 新システム「ヒーロー覚醒」:このキャラクターでの初めてのボス撃退
                # なら永久に覚醒させる(詳細はawaken_character()の定義を参照)。
                awaken_character(selected_character)
                # Boss Defeat(初回1回)の上位版。Elite Hunter->Elite Slayerや
                # High Roller->Card Sharkと同じく、繰り返しボスを倒し続ける
                # ことを評価する累積目標が無かったため、既存の記録
                # (bosses_defeated_count)をそのまま活かして追加した。
                if load_stats().get("bosses_defeated_count", 0) >= 20:
                    unlock_achievement("boss_vanquisher")
                if difficulty in ("Hard", "Nightmare", "Abyss") and floor >= MAX_FLOOR:
                    unlock_achievement("hard_clear")
                if difficulty in ("Nightmare", "Abyss") and floor >= MAX_FLOOR:
                    unlock_achievement("nightmare_clear")
                if difficulty == "Abyss" and floor >= MAX_FLOOR:
                    unlock_achievement("abyss_clear")
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
                # 【新要素】通常ボス撃破時のみ(エコーバトルは周回可能な練習戦なので
                # 対象外)、まれに未所持の秘宝を1つ手に入れる。
                relic_pool = [r for r in RELIC_DEFS if not load_relics().get(r["key"], False)]
                if relic_pool and random.randint(0, 99) < min(99, RELIC_DROP_CHANCE + modifier_relic_drop_bonus()):
                    new_relic = random.choice(relic_pool)
                    if unlock_relic(new_relic["key"]):
                        unlock_achievement("relic_finder")
                        if all(load_relics().get(r["key"], False) for r in RELIC_DEFS):
                            unlock_achievement("relic_collector")
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
                    if in_true_hidden_stage:
                        unlock_achievement("true_hidden_boss_defeat")
                        record_stat("true_hidden_boss_defeats")
                    else:
                        unlock_achievement("hidden_boss_defeat")
                        record_stat("hidden_boss_defeats")
                    in_hidden_stage = False
                    idx = 41
                    tmr = 0
                elif floor >= MAX_FLOOR and not in_endless_mode:
                    unlock_achievement("game_clear")
                    idx = 27
                    tmr = 0
                elif stage_local_floor(floor) == STAGE_LENGTH:
                    # ステージクリア: 次のステージへ進む前に拠点(サンクチュア)を挟む
                    # (エンドレス・ディープス中も30階サイクルごとに同じサンクチュアで
                    # 一息つけるようにしており、ここは通常周回と共通の処理)
                    idx = 28
                    tmr = 0
                else:
                    pygame.mixer.music.load(bgm_field_for_floor(floor))
                    pygame.mixer.music.play(-1)
                    idx = 2
                    tmr = 0

        elif idx == 27:
            # 全3ステージクリア(ゲームクリア)演出。ここから[X]キーで、今の
            # レベル・スキル・所持品をそのまま引き継いだ「エンドレス・ディープス」
            # (終わりの無い91階以降の周回モード)へ直接続けられる(新規に
            # ステータスを作り直す専用モードではなく、達成した周回の続きを
            # そのまま遊べるようにする狙い)。
            if tmr == 1:
                pygame.mixer.music.stop()
                se[5].play()
                record_stat("runs_completed")
                # runs_completed(通算ゲームクリア回数)は以前から記録されて
                # いたが、単発の"game_clear"実績しか無く、Golden Hunter/Rift
                # Master/Bounty Masterなどと同じ「初回はあるが繰り返し達成し
                # 続けることを評価する累積実績が無かった」穴が残っていたため、
                # 既存の記録をそのまま活かして追加した。
                if load_stats().get("runs_completed", 0) >= 5:
                    unlock_achievement("grand_champion")
                flush_playtime()
                if daily_mode:
                    record_daily_result(floor, cleared=True)
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 340))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, "GAME CLEAR!", 280, 290, font, (255, 215, 0))
            draw_text(screen, "You cleared all 3 stages!", 250, 345, font, WHITE)
            draw_text(screen, f"Difficulty: {difficulty}", 320, 400, fontS, DIFFICULTY_COLORS.get(difficulty, WHITE))
            if tmr > 90:
                draw_text(screen, "Press space key to return to Title", 220, 450, fontS, BLINK[tmr%6])
                draw_text(screen, "[X] Continue into Endless Depths!", 220, 490, fontS, (200, 160, 255))
            if tmr > 90 and key[K_SPACE] == 1:
                idx = 0
                tmr = 0
            if tmr > 90 and key[K_x] == 1:
                # 現在のキャラクターをそのまま、フロア91から終わりの無い周回を続ける
                in_endless_mode = True
                floor = floor + 1
                apply_pet_bonuses()
                if floor > fl_max:
                    fl_max = floor
                record_stat("total_floors_descended")
                record_stat_max("deepest_floor_reached", floor)
                if load_stats().get("deepest_floor_reached", 0) >= 60:
                    unlock_achievement("deep_delver")
                pl_life = pl_lifemax
                food = max(food, 150)
                welcome = 15
                make_dungeon()
                put_event()
                info_message = "Entering Endless Depths! Keep descending as deep as you can."
                info_timer = 120
                pygame.mixer.music.load(bgm_field_for_floor(floor))
                pygame.mixer.music.play(-1)
                idx = 1
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
            sanctuary_title = f"Depths Cleared! (Floor {floor})" if in_endless_mode else f"Stage {current_stage(floor)} Cleared!"
            draw_text(screen, sanctuary_title, 260, 210, font, (255, 215, 0))
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

        elif idx == 68:
            # 旅の吟遊詩人: 今の仲間を新しい仲間と交換できる一度限りの機会
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(190)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "A traveling bard!", 280, 160, font, (190, 150, 255))
            if pet_type is not None:
                draw_text(screen, f"Current pet: {PET_TYPES[pet_type]['name']}", 200, 230, fontS, CYAN)
                draw_text(screen, "\"I can sing you a new companion into being...", 130, 280, fontS, WHITE)
                draw_text(screen, " but your old one will be gone for good.\"", 130, 310, fontS, WHITE)
                draw_text(screen, "[Y] Swap for a new pet   [N] Keep current pet", 150, 360, fontS, (255, 215, 0))
            else:
                draw_text(screen, "\"Come back once you have a companion of your own.\"", 110, 260, fontS, WHITE)
            if info_timer > 0 and info_message != "":
                draw_text(screen, info_message, 250, 420, fontS, (120, 255, 150))
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
                no_ultimate_shown = False

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
            if in_true_hidden_stage:
                draw_text(screen, "TRUE ENDING II", 260, 300, font, (200, 60, 220))
                draw_text(screen, "You defeated ??? The Voidcrowned!", 170, 360, font, WHITE)
            else:
                draw_text(screen, "TRUE ENDING", 300, 300, font, (200, 60, 220))
                draw_text(screen, "You defeated the hidden boss!", 210, 360, font, WHITE)
            draw_text(screen, f"Difficulty: {difficulty}", 320, 420, fontS, DIFFICULTY_COLORS.get(difficulty, WHITE))
            if tmr > 90:
                draw_text(screen, "Press space key", 320, 480, font, BLINK[tmr%6])
            if tmr > 90 and key[K_SPACE] == 1:
                in_true_hidden_stage = False
                idx = 0
                tmr = 0

        elif idx == 72:
            # 闘技場: ラウンド開始演出(通常のボス戦idx==25と同様の流れ)
            if tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(battle_bg_for_floor(floor), [bx, by])
                draw_text(screen, f"Arena of Trials - Round {arena_round}", 150, 200, font, (255, 140, 60))
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" appear!", 260, 200, font, (255, 140, 60))
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                no_ultimate_shown = False

        elif idx == 73:
            # 闘技場: ラウンドクリア。次のラウンドに挑む(ハイリスク)か、
            # ここで退いて報酬を持ち帰る(ローリスク)かをプレイヤーに選ばせる、
            # いわゆる「攻めるか、退くか」のプッシュユアラック型の駆け引き。
            draw_battle(screen, fontS)
            if tmr == 1:
                pygame.mixer.music.stop()
                se[5].play()
                heal_amt = int(pl_lifemax * ARENA_HEAL_PCT_PER_ROUND)
                pl_life = min(pl_lifemax, pl_life + heal_amt)
                record_stat_max("arena_best_round", arena_round)
                unlock_achievement("arena_novice")
                if arena_round >= 10:
                    unlock_achievement("arena_gladiator")
                # 実績「Arena Veteran」:継続・退却・敗北のいずれで区切っても
                # クリアした分は必ずこのidx==73(ラウンドクリア演出)を通るため、
                # ここで1回だけ加算すれば全挑戦を通算した数になる。
                record_stat("arena_total_rounds_cleared")
                if load_stats().get("arena_total_rounds_cleared", 0) >= 50:
                    unlock_achievement("arena_veteran")
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, f"Round {arena_round} Cleared!", 260, 290, font, (255, 215, 0))
            draw_text(screen, f"HP: {pl_life}/{pl_lifemax}", 340, 345, fontS, CYAN)
            if tmr > 40:
                draw_text(screen, f"[Space] Continue to Round {arena_round+1}", 180, 400, fontS, (120, 255, 150))
                draw_text(screen, "[Esc] Retreat and bank your rewards", 200, 430, fontS, (255, 215, 90))
            if tmr > 40 and key[K_SPACE] == 1:
                arena_round += 1
                floor = ARENA_BASE_FLOOR + (arena_round - 1) * ARENA_FLOOR_STEP
                init_battle()
                init_message()
                idx = 72
                tmr = 0
            elif tmr > 40 and key[K_ESCAPE] == 1:
                idx = 74
                tmr = 0

        elif idx == 74:
            # 闘技場: 退却(報酬確定)。ここまで勝ち抜いたラウンド数に応じて
            # ポーション・ブレイズジェムを持ち帰れる、退いた場合の安全な着地点。
            if tmr == 1:
                pygame.mixer.music.stop()
                potion += arena_round // 2
                blazegem += arena_round // 4
                in_arena_mode = False
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, "Arena Retreat", 300, 290, font, (255, 215, 0))
            draw_text(screen, f"Rounds cleared: {arena_round}", 280, 345, fontS, WHITE)
            draw_text(screen, f"Rewards: +{arena_round // 2} Potion, +{arena_round // 4} Blaze gem",
                      170, 380, fontS, (120, 255, 150))
            if tmr > 60:
                draw_text(screen, "Press space key to return to Title", 220, 440, font, BLINK[tmr%6])
            if tmr > 60 and key[K_SPACE] == 1:
                idx = 0
                tmr = 0

        elif idx == 75:
            # 闘技場: 敗北。draw_dungeon()前提の通常死亡演出(idx==9)は
            # make_dungeon()未実行の闘技場では使えないため、エコー撃破(idx==60)と
            # 同じ「タイトル背景+パネル」形式の専用結果画面を用意した。最後の
            # 1ラウンド手前まで勝ち抜いた分の報酬は退却時と同じ計算式で渡す。
            if tmr == 1:
                pygame.mixer.music.stop()
                se[3].play()
                cleared_rounds = max(0, arena_round - 1)
                potion += cleared_rounds // 2
                blazegem += cleared_rounds // 4
                in_arena_mode = False
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, "You Fell in the Arena", 230, 290, font, (220, 60, 60))
            cleared_rounds = max(0, arena_round - 1)
            draw_text(screen, f"Rounds cleared: {cleared_rounds}", 280, 345, fontS, WHITE)
            draw_text(screen, f"Rewards: +{cleared_rounds // 2} Potion, +{cleared_rounds // 4} Blaze gem",
                      170, 380, fontS, (120, 200, 255))
            if tmr > 60:
                draw_text(screen, "Press space key to return to Title", 220, 440, font, BLINK[tmr%6])
            if tmr > 60 and key[K_SPACE] == 1:
                idx = 0
                tmr = 0

        elif idx == 76:
            # ボスラッシュ: 次のボス登場演出(闘技場idx==72・通常のボス戦idx==25と同様の流れ)
            if tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(battle_bg_for_floor(floor), [bx, by])
                draw_text(screen, f"Boss Rush - {boss_rush_index+1}/{len(BOSS_RUSH_FLOORS)}", 170, 200, font, (255, 90, 90))
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" appear!", 260, 200, font, (255, 90, 90))
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                no_ultimate_shown = False

        elif idx == 77:
            # ボスラッシュ: 1体撃破。闘技場と違い攻める/退くの選択は無く、
            # 一定割合回復してから次のボスへ進むか(全て倒し切っていれば
            # idx==78のクリア演出へ)を選ぶだけのシンプルな構成。
            draw_battle(screen, fontS)
            if tmr == 1:
                pygame.mixer.music.stop()
                se[5].play()
                heal_amt = int(pl_lifemax * BOSS_RUSH_HEAL_PCT_PER_BOSS)
                pl_life = min(pl_lifemax, pl_life + heal_amt)
                record_stat_max("boss_rush_best_streak", boss_rush_index + 1)
                unlock_achievement("boss_rush_starter")
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, f"{boss_rush_index+1}/{len(BOSS_RUSH_FLOORS)} Bosses Defeated!", 130, 290, font, (255, 215, 0))
            draw_text(screen, f"HP: {pl_life}/{pl_lifemax}", 340, 345, fontS, CYAN)
            if tmr > 50:
                draw_text(screen, "[Space] Face the next boss", 240, 400, fontS, (120, 255, 150))
            if tmr > 50 and key[K_SPACE] == 1:
                boss_rush_index += 1
                if boss_rush_index >= len(BOSS_RUSH_FLOORS):
                    idx = 78
                    tmr = 0
                else:
                    floor = BOSS_RUSH_FLOORS[boss_rush_index]
                    init_boss_battle()
                    init_message()
                    pygame.mixer.music.load("sound/Tolerance_Deviation.mp3")
                    pygame.mixer.music.play(-1)
                    idx = 76
                    tmr = 0

        elif idx == 78:
            # ボスラッシュ: 全9体撃破の完全クリア演出。闘技場の退却報酬より
            # 一段豪華な固定報酬を渡し、称号付き実績「boss_rush_champion」も
            # ここで解除する。
            if tmr == 1:
                pygame.mixer.music.stop()
                se[5].play()
                record_stat("boss_rush_clears")
                unlock_achievement("boss_rush_champion")
                # 実績「Boss Rush Veteran」:通算5回ボスラッシュを完全クリアすると解除。
                if load_stats().get("boss_rush_clears", 0) >= 5:
                    unlock_achievement("boss_rush_veteran")
                potion += 5
                blazegem += 5
                pl_lifemax += 20
                pl_life += 20
                in_boss_rush_mode = False
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, "BOSS RUSH CLEARED!", 210, 290, font, (255, 215, 0))
            draw_text(screen, "All 9 stage bosses defeated in a row!", 150, 345, fontS, WHITE)
            draw_text(screen, "Reward: +5 Potion, +5 Blaze gem, +20 Max HP", 130, 375, fontS, (120, 255, 150))
            if tmr > 60:
                draw_text(screen, "Press space key to return to Title", 220, 440, font, BLINK[tmr%6])
            if tmr > 60 and key[K_SPACE] == 1:
                idx = 0
                tmr = 0

        elif idx == 79:
            # ボスラッシュ: 敗北。闘技場のidx==75と同じ「タイトル背景+パネル」
            # 形式の専用結果画面。ここまで倒し切ったボスの数を結果として示す
            # (途中経過の報酬持ち帰りは無く、次の挑戦への目安のみを見せる)。
            if tmr == 1:
                pygame.mixer.music.stop()
                se[3].play()
                in_boss_rush_mode = False
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            panel = pygame.Surface((880, 300))
            panel.set_alpha(170)
            panel.fill(BLACK)
            screen.blit(panel, [0, 260])
            draw_text(screen, "The Boss Rush Ends Here", 190, 290, font, (220, 60, 60))
            draw_text(screen, f"Bosses defeated: {boss_rush_index}/{len(BOSS_RUSH_FLOORS)}", 220, 345, fontS, WHITE)
            if tmr > 60:
                draw_text(screen, "Press space key to return to Title", 220, 420, font, BLINK[tmr%6])
            if tmr > 60 and key[K_SPACE] == 1:
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
                no_ultimate_shown = False

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
                            "survival": "Survival", "fortune": "Fortune", "tactics": "Tactics"}
            # Tactics枝の追加で5列→6列になったため、Counter追加時のコマンド行間
            # 詰め(60px→45px)と同じ考え方で、箱の幅・列間隔を詰めて880px幅に
            # 収まるよう調整した(実際にfontXSでの各スキルの説明文の描画幅を
            # 計測し、右隣の列の箱が後から重ねて描かれることで前の列のはみ出しが
            # 隠れる仕組みも維持できることを確認済み)。
            BOX_W, BOX_H = 132, 145
            COL_GAP = 6
            START_X = 14
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

        elif idx == 58:
            # ペット情報画面(ダンジョン画面に重ねて表示、スキルツリー画面と同じ構成)。
            # 従来は探索中のステータス行に「Pet: 名前 (効果)」を常時表示していたが、
            # 他のステータス行と重なって視界を圧迫していたため、[P]キーで開く
            # 専用画面に切り出した。
            draw_dungeon(screen, fontS)
            overlay = pygame.Surface((880, 720))
            overlay.set_alpha(190)
            overlay.fill(BLACK)
            screen.blit(overlay, [0, 0])
            draw_text(screen, "Pet Info", 60, 18, font, (255, 215, 0))
            if pet_type is not None:
                icon = imgPet.get(pet_type)
                icon_y = 120
                if icon is not None:
                    screen.blit(icon, [340, icon_y])
                draw_text(screen, PET_TYPES[pet_type]["name"], 60, 340, font, (150, 220, 255))
                draw_text(screen, PET_TYPES[pet_type]["desc"], 60, 380, fontS, WHITE)
                # 【新要素】仲間の絆(Pet Bond):同じ仲間と長く潜り続けると効果が
                # 強化される。専用画面のここでしか表示しない値なので、探索中の
                # 常時表示(過去に一度、重なって見づらいという理由で廃止済み)を
                # 復活させずに済んでいる。
                if pet_is_bonded():
                    draw_text(screen, "* Bonded! (effect boosted)", 60, 410, fontS, (255, 215, 0))
                else:
                    floors_left = max(0, modifier_pet_bond_floor_requirement() - (floor - pet_hatched_floor))
                    draw_text(screen, f"Bonds in {floors_left} more floor(s) together", 60, 410, fontS, (170, 170, 170))
            draw_text(screen, "Esc/P: back", 60, 660, fontS, WHITE)

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
        if rare_treasure_sound_pending:
            se[4].play()
            rare_treasure_sound_pending = False
        if hidden_wall_sound_pending:
            se[0].play()
            hidden_wall_sound_pending = False
        if branch_route_sound_pending:
            se[0].play()
            branch_route_sound_pending = False
        if low_hp_warning_sound_pending:
            se[0].play()
            low_hp_warning_sound_pending = False
        if achievement_sound_pending:
            se[4].play()
            achievement_sound_pending = False
        if relic_sound_pending:
            se[4].play()
            relic_sound_pending = False
        if charm_sound_pending:
            se[4].play()
            charm_sound_pending = False
        draw_achievement_toast(screen)
        draw_relic_toast(screen)
        draw_charm_toast(screen)
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
