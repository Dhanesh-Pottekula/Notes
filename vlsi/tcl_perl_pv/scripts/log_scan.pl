#!/usr/bin/env perl
# log_scan.pl - one status line per Calibre log: finished or not, errors, warnings, run time.
# usage: log_scan.pl logs/*.log
use strict;
use warnings;
use File::Basename qw(basename);

@ARGV or die "usage: $0 <log> [more logs]\n";
printf "%-16s %-9s %6s %6s %9s  %s\n", 'LOG', 'STATUS', 'ERR', 'WARN', 'REAL', 'FIRST ERROR';
my $bad = 0;
for my $log (sort @ARGV) {
    open(my $fh, '<', $log) or do { warn "skip $log: $!\n"; next };
    my ($err, $warn, $done, $real, $first) = (0, 0, 0, undef, '');
    while (my $line = <$fh>) {
        if ($line =~ /^ERROR\b:?\s*(.*)/) { $err++; $first ||= $1; }
        $warn++ if $line =~ /^WARNING\b/;
        if ($line =~ /EXECUTIVE MODULE COMPLETED.*REAL TIME\s*=\s*(\d+)/) { $done = 1; $real = $1; }
    }
    close $fh;
    my $status = $err ? 'FAILED' : $done ? 'DONE' : 'RUNNING?';
    $bad++ unless $status eq 'DONE';
    my $time = defined $real ? sprintf("%dh%02dm", $real / 3600, ($real % 3600) / 60) : '-';
    printf "%-16s %-9s %6d %6d %9s  %s\n", basename($log), $status, $err, $warn, $time, $first;
}
exit($bad ? 1 : 0);
