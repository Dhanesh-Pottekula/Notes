#!/usr/bin/env perl
# lvs_triage.pl - first look at a Calibre LVS report: verdict, error lines, bad cells, count mismatches.
# usage: lvs_triage.pl top.lvs.report
use strict;
use warnings;

my $file = shift or die "usage: $0 <lvs.report>\n";
open(my $fh, '<', $file) or die "cannot open $file: $!\n";

my ($verdict, @errors, @warnings, @bad_cells, @mismatch, $cells_ok);
my $section = '';
while (my $line = <$fh>) {
    chomp $line;
    $section = 'cells'  if $line =~ /CELL\s+SUMMARY/;
    $section = 'counts' if $line =~ /NUMBERS OF OBJECTS/;

    # the verdict is the word inside the box of # signs
    $verdict //= $1 if $line =~ /#\s+(CORRECT|INCORRECT|NOT COMPARED)\s+#/;

    push @errors,   $1 if $line =~ /^\s*Error:\s+(.*\S)/;
    push @warnings, $1 if $line =~ /^\s*Warning:\s+(.*\S)/;

    if ($section eq 'cells' && $line =~ /^\s+(CORRECT|INCORRECT)\s+(\S+)\s+(\S+)/) {
        if ($1 eq 'INCORRECT') { push @bad_cells, "$2 (source $3)" } else { $cells_ok++ }
    }
    # a count line with a trailing star means layout and source disagree
    if ($section eq 'counts' && $line =~ /^\s*([A-Za-z ]+?):\s+(\d+)\s+(\d+)\s+\*/) {
        push @mismatch, sprintf("%-10s layout %d, source %d (diff %+d)", $1, $2, $3, $2 - $3);
    }
}
close $fh;

print "LVS verdict : ", ($verdict // 'not found in report'), "\n";
print "errors      : ", scalar(@errors), "\n", map { "  - $_\n" } @errors;
print "warnings    : ", scalar(@warnings), "\n", map { "  - $_\n" } @warnings;
print "cells       : ", ($cells_ok // 0), " correct, ", scalar(@bad_cells), " incorrect\n",
      map { "  - $_\n" } @bad_cells;
print "count diffs : ", scalar(@mismatch), "\n", map { "  - $_\n" } @mismatch;
print "\nstart with the lowest incorrect cell in the hierarchy: fixing a leaf often fixes its parents\n"
    if @bad_cells > 1;
exit(defined $verdict && $verdict eq 'CORRECT' ? 0 : 1);
