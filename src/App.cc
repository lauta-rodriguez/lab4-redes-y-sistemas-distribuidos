#ifndef APP
#define APP

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>
#include "const.h"

using namespace omnetpp;

class App : public cSimpleModule
{
private:
    cMessage *sendMsgEvent;
    cStdDev delayStats;
    cOutVector delayVector;

    unsigned int sentPackets;
    unsigned int deliveredPackets;

public:
    App();
    virtual ~App();

protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(App);

#endif /* APP */

App::App()
{
}

App::~App()
{
}

void App::initialize()
{
    sentPackets = 0;
    deliveredPackets = 0;

    // If interArrivalTime for this node is higher than 0
    // initialize packet generator by scheduling sendMsgEvent
    if (par("interArrivalTime").doubleValue() != 0)
    {
        sendMsgEvent = new cMessage("sendEvent");
        scheduleAt(par("interArrivalTime"), sendMsgEvent);
    }

    // Initialize statistics
    delayStats.setName("TotalDelay");
    delayVector.setName("Delay");
}

void App::finish()
{
    // Record statistics
    recordScalar("Average delay", delayStats.getMean());
    recordScalar("Number of packets", delayStats.getCount());

    recordScalar("sent packets", sentPackets);
    recordScalar("delivered packets", deliveredPackets);
}

void App::handleMessage(cMessage *msg)
{

    // if msg is a sendMsgEvent, create and send new packet
    if (msg == sendMsgEvent)
    {
        // create new packet
        Packet *pkt = new Packet("packet", this->getParentModule()->getIndex());
        pkt->setByteLength(par("packetByteSize"));
        pkt->setSource(this->getParentModule()->getIndex());
        pkt->setDestination(par("destination"));

        pkt->setKind(KIND_DATA);

        // update statistics
        sentPackets++;

        // send to net layer
        send(pkt, "toNet$o");

        // compute the new departure time and schedule next sendMsgEvent
        simtime_t departureTime = simTime() + par("interArrivalTime");
        scheduleAt(departureTime, sendMsgEvent);
    }
    // else, msg is a packet from net layer
    else
    {
        // update statistics
        deliveredPackets++;

        // compute delay and record statistics
        simtime_t delay = simTime() - msg->getCreationTime();
        delayStats.collect(delay);
        delayVector.record(delay);
        // delete msg
        delete (msg);
    }
}
