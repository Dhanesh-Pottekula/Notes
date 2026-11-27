package PVReport;
# Shared readers for Calibre text outputs. Used by drc_compare.pl, drc_waive.pl,
# rdb_bbox.pl and rdb_hotspot.pl, so the parsing lives in ONE place.
use strict;
use warnings;
use List::Util qw(min max);
use Exporter 'import';
our @EXPORT_OK = qw(read_summary read_rdb);

# read_summary("top.drc.summary") -> { rule_name => result_count, ... }
sub read_summary {
    my ($file) = @_;
    open(my $fh, '<', $file) or die "cannot open $file: $!\n";
    my (%count, $in);
    while (my $line = <$fh>) {
        if (!$in) {                               # skip everything before the section
            $in = 1 if $line =~ /^--- RULECHECK RESULTS STATISTICS\s*$/;
            next;
        }
        last if $line =~ /^-{20,}\s*$/;           # the long dashed line ends the section
        $count{$1} = $2
            if $line =~ /^RULECHECK\s+(\S+)\s.*TOTAL Result Count\s*=\s*(\d+)/;
    }
    close $fh;
    die "$file: no RULECHECK lines found (is this a DRC summary?)\n" unless %count;
    return \%count;
}

# read_rdb("top.drc.results") -> ($top_cell, [ {rule, type, bbox=>[llx,lly,urx,ury]}, ... ])
# Coordinates are returned in microns (file integers / precision on line 1).
sub read_rdb {
    my ($file) = @_;
    open(my $fh, '<', $file) or die "cannot open $file: $!\n";
    my $first = <$fh>;
    defined $first or die "$file: empty file\n";
    my ($top, $prec) = split ' ', $first;
    die "$file: line 1 should be '<topcell> <precision>'\n"
        unless defined $prec && $prec =~ /^\d+$/ && $prec > 0;

    my (@viol, $rule, $prev);
    my $skip = 0;                                  # rule-text lines still to skip
    while (my $line = <$fh>) {
        chomp $line;
        if ($skip > 0) { $skip--; next; }
        if ($line =~ /^([pe])\s+(\d+)\s+(\d+)\s*$/) {       # p = polygon, e = edge cluster
            my ($type, $n) = ($1, $3);
            my (@x, @y);
            my $left = $n;
            while ($left > 0) {
                my $pt = <$fh>;
                defined $pt or die "$file: file ends inside a result of $rule\n";
                next if $pt =~ /^\s*[A-Za-z]/;      # property line (for example "CN <cell> ..."): skip
                $left--;
                my @v = split ' ', $pt;            # polygon line: x y   edge line: x1 y1 x2 y2
                while (@v >= 2) {
                    push @x, shift(@v) / $prec;
                    push @y, shift(@v) / $prec;
                }
            }
            push @viol, { rule => $rule, type => $type,
                          bbox => [ min(@x), min(@y), max(@x), max(@y) ] };
            next;
        }
        if ($line =~ /^(\d+)\s+(\d+)\s+(\d+)\s+[A-Z][a-z]{2}\s/) {   # "count count textlines date"
            $rule = $prev;                          # the line just before it was the rule name
            $skip = $3;
            next;
        }
        $prev = $line;
    }
    close $fh;
    return ($top, \@viol);
}

1;
