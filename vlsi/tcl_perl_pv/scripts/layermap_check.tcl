#!/usr/bin/env tclsh
# layermap_check.tcl - sanity check a layer map before stream-out or a merge.
#   1. two different layers mapped to the same GDS layer/datatype  (shapes get merged: false shorts)
#   2. a required layer that has no line in the map                (shapes get dropped: opens, missing layer)
# usage: tclsh layermap_check.tcl layer.map required_layers.txt
# map line:  <name> <purpose> <gds_layer> <gds_datatype>

if {$argc != 2} {
    puts stderr "usage: tclsh layermap_check.tcl <layer.map> <required_layers.txt>"
    exit 2
}
lassign $argv map_file req_file

proc data_lines {file} {
    set fh [open $file r]
    set out {}
    set n 0
    while {[gets $fh line] >= 0} {
        incr n
        regsub {#.*} $line {} line
        if {[string trim $line] ne ""} { lappend out [list $n $line] }
    }
    close $fh
    return $out
}

array set by_gds {}       ;# "31/0"        -> list of "M1:drawing (line 2)"
array set mapped {}       ;# "M1 drawing"  -> 1
set problems 0
foreach item [data_lines $map_file] {
    lassign $item n line
    if {[llength $line] != 4} {
        puts "line $n: expected 4 fields, got [llength $line]: $line"
        incr problems
        continue
    }
    lassign $line name purpose layer dtype
    lappend by_gds($layer/$dtype) "$name:$purpose (line $n)"
    set mapped([list $name $purpose]) 1
}

foreach key [lsort -dictionary [array names by_gds]] {
    if {[llength $by_gds($key)] > 1} {
        puts "GDS $key is used [llength $by_gds($key)] times: [join $by_gds($key) {, }]"
        incr problems
    }
}
foreach item [data_lines $req_file] {
    lassign [lindex $item 1] name purpose
    if {![info exists mapped([list $name $purpose])]} {
        puts "required layer $name:$purpose is not in the map"
        incr problems
    }
}
puts [expr {$problems ? "$problems problem(s) found" : "layer map looks consistent"}]
exit [expr {$problems > 0}]
