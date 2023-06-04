#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>
#include "const.h"

using namespace omnetpp;

class Net : public cSimpleModule
{
private:
    cStdDev HopCount;

    // 0: clockwise, 1: counterclockwise
    bool preferredOutInterface;

public:
    Net();
    virtual ~Net();

protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

Net::Net()
{
}

Net::~Net()
{
}

void Net::initialize()
{
    HopCount.setName("hop count");

    // initialize with invalid interface value
    preferredOutInterface = -1;

    Packet *hello_pkt = new Packet();

    hello_pkt->setKind(KIND_HELLO);
    hello_pkt->setByteLength(20);

    hello_pkt->setSource(this->getParentModule()->getIndex());
    hello_pkt->setDestination(DEST_NODE);

    hello_pkt->setHopCount(0);

    send(hello_pkt, "toLnk$o", REC_LNK);
}

void Net::finish()
{
    recordScalar("average hop count", HopCount.getMean());
}

void Net::handleMessage(cMessage *msg)
{

    // All msg (events) on net are packets
    Packet *pkt = (Packet *)msg;

    // If this node is the final destination, send to App
    if (pkt->getDestination() == this->getParentModule()->getIndex())
    {
        send(msg, "toApp$o");

        // record as vector de la cantidad de hops de ese paquete
        HopCount.collect(pkt->getHopCount());
    }
    // If not, forward the packet to some else... to who?
    else
    {
        // We send to link interface #0, which is the
        // one connected to the clockwise side of the ring
        // Is this the best choice? are there others?
        send(msg, "toLnk$o", 0);

        // increment hop count
        pkt->setHopCount(pkt->getHopCount() + 1);
    }
}
