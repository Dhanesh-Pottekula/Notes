# 16. Linux for backend engineers

Linux questions check whether you can run and debug your own services: "a server is slow — what do you run
first?", "port 8080 is in use", "SIGTERM vs SIGKILL", "too many open files". A 3-year engineer who has run Docker on
Azure/AWS VMs must read `top`, `free` and `ss` output, explain processes, signals and file descriptors, and write a
safe shell script. Syllabus: 3B Linux (`../../syllabus.html`).

## 16.1 Processes — fork, exec, PIDs, states
**Learn:** `Linux Commands/11. linux commands.txt` (ps, kill) · https://missing.csail.mit.edu/2020/command-line/ (job control) · linuxjourney.com "Processes" · *The Linux Programming Interface* ch.6, 24–28 · `man 2 fork`, `man 2 execve`
- [ ] `L1` What is a process? Process vs program vs thread.
- [ ] `L1` What is a PID? What is PID 1 on a normal Linux machine? ↳ init, usually systemd
- [ ] `L1` What does `ps aux` show? What do the columns USER, PID, %CPU, %MEM, VSZ, RSS, STAT mean?
- [ ] `L1` How do you find the PID of a process by name? ↳ `pgrep`, `ps aux | grep`, `pidof`
- [ ] `L1` Foreground vs background job. What do `&`, `jobs`, `fg`, `bg` and Ctrl+Z do?
- [ ] `L1` What does `nohup` do? How is it different from running with `&`?
- [ ] `L2` How does Linux create a new process? Explain `fork()` then `exec()`.
- [ ] `L2` Why split process creation into fork and exec instead of one call? ↳ child can set up FDs, env, redirects before exec
- [ ] `L2` What is copy-on-write in `fork()` and why does it make fork cheap?
- [ ] `L2` What is the parent PID (PPID)? How do you see the process tree? ↳ `ps -ef --forest`, `pstree`
- [ ] `L2` Process states: R, S, D, T, Z. What does each mean?
- [ ] `L2` What is the D state (uninterruptible sleep), and why can't you kill a process in it? ↳ waiting on I/O in kernel, often disk/NFS
- [ ] `L2` What is a zombie process? How do you get rid of zombies? ↳ exited, parent didn't `wait()`; fix/kill parent
- [ ] `L2` What is an orphan process? Who adopts it? ↳ init/subreaper re-parents and reaps it
- [ ] `L2` Zombie vs orphan.
- [ ] `L2` What is in `/proc/<pid>/`? Name five useful files. ↳ cmdline, environ, status, fd/, maps, limits, cwd
- [ ] `L2` What happens to background jobs when you close your SSH session? How do you keep them running? ↳ SIGHUP; nohup, setsid, tmux/screen, systemd
- [ ] `L2` Process vs thread in Linux: what do threads share? What is a thread in the kernel's eyes? ↳ tasks sharing memory/FDs via `clone()`
- [ ] `L3` What is `clone()` and how do threads and containers both use it?
- [ ] `L3` What is a process group and a session? Why do they matter for signals and terminals?
- [ ] `L3` What is a daemon, and what did the classic "double fork" achieve?
- [ ] `L3` What is `vfork()` / `posix_spawn()` and why do Python's `subprocess` and big JVMs care? ↳ forking a huge process is slow; spawn avoids copying page tables
- [ ] `L3` Why is forking after starting threads dangerous? ↳ only calling thread copied; locks held by others stay locked

## 16.2 Signals and graceful shutdown
**Learn:** `man 7 signal` · https://missing.csail.mit.edu/2020/command-line/ ("Job Control") · `Linux Commands/11. linux commands.txt` (kill, kill -9) · *The Linux Programming Interface* ch.20–22
- [ ] `L1` What is a signal?
- [ ] `L1` SIGTERM vs SIGKILL.
- [ ] `L1` What do SIGINT, SIGHUP, SIGQUIT, SIGSTOP and SIGCONT do?
- [ ] `L1` What does `kill -9 <pid>` do, and why is it the last resort?
- [ ] `L1` What signal does `Ctrl+C` send? `Ctrl+Z`? `Ctrl+\`?
- [ ] `L2` Which signals cannot be caught or ignored? ↳ SIGKILL, SIGSTOP
- [ ] `L2` What is SIGHUP traditionally used for by daemons like nginx? ↳ reload config without restart
- [ ] `L2` What is SIGCHLD and who should handle it?
- [ ] `L2` What is SIGPIPE, and when does a server get it? ↳ writing to a closed socket/pipe; usually ignored, handle EPIPE
- [ ] `L2` What is SIGSEGV? What is a core dump and how do you enable one? ↳ `ulimit -c`, core_pattern
- [ ] `L2` How do you trap a signal in a bash script? Write a cleanup trap. ↳ `trap 'cleanup' EXIT INT TERM`
- [ ] `L2` What does graceful shutdown mean for an HTTP/WebSocket server? List the steps. ↳ stop accepting, fail readiness, drain in-flight, close pools, exit
- [ ] `L2` How do you handle SIGTERM in Python (asyncio / FastAPI) and in Node.js?
- [ ] `L2` What do `kill`, `pkill` and `killall` do differently?
- [ ] `L2` What does `kill -0 <pid>` do? ↳ checks process exists and you may signal it
- [ ] `L3` What is a signal mask, and why are only async-signal-safe functions allowed in a handler?
- [ ] `L3` Why might a process ignore SIGTERM when it runs as PID 1 in a container?
- [ ] `L3` How does systemd stop a service? What are `KillMode`, `TimeoutStopSec` and `KillSignal`?
- [ ] `L3` What is the self-pipe trick / `signalfd`, and why do event loops use them?
- [ ] `L3` What does the exit code 128+N mean in the shell? Decode 130, 137 and 143.

## 16.3 File descriptors, "everything is a file", ulimits
**Learn:** `Linux Commands/6. linux commands.txt` (lsof) · `man 2 open`, `man 1 lsof` · Julia Evans "File descriptors" (jvns.ca) · *The Linux Programming Interface* ch.4–5
- [ ] `L1` What is a file descriptor?
- [ ] `L1` What are FDs 0, 1 and 2?
- [ ] `L1` What does "everything is a file" mean in Linux? Give examples. ↳ files, sockets, pipes, devices, /proc entries
- [ ] `L1` What is `ulimit -n`?
- [ ] `L2` Your server logs "Too many open files" (EMFILE). What is happening and how do you fix it? ↳ FD limit or leak; raise nofile, find leak with lsof
- [ ] `L2` How do you see how many FDs a process has open and what they point to? ↳ `ls /proc/<pid>/fd | wc -l`, `lsof -p <pid>`
- [ ] `L2` Soft vs hard limits. How do you raise `nofile` permanently for a systemd service? For a Docker container? ↳ `LimitNOFILE=`, `--ulimit nofile=`
- [ ] `L2` EMFILE vs ENFILE. ↳ per-process vs system-wide (`fs.file-max`)
- [ ] `L2` Each WebSocket connection uses one FD. How does that set the max connections per process?
- [ ] `L2` What is an inode? How is it different from a filename?
- [ ] `L2` Hard link vs soft (symbolic) link. ↳ hard = same inode, same FS; soft = path pointer, can dangle
- [ ] `L2` You deleted a 20 GB log file but `df` still shows the disk full. Why? ↳ process still holds open FD; `lsof +L1`; restart or truncate
- [ ] `L2` What is `/dev/null`, `/dev/zero`, `/dev/urandom`?
- [ ] `L2` What is in `/proc` and `/sys`? Are they on disk?
- [ ] `L3` What happens to open FDs across `fork()` and `exec()`? What is `O_CLOEXEC` for?
- [ ] `L3` What is `epoll` and why does it scale better than `select`/`poll`?
- [ ] `L3` Blocking vs non-blocking I/O on an FD. What does `EAGAIN` mean?
- [ ] `L3` What is the difference between a file description and a file descriptor (`dup()`, shared offsets)?

## 16.4 Pipes, redirection and the shell
**Learn:** https://missing.csail.mit.edu/2020/course-shell/ · https://www.gnu.org/software/bash/manual/bash.html#Redirections · `Docker/ShellScripting.md` · `Linux Commands/2. linux commands.txt` (ls, cp, mv, rm, mkdir)
- [ ] `L1` What does a pipe `|` do?
- [ ] `L1` `>` vs `>>` vs `<`.
- [ ] `L1` What does `2>&1` mean?
- [ ] `L1` What does `tee` do?
- [ ] `L2` Why is `cmd > out.log 2>&1` different from `cmd 2>&1 > out.log`? ↳ redirections apply left to right
- [ ] `L2` What does `&>` do in bash?
- [ ] `L2` What is a named pipe (FIFO)? When would you use one?
- [ ] `L2` What is a here-document and a here-string?
- [ ] `L2` What is process substitution `<(cmd)`? Give a use. ↳ `diff <(sort a) <(sort b)`
- [ ] `L2` What is the exit status of a pipeline, and what does `pipefail` change?
- [ ] `L2` What happens when the reader of a pipe exits early (`cmd | head -1`)? ↳ writer gets SIGPIPE
- [ ] `L2` What do `$(...)` and backticks do? Why prefer `$(...)`?
- [ ] `L2` What does `xargs` do, and why use `-0` with `find -print0`?
- [ ] `L2` `;` vs `&&` vs `||` between commands.
- [ ] `L3` How does the shell implement a pipe? ↳ `pipe()` syscall, fork two children, `dup2` FDs, exec
- [ ] `L3` Why can output appear out of order or late when piped (stdout buffering)? How do you fix it? ↳ full buffering when not a TTY; `stdbuf -oL`, `PYTHONUNBUFFERED`
- [ ] `L3` What is a pipe's buffer size, and what happens when it is full?

## 16.5 Permissions, users, groups, sudo
**Learn:** `Linux Commands/7. linux commands.txt` (chmod, chown, useradd, groupadd, id) · `Linux Commands/8. linux commands.txt` (visudo, sudo, su) · `Docker/ShellScripting.md` (chmod octal 4/2/1) · linuxjourney.com "Permissions"
- [ ] `L1` Read `-rwxr-x--- 1 app web 4096 file`. Who can do what?
- [ ] `L1` What does `chmod 755` mean? `chmod 644`? `chmod 600`? ↳ r=4, w=2, x=1 for user/group/other
- [ ] `L1` What does `chown user:group file` do?
- [ ] `L1` What do read, write and execute mean on a **directory**? ↳ list names, create/delete entries, enter/traverse
- [ ] `L1` What is `sudo`? `su` vs `sudo`?
- [ ] `L1` How do you add a user and add them to a group? ↳ `useradd`, `usermod -aG`, `groupadd`
- [ ] `L2` What is `umask`? With umask 022, what permissions does a new file get? A new directory? ↳ 644 and 755
- [ ] `L2` What is the setuid bit? Give a real example. ↳ `/usr/bin/passwd` runs as root
- [ ] `L2` What is the setgid bit on a directory?
- [ ] `L2` What is the sticky bit, and why does `/tmp` have it? ↳ only owner can delete their files
- [ ] `L2` Where are users, passwords and groups stored? ↳ `/etc/passwd`, `/etc/shadow`, `/etc/group`
- [ ] `L2` How do you give a user passwordless sudo for one command only? Why edit with `visudo`?
- [ ] `L2` What does `id` show?
- [ ] `L2` Why does your app fail with "Permission denied" after you added your user to the `docker` group, and what fixes it? ↳ new group needs new login session; `newgrp`
- [ ] `L2` Why is being in the `docker` group equivalent to root?
- [ ] `L2` What is a system user (`useradd -r`, nologin shell), and why run services as one?
- [ ] `L2` Your SSH key login fails with "bad permissions". Which permissions must `~/.ssh` and `authorized_keys` have? ↳ 700 and 600
- [ ] `L3` What are ACLs (`getfacl`/`setfacl`) and when are classic permissions not enough?
- [ ] `L3` What are Linux capabilities, and how do they split root's power? ↳ e.g. CAP_NET_BIND_SERVICE for port <1024
- [ ] `L3` How can a non-root process listen on port 80? ↳ capability, authbind, reverse proxy, `ip_unprivileged_port_start`
- [ ] `L3` What are SELinux and AppArmor, and how do you tell they are blocking you?

## 16.6 Memory
**Learn:** `Linux Commands/5. linux commands.txt` (free -m) · `Linux Commands/1. linux commands.txt` (free, /proc) · https://www.linuxatemyram.com · https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html · Brendan Gregg *Systems Performance* ch.7
- [ ] `L1` What does `free -m` show? Explain each column. ↳ total, used, free, shared, buff/cache, available
- [ ] `L1` "free" vs "available" memory: which do you look at?
- [ ] `L1` What is swap?
- [ ] `L1` What is the OOM killer?
- [ ] `L2` RSS vs VSZ (virtual size). Why is VSZ often huge and harmless?
- [ ] `L2` What is shared memory, and why does adding up RSS of all processes overcount? ↳ shared libs, CoW pages; PSS
- [ ] `L2` What is the page cache? Why does Linux "use all my RAM"? ↳ caches files; reclaimable; good thing
- [ ] `L2` What are buffers vs cache in `free`?
- [ ] `L2` How do you tell a process was OOM-killed? ↳ `dmesg -T | grep -i oom`, journalctl -k, exit 137
- [ ] `L2` How does the OOM killer choose which process to kill? ↳ oom_score from memory use, `oom_score_adj`
- [ ] `L2` Is swapping good or bad for a latency-sensitive API? What is `swappiness`?
- [ ] `L2` What is a memory leak vs memory growth from caches? How do you tell them apart in a Python service?
- [ ] `L2` What do `vmstat 1` columns si/so tell you?
- [ ] `L2` What is virtual memory and what does the MMU do?
- [ ] `L2` What is a page fault? Minor vs major.
- [ ] `L3` What is memory overcommit and what do `vm.overcommit_memory` 0/1/2 do?
- [ ] `L3` What are huge pages / transparent huge pages, and why do Redis and databases often say turn THP off?
- [ ] `L3` Why does a Python process often not give memory back to the OS after freeing objects? ↳ allocator arenas, fragmentation
- [ ] `L3` What is NUMA and when does it matter for a backend?
- [ ] `L3` How do you see the memory map of a process? ↳ `/proc/<pid>/smaps`, `pmap -x`

## 16.7 CPU, load average and scheduling
**Learn:** `Linux Commands/5. linux commands.txt` + `1. linux commands.txt` (uptime) · https://www.brendangregg.com/blog/2017-08-08/linux-load-averages.html · `man top` · Brendan Gregg *Systems Performance* ch.6
- [ ] `L1` What do the three numbers in `uptime` / load average mean?
- [ ] `L1` Load average is 4.0. Is that bad? ↳ depends on core count
- [ ] `L1` What does `top` show? What does `htop` add?
- [ ] `L1` How do you see how many CPU cores a machine has? ↳ `nproc`, `lscpu`, `/proc/cpuinfo`
- [ ] `L2` What counts toward Linux load average that does not count on other Unixes? ↳ D-state tasks waiting on disk I/O
- [ ] `L2` Load is 30 on an 8-core box but CPU is 20% busy. What is going on? ↳ D-state, I/O wait, NFS/disk stalls
- [ ] `L2` Explain the CPU fields in `top`: us, sy, ni, id, wa, hi, si, st.
- [ ] `L2` What is steal time (`st`), and what does a high value mean on a cloud VM? ↳ hypervisor gives CPU to other tenants; burstable credits
- [ ] `L2` What is `%iowait` and why is it a misleading metric?
- [ ] `L2` What is a context switch? Voluntary vs involuntary. Where do you see them? ↳ `vmstat` cs, `pidstat -w`
- [ ] `L2` What are `nice` and `renice`? Range and meaning.
- [ ] `L2` A process shows 400% CPU in top. How is that possible?
- [ ] `L2` How do you find which thread inside a process is using the CPU? ↳ `top -H -p`, `ps -L`, py-spy
- [ ] `L2` What does a Python process at 100% on one core tell you, and how does that relate to the GIL and worker count?
- [ ] `L3` How does the Linux CFS scheduler decide who runs next? What is EEVDF?
- [ ] `L3` What is CPU affinity (`taskset`) and when would you pin a process?
- [ ] `L3` What is the run queue length, and how do you see it? ↳ `vmstat` r column, `sar -q`
- [ ] `L3` What are burstable VM types (AWS T-series, Azure B-series) and how do CPU credits cause sudden slowness?

## 16.8 Disk, filesystems and I/O
**Learn:** `Linux Commands/5. linux commands.txt` (df) · `Linux Commands/12. linux commands.txt` (tar, zip) · `man iostat`, `man df`, `man du` · Brendan Gregg *Systems Performance* ch.8–9
- [ ] `L1` `df -h` vs `du -sh`.
- [ ] `L1` How do you find the biggest directories under `/var`? ↳ `du -xh --max-depth=1 /var | sort -h`
- [ ] `L1` What is mounting? What does `/etc/fstab` do?
- [ ] `L1` Explain the standard directories: `/etc`, `/var`, `/var/log`, `/tmp`, `/opt`, `/usr`, `/home`, `/proc`.
- [ ] `L1` How do you create and extract a `.tar.gz`? ↳ `tar -czf`, `tar -xzf`
- [ ] `L2` The disk is full but `du` adds up to much less than `df` says. Why? ↳ deleted-but-open files, other mounts hidden, reserved blocks
- [ ] `L2` `df -h` shows space left but you get "No space left on device". Why? ↳ out of inodes; `df -i`
- [ ] `L2` What creates millions of tiny files and eats inodes on servers? ↳ session files, cache dirs, mail queues, temp files
- [ ] `L2` What does `iostat -x 1` show? What do `%util`, `await` and `r/s`/`w/s` mean?
- [ ] `L2` How do you find which process is doing the most disk I/O? ↳ `iotop`, `pidstat -d`
- [ ] `L2` What is `fsync` and why do databases care?
- [ ] `L2` Why is writing a file "fast" and then the box stalls later? ↳ dirty pages in page cache, writeback flush
- [ ] `L2` What is logrotate and how do you set it up for an app log? What is `copytruncate` for?
- [ ] `L2` ext4 vs xfs: which have you used and what is different?
- [ ] `L2` Your cloud VM disk is slow. What are IOPS and throughput limits on EBS / Azure managed disks?
- [ ] `L3` What is the I/O scheduler, and why is it often `none` on NVMe?
- [ ] `L3` What is direct I/O (`O_DIRECT`) and who uses it?
- [ ] `L3` How do you grow a disk on a cloud VM without downtime? ↳ resize disk, `growpart`, `resize2fs`/`xfs_growfs`
- [ ] `L3` What is LVM and why would you use it on a server?

## 16.9 Networking commands
**Learn:** `Linux Commands/6. linux commands.txt` (lsof) · `Linux Commands/9. linux commands.txt` (curl) · Julia Evans "Bite Size Networking" (wizardzines.com) · linuxjourney.com "Network" · `man ss`, `man ip`
- [ ] `L1` How do you see which ports are listening and which process owns each? ↳ `ss -ltnp`, `lsof -i -P -n`
- [ ] `L1` Port 8080 is already in use. Find and stop the process.
- [ ] `L1` What do `ping`, `curl`, `wget` and `dig` each do?
- [ ] `L1` How do you see the machine's IP addresses? ↳ `ip addr`, `hostname -I`
- [ ] `L2` `ss` vs `netstat`. Why was netstat replaced?
- [ ] `L2` What do `ip route` and `ip neigh` show?
- [ ] `L2` How do you check whether a remote port is reachable from this box? ↳ `nc -zv host port`, `curl -v telnet://`, bash `/dev/tcp`
- [ ] `L2` How do you count TCP connections per state and per remote IP?
- [ ] `L2` What is `/etc/resolv.conf` and `/etc/hosts`? What is `nsswitch.conf`?
- [ ] `L2` How do you make an HTTP request with headers, a JSON body and a timeout using curl?
- [ ] `L2` How do you download a file and resume it if it breaks? ↳ `curl -C -`, `wget -c`
- [ ] `L2` What do `iptables -L -n`, `nft list ruleset` and `ufw status` show?
- [ ] `L2` How do you open a port in the VM firewall and in the cloud security group / NSG? Why both?
- [ ] `L2` What is `tcpdump` and give one command you would actually run.
- [ ] `L2` What is `lsof -i :5432` vs `lsof -p <pid>` vs `lsof +D /dir`?
- [ ] `L3` What are `sysctl` settings like `net.core.somaxconn` and `net.ipv4.ip_local_port_range` for?
- [ ] `L3` What do `nstat` / `netstat -s` counters tell you about retransmits and listen-queue overflows?
- [ ] `L3` How do you see which network namespace a container uses and run a command inside it? ↳ `nsenter -t <pid> -n`, `ip netns`

## 16.10 systemd, services, journalctl, cron and boot
**Learn:** `Linux Commands/10. linux commands.txt` (systemctl) · `Linux Commands/11. linux commands.txt` (systemctl) · https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html · https://crontab.guru · https://wiki.archlinux.org/title/Arch_boot_process
- [ ] `L1` What is systemd?
- [ ] `L1` What do `systemctl start`, `stop`, `restart`, `reload`, `enable`, `status` do?
- [ ] `L1` `enable` vs `start`.
- [ ] `L1` How do you read a service's logs? ↳ `journalctl -u name -f`
- [ ] `L1` What is cron? Read this line: `*/5 * * * * /opt/backup.sh`.
- [ ] `L2` Write a systemd unit file for a FastAPI app. Which sections and keys matter? ↳ [Unit] After=, [Service] User, ExecStart, Restart, Environment, [Install]
- [ ] `L2` What does `Restart=on-failure` do, and what are `RestartSec` and start limits?
- [ ] `L2` After editing a unit file, what must you run? ↳ `systemctl daemon-reload`
- [ ] `L2` How do you pass environment variables and secrets to a systemd service? ↳ `Environment=`, `EnvironmentFile=`, credentials
- [ ] `L2` `journalctl` filters: by time, by boot, by priority, follow. ↳ `--since`, `-b`, `-p err`, `-f`
- [ ] `L2` Why did your cron job work in the shell but fail under cron? ↳ minimal PATH/env, no TTY, cwd, permissions; log output
- [ ] `L2` Where does cron output go, and how do you capture it?
- [ ] `L2` What are systemd timers, and why might you use them instead of cron?
- [ ] `L2` How do you make Docker containers start on boot on a VM — systemd or restart policies?
- [ ] `L2` What is a target in systemd (vs runlevels)?
- [ ] `L2` What are `Type=simple`, `exec`, `forking` and `notify`?
- [ ] `L3` Walk through the Linux boot process from power on to login. ↳ firmware (BIOS/UEFI), GRUB, kernel + initramfs, systemd, targets
- [ ] `L3` What is initramfs and why is it needed?
- [ ] `L3` What sandboxing options does systemd give a service? ↳ ProtectSystem, PrivateTmp, NoNewPrivileges, MemoryMax
- [ ] `L3` What is `systemd-analyze blame` for?
- [ ] `L3` How do you stop the same cron job running twice on three VMs? ↳ `flock`, distributed lock, single scheduler

## 16.11 cgroups, namespaces and a container by hand
**Learn:** `man 7 namespaces`, `man 7 cgroups` · Liz Rice "Containers From Scratch" (GOTO 2018, YouTube) · https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html · Julia Evans "How Containers Work" (wizardzines.com)
- [ ] `L1` What is a namespace in Linux?
- [ ] `L1` What is a cgroup?
- [ ] `L1` Is a container a Linux kernel object?
- [ ] `L2` List the namespace types and what each isolates.
- [ ] `L2` What do `unshare` and `nsenter` do?
- [ ] `L2` Where is the cgroup tree mounted, and how do you see a process's cgroup? ↳ `/sys/fs/cgroup`, `/proc/<pid>/cgroup`
- [ ] `L2` How do you limit a process to 512 MB of memory by hand with cgroup v2? ↳ mkdir group, write `memory.max`, write PID to `cgroup.procs`
- [ ] `L2` What do `memory.max`, `cpu.max` and `pids.max` control?
- [ ] `L2` What does `chroot` do, and why is it not a security boundary?
- [ ] `L2` How does systemd use cgroups for every service? ↳ slice per unit; `systemd-cgls`, `systemd-cgtop`
- [ ] `L3` Build a container by hand: list the steps from `unshare` to a shell in its own rootfs with limits. ↳ unshare pid/mnt/uts/net, mount proc, pivot_root, cgroup
- [ ] `L3` Why must you mount a new `/proc` after creating a PID namespace?
- [ ] `L3` How does a user namespace map container root to an unprivileged host UID?
- [ ] `L3` How do you connect a new network namespace to the host network? ↳ veth pair, bridge, IP, NAT rule
- [ ] `L3` What is `pivot_root` vs `chroot`?
- [ ] `L3` What does a container runtime (runc) do that your hand-built version doesn't? ↳ seccomp, capabilities, AppArmor, device rules, OCI config

## 16.12 Syscalls, strace, perf and eBPF
**Learn:** `man 2 syscalls`, `man 1 strace` · Julia Evans "strace" zine (wizardzines.com) · https://www.brendangregg.com/perf.html · https://www.brendangregg.com/ebpf.html · https://ebpf.io/what-is-ebpf/
- [ ] `L1` What is a system call? Give five you know. ↳ read, write, open, socket, fork, execve, mmap
- [ ] `L1` User space vs kernel space.
- [ ] `L1` What does `strace` do?
- [ ] `L2` A process hangs. How do you use `strace -p` to see what it is waiting on?
- [ ] `L2` What do `strace -f`, `-e trace=network`, `-c` and `-T` do?
- [ ] `L2` Use strace to find which config file an app is actually reading. ↳ `strace -e trace=openat`
- [ ] `L2` Why is strace slow, and why be careful running it in production? ↳ ptrace stops on every syscall; big overhead
- [ ] `L2` What does `ltrace` show that strace doesn't?
- [ ] `L2` What is `perf top` / `perf record` used for?
- [ ] `L2` What is a flame graph and how do you read it? ↳ width = time on CPU; look for wide plateaus
- [ ] `L2` What is py-spy and why is it handy for a running Python service?
- [ ] `L3` What is eBPF, and why is it safer and cheaper than strace for production tracing?
- [ ] `L3` Name a few bcc/bpftrace tools and what they show. ↳ execsnoop, opensnoop, biolatency, tcpconnect, tcpretrans
- [ ] `L3` How does a syscall actually switch into the kernel, and what is the cost?
- [ ] `L3` What is the vDSO and which calls use it? ↳ `gettimeofday`/`clock_gettime` without a real syscall
- [ ] `L3` On-CPU vs off-CPU profiling: what does each find?

## 16.13 Shell scripting
**Learn:** `Docker/ShellScripting.md` (set -e, set -x) · https://missing.csail.mit.edu/2020/shell-tools/ · Aaron Maxwell "Use the Unofficial Bash Strict Mode" (redsymbol.net) · https://www.shellcheck.net · https://mywiki.wooledge.org/BashPitfalls
- [ ] `L1` What is the shebang line? `#!/bin/bash` vs `#!/usr/bin/env bash`.
- [ ] `L1` How do you make a script executable and run it?
- [ ] `L1` How do you define and use a variable? Why quote `"$var"`?
- [ ] `L1` What is an exit code? How do you read the last one? ↳ `$?`; 0 = success
- [ ] `L1` What are `$0`, `$1`, `$#`, `$@`, `$*` and `$$`?
- [ ] `L1` Environment variable vs shell variable. What does `export` do?
- [ ] `L2` What does `set -euo pipefail` do, piece by piece?
- [ ] `L2` What are the gotchas of `set -e`? ↳ ignored in conditions, `&&` lists, subshells; `cmd || true`
- [ ] `L2` What does `set -x` do, and when do you use it?
- [ ] `L2` `"$@"` vs `$*`: why does it matter for filenames with spaces?
- [ ] `L2` Write a loop over all `.log` files in a directory, safely.
- [ ] `L2` Write a loop that reads a file line by line. ↳ `while IFS= read -r line; do …; done < file`
- [ ] `L2` `[ ]` vs `[[ ]]` vs `(( ))`.
- [ ] `L2` How do you test if a file exists, a directory exists, a string is empty? ↳ `-f`, `-d`, `-z`
- [ ] `L2` How do you write a function that returns a value?
- [ ] `L2` How do you give a variable a default value? ↳ `${VAR:-default}`, `${VAR:?error}`
- [ ] `L2` What is a subshell, and why doesn't a variable set inside `cmd | while read` survive?
- [ ] `L2` How do you parse flags in a script? ↳ `getopts`, case loop
- [ ] `L2` What is ShellCheck and what does it catch?
- [ ] `L2` Write a retry-with-backoff loop for a flaky command.
- [ ] `L2` Write a deploy script: pull image, stop old container, start new, health-check, roll back on failure.
- [ ] `L3` How do you make a script safe to run twice (idempotent)?
- [ ] `L3` How do you prevent two copies of a script from running at once? ↳ `flock`
- [ ] `L3` How do you create and always clean up a temp file? ↳ `mktemp` + `trap 'rm -f "$tmp"' EXIT`
- [ ] `L3` When should a script stop being bash and become Python?
- [ ] `L3` `source script.sh` vs `./script.sh`: what is different?

## 16.14 Text processing and log analysis one-liners
**Learn:** `Linux Commands/4. linux commands.txt` (grep, sed, awk, cut, head, tail) · https://missing.csail.mit.edu/2020/data-wrangling/ · https://jqlang.org/manual/ · *The AWK Programming Language* ch.1
- [ ] `L1` What do `grep`, `sed` and `awk` each do, in one line?
- [ ] `L1` What do `grep -i`, `-v`, `-r`, `-n`, `-c`, `-E` and `-A/-B/-C` do?
- [ ] `L1` `head`, `tail`, `tail -f`, `tail -F`, `less`: when do you use each? ↳ -F survives log rotation
- [ ] `L1` What does `wc -l` do?
- [ ] `L1` What do `sort`, `uniq` and `cut` do? Why must you sort before `uniq`?
- [ ] `L2` Count the top 10 client IPs in an nginx access log. ↳ `awk '{print $1}' | sort | uniq -c | sort -rn | head`
- [ ] `L2` Count HTTP status codes in an access log.
- [ ] `L2` Find all 5xx responses in the last hour of logs.
- [ ] `L2` Print the 10 slowest requests from a log that has the response time in field 11.
- [ ] `L2` Replace a string in many files in place with `sed`. What is different on macOS? ↳ `sed -i ''` on BSD
- [ ] `L2` Print only the second column of a CSV. `cut` vs `awk`.
- [ ] `L2` Sum a numeric column with `awk`. Compute an average.
- [ ] `L2` Find files larger than 100 MB modified in the last 7 days. ↳ `find / -xdev -size +100M -mtime -7`
- [ ] `L2` Delete log files older than 30 days safely. ↳ `find … -mtime +30 -print` first, then `-delete`
- [ ] `L2` Grep a pattern across a directory but skip `node_modules`. What is ripgrep?
- [ ] `L2` Extract one field from JSON logs with `jq`. Filter JSON lines where `level == "error"`.
- [ ] `L2` Count requests per minute from a timestamped log.
- [ ] `L2` Show unique error messages and how often each appears.
- [ ] `L2` Follow a log and show only lines with a request id.
- [ ] `L2` What does `sort -k2 -n -t,` do?
- [ ] `L3` Find which request ids appear in log A but not in log B. ↳ `comm`, `sort`, `join` or `grep -vFf`
- [ ] `L3` Parse a multi-GB log quickly. What makes grep/awk fast or slow? ↳ `LC_ALL=C`, fixed strings, avoid UUOC, parallel
- [ ] `L3` Run a command over 10,000 files in parallel. ↳ `xargs -P`, GNU parallel
- [ ] `L3` Write an awk script that prints p50 and p99 latency per endpoint.

## 16.15 SSH, remote work and package management
**Learn:** https://missing.csail.mit.edu/2020/command-line/ ("Remote machines") · `Docker/DockerCommands.md` "AWS SSH Access" · `Linux Commands/9. linux commands.txt` (yum, rpm) · `Linux Commands/13. linux commands.txt` (apt, dpkg) · `Linux Commands/12. linux commands.txt` (yum, tar)
- [ ] `L1` How does SSH key authentication work? ↳ server holds public key; client proves it has private key by signing
- [ ] `L1` How do you create an SSH key and put it on a server? ↳ `ssh-keygen -t ed25519`, `ssh-copy-id`
- [ ] `L1` `scp` vs `rsync`.
- [ ] `L1` `apt` vs `yum`/`dnf`: which distros use which?
- [ ] `L1` How do you install, remove and search for a package with apt? ↳ `apt install`, `apt remove`, `apt search`
- [ ] `L2` What goes in `~/.ssh/config` and why use it?
- [ ] `L2` What is `known_hosts`, and what does "REMOTE HOST IDENTIFICATION HAS CHANGED" mean?
- [ ] `L2` What is ssh-agent and agent forwarding? Why is forwarding risky?
- [ ] `L2` What is an SSH tunnel? Local vs remote port forwarding. ↳ `-L` reach private DB via bastion; `-R` expose local
- [ ] `L2` How do you reach a private VM through a bastion in one command? ↳ `ssh -J` (ProxyJump)
- [ ] `L2` How do you harden SSH on a public VM? ↳ keys only, no root login, fail2ban, restrict source IPs/NSG
- [ ] `L2` What is `tmux` / `screen`, and why use it for long jobs over SSH?
- [ ] `L2` `rsync -avz --delete`: what does each flag do and what is dangerous?
- [ ] `L2` `apt update` vs `apt upgrade`. How do you pin a package version?
- [ ] `L2` `dpkg` vs `apt`; `rpm` vs `yum`.
- [ ] `L2` How do you find which package a file came from? ↳ `dpkg -S`, `rpm -qf`
- [ ] `L2` What are unattended security upgrades, and would you enable them on a prod VM?
- [ ] `L3` How do SSH certificates (signed by a CA) differ from plain keys, and why do big teams use them?
- [ ] `L3` What are cloud alternatives to SSH for VMs? ↳ AWS SSM Session Manager, Azure Bastion, serial console
- [ ] `L3` How do you rebuild a server reproducibly instead of hand-installing packages? ↳ cloud-init, Ansible, images (Packer), containers

## 16.16 Performance in 60 seconds and troubleshooting scenarios
**Learn:** https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55 · https://www.brendangregg.com/usemethod.html · Brendan Gregg *Systems Performance* ch.2 · `Linux Commands/5. linux commands.txt` (free, uptime)
- [ ] `L1` A server is slow. What commands do you run first?
- [ ] `L1` What is the USE method? ↳ utilization, saturation, errors for every resource
- [ ] `L2` List Brendan Gregg's 60-second checklist and what each command tells you. ↳ uptime, dmesg, vmstat, mpstat, pidstat, iostat, free, sar ×2, top
- [ ] `L2` What do you look for in `dmesg -T | tail`? ↳ OOM kills, disk errors, TCP drops, segfaults
- [ ] `L2` Read `vmstat 1` output: r, b, si/so, us/sy/id/wa, cs.
- [ ] `L2` What do `mpstat -P ALL 1` and `pidstat 1` add?
- [ ] `L2` What does `sar -n DEV 1` and `sar -n TCP,ETCP 1` show?
- [ ] `L2` Scenario: disk full at 3 am. Walk through finding and freeing space safely. ↳ `df -h`, `du`, deleted-open files, logs, Docker, inodes
- [ ] `L2` Scenario: load average 50 on 4 cores. Diagnose.
- [ ] `L2` Scenario: the app was OOM-killed overnight. How do you prove it and find the cause?
- [ ] `L2` Scenario: "Too many open files" in the app log. Steps?
- [ ] `L2` Scenario: the service won't start because the port is in use. Steps?
- [ ] `L2` Scenario: the box is slow but CPU and memory look fine. What next? ↳ disk I/O, steal time, network, locks, downstream calls
- [ ] `L2` Scenario: SSH to the VM hangs after login. What could cause it?
- [ ] `L2` Scenario: a cron job silently stopped running. Where do you look?
- [ ] `L2` Scenario: one API endpoint is slow only on the VM, not locally. How do you narrow it down?
- [ ] `L3` Scenario: CPU is 100% `sy` (system time). What does that suggest and how do you dig in? ↳ syscall storms, lock contention, page faults; perf, strace -c
- [ ] `L3` Scenario: memory "used" keeps growing for days but the app's RSS is flat. Explain. ↳ page cache, slab (dentries), tmpfs, other processes
- [ ] `L3` Scenario: a Python worker is stuck at 0% CPU and not responding. How do you find where it is stuck? ↳ py-spy dump, strace -p, /proc/<pid>/stack
- [ ] `L3` Scenario: latency spikes every few minutes on an otherwise idle VM. List hypotheses and how to test each.
- [ ] `L3` Scenario: a VM with lots of free RAM starts swapping. Why can that happen?
- [ ] `L3` Scenario: a deploy left the server with thousands of zombie processes. What happened and how do you clean up?
- [ ] `L3` Tell me about a real production issue you debugged on a Linux VM at AiRA: what you saw, what you ran, what fixed it.

## 16.17 Rapid-fire round
- [ ] `L1` Which signal does `kill` send by default?
- [ ] `L1` Which signal can never be caught?
- [ ] `L1` What is PID 1 on most modern distros?
- [ ] `L1` What state letter is a zombie in `ps`?
- [ ] `L1` What is FD 2?
- [ ] `L1` What does `2>&1` do?
- [ ] `L1` What does `chmod 600` allow?
- [ ] `L1` What does the sticky bit do on `/tmp`?
- [ ] `L1` Which file holds password hashes?
- [ ] `L1` Command to show disk usage per filesystem?
- [ ] `L1` Command to show inode usage?
- [ ] `L1` Command to show free memory in MB?
- [ ] `L1` In `free`, which column tells you how much memory apps can still get?
- [ ] `L1` What does load average count on Linux besides running tasks?
- [ ] `L1` What does `st` mean in `top`?
- [ ] `L1` Command to see listening ports with process names?
- [ ] `L1` Command to follow a systemd service's logs?
- [ ] `L1` What must you run after editing a unit file?
- [ ] `L1` What does `*/15 * * * *` mean in cron?
- [ ] `L1` What does `$?` hold?
- [ ] `L1` What does `set -u` do?
- [ ] `L1` What does `pipefail` do?
- [ ] `L1` Which tool traces system calls?
- [ ] `L1` What does `lsof` stand for?
- [ ] `L1` What does `nohup` protect a process from?
- [ ] `L1` What does `ulimit -n` show?
- [ ] `L1` `apt` or `yum` on Ubuntu?
- [ ] `L1` Which permissions does `~/.ssh/authorized_keys` need?
- [ ] `L1` Which command finds files by name under a directory?
- [ ] `L1` Which command shows the kernel ring buffer (OOM messages)?
