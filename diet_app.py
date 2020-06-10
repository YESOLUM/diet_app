class User:
    activity_step = (27.5, 32.5, 37.5, 40)
    activity_notification = """가벼운 활동(앉아서 하는 일. 일반사무/관리, 자녀 없는 주부) : 27.5
중등도 활동(서서 하는 일. 서비스업. 판매. 제조/가공. 어린 자녀 있는 주부) : 32.5
강한 활동(활동량 많은 일. 농업/어업/건설/축산업) : 37.5
아주 강한 활동(운동선수. 임업. 농번기의 농사) : 40
"""

    @classmethod
    def choice_max(cls, args):
        record_idx = 0
        record_val = args[record_idx]
        for i, arg in enumerate(args):
            if arg > record_val:
                record_idx = i
                record_val = arg
        return record_idx

    def __init__(self, nick=None, tall=None, gender=None, is_diet=None):
        self.nick = nick
        self.tall = tall
        self.gender = gender
        self.is_diet = is_diet
        if self.gender == "male":
            self.stan_weight = (self.tall *0.01) ** 2 * 22
        else:
            self.stan_weight = (self.tall *0.01) ** 2 * 21
        self.act = None
        self.day_kc = None
        self.day_car = None
        self.day_pr = None
        self.day_li = None

    def set_daily(self, is_diet=None, act=None):
        self.is_diet = is_diet
        self.act = act
        if self.is_diet:
            self.day_kc = self.stan_weight * User.activity_step[act - 1]
        else:
            self.day_kc = self.stan_weight * User.activity_step[act - 1] - 250

        if self.is_diet:
            self.day_car = self.day_kc * 0.3
            self.day_pr = self.day_kc * 0.4
            self.day_li = self.day_kc * 0.3
        else:
            self.day_car = self.day_kc * 0.5
            self.day_pr = self.day_kc * 0.3
            self.day_li = self.day_kc * 0.2


        time = input("How much did you sleep last night?")
        if float(time) <= 6:
            print( "깨어있는 시간이 길수록 고칼로리 야식 섭취가 많다는 연구결과가 있어요."
                   "하루 6시간 보다 적게 잘 경우 식욕 호르몬인 그렐린이 늘고 인슐린 민감성이 줄어들며"
                   " 식욕 억제 호르몬인 렙틴이 감소하는 경향이 있답니다."
                   "잠이 부족하면 뇌의 전두엽 활동이 둔화되기 때문에 합리적인 의사결정을 내리기 어려워지고 "
                   "자극적인 음식을 찾게 되요."
                   "오늘 밤 수면시간은 꼭 6시간을 넘겨주시고, 양질의 숙면을 취해주세요."
                   "수면부족인 오늘! 칼로리가 낮고 포만감이 높은 음식을 섭취하는 것이 좋습니다."
                   "콩, 계란, 버섯, 시금치, 키위, 두부, 닭가슴살 등 건강한 음식을 추천합니다!")
        if 9 > float(time) > 6:
            print("적정 수면시간을 지키셨네요! 축하드립니다 (짝짝짝)"
                   "우리 같이 오늘 하루도 건강한 하루를 만들어 봐요!")

        if float(time) >= 9:
            print("피곤하셨군요! 조금 많은 수면시간을 취했지만 괜찮아요! 덕분에 피로가 풀렸다면요ㅎㅎ"
                  "오늘은 다른 날 보다 더 힘찬 하루를 보내시기를 바래요!"
                  "만약 여전히 피곤하다면 오늘은 양질의 수면을 7시간 정도 취해보는 건 어떨까요? 취침 전 따뜻한 우유 반 컵을 마시고 핸드폰은 저~ 멀리 둔 뒤에 불을 끄고 바른 자세로 침대에 누워주세요")


    def set_current(self, menus):
        menu = input("what is menu?\n")
        if menu in list(map(lambda x: x.menu, menus)):
            food = list(filter(lambda x: x.menu == menu, menus))[0]
            time = float(input("what time?\n"))
            ate = float(input("choice amount 0.5, 1, 1.5, 2:\n"))
            am = food.am * ate
            wa = food.wa * ate
            kc = food.kc * ate
            car = food.car * ate
            pr = food.pr * ate
            li = food.li * ate
            fi = food.fi * ate

            self.day_kc -= kc
            self.day_car -= car
            self.day_pr -= pr
            self.day_li -= li
            round_range = 2
            print(f"[ate]\nkc={round(kc, 2)} car={round(car, 2)} pr={round(pr, 2)} li={round(li, 2)} fi={round(fi, 2)}\n"
                  f"[remain]\nkc={round(self.day_kc, 2)} car={round(self.day_car, 2)} pr={round(self.day_pr, 2)} li={round(self.day_li, 2)}")
            if self.day_kc > 0:

                print(f"next time is {time+4.5}")
                tmp_foods = list(filter(lambda menu: menu.kc <= self.day_kc and
                                        menu.car <= self.day_car and
                                        menu.pr <= self.day_pr and
                                        menu.li <= self.day_li and
                                        menu.kc > 0 and
                                        menu.car + menu.pr + menu.li > 0
                                        , menus))
                idx = User.choice_max((self.day_car, self.day_pr, self.day_li))
                funcs = {0: lambda menu: menu.car / (menu.car + menu.pr + menu.li),
                         1: lambda menu: menu.pr / (menu.car + menu.pr + menu.li),
                         2: lambda menu: menu.li / (menu.car + menu.pr + menu.li), }

                tmp_foods = sorted(tmp_foods, key=funcs[idx], reverse=True)[:5]
                print("next menus")
                for food in tmp_foods:
                    print(food)
                # print(f"next menus={tmp_foods}")
                """
                1. 남은 영양소를 넘지 않는 음식
                2. 가장결핍이 된 영양소 비율이 가장 높은 음식
                """
        else:
            print("not found menu")
            return


class Food:
    """
    식품명	1회제공량	에너지(㎉)	수분(g)	단백질(g)	지방(g)	탄수화물(g)	총 식이섬유(g)


    """
    def __init__(self, menu=None, am=None, kc=None, wa=None, pr=None, li=None, car=None, fi=None):
        self.menu = menu
        self.am = Food.convert_type(am)
        self.wa = Food.convert_type(wa)
        self.kc = Food.convert_type(kc)
        self.pr = Food.convert_type(pr) * 4
        self.li = Food.convert_type(li) * 9
        self.car = Food.convert_type(car) * 4
        self.fi = Food.convert_type(fi)

    @classmethod
    def foods_filter(cls, foods):
        return list(filter(lambda x: "-" not in f"{x.kc}{x.car}{x.pr}{x.li}", foods))

    @classmethod
    def is_float(cls, value):
        for c in value:
            if c not in "0123456789.":
                return False
        return True

    @classmethod
    def convert_type(cls, data):
        return round(float(data), 2) if cls.is_float(data) else data

    def __str__(self):
        return f"{self.__dict__}"


def read_file(path):
    with open(path, "r") as f:
        return f.readlines()


def str_filter(foods):
    for i, food in enumerate(foods):
        foods[i] = food.replace("\n", "").replace(" ", "").replace('"', '').replace("  ", " ")



foods = list()
lines = read_file("data/foods.csv")
str_filter(lines)
for i, line in enumerate(lines):
    if i:
        args = line.split(",")
        foods.append(Food(*args))

foods = Food.foods_filter(foods)
for food in foods:
    print(food)


user = User(nick="aaa", tall=170, gender="female")
user.set_daily(is_diet=True, act=1)
user.set_current(foods)