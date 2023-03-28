import pika
import sys
import re

outGoing = list()

def stringToList(tmpStr):
    # conver string back to list
    stringArr = str(tmpStr).split("],")

    for idx,val in enumerate(stringArr):
        #print(stringArr[idx])
        stringArr[idx] = re.sub(r'(\[*)', r'', stringArr[idx])
        stringArr[idx] = re.sub(r'(\]*)', r'', stringArr[idx])
        stringArr[idx] = re.sub(r'\s*', r'', stringArr[idx])
        stringArr[idx] = re.sub(r'\'', r'', stringArr[idx])
        stringArr[idx] = stringArr[idx].split(',')
        stringArr[idx][0] = int(stringArr[idx][0])
        stringArr[idx][1] = int(stringArr[idx][1])
        stringArr[idx][2] = int(stringArr[idx][2])  
    return stringArr

def runDijkstras(weight):
    global outGoing
    outList = list()
    for node in outGoing:
        if (weight <= node[3]):
            outList.append(node)
    return outList
                    
def updateValues(outGoingList):
    global outGoing
    outGoing = outGoingList
    print("Current list of outgoing nodes")
    print(outGoing)

def callbackInstructions(ch, method, properties, body):
    global channel
    global nodeId
    print(" [x] Received %r" % body)
    # convert body to string from byte
    body = body.decode("utf-8")
    edgeList = runDijkstras(body)
    edgeString = str(edgeList)
    channel.basic_publish(exchange='', routing_key=str(nodeId) + "_response", body=edgeString)

def callbackUpdateValues(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # convert body to string from byte
    body = body.decode("utf-8")
    bodyList = stringToList(body)
    updateValues(bodyList)

# accept arg to get id
nodeId = int(sys.argv[1])
# create rabbitmq conenctions 
connection = pika.BlockingConnection(
pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# make queues
# get queue for instructions
channel.queue_declare(queue=str(nodeId))
# get queue to fillout values
channel.queue_declare(queue=str(nodeId) + "_values")
# get queue to send response values
channel.queue_declare(queue=str(nodeId) + "_response")

# wait on queue
channel.basic_consume(queue=str(nodeId), on_message_callback=callbackInstructions, auto_ack=True)
        
# wait on queue
channel.basic_consume(queue=str(nodeId) + "_values", on_message_callback=callbackUpdateValues, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
