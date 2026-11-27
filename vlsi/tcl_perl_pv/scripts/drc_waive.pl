#!/usr/bin/env perl
# drc_waive.pl - apply a waiver list to a DRC summary and say if the block may sign off.
# usage: drc_waive.pl top.drc.summary waivers.txt
# waiver file line:  <rule>  <max_count>  <owner>  <free text reason>      (# starts a comment)
use strict;
use warnings;
use FindBin qw($Bin);
use lib "$Bin/lib";
use PVReport qw(read_summary);

@ARGV == 2 or die "usage: $0 <drc.summary> <waivers.txt>\n";
my ($sum_file, $waive_file) = @ARGV;
my $count = read_summary($sum_file);

my %waiver;                                     # rule => { max, owner, reason }
open(my $fh, '<', $waive_file) or die "cannot open $waive_file: $!\n";
while (my $line = <$fh>) {
    $line =~ s/#.*//;                           # drop comments
    next unless $line =~ /\S/;                  # skip blank lines
    my ($rule, $max, $owner, $reason) = split ' ', $line, 4;
    die "$waive_file line $.: max_count '$max' is not a number\n" unless $max =~ /^\d+$/;
    chomp($reason //= '');
    $waiver{$rule} = { max => $max, owner => $owner, reason => $reason };
}
close $fh;

my @open;
for my $rule (sort keys %$count) {
    my $n = $count->{$rule};
    next if $n == 0;
    my $w = $waiver{$rule};
    if (!$w) {
        push @open, sprintf("%-10s %4d  no waiver", $rule, $n);
    } elsif ($n > $w->{max}) {
        push @open, sprintf("%-10s %4d  waiver covers only %d (%s)", $rule, $n, $w->{max}, $w->{owner});
    } else {
        printf "waived  %-10s %4d  %s\n", $rule, $n, $w->{reason};
    }
}
for my $rule (sort keys %waiver) {              # stale waivers hide future problems
    print "stale   $rule  waiver exists but the rule is clean or not in this run\n"
        unless $count->{$rule};
}
print "\n";
if (@open) {
    print "NOT CLEAN - ", scalar(@open), " rule(s) still open:\n", map { "  $_\n" } @open;
    exit 1;
}
print "CLEAN after waivers\n";
