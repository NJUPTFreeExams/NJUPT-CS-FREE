# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random


##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    SimpleBacteria和ResistantBacteria classes不需要修改
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):

    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):

    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): 最大可能繁殖率
                probability
            death_prob (float in [0, 1]): 最大死亡率
        """
#SimpleBacteria 的构造函数只需要给成员变量赋值，分别为细菌的出生率和死亡率
        
        # TODO
        self.birth_prob = float(birth_prob)
        self.death_prob = float(death_prob)



    def is_killed(self):
        """
随机决定这个细菌细胞是否被杀死
病人的身体在一个时间步骤，即细菌细胞死亡
某个概率等于每个时间步的死亡概率。

返回:
bool:有概率为True self.death_prob，否则为False。
        """
        # TODO
        return (random.random() <= self.death_prob)

    def reproduce(self, pop_density):
        """
随机决定该细菌细胞是否在a
时间步长。由Patient和中的update()方法调用
TreatedPatient类。

细菌细胞有可能繁殖
自我。birth_probb * (1 - pop_density)。

如果该细菌细胞繁殖，则reproduction()创建并返回
后代SimpleBacteria的实例(具有相同的特征)
作为其父节点的Birth_prob和death_prob值)。

参数:
pop_density (float):人口密度，定义为
当前细菌数量除以最大数量

返回:
SimpleBacteria:表示的后代的新实例
这个细菌细胞(如果细菌繁殖的话)。这个孩子
应该有相同的birth_prob和death_prob值
这种细菌。

提出了:
如果该细菌细胞不繁殖，则返回NoChildException。
        """
        #根据 doc string 的中的说明完成 reproduce 方法。在每个时间点，依概率判断
        # 在当前时刻是否会繁殖新的细菌 —— 如果是，则返回一个新的 SimpleBacteria
        # 对象；如果不是，则抛出异常。
        # TODO
        if random.random() <= self.birth_prob*(1 - pop_density):
            return SimpleBacteria(self.birth_prob, self.death_prob)

        else: NoChildException() 


class Patient(object):
    """
    简化病人的表示。病人没有服用任何药物
抗生素和他/她的细菌种群没有抗生素耐药性。
    """
    #构造函数只需要给成员变量赋值，分别为细菌的列表和最大数量
    def __init__(self, bacteria, max_pop):
        """
        参数:
细菌(简单细菌列表):种群中的细菌
max_pop (int):最大可能的细菌种群大小
这个病人
        """
        # TODO
        self.bacteria = list(bacteria)
        self.max_pop = int(max_pop)

    def get_total_pop(self):
        """
获取当前细菌总数的大小。

返回:
int:细菌总数
        """
        # TODO
        return len(self.bacteria)
    
    def get_max_pop(self):
        return self.max_pop

    def update(self):
        """
更新该患者的细菌种群状态
单时间步长。Update()应该执行以下步骤
这个顺序:

1. 确定每个细菌细胞是否死亡(根据
Is_killed方法)，并创建一个新的存活细菌细胞列表。

2. 通过除以存活数来计算当前的人口密度
细菌种群由最大种群组成。这个群体
密度值用于以下步骤，直到下一次调用
更新()

3.根据种群密度，确定每只是否存活
细菌细胞应该繁殖并添加后代细菌细胞
病人体内的细菌列表。新的后代不能繁殖。

4. 把病人的细菌名单改成存活菌名单
细菌和新的后代细菌

返回:
int:更新结束时的细菌总数
        """
        # TODO

        #1
        self.bacteria = self.get_survived_bacteria()

        #2
        pop_density = self.get_pop_density()

        #3
        child_bacteria = self.get_child_bacteria(pop_density)

        #4
        self.bacteria += child_bacteria

        return len(self.bacteria)

        

    def get_survived_bacteria(self):

        survived_bacteria = list()
        for bacterium in self.bacteria:
            if not bacterium.is_killed():
                survived_bacteria.append(bacterium)
        return survived_bacteria

    def get_pop_density(self):
        return self.get_total_pop()/float(self.max_pop)

    def get_child_bacteria(self, pop_density):
        child_bacteria = list()
        for bacterium in self.bacteria:
            child = bacterium.reproduce(pop_density)
            if child is not None:
                child_bacteria.append(child)
        return child_bacteria





##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
找出在时间步骤n的试验中平均细菌种群大小

参数:
population (list of lists或2D array): population [i][j]为
试验I在时间步长j时的细菌数量

返回:
浮子:在时间步长n时的平均菌群大小
    """
    # TODO
    n_population = list()
    for trial in populations:
        n_population.append(trial[n])

    return sum(n_population)/float(len(populations))

def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    """
运行模拟并绘制问题2的图形。没有抗生素
细菌对抗生素没有任何耐药性。

对于每个num_trials的试验:
*实例化一个SimpleBacteria的列表
*使用SimpleBacteria列表实例化一个Patient
*模拟300个时间步的细菌数量变化，
记录每个时间步骤后的细菌数量。请注意
第一个时间步应该包含的起始数
病人体内的细菌

然后，绘制平均细菌种群大小(y轴)作为的函数
您可能会找到make_one_curve_plot
有用的函数。

参数:
num_bacteria (int):要为病人创建的SimpleBacteria的数量
Max_pop (int):患者的最大细菌数量
Birth_prob (float in[0,1]):最大生育
概率
Death_prob (float in[0,1]):最大死亡概率
Num_trials (int):要执行的模拟运行数

返回:
population (list of lists或2D array): population [i][j]为
试验I在时间步长j时的细菌数量
    """
    # TODO
    num_steps = 300

    def create_bacteria():
        bacteria = list()
        for i in range(num_bacteria):
            bacteria.append(SimpleBacteria(birth_prob, death_prob))
        return bacteria

    def run_trial():
        """返回每个时间步长的人口列表"""
        bacteria = create_bacteria()
        patient = Patient(bacteria, max_pop)
        population = list()
        for i in range(num_steps):
            population.append(patient.get_total_pop())
            patient.update()
        return population

    populations = list()
    for trial in range(num_trials):
        populations.append(run_trial())

    #Plot
    def get_x_coords():
        x_coords = list()
        for i in range(num_steps):
            x_coords.append(i)
        return x_coords

    def get_y_coords():
        y_coords = list()
        for i in range(num_steps):
            y_coords.append(calc_pop_avg(populations, i))
        return y_coords

    make_one_curve_plot(get_x_coords(), get_y_coords(), "time-steps", "Population", "Population over time without antibiotic")

    return populations 

# When you are ready to run the simulation, uncomment the next line
populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    求不同试验中总体的标准差
在时间第t步:
*计算时间步长t的平均人口
*计算数据点到平均值的平均距离的平方
然后取平方根

你不能使用第三方函数来计算标准差，
例如numpy.std。其他内置或第三方函数不支持
可以使用计算标准偏差。

参数:
population (list of lists或2D array): population [i][j]为
试验I在时间步骤j中存在的细菌数量
T (int):时间步长

返回:
漂数:不同试验的总体标准差
特定的时间步长
    """
    # TODO

    mean = calc_pop_avg(populations, t)

    quad_deviation_inctance_population = list()
    for trial in populations:
        quad_deviation_inctance_population.append((trial[t]- mean)**2)

    return math.sqrt(sum(quad_deviation_inctance_population)/float(len(populations)))


def calc_95_ci(populations, t):
    """
在平均细菌数量周围找到95%的置信区间
时间:
*计算样本的均值和标准差
*使用样本的标准差来估计
平均标准误差(SEM)
*使用扫描电子显微镜构建置信区间
样本均值

参数:
population (list of lists或2D array): population [i][j]为
试验I在时间步骤j中存在的细菌数量
T (int):时间步长

返回:
均值(float):样本均值
宽度(浮动):1.96 * SEM

也就是说，你应该返回一个包含(mean, width)的元组
    """
    # TODO
    sem = calc_pop_std(populations, t) / float(math.sqrt(len(populations)))
    return (calc_pop_avg(populations, t), 1.96 * sem)



##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """对抗生素有抵抗力的细菌细胞。"""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
参数:
Birth_prob (float in[0,1]):生育概率
Death_prob (float in[0,1]):死亡概率
耐药(bool):该细菌是否具有抗生素耐药性
Mut_prob (float):这个的变异概率
细菌细胞。这是最大概率
后代获得抗生素耐药性
        """
        # TODO
        self.birth_prob = birth_prob
        self.death_prob = death_prob
        self.resistant = resistant
        self.mut_prob = mut_prob


    def get_resistant(self):
        """返回细菌是否具有抗生素耐药性"""
        # TODO
        return self.resistant

    def is_killed(self):
        """随机决定这个细菌细胞是否被杀死
病人的身体在给定的时间步长。

检查细菌是否具有抗生素耐药性。如果耐药,
细菌以正常的死亡概率死亡。如果没有抵抗力，
细菌以常规的死亡概率/ 4死亡。

返回:
bool:如果细菌以适当的概率死亡，则为True
否则为False。
        """
          # TODO

        if self.get_resistant():
            return (random.random() <= self.death_prob)
        else: return (random.random() <= self.death_prob / float(4))

    def reproduce(self, pop_density):
        """
       随机决定该细菌细胞是否在a
时间步长。由TreatedPatient类中的update()方法调用。

存活的细菌细胞有可能繁殖:
自我。birth_probb * (1 - pop_density)。

如果细菌细胞繁殖，则reproduction()创建并返回
抗性细菌后代的一个实例，它将具有
与其父节点相同的birth_prob、death_prob和mut_prob值。

如果细菌对抗生素有抗药性，其后代也会有抗药性
耐药。如果细菌没有抗生素耐药性，它就会
后代有自我的概率。Mut_prob * (1-pop_density
发展这种抵抗特性。也就是说，细菌密度较低
人口稠密的环境有更大的机会发生突变
抗生素耐药性。

参数:
Pop_density (float):人口密度

返回:
耐药细菌:代表后代的实例
这个细菌细胞(如果细菌繁殖的话)。孩子应该
有相同的birth_prob, death_prob值和mut_prob
就像这个细菌。否则，将引发NoChildException
细菌细胞不繁殖。
        """
        # TODO

        if random.random() <= self.birth_prob * (1 - pop_density):
            new_resistant = True
            if not self.get_resistant():
                if not random.random() <= self.mut_prob * (1 - pop_density):
                    new_resistant = False
            return ResistantBacteria(self.birth_prob, self.death_prob, new_resistant, self.mut_prob)




class TreatedPatient(Patient):
    """
    接受治疗的病人的代表。病人能接受治疗
抗生素及其菌群可获得抗生素
阻力。病人一旦使用抗生素就不能停药。
    """
    def __init__(self, bacteria, max_pop):
        """
        参数:
细菌:表示细菌种群的列表(一个列表)
细菌实例)
max_pop:该患者的最大细菌数量(int)

这个函数应该初始化self。On_antibiotic，表示
病人是否服用了抗生素。最初,
病人没有服用抗生素。

不要忘记在开始时调用Patient的__init__方法
方法。
        """
        # TODO
        self.bacteria = bacteria
        self.max_pop = max_pop
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        """
       给这个病人注射抗生素。抗生素作用于
所有后续时间步骤的细菌种群。
        """
        # TODO
        self.on_antibiotic = True

    def get_resist_pop(self):
        """
        得到具有抗生素耐药性的细菌细胞的数量

返回:
Int:具有抗生素耐药性的细菌数量
        """
        # TODO
        return len(self.get_resist_bacteria())

    def get_resist_bacteria(self):

        resistant_bacteria = list(self.bacteria)
        nonresistant_bacteria = list()
        for bacterium in resistant_bacteria:
            if not bacterium.get_resistant():
                nonresistant_bacteria.append(bacterium)
        for each in nonresistant_bacteria:
            resistant_bacteria.remove(each)
        return resistant_bacteria
           

    def update(self):
        """
        更新该患者的细菌种群状态
单时间步长。Update()应该按顺序执行这些操作:

1. 确定每个细菌细胞是否死亡(根据
Is_killed方法)，并创建一个新的存活细菌细胞列表。

2. 如果病人服用抗生素，存活下来的细菌细胞
只有具有耐药性才能存活得更久。如果病人是
不使用抗生素，让所有存活的细菌细胞远离(1)

3.计算当前人口密度。此值将一直使用到
下一个对update()的调用。使用与Patient中相同的计算方法

4. 根据此人口密度值，确定是否每个
存活的细菌细胞会繁殖并增加后代细菌
这个病人体内的细菌。

5. 将病人的细菌名单改为存活菌名单
细菌和新的后代细菌

返回:
int:更新结束时的细菌总数
        """
        # TODO

        #1
        self.bacteria = self.get_survived_bacteria()
        
        #2
        self.bacteria = self.get_resistant_survived_bacteria()

        #3
        pop_density = self.get_pop_density()

        #4
        child_bacteria = self.get_child_bacteria(pop_density)

        #5
        self.bacteria += child_bacteria

        return len(self.bacteria)

    def get_resistant_survived_bacteria(self):
        if not self.on_antibiotic:
            return self.bacteria
        else:
            return self.get_resist_bacteria()


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    为问题4运行模拟并绘制图表。

对于每个num_trials的试验:
*实例化一个ResistantBacteria列表
实例化一个病人
*运行模拟150个时间步，添加抗生素，然后运行
模拟额外的250个时间步长，记录总数
细菌种群和耐药菌种群
每个时间步长

绘制两个总细菌的平均细菌种群大小
种群和耐药细菌种群(y轴)作为a
在同一图上经过的时间步长(x轴)的函数。你可能会发现
辅助函数make_two_curve_plot很有用

参数:
num_bacteria (int):要创建的抗性细菌的数量
病人
Max_pop (int):患者的最大细菌数量
Birth_prob (float int[0-1]):生育概率
Death_prob (float in[0,1]):细菌细胞死亡的概率
耐药(bool):细菌最初是否具有
抗生素耐药性
Mut_prob (float in[0,1]):变量的变异概率
ResistantBacteria细胞
Num_trials (int):要执行的模拟运行数

返回:由两个列表的列表组成的元组，或两个2D数组
种群(list of lists或2D array):细菌总数
在每次试验的每个时间步;Total_population [i][j]为
试验I在时间步长j处的总体
resistant_pop (list of lists或2D array):列表的总数
每个试验每个时间步骤的耐药菌;
Resistant_pop [i][j]为耐药菌的数量
在时间步长j处尝试I
    """
    # TODO

    num_steps_0 = 150
    num_steps_1 = 250

    def create_bacteria():
        bacteria = list()
        for i in range(num_bacteria):
            bacteria.append(ResistantBacteria(birth_prob, death_prob, resistant, mut_prob))
        return bacteria

    def run_trial():
        """返回每个时间步长的人口列表"""
        bacteria = create_bacteria()
        patient = TreatedPatient(bacteria, max_pop)
        population = list()
        resistant_population = list()
        for i in range(num_steps_0 + num_steps_1):
            if i == num_steps_0:
                patient.set_on_antibiotic()
            population.append(patient.get_total_pop())
            resistant_population.append(patient.get_resist_pop())
            patient.update()
        return [population, resistant_population]

    populations = list()
    resistant_populations = list()
    for trial in range(num_trials):
        result = run_trial()
        populations.append(result[1])
        resistant_populations.append(result[0])

    #Plot
    def get_x_coords():
        x_coords = list()
        for i in range(num_steps_0 + num_steps_1):
            x_coords.append(i)
        return x_coords

    def get_y_coords():
        y_coords_total = list()
        y_coords_resistant = list()
        
        for i in range(num_steps_0 + num_steps_1):
            y_coords_total.append(calc_pop_avg(populations, i))
            y_coords_resistant.append(calc_pop_avg(resistant_populations, i))
        return [y_coords_total, y_coords_resistant]

    y = get_y_coords()
    make_two_curve_plot(get_x_coords(), y[0], y[1],"Resistant Population", "Total population", "time-steps", "Population", "Population over time with an antibiotic")

    return [populations, resistant_populations]

# When you are ready to run the simulations, uncomment the next lines one
# at a time
total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.3,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)

total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.17,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)
