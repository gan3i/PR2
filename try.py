# A simple implementation of Priority Queue 
# using Queue. 
class PriorityQueue(object): 
	def __init__(self): 
		self.queue = [] 

	def __str__(self): 
		return ' '.join([str(i) for i in self.queue]) 

	# for checking if the queue is empty 
	def isEmpty(self): 
		return len(self.queue) == 0
	def __add__(self,other):
		self.queue =self.queue + other.queue
		return self
	def has(self,value):
		return value in self.queue

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

if __name__ == '__main__': 
	myQueue = PriorityQueue() 
	myQueue.put((12,1)) 
	myQueue.put((1,1)) 
	myQueue.put((14,2.2)) 
	myQueue.put((7,0.2))
	myQueue1 = PriorityQueue() 
	# myQueue1.put((15,1)) 
	# myQueue1.put((1,1)) 
	# myQueue1.put((14,2)) 
	# myQueue1.put((7,4)) 
	myQueue += myQueue1
	if myQueue.has((12,1)):
		print("Hello")		 
	while not myQueue.isEmpty(): 
		print(myQueue.get()) 




