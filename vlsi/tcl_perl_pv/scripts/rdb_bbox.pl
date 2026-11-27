#!/usr/bin/env perl
# rdb_bbox.pl - turn an ASCII DRC results database into one CSV line per violation.
# usage: rdb_bbox.pl top.drc.results [rule_regex]  > violations.csv
use strict;
use warnings;
use FindBin qw($Bin);
use lib "$Bin/lib";
use PVReport qw(read_rdb);

my $file = shift or die "usage: $0 <drc.results> [rule_regex]\n";
my $want = shift // '.';                       # default: every rule
my ($top, $viol) = read_rdb($file);

print "rule,type,llx,lly,urx,ury,width,height\n";
for my $v (@$viol) {
    next unless $v->{rule} =~ /$want/;
    my ($llx, $lly, $urx, $ury) = @{ $v->{bbox} };
    printf "%s,%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n",
        $v->{rule}, $v->{type}, $llx, $lly, $urx, $ury, $urx - $llx, $ury - $lly;
}
warn sprintf("%s: %d violations read from top cell %s\n", $file, scalar(@$viol), $top);
