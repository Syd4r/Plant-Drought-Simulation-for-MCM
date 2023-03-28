from PIL import Image
import numpy as np
import noise
import random
import copy
import matplotlib.pyplot as plt



class Cell():
    def __init__(self, x, y, plant,soil_type):
        self.x = x
        self.y = y
        self.plant = plant
        self.soil_type = soil_type
        if soil_type == 1:
            z = random.randint(300,400)
            self.water_capacity = z
            self.current_water = z
        elif soil_type == 2:
            z = random.randint(400,500)
            self.water_capacity = z
            self.current_water = z
        elif soil_type == 0:
            z = random.randint(500,600)
            self.water_capacity = z
            self.current_water = z

#make a child class of plant for each type of plant


class Plant():
    def __init__(self,x,y, water_get, life_expectancy, energy_usage, plant_num,seed_energy,energy=100):
        self.x = x
        self.y = y
        self.plant_num = plant_num
        self.water_get = water_get
        self.energy = energy
        self.seed_energy = seed_energy
        self.life_expectancy =  energy_usage*5
        self.max_energy = 500-life_expectancy
        self.age = 0
        self.energy_usage = energy_usage
        self.seed_dispersion = int(water_get/10)
        self.seeds = 0
        self.max_seeds = int(self.energy_usage/5)
    def grow(self):
        self.age += 1
        self.energy -= self.energy_usage
        if self.age > self.life_expectancy:
            list_of_cells[self.x][self.y].plant = 0
            list_of_alive_plants.remove(self)
        if self.energy < 0:
            list_of_cells[self.x][self.y].plant = 0
            list_of_alive_plants.remove(self)
    def get_water(self):
        if self.energy < self.max_energy:
            if list_of_cells[self.x][self.y].current_water > self.water_get:
                list_of_cells[self.x][self.y].current_water -= self.water_get
                self.energy += self.water_get
            else:
                self.energy += list_of_cells[self.x][self.y].current_water
                list_of_cells[self.x][self.y].current_water = 0
    def spread_seeds(self):
        if random.randint(0,(5-self.max_seeds)) == 0:
            if self.seeds < self.max_seeds:
                if self.age > self.life_expectancy/2:
                    i = random.randint((-1*self.seed_dispersion),self.seed_dispersion)
                    j = random.randint((-1*self.seed_dispersion),self.seed_dispersion)
                    try:
                        #make sure theres enough energy to make a seed
                        if self.energy > self.seed_energy:
                            #make sure theres no plant already there
                            if list_of_cells[self.x+i][self.y+j].plant == 0:
                                list_of_cells[self.x+i][self.y+j].plant = -1
                                list_of_seeds.append(Seed(self.x+i,self.y+j,self,self.seed_energy))
                                self.energy -= self.seed_energy
                                self.seeds += 1
                    except:
                        pass
            else:
                list_of_cells[self.x][self.y].plant = 0
                list_of_alive_plants.remove(self)
                
class Seed():
    def __init__(self, x, y, parent, seed_energy):
        self.x = x
        self.y = y
        self.parent = copy.deepcopy(parent)
        self.parent.x = x
        self.parent.y = y
        self.parent.age = 0
        self.parent.seeds = 0
        self.seed_energy = seed_energy
        self.age = 0
        self.time_to_grow = 50 - int(seed_energy/5)
        self.water_to_grow = 300 - seed_energy
    def grow(self):
        self.age += 1
        if self.age > self.time_to_grow:
            if list_of_cells[self.x][self.y].current_water > self.water_to_grow:
                if list_of_cells[self.x][self.y].plant == -1:
                    list_of_cells[self.x][self.y].current_water -= self.water_to_grow
                    list_of_cells[self.x][self.y].plant = self.parent.plant_num
                    list_of_alive_plants.append(randomize_obj(self.parent))
            else:
                list_of_cells[self.x][self.y].plant = 0
            list_of_seeds.remove(self)

def randomize_obj(obj):
    y = random.randint(-3,3)
    obj.water_get = obj.water_get + y
    #obj.life_expectancy = obj.life_expectancy + random.randint(-5,5)
    if obj.energy_usage > 10:
        x = random.randint(-3,3)
        obj.energy_usage = obj.energy_usage + x
    else:
        x = random.randint(1,3)
        obj.energy_usage = obj.energy_usage + x
    obj.max_seeds = int(obj.energy_usage/10)
    obj.seed_dispersion = int(obj.water_get/10)
    obj.life_expectancy = obj.life_expectancy + x*5
    obj.max_energy = 500-obj.life_expectancy
    obj.seed_energy = obj.seed_energy + random.randint(-20,20)
    return obj
    


# Set the random seed to a random value

full_scale = 50
random.seed()

# Generate a 50x50 noise image
scale = 100
octaves = 6
persistence = 0.5
lacunarity = 2.0
seed = random.randint(0, 100)
world = np.zeros((full_scale, full_scale))
for i in range(full_scale):
    for j in range(full_scale):
        world[i][j] = noise.pnoise2(i/scale,
                                     j/scale,
                                     octaves=octaves,
                                     persistence=persistence,
                                     lacunarity=lacunarity,
                                     repeatx=full_scale,
                                     repeaty=full_scale,
                                     base=seed)

# Cluster the noise image into three types of terrain
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
flat_cells = np.reshape(world, (full_scale**2, 1))
kmeans.fit(flat_cells)
landscape = np.reshape(kmeans.labels_, (full_scale, full_scale))



list_of_cells = []
plants = []
list_of_alive_plants =[]
list_of_seeds = []

for i in range(3):
    for j in range(4):
        if i == 0:
            plants.append(Plant(0,0,40+random.randint(-10,10),100,20+random.randint(-5,5),(i*4)+j+1,200+random.randint(-50,50)))
        elif i == 1:
            plants.append(Plant(0,0,50+random.randint(-10,10),75,25+random.randint(-5,5),(i*4)+j+1,200+random.randint(-50,50)))
        elif i == 2:
            plants.append(Plant(0,0,60+random.randint(-10,10),50,30+random.randint(-5,5),(i*4)+j+1,200+random.randint(-50,50)))

# Create an image from the terrain
image = Image.new("RGB", (full_scale, full_scale))
for i in range(len(landscape)):
    list_of_cells.append([])
    for j in range(len(landscape[i])):
        list_of_cells[i].append(Cell(i,j,0,landscape[i][j]))
        if landscape[i][j] == 1:
            image.putpixel((j, i), (255, 255, 0))
        elif landscape[i][j] == 2:
            image.putpixel((j, i), (0, 255, 0))
        elif landscape[i][j] == 3:
            image.putpixel((j, i), (0, 0, 255))
        else:
            image.putpixel((j, i), (0, 90, 10))
#make a clump of 4 plants for each plant type randomly on the map
for i in range(3):
    for j in range(4):
        x = random.randint(0,full_scale-2)
        y = random.randint(0,full_scale-2)
        if list_of_cells[x][y].plant == 0 and list_of_cells[x][y].plant == 0 and list_of_cells[x][y].plant == 0 and list_of_cells[x][y].plant == 0:
            for k in range(2):
                for l in range(2):
                    list_of_cells[x+k][y+l].plant = (i*4)+j+1
                    list_of_alive_plants.append(copy.deepcopy(plants[(i*4)+j]))
                    list_of_alive_plants[-1].x = x+k
                    list_of_alive_plants[-1].y = y+l
                    list_of_alive_plants[-1] = randomize_obj(list_of_alive_plants[-1])
                    image.putpixel((y+l, x+k), (0, 0, 0))
generations = 1000
for i in range(generations):
    for j in range(len(list_of_alive_plants)):
        try:
            list_of_alive_plants[j].grow()
            list_of_alive_plants[j].get_water()
            list_of_alive_plants[j].spread_seeds()
        except:
            pass
    for j in range(len(list_of_seeds)):
        try:
            list_of_seeds[j].grow()
        except:
            pass
    for j in range(len(list_of_cells)):
        for k in range(len(list_of_cells[j])):
            if list_of_cells[j][k].current_water < list_of_cells[j][k].water_capacity:
                if list_of_cells[j][k].soil_type == 0:
                    list_of_cells[j][k].current_water += random.randint(0,40)
                elif list_of_cells[j][k].soil_type == 2:
                    list_of_cells[j][k].current_water += random.randint(0,35)
                elif list_of_cells[j][k].soil_type == 1:
                    list_of_cells[j][k].current_water += random.randint(0,30)
    if i%1 == 0:


        for j in range(len(landscape)):
            for k in range(len(landscape[j])):
                if landscape[j][k] == 1:
                    image.putpixel((k, j), (255, 255, 0))
                elif landscape[j][k] == 2:
                    image.putpixel((k, j), (0, 255, 0))
                elif landscape[j][k] == 3:
                    image.putpixel((k, j), (0, 0, 255))
                else:
                    image.putpixel((k, j), (0, 90, 10))
        for j in range(len(list_of_alive_plants)):
            #do a different color for each plant type
            image.putpixel((list_of_alive_plants[j].y, list_of_alive_plants[j].x), (list_of_alive_plants[j].plant_num*20, 0, 0))


        image.save("images\landscape"+str(i)+".png")
list_of_plant_nums = []
nums_of_nums = []
for i in range(len(list_of_alive_plants)):
    list_of_plant_nums.append(list_of_alive_plants[i].plant_num)
for i in range(12):
    nums_of_nums.append(list_of_plant_nums.count(i+1))
check_for = nums_of_nums.index(max(nums_of_nums))+1
for i in range(len(list_of_alive_plants)):
    if list_of_alive_plants[i].plant_num == check_for:
        print("Most Common Plant Type")
        print(list_of_alive_plants[i].plant_num , " Plant Number")
        print(list_of_alive_plants[i].water_get , " Water Get")
        print(list_of_alive_plants[i].energy , " Energy")
        print(list_of_alive_plants[i].seed_energy , " Seed Energy")
        print(list_of_alive_plants[i].life_expectancy , " Life Expectancy")
        print(list_of_alive_plants[i].max_energy , " Max Energy")
        print(list_of_alive_plants[i].age , " Age")
        print(list_of_alive_plants[i].energy_usage , " Energy Usage")
        print(list_of_alive_plants[i].seed_dispersion , " Seed Dispersion")
        break
#find a random plant in each soil type and print its stats

def print_values(soil,name):
    water_get = 0
    energy = 0
    seed_energy = 0
    life_expectancy = 0
    max_energy = 0
    energy_usage = 0
    seed_dispersion = 0
    inc = 0
    print()
    for i in list_of_alive_plants:
        if list_of_cells[i.x][i.y].soil_type == soil:
            water_get += i.water_get
            energy += i.energy
            seed_energy += i.seed_energy
            life_expectancy += i.life_expectancy
            max_energy += i.max_energy
            energy_usage += i.energy_usage
            seed_dispersion += i.seed_dispersion
            inc += 1
    print("Average Plant in "+name+" Water Soil")
    print(int(water_get/inc) , " Water Get")
    print(int(energy/inc) , " Energy")
    print(int(seed_energy/inc) , " Seed Energy")
    print(int(life_expectancy/inc) , " Life Expectancy")
    print(int(max_energy/inc) , " Max Energy")
    print(int(energy_usage/inc) , " Energy Usage")
    print(int(seed_dispersion/inc) , " Seed Dispersion")
    print(inc)

print_values(0,"High")
print_values(2,"Medium")
print_values(1,"Low")

