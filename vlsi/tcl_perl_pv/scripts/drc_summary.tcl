#!/usr/bin/env tclsh
# drc_summary.tcl - the Tcl twin of drc_summary.pl: failing rules of a DRC summary, worst first.
# usage: tclsh drc_summary.tcl top.drc.summary
source [file join [file dirname [info script]] pvlib.tcl]

if {$argc < 1} {
    puts stderr "usage: tclsh drc_summary.tcl <drc.summary>"
    exit 2
}
set file [lindex $argv 0]
if {[catch {pv::read_summary $file} counts]} {
    puts stderr "error: $counts"
    exit 2
}

# dict -> list of {rule count} pairs, so lsort can sort on the count column
set pairs {}
dict for {rule n} $counts { lappend pairs [list $rule $n] }
set pairs [lsort -index 0 $pairs]                          ;# first by name ...
set pairs [lsort -integer -decreasing -index 1 $pairs]     ;# ... then by count (lsort is stable)

set total 0
set failing 0
puts [format "%-14s %8s" RULE RESULTS]
foreach pair $pairs {
    lassign $pair rule n
    incr total $n
    if {$n > 0} {
        incr failing
        puts [format "%-14s %8d" $rule $n]
    }
}
puts ""
puts "[llength $pairs] rules checked, $failing failing, $total results in total"
exit [expr {$failing > 0}]
