import discord
import random
import math
import youtube_dl
import os
import re
import shutil
import asyncio
from datetime import datetime
from discord.ext import commands

# Configure intents (1.5.0)
client = commands.Bot(command_prefix='^', guild_subscriptions=True, intents=discord.Intents.default())


@client.event
async def on_ready():  # 봇이 준비되었을때. 스탠바이 상태일때 출력.
    print(f'{client.user.name} online!')
    flag = True  # 하루 날짜를 갱신하고 나면, 그 뒤로는 86400초 마다 날짜를 갱신.
    while True:
        # price = pyupbit.get_current_price("KRW-XTZ")
        date = datetime.today().strftime("%Y/%m/%d")
        game = discord.Game(f"^cmd_list | {date}")
        await client.change_presence(status=discord.Status.online, activity=game)
        # await asyncio.sleep(5)

        current_time = datetime.today().strftime("%H/%M/%S")
        time_list = current_time.split("/")

        if flag:
            # 날짜 갱신까지(0시 0분 0초) 남은 시간(초 단위 기준)
            wait_time = 86400 - (int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int(time_list[2]))
            await asyncio.sleep(wait_time)
            flag = False
        else:
            await asyncio.sleep(86400)


# @client.event
# async def on_command_error(ctx, error):
#     await ctx.send('매개변수가 부족하거나 잘못된 명령어입니다.\n'
#                    '^cmd_list 명령어를 통해 전체 명령어를 확인할 수 있습니다.')


# @client.event
# async def on_member_join(member):
#     guild = member.guild
#     if guild.system_channel is not None:
#         to_send = f'{member.mention}님이 {guild.name}에 등장했습니다!'
#         await guild.system_channel.send(to_send)
#
#
# @client.event
# async def on_member_remove(member):
#     guild = member.guild
#     if guild.system_channel is not None:
#         to_send = f'{member.mention}님이 {guild.name}에서 나가셨습니다..'
#         await guild.system_channel.send(to_send)


@client.command()
async def cmd_list(ctx):
    await ctx.send("prefix: ^\n"
                   "• ^hello → \'Hello, world!\'\n"
                   "• ^check_ping → 봇의 현재 지연시간을 출력합니다.\n"
                   "• ^echo [] → 자신이 한 말을 그대로 따라합니다.\n"
                   "• ^dice [] 또는 [] [] → 주사위를 굴립니다.\n"
                   "• ^poker 또는 [] → 와! 즐겁다!\n"
                   "• ^sutda → 즐거운 민속놀이\n"
                   "• ^gacha → 그지빵꾸쟁이를 위한 작혼 가챠 시뮬레이터\n"
                   "• ^set_pickup → 픽업 작사를 무작위로 설정합니다.\n"
                   "• ^server → 서버의 정보를 출력합니다.\n"
                   "• ^calc → 계산기, [연산순서: 왼쪽->오른쪽] [연산자: (+,-,*,/,^)]\n\n"
                   # "• ^random_pic → 랜덤한 사진을 출력합니다.\n\n"
                   
                   "• ^join → 음성채널에 봇을 초대합니다.\n"
                   "• ^leave → 음성채널에서 봇을 내보냅니다.\n"
                   "• ^play [url] → 해당 url의 곡을 재생합니다.\n"
                   # "• ^queue [url] → 봇의 재생목록에 곡을 추가합니다.\n"
                   "• ^pause → 음악을 일시정지합니다.\n"
                   "• ^resume → 음악 재생을 재개합니다.\n"
                   "• ^skip → 음악을 건너뜁니다.\n")


@client.command()
async def hello(ctx, user: discord.User):
    print(ctx.message.author.id)
    content = "Hello, World!"
    await client.send(content)


@client.command()
async def echo(ctx, *, text):
    await ctx.send(text)


@client.command()
async def score(ctx):
    await ctx.send(file=discord.File("mahjong_score.jpg"))


@client.command()
async def last_origin(ctx):
    await ctx.send(file=discord.File("last_origin.png"))


def check_authorization(ctx):
    auth_list = [462616417012023307,  # 내 아이디
                 # 254570370189754369,  # 자비
                 # 206770538062807040,  # 은호
                 # 381021569561919489,  # 민경님
                 # 460111416985124874,  # 내 부캐
                 ]

    for user in auth_list:
        if ctx.message.author.id == user:
            return True
    return False


@client.command()
async def current_status(ctx, *, stat):
    auth = check_authorization(ctx)
    if not auth:
        await ctx.send(f"{ctx.author.mention} 커맨드 사용 권한이 없습니다!")
        return

    game = discord.Game(stat)
    await client.change_presence(status=discord.Status.online, activity=game)
    await ctx.send(f"{ctx.author.mention} 변경 완료!")


@client.command()
async def check_ping(ctx):
    await ctx.send(f"current ping: {round(client.latency * 1000)}ms")


@client.command()
async def poker(ctx, player_num=0):
    your_hand = list()
    print_hand = ""
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    card_list = {1: ":regional_indicator_a:", 2: ":two:", 3: ":three:", 4: ":four:", 5: ":five:", 6: ":six:",
                 7: ":seven:", 8: ":eight:", 9: ":nine:", 10: ":keycap_ten:", 11: ":regional_indicator_j:",
                 12: ":regional_indicator_q:", 13: ":regional_indicator_k:"}

    if player_num:
        hand_list = list()
        common_card = list()
        for i in range(player_num):
            your_hand = list()
            for j in range(2):  # 플레이어 카드 2장
                draw = random.choice(num_list)
                your_hand.append(draw)
            your_hand.sort()
            hand_list.append(your_hand)

        for i in range(5):  # 공통 카드 5장
            common_card.append(random.choice(num_list))
        common_card.sort()

        count = 1
        for hand in hand_list:
            print_hand = f"Player {count}: "
            for card in hand:
                print_hand += (card_list[card] + " ")
            await ctx.send(print_hand.rstrip())
            count += 1

        print_hand = ""
        for card in common_card:
            print_hand += (card_list[card] + " ")

        await ctx.send(print_hand.rstrip())

    else:
        for i in range(5):
            your_hand.append(random.choice(num_list))
        your_hand.sort()

        for card in your_hand:
            print_hand += (card_list[card] + " ")

        await ctx.send(print_hand.rstrip())


character_list = ["<:aihara:810860484991123456>", "<:fujita:810860493056770069>", "<:hinamomo:810860506474741810>",
                      "<:igarashi:810860529579982850>", "<:jinia:810860545451491389>", "<:kirby:810860568407048232>",
                      "<:kitami:810860576615038997>", "<:kotori:810860586069655552>", "<:kujo:810860596097581057>",
                      "<:mikami:810860608698056734>", "<:nadeshiko:810860616692137985>",
                      "<:ninomiya:810860630067904542>", "<:sara:810860649869344781>", "<:shiroishi:810860659117916191>",
                      "<:suzumiya:810860667053408287>", "<:yagi:810860679539720242>", "<:kaguya:817585332950007879>",
                      "<:terasaki:817585340625715221>", "<:fuji:817585316437033001>", "<:fujimoto:817585324770328576>",
                      "<:erisa:817585303228383254>"]


@client.command()
async def set_pickup(ctx):
    filename = "gacha_pickup.txt"
    pickup = random.randint(0, 20)
    with open(filename, 'w') as file_object:
        file_object.write(str(pickup))
    await ctx.send(f"새로운 픽업 작사는 {character_list[pickup]}입니다!")


@client.command()
async def gacha(ctx):
    is_char = False
    is_purple = False
    result = list()

    filename = "gacha_pickup.txt"
    with open(filename) as file_object:
        content = file_object.read()

    soushoku_list = ["<:akai_bara:810848656457990154>", "<:bakuen:810848671507152896>", "<:crimson:810848679284047883>",
                     "<:denshi:810848687726919731>", "<:dot_coin:810848694890922025>", "<:dot_KO:810848702574886933>",
                     "<:emerald:810848712225325056>", "<:gekirin:810848719977054218>", "<:ghost:810848728718114836>",
                     "<:ghost_pai:810848739316990033>", "<:gold:810848748452053023>", "<:green:810848756282425344>",
                     "<:hane:810848767930662922>", "<:hone:810848776427405312>", "<:hono:810848784727801867>",
                     "<:hono_arashi:810848793465061417>", "<:ice_bar:810848801773453362>",
                     "<:isshoku:810848811286921247>", "<:ketto:810849032598454312>", "<:koakuma:810849042132631562>",
                     "<:kokuen:810849049677922354>", "<:koneko:810849056813350965>", "<:koumori:810849066782162954>",
                     "<:negi:810849074205949963>", "<:niboshi:810849093316116511>", "<:red:810849103734767656>",
                     "<:reppu:810853326169964594>", "<:ryubu:810853333421654016>", "<:sakura_fubuki:810853340707160094>",
                     "<:seien:810853349535776799>", "<:shinken:810853357911539753>", "<:shussen:810853367810490388>",
                     "<:suika:810853377101266975>", "<:sword:810853388236619817>", "<:touketsu:810853396416430112>",
                     "<:violet:810853409049149440>", "<:white:810853419254415391>", "<:yellow:810853427428458507>",
                     "<:zanei:810853437146267698>"]

    item_list_green = ["<:item_1_g:810848827434598410>", "<:item_2_g:810848848192864266>",
                       "<:item_3_g:810848890424393759>", "<:item_4_g:810848923950252043>",
                       "<:item_5_g:810848951422287882>", "<:item_6_g:810848975439003658>",
                       "<:item_7_g:810848999006535751>", "<:item_8_g:810849017876971571>"]

    item_list_blue = ["<:item_1_b:810848819544588349>", "<:item_2_b:810848843872469012>",
                      "<:item_3_b:810848879066873867>", "<:item_4_b:810848916086063134>",
                      "<:item_5_b:810848942744928306>", "<:item_6_b:810848967747305512>",
                      "<:item_7_b:810848991951585301>", "<:item_8_b:810849012072316938>"]

    item_list_purple = ["<:item_1_p:810848834728886323>", "<:item_2_p:810848864411058226>",
                        "<:item_3_p:810848897248264212>", "<:item_4_p:810848933554683915>",
                        "<:item_5_p:810848958372642818>", "<:item_6_p:810848983375020032>",
                        "<:item_7_p:810849005864747098>", "<:item_8_p:810849025246887986>"]

    kakutei_enshutsu = ["gacha_list/kakutei.png", "gacha_list/kakutei_1.png", "gacha_list/kakutei_2.png",
                        "gacha_list/kakutei_3.png", "gacha_list/kakutei_4.png", "gacha_list/no_kaku.png"]

    for i in range(10):  # range(10)은 0부터 10 미만의 숫자를 포함하는 range 객체를 만들어 준다.
        probability = random.randint(1, 100)
        if probability <= 5:  # 캐릭터 등장 확률 5%, 픽업 작사인경우 그 중에서도 59%
            pickup_prob = random.randint(1, 100)
            if pickup_prob <= 0.59:
                result.append(character_list[int(content)])
            else:
                result.append(random.choice(character_list))
            is_char = True
        elif probability <= 20:  # 장식품 등장 확률 15%, 픽업 장식품인경우 그 중에서도 49%(미구현)
            result.append(random.choice(soushoku_list))
        elif probability <= 44:  # 녹색 아이템 등장 확률 24%
            result.append(random.choice(item_list_green))
        elif probability <= 95:  # 청색 아이템 등장 확률 51%
            result.append(random.choice(item_list_blue))
        else:  # 자색 아이템 등장 확률 5%, 10연챠를 하게 될 경우, 자색 아이템을 반드시 한개 이상 획득 가능
            result.append(random.choice(item_list_purple))
            is_purple = True

        if i == 8 and not is_purple:  # 자색 아이템이 안나왔을때, 반드시 나오도록 함.
            rand_index = random.randint(0, 8)
            result.insert(rand_index, random.choice(item_list_purple))
            break

    if is_char:
        await ctx.send(file=discord.File(random.choice(kakutei_enshutsu)))
        await asyncio.sleep(1)
    else:
        await ctx.send(file=discord.File("gacha_list/no_kaku.png"))
        await asyncio.sleep(1)
    await ctx.send(" ".join(result))


@client.command()
async def uma(ctx, times):
    speed, stamina, power, patience, intelligence, repeat = 0, 0, 0, 0, 0, 0
    while repeat < int(times):
        rand = random.randint(1, 100)
        if rand <= 20:
            speed += 1
        elif rand <= 40:
            stamina += 1
        elif rand <= 60:
            power += 1
        elif rand <= 80:
            patience += 1
        else:
            intelligence += 1
        repeat += 1
    await ctx.send(f"반복 횟수: {repeat}\n\n"
                   f"스피드: {speed}, 스태미나: {stamina}, 파워: {power},"
                   f"근성: {patience}, 능지: {intelligence}\n\n"
                   f"<비율>\n"
                   f"스피드: {round((speed / repeat) * 100, 2)}%, "
                   f"스태미나: {round((stamina / repeat) * 100, 2)}%, "
                   f"파워: {round((power / repeat) * 100, 2)}%, "
                   f"근성: {round((patience / repeat) * 100, 2)}%, "
                   f"능지: {round((intelligence / repeat) * 100, 2)}%\n\n")


def black_cube_rare():
    global first_ability, second_ability, third_ability

    first_pick = random.randint(1, 1000000)
    second_pick = random.randint(1, 1000000)
    third_pick = random.randint(1, 1000000)

    if first_pick <= 61224: first_ability = "STR: +12"
    elif first_pick <= 122448: first_ability = "DEX: +12"
    elif first_pick <= 183672: first_ability = "INT: +12"
    elif first_pick <= 244896: first_ability = "LUK: +12"
    elif first_pick <= 306120: first_ability = "최대 HP: +120"
    elif first_pick <= 367344: first_ability = "최대 MP: +120"
    elif first_pick <= 408160: first_ability = "공격력: +12"
    elif first_pick <= 448976: first_ability = "마력: +12"
    elif first_pick <= 510200: first_ability = "STR: +3%"
    elif first_pick <= 571424: first_ability = "DEX: +3%"
    elif first_pick <= 632648: first_ability = "INT: +3%"
    elif first_pick <= 693872: first_ability = "LUK: +3%"
    elif first_pick <= 714280: first_ability = "공격력: +3%"
    elif first_pick <= 734688: first_ability = "마력: +3%"
    elif first_pick <= 755096: first_ability = "크리티컬 확률: +4%"
    elif first_pick <= 775504: first_ability = "데미지: +3%"
    elif first_pick <= 816320: first_ability = "올스탯: +5"
    elif first_pick <= 836728: first_ability = "공격 시 20% 확률로 240의 HP 회복"
    elif first_pick <= 857136: first_ability = "공격 시 20% 확률로 120의 MP 회복"
    elif first_pick <= 877544: first_ability = "공격 시 20% 확률로 6레벨 중독효과 적용"
    elif first_pick <= 897952: first_ability = "공격 시 10% 확률로 2레벨 기절효과 적용"
    elif first_pick <= 918360: first_ability = "공격 시 20% 확률로 2레벨 슬로우효과 적용"
    elif first_pick <= 938768: first_ability = "공격 시 20% 확률로 3레벨 암흑효과 적용"
    elif first_pick <= 959176: first_ability = "공격 시 10% 확률로 2레벨 빙결효과 적용"
    elif first_pick <= 979584: first_ability = "공격 시 10% 확률로 2레벨 봉인효과 적용"
    else: first_ability = "몬스터 방어율 무시: +15%"  # 999992

    if second_pick <= 109091: second_ability = "STR: +6"
    elif second_pick <= 218182: second_ability = "DEX: +6"
    elif second_pick <= 327273: second_ability = "INT: +6"
    elif second_pick <= 436364: second_ability = "LUK: +6"
    elif second_pick <= 545455: second_ability = "최대 HP: +60"
    elif second_pick <= 654546: second_ability = "최대 MP: +60"
    elif second_pick <= 727273: second_ability = "공격력: +6"
    elif second_pick <= 800000: second_ability = "마력: +6"
    elif second_pick <= 812245: second_ability = "STR: +12"
    elif second_pick <= 824490: second_ability = "DEX: +12"
    elif second_pick <= 836745: second_ability = "INT: +12"
    elif second_pick <= 848980: second_ability = "LUK: +12"
    elif second_pick <= 861225: second_ability = "최대 HP: +120"
    elif second_pick <= 873470: second_ability = "최대 MP: +120"
    elif second_pick <= 881633: second_ability = "공격력: +12"
    elif second_pick <= 889796: second_ability = "마력: +12"
    elif second_pick <= 902041: second_ability = "STR: +3%"
    elif second_pick <= 914286: second_ability = "DEX: +3%"
    elif second_pick <= 926531: second_ability = "INT: +3%"
    elif second_pick <= 938776: second_ability = "LUK: +3%"
    elif second_pick <= 942858: second_ability = "공격력: +3%"
    elif second_pick <= 946940: second_ability = "마력: +3%"
    elif second_pick <= 951022: second_ability = "크리티컬 확률: +4%"
    elif second_pick <= 955104: second_ability = "데미지: +3%"
    elif second_pick <= 963267: second_ability = "올스탯: +5"
    elif second_pick <= 967349: second_ability = "공격 시 20% 확률로 240의 HP 회복"
    elif second_pick <= 971431: second_ability = "공격 시 20% 확률로 120의 MP 회복"
    elif second_pick <= 975513: second_ability = "공격 시 20% 확률로 6레벨 중독효과 적용"
    elif second_pick <= 979595: second_ability = "공격 시 10% 확률로 2레벨 기절효과 적용"
    elif second_pick <= 983677: second_ability = "공격 시 20% 확률로 2레벨 슬로우효과 적용"
    elif second_pick <= 987759: second_ability = "공격 시 20% 확률로 3레벨 암흑효과 적용"
    elif second_pick <= 991841: second_ability = "공격 시 10% 확률로 2레벨 빙결효과 적용"
    elif second_pick <= 995923: second_ability = "공격 시 10% 확률로 2레벨 봉인효과 적용"
    else: second_ability = "몬스터 방어율 무시: +15%"  # 1000005

    if third_pick <= 129545: third_ability = "STR: +6"
    elif third_pick <= 259090: third_ability = "DEX: +6"
    elif third_pick <= 388635: third_ability = "INT: +6"
    elif third_pick <= 518180: third_ability = "LUK: +6"
    elif third_pick <= 647725: third_ability = "최대 HP: +60"
    elif third_pick <= 777270: third_ability = "최대 MP: +60"
    elif third_pick <= 863634: third_ability = "공격력: +6"
    elif third_pick <= 949998: third_ability = "마력: +6"
    elif third_pick <= 953059: third_ability = "STR: +12"
    elif third_pick <= 956120: third_ability = "DEX: +12"
    elif third_pick <= 959181: third_ability = "INT: +12"
    elif third_pick <= 962242: third_ability = "LUK: +12"
    elif third_pick <= 965303: third_ability = "최대 HP: +120"
    elif third_pick <= 968364: third_ability = "최대 MP: +120"
    elif third_pick <= 970405: third_ability = "공격력: +12"
    elif third_pick <= 972446: third_ability = "마력: +12"
    elif third_pick <= 975507: third_ability = "STR: +3%"
    elif third_pick <= 978568: third_ability = "DEX: +3%"
    elif third_pick <= 981629: third_ability = "INT: +3%"
    elif third_pick <= 984690: third_ability = "LUK: +3%"
    elif third_pick <= 985710: third_ability = "공격력: +3%"
    elif third_pick <= 986730: third_ability = "마력: +3%"
    elif third_pick <= 987750: third_ability = "크리티컬 확률: +4%"
    elif third_pick <= 988770: third_ability = "데미지: +3%"
    elif third_pick <= 990811: third_ability = "올스탯: +5"
    elif third_pick <= 991831: third_ability = "공격 시 20% 확률로 240의 HP 회복"
    elif third_pick <= 992851: third_ability = "공격 시 20% 확률로 120의 MP 회복"
    elif third_pick <= 993871: third_ability = "공격 시 20% 확률로 6레벨 중독효과 적용"
    elif third_pick <= 994891: third_ability = "공격 시 10% 확률로 2레벨 기절효과 적용"
    elif third_pick <= 995911: third_ability = "공격 시 20% 확률로 2레벨 슬로우효과 적용"
    elif third_pick <= 996931: third_ability = "공격 시 20% 확률로 3레벨 암흑효과 적용"
    elif third_pick <= 997951: third_ability = "공격 시 10% 확률로 2레벨 빙결효과 적용"
    elif third_pick <= 998971: third_ability = "공격 시 10% 확률로 2레벨 봉인효과 적용"
    else: third_ability = "몬스터 방어율 무시: +15%"  # 999991


def black_cube_epic():
    global first_ability, second_ability, third_ability

    first_pick = random.randint(1, 1000000)
    second_pick = random.randint(1, 1000000)
    third_pick = random.randint(1, 1000000)

    if first_pick <= 108696: first_ability = "STR: +6%"
    elif first_pick <= 217392: first_ability = "DEX: +6%"
    elif first_pick <= 326088: first_ability = "INT: +6%"
    elif first_pick <= 434784: first_ability = "LUK: +6%"
    elif first_pick <= 543480: first_ability = "최대 HP: +6%"
    elif first_pick <= 652176: first_ability = "최대 MP: +6%"
    elif first_pick <= 695654: first_ability = "공격력: +6%"
    elif first_pick <= 739132: first_ability = "마력: +6%"
    elif first_pick <= 782610: first_ability = "크리티컬 확률: +8%"
    elif first_pick <= 826088: first_ability = "데미지: +6%"
    elif first_pick <= 869566: first_ability = "올스탯: +3%"
    elif first_pick <= 913044: first_ability = "공격 시 20% 확률로 360의 HP 회복"
    elif first_pick <= 956522: first_ability = "공격 시 20% 확률로 180의 HP 회복"
    else: first_ability = "몬스터 방어율 무시: +15%"

    if second_pick <= 48980: second_ability = "STR: +12"
    elif second_pick <= 97960: second_ability = "DEX: +12"
    elif second_pick <= 146940: second_ability = "INT: +12"
    elif second_pick <= 195920: second_ability = "LUK: +12"
    elif second_pick <= 244900: second_ability = "최대 HP: +120"
    elif second_pick <= 293880: second_ability = "최대 MP: +120"
    elif second_pick <= 326533: second_ability = "공격력: +12"
    elif second_pick <= 359186: second_ability = "마력: +12"
    elif second_pick <= 408166: second_ability = "STR: +3%"
    elif second_pick <= 457146: second_ability = "DEX: +3%"
    elif second_pick <= 506126: second_ability = "INT: +3%"
    elif second_pick <= 555106: second_ability = "LUK: +3%"
    elif second_pick <= 571433: second_ability = "공격력: +3%"
    elif second_pick <= 587760: second_ability = "마력: +3%"
    elif second_pick <= 604087: second_ability = "크리티컬 확률: +4%"
    elif second_pick <= 620414: second_ability = "데미지: +3%"
    elif second_pick <= 653067: second_ability = "올스탯: +5"
    elif second_pick <= 669394: second_ability = "공격 시 20% 확률로 240의 HP 회복"
    elif second_pick <= 685721: second_ability = "공격 시 20% 확률로 120의 MP 회복"
    elif second_pick <= 702048: second_ability = "공격 시 20% 확률로 6레벨 중독효과 적용"
    elif second_pick <= 718375: second_ability = "공격 시 10% 확률로 2레벨 기절효과 적용"
    elif second_pick <= 734702: second_ability = "공격 시 20% 확률로 2레벨 슬로우효과 적용"
    elif second_pick <= 751029: second_ability = "공격 시 20% 확률로 3레벨 암흑효과 적용"
    elif second_pick <= 767356: second_ability = "공격 시 10% 확률로 2레벨 빙결효과 적용"
    elif second_pick <= 783683: second_ability = "공격 시 10% 확률로 2레벨 봉인효과 적용"
    elif second_pick <= 800010: second_ability = "몬스터 방어율 무시: +15%"
    elif second_pick <= 821749: second_ability = "STR: +6%"
    elif second_pick <= 843488: second_ability = "DEX: +6%"
    elif second_pick <= 865227: second_ability = "INT: +6%"
    elif second_pick <= 886966: second_ability = "LUK: +6%"
    elif second_pick <= 908705: second_ability = "최대 HP: +6%"
    elif second_pick <= 930444: second_ability = "최대 MP: +6%"
    elif second_pick <= 939140: second_ability = "공격력: +6%"
    elif second_pick <= 947836: second_ability = "마력: +6%"
    elif second_pick <= 956532: second_ability = "크리티컬 확률: +8%"
    elif second_pick <= 965228: second_ability = "데미지: +6%"
    elif second_pick <= 973924: second_ability = "올스탯: +3%"
    elif second_pick <= 982620: second_ability = "공격 시 20% 확률로 360의 HP 회복"
    elif second_pick <= 991316: second_ability = "공격 시 20% 확률로 180의 HP 회복"
    else: second_ability = "몬스터 방어율 무시: +15%"  # 1000012

    if third_pick <= 58163: third_ability = "STR: +12"
    elif third_pick <= 116326: third_ability = "DEX: +12"
    elif third_pick <= 174489: third_ability = "INT: +12"
    elif third_pick <= 232652: third_ability = "LUK: +12"
    elif third_pick <= 290815: third_ability = "최대 HP: +120"
    elif third_pick <= 348978: third_ability = "최대 MP: +120"
    elif third_pick <= 387754: third_ability = "공격력: +12"
    elif third_pick <= 426530: third_ability = "마력: +12"
    elif third_pick <= 484693: third_ability = "STR: +3%"
    elif third_pick <= 542856: third_ability = "DEX: +3%"
    elif third_pick <= 601019: third_ability = "INT: +3%"
    elif third_pick <= 659182: third_ability = "LUK: +3%"
    elif third_pick <= 678570: third_ability = "공격력: +3%"
    elif third_pick <= 697958: third_ability = "마력: +3%"
    elif third_pick <= 717346: third_ability = "크리티컬 확률: +4%"
    elif third_pick <= 736734: third_ability = "데미지: +3%"
    elif third_pick <= 775510: third_ability = "올스탯: +5"
    elif third_pick <= 794898: third_ability = "공격 시 20% 확률로 240의 HP 회복"
    elif third_pick <= 814286: third_ability = "공격 시 20% 확률로 120의 MP 회복"
    elif third_pick <= 833674: third_ability = "공격 시 20% 확률로 6레벨 중독효과 적용"
    elif third_pick <= 853062: third_ability = "공격 시 10% 확률로 2레벨 기절효과 적용"
    elif third_pick <= 872450: third_ability = "공격 시 20% 확률로 2레벨 슬로우효과 적용"
    elif third_pick <= 891838: third_ability = "공격 시 20% 확률로 3레벨 암흑효과 적용"
    elif third_pick <= 911226: third_ability = "공격 시 10% 확률로 2레벨 빙결효과 적용"
    elif third_pick <= 930614: third_ability = "공격 시 10% 확률로 2레벨 봉인효과 적용"
    elif third_pick <= 950002: third_ability = "몬스터 방어율 무시: +15%"
    elif third_pick <= 955437: third_ability = "STR: +6%"
    elif third_pick <= 960872: third_ability = "DEX: +6%"
    elif third_pick <= 966307: third_ability = "INT: +6%"
    elif third_pick <= 971742: third_ability = "LUK: +6%"
    elif third_pick <= 977177: third_ability = "최대 HP: +6%"
    elif third_pick <= 982612: third_ability = "최대 MP: +6%"
    elif third_pick <= 984786: third_ability = "공격력: +6%"
    elif third_pick <= 986960: third_ability = "마력: +6%"
    elif third_pick <= 989134: third_ability = "크리티컬 확률: +8%"
    elif third_pick <= 991308: third_ability = "데미지: +6%"
    elif third_pick <= 993482: third_ability = "올스탯: +3%"
    elif third_pick <= 995656: third_ability = "공격 시 20% 확률로 360의 HP 회복"
    elif third_pick <= 997830: third_ability = "공격 시 20% 확률로 180의 HP 회복"
    else: third_ability = "몬스터 방어율 무시: +15%"  # 1000004


def black_cube_unique():
    global first_ability, second_ability, third_ability

    first_pick = random.randint(1, 1000000)
    second_pick = random.randint(1, 1000000)
    third_pick = random.randint(1, 1000000)

    if first_pick <= 111111: first_ability = "STR: +9%"
    elif first_pick <= 222222: first_ability = "DEX: +9%"
    elif first_pick <= 333333: first_ability = "INT: +9%"
    elif first_pick <= 444444: first_ability = "LUK: +9%"
    elif first_pick <= 511111: first_ability = "공격력: +9%"
    elif first_pick <= 577778: first_ability = "마력: +9%"
    elif first_pick <= 666667: first_ability = "크리티컬 확률: +9%"
    elif first_pick <= 733334: first_ability = "데미지: +9%"
    elif first_pick <= 822223: first_ability = "올스탯: +6%"
    elif first_pick <= 888890: first_ability = "몬스터 방어율 무시: +30%"
    elif first_pick <= 955557: first_ability = "보스 몬스터 공격 시 데미지: +20%"
    else: first_ability = "보스 몬스터 공격 시 데미지: +30%"  # 1000001

    if second_pick <= 86957: second_ability = "STR: +6%"
    elif second_pick <= 173914: second_ability = "DEX: +6%"
    elif second_pick <= 260871: second_ability = "INT: +6%"
    elif second_pick <= 347828: second_ability = "LUK: +6%"
    elif second_pick <= 434785: second_ability = "최대 HP: +6%"
    elif second_pick <= 521742: second_ability = "최대 MP: +6%"
    elif second_pick <= 556525: second_ability = "공격력: +6%"
    elif second_pick <= 591308: second_ability = "마력: +6%"
    elif second_pick <= 626091: second_ability = "크리티컬 확률: +8%"
    elif second_pick <= 660874: second_ability = "데미지: +6%"
    elif second_pick <= 695657: second_ability = "올스탯: +3%"
    elif second_pick <= 730440: second_ability = "공격 시 20% 확률로 360의 HP 회복"
    elif second_pick <= 765223: second_ability = "공격 시 20% 확률로 180의 HP 회복"
    elif second_pick <= 800006: second_ability = "몬스터 방어율 무시: +15%"
    elif second_pick <= 822228: second_ability = "STR: +9%"
    elif second_pick <= 844450: second_ability = "DEX: +9%"
    elif second_pick <= 866672: second_ability = "INT: +9%"
    elif second_pick <= 888894: second_ability = "LUK: +9%"
    elif second_pick <= 902227: second_ability = "공격력: +9%"
    elif second_pick <= 915560: second_ability = "마력: +9%"
    elif second_pick <= 933338: second_ability = "크리티컬 확률: +9%"
    elif second_pick <= 946671: second_ability = "데미지: +9%"
    elif second_pick <= 964449: second_ability = "올스탯: +6%"
    elif second_pick <= 977782: second_ability = "몬스터 방어율 무시: +30%"
    elif second_pick <= 991115: second_ability = "보스 몬스터 공격 시 데미지: +20%"
    else: second_ability = "보스 몬스터 공격 시 데미지: +30%"  # 1000004

    if third_pick <= 103261: third_ability = "STR: +6%"
    elif third_pick <= 206522: third_ability = "DEX: +6%"
    elif third_pick <= 309783: third_ability = "INT: +6%"
    elif third_pick <= 413044: third_ability = "LUK: +6%"
    elif third_pick <= 516305: third_ability = "최대 HP: +6%"
    elif third_pick <= 619566: third_ability = "최대 MP: +6%"
    elif third_pick <= 660870: third_ability = "공격력: +6%"
    elif third_pick <= 702174: third_ability = "마력: +6%"
    elif third_pick <= 743478: third_ability = "크리티컬 확률: +8%"
    elif third_pick <= 784782: third_ability = "데미지: +6%"
    elif third_pick <= 826086: third_ability = "올스탯: +3%"
    elif third_pick <= 867390: third_ability = "공격 시 20% 확률로 360의 HP 회복"
    elif third_pick <= 908694: third_ability = "공격 시 20% 확률로 180의 HP 회복"
    elif third_pick <= 949998: third_ability = "몬스터 방어율 무시: +15%"
    elif third_pick <= 955554: third_ability = "STR: +9%"
    elif third_pick <= 961110: third_ability = "DEX: +9%"
    elif third_pick <= 966666: third_ability = "INT: +9%"
    elif third_pick <= 972222: third_ability = "LUK: +9%"
    elif third_pick <= 975555: third_ability = "공격력: +9%"
    elif third_pick <= 978888: third_ability = "마력: +9%"
    elif third_pick <= 983332: third_ability = "크리티컬 확률: +9%"
    elif third_pick <= 986665: third_ability = "데미지: +9%"
    elif third_pick <= 991109: third_ability = "올스탯: +6%"
    elif third_pick <= 994442: third_ability = "몬스터 방어율 무시: +30%"
    elif third_pick <= 997775: third_ability = "보스 몬스터 공격 시 데미지: +20%"
    else: third_ability = "보스 몬스터 공격 시 데미지: +30%"  # 999997


def black_cube_legendary():
    global first_ability, second_ability, third_ability

    first_pick = random.randint(1, 1000000)
    second_pick = random.randint(1, 1000000)
    third_pick = random.randint(1, 1000000)

    if first_pick <= 97561: first_ability = "STR: +12%"
    elif first_pick <= 195122: first_ability = "DEX: +12%"
    elif first_pick <= 292683: first_ability = "INT: +12%"
    elif first_pick <= 390244: first_ability = "LUK: +12%"
    elif first_pick <= 439024: first_ability = "공격력: +12%"
    elif first_pick <= 487804: first_ability = "마력: +12%"
    elif first_pick <= 536584: first_ability = "크리티컬 확률: +12%"
    elif first_pick <= 585364: first_ability = "데미지: +12%"
    elif first_pick <= 658535: first_ability = "올스탯: +9%"
    elif first_pick <= 707315: first_ability = "캐릭터 기준 10레벨 당 공격력: +1"
    elif first_pick <= 756095: first_ability = "캐릭터 기준 10레벨 당 마력: +1"
    elif first_pick <= 804875: first_ability = "몬스터 방어율 무시: +35%"
    elif first_pick <= 853655: first_ability = "몬스터 방어율 무시: +40%"
    elif first_pick <= 902435: first_ability = "보스 몬스터 공격 시 데미지: +30%"
    elif first_pick <= 951215: first_ability = "보스 몬스터 공격 시 데미지: +35%"
    else: first_ability = "보스 몬스터 공격 시 데미지: +40%"  # 999995

    if second_pick <= 88889: second_ability = "STR: +9%"
    elif second_pick <= 177778: second_ability = "DEX: +9%"
    elif second_pick <= 266667: second_ability = "INT: +9%"
    elif second_pick <= 355556: second_ability = "LUK: +9%"
    elif second_pick <= 408889: second_ability = "공격력: +9%"
    elif second_pick <= 462222: second_ability = "마력: +9%"
    elif second_pick <= 533333: second_ability = "크리티컬 확률: +9%"
    elif second_pick <= 586666: second_ability = "데미지: +9%"
    elif second_pick <= 657777: second_ability = "올스탯: +6%"
    elif second_pick <= 711110: second_ability = "몬스터 방어율 무시: +30%"
    elif second_pick <= 764443: second_ability = "보스 몬스터 공격 시 데미지: +20%"
    elif second_pick <= 799999: second_ability = "보스 몬스터 공격 시 데미지: +30%"
    elif second_pick <= 819511: second_ability = "STR: +12%"
    elif second_pick <= 839023: second_ability = "DEX: +12%"
    elif second_pick <= 858535: second_ability = "INT: +12%"
    elif second_pick <= 878047: second_ability = "LUK: +12%"
    elif second_pick <= 887803: second_ability = "공격력: +12%"
    elif second_pick <= 897559: second_ability = "마력: +12%"
    elif second_pick <= 907315: second_ability = "크리티컬 확률: +12%"
    elif second_pick <= 917071: second_ability = "데미지: +12%"
    elif second_pick <= 931705: second_ability = "올스탯: +9%"
    elif second_pick <= 941461: second_ability = "캐릭터 기준 10레벨 당 공격력: +1"
    elif second_pick <= 951217: second_ability = "캐릭터 기준 10레벨 당 마력: +1"
    elif second_pick <= 960973: second_ability = "몬스터 방어율 무시: +35%"
    elif second_pick <= 970729: second_ability = "몬스터 방어율 무시: +40%"
    elif second_pick <= 980485: second_ability = "보스 몬스터 공격 시 데미지: +30%"
    elif second_pick <= 990241: second_ability = "보스 몬스터 공격 시 데미지: +35%"
    else: second_ability = "보스 몬스터 공격 시 데미지: +40%"  # 999997

    if third_pick <= 105556: third_ability = "STR: +9%"
    elif third_pick <= 211112: third_ability = "DEX: +9%"
    elif third_pick <= 316668: third_ability = "INT: +9%"
    elif third_pick <= 422224: third_ability = "LUK: +9%"
    elif third_pick <= 485557: third_ability = "공격력: +9%"
    elif third_pick <= 548890: third_ability = "마력: +9%"
    elif third_pick <= 633334: third_ability = "크리티컬 확률: +9%"
    elif third_pick <= 696667: third_ability = "데미지: +9%"
    elif third_pick <= 781111: third_ability = "올스탯: +6%"
    elif third_pick <= 844444: third_ability = "몬스터 방어율 무시: +30%"
    elif third_pick <= 907777: third_ability = "보스 몬스터 공격 시 데미지: +20%"
    elif third_pick <= 949999: third_ability = "보스 몬스터 공격 시 데미지: +30%"
    elif third_pick <= 954877: third_ability = "STR: +12%"
    elif third_pick <= 959755: third_ability = "DEX: +12%"
    elif third_pick <= 964633: third_ability = "INT: +12%"
    elif third_pick <= 969511: third_ability = "LUK: +12%"
    elif third_pick <= 971950: third_ability = "공격력: +12%"
    elif third_pick <= 974389: third_ability = "마력: +12%"
    elif third_pick <= 976828: third_ability = "크리티컬 확률: +12%"
    elif third_pick <= 979267: third_ability = "데미지: +12%"
    elif third_pick <= 982926: third_ability = "올스탯: +9%"
    elif third_pick <= 985365: third_ability = "캐릭터 기준 10레벨 당 공격력: +1"
    elif third_pick <= 987804: third_ability = "캐릭터 기준 10레벨 당 마력: +1"
    elif third_pick <= 990243: third_ability = "몬스터 방어율 무시: +35%"
    elif third_pick <= 992682: third_ability = "몬스터 방어율 무시: +40%"
    elif third_pick <= 995121: third_ability = "보스 몬스터 공격 시 데미지: +30%"
    elif third_pick <= 997560: third_ability = "보스 몬스터 공격 시 데미지: +35%"
    else: third_ability = "보스 몬스터 공격 시 데미지: +40%"  # 999999


@client.command()
async def cube(ctx):
    filename = "your_item.txt"
    file_exist = os.path.isfile(filename)
    if file_exist:
        with open(filename) as file_object:
            item = file_object.read()
            item_info = item.split("|")
    else:
        with open(filename, 'w') as file_object:
            file_object.write("rare|0|0")

    promote = random.randint(1, 1000)
    if item_info[0] == "rare" and promote <= 150:
        item_info[0] = "epic"
        await ctx.send("등급이 에픽으로 상승했습니다!")
    elif item_info[0] == "epic" and promote <= 35:
        item_info[0] = "unique"
        await ctx.send("등급이 유니크로 상승했습니다!")
    elif item_info[0] == "unique" and promote <= 10:
        item_info[0] = "legendary"
        await ctx.send("등급이 레전더리로 상승했습니다!")

    if item_info[0] == "rare":
        black_cube_rare()
        rarity = "레어"
        # await ctx.send(f"<:rare_item:819546815820202026>")
    elif item_info[0] == "epic":
        black_cube_epic()
        rarity = "에픽"
        # await ctx.send(f"<:epic_item:819546815850217503>")
    elif item_info[0] == "unique":
        black_cube_unique()
        rarity = "유니크"
        # await ctx.send(f"<:unique_item:819546815909199902>")
    elif item_info[0] == "legendary":
        black_cube_legendary()
        rarity = "레전더리"
        # await ctx.send(f"<:legendary_item:819546815464603659>")

    item_info[1] = int(item_info[1])
    item_info[2] = int(item_info[2])
    item_info[1] += 1
    item_info[2] = ((item_info[1] // 12) + 1) * 19800

    # embed = discord.Embed(description="asdf", image="maple_cube/legendary_item.png")
    # await ctx.send(embed=embed)
    await ctx.send(f"등급: {rarity}\n\n"
                   f"{first_ability}\n{second_ability}\n{third_ability}\n\n"
                   f"소비한 큐브 수: {item_info[1]}\n삭제된 금액: -{item_info[2]}")

    with open(filename, 'w') as file_object:
        file_object.write(f"{item_info[0]}|{item_info[1]}|{item_info[2]}")


class User:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = list()


def sutda_draw():
    your_hand = list()
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    for i in range(2):  # 중복 제거
        draw = random.choice(num_list)
        if your_hand:
            for check_duplicate in your_hand:
                if draw == check_duplicate:
                    while True:
                        draw = random.choice(num_list)
                        if draw != check_duplicate:
                            break
        your_hand.append(draw)

    your_hand.sort()

    return your_hand


def sutda_calc(your_hand, players=""):
    score_check = list()

    for hand in your_hand:
        card_month = math.floor((hand + 1) / 2)  # 패의 月 종류를 반환
        score_check.append(card_month)

    if score_check[0] == score_check[1]:
        if score_check[0] == 1:
            score_info = "1땡 입니다!"
            score_code = 21
        elif score_check[0] == 2:
            score_info = "2땡 입니다!"
            score_code = 22
        elif score_check[0] == 3:
            score_info = "3땡 입니다!"
            score_code = 23
        elif score_check[0] == 4:
            score_info = "4땡 입니다!"
            score_code = 24
        elif score_check[0] == 5:
            score_info = "5땡 입니다!"
            score_code = 25
        elif score_check[0] == 6:
            score_info = "6땡 입니다!"
            score_code = 26
        elif score_check[0] == 7:
            score_info = "7땡 입니다!"
            score_code = 27
        elif score_check[0] == 8:
            score_info = "8땡 입니다!"
            score_code = 28
        elif score_check[0] == 9:
            score_info = "9땡 입니다!"
            score_code = 29
        elif score_check[0] == 10:
            score_info = "장땡 입니다!"
            score_code = 30
    else:
        if score_check[0] == 4 and score_check[1] == 6:
            score_info = "세륙 입니다!"
            score_code = 11
        elif score_check[0] == 4 and score_check[1] == 10:
            score_info = "장사 입니다!"
            score_code = 12
        elif score_check[0] == 1 and score_check[1] == 10:
            score_info = "장삥 입니다!"
            score_code = 13
        elif score_check[0] == 1 and score_check[1] == 9:
            score_info = "구삥 입니다!"
            score_code = 14
        elif score_check[0] == 1 and score_check[1] == 4:
            score_info = "독사 입니다!"
            score_code = 15
        elif score_check[0] == 1 and score_check[1] == 2:
            score_info = "알리 입니다!"
            score_code = 16
        elif score_check[0] == 4 and score_check[1] == 9:
            score_info = "구사 입니다."
            score_code = -1
        elif score_check[0] == 3 and score_check[1] == 7:
            score_info = "땡잡이 입니다."
            score_code = -3
        else:
            ggut = score_check[1] + score_check[0]
            if ggut == 9 or ggut == 19:
                score_info = "갑오 입니다."
                score_code = 9
            elif ggut == 10:
                score_info = "망통 입니다."
                score_code = 0
            else:
                if ggut >= 11:
                    score_info = f"{ggut - 10}끗 입니다."
                    score_code = ggut - 10
                else:
                    score_info = f"{ggut}끗 입니다."
                    score_code = ggut

    if your_hand[0] == 5 and your_hand[1] == 15:
        score_info = "38광땡 입니다!!!"
        score_code = 33
    elif your_hand[0] == 1 and your_hand[1] == 15:
        score_info = "18광땡 입니다!!"
        score_code = 32
    elif your_hand[0] == 1 and your_hand[1] == 5:
        score_info = "13광땡 입니다!!"
        score_code = 31
    elif your_hand[0] == 7 and your_hand[1] == 17:
        score_info = "멍텅구리구사 입니다."
        score_code = -2
    elif your_hand[0] == 7 and your_hand[1] == 13:
        score_info = "암행어사 입니다."
        score_code = -4

    if players:
        return score_code
    else:
        return score_info


def special_score_compare(score_list):  # 특수 승리 판별기
    is_94 = False
    is_super94 = False
    is_37 = False
    is_47 = False
    is_21 = False  # 땡잡이
    is_30 = False  # 장땡
    is_31 = False  # 암행어사
    result = 0
    index_94, index_super94, index_37, index_47 = 0, 0, 0, 0

    for score in score_list:
        if score == -1:
            is_94 = True
        elif score == -2:
            is_super94 = True
        elif score == -3:
            is_37 = True
            index_37 = score_list.index(score)
        elif score == -4:
            is_47 = True
            index_47 = score_list.index(score)
        elif 20 <= score < 30:
            is_21 = True
        elif score == 30:
            is_30 = True
        elif 30 < score < 33:
            is_31 = True

    if not is_21 and not is_30 and not is_31 and is_94:  # 땡 이상이 없고 구사가 나오면
        result = -1
    elif is_21 and not is_30 and not is_31 and is_super94:  # 장땡 이상이 없고 멍구사가 나오면
        result = -1
    elif is_21 and is_37:  # 1~9땡이 나오고 땡잡이가 나오면
        result = index_37  # 땡잡이의 위치
    elif is_31 and is_47:  # 광땡이 나오고 암행어사가 나오면
        result = index_47  # 암행어사의 위치

    return result


@client.command()
async def sutda(ctx, *, players=""):
    info_list = list()
    score_list = list()
    special, winner = 0, 0
    if players:
        player_list = players.split(" ")
        for element in player_list:
            info_list.append(User(element))

    print_hand = ""
    card_list = {1: "<:sutda1:806271821053820989>", 2: "<:sutda2:806271853651820575>",
                 3: "<:sutda3:806271867366932480>", 4: "<:sutda4:806271880617132052>",
                 5: "<:sutda5:806271895582277672>", 6: "<:sutda6:806271906977939498>",
                 7: "<:sutda7:806271919329378405>", 8: "<:sutda8:806271932751151125>",
                 9: "<:sutda9:806271945745891338>", 10: "<:sutda10:806271958735257620>",
                 11: "<:sutda11:806271976095350816>", 12: "<:sutda12:806272002407137303>",
                 13: "<:sutda13:806272016217931787>", 14: "<:sutda14:806272029795811335>",
                 15: "<:sutda15:806272053296627713>", 16: "<:sutda16:806272067158671433>",
                 17: "<:sutda17:806272081855250493>", 18: "<:sutda18:806272096358498335>",
                 19: "<:sutda19:806272112926261312>", 20: "<:sutda20:806272136717140019>"}

    if players:
        for info in info_list:
            info.hand = sutda_draw()
            for card in info.hand:
                del card_list[card]
            info.score = sutda_calc(info.hand, "true")
            score_list.append(info.score)

        special = special_score_compare(score_list)
        if special:
            pass
        else:
            for element in score_list:
                if winner < element:
                    winner = element
        # 프린트해주고
        # 누가 우승인지 출력하면 끝
    else:
        your_hand = sutda_draw()
        score = sutda_calc(your_hand)
        for card in your_hand:
            print_hand += (card_list[card])
            del card_list[card]
        await ctx.send(print_hand.rstrip())
        await ctx.send(score)


@client.command()
async def tanto(ctx):
    await ctx.send(file=discord.File("tanto.jpg"))


@client.command()
async def random_pic(ctx):
    pic_list = ["rand_img/image1.jpg", "rand_img/image2.jpg", "rand_img/image3.jpg", "rand_img/image4.jpg",
                "rand_img/image6.png", "rand_img/image7.jpg", "rand_img/image8.png",
                "rand_img/image9.jpg", "rand_img/image11.jpg", "rand_img/image12.jpg",
                "rand_img/image13.gif", "rand_img/image15.jpeg", "rand_img/image16.jpg",
                "rand_img/image17.png", "rand_img/image18.png", "rand_img/image19.jpg"]
    geki_rare = random.randint(1, 1000)
    if geki_rare % 100 == 0:  # 100 분의 1 확률로 희귀 짤
        await ctx.send(content="와! 1% 확률의 이미지를 뽑았어요!",
                       file=discord.File("rand_img/geki_rare.jpg"))
    elif geki_rare == 1:  # 1000 분의 1 확률로 숨겨진 짤
        await ctx.send(content="축하해요!! 0.1% 확률의 숨겨진 이미지를 뽑았어요!!",
                       file=discord.File("rand_img/geki_atsu.jpg"))
    else:
        await ctx.send(file=discord.File(random.choice(pic_list)))


@client.command()
async def dice(ctx, number, number_2=0):
    try:
        number = int(number)
        number_2 = int(number_2)
        if number_2:
            if number > number_2:
                temp = number
                number = number_2
                number_2 = temp
            await ctx.send(f"{number}부터 {number_2}사이의 랜덤한 수를 출력합니다.\n"
                           f"{random.randint(number, number_2)}이(가) 나왔습니다!")
        else:
            await ctx.send(f"1부터 {number}사이의 랜덤한 수를 출력합니다.\n"
                           f"{random.randint(1, number)}이(가) 나왔습니다!")
    except:
        await ctx.send(f"올바른 값을 입력해주세요!")


@client.command()
async def imo(ctx, time):
    filename = "imo_time.txt"
    if time == "check":
        file_exist = os.path.isfile(filename)
        if file_exist:
            with open(filename) as file_object:
                content = file_object.read()
            time_list = content.split(":")
            await ctx.send(f"다음 젠 타임은 {time_list[0]}시 {time_list[1]}분 {time_list[2]}초 입니다.")
        else:
            await ctx.send("기록해놓은 젠 타임이 없어요!")
        return

    auth = check_authorization(ctx)
    if not auth:
        await ctx.send(f"{ctx.author.mention} 커맨드 사용 권한이 없습니다!")
        return

    now = datetime.today()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")

    hour = int(hour)
    minute = int(minute)
    second = int(second)
    time = int(time)

    if (minute + time) >= 60:
        plus_hour = (minute + time) // 60
        nokori_minute = (minute + time) % 60
        hour += plus_hour
        minute = nokori_minute
    else:
        minute += time

    with open(filename, 'w') as file_object:
        file_object.write(f"{hour}:{minute}:{second}")
        # if mob_name:
        #     file_object.write(f",{mob_name}")

    # if mob_name:
    #     await ctx.send(f"{mob_name}의 다음 젠 타임은 {hour}시 {minute}분 {second}초 입니다.")
    await ctx.send(f"다음 젠 타임은 {hour}시 {minute}분 {second}초 입니다.")


@client.command()
async def calc(ctx, *, formula):
    formula = formula.replace(" ", "")
    flag = True
    error = False
    point_detect = False
    index, result, i, start_point, last_point = 0, 0, 0, 0, 0
    p = re.compile('[^0-9]')    # 숫자인지 기호인지 판별하는 정규표현식 ^: not

    for element in formula:     # 한글자씩 순서대로 판별
        m = p.match(element)
        if m:
            if element == ".":  # 소수점을 감지
                point_detect = True
                continue
            index = formula.index(element, start_point, len(formula))  # operator의 위치

            if not index:   # operator의 위치가 0이라면
                error = True
                await ctx.send("잘못된 수식을 입력하셨습니다!")
                break

            if flag:
                if point_detect:
                    result = float(formula[start_point:index])
                    point_detect = False
                else:
                    result = int(formula[start_point:index])    # 첫 operand를 result에 대입
            start_point = index + 1     # 다음 operand의 시작지점
            flag = False

            for check in formula[start_point:]:     # 추가적인 operator가 있는가?
                n = p.match(check)
                if n and check != ".":
                    last_point = formula.index(check, start_point, len(formula))    # 다음 operand의 종료지점
                    break
                if check == ".":
                    point_detect = True
                last_point = len(formula)   # 만약에 추가적인 operator가 없다면 종료지점은 수식의 끝부분과 같음

            # result 값에 다음 operand를 연산, 소수의 경우 float로 연산
            if formula[index] == "+":
                if point_detect:
                    result += float(formula[start_point:last_point])
                    point_detect = False
                else:
                    result += int(formula[start_point:last_point])
            elif formula[index] == "-":
                if point_detect:
                    result -= float(formula[start_point:last_point])
                    point_detect = False
                else:
                    result -= int(formula[start_point:last_point])
            elif formula[index] == "*":
                if point_detect:
                    result *= float(formula[start_point:last_point])
                    point_detect = False
                else:
                    result *= int(formula[start_point:last_point])
            elif formula[index] == "/":
                if point_detect:
                    result /= float(formula[start_point:last_point])
                    point_detect = False
                else:
                    result /= int(formula[start_point:last_point])
            elif formula[index] == "^":
                if point_detect:
                    result **= float(formula[start_point:last_point])
                    point_detect = False
                else:
                    result **= int(formula[start_point:last_point])
            else:
                error = True  # 설정된 operator이외의 연산자가 나오면 error로 판별
                await ctx.send("잘못된 수식을 입력하셨습니다!")
                break

    if not error:  # error가 검출되지 않았다면 결과값을 정상적으로 출력
        if not index:   # 수식의 요소가 operand 단 하나 인경우
            result = formula
        if not index and point_detect:  # 수식이 .XXX 이나 XXX. operand 단 하나 인경우
            result = float(formula)
        await ctx.send(result)


@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = ctx.guild.owner
    id = ctx.guild.id
    region = ctx.guild.region
    member_count = ctx.guild.member_count
    created_at = str(ctx.guild.created_at)

    icon = ctx.guild.icon_url

    embed = discord.Embed(
        title=name + " 서버 정보",
        # description=description,
        color=discord.Color.teal()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="서버 ID", value=id, inline=True)
    embed.add_field(name="👑관리자", value=owner, inline=True)
    embed.add_field(name="🌍지역", value=region, inline=True)
    embed.add_field(name="👥멤버 수", value=member_count, inline=True)
    embed.add_field(name="📆만들어진 날짜", value=created_at[:10], inline=True)

    await ctx.send(embed=embed)


@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        await ctx.send("봇이 이미 다른 음성 채널에서 재생중입니다!")
        return

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f"{channel} 채널에 들어왔어요!")
        print(f"client has connected to {channel} channel.")


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Byebye 👋")
        print(f"client has left from {channel} channel.")
    else:
        await ctx.send("저는 어떤 음성 채널에도 들어가 있지 않아요!")


youtube_queue = {}
music_title = {}


@client.command()
async def play(ctx, url: str):
    def chk_queue():
        queue_exist = os.path.isdir("./queue")
        if queue_exist is True:
            dir = os.path.abspath(os.path.realpath("queue"))
            length = len(os.listdir(dir))
            still_queue = length - 1  # queue에 남아있는 곡들의 수
            try:
                first_file = os.listdir(dir)[0]
            except:
                youtube_queue.clear()
                return
            main_loc = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("queue") + "\\" + first_file)

            if length != 0:
                print("Bot Status: Playing next queued")
                print(f"Bot Status: {still_queue} song(s) still exist")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_loc)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: chk_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.5
            else:
                youtube_queue.clear()
                return
        else:
            youtube_queue.clear()
            print("Bot Status: No songs were exist in queue")

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not (voice and voice.is_connected()):
        await join(ctx)
        await play(ctx, url)
        return
        # await ctx.send("현재 봇이 어느 음성 채널에도 참여하지 않았습니다.")

    song_exist = os.path.isfile("song.mp3")
    try:
        if song_exist:
            os.remove("song.mp3")
            youtube_queue.clear()
    except PermissionError:
        await queue(ctx, url)
        # await ctx.send("음악이 이미 재생중입니다!")
        return

    queue_infile = os.path.isdir("./queue")
    try:
        queue_folder = "./queue"
        if queue_infile is True:
            print("Bot Status: Remove old queue folder")
            shutil.rmtree(queue_folder)
    except:
        print("No old queue folder")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Bot Status:Downloading audio")
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Bot Status: {file} renamed")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: chk_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    new_name = name.rsplit("-", 2)
    await ctx.send(f":headphones:현재 재생중 : {new_name[0]}")
    print(f"Bot Status: Now playing {new_name[0]}")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        await ctx.send("현재 음악이 일시정지 상태입니다!")
        return
    if voice and voice.is_playing():
        print("Bot Status: Music passed")
        voice.pause()
        await ctx.send("음악을 일시정지합니다.")
    else:
        await ctx.send("현재 음악을 재생하고 있지 않습니다!")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        await ctx.send("음악이 이미 재생중입니다!")
        return
    if voice and voice.is_paused():
        print("Bot Status: Music resumed")
        voice.resume()
        await ctx.send("음악을 다시 재생합니다.")
    else:
        await ctx.send("현재 음악을 재생하고 있지 않습니다!")


@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    youtube_queue.clear()

    if voice and voice.is_playing():
        print("Bot Status: Music Skipped")
        voice.stop()
        await ctx.send("현재 음악을 스킵합니다.")
    else:
        await ctx.send("현재 음악을 재생하고 있지 않습니다!")


@client.command()
async def queue(ctx, url: str):
    queue_exist = os.path.isdir("./queue")
    if queue_exist is False:
        os.mkdir("queue")
    dir = os.path.abspath(os.path.realpath("queue"))
    queue_num = len(os.listdir(dir))
    queue_num += 1
    add_queue = True
    while add_queue:
        if queue_num in youtube_queue:
            queue_num += 1
        else:
            add_queue = False
            youtube_queue[queue_num] = queue_num

    # music_title.append()
    dir_queue = os.path.abspath(os.path.realpath("queue") + f"\song{queue_num}.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': dir_queue,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Bot Status: Downloading audio")
        ydl.download([url])
    await ctx.send("대기 목록에 음악이 성공적으로 추가되었습니다!")  # 곧 삭제할것(임시방편)
    # await ctx.send("현재 대기중인 음악 수: " + str(queue_num))
    print("Bot Status: Song added to queue")


TOKEN = 'Token name'

client.run(TOKEN)
