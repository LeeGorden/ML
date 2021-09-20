# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""
import random

###三种原地排序方法-low B 排序
def bubble_sort(li):
    '''
    原理：从index=0处开始，每次比较当前数和后面一个数的大小，若比后面一个数大，将当前
    数往后移动一位，然后看index=1处的数字。遍历所有位置后视为完成一轮，没完成一轮，最
    大的数字被排到了最后。然后开始下一轮，下一轮不用看倒数第二个数和最后一个数的大小。
    时间复杂度：O(n^2)
    li:待排序list
    
    '''
    for i in range(len(li)-1): #一个轮次
        exchange = False
        for j in range(len(li)-i-1): #一次比较
            if li[j] > li[j+1]: #升序排列
                li[j], li[j+1] = li[j+1], li[j] #python内部同时交换两个数，是元组的交换
                exchange = True
    if not exchange: #当在一个轮次中没有任何位置发生换位，则已经排序完成
        return
li = [random.randint(0, 10000) for i in range(10)]
bubble_sort(li)
'''------------------------------------------------------------------------'''

def select_sort(li):
    '''
    原理：不开辟新列表（这样增加内存）,所以每次遍历无序区，取出最小值与无序区第一个数
    交换位置。这里在内循环中不用min、remove, 因为它们的复杂度是O(n),会导致最后整体的
    复杂度超过O(n^2)
    时间复杂度：O(n^2)
    '''
    for i in range(len(li)-1): #因为最后一个数和自己比较，位置不更换所以是n-1次, i是第几轮
        min_loc = i #当前无序区第一个数
        for j in range(i+1, len(li)): 
        #range包前不包后，这里是无序区的范围。因为没经过一个轮次会确定之前无序区第一个最小数, range(i+1,..)是因为自己不用和自己比
            if li[j] < li[min_loc]:
                min_loc = j
        li[i], li[min_loc] = li[min_loc], li[i] #将找到的最小值与无序区第一个数交换
li = [random.randint(0, 10000) for i in range(10)]
select_sort(li)
'''------------------------------------------------------------------------'''
            
def insert_sort(li):
    '''
    原理：跟理牌类似，初始有序区就一张牌，每插入排序一次，有序区的牌+1
    时间复杂度：O(n^2)
    '''
    for i in range(1, len(li)): #i表示摸到的牌（无序区的数）的下标
        tmp = li[i] #之所以要用tmp存储是因为这里比较不止一次，位置会变，所以不适合交换
        j = i - 1 #指手里的牌（有序区）的最后一位的下标：
        while j >= 0 and li[j] > tmp:
            li[j+1] = li[j]
            j -= 1 #当升序时，不停的将摸到的牌和手头的牌从右到左比大小，直到放到有序区的合适位置，即前一个数li[j]<待放入的数或者已经到达第一位时停下
        li[j+1] = tmp #这里是让进行插入排序的数字放到合适的位置
li = [random.randint(0, 10000) for i in range(10)]   
insert_sort(li) 
'''------------------------------------------------------------------------'''
'''------------------------------------------------------------------------'''
###NB 三排序
#快速排序
def partition(li, left, right):
    '''
    归位操作：以升序为例，取出第一个数a，第一个位置留给从右边数起第一个比被取出的数小
        的数b。b的位置留给从左边数起第一个比a大的数c，以此类推，知道没有数字满足条件。
        这时多出的位置留给a。
    left:无序区最左边元素的index, 也是下一个被归位对象所在的初始位置。这个无序区是指被归位元素分割的两个无序部分部分：有序区,left~mid,mid~right,有序区
    注意：归位完成后只保证左、右两边分别比被归位元素小、大。不保证左右两部分自身排序
    '''
    tmp = li[left]
    while left < right:
        while left < right and li[right] >= tmp: 
            #以升序为例，从最右边开始找比被取出数tmp小的数
            #当被取出数右边全部都>=该数时，要退出循环，把被取出数放回原处，所以内循环设置left<right
            right -= 1
        li[left] = li[right] #当在右边找到比被取数小的数字或者根本没找到比它小的数字触发left=right退出循环后，进行换位(left<right)或者保持原样(left=right时)
        print(li, '从右往左找第一个比', tmp, '小的') #在每次右向左换完后打印一次
        while left < right and li[left] <= tmp: #这里要<=tmp因为left初始是0，第0个位置的元素不参与排序
            left += 1
        li[right] = li[left]
        print(li, '从左往右找第一个比', tmp, '大的') #在每次左向右换完后打印一次
    li[left] = tmp #当left = right后把一开始被取数tmp放到最后的空位上
    return left #返回最后空出来的位置，也就是tmp被归位的位置
li = [random.randint(0, 10) for i in range(10)]
print(li)
partition(li, 0, len(li)-1)
print(li)

def quick_sort(data, left, right):
    '''
    原理：排序在无序区进行。取一个元素（第一个元素）；对其进行归位操作---该元素左边的
        数比它小，右边比它大。当某次归位后左边的元素个数<=1，该元素及其左边的所有元素
        成为有序区。
    left:无序区最左边元素的index, 也是下一个被归位对象所在的初始位置。这个无序区是指
    被归位元素分割的两个无序部分部分：有序区,left~mid,mid~right,有序区时间复杂度：
    O(nlogn)，每个partition的复杂度是O(n),因为partition是两边收缩所以尽管有循环但复
    杂度还是n不是n^2。然后假设每次partition都是对半开，那么就要做log2(n)次partition,
    所以最终时间复杂度是O(nlogn)快速排序最坏情况：升序快排去做倒序list，时间复杂度
    =O(N^2),这时只需要打乱list顺序即可，用random.shuffle(li)
    '''
    if left < right: #left < right说明无序区至少有两个元素，left = right说明无序区只有一个元素
        mid = partition(data, left, right) #将第一个元素归位, 返回归位位置mid
        quick_sort(data, left, mid-1)
        quick_sort(data, mid+1, right)
li = [random.randint(0, 10) for i in range(10)]
print(li)
quick_sort(li, 0, len(li)-1)
print(li)
'''------------------------------------------------------------------------'''

#堆排序
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=23&spm_id_from=pageDriver
堆是一种特殊的完全二叉树。特殊体现在其分为大根堆：一颗完全二叉树，满足任意节点都比其子
节点大；小根堆：一颗完全二叉树，满足任意节点都比其子节点小。满足大、小根堆的条件才能被
叫做"堆"。
★堆排序利用了堆的向下调整性，将不是"堆"的二叉树，通过将上层不符合"堆"要求的节点往下调
整，将其变成"堆"。
★堆排序的原理：先构造一个初始"堆"。然后将最顶端的数字取出，作为最大/最小值。这样空出一个
位置，将最下层最右边的子节点放到顶端空位，底下的空位交给顶端被取出的数字，并将其排除在
之后的堆外（避免另外开一个新的数据结构存储浪费内存）。进行向下调整，再次变成特殊的完全
二叉树，这时再将顶端数值取出作为第二大/第二小的数。以此类推。
★如何构造初始堆：从最下层最右侧子节点开始，下上交换（大根数大换小，小根数小换大）。每
层节点从右往左遍历。
'''
def sift(li, low, high):
    '''
    这是建立大根堆的sift
    作用:对low位置元素进行一次向下调整函数（即将low位置的数字进行一次向下调整，即在下
    几层层寻找有没有合适的位置知道安顿好被移动的数字。当中涉及到low节点下多个父子节点
    的互相换位，但这些换位的目的都是为了满足将low放下去且保证是大根堆）。这里是将大数放上来。
    high = 堆的最后一个元素的下标index
    low = 堆的第一个元素，堆顶（根节点）index
    函数时间复杂度: O(Logn), 因为二叉树走了一边就不考虑另一边，实际上走的是二叉树的高度 = Log2(n)
    '''
    #i, j是待换位的两个节点位置。i是父节点，j是左子节点
    i = low
    j = 2 * i + 1 #先查看左子节点j
    tmp = li[low] #把堆顶的数存起来
    while j <= high: #只要j位置没超过最后一个节点的index就继续
        if j + 1 <= high and li[j+1] > li[j]: #如果存在右子节点且右子节点>左子节点
            j += 1 #把指针j指向右子节点（以大根堆案例为例，即排倒叙）---不能直接换左右子节点数值，因为不能保证更换完之后原本左子节点比右子节点的子节点大(在大根堆例子中，小根堆例子中相反)
        if li[j] > tmp:
            li[i] = li[j] #向下调整
            #跟新i, j到下一层子结点中继续上述操作，进入新循环
            i = j 
            j = 2 * i + 1
        else: #tmp更大，tmp放到空出的当前i位置上
            li[i] = tmp
            break #当发生li[i] = tmp时，下面没有向下调整的必要了,下面的数全比tmp小(大根堆案例)。
    else: #while...else是一个整体模块，所以当while内出发到break，则不会出发while...else的else
        li[i] = tmp #当i调整下移到当前节点i下没有子节点的时候，把tmp放到空出的当前i节点位置。
        
def heap_sort(li):
    #堆排序不需要递归,实际表现没有快速排序快，但堆排序有其他用处
    '''
    堆排序公式, 这里是实现的是从小到大排序,实现的是大根堆
    时间复杂度：O(nlogn)
    '''      
    n = len(li) #n为总节点数, n-1为最后一个子节点的下标
    for i in range(((len(li)-1)-1)//2, -1, -1): 
        '''
        从最下面最后一个父节点开始，比较其子节点与其大小，并逐步往左，再逐步向上地查看
        每个父节点有必要跟它们的子节点交换吗，将堆整理成大根堆(这里是大根堆)。
        无论左、右子节点，它们的父节点都能用(i-1)//2表示。这里从最后一个父节点index递
        减到0号位(根节点)
        '''
        sift(li, i, n-1)
        '''
        这里之所以能直接将sift中high参数设置为n-1, 是因为sift函数本身的作用就是给low
        位置的元素在其下层找到一个合适的位置。在sift中，high参数扮演的是避免low位置要
        进行换位的元素跟不存在的节点互动。而"堆"是特殊的完全二叉树，它可以视作从左到右
        、自上而下的铺上元素，第三层有元素，第三层最后一个元素左边以及第二层一定铺满元
        素。所以sift中只要把high设置为最后一个节点的index，其执行就不会报错。
        '''
    #建立初始堆至此完成完成
    #下面对"初始堆"进行排序
    '''
    将初始堆最上面的数字和最后一个子节点的数字交换，视作找到最大数。再把high指针(指示堆
    末尾index的指标)往前移，减少堆的一个末尾节点，该节点让给已经排出大小的初始堆嘴上面
    的数字了，已经是有序区了。然后对交换根节点、末子节点的堆再次进行向下调整，找出第二个
    最大值，以此类推...
    '''
    for j in range(n-1, -1, -1):
        #j一直指向堆无序区的最后一个子节点位置
        li[0], li[j] = li[j], li[0] #将堆顶与堆无序区最后一个节点位置交换
        sift(li, 0, j-1) #j-1是堆无序区最后一个节点的位置，因为原本最后一个节点j给了找到的极值，变成了有序区
        #当无序区只剩一个元素，其index = 0. 这时候high = 0, sift()中j+1 > high跳出循环完成排序

li = [random.randint(0, 10) for i in range(10)]
print(li)
heap_sort(li)
print(li)

#堆排序内置模块
import heapq

li = list(range(100))
li_sort = []
random.shuffle(li)

heapq.heapify(li) #建小根堆
print(li)
for i in range(len(li)):
    li_sort.append((heapq.heappop(li))) #往外弹出一个最小元素（小根堆每次选出来的有序区，即堆的最小值）

#堆排序---topk问题(取前k个极值，k<n)
'''
常见方法
排序后切片:O(nlogn)
冒泡、插入、选择排序: O(kn)
堆排序：nlogk---去列表前k个数建立一个小根堆，堆顶就是目前第k大的数。依次向后遍历原列表
       对于列表中的元素，如果小于堆顶，则忽略该元素；如果大于堆顶，则将堆顶更换为该元素，
       并对堆做一次调整，使其再次成为小根堆。当遍历完列表后，小根堆里的数就是前k大的数。
nlogk < kn < nlogn，特别当n很大的时候，堆排序选前k个值更快。
'''
def sift_small(li, low, high):
    '''
    这是建立小根堆的sift
    '''
    i = low
    j = 2 * i + 1 
    tmp = li[low] 
    while j <= high: 
        if j + 1 <= high and li[j+1] < li[j]: #这里and后换成<，是与大根堆sift的区别
            j += 1 
        if li[j] < tmp: #这里换成<，是与大根堆sift的区别
            li[i] = li[j] 
            i = j 
            j = 2 * i + 1
        else: 
            li[i] = tmp
            break 
    else: 
        li[i] = tmp
        
def topk(li, k):
    #建小根堆
    heap = li[0:k]
    for i in range(((k-1)-1)//2, -1, -1):
        sift_small(heap, i, k-1)
    #遍历列表中剩下n-k个元素，如果比小根堆堆顶的大，替换小根堆堆顶
    for i in range(k, len(li)):
        if li[i] > heap[0]:
            heap[0] = li[i]
            sift_small(heap, 0, k-1)
    #出数
    for j in range(k-1, -1, -1):
        heap[0], heap[j] = heap[j], heap[0]
        sift_small(heap, 0, j-1)
    return heap

li = [random.randint(0, 10) for i in range(10)]
print(li)
li = topk(li, 3)
print(li)
'''------------------------------------------------------------------------'''

#归并排序
'''
这是python里排序用到的方法sort是归并排序+插入排序，他于前几种方法不同，不是原地排序，需要新建列表ltmp放入排序数字
原理：一个列表两段有序，从两段数字最左侧开始分别比较每段内最左侧数字大小，并将较小方放
到新列表的前端。以此类推
'''
def merge(li, low, mid, high):
    '''
    归并函数, 将两个有序段合成一个有序段
    一次归并时间复杂度：O(n)
    low是第一段有序字段第一位index
    mid是第一段有序字段最后一位index
    high是第二段有序字段最后一位index
    '''
    i = low
    j = mid + 1
    ltmp = []
    while i <= mid and j <= high: #只要左右两段有序区都有数
        if li[i] < li[j]:
            ltmp.append(li[i]) #list.append时间复杂度是O(1)
            i += 1
        else:
            ltmp.append(li[j])
            j += 1
    #上一个while执行完后，一定有一段数字被消耗完，这时只要将多出来的字段直接放入ltmp就好，因为它们本身各自就是有序的
    while i <= mid:
        ltmp.append(li[i])
        i += 1
    while j <= high:
        ltmp.append(li[j])
        j += 1
    #这里之所以写low. high进行切片写入是因为后面可能有递归，所以不从0开始
    li[low:high+1] = ltmp #切片操作li[a:b]是index且包前不包后, 这里li[low:high+1]是对index=low~high部分进行切片

li = [1, 2, 6, 1, 3,5]
merge(li, 0, 2, 5)
print(li)

def merge_sort(li, low, high):
    '''
    归并排序前提：制造分段有序list。要实现它就得把原始的list进行分解。分解成小列表，
    这个小列表有1个或者0个元素，总的目的是构成若干个有序小列表(有序段)。然后进行递归。 
    整个过程其实就是把整个过程看成有限个三部曲：归并左边被分解的小列表使其成为有序段，归并
    右边被分解的小列表使其成为有序段。归并左右两个有序段。
    时间复杂度:O(n*logn),每层一次merge，复杂度是n，有logn层
    low:最左边元素index
    high:最右边元素index
    '''
    if low < high: #至少有两个元素, 进行递归
        mid = (low + high) // 2 #将大列表进行拆解，一分为二。
        merge_sort(li, low, mid) #将左小列表进行拆解一分为二，不停递归直到拆分后小段只有0~1个元素。
        merge_sort(li, mid+1, high) #将右小列表进行拆解一分为二，不停递归直到拆分后小段只有0~1个元素。
        merge(li, low, mid, high) #将左右两段小段有序段进行归并成为一个大列表。
        #merge在递归中不停运行，将2个各含1个元素的小列表进行归并，然后将2个各含2个元素的小列表进行归并，知道最后完成大列表的归并。
        print(li[low: high+1])

li = list(range(10))
random.shuffle(li)
print(li)
merge_sort(li, 0, len(li)-1)   
'''------------------------------------------------------------------------'''

#三种NB排序总结
'''
时间复杂度都是O(nlogn)
运行时间：快速排序<归并<堆排序
三种排序的优缺点：
快速排序-快，但是极端情况下效率低（如倒叙list进行顺序排序），解决方法：将这种情况第一
        个数与随机一个数互换。 空间复杂度：O(logn)，因为递归时是一层层往下深入，
        系统需要记录上一层开始递归位置，没记录一次花费O(1)复杂度。平均走logn层所以平
        均空间复杂度是O(logn)。最坏情况走n层，空间复杂度是O(n)（给倒序list顺序排序的时候）
归并排序-不是原地排序，需要额外内存，空间复杂度：O(n)，因为递归时是一层层往下深入，
        系统需要记录上一层开始递归位置，没记录一次花费O(1)复杂度,走logn层，所以归并中
        递归的空间复杂度是O(logn)。但是归并本身就已经开了一个长度为n的新list，O(n)>
        O(logn),所以取大，归并排序空间复杂度是O(n)
堆排序：在三种排序中最慢, 空间复杂度O(1)
''' 
'''------------------------------------------------------------------------'''
'''------------------------------------------------------------------------'''

#希尔排序
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=34
由插入排序演变，为分组插入排序。
时间复杂度: 与每个轮次的gap值有关，比较复杂。比堆排序慢，比插入排序快
'''
def insert_sort_gap(li, gap):
    for i in range(gap, len(li)):
        tmp = li[i]
        j = i - gap #这里是每跨gap个数进行插入排序
        while j >= 0 and li[j] > tmp:
            li[j+gap] = li[j]
            j -= gap
        li[j+gap] = tmp

def shell_sort(li):
    d = len(li) // 2
    while d >= 1: #d就是gap值, 当d = 1，说明此时就剩1个数了，1//2 = 0，结束排序
        insert_sort_gap(li, d)
        d //= 2
        
li = list(range(10))
random.shuffle(li)
shell_sort(li)
'''------------------------------------------------------------------------'''

#计数排序
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=36&spm_id_from=pageDriver
上面的都是比较排序。计数排序与比较排序不同，比较排序最快的时间复杂度也是O(nlogn)
前提：已经知道待排序数字的具体可能值eg:0~100间的整数。
原理：计数以统计信息，然后再用统计完的计数表为信息源建表排序
而且会额外创建一个列表，占用更多内存
'''
def count_sort(li, max_count = 100):
    '''
    已知要排序的数字范围是0~100的int
    '''
    count = [0 for _ in range(max_count+1)] #创建0~100的列表
    for val in li:
        count[val] += 1
    li.clear() #清空list
    #按照计数信息进行排序,这两层循环时间复杂度是O(n)不是O(n^2),因为两层循环其实指示把n个数字全部重新填写了一遍。O(外循环)*O(内循环)=O(n)
    for ind, val in enumerate(count):
        for i in range(val):
            li.append(ind)

li = list(range(10))
random.shuffle(li)
count_sort(li)
'''------------------------------------------------------------------------'''

#桶排序
'''
是计数排序的优化。计数排序可能面临一个很大的范围，导致内存占用大。桶排序将元
素按照范围放到多个桶里，让每个桶里的元素保持有序。
时间复杂度：取决于数据分布。因为划分每个桶收纳多少数是均匀的，而当数据分布99%落到90~100，
则99%的数据都进入了最后一个桶，桶里的数据就多了，效率就变成了计数排序。平均为O(n+k)，最
坏为(n^2 *k)
空间复杂度：O(nk)
'''
def bucket_sort(li, n=100, max_num=10000):
    '''
    n为桶个数0~99（0~n-1）
    max_num为最大数
    '''
    buckets = [[] for _ in range(n)] #创建一个n个桶的列表，每个桶又是一个列表。所以这是二位列表
    #保证所有桶都有序
    for var in li:
        i = min(var // (max_num // n), n-1) 
        #i表示var放到几号桶里
        #var // (max_num//n)表示var放到几号桶里，但是当var = max_num时会导致算下来超出桶index99,所以要min(..., n-1)
        buckets[i].append(var) #把var加入到对应的桶里
        #保持桶里的数据
        for j in range(len(buckets[i])-1, 0, -1):
            if buckets[i][j] <buckets[i][j-1]:
                buckets[i][j-1], buckets[i][j] = buckets[i][j], buckets[i][j-1]
            else:
                break #因为只要按照这个j循环放入的数字，一定是有序的。所以如果新放入的数字连前一个数都没必要比的话，就更没必要更之前的数字比了
    #将全部排好序的桶挨个输出
    sorted_li = []
    for buc in buckets: #buc是一个桶，是列表
        sorted_li.extend(buc) #extend是将list内元素加到sorted_li中而非整个桶，这是与append的区别
    return sorted_li

li = list(range(10000))
random.shuffle(li)
li = bucket_sort(li)
'''------------------------------------------------------------------------'''

#基数排序
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=39
原理：把数字按照不同位数去看。与桶排序不同的是基数排序装多次桶且不在桶内排序。
时间复杂度: O(kn), 是线性时间复杂度。因为内循环是O(n), while外循环是k,取决于最大数有
多少位k, k = log(10, max_num)。而快速排序是O(n*log2(n)),log2(n)与log(10, max_num)
的大小取决于最大数的位数。所以当最大数很大时，快排比基数排序快。
空间复杂度:O(k+n)
'''
def radix_sort(li):
    max_num = max(li) #确定最大值，若999按位数做3次，若88按照位数做2次..
    it = 0
    while 10 ** it <= max_num:
        #按个位向十位，继续向前的顺序取数。每次都要清空buckets放不同的位数
        buckets = [[] for _ in range(10)] #桶的数量固定=10，因为每个位数上的数字是0~9
        for var in li:
            digit = (var // (10 ** it)) % 10 #%表示对10取余
            buckets[digit].append(var) #10个桶分别编号是0~9，对应取出位数上的数digit
        #数字按一个位数分桶完成
        li.clear()
        for buc in buckets:
            li.extend(buc) #把数字重新写回li，这列用buc extend，将buc中的元素放入到li中
        it += 1 

li = list(range(10000))
random.shuffle(li)
radix_sort(li)