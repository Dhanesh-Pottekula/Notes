#!/usr/bin/env perl
# drc_summary.pl - print the failing rules of one Calibre DRC summary, worst first.
# usage: drc_summary.pl top.drc.summary [--all]
# exit code: 0 = clean, 1 = violations found (so a shell or Makefile can test it)
use strict;
use warnings;

my $file = shift @ARGV or die "usage: $0 <drc.summary> [--all]\n";
my $show_all = grep { $_ eq '--all' } @ARGV;

open(my $fh, '<', $file) or die "cannot open $file: $!\n";
my (%count, $in);
while (my $line = <$fh>) {
    if (!$in) {
        $in = 1 if $line =~ /^--- RULECHECK RESULTS STATISTICS\s*$/;
        next;
    }
    last if $line =~ /^-{20,}\s*$/;      # stop before the "(BY CELL)" section repeats the rules
    if ($line =~ /^RULECHECK\s+(\S+)\s.*TOTAL Result Count\s*=\s*(\d+)/) {
        $count{$1} = $2;
    }
}
close $fh;
die "$file: no RULECHECK lines found\n" unless %count;

my @rules = sort { $count{$b} <=> $count{$a} || $a cmp $b } keys %count;
my ($total, $failing) = (0, 0);
printf "%-14s %8s\n", 'RULE', 'RESULTS';
for my $r (@rules) {
    $total += $count{$r};
    $failing++ if $count{$r} > 0;
    next unless $show_all || $count{$r} > 0;
    printf "%-14s %8d\n", $r, $count{$r};
}
printf "\n%d rules checked, %d failing, %d results in total\n",
    scalar(@rules), $failing, $total;
exit($failing ? 1 : 0);
