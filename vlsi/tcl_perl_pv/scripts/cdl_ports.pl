#!/usr/bin/env perl
# cdl_ports.pl - compare the pin list of every .SUBCKT in two SPICE/CDL netlists.
# Catches the classic LVS starters: missing pins, extra pins, swapped pin order, missing cells.
# usage: cdl_ports.pl source.cdl layout.cdl
use strict;
use warnings;

@ARGV == 2 or die "usage: $0 <source.cdl> <layout.cdl>\n";

sub read_subckts {
    my ($file) = @_;
    open(my $fh, '<', $file) or die "cannot open $file: $!\n";
    my (@joined, %pins);
    while (my $line = <$fh>) {
        chomp $line;
        next if $line =~ /^\s*\*/ || $line !~ /\S/;     # comment or blank
        if ($line =~ s/^\s*\+\s*//) {                    # "+" continues the previous line
            $joined[-1] .= " $line" if @joined;
        } else {
            push @joined, $line;
        }
    }
    close $fh;
    for my $line (@joined) {
        next unless $line =~ /^\s*\.subckt\s+(\S+)\s*(.*)/i;
        my ($name, $rest) = (lc $1, $2);
        $pins{$name} = [ grep { !/=/ } split ' ', $rest ];   # drop "param=value" items
    }
    return \%pins;
}

my ($src, $lay) = map { read_subckts($_) } @ARGV;
my $problems = 0;
for my $cell (sort keys %$src) {
    if (!$lay->{$cell}) { print "$cell: missing in layout netlist\n"; $problems++; next; }
    my @s = @{ $src->{$cell} };
    my @l = @{ $lay->{$cell} };
    my %in_s = map { $_ => 1 } @s;
    my %in_l = map { $_ => 1 } @l;
    my @only_s = grep { !$in_l{$_} } @s;
    my @only_l = grep { !$in_s{$_} } @l;
    if (@only_s || @only_l) {
        print "$cell: pins only in source: @only_s\n" if @only_s;
        print "$cell: pins only in layout: @only_l\n" if @only_l;
        $problems++;
    } elsif ("@s" ne "@l") {
        print "$cell: same pins, different order\n  source: @s\n  layout: @l\n";
        $problems++;
    }
}
for my $cell (sort grep { !$src->{$_} } keys %$lay) {
    print "$cell: only in layout netlist (filler or physical-only cell?)\n";
}
print "\n", ($problems ? "$problems cell(s) need a look\n" : "all shared cells have matching pins\n");
exit($problems ? 1 : 0);
