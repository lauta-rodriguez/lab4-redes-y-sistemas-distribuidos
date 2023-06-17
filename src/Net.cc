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

    // length of the network
    int NET_LENGTH;

public:
    Net();
    virtual ~Net();

protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);

    virtual void handleDataPacket(Packet *data_pkt);
    virtual void handleHelloPacket(Packet *hello_pkt);
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
    NET_LENGTH = 0;

    Packet *hello_pkt = new Packet();

    hello_pkt->setKind(KIND_HELLO);
    hello_pkt->setByteLength(20);

    hello_pkt->setSource(this->getParentModule()->getIndex());
    hello_pkt->setDestination(DEST_NODE);

    hello_pkt->setHopCount(0);
    hello_pkt->setHopsToDestination(0);

    send(hello_pkt, "toLnk$o", REC_LNK);
}

void Net::finish()
{
    recordScalar("average hop count", HopCount.getMean());
}

void Net::handleDataPacket(Packet *data_pkt)
{
    assert(data_pkt->getKind() == 12);

    // If this node is the final destination, send to App
    if (data_pkt->getDestination() == this->getParentModule()->getIndex())
    {
        send(data_pkt, "toApp$o");

        // record as vector de la cantidad de hops de ese paquete
        HopCount.collect(data_pkt->getHopCount());
    }
    else // If not, forward the packet
    {
        // increment hop count
        data_pkt->setHopCount(data_pkt->getHopCount() + 1);
        send(data_pkt, "toLnk$o", (int)preferredOutInterface);
    }
}

void Net::handleHelloPacket(Packet *hello_pkt)
{
    // hello packet has returned to its source node
    if (hello_pkt->getSource() == this->getParentModule()->getIndex())
    {
        // the packet has completed a round and we now know the network length
        NET_LENGTH = hello_pkt->getHopCount();

        // if distance to destination is less than half the network length,
        // then the optimal interface is the same as the one used to send hello packets
        if (hello_pkt->getHopsToDestination() < NET_LENGTH / 2)
            preferredOutInterface = (int)REC_LNK;
        else // otherwise choose the other interface, because the topology is symmetrical
            preferredOutInterface = (int)!REC_LNK;

        delete (hello_pkt);
    }
    else // hello packet hasn't yet returned to its source node
    {
        if (hello_pkt->getDestination() == this->getParentModule()->getIndex())
            // set distance covered so far as distance to destination
            hello_pkt->setHopsToDestination(hello_pkt->getHopCount());

        // increment hop count
        hello_pkt->setHopCount(hello_pkt->getHopCount() + 1);

        // forward the packet
        send(hello_pkt, "toLnk$o", REC_LNK);
    }
}

void Net::handleMessage(cMessage *msg)
{

    // All msg (events) on net are packets
    Packet *pkt = (Packet *)msg;

    if (pkt->getKind() == KIND_DATA)
    {
        handleDataPacket(pkt);
    }
    else if (pkt->getKind() == KIND_HELLO)
    {
        handleHelloPacket(pkt);
    }
}
