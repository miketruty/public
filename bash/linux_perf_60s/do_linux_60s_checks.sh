#!/usr/bin/env bash

server_name=$(hostname)


echo ----------------------------------------
echo Section 1.10.1 **Linux Perf Analysis in 60 Seconds**
echo ----------------------------------------

INTERVAL=1
COUNT=5


function banner() {
  echo
  echo ----------------------------------------
}


function show_cmd() {
  echo
  echo "$ $@"
  echo
}


function do_cmd() {
  command="$@"
  show_cmd "$command"
  $command
  banner
}


function tail_cmd() {
  command="$@"
  show_cmd "$command"
  $command | tail -50
  banner
}


function check_increasing_load() {
  echo 1. Check Increasing/Decreasing Load
  echo Load averages to identify if load is increasing or decreasing.
  echo Shows: current time, how long running, how many users logged on, then system load averages.
  echo Compare 1-, 5-, and 15- minute averages.
  do_cmd uptime
}


function check_kernel_errors() {
  echo 2. Check Kernel Errors
  echo Kernel errors including OOM events, with human-readable timestamps
  tail_cmd dmesg -T
}


function check_system_queue_swapping_cpuusage() {
  echo 3. Check System Queue Swapping and CPU Usage
  echo System-wide statistics: run queue length, swapping, overall CPU usage
  echo "I like -w (wide) repeated 5x"
  echo "PROCS"
  echo "  r: runnable processes (running or waiting)"
  echo "  b: blocked: processes in uninterruptible sleep"
  echo "MEMORY"
  echo "  swpd: virtual memory used"
  echo "  free: idle memory"
  echo "  buff: memory used as buffers"
  echo "  cache: memory used as cache"
  echo "SWAP"
  echo "  si: swapped in from disk (/s)"
  echo "  so: swapped to disk (/s)"
  echo "IO"
  echo "  bi: blocks received from block device"
  echo "  bo: blocks sent to block device"
  echo "System"
  echo "  in: interrupts per second, including clock"
  echo "  cs: context switches per second"
  echo "CPU"
  echo "  us: time in non-kernel code (user time, includes nice time)"
  echo "  sy: time spent running kernel code"
  echo "  id: time spent idle"
  echo "  wa: time spent waiting for IO"
  echo "  st: time stolen from a virtual machine"
  do_cmd vmstat -SM 1 -w 5
}


function check_per_cpu_balance() {
  echo 4. Check Per-CPU balance
  echo Per-CPU balance: a single busy CPU can indicate poor thread scaling.
  do_cmd mpstat -P ALL $INTERVAL $COUNT
}


function check_per_process_cpu() {
  echo 5. Check per-process CPU
  echo Per-process CPU usage: identify unexpected CPU consumers, and user/system
  echo CPU time for each process.
  do_cmd pidstat $INTERVAL $COUNT
}


function check_disk_io() {
  echo 6. Check Disk IO
  echo Disk I/O statistics: IOPS and throughput, average wait time, percent busy.
  echo "Note: -s seems to be deprecated"
  do_cmd iostat -xz $INTERVAL $COUNT
}


function check_memory_usage() {
  echo 7. Check Memory Usage
  echo Memory usage including the file system cache.
  do_cmd free -m
}


function check_network_io() {
  echo 8. Check Network IO
  echo Network device I/O: packets and throughput.
  do_cmd sar -n DEV $INTERVAL $COUNT
}


function check_tcp_stats() {
  echo 9. Check TCP Stats
  echo TCP statistics: connection rates, retransmets.
  do_cmd sar -n TCP,ETCP $INTERVAL $COUNT
}


function show_kernel_version() {
  echo "The exact Kernel version on ${server_name} is: "
  uname -r
}


function all_checks() {
  check_increasing_load
  check_kernel_errors
  check_system_queue_swapping_cpuusage
  check_per_cpu_balance
  check_per_process_cpu
  check_disk_io
  check_memory_usage
  check_network_io
  check_tcp_stats
  show_kernel_version
}


all_checks
