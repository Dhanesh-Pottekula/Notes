# pvlib.tcl - small library of procs shared by the Tcl practice scripts.
# Load it with:   source [file join [file dirname [info script]] pvlib.tcl]
# Written for Tcl 8.5, the oldest Tcl you are likely to meet inside an EDA tool.

namespace eval pv {
    namespace export read_summary read_rdb bbox_area bbox_overlap bbox_expand bbox_union
}

# pv::read_lines file -> list of lines (no trailing newline problems)
proc pv::read_lines {file} {
    set fh [open $file r]
    set text [read $fh]
    close $fh
    return [split [string trimright $text "\n"] "\n"]
}

# pv::read_summary file -> dict  rule -> result count
proc pv::read_summary {file} {
    set counts [dict create]
    set in 0
    foreach line [pv::read_lines $file] {
        if {!$in} {
            if {[regexp {^--- RULECHECK RESULTS STATISTICS\s*$} $line]} { set in 1 }
            continue
        }
        if {[regexp {^-{20,}\s*$} $line]} break
        if {[regexp {^RULECHECK\s+(\S+)\s.*TOTAL Result Count\s*=\s*(\d+)} $line -> rule n]} {
            dict set counts $rule $n
        }
    }
    if {[dict size $counts] == 0} {
        error "$file: no RULECHECK lines found (is this a DRC summary?)"
    }
    return $counts
}

# pv::read_rdb file -> list of {rule type llx lly urx ury}, coordinates in microns
proc pv::read_rdb {file} {
    set lines [pv::read_lines $file]
    lassign [lindex $lines 0] top prec
    if {![string is integer -strict $prec] || $prec <= 0} {
        error "$file: line 1 should be '<topcell> <precision>'"
    }
    set viol {}
    set rule ""
    set prev ""
    set i 1
    set n [llength $lines]
    while {$i < $n} {
        set line [lindex $lines $i]
        incr i
        if {[regexp {^([pe])\s+\d+\s+(\d+)\s*$} $line -> type npts]} {
            set xs {}
            set ys {}
            set left $npts
            while {$left > 0} {
                if {$i >= $n} { error "$file: file ends inside a result of $rule" }
                set pt [lindex $lines $i]
                incr i
                if {[regexp {^\s*[A-Za-z]} $pt]} continue   ;# property line ("CN <cell> ..."): skip
                incr left -1
                foreach {x y} $pt {                     ;# 2 numbers (polygon) or 4 (edge)
                    lappend xs [expr {double($x) / $prec}]
                    lappend ys [expr {double($y) / $prec}]
                }
            }
            set xs [lsort -real $xs]
            set ys [lsort -real $ys]
            lappend viol [list $rule $type [lindex $xs 0] [lindex $ys 0] [lindex $xs end] [lindex $ys end]]
            continue
        }
        if {[regexp {^\d+\s+\d+\s+(\d+)\s+[A-Z][a-z]{2}\s} $line -> ntext]} {
            set rule $prev                   ;# the line before the counts is the rule name
            incr i $ntext                    ;# jump over the rule text lines
            continue
        }
        set prev $line
    }
    return $viol
}

# A bbox is a list {llx lly urx ury}.
proc pv::bbox_area {box} {
    lassign $box llx lly urx ury
    return [expr {($urx - $llx) * ($ury - $lly)}]
}

# 1 if the two boxes overlap or touch
proc pv::bbox_overlap {a b} {
    lassign $a ax1 ay1 ax2 ay2
    lassign $b bx1 by1 bx2 by2
    return [expr {$ax1 <= $bx2 && $bx1 <= $ax2 && $ay1 <= $by2 && $by1 <= $ay2}]
}

# grow a box by "margin" on every side (margin defaults to 1 um)
proc pv::bbox_expand {box {margin 1.0}} {
    lassign $box llx lly urx ury
    return [list [expr {$llx - $margin}] [expr {$lly - $margin}] \
                 [expr {$urx + $margin}] [expr {$ury + $margin}]]
}

# smallest box that covers every box given:  pv::bbox_union $b1 $b2 $b3 ...
proc pv::bbox_union {first args} {
    lassign $first llx lly urx ury
    foreach box $args {
        lassign $box x1 y1 x2 y2
        if {$x1 < $llx} { set llx $x1 }
        if {$y1 < $lly} { set lly $y1 }
        if {$x2 > $urx} { set urx $x2 }
        if {$y2 > $ury} { set ury $y2 }
    }
    return [list $llx $lly $urx $ury]
}
