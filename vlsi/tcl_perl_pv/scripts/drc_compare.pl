#!/usr/bin/env perl
# drc_compare.pl - what changed between two DRC runs (yesterday vs today)?
# usage: drc_compare.pl old.drc.summary new.drc.summary
use strict;
use warnings;
use FindBin qw($Bin);
use lib "$Bin/lib";
use PVReport qw(read_summary);

@ARGV == 2 or die "usage: $0 <old.summary> <new.summary>\n";
my ($old, $new) = map { read_summary($_) } @ARGV;

my %seen;
my @rules = grep { !$seen{$_}++ } (keys %$old, keys %$new);     # union of both rule lists

my %bucket;      # status => [ lines ]
for my $r (sort @rules) {
    my $o = $old->{$r};
    my $n = $new->{$r};
    my $status =
        !defined $o        ? 'NEW RULE'
      : !defined $n        ? 'RULE GONE'
      : $o == 0 && $n > 0  ? 'NEW FAIL'
      : $o > 0 && $n == 0  ? 'FIXED'
      : $n > $o            ? 'WORSE'
      : $n < $o            ? 'BETTER'
      :                      'SAME';
    next if $status eq 'SAME' && ($n // 0) == 0;                # clean before, clean now
    push @{ $bucket{$status} },
        sprintf("  %-12s %5s -> %-5s", $r, $o // '-', $n // '-');
}

for my $status ('NEW FAIL', 'WORSE', 'NEW RULE', 'RULE GONE', 'SAME', 'BETTER', 'FIXED') {
    next unless $bucket{$status};
    print "$status\n", map { "$_\n" } @{ $bucket{$status} };
}
