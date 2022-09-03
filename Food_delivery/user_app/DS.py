

class Node:
    def __init__(self,data=None,next=None):
        self.data=data
        self.next=next  

class LinkedList:
    def __init__(self):
        self.head=None
    def insert_at_begin(self,data):
        node=Node(data,self.head)
        self.head=node

    def print(self):
        if self.head is None:
            print("Empty")
            return
        itr=self.head
        llstr=''

        while itr:
            llstr+=str(itr.data)+'--->'
            itr=itr.next
        print(llstr)

    def insert_at_end(self,data):                
        if self.head is None:                          
            self.head=Node(data,None)                          
            return                                             
        itr=self.head                                  
        while itr.next:                               
            itr=itr.next
        itr.next=Node(data,None)


    def insert_values(self,d_list):
        self.head=None
        for x in d_list:
            self.insert_at_end(x)

if __name__ == '__main__':
    obj=LinkedList()
    obj.insert_at_end(230)
    obj.insert_at_end(7000)
    obj.insert_at_end(2300)
    obj.insert_values(['red','yellow','blue','orange'])
    obj.print()

    



    
    

