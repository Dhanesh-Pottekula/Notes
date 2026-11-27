#!/usr/bin/env perl
# rdb_hotspot.pl - where on the chip do the violations cluster?
# Cuts the layout into square windows and counts violations per window.
# usage: rdb_hotspot.pl top.drc.results [window_um]      (default window 10 um)
use strict;
use warnings;
use POSIX qw(floor);
use FindBin qw($Bin);
use lib "$Bin/lib";
use PVReport qw(read_rdb);

my $file = shift or die "usage: $0 <drc.results> [window_um]\n";
my $win  = shift // 10;
$win > 0 or die "window must be > 0\n";
my (undef, $viol) = read_rdb($file);

my %hits;                                       # "col,row" => { rule => count }
for my $v (@$viol) {
    my ($llx, $lly, $urx, $ury) = @{ $v->{bbox} };
    my $col = floor( ($llx + $urx) / 2 / $win );     # window that holds the centre
    my $row = floor( ($lly + $ury) / 2 / $win );
    $hits{"$col,$row"}{ $v->{rule} }++;
}

my %total;
for my $w (keys %hits) {
    $total{$w} += $_ for values %{ $hits{$w} };
}
printf "%-26s %5s  %s\n", 'WINDOW (um)', 'COUNT', 'RULES';
for my $w (sort { $total{$b} <=> $total{$a} || $a cmp $b } keys %total) {
    my ($col, $row) = split /,/, $w;
    my $box = sprintf "(%g %g) (%g %g)", $col * $win, $row * $win, ($col + 1) * $win, ($row + 1) * $win;
    my $rules = join ' ', map { "$_=$hits{$w}{$_}" } sort keys %{ $hits{$w} };
    printf "%-26s %5d  %s\n", $box, $total{$w}, $rules;
}
