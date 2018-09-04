from zeep import Client

def sendSMS(list, text):
    client = Client(wsdl='http://api.payamak-panel.com/post/Send.asmx?wsdl')
    if len(list) // 100 == len(list) / 100:
        t = (len(list) // 100)
    else:
        t = (len(list) // 100) + 1
    for i in range(0, t):
        b = ""
        for j in range(0, 100):
            if (j + (i * 100)) == len(list):
                break
            if j == 0:
                b = b + str(list[j + (i * 100)])
            else:
                b = b + "," + str(list[j + (i * 100)])
        client.service.SendSimpleSMS2('9174486355', '3496', b, '50002016008706', text, False)

