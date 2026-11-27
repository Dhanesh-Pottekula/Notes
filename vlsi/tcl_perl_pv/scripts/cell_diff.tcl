#!/usr/bin/env tclsh
# cell_diff.tcl - which names are in list A but not in list B, and the other way round?
# Typical use: cells in the merged GDS vs cells that have a LEF or a CDL view.
# usage: tclsh cell_diff.tcl a.txt b.txt        (one name per line)

if {$argc != 2} {
    puts stderr "usage: tclsh cell_diff.tcl <a.txt> <b.txt>"
    exit 2
}

proc read_names {file} {
    set fh [open $file r]
    set names {}
    foreach line [split [read $fh] "\n"] {
        set name [string trim $line]
        if {$name ne "" && [string index $name 0] ne "#"} { lappend names $name }
    }
    close $fh
    return [lsort -unique $names]
}

# names in $a that are not in $b. An array lookup is fast even for a million cells;
# lsearch inside a loop would be far too slow at that size.
proc only_in {a b} {
    foreach name $b { set seen($name) 1 }
    set out {}
    foreach name $a {
        if {![info exists seen($name)]} { lappend out $name }
    }
    return $out
}

lassign $argv file_a file_b
set a [read_names $file_a]
set b [read_names $file_b]
set only_a [only_in $a $b]
set only_b [only_in $b $a]

puts "[llength $a] names in $file_a, [llength $b] in $file_b"
puts "only in [file tail $file_a] ([llength $only_a]): $only_a"
puts "only in [file tail $file_b] ([llength $only_b]): $only_b"
exit [expr {[llength $only_a] + [llength $only_b] > 0}]
