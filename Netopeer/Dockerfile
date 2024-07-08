FROM sysrepo/sysrepo-netopeer2:latest
RUN ssh-keygen -A && ssh-keygen -t dsa -P '' -f /home/netconf/.ssh/id_dsa && cat /home/netconf/.ssh/id_dsa.pub > /home/netconf/.ssh/authorized_keys
COPY ietf-interfaces@2018-02-20.yang /opt/dev/sysrepo/modules
COPY iana-if-type@2017-01-19.yang /opt/dev/sysrepo/modules
COPY ieee802-types@2020-10-23.yang /opt/dev/sysrepo/modules
COPY ieee802-dot1q-types@2023-08-29.yang /opt/dev/sysrepo/modules
COPY ieee802-dot1q-sched@2021-04-09.yang /opt/dev/sysrepo/modules
COPY ieee802-dot1q-bridge@2021-04-09.yang /opt/dev/sysrepo/modules
COPY ietf-interfaces@2018-02-20.yang /opt/dev/Netopeer2/modules
COPY iana-if-type@2017-01-19.yang /opt/dev/Netopeer2/modules
COPY ieee802-types@2020-10-23.yang /opt/dev/Netopeer2/modules
COPY ieee802-dot1q-types@2023-08-29.yang /opt/dev/Netopeer2/modules
COPY ieee802-dot1q-sched@2021-04-09.yang /opt/dev/Netopeer2/modules
COPY ieee802-dot1q-bridge@2021-04-09.yang /opt/dev/Netopeer2/modules
COPY Netopeer/qbv_config_1.xml /opt/dev/Netopeer2/example_configuration
RUN sysrepoctl --install /opt/dev/Netopeer2/modules/ietf-interfaces@2018-02-20.yang
RUN sysrepoctl --install /opt/dev/Netopeer2/modules/iana-if-type@2017-01-19.yang 
RUN sysrepoctl --install /opt/dev/Netopeer2/modules/ieee802-types@2020-10-23.yang
RUN sysrepoctl --install /opt/dev/Netopeer2/modules/ieee802-dot1q-types@2023-08-29.yang 
RUN sysrepoctl --install /opt/dev/Netopeer2/modules/ieee802-dot1q-bridge@2021-04-09.yang 
RUN sysrepoctl --install /opt/dev/Netopeer2/modules/ieee802-dot1q-sched@2021-04-09.yang --enable-feature "scheduled-traffic"

