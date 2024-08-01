## Probelm encouterred 

* Wifi Module does not connect immedimately

    At first, not sure what is the problem.  It connects within 5 seconds but often need to retry for many times.  

    After printing out the status code and check the meaning of the code, now thinking the wifi.connect() function may need time to establish the connection.   

* mqtt

    Using the default micropython library umqtt.simple since here just need a simple subscriber to get the messages from MQ.  

    Since new to this library, encountered 2 issues:

    1. waitmsg() is a synchronous function and blocking the app

        Check the document and it says waitmsg() is blocking while chechmsg() isn't.  

    2. The connection disconnected after a while

        According to some pages on Internet, need to either:

        a) set the keep-alive parameters, or

        b) the client need to constantly ping the server using client.ping()

    * There are also people saying if need a reliable mqtt library, could try :
    
        https://github.com/peterhinch/micropython-mqtt
    
    * Useful guide:

        https://dev.to/codemee/micropython-umqtt-2p5e

    * For library reference:

        https://mpython.readthedocs.io/en/v2.2.1/library/mPython/umqtt.simple.html

Tried with umqtt.robust, turns out when wifi is disconnected, umqtt.robust.connect() will become an infinite loop.  So decided to go back and using umqtt.simple.  However, what happened before (without keepalive and ping) doesn't happen any more.  No exception but also doesn't receive any message from mq

