#!/usr/bin/env tclsh
# pvlib_test.tcl - quick self-test of the box procs. Run it after every change to pvlib.tcl.
source [file join [file dirname [info script]] pvlib.tcl]

set pass 0
set fail 0
proc check {what got want} {
    global pass fail
    if {$got eq $want} {
        incr pass
    } else {
        incr fail
        puts "FAIL $what: got '$got', wanted '$want'"
    }
}

check "area"            [pv::bbox_area {0 0 2 3}]                 6
check "overlap yes"     [pv::bbox_overlap {0 0 2 2} {1 1 3 3}]     1
check "overlap touch"   [pv::bbox_overlap {0 0 2 2} {2 0 4 2}]     1
check "overlap no"      [pv::bbox_overlap {0 0 2 2} {3 3 4 4}]     0
check "expand default"  [pv::bbox_expand {1 1 2 2}]                {0.0 0.0 3.0 3.0}
check "expand 0.5"      [pv::bbox_expand {1 1 2 2} 0.5]            {0.5 0.5 2.5 2.5}
check "union"           [pv::bbox_union {0 0 1 1} {5 5 6 6} {-1 2 0 3}]  {-1 0 6 6}

puts "$pass passed, $fail failed"
exit [expr {$fail > 0}]
