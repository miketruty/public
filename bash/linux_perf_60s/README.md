# Linux 60s Analysis Checklist

From the latest _Systems Performance_ book by **Brendan Gregg**.

**NOTE:** Remember - run these on a **Linux** system, not your macbook.

Section 1.10.1 **Linux Perf Analysis in 60 Seconds**

1.  `uptime`
    *   Load averages to identify if load is increasing or decreasing. 
        Compare 1-, 5-, and 15- minute averages.
    *   Section 6.6.1
2.  `dmesg -T | tail`
    *   Kernel errors including OOM events.
    *   Section 7.5.11
3.  `vmstat -SM 1`
    *   System-wide statistics: run queue length, swapping, overall CPU usage
    *   Section 7.5.1
4.  `mpstat -P ALL 1`
    *   Per-CPU balance: a single busy CPU can indicate poor thread scaling.
    *   Section 6.6.3
5.  `pidstat 1`
    *   Per-process CPU usage: identify unexpected CPU consumers, and
        user/system CPU time for each process.
    *   Section 6.6.7
6.  `iostat -sxz 1`
    *   Disk I/O statistics: IOPS and throughput, average wait time, percent
        busy.
    *   Section 9.6.1
7.  `free -m`
    *   Memory usage including the file system cache.
    *   Section 8.6.2
8.  `sar -n DEV 1`
    *   Network device I/O: packets and throughput.
    *   Section 10.6.6
9.  `sar -n TCP,ETCP 1`
    *   TCP statistics: connection rates, retransmets.
    *   Section 10.6.6


