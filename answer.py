import sys
import math
import random
from queue import Queue
import time

RETAIN = 0.9

def log(*args):
    for i in args:
        print(i,file = sys.stderr)

def log_line(*args):
    print(f"{' '.join(str(x) for x in args)}",file = sys.stderr)


class PriorityQueue(object): 
	def __init__(self): 
		self.queue = [] 

	def __str__(self): 
		return ' '.join([str(i) for i in self.queue])
	def __add__(self,other): 
		self.queue =self.queue + other.queue
		return self
	def has(self,value): 
		return value in self.queue
	def length(self,value): 
		return len(self.queue)   
	# for checking if the queue is empty 
	def isEmpty(self): 
		return len(self.queue) == 0
	# for inserting an element in the queue 
	def put(self, data): 
		self.queue.append(data) 

	# for popping an element based on Priority 
	def get(self): 
		try: 
			max = 0
			for i in range(len(self.queue)): 
				if self.queue[i][1] > self.queue[max][1]: 
					max = i 
			item = self.queue[max]
			del self.queue[max] 
			return item 
		except IndexError: 
			print() 
			exit() 
# class Pods():
class Path():
    def __init__(self,path):
        self.path = path
        self.dist = len(path)

class Zone():
    def __init__(self,zone_id):
        self.id =zone_id 
        self.adj_zones = []
        self.owner_id = -1
        self.my_pods = 0
        self.enemy_pods = 0
        self.visible =False
        self.platinum = 0
        self.backup_capacity = 0 #TODO reset backup capacity
        self.neutral = False
        
    def is_mine(self,my_id):
        return self.owner_id == my_id
    def is_neutral(self):
        return self.neutral
    def need_backup(self):
        if self.enemy_pods > 0 and self.my_pods >0 and self.enemy_pods > self.my_pods:
            self.backup_capacity = self.my_pods - self.enemy_pods +1
            return True
        else:
            return False
class Game():
    def __init__(self,player_count,my_id,zone_count,link_count):
        self.player_count = player_count
        self.my_id = my_id 
        self.zone_count =zone_count
        self.link_count = link_count
        self.zones = {}
        self.paths = {}
        self.my_platinum = 0
        self.orders = []
        self.my_HQ = -1
        self.enemy_HQ = -1
        self.defenders = 0
        self.war_zones = []
        self.turn = 1
        self.enemy_HQ_dist = 0
        self.tic = 0
        self.toc = 0
    def enemy_id(self):
        if self.my_id:
            return 0
        else:
            return 1
    def first_turn(self):
        return self.turn == 1
    def next_turn(self):
        self.turn +=1
    def set_enemy_HQ_distance(self):
        self.enemy_HQ_dist=self.get_path_dist(self.my_HQ,self.enemy_HQ)
    def clear(self):
        self.orders = []
    def get_zone(self, zone_id):
        return self.zones[zone_id]
    def get_neighbours(self,zone_id):
        return self.get_zone(zone_id).adj_zones
    def get_value_zones(self,zone):
        for adj_zone in zone.adj_zones:
            # if self.get_zone(zone.id).platinum > 0:
            yield adj_zone
    def initialize_zones(self):
        # adj_list = {Zone}
        for _ in range(self.zone_count):
            # zone_id: this zone's ID (between 0 and zoneCount-1)
            # platinum_source: Because of the fog, will always be 0
            zone_id, _ = [int(j) for j in input().split()]
            self.zones[zone_id] = Zone(zone_id) 
    def fill_links(self):
        for _ in range(link_count):
            zone_1, zone_2 = [int(j) for j in input().split()]
            self.zones[zone_1].adj_zones.append(zone_2)
            self.zones[zone_2].adj_zones.append(zone_1)
    def fill_path(self):
        # tic = time.process_time()
        for start in range(self.zone_count):
            all_paths = self.BFS(start)
            # for k,v in all_paths.items():
            #     log_line(k,v)
            for end in range(start+1,zone_count):
                self.paths[(start,end)] = Path(all_paths[end])
        # toc = time.process_time()
        # log(toc-tic)
    def get_path(self,start, end):
        if start > end :#TODO handle no key error
            return self.paths[(end,start)].path[::-1]
        else:
            return self.paths[(start,end)].path
    def get_path_dist(self,start, end):
        if start == end :
            return 1
        if start > end :#TODO handle no key error
            return self.paths[(end,start)].dist
        else:
            return self.paths[(start,end)].dist
    def has_path(self,start,end):
        if (start,end) in self.paths or (end,start) in self.paths:
            return True
        else :
            return False
    def get_pathv2(self,start, end):
        return self.paths[(start,end)].path
    def BFS(self,start):
        q = []
        all_paths = {start:[start]}
        visited = {start:True}
        q.append(start)
        while q :
            current_node = q[0]
            q.pop(0)
            current_path = all_paths[current_node]
            for nbr in self.get_neighbours(current_node):
                if nbr not in visited:
                    new_path = current_path + [nbr]
                    all_paths[nbr] = new_path
                    q.append(nbr)
                    visited[nbr] = True
        return all_paths
    def append_order(self,pods_count,zone_from,zone_to):
        if zone_from != zone_to :
            zone_to = self.get_path(zone_from,zone_to)[1]
            self.orders.append(pods_count)
            self.orders.append(zone_from)
            self.orders.append(zone_to)
    def send_order(self):
        print(f"{' '.join(str(x) for x in self.orders)}")
        print("WAIT")
    def is_war_zone(self,zone):
        if zone.need_backup():
            self.war_zones.append(zone.id)
            return True
        else:
            return False
    def is_under_attack(self,zone):
        enemy_pods = 0 
        if zone.enemy_pods>0:
            enemy_pods += zone.enemy_pods
        for first in zone.adj_zones:
            first_nhbr = self.get_zone(first)
            if first_nhbr.enemy_pods>0:
                enemy_pods += first_nhbr.enemy_pods
            # else:
            #     for sec in first_nhbr.adj_zones:
            #         if self.get_zone(sec).enemy_pods>0:
            #             return True

        return enemy_pods       
    def is_dead_end(self, zone):
        if zone.platinum >0:
            return False
        if len(zone.adj_zones) == 1:
            return True
        for nz_id in zone.adj_zones:
            nz = self.get_zone(nz_id)  
            if not nz.neutral and not nz.is_mine(self.my_id):
                return False
        return True               
    def get_priorityQ(self,zone,p_queue,picked):
        first_nhbrs = zone.adj_zones
        pods_got_job = 0
        visited = [zone.id]
        for nz_id in first_nhbrs:
            # log_line("set priority",zone.id,nz_id)
            visited.append(nz_id)
            nz = self.get_zone(nz_id)
            nz_enemy_pods = nz.enemy_pods
            if zone.platinum > 0 and nz_enemy_pods>0:
                # log("HI")
                if nz_enemy_pods ==zone.my_pods:
                    p_queue.put((zone.id,12))# 12 for stay put
                    zone.backup_capacity +=1
                    log("return")
                    return
                elif nz_enemy_pods > zone.my_pods:
                    p_queue.put((zone.id,12))
                    zone.backup_capacity += ((nz_enemy_pods-zone.my_pods)+1)
                    # log("return")
                    return
                else:
                    for i in range(nz_enemy_pods+1):
                        p_queue.put((zone.id,12))# 12 for stay put
                        # log_line(f"stay put {i}:",zone.id,nz_id)
                # for _ in range(nz.)
                # return
            # log_line("is dead_end",zone.id,nz_id,self.is_dead_end(nz))
            # if self.is_dead_end(nz):
            #     # log_line("dead_end",zone.id,nz_id,nz.platinum)
            #     continue
            
            pods_got_job += self.set_priority(nz,p_queue,picked)
        # log_line("pods_got_job1",pods_got_job,zone.id)
        sec_nhbrs = []
        for nz_id in first_nhbrs:
            sec_nhbr = self.get_zone(nz_id).adj_zones
            for sec_nz_id in sec_nhbr:
                sec_nz = self.get_zone(sec_nz_id) 
                if sec_nz_id not in visited and sec_nz.my_pods==0 :
                    visited.append(sec_nz_id)
                    if not self.is_dead_end(sec_nz):
                        sec_nhbrs.append(sec_nz_id)
                        pods_got_job += self.set_priority(sec_nz,p_queue,picked)
        # log_line("pods_got_job2",pods_got_job,zone.id)
        # for sec_nz_id in sec_nhbrs:
        #     t_nhbr = self.get_zone(sec_nz_id).adj_zones
        #     for t_nz_id in t_nhbr:
        #         t_nz = self.get_zone(t_nz_id)
        #         if t_nz_id not in visited and t_nz.my_pods==0:
        #             visited.append(t_nz_id)
        #             if not self.is_dead_end(t_nz):
        #                 pods_got_job += self.set_priority(t_nz,p_queue,picked)
        # log_line("pods_got_job3",pods_got_job,zone.id)
    def set_priority(self,nz,p_queue,picked): 

            if not nz.is_mine(self.my_id) :
                # log("im")
                if nz.owner_id == self.enemy_id() and nz.enemy_pods == 0:
                    # log_line("enemyzone",nz.id,nz.platinum + 11)
                    p_queue.put((nz.id,nz.platinum + 11))# 5 to 10 platinum source
                if nz.platinum > 0:
                    # log_line("platinum",nz.id,nz.platinum+4)
                    p_queue.put((nz.id,nz.platinum+4))# 5 to 10 platinum source
                elif nz.backup_capacity:
                    # log_line("Backup",nz.id,4)
                    for _ in range(nz.backup_capacity):
                        p_queue.put(nz.id,4)
                else:
                    # log_line("neutral",nz.id,3)
                    p_queue.put((nz.id,3)) # 4 for neutral or enemy zone #TODO try to avoid heavy enemy zone
                return 1
            return 0
    def set_priority_v2(self,r_zone,p1_queue,not_visited,picked):
        for zone in not_visited:
            if zone.id in picked or r_zone.id == zone.id:
                continue
            priority = (100/self.get_path_dist(r_zone.id,zone.id)) + zone.platinum
            # log_line(zone.id ,priority)
            p1_queue.put((zone.id ,priority))

    def run(self):
        picked = [] #TODO make this hash map if there is timeout
        remaining = []
        for zone in [zone for zone in self.zones.values() if not self.is_war_zone(zone) and  zone.my_pods>0]:

            if zone.id == self.my_HQ:
                enemy_pods = self.is_under_attack(zone)
                if enemy_pods != 0 and zone.my_pods > enemy_pods + 1:
                    log("Hello",enemy_pods)
                    pods_count = zone.my_pods - enemy_pods +1 
                else :
                    pods_count = zone.my_pods
            else:
                pods_count = zone.my_pods

            used_pods = 0
            if pods_count>0:
                if self.get_path_dist(zone.id,self.enemy_HQ) < 4:# if enemy HQ is Adjacent move all pods to enemy HQ 
                    log("dist")
                    self.append_order(pods_count,zone.id,self.enemy_HQ)
                    continue

                p_queue = PriorityQueue()
                self.get_priorityQ(zone,p_queue,picked)
                # log_line("is Q not empty",zone.id, p_queue.isEmpty())    
                while not p_queue.isEmpty():
                    target = p_queue.get()
                    # log_line("Q not empty",zone.id,target)
                    if target[0] not in picked:
                        picked.append(target)
                        self.append_order(1,zone.id,target[0])
                        used_pods +=1
                        if used_pods == pods_count:
                            break                    
                if used_pods == pods_count:    
                    continue
                
                remaining.append((zone.id,pods_count-used_pods))


        not_visited = [zone for zone in self.zones.values() if zone.id not in picked and not zone.is_mine(self.my_id)  and not zone.neutral]  
        total = len(self.zones)
        visited_perce = ((total-len(not_visited))/total)*100
        # log_line("visited_perce",visited_perce,total,len(not_visited))
        for r in remaining:
            if visited_perce > 80 or self.enemy_HQ_dist < 5 or self.get_path_dist(r[0],self.enemy_HQ) < 5:
                self.append_order(r[1],r[0],self.enemy_HQ)
                log_line("invade",r[1],r[0])
                continue

            p1_queue = PriorityQueue()
            r_zone = self.get_zone(r[0])
            self.set_priority_v2(r_zone,p1_queue,not_visited,picked)
            used = 0
            for i in range(r[1]):
                if not p1_queue.isEmpty():
                    x = p1_queue.get()
                    picked.append(x[0])
                    self.append_order(r[1],r[0],x[0])
                    used +=1
                else:
                    remaining_pods = r[1] - i+1
                    self.append_order(remaining_pods,r[0],self.enemy_HQ)
                    log_line("early invasion")
                    used +=remaining_pods
                    break

            # log_line("remainng",r[1],"on" ,r[0],"Used",used)



                
        self.send_order()
        self.clear()

                
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]
game = Game(player_count,my_id,zone_count,link_count)
game.initialize_zones()
game.fill_links()
game.fill_path()
# for key, values in game.paths.items():
#     log_line(key,values)
# log(game.paths)
# game loop
while True:    
    # game.tic = time.process_time()
    my_platinum = int(input())  # your available Platinum
    game.my_platinum = my_platinum
    for i in range(zone_count):
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
        zone = game.zones[z_id]
        if not game.my_id:
            zone.my_pods = pods_p0
            zone.enemy_pods = pods_p1
        else:
            zone.my_pods = pods_p1
            zone.enemy_pods = pods_p0
        zone.visible = visible
        if visible:
            zone.platinum = platinum
            zone.owner_id = owner_id
            if owner_id == -1:
                zone.neutral = True
        if game.first_turn() and zone.my_pods>0:
            game.my_HQ = z_id
        if game.first_turn() and zone.enemy_pods>0:
            game.enemy_HQ = z_id

    if game.first_turn():
        game.set_enemy_HQ_distance()
    game.run()
    game.next_turn()
    # game.toc = time.process_time()
    # log(game.toc-game.tic)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)



