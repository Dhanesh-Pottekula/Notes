#!/usr/bin/env tclsh
# rdb_to_tcl.tcl - turn an ASCII DRC results database into a small Tcl data file that
# another Tcl tool (Innovus, a layout viewer, another tclsh script) can "source".
# usage: tclsh rdb_to_tcl.tcl top.drc.results viol.tcl ?margin_um?
# The output file sets one variable:
#   set pv_viol { {rule llx lly urx ury} {rule llx lly urx ury} ... }
source [file join [file dirname [info script]] pvlib.tcl]

if {$argc < 2} {
    puts stderr "usage: tclsh rdb_to_tcl.tcl <drc.results> <out.tcl> ?margin_um?"
    exit 2
}
lassign $argv rdb out_file margin
if {$margin eq ""} { set margin 0.5 }

set out [open $out_file w]
puts $out "# made by rdb_to_tcl.tcl from [file tail $rdb]; boxes grown by $margin um"
puts $out "set pv_viol \{"
array set per_rule {}
foreach v [pv::read_rdb $rdb] {
    lassign $v rule type llx lly urx ury
    set box [pv::bbox_expand [list $llx $lly $urx $ury] $margin]
    puts $out [format "  {%s %.3f %.3f %.3f %.3f}" $rule {*}$box]
    if {![info exists per_rule($rule)]} { set per_rule($rule) 0 }
    incr per_rule($rule)
}
puts $out "\}"
close $out

foreach rule [lsort [array names per_rule]] {
    puts [format "%-10s %4d" $rule $per_rule($rule)]
}
puts "wrote $out_file"
