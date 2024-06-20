#!/bin/sh

# Issue https://github.com/k3s-io/k3s/issues/5123
# Solution https://github.com/k3d-io/k3d/blob/main/pkg/types/fixes/assets/k3d-entrypoint-cgroupv2.sh

set -o errexit
set -o nounset

#########################################################################################################################################
# DISCLAIMER																																																														#
# Copied from https://github.com/moby/moby/blob/ed89041433a031cafc0a0f19cfe573c31688d377/hack/dind#L28-L37															#
# Permission granted by Akihiro Suda <akihiro.suda.cz@hco.ntt.co.jp> (https://github.com/k3d-io/k3d/issues/493#issuecomment-827405962)	#
# Moby License Apache 2.0: https://github.com/moby/moby/blob/ed89041433a031cafc0a0f19cfe573c31688d377/LICENSE														#
#########################################################################################################################################
if [ -f /sys/fs/cgroup/cgroup.controllers ]; then
  echo "[$(date -Iseconds)] [CgroupV2 Fix] Evacuating Root Cgroup ..."
	# move the processes from the root group to the /init group,
  # otherwise writing subtree_control fails with EBUSY.
  mkdir -p /sys/fs/cgroup/init
  busybox xargs -rn1 < /sys/fs/cgroup/cgroup.procs > /sys/fs/cgroup/init/cgroup.procs || :
  # enable controllers
  sed -e 's/ / +/g' -e 's/^/+/' <"/sys/fs/cgroup/cgroup.controllers" >"/sys/fs/cgroup/cgroup.subtree_control"
  echo "[$(date -Iseconds)] [CgroupV2 Fix] Done"
fi

# Enable k3s to resolve docker DNS (k3s can connect to postgres that is outside the cluster but in docker compose)
# Source https://github.com/corneliusludmann/k3s-docker-compose-dns

# Add IP tables rules to access Docker's internal DNS 127.0.0.11 from outside
# based on https://serverfault.com/a/826424

TCP_DNS_ADDR=$(iptables-save | grep DOCKER_OUTPUT | grep tcp | grep -o '127\.0\.0\.11:.*$')
UDP_DNS_ADDR=$(iptables-save | grep DOCKER_OUTPUT | grep udp | grep -o '127\.0\.0\.11:.*$')

iptables -t nat -A PREROUTING -p tcp --dport 53 -j DNAT --to "$TCP_DNS_ADDR"
iptables -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to "$UDP_DNS_ADDR"


# Add this IP to resolv.conf since CoreDNS of k3s uses this file

TMP_FILE=$(mktemp)
sed "/nameserver.*/ a nameserver $(hostname -i | cut -f1 -d' ')" /etc/resolv.conf > "$TMP_FILE"
cp "$TMP_FILE" /etc/resolv.conf
rm "$TMP_FILE"

/bin/k3s server --bind-address k3s --tls-san 127.0.0.1 --kubelet-arg=runtime-request-timeout=10m0s