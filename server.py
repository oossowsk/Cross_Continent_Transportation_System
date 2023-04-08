import pika
import sys 
import re
import copy
weightList = list()

def waitOnNodeResponse(ch, method, properties, body):
    global weightList
    global channel
    print(" [x] Received %r" % body)
    body = body.decode("utf-8")
    weightList = stringToList(body)
    channel.stop_consuming()
    return

def dijsktraSearch(startNode,endNode,weight):
    global graph
    global weightList
    global channel
    # path dict format is
    # key = destingation
    # value is new dict with 4 keys
    #   source -> source node
    #   time -> time taken to reach 
    #   weight -> weight capacity of link before use
    #   transportType -> type of transport used
    pathDict = dict()
    # keep track of previously visited nodes
    usedDict = dict()
    minDist = dict()

    minDist[startNode] = 0
    minDist[endNode] = -1

    current = startNode
    
    while(not current is None):
        # update queue for current node
        # send format -- weight 
        message = str(weight)
        channel.basic_publish(exchange='', routing_key=str(current), body=message)
        # wait on response from queue on current node
        channel.basic_consume(queue=str(current)+"_response", on_message_callback=waitOnNodeResponse, auto_ack=True)
        channel.start_consuming()
        # return format -- [destLoc1;destTime1;destWeight1;outGoingNodes1],[destLoc2;destTime2;destWeight2;outGoingNodes2]

        destinationList = weightList
        #print("Weightlist recieved from node = " + str(current))
        #print(destinationList)
        for node in destinationList:
            #print("Node recieved = ")
            #print(node)
            destLoc = node[0]
            destTime = node[1]

            # time is equal to transport time + all before time
            destTime = destTime + minDist[current]

            destWeight = node[2]
            destTransportType = node[3]
            update = False
            # if this is closest path to destLoc found so far
            # also make sure that the wieght isnt more than the current closest path to endNode
            if (destWeight >= weight):
                if (destLoc in minDist):
                    if ((destTime < minDist[destLoc] or minDist[destLoc] == -1) and (destTime < minDist[endNode] or minDist[endNode] == -1)):
                        update = True
                else:
                    update = True
            
            if (update):
                    # add the node to the path dict if it doesnt already exist
                    if destLoc not in pathDict:
                        pathDict[destLoc] = dict()
                    # populate the path dict with the new data
                    pathDict[destLoc]['source'] = current
                    # for time we want to keep only the distance from current to destLoc instead of from start node to destLoc
                    # current to destLoc is instead stored in minDist[destLoc]
                    pathDict[destLoc]['time'] = node[1] 
                    pathDict[destLoc]['weight'] = destWeight
                    pathDict[destLoc]['transportType'] = destTransportType
                    minDist[destLoc] = destTime
        
        # add current to usedDict
        usedDict[current] = 1
        # update current to smallest unused non negative numeber in minDist
        min = -1
        tempSmallestDistanceNode = None
        #print("MinDist")
        #print(minDist)
        for idx in minDist:
            #print(idx)
            node = minDist[idx]
            #print("Index currently considered = " + str(idx))
            #print("Distance to the index = " + str(node))
            # skip if node already used
            if (idx in usedDict):
                #print("skipping " + str(idx))
                continue
            # check if it is smaller than current min dist
            if ((node < min or min == -1) and (node >= 0 )):
                min = node
                tempSmallestDistanceNode = idx
        

        current = tempSmallestDistanceNode
        #print("Current node to explore = " + str(current))
        #print("EndNode = " + str(endNode))
        # if current is endNode then break out as we cant find any short paths to it
        if (current == endNode):
            break

    if (minDist[endNode] != -1):
        # update graph based on values
        traverseNode = endNode
        # graph[1] = [[2,40,100,'p'],[4,70,150,'t']]
        #traverseNode = pathDict[traverseNode]['source']
        #prevTraverse = traverseNode
        #traverseNode = pathDict[traverseNode]['source']
        graphTmp = copy.deepcopy(graph)
        while(traverseNode != startNode):
            #print("TraverseNode = " + str(traverseNode))
            prevTraverse = traverseNode
            traverseNode = pathDict[traverseNode]['source']
            for idx,path in enumerate(graphTmp[traverseNode]):
                #print("path = ")
                #print(path)
                #print("Path dict = ")
                #print(pathDict[prevTraverse])
                if (path[0] == prevTraverse and path[1] == pathDict[prevTraverse]['time'] and path[2] == pathDict[prevTraverse]['weight'] and path[3] == pathDict[prevTraverse]['transportType']):
                    #print("Update graph")
                    #print(graph[traverseNode][idx][2] - weight)
                    graph[traverseNode][idx][2] = int(graph[traverseNode][idx][2] - weight)
            
        # send all in path list to update node
        updateNodes(graph)
        #print("updated graph = ")
        #print(graph)
    return pathDict, minDist

def stringToList(tmpStr):
    # conver string back to list
    stringArr = tmpStr.split("],")
    for idx,val in enumerate(stringArr):
        print(stringArr[idx])
        stringArr[idx] = re.sub(r'(\[*)', r'', stringArr[idx])
        stringArr[idx] = re.sub(r'(\]*)', r'', stringArr[idx])
        stringArr[idx] = re.sub(r'\s*', r'', stringArr[idx])
        stringArr[idx] = re.sub(r'\'', r'', stringArr[idx])
        stringArr[idx] = stringArr[idx].split(',')
        stringArr[idx][0] = int(stringArr[idx][0])
        stringArr[idx][1] = int(stringArr[idx][1])
        stringArr[idx][2] = int(stringArr[idx][2])

    return stringArr

def updateNodes(graphNew):
    global channel
    global graph
    graph = graphNew
    # make queues
    for i in range(len(graphNew)):
    #    # queue to trigger dijkstra search on the node
        channel.queue_declare(queue=str(i))
        # queue to get result back
        channel.queue_declare(queue=str(i)+"_response")
        # queue to update nodes with proper data
        channel.queue_declare(queue=str(i) + "_values")

        outGoingNodes = str(graphNew[i])
        channel.basic_publish(exchange='', routing_key=str(i) + "_values", body=outGoingNodes)

def createPikaConnections():
    global channel
    # create rabbitmq conenctions 
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    tmpStr = str(graph[0])
    tmpList = list(tmpStr)

def returnGraph():
    global graph
    return graph

graph = dict()
graph[0] = [[1,10,34,'p'],[2,100,1000,'s']]
graph[1] = [[2,40,100,'p'],[4,70,150,'t']]
graph[2] = [[3,10,80,'p'],[5,60,100,'t']]
graph[3] = [[4,50,20,'t'],[1,54,32,'t']]
graph[4] = [[5,5,100,'p'],[5,30,1000,'s']]
graph[5] = [[2,30,10,'p'],[0,50,50,'t']]

createPikaConnections()
updateNodes(graph)

if __name__ == '__main__':
    # run dijstra search using distributed nodes
    pathDict, minDist = dijsktraSearch(0,2,30)
    print("Path and min dist")
    print(pathDict)
    print(minDist)

    print("New graph = ")
    print(graph)

    pathDict, minDist = dijsktraSearch(0,2,30)
    print("Path and min dist")
    print(pathDict)
    print(minDist)

    print("New graph = ")
    print(graph)

#https://pika.readthedocs.io/en/latest/modules/adapters/blocking.html?highlight=start_consuming

