from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import uvicorn
import pydantic
import server
import copy


# api endpoints:

# Create order -- Frontend sends start, end, weight and email -- Backend sends path comma separated and total travel time
# Login (email only) -- frontend sends email -- backend returns success
# View order -- Frontend sends request with email -- backend sends all done requests
# Update graph -- Sends graph to backend to update nodes

app = FastAPI()

templates = Jinja2Templates(directory="")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class createOrderRequest(pydantic.BaseModel):
    email: str
    start: int
    end: int
    weight: int


class emailRequest(pydantic.BaseModel):
    email: str


class deleteOrderRequest(pydantic.BaseModel):
    email: str
    orderId: int


class addNodePathRequest(pydantic.BaseModel):
    nodeNum: int
    endNode: int
    pathTime: int
    pathWeight: int
    pathType: str


class createNodeRequest(pydantic.BaseModel):
    nodeNum: int


class deleteNodeRequest(pydantic.BaseModel):
    nodeNum: int


userOrders = dict()


@app.get('/')
# client sends over start, end, weight and email
# return is route and total time
async def default(request: Request):
    # return {"default": "test"}
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get('/trackOrder')
# client sends over start, end, weight and email
# return is route and total time
async def trackOrder(request: Request):
    # return {"default": "test"}
    return templates.TemplateResponse("order.html", context={"request": request})


@app.get('/viewOrderInfo')
# client sends over start, end, weight and email
# return is route and total time
async def viewOrderInfo(request: Request):
    # return {"default": "test"}
    return templates.TemplateResponse("user_home.html", context={"request": request})


@app.post('/createOrder')
# client sends over start, end, weight and email
# return is route and total time
async def createOrder(request: createOrderRequest):
    global userOrders

    startNode = request.start
    endNode = request.end
    nodeWeight = request.weight
    email = request.email
    # print(request.dict())

    pathDict, minDist = server.dijsktraSearch(startNode, endNode, nodeWeight)
    currentNode = endNode
    totalTime = 0
    returnDict = dict()
    print("Min dist = ")
    print(minDist)
    if (minDist[endNode] != -1):
        while (currentNode != startNode):
            totalTime = totalTime + pathDict[currentNode]['time']
            returnDict[currentNode] = pathDict[currentNode]
            currentNode = pathDict[currentNode]['source']
        returnDict['weight'] = nodeWeight

        if (not email in userOrders):
            userOrders[email] = list()
            userOrders[email].append(-1)

        userOrders[email][0] = userOrders[email][0] + 1
        returnDict['id'] = userOrders[email][0]
        returnDict['endNode'] = endNode
        returnDict['startNode'] = startNode
        userOrders[email].append(returnDict)

        return {'Route': returnDict, 'time': totalTime}
    else:
        return {'Route': "None", 'time': -1}


@app.post('/login')
# gets email and checks if it exists in database and if not registers it
# returns either login or register depending on the action done
async def login():
    resp = ""
    return {'response': resp}


@app.post('/viewOrders')
# gets email from frontend and return all current orders
async def viewOrder(request: emailRequest):
    global userOrders
    email = request.email
    if (email in userOrders):
        return {'orders': userOrders[email]}
    else:
        return {'orders': 'Fail user has no orders'}


@app.get('/getGraph')
# gets node id and path to add to it and updates all nodes
async def getGraph():
    graph = server.returnGraph()
    return {'Graph': graph}


@app.post('/addNodePath')
# gets node id and path to add to it and updates all nodes
async def addNodePath(request: addNodePathRequest):
    startNode = request.nodeNum
    endNode = request.endNode
    nodeWeight = request.pathWeight
    pathType = request.pathType
    pathTime = request.pathTime
    graph = server.returnGraph()
    # add path to graph
    if (not startNode in graph):
        graph[startNode] = list()

    graph[startNode].append([endNode, pathTime, nodeWeight, pathType])
    print(graph)
    server.updateNodes(graph)

    return {'status': 'success'}

# to-do


@app.post('/deleteOrder')
# gets email and order from frontend and removes it from the database and updates all the workers, returns
async def deleteOrder(request: deleteOrderRequest):
    email = request.email
    orderId = request.orderId
    status = removeOrder(email, orderId)

    return {'status': status}

# remove order and update graph to add back weight capacity


def removeOrder(email, order):
    global userOrders
    graph = server.returnGraph()
    # check if user has any orders
    if (not email in userOrders):
        return "Fail no orders for this user"

    usePath = -1
    # find if order exists for user
    for idx, val in enumerate(userOrders[email]):
        if (type(userOrders[email][idx]) == type(dict())):
            if (userOrders[email][idx]['id'] == order):
                usePath = idx
    # fail if order does not exist
    if (usePath == -1):
        return "Fail order id invalid for given user"

    print(userOrders[email][usePath]['id'])
    # update graph to remove order
    endNode = userOrders[email][usePath]['endNode']
    startNode = userOrders[email][usePath]['startNode']
    currentNode = endNode
    while (currentNode != startNode):
        prevTraverse = currentNode
        currentNode = userOrders[email][usePath][currentNode]['source']
        graphTmp = copy.deepcopy(graph)
        for idx, path in enumerate(graphTmp[currentNode]):
            if (path[0] == prevTraverse and path[1] == userOrders[email][usePath][prevTraverse]['time'] and path[3] == userOrders[email][usePath][prevTraverse]['transportType']):
                print("updating weights for node = " + str(currentNode))
                print(graph)
                print(graph[currentNode])
                print(graph[currentNode][idx])
                graph[currentNode][idx][2] = int(
                    graph[currentNode][idx][2] + userOrders[email][usePath]['weight'])
    # delete order
    del userOrders[email][usePath]
    # update nodes with new graph
    server.updateNodes(graph)
    status = 'success'
    return status


@app.post('/createNode')
# create a node based on id
async def deleteNode(request: createNodeRequest):
    nodeNum = request.nodeNum
    graph = server.returnGraph()
    if (nodeNum in graph):
        return {'status': 'Fail node already exists'}
    else:
        graph[nodeNum] = list()
        server.updateNodes(graph)
        return {'status': 'success'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
