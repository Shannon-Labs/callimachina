#include <rte_ethdev.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    int ret = rte_eal_init(argc, argv);
    if (ret < 0) {
        printf("EAL init failed\n");
        return -1;
    }
    
    struct rte_eth_dev_info dev_info;
    if (rte_eth_dev_info_get(0, &dev_info);
    
    printf("=== RSS Capabilities ===\n");
    printf("Max RX queues: %u\n", dev_info.max_rx_queues);
    printf("Max TX queues: %u\n", dev_info.max_tx_queues);
    printf("Flow type RSS offloads: 0x%lx\n", dev_info.flow_type_rss_offloads);
    
    printf("\nSupported RSS hash functions:\n");
    if (dev_info.flow_type_rss_offloads & RTE_ETH_RSS_IPV4)
        printf("  - RTE_ETH_RSS_IPV4\n");
    if (dev_info.flow_type_rss_offloads & RTE_ETH_RSS_FRAG_IPV4)
        printf("  - RTE_ETH_RSS_FRAG_IPV4\n");
    if (dev_info.flow_type_rss_offloads & RTE_ETH_RSS_NONFRAG_IPV4_TCP)
        printf("  - RTE_ETH_RSS_NONFRAG_IPV4_TCP\n");
    if (dev_info.flow_type_rss_offloads & RTE_ETH_RSS_NONFRAG_IPV4_UDP)
        printf("  - RTE_ETH_RSS_NONFRAG_IPV4_UDP\n");
    if (dev_info.flow_type_rss_offloads & RTE_ETH_RSS_IPV6)
        printf("  - RTE_ETH_RSS_IPV6\n");
    if (dev_info.flow_type_rss_offloads & RTE_RSS_IPV6)
        printf("  - RTE_ETH_RSS_IPV6\n");
    if (dev_info.flow_type_rss_offloads & RTE_RSS_IPV6_TCP)
        printf("  - RTE_ETH_RSS_IPV6_TCP\n");
    if (dev_info.flow_type_rss_offloads & RTE_RSS_IPV6_UDP)
        printf("  - RTE_ETH_RSS_IPV6_UDP\n");
    if (dev_info.flow_type_rss_offloads & RTE_RSS_IPV6_SCTP)
        printf("  - RTE_ETH_RSS_IPV6_SCTP\n");
    if (dev_info.flow_type_rss_offloads & RTE_RSS_IPV6_OTHER)
        printf("  - RTE_ETH_RSS_IPV6_OTHER\n");
    
    return 0;
}
